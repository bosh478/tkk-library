import os
import re
from pathlib import Path

VAULT_ROOT = Path("D:/AI agent/tkk-library")
SOURCE_DIR = VAULT_ROOT / "sources/微信公号资料/最高人民法院/最高法-入库案例选介-md"
TARGET_DIR = VAULT_ROOT / "wiki/syntheses"

source_files = sorted(SOURCE_DIR.glob("*.md"))
print(f"Found {len(source_files)} source files")

success = 0
errors = 0

for sf in source_files:
    try:
        content = sf.read_text(encoding="utf-8")
        lines = content.split("\n")

        title = ""
        for line in lines:
            if line.startswith("#"):
                t = line.lstrip("#").strip()
                t = re.sub(r"^入库案例选介", "", t)
                t = re.sub(r"^人民法院案例库入库案例", "", t)
                t = re.sub(r"^人民法院案例库入库参考案例选介", "", t)
                t = re.sub(r"^人民法院案例库入库参考案例", "", t)
                t = re.sub(r"^人民法院案例库入库参考案例解读", "", t)
                t = re.sub(r"^[【\[].*?[\】\]]", "", t)
                title = t.strip()
                break

        # 裁判要旨
        caipan = ""
        m = re.search(r"\*\*裁判要旨\*\*\s*\n?\s*([^\n]+?)(?:\n\n|\*\*|\Z)", content, re.DOTALL)
        if m:
            caipan = m.group(1).strip()

        # 基本案情
        basic = ""
        m = re.search(r"【基本案情】(.+?)(?=【裁判理由】|【专家点评】|【关联索引】|\Z)", content, re.DOTALL)
        if m:
            basic = m.group(1).strip()[:500]

        # 裁判理由
        ruling = ""
        m = re.search(r"【裁判理由】(.+?)(?=【专家点评】|【关联索引】|\Z)", content, re.DOTALL)
        if m:
            ruling = m.group(1).strip()[:800]

        # 专家点评
        expert = ""
        m = re.search(r"【专家点评】(.+?)(?=来源：|编辑：|\Z)", content, re.DOTALL)
        if m:
            expert = m.group(1).strip()[:600]

        # 关联法条
        laws = re.findall(r"《([^》]+)》第?\d+条", content)
        laws = list(set(laws))[:5]

        # 问题意识
        if "正当防卫" in title:
            issue = "正当防卫的认定标准与限度条件"
        elif "劳动关系" in title:
            issue = "新就业形态下劳动关系的认定标准"
        elif "饲养动物" in title or "犬只" in title:
            issue = "动物致害责任中无接触式损害的认定"
        elif "受贿" in title or "贪污" in title:
            issue = "贿赂类犯罪的构成要件与量刑标准"
        elif "诈骗" in title:
            issue = "诈骗类犯罪的司法认定"
        elif "交通肇事" in title:
            issue = "交通事故责任的认定与量刑"
        elif "故意伤害" in title:
            issue = "故意伤害罪的认定与正当防卫界限"
        elif "组织卖淫" in title:
            issue = "组织卖淫罪与立功的认定"
        elif "知识产权" in title or "商标" in title:
            issue = "知识产权侵权的认定与赔偿"
        elif "建设工程" in title:
            issue = "建设工程合同的效力与履行"
        elif "破产" in title or "重整" in title:
            issue = "企业破产程序的启动与效力"
        elif "行政" in title and ("确认" in title or "许可" in title):
            issue = "行政行为的合法性审查标准"
        elif "危险作业" in title:
            issue = "危险作业罪的认定"
        elif "制造毒品" in title or "毒品" in title:
            issue = "毒品犯罪的认定"
        elif "偷越国边境" in title:
            issue = "偷越国边境罪的认定"
        elif "集资诈骗" in title:
            issue = "集资诈骗罪的认定"
        elif "学校" in title and "责任" in title:
            issue = "学校事故责任的认定"
        elif "危险驾驶" in title:
            issue = "危险驾驶罪的认定"
        elif "竞业限制" in title:
            issue = "竞业限制纠纷的处理"
        elif "帮信" in title or "帮助信息网络" in title:
            issue = "帮信罪的认定"
        elif "强制医疗" in title:
            issue = "强制医疗的决定与救济"
        elif "网络直播" in title:
            issue = "网络灰产行为的刑法规制"
        elif "执行监督" in title:
            issue = "执行异议与执行监督"
        elif "个人信息" in title or "开盒" in title:
            issue = "侵犯公民个人信息罪的认定"
        elif "食品安全" in title:
            issue = "食品安全责任的认定"
        elif "加装电梯" in title:
            issue = "业主自治与行政许可是"
        elif "无罪" in title:
            issue = "刑事案件无罪判决的标准"
        elif "猥亵" in title or "侮辱" in title:
            issue = "性犯罪行为的认定"
        elif "开设赌场" in title or "赌场" in title:
            issue = "开设赌场罪的认定"
        else:
            issue = f"涉及{laws[0] if laws else '相关法律'}的法律适用问题"

        tags = ["入库案例选介", "最高人民法院", "人民法院案例库"]
        for law in laws[:2]:
            if law not in tags:
                tags.append(law)

        related = [f"[[concept_{law}]]" for law in laws[:2]] if laws else ["[[concept_人民法院案例库]]"]

        parts = []
        if caipan:
            parts.append(f"## 裁判要旨\n\n{caipan}\n")
        if basic:
            parts.append(f"## 基本案情\n\n{basic}\n")
        if ruling:
            parts.append(f"## 裁判理由\n\n{ruling}\n")
        if expert:
            parts.append(f"## 专家点评\n\n{expert}\n")
        if laws:
            parts.append(f"## 关联法条\n\n{' / '.join([f'《{l}》' for l in laws])}\n")

        body = "\n".join(parts) if parts else f"## 案例概要\n\n{caipan or basic or '详见原文'}\n"

        clean = re.sub(r"^\[\d{4}-\d{2}-\d{2}\]", "", sf.name)
        for p in [r"^入库案例选介", r"^人民法院案例库入库案例", r"^人民法院案例库入库参考案例选介", r"^人民法院案例库入库参考案例", r"^人民法院案例库入库参考案例解读"]:
            clean = re.sub(p, "", clean)
        clean = clean.replace(".md", "")
        outfile = f"CourtFa_入库案例_{clean}.md"

        fm = f"""---
title: {title}
type: synthesis
created: 2026-05-11
updated: 2026-05-11
tags: [{", ".join(tags)}]
source: "sources/微信公号资料/最高人民法院/最高法-入库案例选介-md/{sf.name}"
related: [{", ".join(related)}]
案例分级: ⭐⭐⭐⭐
问题意识: {issue}
---

"""
        (TARGET_DIR / outfile).write_text(fm + body, encoding="utf-8")
        success += 1
        if success % 20 == 0:
            print(f"Processed {success}/{len(source_files)}...")

    except Exception as e:
        errors += 1
        print(f"Error {sf.name}: {e}")

print(f"Done: {success} success, {errors} errors")