// 加载增强版国内热点数据
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
    
    // 数据标准化函数
    const normalizeData = (data) => {
        return (data || []).map(item => {
            const changeMatch = item.content?.match(/涨跌幅:\s*([\d.]+)%/);
            const changePercent = changeMatch ? parseFloat(changeMatch[1]) : 0;
            
            return {
                id: String(item.id || `ID_${Math.random().toString(36).slice(2, 10)}`),
                title: String(item.title || '未命名热点'),
                category: String(item.category || item.keywords?.[0] || '综合资讯'),
                content: String(item.content || '暂无详细内容'),
                publishTime: item.publishTime || new Date().toLocaleString(),
                source: String(item.source || '数据源未知'),
                heatScore: Math.max(1, Number(item.heatScore) || Math.round(Math.abs(changePercent) * 2)),
                sentiment: ['积极','中性','消极'].includes(item.sentiment) ? item.sentiment : '中性',
                keywords: Array.isArray(item.keywords) ? 
                    item.keywords.filter(k => k && String(k).trim()) : ['热门']
            };
        });
    };

    // 处理API请求
    fetch('/api/domestic-hotspot')
        .then(async response => {
            if (!response.ok) {
                const err = new Error(`HTTP错误! 状态: ${response.status}`);
                err.response = await response.json().catch(() => null);
                throw err;
            }
            return response.json();
        })
        .then(result => {
            if (!result || typeof result !== 'object') {
                throw new Error('无效的API响应结构');
            }

            const normalizedData = normalizeData(result.data);
            
            try {
                renderData(normalizedData);
            } catch (e) {
                console.error('渲染失败:', e);
                showError(contentArea, e, {
                    title: '数据渲染异常',
                    dataPreview: normalizedData.slice(0, 3)
                });
            }
        })
        .catch(error => {
            console.error('API请求失败:', error);
            showError(contentArea, error, {
                title: '数据加载失败',
                apiResponse: error.response
            });
        });

    // 显示错误函数
    function showError(container, error, {title, dataPreview, apiResponse}) {
        container.innerHTML = `
            <div class="alert alert-danger">
                <h4>${title}</h4>
                <p>${error.message}</p>
                ${dataPreview ? `
                <div class="mt-3">
                    <button class="btn btn-sm btn-outline-primary" 
                            onclick="this.nextElementSibling.style.display='block'">
                        显示数据预览
                    </button>
                    <pre style="display:none" class="mt-2 p-2 bg-light">
                        ${JSON.stringify(dataPreview, null, 2)}
                    </pre>
                </div>
                ` : ''}
                ${apiResponse ? `
                <div class="mt-3">
                    <button class="btn btn-sm btn-outline-secondary" 
                            onclick="this.nextElementSibling.style.display='block'">
                        显示API响应
                    </button>
                    <pre style="display:none" class="mt-2 p-2 bg-light">
                        ${JSON.stringify(apiResponse, null, 2)}
                    </pre>
                </div>
                ` : ''}
                <div class="mt-3">
                    <button class="btn btn-primary me-2" onclick="loadEnhancedDomesticHotspotData()">
                        <i class="bi bi-arrow-clockwise"></i> 重试
                    </button>
                </div>
            </div>
        `;
    }
}

// 数据渲染函数
function renderData(data) {
    const contentArea = document.querySelector(".content-area");
    if (!contentArea || !Array.isArray(data)) return;

    // 按热度排序
    const sortedData = [...data].sort((a, b) => b.heatScore - a.heatScore);
    
    // 按类别分组
    const categories = {};
    sortedData.forEach(item => {
        const category = item.category || '其他';
        if (!categories[category]) {
            categories[category] = [];
        }
        categories[category].push(item);
    });

    // 构建HTML内容
    let html = `
        <div class="content-header mb-4">
            <h2><i class="bi bi-fire text-danger"></i> 国内热点数据</h2>
            <p class="text-muted">共 ${data.length} 条数据</p>
        </div>
        
        <div class="row g-3">
    `;

    // 添加分类卡片
    Object.entries(categories).forEach(([category, items]) => {
        const topItem = items[0];
        html += `
            <div class="col-md-6 col-lg-4">
                <div class="card h-100">
                    <div class="card-header bg-light">
                        <h5 class="card-title mb-0">
                            <i class="bi bi-tag"></i> ${category}
                            <span class="badge bg-primary float-end">${items.length}</span>
                        </h5>
                    </div>
                    <div class="card-body">
                        <h6>${topItem.title}</h6>
                        <p class="small text-muted">${topItem.content}</p>
                        <div class="d-flex justify-content-between small">
                            <span class="text-muted">${topItem.source}</span>
                            <span class="text-primary">
                                <i class="bi bi-fire"></i> ${topItem.heatScore}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    html += `</div>`;
    contentArea.innerHTML = html;
}

// 确保函数全局可用
if (typeof window.loadEnhancedDomesticHotspotData !== 'function') {
    window.loadEnhancedDomesticHotspotData = loadEnhancedDomesticHotspotData;
}

// DOM加载完成后初始化
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(() => {
        if (typeof loadEnhancedDomesticHotspotData === 'function') {
            loadEnhancedDomesticHotspotData();
        }
    }, 100);
});