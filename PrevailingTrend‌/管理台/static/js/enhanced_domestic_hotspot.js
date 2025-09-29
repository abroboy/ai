// 国内热点数据模块 - 自包含实现
function loadEnhancedDomesticHotspotData() {
    const contentArea = document.querySelector(".content-area");
    if (!contentArea) return;
    
    // 显示加载状态
    contentArea.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-3">正在加载国内热点数据...</p>
        </div>
    `;

    // 自包含数据生成
    function generateFullDataset() {
        const industries = ['科技', '金融', '医疗', '消费', '能源', '制造', '地产', '公用事业'];
        const companies = [
            '阿里巴巴', '腾讯', '美团', '京东', '拼多多', 
            '中国平安', '招商银行', '中信证券', '贵州茅台', '五粮液'
        ];
        
        return Array.from({length: 200}, (_, i) => {
            const change = (Math.random() * 10 - 3).toFixed(2);
            return {
                id: `BK${1000 + i}`,
                title: `${companies[i % companies.length]}(${1000 + i})`,
                category: industries[i % industries.length],
                content: `当前价格: ¥${(Math.random() * 500 + 50).toFixed(2)} 涨跌幅: ${change}%`,
                source: ['东方财富', '同花顺', '雪球'][i % 3],
                heatScore: Math.abs(parseFloat(change)) * 10 + Math.random() * 50,
                sentiment: change > 0 ? '积极' : '消极',
                keywords: [industries[i % industries.length], 'A股'],
                publishTime: new Date(Date.now() - Math.random() * 86400000).toISOString()
            };
        });
    }

    // 模拟异步加载
    setTimeout(() => {
        try {
            const fullData = generateFullDataset();
            renderData(fullData);
        } catch (e) {
            contentArea.innerHTML = `
                <div class="alert alert-danger">
                    <h4>数据加载失败</h4>
                    <p>${e.message}</p>
                    <button class="btn btn-primary mt-2" onclick="loadEnhancedDomesticHotspotData()">
                        重试加载
                    </button>
                </div>
            `;
        }
    }, 800);
}

// 渲染逻辑（优化版）
function renderData(data) {
    const contentArea = document.querySelector(".content-area");
    if (!contentArea) return;
    
    // 按热度排序
    const sortedData = [...data].sort((a, b) => b.heatScore - a.heatScore);
    
    // 构建HTML
    let html = `
        <div class="market-header">
            <h2><i class="bi bi-graph-up"></i> 国内上市公司全景</h2>
            <p class="text-muted">共 ${data.length} 家公司 • 最后更新: ${new Date().toLocaleString()}</p>
        </div>
        <div class="market-grid">
    `;

    sortedData.forEach(item => {
        html += `
            <div class="market-card">
                <div class="card-header ${item.sentiment === '积极' ? 'bg-success' : 'bg-danger'}">
                    ${item.title}
                    <span class="badge bg-light text-dark float-end">
                        ${item.category}
                    </span>
                </div>
                <div class="card-body">
                    <p>${item.content}</p>
                    <div class="card-footer">
                        <small>
                            <i class="bi bi-source"></i> ${item.source} 
                            • <i class="bi bi-clock"></i> ${new Date(item.publishTime).toLocaleTimeString()}
                        </small>
                    </div>
                </div>
            </div>
        `;
    });

    html += `</div>`;
    contentArea.innerHTML = html;
}

// 全局注册
window.loadEnhancedDomesticHotspotData = loadEnhancedDomesticHotspotData;

// 页面加载后自动执行
document.addEventListener("DOMContentLoaded", () => {
    setTimeout(loadEnhancedDomesticHotspotData, 100);
});