// 测试行业分值表功能
const fs = require('fs');
const path = require('path');

// 读取行业公司分值表文件
const filePath = path.join(__dirname, 'industry_company_score_table.js');
const fileContent = fs.readFileSync(filePath, 'utf8');

// 检查关键函数是否存在
const functionsToCheck = [
    'showHeatmap',
    'showIndustryScores', 
    'generateHeatmapData',
    'generateIndustryScoresTable',
    'calculateIndustryScores',
    'getIndustryName',
    'getScoreBadgeClass',
    'getRecommendation',
    'getRecommendationClass',
    'viewIndustryDetail'
];

console.log('=== 行业分值表功能测试 ===');
console.log('检查的函数列表:');

let missingFunctions = [];
let foundFunctions = [];

functionsToCheck.forEach(funcName => {
    const regex = new RegExp(`function ${funcName}|const ${funcName} =|let ${funcName} =`);
    if (regex.test(fileContent)) {
        console.log(`✓ ${funcName} - 存在`);
        foundFunctions.push(funcName);
    } else {
        console.log(`✗ ${funcName} - 缺失`);
        missingFunctions.push(funcName);
    }
});

console.log('\n=== 测试结果 ===');
console.log(`找到的函数: ${foundFunctions.length}/${functionsToCheck.length}`);
console.log(`缺失的函数: ${missingFunctions.length}`);

if (missingFunctions.length > 0) {
    console.log('缺失的函数列表:');
    missingFunctions.forEach(func => console.log(`  - ${func}`));
} else {
    console.log('✓ 所有函数都存在，功能完整！');
}

// 测试行业名称映射
console.log('\n=== 行业名称映射测试 ===');
const industryIds = ['banking', 'securities', 'insurance', 'real_estate', 'construction'];
industryIds.forEach(id => {
    const nameRegex = new RegExp(`'${id}':\\s*'([^']+)'`);
    const match = fileContent.match(nameRegex);
    if (match) {
        console.log(`✓ ${id} -> ${match[1]}`);
    } else {
        console.log(`✗ ${id} -> 未找到映射`);
    }
});

console.log('\n=== 测试完成 ===');