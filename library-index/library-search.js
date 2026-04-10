/**
 * 数字图书馆检索命令行工具
 * 用法: node library-search.js "检索问题" [书库路径]
 *
 * 功能：
 * 1. 自动检查并构建索引（如有新增资料）
 * 2. 执行全文检索
 * 3. 返回结构化检索结果
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const LIBRARY_PATH = process.argv[3] || path.join(__dirname, '..');
const INDEX_DIR = __dirname;
const MAX_CANDIDATES = 10;
const MAX_RESULTS = 5;

// 检查索引是否存在且最新
function checkIndex() {
  const indexFile = path.join(INDEX_DIR, 'index.json');
  const sectionsFile = path.join(INDEX_DIR, 'sections.json');
  const searchIndexFile = path.join(INDEX_DIR, 'search-index.json');

  // 检查索引文件是否存在
  if (!fs.existsSync(indexFile) || !fs.existsSync(sectionsFile) || !fs.existsSync(searchIndexFile)) {
    return { needRebuild: true, reason: '索引文件不存在' };
  }

  // 读取索引元数据
  try {
    const indexData = JSON.parse(fs.readFileSync(indexFile, 'utf-8'));

    // 检查索引的书库路径是否匹配
    if (indexData.libraryPath !== LIBRARY_PATH) {
      return { needRebuild: true, reason: '书库路径变更' };
    }

    // 检查书库中是否有比索引更新的文件
    const indexBuildTime = new Date(indexData.buildAt).getTime();

    // 获取书库中所有 .md 文件的最新修改时间
    const mdFiles = getAllMdFiles(LIBRARY_PATH);
    let latestFileTime = 0;

    for (const file of mdFiles) {
      // 跳过非书籍文件
      if (isExcludedFile(file)) continue;

      const stat = fs.statSync(file);
      if (stat.mtimeMs > latestFileTime) {
        latestFileTime = stat.mtimeMs;
      }
    }

    if (latestFileTime > indexBuildTime) {
      return { needRebuild: true, reason: '书库文件有更新' };
    }

    return { needRebuild: false, reason: '索引已是最新' };

  } catch (error) {
    return { needRebuild: true, reason: `索引读取失败: ${error.message}` };
  }
}

// 获取所有 .md 文件
function getAllMdFiles(dir, files = []) {
  const items = fs.readdirSync(dir);

  for (const item of items) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      getAllMdFiles(fullPath, files);
    } else if (item.endsWith('.md')) {
      files.push(fullPath);
    }
  }

  return files;
}

// 检查是否是需要排除的文件
function isExcludedFile(filePath) {
  const excluded = [
    '.obsidian', '.git', 'copilot', '欢迎.md', '2026-04-07.md',
    'CHANGELOG.md', 'README.md', 'Clip Web Page', 'Clip YouTube Transcript',
    'Emojify', 'Explain like I am 5', 'Fix grammar and spelling',
    'Generate glossary', 'Generate table of contents', 'Make longer',
    'Make shorter', 'Remove URLs', 'Rewrite as tweet',
    'Simplify', 'Summarize', 'Translate to Chinese'
  ];

  for (const ex of excluded) {
    if (filePath.includes(ex)) return true;
  }
  return false;
}

// 构建索引
function buildIndex() {
  console.log('🔨 开始构建索引...\n');

  try {
    execSync(`node "${path.join(INDEX_DIR, 'build-index.js')}" "${LIBRARY_PATH}"`, {
      encoding: 'utf-8',
      stdio: 'inherit'
    });
    console.log('✅ 索引构建完成！\n');
    return true;
  } catch (error) {
    console.error('❌ 索引构建失败:', error.message);
    return false;
  }
}

// 加载索引
function loadIndex() {
  const MiniSearch = require('minisearch');

  const indexData = JSON.parse(fs.readFileSync(path.join(INDEX_DIR, 'index.json'), 'utf-8'));
  const sectionsData = JSON.parse(fs.readFileSync(path.join(INDEX_DIR, 'sections.json'), 'utf-8'));
  const searchIndexData = JSON.parse(fs.readFileSync(path.join(INDEX_DIR, 'search-index.json'), 'utf-8'));

  const miniSearch = MiniSearch.loadJSON(JSON.stringify(searchIndexData.index), {
    fields: ['title', 'headings_text', 'case_ids_text']
  });

  return { indexData, sectionsData, miniSearch };
}

// 获取内容片段
function getContentExcerpt(filePath, lineNum, contextLines = 5) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');
    const start = Math.max(0, lineNum - contextLines - 1);
    const end = Math.min(lines.length, lineNum + contextLines);
    return lines.slice(start, end).join('\n');
  } catch {
    return '';
  }
}

// 关键词检索
function keywordSearch(miniSearch, query, sections, indexData) {
  const results = miniSearch.search(query, {
    prefix: true,
    fuzzy: 0.2,
    combineWith: 'OR'
  });

  return results.slice(0, MAX_CANDIDATES).map(r => {
    const section = sections.sections.find(s => s.id === r.id) || {};
    const book = indexData.books.find(b => b.id === section.book_id) || {};
    const filePath = path.join(LIBRARY_PATH, r.relativePath);
    const excerpt = getContentExcerpt(filePath, r.lineNum, 3);

    return {
      id: r.id,
      book_id: section.book_id,
      book_title: book.title || r.book_title,
      relativePath: r.relativePath,
      category: r.category,
      year: r.year,
      heading: r.heading,
      lineNum: r.lineNum,
      case_ids: r.case_ids || [],
      excerpt,
      score: r.score
    };
  });
}

// 调用 Claude 进行语义排序
function callAIForRerank(query, candidates) {
  const candidatesText = candidates.map((c, i) =>
`【${i + 1}】${c.book_title}
章节: ${c.heading}
${c.case_ids.length > 0 ? '案例编号: ' + c.case_ids.join(', ') : ''}
内容片段: ${c.excerpt.substring(0, 300)}...`
  ).join('\n\n');

  const prompt = `你是法律检索专家。用户的问题是：「${query}」

请判断以下每个检索结果与问题的相关性，按0-1打分，返回JSON格式：

${candidatesText}

返回格式：
{"results": [{"index": 1, "score": 0.95, "reason": "判断理由"}, ...]}
只返回相关的结果（score > 0.3），不相关的不返回。`;

  // Claude Code 环境可以直接调用 AI，这里返回 null
  // 用户可以使用 /tkk-library skill 来进行完整检索
  console.log('💡 提示: 如需 AI 语义排序，请使用 /tkk-library skill');
  return null;
}

// 格式化输出
function formatResults(query, results) {
  let output = `# 📚 检索结果\n\n`;
  output += `**问题：** ${query}\n\n`;
  output += `---\n\n`;

  if (results.length === 0) {
    output += `❌ 未找到相关内容\n\n`;
    output += `**建议：**\n`;
    output += `- 尝试使用更简短的关键词\n`;
    output += `- 检查是否有拼写错误\n`;
    output += `- 尝试使用案例编号搜索\n`;
    return output;
  }

  results.forEach((r, i) => {
    const score = r.aiScore || r.score;
    const label = score >= 0.9 ? '🟢 高度相关' :
                  score >= 0.7 ? '🟡 中度相关' : '🔵 低度相关';

    output += `## 结果 ${i + 1}：${label}\n\n`;
    output += `**来源：** ${r.book_title}\n\n`;
    output += `**路径：** ${r.relativePath}\n\n`;
    output += `**章节：** ${r.heading}\n\n`;

    if (r.case_ids && r.case_ids.length > 0) {
      output += `**案例编号：** ${r.case_ids.join(', ')}\n\n`;
    }

    output += `**相关度：** ${(score * 100).toFixed(0)}%\n\n`;

    if (r.aiReason) {
      output += `**判断理由：** ${r.aiReason}\n\n`;
    }

    output += `**原文摘录：**\n`;
    output += `> ${r.excerpt.split('\n').join('\n> ')}\n\n`;
    output += `---\n\n`;
  });

  output += `\n共找到 ${results.length} 条相关结果`;

  return output;
}

// 主函数
async function search(query, libraryPath) {
  const targetLibraryPath = libraryPath || LIBRARY_PATH;

  console.log('='.repeat(50));
  console.log('🔍 数字图书馆全文检索系统');
  console.log('='.repeat(50));
  console.log();
  console.log(`📚 书库路径: ${targetLibraryPath}`);
  console.log();

  if (!query) {
    console.log('用法: node library-search.js "检索问题" [书库路径]');
    console.log('示例: node library-search.js "刑讯逼供"');
    console.log('     node library-search.js "毒品犯罪" "D:\\书籍文件夹"');
    process.exit(1);
  }

  const startTime = Date.now();

  // 步骤1：检查索引
  console.log('🔍 检查索引状态...');
  const indexStatus = checkIndex();
  console.log(`   ${indexStatus.needRebuild ? '⚠️ ' + indexStatus.reason : '✅ ' + indexStatus.reason}`);

  // 步骤2：必要时重建索引
  if (indexStatus.needRebuild) {
    console.log();
    if (!buildIndex()) {
      process.exit(1);
    }
  }

  // 步骤3：加载索引
  console.log('📂 加载索引...');
  try {
    const { indexData, sectionsData, miniSearch } = loadIndex();
    console.log(`   ✅ 已加载 ${indexData.totalBooks} 本书籍，${sectionsData.sections.length} 个章节\n`);
  } catch (error) {
    console.error('❌ 索引加载失败:', error.message);
    process.exit(1);
  }

  // 步骤4：关键词检索
  console.log('🔍 执行关键词检索...');
  const { indexData, sectionsData, miniSearch } = loadIndex();
  const candidates = keywordSearch(miniSearch, query, sectionsData, indexData);
  console.log(`   找到 ${candidates.length} 个候选\n`);

  // 步骤5：AI 语义排序（可选）
  let results = candidates;
  console.log('🤖 AI 语义排序...');

  try {
    const aiResults = callAIForRerank(query, candidates);
    if (aiResults && aiResults.results) {
      results = aiResults.results
        .filter(r => r.score > 0.3)
        .sort((a, b) => b.score - a.score)
        .slice(0, MAX_RESULTS)
        .map(r => ({
          ...candidates[r.index - 1],
          aiScore: r.score,
          aiReason: r.reason
        }));
      console.log(`   AI 排序完成，保留 ${results.length} 条\n`);
    }
  } catch (e) {
    console.log('   使用关键词排序结果\n');
  }

  // 步骤6：格式化输出
  const output = formatResults(query, results);
  console.log(output);

  const elapsed = Date.now() - startTime;
  console.log(`\n⏱️ 检索耗时: ${elapsed}ms`);

  return { query, results, output, elapsed };
}

// 运行
const query = process.argv[2];
const libraryPath = process.argv[3];
search(query, libraryPath).catch(console.error);
