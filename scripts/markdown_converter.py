#!/usr/bin/env python3
"""
markdown_converter.py - 写入 sources/discovered-in-research/ 的工具脚本

职责：
  1. 接收已转换的 Markdown 内容 + 元数据
  2. 自动添加 frontmatter（按 tkk-legal-ingest v2.0 schema）
  3. 写入 sources/discovered-in-research/{task_id}/SRC-NNN__标题.md
  4. 增量更新 INDEX.md + research_log.md
  5. file_hash_sha256 自动计算

输入方式：
  - CLI 参数（最常用）
  - Python API（脚本调用）

依赖：仅 Python 3.7+ 标准库（不依赖第三方库）。
"""

import argparse
import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# 默认 vault 根目录
DEFAULT_VAULT_ROOT = Path(r"D:\AI agent\tkk-library")


def compute_sha256(content: str) -> str:
    """计算内容 SHA-256 哈希"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def meta_to_yaml(meta: dict, indent: int = 0) -> str:
    """简单 dict → YAML 字符串（支持嵌套 dict + 列表）"""
    lines = []
    prefix = "  " * indent
    for k, v in meta.items():
        if isinstance(v, dict):
            lines.append(f"{prefix}{k}:")
            sub = meta_to_yaml(v, indent + 1)
            lines.append(sub)
        elif isinstance(v, list):
            if not v:
                lines.append(f"{prefix}{k}: []")
            else:
                lines.append(f"{prefix}{k}:")
                for item in v:
                    lines.append(f"{prefix}  - {item}")
        elif v is None:
            lines.append(f"{prefix}{k}: null")
        elif isinstance(v, str) and (":" in v or "#" in v or v.startswith("-") or v.startswith("'") or v.startswith('"')):
            escaped = v.replace('"', '\\"')
            lines.append(f'{prefix}{k}: "{escaped}"')
        else:
            lines.append(f"{prefix}{k}: {v}")
    return "\n".join(lines)


def build_full_markdown(meta: dict, body_md: str) -> str:
    """构建完整 .md 文件（frontmatter + 正文）"""
    yaml_content = meta_to_yaml(meta)
    return f"---\n{yaml_content}\n---\n\n{body_md.rstrip()}\n"


def get_next_src_id(task_dir: Path) -> str:
    """获取下一个 SRC-NNN 编号（按现有文件递增）"""
    existing = list(task_dir.glob("SRC-*__*.md"))
    if not existing:
        return "SRC-001"
    nums = []
    for f in existing:
        m = re.match(r"SRC-(\d+)__", f.name)
        if m:
            nums.append(int(m.group(1)))
    next_num = max(nums) + 1 if nums else 1
    return f"SRC-{next_num:03d}"


def sanitize_filename(name: str) -> str:
    """清理文件名非法字符"""
    return re.sub(r'[\\/:*?"<>|\r\n]', '_', name).strip()


def extract_domain(url: str) -> str:
    """从 URL 提取域名"""
    m = re.match(r"https?://([^/]+)", url)
    return m.group(1) if m else ""


def write_research_log(task_dir: Path, entry: dict):
    """追加一条 research_log.md 记录"""
    log_file = task_dir / "research_log.md"
    if not log_file.exists():
        log_file.write_text(
            f"# 研究检索方案日志 · {task_dir.name}\n\n本日志由 `scripts/markdown_converter.py` 自动追加。\n\n",
            encoding="utf-8"
        )

    timestamp = entry.get("query_time", datetime.now().isoformat(timespec="seconds"))
    keywords_str = "、".join(entry.get("keywords", [])) or "（无）"
    log_entry = (
        f"\n## 会话 · {timestamp}\n\n"
        f"- 触发：{entry.get('trigger', 'tkk-discover 环节 3 web-access 检索')}\n"
        f"- 关键词：{keywords_str}\n"
        f"- 搜索引擎：{entry.get('search_engine', 'N/A')}\n"
        f"- 平台：{entry.get('platform', 'N/A')}\n"
        f"- 命中：{entry.get('hits', 1)} 条权威资料\n"
        f"- 操作：自动捕获 → `sources/discovered-in-research/{task_dir.name}/`\n\n"
    )
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)


def update_task_index(task_dir: Path, row: dict):
    """在任务 INDEX.md 表格中追加一行（带去重保护）"""
    index_file = task_dir / "INDEX.md"
    if not index_file.exists():
        return
    content = index_file.read_text(encoding="utf-8")

    # 去重保护：若 source_id 已存在，跳过（避免重复插入）
    if f"| {row['source_id']} |" in content:
        return

    new_row = (
        f"| {row['source_id']} "
        f"| {row['title']} "
        f"| {row['tier']} "
        f"| {row['origin_url']} "
        f"| {row['authenticity']} "
        f"| {row.get('ingested_to_wiki', '—')} |"
    )
    # 用正则匹配占位行（无论占位行有多少 `|`，只要以"（暂无记录"开头即可）
    placeholder_pattern = re.compile(r"^\| （暂无记录.*$", re.MULTILINE)
    if placeholder_pattern.search(content):
        content = placeholder_pattern.sub(new_row, content, count=1)
    else:
        # 占位行已被替换过 → 在表头分隔线之后插入新行
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("|---") or line.startswith("| ---"):
                lines.insert(i + 1, new_row)
                break
        content = "\n".join(lines)
    # 更新时间戳
    content = re.sub(
        r"updated_at: \d{4}-\d{2}-\d{2}",
        f"updated_at: {datetime.now().strftime('%Y-%m-%d')}",
        content
    )
    index_file.write_text(content, encoding="utf-8")


def write_research_source(
    vault_root: Path,
    task_id: str,
    title: str,
    body_md: str,
    origin_url: str,
    publish_date: Optional[str] = None,
    tier: str = "T3",
    keywords: Optional[list] = None,
    search_engine: Optional[str] = None,
    platform: Optional[str] = None,
    research_phase: str = "环节3-深度挖掘",
    quality_authority: int = 3,
    quality_timeliness: int = 3,
    quality_relevance: int = 3,
    tags: Optional[list] = None,
) -> Path:
    """
    写入一份原始资料到 sources/discovered-in-research/{task_id}/

    返回写入的文件路径。
    """
    keywords = keywords or []
    tags = tags or []

    # 任务子目录
    task_id_short = task_id.split("/")[-1]
    task_dir = vault_root / "sources" / "discovered-in-research" / task_id_short
    task_dir.mkdir(parents=True, exist_ok=True)

    # 编号
    src_id = get_next_src_id(task_dir)
    file_hash = compute_sha256(body_md)
    now_iso = datetime.now().isoformat(timespec="seconds")

    # 构建 frontmatter
    meta = {
        "source_id": src_id,
        "file_hash_sha256": file_hash,
        "task_id": task_id,
        "task_type": "tkk-discover",
        "research_phase": research_phase,
        "discovery_method": "web-access/CDP",
        "search_strategy": {
            "keywords": keywords,
            "search_engine": search_engine or "N/A",
            "platform": platform or "N/A",
            "query_time": now_iso,
        },
        "origin_url": origin_url,
        "origin_domain": extract_domain(origin_url),
        "publish_date": publish_date or "",
        "tier": tier,
        "authenticity_status": "pending",
        "cross_verified": False,
        "quality": {
            "authority": quality_authority,
            "timeliness": quality_timeliness,
            "relevance": quality_relevance,
        },
        "referenced_by_wiki": [],
        "tags": tags,
    }

    # 写文件
    safe_title = sanitize_filename(title)
    out_file = task_dir / f"{src_id}__{safe_title}.md"
    out_content = build_full_markdown(meta, body_md)
    out_file.write_text(out_content, encoding="utf-8")

    # 写 research_log
    write_research_log(task_dir, {
        "query_time": now_iso,
        "keywords": keywords,
        "search_engine": search_engine,
        "platform": platform,
        "hits": 1,
    })

    # 更新 INDEX.md
    update_task_index(task_dir, {
        "source_id": src_id,
        "title": title,
        "tier": tier,
        "origin_url": origin_url,
        "authenticity": "pending",
        "ingested_to_wiki": "—",
    })

    return out_file


def main():
    parser = argparse.ArgumentParser(
        description="写入 sources/discovered-in-research/ 原始资料（tkk-legal-ingest v2.0）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python markdown_converter.py ^
    --task-id tkk-discover/2026-06-12-中医号脉直播课骗局 ^
    --title 新京报原文 ^
    --body-file ./temp/new_jing_bao.md ^
    --origin-url https://www.bjnews.com.cn/detail/... ^
    --publish-date 2026-06-12 ^
    --tier T1 ^
    --keywords 中医号脉 直播课 新京报 ^
    --search-engine Baidu ^
    --platform 新京报官网
        """,
    )
    parser.add_argument("--vault-root", default=str(DEFAULT_VAULT_ROOT))
    parser.add_argument("--task-id", required=True,
                        help="任务 ID，如 tkk-discover/2026-06-12-中医号脉直播课骗局")
    parser.add_argument("--title", required=True, help="资料标题")
    parser.add_argument("--body-file", required=True,
                        help="已转换的 Markdown 正文文件路径")
    parser.add_argument("--origin-url", required=True, help="原始 URL")
    parser.add_argument("--publish-date", help="原始发布日期 (YYYY-MM-DD)")
    parser.add_argument("--tier", default="T3", choices=["T1", "T2", "T3", "T4"])
    parser.add_argument("--keywords", nargs="+", default=[],
                        help="检索关键词（空格分隔）")
    parser.add_argument("--search-engine", help="搜索引擎")
    parser.add_argument("--platform", help="平台")
    parser.add_argument("--research-phase", default="环节3-深度挖掘")
    parser.add_argument("--quality-authority", type=int, default=4, choices=range(1, 6))
    parser.add_argument("--quality-timeliness", type=int, default=5, choices=range(1, 6))
    parser.add_argument("--quality-relevance", type=int, default=5, choices=range(1, 6))
    parser.add_argument("--tags", nargs="+", default=[])

    args = parser.parse_args()

    vault_root = Path(args.vault_root)
    if not vault_root.exists():
        print(f"[!] vault 根目录不存在: {vault_root}", file=sys.stderr)
        sys.exit(1)

    body_path = Path(args.body_file)
    if not body_path.exists():
        print(f"[!] 正文文件不存在: {body_path}", file=sys.stderr)
        sys.exit(1)
    body_md = body_path.read_text(encoding="utf-8")

    out_file = write_research_source(
        vault_root=vault_root,
        task_id=args.task_id,
        title=args.title,
        body_md=body_md,
        origin_url=args.origin_url,
        publish_date=args.publish_date,
        tier=args.tier,
        keywords=args.keywords,
        search_engine=args.search_engine,
        platform=args.platform,
        research_phase=args.research_phase,
        quality_authority=args.quality_authority,
        quality_timeliness=args.quality_timeliness,
        quality_relevance=args.quality_relevance,
        tags=args.tags,
    )

    print(f"[OK] 写入成功: {out_file}")
    print(f"    source_id: {out_file.name.split('__')[0]}")
    print(f"    tier: {args.tier}")
    print(f"    authenticity_status: pending (waiting for manual verification)")


if __name__ == "__main__":
    main()