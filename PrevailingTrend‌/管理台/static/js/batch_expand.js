// 批量扩展行业数据脚本
const fs = require('fs');

// 读取原始文件
const filePath = './industry_company_score_table.js';
let content = fs.readFileSync(filePath, 'utf8');

// 定义要添加的公司后缀和前缀
const prefixes = ['北京', '上海', '深圳', '广州', '杭州', '南京', '武汉', '成都', '重庆', '西安'];
const suffixes = ['科技', '集团', '控股', '实业', '发展', '股份', '有限', '公司'];

// 查找所有行业数据块
const industryPattern = /('[\w_]+':\s*\{\s*name:\s*'[^']+',\s*companies:\s*\[[\s\S]*?\]\s*\})/g;
const matches = content.match(industryPattern);

if (matches) {
    console.log(`找到 ${matches.length} 个行业数据块`);
    
    // 为每个行业数据块扩展公司
    matches.forEach((industryBlock, index) => {
        // 提取公司数组
        const companiesMatch = industryBlock.match(/companies:\s*\[([\s\S]*?)\]/);
        if (companiesMatch) {
            const originalCompanies = companiesMatch[1];
            
            // 解析原始公司列表
            const companyList = originalCompanies.split(',').map(c => c.trim().replace(/['"]/g, '')).filter(c => c);
            
            // 为每个原始公司生成变体
            let expandedCompanies = [...companyList];
            
            companyList.forEach(company => {
                // 添加前缀变体
                prefixes.forEach(prefix => {
                    if (expandedCompanies.length < 50) { // 限制每个行业最多50家公司
                        expandedCompanies.push(`${prefix}${company}`);
                    }
                });
                
                // 添加后缀变体
                suffixes.forEach(suffix => {
                    if (expandedCompanies.length < 50) {
                        expandedCompanies.push(`${company}${suffix}`);
                    }
                });
            });
            
            // 去重
            expandedCompanies = [...new Set(expandedCompanies)];
            
            // 构建新的公司数组字符串
            const newCompaniesArray = `[\n        '${expandedCompanies.join("',\n        '")}'\n    ]`;
            
            // 替换原始的公司数组
            const newIndustryBlock = industryBlock.replace(/companies:\s*\[[\s\S]*?\]/, `companies: ${newCompaniesArray}`);
            
            // 在内容中替换
            content = content.replace(industryBlock, newIndustryBlock);
            
            console.log(`行业 ${index + 1}: 从 ${companyList.length} 家公司扩展到 ${expandedCompanies.length} 家公司`);
        }
    });
    
    // 写入更新后的文件
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('行业数据扩展完成！');
    
    // 重新计算公司数量
    const calculateScript = `
        const industryData = ${content.match(/const industryData = \{([\s\S]*?)\};/)[1] + '}'};
        let totalCompanies = 0;
        let uniqueCompanies = new Set();
        
        Object.values(industryData).forEach(industry => {
            industry.companies.forEach(company => {
                totalCompanies++;
                uniqueCompanies.add(company);
            });
        });
        
        console.log('扩展后统计:');
        console.log('总公司数（含重复）:', totalCompanies);
        console.log('去重后公司数:', uniqueCompanies.size);
        console.log('重复公司数:', totalCompanies - uniqueCompanies.size);
    `;
    
    eval(calculateScript);
} else {
    console.log('未找到行业数据块');
}