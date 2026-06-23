#!/usr/bin/env python3
"""
ingest_web_to_research.py - 把网络文章自动捕获到 tkk-library 的 discovered-in-research/

E2E 流程:
  [1] 抓 HTML(主路径: web-access/CDP Proxy at localhost:3456)
  [2] HTML → Markdown(主路径: html2md.py + markdownify)
  [3] 写 discovered-in-research/{task_id}/SRC-NNN__标题.md(主路径: markdown_converter.py)
  [4] 增量更新 INDEX.md + research_log.md(markdown_converter 内部)

主路径哲学(per feedback-no-design-degradation-2026-06-22):
  - 不预埋 urllib 降级
  - 不预埋 html.parser 降级
  - 缺依赖/CDP 不通 → loudly 报错 + 修复指引,不静默降级

依赖:
  - web-access skill(cdp-proxy.mjs 跑在 localhost:3456)
  - html2md.py(本目录)
  - markdown_converter.py(本目录)
  - markdownify(pip)

启动前置:
  1. Chrome 开 remote-debugging
  2. node ~/.claude/skills/web-access/scripts/cdp-proxy.mjs &
"""

import argparse
import json
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path
from typing import Optional

# 同目录依赖
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

# 主路径依赖(本目录其他脚本)
try:
    import markdown_converter
except ImportError as e:
    print(
        "[FAIL] 缺依赖 markdown_converter.py\n"
        "       原因: scripts/markdown_converter.py 不可导入\n"
        "       修复: 确保 /home/kangkang/tkk-library/scripts/ 在 sys.path\n"
        f"       原始错误: {e}",
        file=sys.stderr,
    )
    sys.exit(2)

# html2md.py 通过 subprocess 调用(避免 Python 进程内 import markdownify 冲突)

CDP_BASE_URL = "http://localhost:3456"


# ---------------------------------------------------------------------------
# Step 1: 抓 HTML(主路径 = web-access/CDP,失败 loudly 报错)
# ---------------------------------------------------------------------------

def check_cdp_alive() -> bool:
    """检查 CDP Proxy 是否在 :3456 监听。"""
    try:
        result = subprocess.run(
            ["curl", "-s", "-f", "--max-time", "3", f"{CDP_BASE_URL}/health"],
            capture_output=True, text=True, timeout=5,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return False


def fetch_html_via_cdp(url: str, wait_ms: int = 2000) -> str:
    """
    通过 web-access CDP Proxy 抓取 URL 的 HTML。
    流程: /new?url=URL → /eval document.documentElement.outerHTML → /close

    主路径(per feedback-no-design-degradation-2026-06-22):
    - 不预埋 urllib 降级
    - CDP 不通/Chrome 未开 → sys.exit(3) + 修复指引
    """
    # 1. 健康检查
    if not check_cdp_alive():
        print(
            "[FAIL] web-access CDP Proxy 未在 :3456 监听\n"
            "       原因: Chrome 未启 remote-debugging 或 cdp-proxy.mjs 未跑\n"
            "       修复 1: Chrome 地址栏打开 chrome://inspect/#remote-debugging\n"
            "              勾选 'Allow remote debugging for this browser instance'\n"
            "       修复 2: 跑 `node ~/.claude/skills/web-access/scripts/cdp-proxy.mjs &`\n"
            "       修复 3: 验证 `curl -s http://localhost:3456/health` 应返回 200\n"
            f"       当前 URL: {url}",
            file=sys.stderr,
        )
        sys.exit(3)

    # 2. 新建 tab
    new_url = f"{CDP_BASE_URL}/new?url={urllib.parse.quote(url, safe='')}"
    result = subprocess.run(
        ["curl", "-s", "-f", "--max-time", "30", new_url],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(
            f"[FAIL] CDP /new 失败: HTTP 错误或超时\n"
            f"       curl exit: {result.returncode}\n"
            f"       stderr: {result.stderr.strip()[:200]}\n"
            f"       修复: 检查 Chrome 远程调试端口 + CDP Proxy 日志",
            file=sys.stderr,
        )
        sys.exit(4)
    try:
        new_resp = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(
            f"[FAIL] CDP /new 返回非 JSON: {result.stdout[:200]}\n"
            f"       解析错误: {e}",
            file=sys.stderr,
        )
        sys.exit(4)
    target_id = new_resp.get("targetId")
    if not target_id:
        print(f"[FAIL] CDP /new 响应无 targetId: {new_resp}", file=sys.stderr)
        sys.exit(4)

    # 3. 等待页面渲染
    if wait_ms > 0:
        import time
        time.sleep(wait_ms / 1000.0)

    # 4. eval 拿 HTML
    eval_url = f"{CDP_BASE_URL}/eval?target={target_id}"
    result = subprocess.run(
        ["curl", "-s", "-f", "-X", "POST", "--max-time", "15",
         "-H", "Content-Type: text/plain",
         "-d", "document.documentElement.outerHTML",
         eval_url],
        capture_output=True, text=True,
    )
    html_content = result.stdout

    # 5. 关闭 tab
    close_url = f"{CDP_BASE_URL}/close?target={target_id}"
    subprocess.run(
        ["curl", "-s", "-f", "--max-time", "5", close_url],
        capture_output=True, text=True,
    )

    if not html_content.strip():
        print(
            f"[FAIL] CDP /eval 返回空 HTML\n"
            f"       target: {target_id}\n"
            f"       修复: 检查目标页面是否需要登录/反爬",
            file=sys.stderr,
        )
        sys.exit(4)
    return html_content


# ---------------------------------------------------------------------------
# Step 2: HTML → Markdown(主路径 = html2md.py subprocess)
# ---------------------------------------------------------------------------

def convert_html_to_md_via_subprocess(html_file: Path, output_md: Path, meta: dict) -> Path:
    """调 html2md.py 转 markdown(主路径)。

    meta 参数: 当前为兼容性保留,但**不应再传**(避免与 markdown_converter 的
    schema frontmatter 重复)。E2E 流程下 frontmatter 由 markdown_converter 统一加。
    """
    if not (SCRIPT_DIR / "html2md.py").exists():
        print(
            f"[FAIL] html2md.py 不存在: {SCRIPT_DIR / 'html2md.py'}\n"
            f"       修复: 从 tkk-skills/scripts/ 复制 html2md.py 到此目录",
            file=sys.stderr,
        )
        sys.exit(2)
    args = ["python3", str(SCRIPT_DIR / "html2md.py"), str(html_file), "-o", str(output_md)]
    for k, v in meta.items():
        args.extend(["--meta", f"{k}={v}"])
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(
            f"[FAIL] html2md.py 转换失败(exit {result.returncode})\n"
            f"       stderr: {result.stderr[:500]}",
            file=sys.stderr,
        )
        sys.exit(5)
    if not output_md.exists():
        print(f"[FAIL] html2md.py 未产出 {output_md}", file=sys.stderr)
        sys.exit(5)
    return output_md


# ---------------------------------------------------------------------------
# Step 3: 写 discovered-in-research/(主路径 = markdown_converter.write_research_source)
# ---------------------------------------------------------------------------

def write_to_research(
    task_id: str,
    title: str,
    body_md: str,
    origin_url: str,
    publish_date: Optional[str],
    tier: str,
    keywords: list,
    search_engine: str,
    platform: str,
    vault_root: Path,
) -> Path:
    """调 markdown_converter.write_research_source 写入 SRC-NNN__标题.md。"""
    out_file = markdown_converter.write_research_source(
        vault_root=vault_root,
        task_id=task_id,
        title=title,
        body_md=body_md,
        origin_url=origin_url,
        publish_date=publish_date,
        tier=tier,
        keywords=keywords,
        search_engine=search_engine,
        platform=platform,
    )
    return out_file


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="把网络文章自动捕获到 tkk-library 的 discovered-in-research/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 主路径: 通过 web-access/CDP 抓 URL → 转 md → 写入 discovered-in-research
  python ingest_web_to_research.py \\
    --url https://www.bjnews.com.cn/detail/123456 \\
    --task-id tkk-discover/2026-06-22-测试主题 \\
    --title "新京报原文标题" \\
    --tier T1 \\
    --keywords 测试 关键词 \\
    --platform 新京报官网

  # 备模式: 已下载的 HTML 文件 → 转 md → 写入
  python ingest_web_to_research.py \\
    --html-file /tmp/article.html \\
    --task-id tkk-discover/2026-06-22-测试 \\
    --title "..." \\
    --origin-url "https://..."
        """,
    )
    parser.add_argument("--url",
                        help="目标 URL(主路径:web-access/CDP 抓取,CDP 不通报错)")
    parser.add_argument("--html-file",
                        help="已下载的 HTML 文件路径(备模式:不调 CDP,直接转 md)")
    parser.add_argument("--task-id", required=True,
                        help="任务 ID,如 tkk-discover/2026-06-22-主题名")
    parser.add_argument("--title", required=True, help="文章标题")
    parser.add_argument("--origin-url", help="原始 URL(若 --html-file 模式未传则必填)")
    parser.add_argument("--publish-date", help="原始发布日期 (YYYY-MM-DD)")
    parser.add_argument("--tier", default="T3", choices=["T1", "T2", "T3", "T4"])
    parser.add_argument("--keywords", nargs="+", default=[],
                        help="检索关键词(空格分隔)")
    parser.add_argument("--platform", default="N/A",
                        help="平台(如 新京报官网/澎湃新闻)")
    parser.add_argument("--search-engine", default="N/A",
                        help="搜索引擎(若 web-access 抓则记录)")
    parser.add_argument("--vault-root", default=None,
                        help="vault 根目录(默认 /home/kangkang/tkk-library)")
    parser.add_argument("--wait-ms", type=int, default=2000,
                        help="CDP 抓取后等待渲染时间(毫秒,默认 2000)")
    args = parser.parse_args()

    # 输入校验
    if not args.url and not args.html_file:
        print("[FAIL] --url 或 --html-file 必传其一", file=sys.stderr)
        sys.exit(1)
    if args.url and args.html_file:
        print("[FAIL] --url 和 --html-file 互斥,只传一个", file=sys.stderr)
        sys.exit(1)
    origin_url = args.origin_url or args.url
    if not origin_url:
        print("[FAIL] --origin-url 必填(在 --html-file 模式下)", file=sys.stderr)
        sys.exit(1)

    vault_root = Path(args.vault_root) if args.vault_root else Path("/home/kangkang/tkk-library")
    if not vault_root.exists():
        print(f"[FAIL] vault 根目录不存在: {vault_root}", file=sys.stderr)
        sys.exit(1)

    # Step 1: 抓 HTML
    if args.html_file:
        html_path = Path(args.html_file)
        if not html_path.exists():
            print(f"[FAIL] --html-file 不存在: {html_path}", file=sys.stderr)
            sys.exit(1)
        html_content = html_path.read_text(encoding="utf-8")
        print(f"[1/3] 读 HTML 文件: {html_path} ({len(html_content)} bytes)", file=sys.stderr)
    else:
        print(f"[1/3] CDP 抓取 {args.url} ...", file=sys.stderr)
        html_content = fetch_html_via_cdp(args.url, wait_ms=args.wait_ms)
        print(f"     拿到 HTML: {len(html_content)} bytes", file=sys.stderr)

    # 临时存 HTML(供 html2md.py 读)
    tmp_html = Path("/tmp") / f"_ingest_{Path(args.task_id).name}.html"
    tmp_html.write_text(html_content, encoding="utf-8")
    tmp_md = Path("/tmp") / f"_ingest_{Path(args.task_id).name}.md"

    # Step 2: HTML → Markdown
    # 注意: 不传 --meta 给 html2md.py,因为 markdown_converter.py 会加完整 schema frontmatter
    # (含 source_id / file_hash_sha256 / task_id 等),避免双层 frontmatter
    print(f"[2/3] HTML → Markdown(主路径:html2md.py + markdownify)...", file=sys.stderr)
    convert_html_to_md_via_subprocess(tmp_html, tmp_md, meta={})
    body_md = tmp_md.read_text(encoding="utf-8")
    print(f"     Markdown 产出: {len(body_md)} bytes", file=sys.stderr)

    # 清理临时文件
    tmp_html.unlink(missing_ok=True)
    tmp_md.unlink(missing_ok=True)

    # Step 3: 写 discovered-in-research/
    print(f"[3/3] 写入 discovered-in-research/{Path(args.task_id).name}/...", file=sys.stderr)
    out_file = write_to_research(
        task_id=args.task_id,
        title=args.title,
        body_md=body_md,
        origin_url=origin_url,
        publish_date=args.publish_date,
        tier=args.tier,
        keywords=args.keywords,
        search_engine=args.search_engine,
        platform=args.platform,
        vault_root=vault_root,
    )
    print(f"[OK] 写入成功: {out_file}", file=sys.stderr)
    print(f"     source_id: {out_file.name.split('__')[0]}", file=sys.stderr)
    print(f"     tier: {args.tier}", file=sys.stderr)
    print(f"     authenticity_status: pending(等待人工核验)", file=sys.stderr)


if __name__ == "__main__":
    main()
