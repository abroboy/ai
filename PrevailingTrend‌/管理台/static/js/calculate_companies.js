// 计算行业数据中的公司数量
const fs = require('fs');

// 读取实际的行业数据文件
const industryFileContent = fs.readFileSync('./industry_company_score_table.js', 'utf8');

// 简单统计公司数量
let totalCompanies = 0;
let allCompanies = new Set();

// 查找所有公司数组
const companyArrays = industryFileContent.match(/companies:\s*\[[^\]]*\]/g);
if (companyArrays) {
    companyArrays.forEach(arrayStr => {
        // 提取公司名称
        const companies = arrayStr.match(/'([^']+)'/g);
        if (companies) {
            totalCompanies += companies.length;
            companies.forEach(company => {
                const name = company.replace(/'/g, '');
                allCompanies.add(name);
            });
        }
    });
}

console.log('总行业数:', companyArrays ? companyArrays.length : 0);
console.log('总公司数（含重复）:', totalCompanies);
console.log('去重后公司数:', allCompanies.size);
console.log('重复公司数:', totalCompanies - allCompanies.size);