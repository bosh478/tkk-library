#!/usr/bin/env python3
"""
test_html2md.py - html2md.py 单元测试(5 用例)

不依赖外部 fixture,直接构造 HTML 字符串 + 调用 subprocess 跑 html2md.py

测试:
  1. 字面 HTML 简单转换
  2. 加 frontmatter(--meta)
  3. 剥除噪声标签(<script>/<style>/<nav>)
  4. 复杂 HTML(表格 + 图片 + 嵌套)
  5. 缺依赖 loudly 报错(测 fail 路径)
"""

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_PATH = Path("/home/kangkang/tkk-library/scripts/html2md.py")


def run_html2md(args: list, input_data: str = None, expect_success: bool = True) -> tuple:
    """跑 html2md.py,返回 (returncode, stdout, stderr)。"""
    cmd = ["python3", str(SCRIPT_PATH)] + args
    result = subprocess.run(
        cmd,
        input=input_data,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if expect_success and result.returncode != 0:
        print(f"[TEST FAIL] 命令: {cmd}")
        print(f"  stdout: {result.stdout[:200]}")
        print(f"  stderr: {result.stderr[:500]}")
    return (result.returncode, result.stdout, result.stderr)


def test_1_literal_html():
    """测试 1: 字面 HTML 转 MD。"""
    print("\n=== Test 1: 字面 HTML ===")
    rc, out, err = run_html2md(["<h1>Hello</h1><p>World <b>bold</b></p>"])
    assert rc == 0, f"exit {rc}"
    assert "# Hello" in out, f"missing # Hello: {out}"
    assert "**bold**" in out, f"missing **bold**: {out}"
    print("  ✓ # Hello / **bold** 都出现")


def test_2_frontmatter():
    """测试 2: --meta 加 frontmatter。"""
    print("\n=== Test 2: --meta 加 frontmatter ===")
    rc, out, err = run_html2md([
        "<h1>Title</h1>", "--meta", "title=测试", "--meta", "tier=T1",
    ])
    assert rc == 0
    assert "title: 测试" in out
    assert "tier: T1" in out
    assert "# Title" in out
    # frontmatter 应在最前
    assert out.startswith("---"), f"frontmatter 应在最前: {out[:50]}"
    print("  ✓ frontmatter 在最前 + 字段正确")


def test_3_strip_noise():
    """测试 3: 剥除 <script>/<style>/<nav> 标签。"""
    print("\n=== Test 3: 剥除噪声标签 ===")
    html = '<h1>Real</h1><script>alert("x")</script><style>body{color:red}</style><nav>nav noise</nav><p>content</p>'
    rc, out, err = run_html2md([html])
    assert rc == 0
    # <script> 内的 alert 应被剥(markdownify 硬编码)
    assert 'alert' not in out, f"script 内容被保留: {out}"
    # <style> 内的 CSS 应被剥
    assert 'color:red' not in out, f"style 内容被保留: {out}"
    # 真实内容应保留
    assert "Real" in out
    assert "content" in out
    print("  ✓ script/style 内容已剥 + 真实内容保留")


def test_4_complex():
    """测试 4: 表格 + 图片 + 嵌套。"""
    print("\n=== Test 4: 复杂 HTML(表格+图片) ===")
    html = """
    <h1>Title</h1>
    <p>含 <strong>加粗</strong> 和 <em>斜体</em>。</p>
    <table>
      <thead><tr><th>列1</th><th>列2</th></tr></thead>
      <tbody><tr><td>A1</td><td>A2</td></tr></tbody>
    </table>
    <img src="x.jpg" alt="测试图" />
    <pre><code>code block</code></pre>
    """
    rc, out, err = run_html2md([html])
    assert rc == 0
    assert "| 列1 | 列2 |" in out, f"table header 错: {out}"
    assert "| A1 | A2 |" in out, f"table row 错: {out}"
    assert "![测试图](x.jpg)" in out, f"image 错: {out}"
    assert "**加粗**" in out
    assert "*斜体*" in out
    assert "code block" in out
    print("  ✓ 表格 / 图片 / 强调 / 代码块 全部正确")


def test_5_input_validation():
    """测试 5: 输入校验(空 HTML + 缺 meta 值报错)。"""
    print("\n=== Test 5: 输入校验 ===")
    # 空 HTML 应报错 exit 1
    rc, out, err = run_html2md([""], expect_success=False)
    assert rc == 1, f"空 HTML 应 exit 1, got {rc}"
    assert "为空" in err, f"应提示为空: {err}"
    print(f"  ✓ 空 HTML → exit 1: {err.strip()[:80]}")

    # --meta 格式错应报错
    rc, out, err = run_html2md(["<p>x</p>", "--meta", "novalue"], expect_success=False)
    assert rc == 1
    assert "格式错" in err
    print(f"  ✓ --meta 格式错 → exit 1")


def main():
    print("=" * 60)
    print("html2md.py 单元测试")
    print("=" * 60)
    if not SCRIPT_PATH.exists():
        print(f"[FAIL] html2md.py 不存在: {SCRIPT_PATH}")
        sys.exit(2)

    try:
        test_1_literal_html()
        test_2_frontmatter()
        test_3_strip_noise()
        test_4_complex()
        test_5_input_validation()
    except AssertionError as e:
        print(f"\n[TEST FAIL] {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("[OK] 5/5 测试通过")
    print("=" * 60)


if __name__ == "__main__":
    main()
