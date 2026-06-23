#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件夹大小查询工具
扫描指定目录或全盘，计算所有子文件夹占用的磁盘空间，生成 HTML 报告
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

# 解决 Windows 终端中文编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def get_drives() -> List[str]:
    """获取 Windows 系统上所有可用的驱动器"""
    drives = []
    if sys.platform == 'win32':
        # Windows 系统：遍历 A-Z 检查驱动器是否存在
        for letter in range(ord('A'), ord('Z') + 1):
            drive = f"{chr(letter)}:\\"
            if os.path.exists(drive):
                drives.append(drive)
    else:
        # 非 Windows 系统：返回根目录
        drives.append('/')
    return drives


def get_folder_size(folder_path: str) -> int:
    """递归计算文件夹大小（字节）"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            try:
                for filename in filenames:
                    fp = os.path.join(dirpath, filename)
                    if os.path.exists(fp):
                        try:
                            total_size += os.path.getsize(fp)
                        except (OSError, PermissionError):
                            continue
            except (PermissionError, OSError):
                continue
    except (PermissionError, OSError):
        pass
    return total_size


def format_size(size_bytes: int) -> str:
    """格式化文件大小为人类可读格式"""
    if size_bytes >= 1024 ** 4:
        return f"{size_bytes / 1024**4:.2f} TB"
    elif size_bytes >= 1024 ** 3:
        return f"{size_bytes / 1024**3:.2f} GB"
    elif size_bytes >= 1024 ** 2:
        return f"{size_bytes / 1024**2:.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} B"


def scan_single_drive(root_path: str, progress: bool = True) -> List[Tuple[str, str, int, str]]:
    """
    扫描单个驱动器/目录，返回所有文件夹大小列表
    """
    folder_sizes = []
    count = 0

    try:
        for dirpath, dirnames, _ in os.walk(root_path):
            for dirname in dirnames:
                full_path = os.path.join(dirpath, dirname)
                size = get_folder_size(full_path)
                folder_sizes.append((
                    dirname,
                    full_path,
                    size,
                    format_size(size)
                ))
                count += 1
                if progress and count % 10000 == 0:
                    print(f"  已扫描 {count} 个文件夹...")
    except (PermissionError, OSError) as e:
        print(f"  警告: 无法完全访问 {root_path}: {e}", file=sys.stderr)

    if progress:
        print(f"  完成: {count} 个文件夹")
    return folder_sizes


def scan_all_drives(top: int = 20) -> Tuple[List[Tuple[str, str, int, str]], List[str]]:
    """
    扫描所有驱动器，返回文件夹大小列表
    返回: (文件夹列表, 已扫描的驱动器列表)
    """
    drives = get_drives()
    print(f"发现 {len(drives)} 个驱动器: {', '.join(drives)}")
    print()

    all_folders = []
    scanned_drives = []

    for drive in drives:
        print(f"正在扫描驱动器: {drive}")
        print("这可能需要几分钟，请稍候...")
        start = time.time()

        folders = scan_single_drive(drive)
        all_folders.extend(folders)
        scanned_drives.append(drive)

        elapsed = time.time() - start
        print(f"  完成: {len(folders)} 个文件夹, 耗时 {elapsed:.1f} 秒")
        print()

    # 排序
    all_folders.sort(key=lambda x: x[2], reverse=True)

    # 返回全部或限制数量
    if top > 0:
        all_folders = all_folders[:top]

    return all_folders, scanned_drives


def scan_folders(root_path: str, top: int = 0) -> Tuple[List[Tuple[str, str, int, str]], List[str]]:
    """
    扫描目录并返回文件夹大小列表
    返回: (文件夹列表, [扫描的目录])
    """
    print(f"正在扫描: {root_path}")
    print("正在计算文件夹大小，请稍候...")

    start_time = time.time()
    folder_list = scan_single_drive(root_path)
    elapsed_time = time.time() - start_time

    print(f"扫描完成，共发现 {len(folder_list)} 个文件夹，耗时 {elapsed_time:.1f} 秒")
    print()

    # 排序
    folder_list.sort(key=lambda x: x[2], reverse=True)

    # 返回全部或限制数量
    if top > 0:
        folder_list = folder_list[:top]

    return folder_list, [root_path]


def generate_html_report(
    scan_path: str,
    folder_list: List[Tuple[str, str, int, str]],
    output_file: str,
    elapsed_time: float,
    is_all_drives: bool = False
) -> None:
    """生成 HTML 报告"""

    # 计算最大尺寸用于百分比条
    max_size = folder_list[0][2] if folder_list else 0

    rows_html = ""
    for rank, (name, path, size, size_str) in enumerate(folder_list, 1):
        percentage = (size / max_size * 100) if max_size > 0 else 0

        # 前三名特殊样式
        if rank == 1:
            rank_class = "top1"
            rank_symbol = "🥇"
        elif rank == 2:
            rank_class = "top2"
            rank_symbol = "🥈"
        elif rank == 3:
            rank_class = "top3"
            rank_symbol = "🥉"
        else:
            rank_class = ""
            rank_symbol = f"#{rank}"

        rows_html += f"""
            <tr>
                <td class="rank {rank_class}">{rank_symbol}</td>
                <td class="name">{name}</td>
                <td class="path">{path}</td>
                <td class="size">
                    {size_str}
                    <div class="size-bar">
                        <div class="size-bar-fill" style="width: {percentage:.1f}%"></div>
                    </div>
                </td>
                <td>{percentage:.1f}%</td>
            </tr>
        """

    if not folder_list:
        table_content = '<div class="note">⚠️ 未找到任何子文件夹</div>'
    else:
        table_content = f"""
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>文件夹名称</th>
                        <th>路径</th>
                        <th>大小</th>
                        <th>占比</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文件夹大小报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 25px 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }}
        .header h1 {{
            color: #1a1a2e;
            font-size: 24px;
            margin-bottom: 10px;
        }}
        .header .info {{
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
            font-size: 14px;
            color: #666;
        }}
        .header .info span {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            overflow-x: auto;
        }}
        .card h2 {{
            color: #1a1a2e;
            font-size: 18px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #f8f9fa;
            color: #1a1a2e;
            font-weight: 600;
            text-align: left;
            padding: 12px 15px;
            border-bottom: 2px solid #dee2e6;
            position: sticky;
            top: 0;
        }}
        td {{
            padding: 10px 15px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .rank {{
            font-weight: bold;
            color: #666;
            width: 60px;
            text-align: center;
        }}
        .rank.top1 {{ color: #ffd700; }}
        .rank.top2 {{ color: #c0c0c0; }}
        .rank.top3 {{ color: #cd7f32; }}
        .name {{
            font-weight: 500;
            color: #1a1a2e;
            max-width: 250px;
            word-break: break-all;
        }}
        .path {{
            color: #666;
            font-size: 13px;
            max-width: 400px;
            word-break: break-all;
        }}
        .size {{
            font-weight: 600;
            color: #2c5282;
            white-space: nowrap;
        }}
        .size-bar {{
            width: 100px;
            height: 6px;
            background: #e2e8f0;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 4px;
        }}
        .size-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4299e1, #2b6cb0);
            border-radius: 3px;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: rgba(255, 255, 255, 0.6);
            font-size: 12px;
        }}
        .note {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            font-size: 14px;
        }}
        .drive-tag {{
            background: #dc3545;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📁 文件夹大小报告 {'(全盘扫描)' if is_all_drives else ''}</h1>
            <div class="info">
                <span>📂 扫描目录: <strong>{scan_path}{'<span class="drive-tag">全盘</span>' if is_all_drives else ''}</strong></span>
                <span>📊 显示数量: <strong>{len(folder_list)} 个文件夹</strong></span>
                <span>⏱️ 扫描时间: <strong>{elapsed_time:.1f} 秒</strong></span>
                <span>🕐 生成时间: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></span>
            </div>
        </div>

        <div class="card">
            <h2>📊 文件夹大小排名（按大小降序）</h2>
            {table_content}
        </div>

        <div class="footer">
            由 Python 脚本自动生成 | 文件夹大小分析工具
        </div>
    </div>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='扫描目录或全盘并生成文件夹大小报告（HTML格式）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python folder-size.py --all              # 扫描所有驱动器（显示全部）
  python folder-size.py --all -n 30        # 扫描全盘，显示前30名
  python folder-size.py --all -n 0         # 扫描全盘，显示全部
  python folder-size.py "D:\\Projects"     # 扫描指定目录（显示全部）
  python folder-size.py "D:\\Projects" -n 10 # 扫描指定目录，显示前10名
        '''
    )

    parser.add_argument('path', nargs='?', default=None,
                        help='要扫描的根目录（默认当前目录）')
    parser.add_argument('-a', '--all', action='store_true',
                        help='扫描所有驱动器（全盘扫描）')
    parser.add_argument('-n', '--top', type=int, default=0,
                        help='显示前 N 个最大的文件夹（0或不指定表示全部）')
    parser.add_argument('-o', '--output', default='folder-size-report.html',
                        help='HTML输出文件路径（默认 folder-size-report.html）')

    args = parser.parse_args()

    start_time = time.time()
    is_all_drives = args.all
    top_n = args.top if args.top > 0 else 0  # 0 表示全部

    if is_all_drives:
        # 全盘扫描
        print("=" * 50)
        print("全盘扫描模式" + ("（显示全部）" if top_n == 0 else f"（显示前{top_n}名）"))
        print("=" * 50)
        folder_list, scanned_drives = scan_all_drives(top_n)
        scan_path = "所有驱动器: " + ", ".join(scanned_drives)
    else:
        # 单目录扫描
        root_path = args.path if args.path else '.'
        root_path = os.path.abspath(root_path)

        if not os.path.exists(root_path):
            print(f"错误: 路径不存在 - {root_path}", file=sys.stderr)
            sys.exit(1)

        if not os.path.isdir(root_path):
            print(f"错误: 路径不是有效的目录 - {root_path}", file=sys.stderr)
            sys.exit(1)

        print("=" * 50)
        print(f"扫描目录: {root_path}" + ("（显示全部）" if top_n == 0 else f"（显示前{top_n}名）"))
        print("=" * 50)

        folder_list, scanned_drives = scan_folders(root_path, top_n)
        scan_path = root_path

    elapsed_time = time.time() - start_time

    # 生成报告
    generate_html_report(scan_path, folder_list, args.output, elapsed_time, is_all_drives)

    # 输出结果
    print()
    print(f"\033[92m✅ 报告生成完成！\033[0m")
    print(f"\033[94m📄 输出文件: {os.path.abspath(args.output)}\033[0m")
    print(f"\033[93m🌐 可在浏览器中打开查看\033[0m")


if __name__ == '__main__':
    main()
