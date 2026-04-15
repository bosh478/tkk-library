const fs = require('fs');
const path = require('path');

const CLIPPINGS_DIR = "D:/AI agent/tkk-library/Clippings";
const SOURCES_DIR = "D:/AI agent/tkk-library/sources/网络文章";
const SUMMARIES_DIR = "D:/AI agent/tkk-library/wiki/summaries";

const FILES = [
    ["律师从事关税法律业务操作指引（2025）（试行） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2025-05-13", "律师从事关税法律业务操作指引（2025）（试行）", "https://www.lawyers.org.cn/info/07e2655265534a46ae31d5f329d94b88"],
    ["律师从事劳动争议调解业务操作指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-03-27", "律师从事劳动争议调解业务操作指引（2024）", "https://www.lawyers.org.cn/info/1c76fa42b7be4ff69dba61aaf4c4a30d"],
    ["律师从事国际贸易合同（出口）业务操作指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-03-27", "律师从事国际贸易合同（出口）业务操作指引（2024）", "https://www.lawyers.org.cn/info/2182d5480d194c4e824c8e88cc1febf2"],
    ["律师从事婚姻家事案件调解业务操作指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-03-27", "律师从事婚姻家事案件调解业务操作指引（2024）", "https://www.lawyers.org.cn/info/84b2758a4c2545a1aa8b7f0298af610d"],
    ["律师从事物业服务费催收业务操作指引（2022） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2022-01-05", "律师从事物业服务费催收业务操作指引（2022）", "https://www.lawyers.org.cn/info/2f67e8c2d7794899899034c30767fb27"],
    ["律师从事物业服务费催收业务操作指引（2025）（试行） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2025-01-01", "律师从事物业服务费催收业务操作指引（2025）（试行）", "https://www.lawyers.org.cn/info/5116351d578242c5a9166e3cc4b45696"],
    ["律师从事调解业务操作指引（2021） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2021-06-24", "律师从事调解业务操作指引（2021）", "https://www.lawyers.org.cn/info/390710fa42494d729c76893037f82fd5"],
    ["律师从事金融（消费）纠纷案件调解 业务操作指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-03-27", "律师从事金融（消费）纠纷案件调解业务操作指引（2024）", "https://www.lawyers.org.cn/info/5f02f6697a98469dba3ba18f9f8ae447"],
    ["律师代理临时仲裁案件业务指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-12-17", "律师代理临时仲裁案件业务指引（2024）", "https://www.lawyers.org.cn/info/3e1fe5988dc64039ab226c0709a32ff1"],
    ["律师代理劳动人事争议诉讼案件操作指引（2020） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2020-12-30", "律师代理劳动人事争议诉讼案件操作指引（2020）", "https://www.lawyers.org.cn/info/3f9655f7c4f5402681a07f874a775e1a"],
    ["律师代理医保行政处罚案件操作指引（2025）（试行） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2025-08-13", "律师代理医保行政处罚案件操作指引（2025）（试行）", "https://www.lawyers.org.cn/info/b72e5ec29cdf4a43906dc09dc829ee09"],
    ["律师代理医疗机构行政处罚案件操作指引（2022） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2022-01-05", "律师代理医疗机构行政处罚案件操作指引（2022）", "https://www.lawyers.org.cn/info/e96dd790624949d38f8007253d4f368f"],
    ["律师代理医疗科技成果转化业务操作指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-03-27", "律师代理医疗科技成果转化业务操作指引（2024）", "https://www.lawyers.org.cn/info/638f41cb8d99433aba1da5b179883147"],
];

function cleanContent(content) {
    // Remove frontmatter
    content = content.replace(/^---\n[\s\S]*?\n---\n/, '');
    // Remove breadcrumb
    content = content.replace(/^当前位置：.*?(?=\n\- \[|$)/gm, '');
    // Remove committee links block
    content = content.replace(/^\| ESG \|.*?(?=##\s+|$)/gm, '');
    // Remove editor info at end
    content = content.replace(/\*\*策划：\*\*[\s\S]*$/, '');
    content = content.replace(/\*\*执笔：\*\*[\s\S]*$/, '');
    content = content.replace(/^\s*执笔：.*/gm, '');
    content = content.replace(/^\s*策划：.*/gm, '');
    content = content.replace(/^\s*统筹人：.*/gm, '');
    content = content.replace(/^\s*策划人：.*/gm, '');
    content = content.replace(/^\s*执笔人：.*/gm, '');
    // Remove trailing notification and tools sections
    content = content.replace(/\[更多\][\s\S]*$/, '');
    content = content.replace(/常用工具[\s\S]*$/, '');

    // Remove navigation links at end
    const lines = content.split('\n');
    const cleanedLines = [];
    let skipSection = false;
    for (const line of lines) {
        if (line.includes('[更多]')) {
            skipSection = true;
            continue;
        }
        if (skipSection) continue;
        if (line.trim().startsWith('- [') && line.includes('http')) continue;
        const navItems = ['城市地图查询', '城市天气查询', '统计局数据公布', '万年历查询', '法院在线服务平台', '法院开庭信息检索', '诉讼费计算器'];
        if (navItems.some(item => line.includes(item))) continue;
        cleanedLines.push(line);
    }
    content = cleanedLines.join('\n');
    content = content.replace(/\n{3,}/g, '\n\n');
    return content.trim();
}

function processFile(sourceFile, published, coreTitle, sourceUrl) {
    const sourcePath = path.join(CLIPPINGS_DIR, sourceFile);

    if (!fs.existsSync(sourcePath)) {
        return [false, `文件不存在: ${sourceFile}`];
    }

    try {
        var content = fs.readFileSync(sourcePath, 'utf-8');
    } catch (e) {
        return [false, `读取失败: ${e}`];
    }

    // Find title from H2
    const titleMatch = content.match(/^##\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1] : coreTitle;

    // Clean content
    const cleaned = cleanContent(content);

    // Build output
    const outputPath = path.join(SOURCES_DIR, `${published}_${coreTitle}.md`);
    try {
        fs.writeFileSync(outputPath, `---
title: "${title}"
source: "${sourceUrl}"
author:
published: ${published}
created: 2026-04-14
description:
tags: ["clippings"]
---

${cleaned}
`);
    } catch (e) {
        return [false, `写入失败: ${e}`];
    }

    // Generate summary page
    const summaryContent = `---
title: ${title}
type: summary
created: 2026-04-14
updated: 2026-04-14
tags: [律师业务指引]
source: [[${published}_${coreTitle}.md]]
---

## 关键要点

（需要手动填写）

## 相关链接

- [[${published}_${coreTitle}.md]]
`;

    const summaryPath = path.join(SUMMARIES_DIR, `${published}_${coreTitle}.md`);
    try {
        fs.writeFileSync(summaryPath, summaryContent);
    } catch (e) {
        return [false, `写入摘要失败: ${e}`];
    }

    return [true, `成功: ${published}_${coreTitle}.md`];
}

function main() {
    fs.mkdirSync(SOURCES_DIR, { recursive: true });
    fs.mkdirSync(SUMMARIES_DIR, { recursive: true });

    const results = [];
    for (const [sourceFile, published, coreTitle, sourceUrl] of FILES) {
        const [success, message] = processFile(sourceFile, published, coreTitle, sourceUrl);
        results.push([sourceFile, success, message]);
        console.log(`${success ? 'OK' : 'FAIL'}: ${message}`);
    }

    console.log("\n" + "=".repeat(50));
    const successCount = results.filter(([, s]) => s).length;
    console.log(`处理完成: ${successCount}/${results.length} 成功`);
    const failed = results.filter(([, s]) => !s);
    if (failed.length > 0) {
        console.log("失败列表:");
        for (const [f, , m] of failed) {
            console.log(`  - ${f}: ${m}`);
        }
    }
}

main();