/**
 * 国内热点数据交互模块
 */

// 切换页面
function changePage(page) {
    if (page < 1) return;
    
    const totalPages = Math.ceil(currentHotspotData.length / pageSize);
    if (page > totalPages) return;
    
    currentPage = page;
    
    // 重新渲染列表
    const listContainer = document.getElementById('hotspot-list');
    if (listContainer) {
        listContainer.innerHTML = renderHotspotList(getFilteredData());
    }
    
    // 重新渲染分页
    const paginationContainer = document.getElementById('pagination-container');
    if (paginationContainer) {
        paginationContainer.innerHTML = renderPagination(getFilteredData().length);
    }
}

// 按分类筛选
function filterByCategory(category) {
    currentFilter = category;
    currentPage = 1;
    
    const filteredData = getFilteredData();
    
    // 重新渲染列表和分页
    const listContainer = document.getElementById('hotspot-list');
    if (listContainer) {
        listContainer.innerHTML = renderHotspotList(filteredData);
    }
    
    const paginationContainer = document.getElementById('pagination-container');
    if (paginationContainer) {
        paginationContainer.innerHTML = renderPagination(filteredData.length);
    }
}

// 按情感筛选
function filterBySentiment(sentiment) {
    currentFilter = sentiment;
    currentPage = 1;
    
    const filteredData = getFilteredData();
    
    // 重新渲染列表和分页
    const listContainer = document.getElementById('hotspot-list');
    if (listContainer) {
        listContainer.innerHTML = renderHotspotList(filteredData);
    }
    
    const paginationContainer = document.getElementById('pagination-container');
    if (paginationContainer) {
        paginationContainer.innerHTML = renderPagination(filteredData.length);
    }
}

// 获取筛选后的数据
function getFilteredData() {
    if (currentFilter === 'all') {
        return currentHotspotData;
    }
    
    return currentHotspotData.filter(item => 
        item.category === currentFilter || item.sentiment === currentFilter
    );
}

// 显示热点详情
function showHotspotDetail(id) {
    const hotspot = currentHotspotData.find(item => item.id === id);
    if (!hotspot) {
        alert('找不到热点详情');
        return;
    }
    
    // 更新模态框标题
    const titleElement = document.getElementById('hotspotDetailTitle');
    if (titleElement) {
        titleElement.textContent = hotspot.title;
    }
    
    // 更新模态框内容
    const contentElement = document.getElementById('hotspotDetailContent');
    if (contentElement) {
        contentElement.innerHTML = `
            <div class="mb-4">
                <div class="d-flex justify-content-between mb-3">
                    <div>
                        <span class="badge bg-${getCategoryColor(hotspot.category)} me-2">${hotspot.category}</span>
                        <span class="badge bg-${getSentimentColor(hotspot.sentiment)}">${hotspot.sentiment}</span>
                    </div>
                    <div class="text-muted small">
                        来源: ${hotspot.source} | 发布时间: ${formatDateTime(hotspot.publish_time)}
                    </div>
                </div>
                
                <div class="alert alert-light">
                    <h6 class="fw-bold">内容摘要</h6>
                    <p>${hotspot.content}</p>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header bg-light">
                                <h6 class="card-title mb-0">热度评分</h6>
                            </div>
                            <div class="card-body text-center">
                                <h2 class="text-${getHeatColor(hotspot.heat_score)}">${hotspot.heat_score}</h2>
                                <div class="progress">
                                    <div class="progress-bar bg-${getHeatColor(hotspot.heat_score)}" 
                                         style="width: ${hotspot.heat_score}%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header bg-light">
                                <h6 class="card-title mb-0">关键词</h6>
                            </div>
                            <div class="card-body">
                                ${hotspot.keywords.map(keyword => 
                                    `<span class="badge bg-primary me-1 mb-1">#${keyword}</span>`
                                ).join('')}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header bg-light">
                        <h6 class="card-title mb-0">相关链接</h6>
                    </div>
                    <div class="card-body">
                        <a href="${hotspot.url}" target="_blank" class="btn btn-outline-primary btn-sm">
                            <i class="bi bi-link-45deg"></i> 查看原文
                        </a>
                    </div>
                </div>
            </div>
        `;
    }
    
    // 显示模态框
    const modal = new bootstrap.Modal(document.getElementById('hotspotDetailModal'));
    modal.show();
}

// 搜索热点
function searchHotspots(keyword) {
    if (!keyword.trim()) {
        // 如果搜索关键词为空，显示所有数据
        currentFilter = 'all';
        currentPage = 1;
        
        const listContainer = document.getElementById('hotspot-list');
        if (listContainer) {
            listContainer.innerHTML = renderHotspotList(currentHotspotData);
        }
        
        const paginationContainer = document.getElementById('pagination-container');
        if (paginationContainer) {
            paginationContainer.innerHTML = renderPagination(currentHotspotData.length);
        }
        return;
    }
    
    // 搜索标题、内容和关键词
    const filteredData = currentHotspotData.filter(item => 
        item.title.toLowerCase().includes(keyword.toLowerCase()) ||
        item.content.toLowerCase().includes(keyword.toLowerCase()) ||
        item.keywords.some(k => k.toLowerCase().includes(keyword.toLowerCase()))
    );
    
    currentPage = 1;
    
    // 重新渲染列表
    const listContainer = document.getElementById('hotspot-list');
    if (listContainer) {
        if (filteredData.length > 0) {
            listContainer.innerHTML = renderHotspotList(filteredData);
        } else {
            listContainer.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-search fs-1 text-muted"></i>
                    <p class="text-muted mt-3">未找到包含 "${keyword}" 的热点</p>
                </div>
            `;
        }
    }
    
    // 重新渲染分页
    const paginationContainer = document.getElementById('pagination-container');
    if (paginationContainer) {
        paginationContainer.innerHTML = renderPagination(filteredData.length);
    }
}

// 全局注册函数
window.changePage = changePage;
window.filterByCategory = filterByCategory;
window.filterBySentiment = filterBySentiment;
window.showHotspotDetail = showHotspotDetail;
window.searchHotspots = searchHotspots;