/**
 * 数字图书馆检索脚本
 * 功能：
 * 1. 加载索引
 * 2. 接收用户问题
 * 3. 执行混合检索（关键词预筛选 + AI语义精排）
 * 4. 输出结构化结果
 */

const fs = require('fs');
const path = require('path');

// 引入 MiniSearch
const MiniSearch = require('minisearch');

// 配置
const LIBRARY_PATH = path.join(__dirname, '..');
const OUTPUT_DIR = __dirname;
const MAX_CANDIDATES = 20;  // 预筛选候选数量
const MAX_RESULTS = 5;      // 最终返回结果数量

// 加载索引
function loadIndex() {
  console.log('📂 加载索引...\n');

  // 加载书籍元数据
  const indexData = JSON.parse(
    fs.readFileSync(path.join(OUTPUT_DIR, 'index.json'), 'utf-8')
  );

  // 加载章节结构
  const sectionsData = JSON.parse(
    fs.readFileSync(path.join(OUTPUT_DIR, 'sections.json'), 'utf-8')
  );

  // 加载 MiniSearch 索引
  const searchIndexData = JSON.parse(
    fs.readFileSync(path.join(OUTPUT_DIR, 'search-index.json'), 'utf-8')
  );

  const miniSearch = MiniSearch.loadJSON(
    JSON.stringify(searchIndexData.index),
    { fields: ['title', 'headings_text', 'case_ids_text'] }
  );

  console.log(`✅ 已加载 ${indexData.totalBooks} 本书籍, ${sectionsData.sections.length} 个章节\n`);

  return {
    indexData,
    sectionsData,
    miniSearch
  };
}

// 从文件内容中获取指定行及其上下文
function getContentAroundLine(filePath, targetLine, contextLines = 5) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');

    const startLine = Math.max(0, targetLine - contextLines - 1);
    const endLine = Math.min(lines.length, targetLine + contextLines);

    const excerpt = lines.slice(startLine, endLine).join('\n');

    return {
      excerpt,
      startLine: startLine + 1,
      endLine,
      fullContent: content
    };
  } catch (error) {
    return { excerpt: '', startLine: 0, endLine: 0, fullContent: '' };
  }
}

// 关键词预检索
function keywordSearch(miniSearch, query, sections, indexData) {
  console.log('🔍 第一层：关键词预检索...\n');

  // 增强查询：加入原始问题和提取的关键词
  const enhancedQuery = query;

  // 执行搜索
  const results = miniSearch.search(enhancedQuery, {
    prefix: true,
    fuzzy: 0.2,
    combineWith: 'OR'
  });

  // 限制候选数量
  const candidates = results.slice(0, MAX_CANDIDATES);

  // 构建候选上下文
  const candidatesWithContext = candidates.map(r => {
    const section = sections.sections.find(s => s.id === r.id) || {};
    const book = indexData.books.find(b => b.id === section.book_id) || {};

    const filePath = path.join(LIBRARY_PATH, r.relativePath);
    const contentInfo = getContentAroundLine(filePath, r.lineNum, 3);

    return {
      index_id: r.id,
      book_id: section.book_id,
      book_title: book.title || r.book_title,
      relative_path: r.relativePath,
      full_path: filePath,
      category: r.category,
      year: r.year,
      heading: r.heading,
      heading_level: r.heading_level,
      line_num: r.lineNum,
      case_ids: r.case_ids || [],
      excerpt: contentInfo.excerpt,
      score: r.score
    };
  });

  console.log(`   找到 ${candidates.length} 个候选章节\n`);

  return candidatesWithContext;
}

// 生成AI检索提示
function generateAIPrompt(query, candidates) {
  const candidatesText = candidates.map((c, i) => `
候选段落 ${i + 1}:
- 书籍: ${c.book_title}
- 章节: ${c.heading}
- 案例编号: ${c.case_ids.join(', ') || '无'}
- 内容片段:
"""
${c.excerpt.substring(0, 500)}${c.excerpt.length > 500 ? '...' : ''}
"""
`).join('\n');

  return `你是法律检索助手。用户的问题是：「${query}」

请判断以下每个候选段落是否与问题相关，按相关度打分（0-1）。

${candidatesText}

输出格式（仅返回JSON，不要其他内容）：
{
  "results": [
    {"index": 1, "score": 0.95, "reason": "简要说明为什么相关"},
    {"index": 2, "score": 0.80, "reason": "说明"}
  ]
}

注意：
- 只返回与问题真正相关的段落（score > 0.3）
- 相关度 0.95-1.0 = 高度相关（直接回答问题）
- 相关度 0.70-0.94 = 中度相关（提供参考信息）
- 相关度 0.30-0.69 = 低度相关（边缘相关）
- score <= 0.3 的不要包含在结果中`;
}

// 解析AI返回结果
function parseAIResults(aiResponse, candidates) {
  try {
    const jsonMatch = aiResponse.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      console.log('⚠️ 无法解析AI返回，将使用关键词排序结果\n');
      return candidates.slice(0, MAX_RESULTS);
    }

    const aiResults = JSON.parse(jsonMatch[0]);
    return aiResults.results
      .filter(r => r.score > 0.3)
      .sort((a, b) => b.score - a.score)
      .slice(0, MAX_RESULTS)
      .map(r => ({
        ...candidates[r.index - 1],
        ai_score: r.score,
        ai_reason: r.reason
      }));
  } catch (error) {
    console.log(`⚠️ AI结果解析失败: ${error.message}，使用关键词排序结果\n`);
    return candidates.slice(0, MAX_RESULTS);
  }
}

// 格式化输出结果
function formatResults(query, results) {
  let output = '';
  output += '# 检索结果\n\n';
  output += `**问题：** ${query}\n\n`;
  output += `---\n\n`;

  if (results.length === 0) {
    output += '❌ 未找到相关内容\n\n';
    output += '**建议：**\n';
    output += '- 尝试使用更简短或更通用的关键词\n';
    output += '- 检查是否有拼写错误\n';
    output += '- 尝试使用案例编号（如"第1038号"）\n';
    return output;
  }

  results.forEach((r, i) => {
    const relevanceLabel = r.ai_score >= 0.95 ? '🟢 高度相关' :
                          r.ai_score >= 0.70 ? '🟡 中度相关' : '🔵 低度相关';

    output += `## 结果 ${i + 1}：${relevanceLabel}\n\n`;
    output += `**来源：** ${r.book_title}\n\n`;
    output += `**路径：** ${r.relative_path}\n\n`;
    output += `**章节：** ${r.heading}\n\n`;

    if (r.case_ids.length > 0) {
      output += `**案例编号：** ${r.case_ids.join(', ')}\n\n`;
    }

    output += `**相关度：** ${r.ai_score?.toFixed(2) || r.score.toFixed(2)}\n\n`;

    if (r.ai_reason) {
      output += `**判断理由：** ${r.ai_reason}\n\n`;
    }

    output += `**原文摘录：**\n`;
    output += `> ${r.excerpt.split('\n').join('\n> ')}\n\n`;
    output += `---\n\n`;
  });

  output += `\n**说明：** 共找到 ${results.length} 条相关结果\n`;

  return output;
}

// 主检索函数
async function search(query, useAI = true) {
  console.log('='.repeat(60));
  console.log('🔎 数字图书馆检索系统');
  console.log('='.repeat(60));
  console.log();

  if (!query) {
    console.log('❌ 请提供检索问题');
    return;
  }

  const startTime = Date.now();

  // 加载索引
  const { indexData, sectionsData, miniSearch } = loadIndex();

  // 第一层：关键词预检索
  const candidates = keywordSearch(miniSearch, query, sectionsData, indexData);

  let results;

  if (useAI && candidates.length > 0) {
    // 第二层：AI语义精排
    console.log('🤖 第二层：AI语义精排...\n');

    const prompt = generateAIPrompt(query, candidates);

    console.log('📝 请在下方粘贴 AI 返回结果（JSON格式）：\n');
    console.log('--- AI提示 ---');
    console.log(prompt);
    console.log('--- 提示结束 ---\n');

    // 这里需要用户手动调用AI或通过其他方式获取结果
    // 暂时返回候选结果供用户选择
    console.log('💡 提示：请使用 /library-search 命令配合 AI 进行语义精排\n');

    results = candidates.slice(0, MAX_RESULTS).map(c => ({
      ...c,
      ai_score: c.score,
      ai_reason: '（关键词匹配，未经过AI精排）'
    }));
  } else {
    results = candidates.slice(0, MAX_RESULTS);
  }

  // 格式化输出
  const output = formatResults(query, results);

  console.log(output);

  const elapsed = Date.now() - startTime;
  console.log(`\n⏱️ 检索耗时: ${elapsed}ms`);

  return {
    query,
    results,
    rawOutput: output,
    elapsed
  };
}

// 导出模块
module.exports = { search, loadIndex, keywordSearch };

// CLI 模式
if (require.main === module) {
  const query = process.argv.slice(2).join(' ');
  const useAI = !process.argv.includes('--no-ai');

  if (!query) {
    console.log('用法: node search.js "检索问题" [--no-ai]');
    console.log('示例: node search.js "刑讯逼供取得的证据如何处理"');
    process.exit(1);
  }

  search(query, useAI).catch(console.error);
}
