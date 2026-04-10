/**
 * 数字图书馆索引构建脚本
 * 功能：
 * 1. 扫描所有 .md 书籍文件
 * 2. 提取书籍元数据
 * 3. 解析章节结构（标题层级、案例编号）
 * 4. 构建 MiniSearch 全文索引
 * 5. 输出 index.json 和 sections.json
 */

const fs = require('fs');
const path = require('path');

// 引入 MiniSearch
// npm install minisearch
const MiniSearch = require('minisearch');

// 配置
// 支持命令行参数指定书库路径
const LIBRARY_PATH = process.argv[2] || path.join(__dirname, '..');
const OUTPUT_DIR = __dirname;

// 书籍分类映射
const CATEGORY_MAP = {
  '《刑事审判参考》': '刑事审判参考',
  '《刑事审判方法》': '刑事审判方法',
  '《刑事审判实务规范》': '刑事审判实务规范',
  '司法解释全书': '司法解释',
  '民商事审判实务': '民商事审判',
  '审委会手册': '审委会手册',
  '法院培训统编教材': '法院培训教材'
};

// 书籍ID生成
function generateBookId(title) {
  return title
    .replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '_')
    .replace(/_+/g, '_')
    .substring(0, 50);
}

// 从文件名提取书籍信息
function parseBookInfo(filePath, fileName) {
  let title = fileName.replace(/\.md$/, '');

  // 提取年份
  const yearMatch = title.match(/(\d{4})年?/);
  const year = yearMatch ? parseInt(yearMatch[1]) : null;

  // 提取分类（使用完整路径匹配）
  let category = '其他';
  for (const [key, value] of Object.entries(CATEGORY_MAP)) {
    if (filePath.includes(key)) {
      category = value;
      break;
    }
  }

  // 提取辑号（用于刑事审判参考）
  const jiMatch = title.match(/总第(\d+)辑?/);
  const ji = jiMatch ? jiMatch[1] : null;

  return { title, year, category, ji };
}

// 解析章节标题和案例编号
function parseSections(content) {
  const sections = [];
  const lines = content.split('\n');

  // 匹配标题行（# 开头）
  const headingRegex = /^(#{1,6})\s+(.+)$/;
  // 匹配无序列表项（- 开头）
  const listItemRegex = /^[-*]\s+(.+)$/;
  // 匹配案例编号
  const caseRegex = /\[?第(\d+)[号辑]\]/g;
  // 检查是否包含案例编号
  const hasCaseRegex = /\[?第(\d+)[号辑]\]/;

  let currentSection = null;
  let currentSectionLine = 0;

  for (let i = 0; i < lines.length; i++) {
    const lineNum = i + 1;
    const line = lines[i];
    const headingMatch = line.match(headingRegex);
    const listMatch = line.match(listItemRegex);

    if (headingMatch) {
      const level = headingMatch[1].length;
      const heading = headingMatch[2].trim();

      // 提取案例编号
      const caseIds = [];
      let caseMatch;
      while ((caseMatch = caseRegex.exec(heading)) !== null) {
        caseIds.push(`第${caseMatch[1]}号`);
      }

      sections.push({
        level,
        heading,
        line_start: lineNum,
        case_ids: caseIds,
        is_case: caseIds.length > 0,
        is_heading: true
      });

      currentSection = heading;
      currentSectionLine = lineNum;
    } else if (currentSection) {
      // 在当前章节下，处理任何包含案例编号的行
      const trimmedLine = line.trim();

      if (trimmedLine && hasCaseRegex.test(trimmedLine)) {
        // 提取案例编号
        const caseIds = [];
        let caseMatch;
        while ((caseMatch = caseRegex.exec(trimmedLine)) !== null) {
          caseIds.push(`第${caseMatch[1]}号`);
        }

        if (caseIds.length > 0) {
          sections.push({
            level: 3,
            heading: trimmedLine,
            line_start: lineNum,
            case_ids: caseIds,
            is_case: true,
            is_heading: false,
            parent_section: currentSection,
            parent_line: currentSectionLine
          });
        }
      }
    }
  }

  return sections;
}

// 构建单本书籍的索引文档
function buildBookDocument(bookInfo, filePath, sections) {
  const doc = {
    id: generateBookId(bookInfo.title),
    title: bookInfo.title,
    path: filePath,
    relativePath: path.relative(LIBRARY_PATH, filePath),
    category: bookInfo.category,
    year: bookInfo.year,
    ji: bookInfo.ji,
    sectionCount: sections.length,
    caseCount: sections.filter(s => s.is_case).length,
    sections: sections
  };

  return doc;
}

// 主函数
async function buildIndex() {
  console.log('🚀 开始构建数字图书馆索引...\n');

  // 获取所有 .md 书籍文件
  const allFiles = getAllMdFiles(LIBRARY_PATH);
  const bookFiles = allFiles.filter(f =>
    !f.includes('.obsidian') &&
    !f.includes('.git') &&
    !f.includes('copilot/') &&
    !f.includes('欢迎.md') &&
    !f.includes('2026-04-07.md') &&
    !f.includes('CHANGELOG.md') &&
    !f.includes('README.md') &&
    !f.includes('Clip ') &&
    !f.includes('Emojify') &&
    !f.includes('Explain ') &&
    !f.includes('Fix grammar') &&
    !f.includes('Generate ') &&
    !f.includes('Make ') &&
    !f.includes('Remove URLs') &&
    !f.includes('Rewrite ') &&
    !f.includes('Simplify') &&
    !f.includes('Summarize') &&
    !f.includes('Translate ')
  );

  console.log(`📚 发现 ${bookFiles.length} 本书籍\n`);

  // 初始化 MiniSearch
  const miniSearch = new MiniSearch({
    fields: ['title', 'headings_text', 'case_ids_text'],
    storeFields: ['id', 'title', 'relativePath', 'category', 'year', 'heading', 'lineNum', 'case_ids']
  });

  // 索引数据
  const booksIndex = [];
  const sectionsIndex = [];

  // 处理每本书
  for (const filePath of bookFiles) {
    const fileName = path.basename(filePath);
    console.log(`📖 处理: ${fileName}`);

    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const bookInfo = parseBookInfo(filePath, fileName);
      const sections = parseSections(content);

      // 构建书籍文档
      const bookDoc = buildBookDocument(bookInfo, filePath, sections);
      booksIndex.push(bookDoc);

      // 为每个章节创建索引文档
      for (const section of sections) {
        // 提取章节内容片段（简化处理：使用标题）
        const headingsText = section.heading;
        const caseIdsText = section.case_ids.join(' ');

        const sectionDoc = {
          id: `${bookDoc.id}_${section.line_start}`,
          book_id: bookDoc.id,
          book_title: bookDoc.title,
          relativePath: bookDoc.relativePath,
          category: bookDoc.category,
          year: bookDoc.year,
          heading: section.heading,
          heading_level: section.level,
          lineNum: section.line_start,
          case_ids: section.case_ids,
          headings_text: headingsText,
          case_ids_text: caseIdsText
        };

        sectionsIndex.push(sectionDoc);

        // 添加到 MiniSearch
        miniSearch.add(sectionDoc);
      }

      console.log(`   ✅ ${sections.length} 个章节, ${bookDoc.caseCount} 个案例\n`);

    } catch (error) {
      console.error(`   ❌ 处理失败: ${error.message}\n`);
    }
  }

  // 保存索引文件
  console.log('💾 保存索引文件...');

  // 1. 保存书籍元数据索引
  fs.writeFileSync(
    path.join(OUTPUT_DIR, 'index.json'),
    JSON.stringify({
      version: '1.0',
      buildAt: new Date().toISOString(),
      libraryPath: LIBRARY_PATH,
      totalBooks: booksIndex.length,
      totalSections: sectionsIndex.length,
      books: booksIndex
    }, null, 2),
    'utf-8'
  );

  // 2. 保存章节结构索引
  fs.writeFileSync(
    path.join(OUTPUT_DIR, 'sections.json'),
    JSON.stringify({
      version: '1.0',
      buildAt: new Date().toISOString(),
      sections: sectionsIndex
    }, null, 2),
    'utf-8'
  );

  // 3. 保存 MiniSearch 索引
  const miniSearchState = miniSearch.toJSON();
  fs.writeFileSync(
    path.join(OUTPUT_DIR, 'search-index.json'),
    JSON.stringify({
      version: '1.0',
      buildAt: new Date().toISOString(),
      index: miniSearchState
    }, null, 2),
    'utf-8'
  );

  console.log('✅ 索引构建完成！\n');
  console.log('📊 统计:');
  console.log(`   - 书籍数量: ${booksIndex.length}`);
  console.log(`   - 章节数量: ${sectionsIndex.length}`);
  console.log(`   - 输出目录: ${OUTPUT_DIR}`);

  // 按分类统计
  const categoryStats = {};
  for (const book of booksIndex) {
    categoryStats[book.category] = (categoryStats[book.category] || 0) + 1;
  }
  console.log('\n📚 分类统计:');
  for (const [cat, count] of Object.entries(categoryStats)) {
    console.log(`   - ${cat}: ${count} 本`);
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

// 运行
buildIndex().catch(console.error);
