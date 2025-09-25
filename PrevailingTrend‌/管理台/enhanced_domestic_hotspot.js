// 加载增强版国内热点数据
async function loadEnhancedDomesticHotspotData() {
    const contentArea = document.querySelector(".content-area");
    
    // 显示加载状态
    contentArea.innerHTML = `
        <div class="content-header">
            <h2><i class="bi bi-fire"></i> 增强版国内热点数据</h2>
            <p class="text-muted">第一层模块 - 基础数据采集</p>
        </div>
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-3">正在加载增强版国内热点数据...</p>
            <p class="text-muted">尝试连接API: /api/domestic-hotspot</p>
        </div>
    `;
    
    try {
        console.log("开始尝试连接增强版国内热点数据API...");
        
        // 尝试从增强版国内热点数据API获取数据
        const response = await fetch("/api/domestic-hotspot", {
            method: "GET",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        });
        
        console.log("API响应状态:", response.status);
        
        let hotspotData = [];
        let statsData = {};
        
        if (response.ok) {
            const result = await response.json();
            console.log("API返回数据:", result);
            if (result.success && result.data) {
                hotspotData = result.data;
                console.log("成功获取热点数据，数量:", hotspotData.length);
            }
        } else {
            console.log("API响应错误:", response.status, response.statusText);
        }
        
        // 获取统计数据
        try {
            const statsResponse = await fetch("/api/domestic-hotspot/stats", {
                method: "GET",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            });
            
            if (statsResponse.ok) {
                const statsResult = await statsResponse.json();
                if (statsResult.success && statsResult.data) {
                    statsData = statsResult.data;
                    console.log("成功获取统计数据:", statsData);
                }
            }
        } catch (statsError) {
            console.log("获取统计数据失败:", statsError);
        }
        
        // 如果API不可用，使用模拟数据
        if (hotspotData.length === 0) {
            console.log("API数据为空，使用模拟数据");
            hotspotData = generateMockHotspotData();
            statsData = generateMockStatsData();
        }
        
        // 按类别分组数据
        const categoryGroups = {};
        hotspotData.forEach(item => {
            const category = item.category || "其他";
            if (!categoryGroups[category]) {
                categoryGroups[category] = [];
            }
            categoryGroups[category].push(item);
        });
        
        console.log("数据分组完成:", Object.keys(categoryGroups));
        
        // 生成HTML内容
        const categoryCards = Object.keys(categoryGroups).map(category => {
            const items = categoryGroups[category];
            const itemsHtml = items.slice(0, 5).map(item => `
                <div class="list-group-item">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <h6 class="mb-1">${item.url ? `<a href="${item.url}" target="_blank" rel="noopener">${item.title}</a>` : item.title}</h6>
                            <p class="mb-1 small">${item.content}</p>
                            <small class="text-muted">来源: ${item.source} | ${item.publishTime}</small>
                        </div>
                        <div class="text-end">
                            <span class="badge bg-${getSentimentColor(item.sentiment)}">${item.sentiment}</span>
                            <br>
                            <small class="text-muted">热度: ${Math.round(item.heatScore)}</small>
                        </div>
                    </div>
                </div>
            `).join("");
            
            return `
                <div class="col-md-6 mb-4">
                    <div class="card">
                        <div class="card-header bg-${getCategoryColor(category)} text-white d-flex justify-content-between">
                            <span><i class="bi bi-${getCategoryIcon(category)}"></i> ${category}</span>
                            <span class="badge bg-light text-dark">${items.length}</span>
                        </div>
                        <div class="card-body" style="max-height: 420px; overflow-y: auto;">
                            <div class="list-group list-group-flush">
                                ${itemsHtml}
                            </div>
                            ${items.length > 5 ? `<div class="text-center mt-2"><small class="text-muted">显示前5个，共${items.length}个</small></div>` : ""}
                        </div>
                    </div>
                </div>
            `;
        }).join("");
        
        const dataSource = hotspotData.length > 0 && hotspotData[0].id ? "增强版国内热点数据API" : "模拟数据";
        
        contentArea.innerHTML = `
            <div class="content-header">
                <h2><i class="bi bi-fire"></i> 增强版国内热点数据</h2>
                <p class="text-muted">第一层模块 - 基础数据采集</p>
                <div class="d-flex justify-content-between align-items-center">
                    <span class="badge bg-info">共 ${hotspotData.length} 条热点资讯</span>
                    <div>
                        <span class="badge bg-secondary me-2">数据源: ${dataSource}</span>
                        <button class="btn btn-sm btn-outline-primary" onclick="loadEnhancedDomesticHotspotData()">
                            <i class="bi bi-arrow-clockwise"></i> 刷新数据
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- 统计数据卡片 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h4 class="text-primary">${statsData.total_hotspots || hotspotData.length}</h4>
                            <p class="mb-0">总数据量</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h4 class="text-success">${statsData.positive_count || 0}</h4>
                            <p class="mb-0">积极情绪</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h4 class="text-warning">${statsData.neutral_count || 0}</h4>
                            <p class="mb-0">中性情绪</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h4 class="text-danger">${statsData.negative_count || 0}</h4>
                            <p class="mb-0">消极情绪</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 分类数据展示 -->
            <div class="row">
                ${categoryCards}
            </div>
            
            <!-- 详细统计 -->
            <div class="row mt-4">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header bg-info text-white">
                            <i class="bi bi-bar-chart"></i> 详细统计信息
                        </div>
                        <div class="card-body">
                            <div class="row text-center">
                                <div class="col-md-2">
                                    <div class="border rounded p-3">
                                        <h5 class="text-primary">${statsData.finance_hotspots || 0}</h5>
                                        <p class="mb-0 small">财经热点</p>
                                    </div>
                                </div>
                                <div class="col-md-2">
                                    <div class="border rounded p-3">
                                        <h5 class="text-success">${statsData.policy_hotspots || 0}</h5>
                                        <p class="mb-0 small">政策动态</p>
                                    </div>
                                </div>
                                <div class="col-md-2">
                                    <div class="border rounded p-3">
                                        <h5 class="text-info">${statsData.market_hotspots || 0}</h5>
                                        <p class="mb-0 small">市场新闻</p>
                                    </div>
                                </div>
                                <div class="col-md-2">
                                    <div class="border rounded p-3">
                                        <h5 class="text-warning">${statsData.industry_hotspots || 0}</h5>
                                        <p class="mb-0 small">行业资讯</p>
                                    </div>
                                </div>
                                <div class="col-md-2">
                                    <div class="border rounded p-3">
                                        <h5 class="text-secondary">${statsData.company_hotspots || 0}</h5>
                                        <p class="mb-0 small">公司热点</p>
                                    </div>
                                </div>
                                <div class="col-md-2">
                                    <div class="border rounded p-3">
                                        <h5 class="text-dark">${statsData.macro_hotspots || 0}</h5>
                                        <p class="mb-0 small">宏观经济</p>
                                    </div>
                                </div>
                            </div>
                            <div class="row text-center mt-3">
                                <div class="col-md-6">
                                    <div class="border rounded p-3">
                                        <h5 class="text-primary">${statsData.investment_hotspots || 0}</h5>
                                        <p class="mb-0 small">投资热点</p>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="border rounded p-3">
                                        <h5 class="text-success">${statsData.market_sentiment || "积极"}</h5>
                                        <p class="mb-0 small">整体市场情绪</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="alert alert-info mt-3">
                <i class="bi bi-info-circle"></i>
                增强版国内热点数据 | 数据来源：${dataSource} | 更新时间：${statsData.last_update || new Date().toLocaleString()}
            </div>
        `;
        
    } catch (error) {
        console.error("加载增强版国内热点数据失败:", error);
        
        // 使用模拟数据作为备用方案
        const hotspotData = generateMockHotspotData();
        const statsData = generateMockStatsData();
        
        const categoryGroups = {};
        hotspotData.forEach(item => {
            const category = item.category || "其他";
            if (!categoryGroups[category]) {
                categoryGroups[category] = [];
            }
            categoryGroups[category].push(item);
        });
        
        const categoryCards = Object.keys(categoryGroups).map(category => {
            const items = categoryGroups[category];
            const itemsHtml = items.slice(0, 5).map(item => `
                <div class="list-group-item">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <h6 class="mb-1">${item.url ? `<a href="${item.url}" target="_blank" rel="noopener">${item.title}</a>` : item.title}</h6>
                            <p class="mb-1 small">${item.content}</p>
                            <small class="text-muted">来源: ${item.source} | ${item.publishTime}</small>
                        </div>
                        <div class="text-end">
                            <span class="badge bg-${getSentimentColor(item.sentiment)}">${item.sentiment}</span>
                            <br>
                            <small class="text-muted">热度: ${Math.round(item.heatScore)}</small>
                        </div>
                    </div>
                </div>
            `).join("");
            
            return `
                <div class="col-md-6 mb-4">
                    <div class="card">
                        <div class="card-header bg-${getCategoryColor(category)} text-white d-flex justify-content-between">
                            <span><i class="bi bi-${getCategoryIcon(category)}"></i> ${category}</span>
                            <span class="badge bg-light text-dark">${items.length}</span>
                        </div>
                        <div class="card-body" style="max-height: 420px; overflow-y: auto;">
                            <div class="list-group list-group-flush">
                                ${itemsHtml}
                            </div>
                            ${items.length > 5 ? `<div class="text-center mt-2"><small class="text-muted">显示前5个，共${items.length}个</small></div>` : ""}
                        </div>
                    </div>
                </div>
            `;
        }).join("");
        
        contentArea.innerHTML = `
            <div class="content-header">
                <h2><i class="bi bi-fire"></i> 增强版国内热点数据</h2>
                <p class="text-muted">第一层模块 - 基础数据采集</p>
                <div class="d-flex justify-content-between align-items-center">
                    <span class="badge bg-info">共 ${hotspotData.length} 条热点资讯</span>
                    <div>
                        <span class="badge bg-warning me-2">使用模拟数据</span>
                        <button class="btn btn-sm btn-outline-primary" onclick="loadEnhancedDomesticHotspotData()">
                            <i class="bi bi-arrow-clockwise"></i> 重试连接API
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="alert alert-warning">
                <i class="bi bi-exclamation-triangle"></i>
                <strong>API连接失败:</strong> ${error.message}
                <br><small>当前显示模拟数据。</small>
            </div>
            
            <!-- 统计数据卡片 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h4 class="text-primary">${statsData.total_hotspots || hotspotData.length}</h4>
                            <p class="mb-0">总数据量</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h4 class="text-success">${statsData.positive_count || 0}</h4>
                            <p class="mb-0">积极情绪</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h4 class="text-warning">${statsData.neutral_count || 0}</h4>
                            <p class="mb-0">中性情绪</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h4 class="text-danger">${statsData.negative_count || 0}</h4>
                            <p class="mb-0">消极情绪</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 分类数据展示 -->
            <div class="row">
                ${categoryCards}
            </div>
            
            <div class="alert alert-info mt-3">
                <i class="bi bi-info-circle"></i>
                增强版国内热点数据 | 数据来源：模拟数据 | 更新时间：${new Date().toLocaleString()}
            </div>
        `;
    }
}

// 辅助函数
function getSentimentColor(sentiment) {
    switch(sentiment) {
        case "积极": return "success";
        case "中性": return "warning";
        case "消极": return "danger";
        default: return "secondary";
    }
}

function getCategoryColor(category) {
    switch(category) {
        case "财经热点": return "primary";
        case "政策动态": return "success";
        case "市场新闻": return "info";
        case "行业资讯": return "warning";
        case "公司热点": return "secondary";
        case "宏观经济": return "dark";
        case "投资热点": return "danger";
        default: return "light";
    }
}

function getCategoryIcon(category) {
    switch(category) {
        case "财经热点": return "currency-dollar";
        case "政策动态": return "file-earmark-text";
        case "市场新闻": return "newspaper";
        case "行业资讯": return "building";
        case "公司热点": return "briefcase";
        case "宏观经济": return "graph-up";
        case "投资热点": return "trending-up";
        default: return "circle";
    }
}

// 生成模拟数据
function generateMockHotspotData() {
    return [
        {
            id: "FIN_0001",
            title: "央行货币政策调整分析 - 1",
            category: "财经热点",
            content: "这是一条关于央行货币政策调整分析的详细分析内容，包含市场数据、专家观点和投资建议...",
            heatScore: 85.5,
            sentiment: "积极",
            source: "新华财经",
            publishTime: "2025-09-20 14:30:25"
        },
        {
            id: "POL_0001",
            title: "金融监管新政策 - 1",
            category: "政策动态",
            content: "关于金融监管新政策的最新政策解读和影响分析，包括政策背景、实施细节和市场影响...",
            heatScore: 92.3,
            sentiment: "积极",
            source: "人民日报",
            publishTime: "2025-09-20 13:15:10"
        },
        {
            id: "MKT_0001",
            title: "股市收盘分析 - 1",
            category: "市场新闻",
            content: "今日股市收盘分析的详细市场分析和投资建议，包含技术分析和基本面分析...",
            heatScore: 78.9,
            sentiment: "中性",
            source: "财新网",
            publishTime: "2025-09-20 15:45:30"
        },
        {
            id: "IND_0001",
            title: "科技行业发展 - 1",
            category: "行业资讯",
            content: "关于科技行业发展的最新行业分析和发展前景，包含行业数据和趋势预测...",
            heatScore: 88.7,
            sentiment: "积极",
            source: "中国产经新闻",
            publishTime: "2025-09-20 12:20:15"
        },
        {
            id: "COM_0001",
            title: "上市公司业绩 - 1",
            category: "公司热点",
            content: "关于上市公司业绩的详细报道和分析，包含公司背景和影响评估...",
            heatScore: 75.2,
            sentiment: "积极",
            source: "公司公告",
            publishTime: "2025-09-20 11:30:45"
        },
        {
            id: "MAC_0001",
            title: "GDP增长数据 - 1",
            category: "宏观经济",
            content: "关于GDP增长数据的详细数据分析和经济解读，包含历史对比和趋势分析...",
            heatScore: 90.1,
            sentiment: "积极",
            source: "国家统计局",
            publishTime: "2025-09-20 10:15:20"
        },
        {
            id: "INV_0001",
            title: "投资策略分析 - 1",
            category: "投资热点",
            content: "关于投资策略分析的专业分析和投资建议，包含风险评估和收益预期...",
            heatScore: 82.6,
            sentiment: "中性",
            source: "投资机构",
            publishTime: "2025-09-20 09:45:55"
        }
    ];
}

function generateMockStatsData() {
    return {
        total_hotspots: 550,
        finance_hotspots: 100,
        policy_hotspots: 80,
        market_hotspots: 120,
        industry_hotspots: 100,
        company_hotspots: 50,
        macro_hotspots: 50,
        investment_hotspots: 50,
        positive_count: 201,
        neutral_count: 216,
        negative_count: 133,
        market_sentiment: "积极",
        last_update: new Date().toLocaleString()
    };
}
