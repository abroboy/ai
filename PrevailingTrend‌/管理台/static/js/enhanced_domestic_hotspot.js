// 加载增强版国内热点数据
// 使用传统函数替代async/await，使用XMLHttpRequest替代fetch，优化IE浏览器性能
function loadEnhancedDomesticHotspotData() {
    // 检测是否为IE浏览器
    var isIE = /Trident|MSIE/.test(navigator.userAgent);
    var contentArea = document.querySelector(".content-area");
    
    // 显示加载状态（简化版，减少DOM操作）
    displayLoadingState(contentArea);
    
    console.log("开始尝试连接增强版国内热点数据API...");
    
    // 使用XMLHttpRequest替代fetch，确保IE兼容性
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/domestic-hotspot", true);
    xhr.setRequestHeader("Accept", "application/json");
    
    // 设置超时时间，避免IE中长时间等待
    xhr.timeout = 10000; // 10秒
    
    xhr.onload = function() {
        var hotspotData = [];
        var statsData = {};
        
        if (xhr.status === 200) {
            try {
                var result = JSON.parse(xhr.responseText);
                console.log("API返回数据:", result);
                if (result.success && result.data) {
                    // 直接使用后端已映射好的数据
                    hotspotData = result.data;
                    console.log("成功获取热点数据，数量:", hotspotData.length);
                }
            } catch (e) {
                console.error("解析API数据失败:", e);
            }
        } else {
            console.log("API响应错误:", xhr.status, xhr.statusText);
        }
        
        // 处理数据并渲染页面
        processAndRenderData(hotspotData, statsData, contentArea, isIE);
    };
    
    xhr.onerror = function(error) {
        console.error("API请求错误:", error);
        handleErrorCase(contentArea, error, isIE);
    };
    
    xhr.ontimeout = function() {
        console.error("API请求超时");
        var timeoutError = new Error("请求超时，请检查网络连接");
        handleErrorCase(contentArea, timeoutError, isIE);
    };
    
    xhr.send();
}

// 显示加载状态（分离为独立函数，减少代码重复）
function displayLoadingState(contentArea) {
    // 使用简单的HTML结构，减少DOM元素数量
    contentArea.innerHTML = 
        '<div class="content-header">' +
        '    <h2><i class="bi bi-fire"></i> 增强版国内热点数据</h2>' +
        '    <p class="text-muted">第一层模块 - 基础数据采集</p>' +
        '</div>' +
        '<div class="text-center py-5">' +
        '    <div class="loading-indicator"></div>' +
        '    <p class="mt-3">正在加载数据...</p>' +
        '</div>';
}

// 处理数据并渲染页面
function processAndRenderData(hotspotData, statsData, contentArea, isIE) {
    // 如果API返回了数据，根据返回的数据生成统计信息
    if (hotspotData.length > 0) {
        // 优化统计数据生成，使用单次遍历替代多次filter
        statsData = generateStatsData(hotspotData);
    } else {
        // 如果API不可用或返回空数据，使用模拟数据
        console.log("API数据为空，使用模拟数据");
        hotspotData = generateMockHotspotData();
        statsData = generateMockStatsData();
    }
    
    // 按类别分组数据
    var categoryGroups = groupDataByCategory(hotspotData);
    console.log("数据分组完成:", Object.keys(categoryGroups));
    
    // 生成HTML内容
    var dataSource = hotspotData.length > 0 && hotspotData[0].id ? "增强版国内热点数据API" : "模拟数据";
    
    // 优化DOM渲染，使用DocumentFragment减少重绘
    renderPageContent(hotspotData, statsData, categoryGroups, dataSource, contentArea, isIE);
}

// 生成统计数据（优化版，使用单次遍历）
function generateStatsData(hotspotData) {
    var stats = {
        total_hotspots: hotspotData.length,
        finance_hotspots: 0,
        policy_hotspots: 0,
        market_hotspots: 0,
        industry_hotspots: 0,
        company_hotspots: 0,
        macro_hotspots: 0,
        investment_hotspots: 0,
        positive_count: 0,
        neutral_count: 0,
        negative_count: 0,
        last_update: new Date().toLocaleString()
    };
    
    // 使用单次遍历统计所有数据，大幅提升性能
    for (var i = 0; i < hotspotData.length; i++) {
        var item = hotspotData[i];
        
        // 统计类别数据
        switch(item.category) {
            case "财经热点": stats.finance_hotspots++;
                break;
            case "政策动态":
            case "货币政策":
            case "产业政策": stats.policy_hotspots++;
                break;
            case "市场新闻": stats.market_hotspots++;
                break;
            case "行业资讯": stats.industry_hotspots++;
                break;
            case "公司热点": stats.company_hotspots++;
                break;
            case "宏观经济": stats.macro_hotspots++;
                break;
            case "投资热点": stats.investment_hotspots++;
                break;
        }
        
        // 统计情绪数据
        switch(item.sentiment) {
            case "积极": stats.positive_count++;
                break;
            case "中性": stats.neutral_count++;
                break;
            case "消极": stats.negative_count++;
                break;
        }
    }
    
    // 计算市场情绪
    stats.market_sentiment = calculateMarketSentiment(hotspotData);
    
    return stats;
}

// 按类别分组数据
function groupDataByCategory(hotspotData) {
    var categoryGroups = {};
    
    // 使用传统for循环替代forEach，提升IE性能
    for (var i = 0; i < hotspotData.length; i++) {
        var item = hotspotData[i];
        var category = item.category || "其他";
        
        if (!categoryGroups[category]) {
            categoryGroups[category] = [];
        }
        categoryGroups[category].push(item);
    }
    
    return categoryGroups;
}

// 渲染页面内容（使用DocumentFragment优化）
function renderPageContent(hotspotData, statsData, categoryGroups, dataSource, contentArea, isIE) {
    // 创建DocumentFragment，减少DOM重绘次数
    var fragment = document.createDocumentFragment();
    var container = document.createElement('div');
    
    // 构建HTML内容
    var htmlContent = 
        '<div class="content-header">' +
        '    <h2><i class="bi bi-fire"></i> 增强版国内热点数据</h2>' +
        '    <p class="text-muted">第一层模块 - 基础数据采集</p>' +
        '    <div class="d-flex justify-content-between align-items-center">' +
        '        <span class="badge bg-info">共 ' + (hotspotData.length) + ' 条热点资讯</span>' +
        '        <div>' +
        '            <span class="badge bg-secondary me-2">数据源: ' + dataSource + '</span>' +
        '            <button class="btn btn-sm btn-outline-primary" onclick="loadEnhancedDomesticHotspotData()">' +
        '                <i class="bi bi-arrow-clockwise"></i> 刷新数据' +
        '            </button>' +
        '        </div>' +
        '    </div>' +
        '</div>' +
        
        // 统计数据卡片
        '<div class="row mb-4">' +
        '    <div class="col-md-3">' +
        '        <div class="card text-center">' +
        '            <div class="card-body">' +
        '                <h4 class="text-primary">' + (statsData.total_hotspots || hotspotData.length) + '</h4>' +
        '                <p class="mb-0">总数据量</p>' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '    <div class="col-md-3">' +
        '        <div class="card text-center">' +
        '            <div class="card-body">' +
        '                <h4 class="text-success">' + (statsData.positive_count || 0) + '</h4>' +
        '                <p class="mb-0">积极情绪</p>' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '    <div class="col-md-3">' +
        '        <div class="card text-center">' +
        '            <div class="card-body">' +
        '                <h4 class="text-warning">' + (statsData.neutral_count || 0) + '</h4>' +
        '                <p class="mb-0">中性情绪</p>' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '    <div class="col-md-3">' +
        '        <div class="card text-center">' +
        '            <div class="card-body">' +
        '                <h4 class="text-danger">' + (statsData.negative_count || 0) + '</h4>' +
        '                <p class="mb-0">消极情绪</p>' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '</div>' +
        
        // 分类数据展示
        '<div class="row">' + generateCategoryCards(categoryGroups, isIE) + '</div>' +
        
        // 详细统计
        '<div class="row mt-4">' +
        '    <div class="col-md-12">' +
        '        <div class="card">' +
        '            <div class="card-header bg-info text-white">' +
        '                <i class="bi bi-bar-chart"></i> 详细统计信息' +
        '            </div>' +
        '            <div class="card-body">' +
        '                <div class="row text-center">' +
        '                    <div class="col-md-2">' +
        '                        <div class="border rounded p-3">' +
        '                            <h5 class="text-primary">' + (statsData.finance_hotspots || 0) + '</h5>' +
        '                            <p class="mb-0 small">财经热点</p>' +
        '                        </div>' +
        '                    </div>' +
        '                    <div class="col-md-2">' +
        '                        <div class="border rounded p-3">' +
        '                            <h5 class="text-success">' + (statsData.policy_hotspots || 0) + '</h5>' +
        '                            <p class="mb-0 small">政策动态</p>' +
        '                        </div>' +
        '                    </div>' +
        '                    <div class="col-md-2">' +
        '                        <div class="border rounded p-3">' +
        '                            <h5 class="text-info">' + (statsData.market_hotspots || 0) + '</h5>' +
        '                            <p class="mb-0 small">市场新闻</p>' +
        '                        </div>' +
        '                    </div>' +
        '                    <div class="col-md-2">' +
        '                        <div class="border rounded p-3">' +
        '                            <h5 class="text-warning">' + (statsData.industry_hotspots || 0) + '</h5>' +
        '                            <p class="mb-0 small">行业资讯</p>' +
        '                        </div>' +
        '                    </div>' +
        '                    <div class="col-md-2">' +
        '                        <div class="border rounded p-3">' +
        '                            <h5 class="text-secondary">' + (statsData.company_hotspots || 0) + '</h5>' +
        '                            <p class="mb-0 small">公司热点</p>' +
        '                        </div>' +
        '                    </div>' +
        '                    <div class="col-md-2">' +
        '                        <div class="border rounded p-3">' +
        '                            <h5 class="text-dark">' + (statsData.macro_hotspots || 0) + '</h5>' +
        '                            <p class="mb-0 small">宏观经济</p>' +
        '                        </div>' +
        '                    </div>' +
        '                </div>' +
        '                <div class="row text-center mt-3">' +
        '                    <div class="col-md-6">' +
        '                        <div class="border rounded p-3">' +
        '                            <h5 class="text-primary">' + (statsData.investment_hotspots || 0) + '</h5>' +
        '                            <p class="mb-0 small">投资热点</p>' +
        '                        </div>' +
        '                    </div>' +
        '                    <div class="col-md-6">' +
        '                        <div class="border rounded p-3">' +
        '                            <h5 class="text-success">' + (statsData.market_sentiment || "积极") + '</h5>' +
        '                            <p class="mb-0 small">整体市场情绪</p>' +
        '                        </div>' +
        '                    </div>' +
        '                </div>' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '</div>' +
        
        '<div class="alert alert-info mt-3">' +
        '    <i class="bi bi-info-circle"></i>' +
        '    增强版国内热点数据 | 数据来源：' + dataSource + ' | 更新时间：' + (statsData.last_update || new Date().toLocaleString()) +
        '</div>';
    
    // 设置容器HTML
    container.innerHTML = htmlContent;
    
    // 将所有内容一次性添加到DocumentFragment
    while (container.firstChild) {
        fragment.appendChild(container.firstChild);
    }
    
    // 清空contentArea并一次性添加所有内容，减少重绘次数
    contentArea.innerHTML = '';
    contentArea.appendChild(fragment);
}

// 生成分类卡片HTML
function generateCategoryCards(categoryGroups, isIE) {
    var categoryCards = [];
    var categories = Object.keys(categoryGroups);
    
    // 使用传统for循环替代map，提升IE性能
    for (var i = 0; i < categories.length; i++) {
        var category = categories[i];
        var items = categoryGroups[category];
        
        // 生成项目HTML
        var itemsHtml = generateItemsHtml(items, isIE);
        
        // 添加分类卡片
        categoryCards.push(
            '<div class="col-md-6 mb-4">' +
            '    <div class="card">' +
            '        <div class="card-header bg-' + getCategoryColor(category) + ' text-white d-flex justify-content-between">' +
            '            <span><i class="bi bi-' + getCategoryIcon(category) + '"></i> ' + category + '</span>' +
            '            <span class="badge bg-light text-dark">' + items.length + '</span>' +
            '        </div>' +
            '        <div class="card-body" style="max-height: 420px; overflow-y: auto;">' +
            '            <div class="list-group list-group-flush">' +
            itemsHtml +
            '            </div>' +
            (items.length > 5 ? '<div class="text-center mt-2"><small class="text-muted">显示前5个，共' + items.length + '个</small></div>' : '') +
            '        </div>' +
            '    </div>' +
            '</div>'
        );
    }
    
    return categoryCards.join('');
}

// 生成项目HTML
function generateItemsHtml(items, isIE) {
    var itemsHtml = [];
    var displayItems = items.slice(0, 5); // 只显示前5个项目
    
    // 使用传统for循环替代map，提升IE性能
    for (var i = 0; i < displayItems.length; i++) {
        var item = displayItems[i];
        var titleHtml = item.url ? 
            '<a href="' + item.url + '" target="_blank" rel="noopener">' + item.title + '</a>' : 
            item.title;
        
        itemsHtml.push(
            '<div class="list-group-item">' +
            '    <div class="d-flex justify-content-between align-items-start">' +
            '        <div class="flex-grow-1">' +
            '            <h6 class="mb-1">' + titleHtml + '</h6>' +
            '            <p class="mb-1 small">' + item.content + '</p>' +
            '            <small class="text-muted">来源: ' + item.source + ' | ' + item.publishTime + '</small>' +
            '        </div>' +
            '        <div class="text-end">' +
            '            <span class="badge bg-' + getSentimentColor(item.sentiment) + '">' + item.sentiment + '</span>' +
            '            <br>' +
            '            <small class="text-muted">热度: ' + Math.round(item.heatScore) + '</small>' +
            '        </div>' +
            '    </div>' +
            '</div>'
        );
    }
    
    return itemsHtml.join('');
}

// 处理错误情况
function handleErrorCase(contentArea, error, isIE) {
    console.error("加载增强版国内热点数据失败:", error);
    
    // 使用模拟数据作为备用方案
    var hotspotData = generateMockHotspotData();
    var statsData = generateMockStatsData();
    
    // 按类别分组数据
    var categoryGroups = groupDataByCategory(hotspotData);
    
    // 创建DocumentFragment，减少DOM重绘次数
    var fragment = document.createDocumentFragment();
    var container = document.createElement('div');
    
    // 构建HTML内容
    var errorMessage = error ? (error.message || "未知错误") : "网络连接错误";
    var htmlContent = 
        '<div class="content-header">' +
        '    <h2><i class="bi bi-fire"></i> 增强版国内热点数据</h2>' +
        '    <p class="text-muted">第一层模块 - 基础数据采集</p>' +
        '    <div class="d-flex justify-content-between align-items-center">' +
        '        <span class="badge bg-info">共 ' + hotspotData.length + ' 条热点资讯</span>' +
        '        <div>' +
        '            <span class="badge bg-warning me-2">使用模拟数据</span>' +
        '            <button class="btn btn-sm btn-outline-primary" onclick="loadEnhancedDomesticHotspotData()">' +
        '                <i class="bi bi-arrow-clockwise"></i> 重试连接API' +
        '            </button>' +
        '        </div>' +
        '    </div>' +
        '</div>' +
        
        '<div class="alert alert-warning">' +
        '    <i class="bi bi-exclamation-triangle"></i>' +
        '    <strong>API连接失败:</strong> ' + errorMessage +
        '    <br><small>当前显示模拟数据。</small>' +
        '</div>' +
        
        // 统计数据卡片
        '<div class="row mb-4">' +
        '    <div class="col-md-3">' +
        '        <div class="card text-center">' +
        '            <div class="card-body">' +
        '                <h4 class="text-primary">' + (statsData.total_hotspots || hotspotData.length) + '</h4>' +
        '                <p class="mb-0">总数据量</p>' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '    <div class="col-md-3">' +
        '        <div class="card text-center">' +
        '            <div class="card-body">' +
        '                <h4 class="text-success">' + (statsData.positive_count || 0) + '</h4>' +
        '                <p class="mb-0">积极情绪</p>' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '    <div class="col-md-3">' +
        '        <div class="card text-center">' +
        '            <div class="card-body">' +
        '                <h4 class="text-warning">' + (statsData.neutral_count || 0) + '</h4>' +
        '                <p class="mb-0">中性情绪</p>' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '    <div class="col-md-3">' +
        '        <div class="card text-center">' +
        '            <div class="card-body">' +
        '                <h4 class="text-danger">' + (statsData.negative_count || 0) + '</h4>' +
        '                <p class="mb-0">消极情绪</p>' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '</div>' +
        
        // 分类数据展示
        '<div class="row">' + generateCategoryCards(categoryGroups, isIE) + '</div>' +
        
        '<div class="alert alert-info mt-3">' +
        '    <i class="bi bi-info-circle"></i>' +
        '    增强版国内热点数据 | 数据来源：模拟数据 | 更新时间：' + new Date().toLocaleString() +
        '</div>';
    
    // 设置容器HTML
    container.innerHTML = htmlContent;
    
    // 将所有内容一次性添加到DocumentFragment
    while (container.firstChild) {
        fragment.appendChild(container.firstChild);
    }
    
    // 清空contentArea并一次性添加所有内容，减少重绘次数
    contentArea.innerHTML = '';
    contentArea.appendChild(fragment);
}

// 辅助函数
// 优化市场情绪计算函数，使用单次遍历替代多次filter
function calculateMarketSentiment(hotspotData) {
    var positiveCount = 0;
    var negativeCount = 0;
    
    // 使用单次遍历计算情绪统计，提高性能
    for (var i = 0; i < hotspotData.length; i++) {
        var item = hotspotData[i];
        if (item.sentiment === "积极") {
            positiveCount++;
        } else if (item.sentiment === "消极") {
            negativeCount++;
        }
    }
    
    if (positiveCount > negativeCount + 2) return "积极";
    if (negativeCount > positiveCount + 2) return "消极";
    return "中性";
}

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
        case "货币政策": return "primary";
        case "产业政策": return "success";
        case "科技动态": return "info";
        case "环保政策": return "success";
        default: return "light";
    }
}

// 优化图标映射函数，确保IE浏览器兼容性
function getCategoryIcon(category) {
    // 对于IE浏览器，简化图标名称以确保更好的兼容性
    var isIE = /Trident|MSIE/.test(navigator.userAgent);
    
    // 基础图标映射
    var iconMap = {
        "财经热点": "currency-dollar",
        "政策动态": "file-earmark-text",
        "市场新闻": "newspaper",
        "行业资讯": "building",
        "公司热点": "briefcase",
        "宏观经济": "graph-up",
        "投资热点": "trending-up",
        "货币政策": "coin",
        "产业政策": "file-lines",
        "科技动态": "cpu",
        "环保政策": "leaf",
        "default": "circle"
    };
    
    // 对于IE浏览器，使用更简单的图标名称
    if (isIE) {
        var simpleIconMap = {
            "财经热点": "dollar",
            "政策动态": "file",
            "市场新闻": "newspaper",
            "行业资讯": "building",
            "公司热点": "briefcase",
            "宏观经济": "chart",
            "投资热点": "trending",
            "货币政策": "coin",
            "产业政策": "file-text",
            "科技动态": "cpu",
            "环保政策": "leaf",
            "default": "circle"
        };
        
        return simpleIconMap[category] || simpleIconMap.default;
    }
    
    return iconMap[category] || iconMap.default;
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
