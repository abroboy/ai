/**
 * 国内热点数据渲染模块
 */

// 渲染国内热点数据模块
function renderDomesticHotspotModule(container, data) {
    const statistics = data.statistics || {};
    const hotspots = data.data || [];
    
    const moduleHTML = `
        <div class="domestic-hotspot-module">
            <!-- 页面标题 -->
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h2 class="fw-bold text-primary mb-1">
                        <i class="bi bi-fire"></i> 国内热点数据
                        <span class="badge bg-danger ms-2">实时</span>
                    </h2>
                    <p class="text-muted mb-0">最后更新: ${formatDateTime(data.last_update)}</p>
                </div>
                <div class="btn-group">
                    <button class="btn btn-primary" onclick="refreshDomesticHotspots()">
                        <i class="bi bi-arrow-clockwise"></i> 刷新数据
                    </button>
                    <button class="btn btn-outline-secondary" onclick="exportHotspotData()">
                        <i class="bi bi-download"></i> 导出
                    </button>
                </div>
            </div>
            
            <!-- 统计卡片 -->
            <div class="row mb-4">
                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h4 class="fw-bold">${statistics.total_count || 0}</h4>
                                    <p class="mb-0">热点总数</p>
                                </div>
                                <div class="align-self-center">
                                    <i class="bi bi-newspaper fs-1"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h4 class="fw-bold">${statistics.sentiment_distribution?.积极 || 0}</h4>
                                    <p class="mb-0">积极情感</p>
                                </div>
                                <div class="align-self-center">
                                    <i class="bi bi-emoji-smile fs-1"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h4 class="fw-bold">${statistics.heat_distribution?.high || 0}</h4>
                                    <p class="mb-0">高热度</p>
                                </div>
                                <div class="align-self-center">
                                    <i class="bi bi-thermometer-high fs-1"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h4 class="fw-bold">${Object.keys(statistics.source_distribution || {}).length}</h4>
                                    <p class="mb-0">数据源</p>
                                </div>
                                <div class="align-self-center">
                                    <i class="bi bi-globe fs-1"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 主要内容区域 -->
            <div class="row">
                <!-- 热点列表 -->
                <div class="col-lg-8">
                    <div class="card shadow-sm">
                        <div class="card-header bg-light">
                            <div class="d-flex justify-content-between align-items-center">
                                <h5 class="card-title mb-0">热点列表</h5>
                                <div class="d-flex gap-2">
                                    <select class="form-select form-select-sm" onchange="filterByCategory(this.value)">
                                        <option value="all">全部分类</option>
                                        ${Object.keys(statistics.category_distribution || {}).map(cat => 
                                            `<option value="${cat}">${cat}</option>`
                                        ).join('')}
                                    </select>
                                    <select class="form-select form-select-sm" onchange="filterBySentiment(this.value)">
                                        <option value="all">全部情感</option>
                                        <option value="积极">积极</option>
                                        <option value="中性">中性</option>
                                        <option value="消极">消极</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="card-body p-0">
                            <div id="hotspot-list">
                                ${renderHotspotList(hotspots)}
                            </div>
                        </div>
                        <div class="card-footer">
                            <div id="pagination-container">
                                ${renderPagination(hotspots.length)}
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 侧边栏统计 -->
                <div class="col-lg-4">
                    <!-- 分类分布图表 -->
                    <div class="card shadow-sm mb-4">
                        <div class="card-header bg-light">
                            <h5 class="card-title mb-0">分类分布</h5>
                        </div>
                        <div class="card-body">
                            <div id="category-chart" style="height: 250px;"></div>
                        </div>
                    </div>
                    
                    <!-- 热门关键词 -->
                    <div class="card shadow-sm mb-4">
                        <div class="card-header bg-light">
                            <h5 class="card-title mb-0">热门关键词</h5>
                        </div>
                        <div class="card-body">
                            <div id="keywords-cloud">
                                ${renderKeywordsCloud(statistics.top_keywords || [])}
                            </div>
                        </div>
                    </div>
                    
                    <!-- 数据源分布 -->
                    <div class="card shadow-sm">
                        <div class="card-header bg-light">
                            <h5 class="card-title mb-0">数据源分布</h5>
                        </div>
                        <div class="card-body">
                            <div id="source-distribution">
                                ${renderSourceDistribution(statistics.source_distribution || {})}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 热点详情模态框 -->
        <div class="modal fade" id="hotspotDetailModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="hotspotDetailTitle">热点详情</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body" id="hotspotDetailContent">
                        <!-- 详情内容将通过JS动态填充 -->
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                        <button type="button" class="btn btn-primary">生成分析报告</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = moduleHTML;
    
    // 初始化图表
    setTimeout(() => {
        initCategoryChart(statistics.category_distribution || {});
    }, 100);
}

// 渲染热点列表
function renderHotspotList(hotspots) {
    if (!hotspots.length) {
        return `
            <div class="text-center py-5">
                <i class="bi bi-inbox fs-1 text-muted"></i>
                <p class="text-muted mt-3">暂无热点数据</p>
            </div>
        `;
    }
    
    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    const pageData = hotspots.slice(startIndex, endIndex);
    
    return pageData.map(hotspot => `
        <div class="border-bottom p-3 hotspot-item" data-id="${hotspot.id}">
            <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                    <h6 class="mb-2">
                        <a href="#" class="text-decoration-none" onclick="showHotspotDetail('${hotspot.id}')">
                            ${hotspot.title}
                        </a>
                    </h6>
                    <p class="text-muted small mb-2">${hotspot.content}</p>
                    <div class="d-flex flex-wrap gap-2 align-items-center">
                        <span class="badge bg-${getCategoryColor(hotspot.category)}">${hotspot.category}</span>
                        <span class="badge bg-${getSentimentColor(hotspot.sentiment)}">${hotspot.sentiment}</span>
                        <small class="text-muted">${hotspot.source}</small>
                        <small class="text-muted">${formatDateTime(hotspot.publish_time)}</small>
                    </div>
                    <div class="mt-2">
                        ${hotspot.keywords.map(keyword => 
                            `<span class="badge bg-light text-dark me-1">#${keyword}</span>`
                        ).join('')}
                    </div>
                </div>
                <div class="ms-3 text-center">
                    <div class="heat-score">
                        <div class="progress" style="width: 60px; height: 8px;">
                            <div class="progress-bar bg-${getHeatColor(hotspot.heat_score)}" 
                                 style="width: ${hotspot.heat_score}%"></div>
                        </div>
                        <small class="text-muted">${hotspot.heat_score}</small>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// 渲染分页
function renderPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / pageSize);
    
    if (totalPages <= 1) return '';
    
    let paginationHTML = '<nav><ul class="pagination pagination-sm justify-content-center">';
    
    // 上一页
    paginationHTML += `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPage - 1})">上一页</a>
        </li>
    `;
    
    // 页码
    for (let i = 1; i <= totalPages; i++) {
        if (i === currentPage) {
            paginationHTML += `<li class="page-item active"><span class="page-link">${i}</span></li>`;
        } else {
            paginationHTML += `<li class="page-item"><a class="page-link" href="#" onclick="changePage(${i})">${i}</a></li>`;
        }
    }
    
    // 下一页
    paginationHTML += `
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPage + 1})">下一页</a>
        </li>
    `;
    
    paginationHTML += '</ul></nav>';
    return paginationHTML;
}

// 渲染关键词云
function renderKeywordsCloud(keywords) {
    if (!keywords.length) {
        return '<p class="text-muted">暂无关键词数据</p>';
    }
    
    return keywords.map(item => {
        const size = Math.max(12, Math.min(24, 12 + item.count * 2));
        return `<span class="badge bg-primary me-2 mb-2" style="font-size: ${size}px;">${item.keyword} (${item.count})</span>`;
    }).join('');
}

// 渲染数据源分布
function renderSourceDistribution(sources) {
    if (!Object.keys(sources).length) {
        return '<p class="text-muted">暂无数据源信息</p>';
    }
    
    const total = Object.values(sources).reduce((sum, count) => sum + count, 0);
    
    return Object.entries(sources).map(([source, count]) => {
        const percentage = ((count / total) * 100).toFixed(1);
        return `
            <div class="mb-2">
                <div class="d-flex justify-content-between">
                    <span>${source}</span>
                    <span>${count} (${percentage}%)</span>
                </div>
                <div class="progress" style="height: 6px;">
                    <div class="progress-bar" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }).join('');
}

// 获取分类颜色
function getCategoryColor(category) {
    const colorMap = {
        '金融政策': 'primary',
        '行业动态': 'success',
        '资本市场': 'danger',
        '政策动态': 'warning',
        '科技创新': 'info',
        '大宗商品': 'secondary'
    };
    return colorMap[category] || 'secondary';
}

// 获取情感颜色
function getSentimentColor(sentiment) {
    const colorMap = {
        '积极': 'success',
        '中性': 'warning',
        '消极': 'danger'
    };
    return colorMap[sentiment] || 'secondary';
}

// 获取热度颜色
function getHeatColor(score) {
    if (score >= 80) return 'danger';
    if (score >= 60) return 'warning';
    return 'success';
}