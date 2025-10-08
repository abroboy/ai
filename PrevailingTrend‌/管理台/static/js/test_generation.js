// 测试数据生成功能
const fs = require('fs');

// 读取行业数据文件
const industryFileContent = fs.readFileSync('./industry_company_score_table.js', 'utf8');

// 提取generateAStockCompanies函数
const functionMatch = industryFileContent.match(/function generateAStockCompanies\(\) \{[\s\S]*?\n\}/);
if (functionMatch) {
    // 创建一个简单的测试环境
    const testCode = `
        // 模拟行业数据
        const industryData = {
            'banking': { name: '银行', companies: ['工商银行', '建设银行'] },
            'securities': { name: '证券', companies: ['中信证券', '海通证券'] }
        };
        
        // 模拟辅助函数
        function generateStockCode(index, industry) { return '60000' + index; }
        function generateFinancialScore() { return Math.random() * 100; }
        function generateMarketScore() { return Math.random() * 100; }
        function generateIndustryScore() { return Math.random() * 100; }
        function calculateCompositeScore(f, m, i) { return (f + m + i) / 3; }
        function generateRecommendation(score) { return score > 60 ? '推荐' : '观望'; }
        function generateMarketCap() { return Math.random() * 1000; }
        function generatePERatio() { return Math.random() * 50; }
        function generatePBRatio() { return Math.random() * 10; }
        function generateROE() { return Math.random() * 30; }
        function generateRevenueGrowth() { return Math.random() * 50 - 10; }
        function generateProfitGrowth() { return Math.random() * 60 - 15; }
        function generateMarketSector() { return '主板'; }
        
        ${functionMatch[0]}
        
        // 添加createCompanyData函数
        function createCompanyData(id, companyName, industryInfo, industryKey, index) {
            const stockCode = generateStockCode(index, industryKey);
            const financialScore = generateFinancialScore(companyName, industryKey);
            const marketScore = generateMarketScore(companyName, industryKey);
            const industryScore = generateIndustryScore(industryKey);
            const compositeScore = calculateCompositeScore(financialScore, marketScore, industryScore);
            
            return {
                id: id,
                companyName: companyName,
                stockCode: stockCode,
                industry: industryInfo.name,
                industryKey: industryKey,
                marketSector: generateMarketSector(stockCode),
                financialScore: financialScore,
                marketScore: marketScore,
                industryScore: industryScore,
                compositeScore: compositeScore,
                recommendation: generateRecommendation(compositeScore),
                marketCap: generateMarketCap(companyName),
                peRatio: generatePERatio(companyName),
                pbRatio: generatePBRatio(companyName),
                roe: generateROE(companyName),
                revenueGrowth: generateRevenueGrowth(companyName),
                profitGrowth: generateProfitGrowth(companyName)
            };
        }
        
        // 测试生成
        const companies = generateAStockCompanies();
        console.log('生成公司总数:', companies.length);
        console.log('前5家公司:', companies.slice(0, 5).map(c => c.companyName));
    `;
    
    eval(testCode);
} else {
    console.error('无法找到generateAStockCompanies函数');
}