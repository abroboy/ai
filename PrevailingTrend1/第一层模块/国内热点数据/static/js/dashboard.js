/**
 * 国内热点数据管理台 JavaScript
 */

// 全局变量
let currentPage = 1;
let currentView = 'dashboard';
let currentSortBy = 'publish_time';
let currentSortOrder = 'desc';

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
    // 初始化排序指示器
    updateSortIndicators();
});

// 显示仪表盘
function showDashboard() {
    hideAllContent();
    document.getElementById('dashboard-content').style.display = 'block';
    currentView = 'dashboard';
    loadDashboard();
}

// 显示热点列表
function showHotspots() {
    hideAllContent();
    const hotspotsElement = document.getElementById('hotspots-content');
    if (hotspotsElement) {
        hotspotsElement.style.display = 'block';
        currentView = 'hotspots';
        loadHotspots();
    } else {
        console.error('找不到热点列表内容元素');
    }
}

// 显示热点列表 (别名函数，用于兼容)
function showHotspotList() {
    showHotspots();
}

// 显示统计分析
function showStatistics() {
    hideAllContent();
    document.getElementById('statistics-content').style.display = 'block';
    currentView = 'statistics';
    loadStatistics();
}

// 显示数据采集
function showCollection() {
    hideAllContent();
    const collectionElement = document.getElementById('collection-content');
    if (collectionElement) {
        collectionElement.style.display = 'block';
        currentView = 'collection';
        loadCollection();
    } else {
        console.error('找不到数据采集内容元素');
    }
}

// 显示数据采集 (别名函数，用于兼容)
function showDataCollection() {
    showCollection();
}

// 显示系统设置
function showSettings() {
    hideAllContent();
    const settingsElement = document.getElementById('settings-content');
    if (settingsElement) {
        settingsElement.style.display = 'block';
        currentView = 'settings';
        loadSettings();
    } else {
        console.error('找不到系统设置内容元素');
    }
}

// 显示热度排名
function showRankings() {
    hideAllContent();
    const rankingsElement = document.getElementById('rankings-content');
    if (rankingsElement) {
        rankingsElement.style.display = 'block';
        currentView = 'rankings';
        loadRankings();
    } else {
        console.error('找不到热度排名内容元素');
    }
}

// 显示分析
function showAnalysis() {
    hideAllContent();
    const analysisElement = document.getElementById('statistics-content');
    if (analysisElement) {
        analysisElement.style.display = 'block';
        currentView = 'analysis';
        loadAnalysis();
    } else {
        console.error('找不到统计分析内容元素');
    }
}

// 隐藏所有内容
function hideAllContent() {
    const contents = [
        'dashboard-content',
        'hotspots-content', 
        'statistics-content',
        'collection-content',
        'settings-content',
        'rankings-content',
        'analysis-content'
    ];
    
    contents.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.style.display = 'none';
        }
    });
    
    // 清除所有导航激活状态
    document.querySelectorAll('.nav-item').forEach(link => {
        link.classList.remove('active');
    });
    
    // 设置当前导航为激活状态
    if (event && event.target) {
        event.target.classList.add('active');
    }
}

// 加载仪表盘数据
function loadDashboard() {
    // 加载统计数据
    fetch('/api/statistics')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateDashboardStats(data.data);
                createSimpleCharts(data.data);
            }
        })
        .catch(error => {
            console.error('加载统计数据失败:', error);
            showError('加载统计数据失败');
        });
    
    // 加载最新热点
    loadLatestHotspots();
}

// 更新仪表盘统计
function updateDashboardStats(stats) {
    // 安全地更新统计数据，避免undefined错误
    const totalHotspotsEl = document.getElementById('total-hotspots');
    const avgHeatEl = document.getElementById('avg-heat');
    const avgSentimentEl = document.getElementById('avg-sentiment');
    const activeHotspotsEl = document.getElementById('active-hotspots');
    
    if (totalHotspotsEl) {
        totalHotspotsEl.textContent = stats.total_count || 0;
    }
    if (avgHeatEl) {
        avgHeatEl.textContent = stats.avg_heat || 0;
    }
    if (avgSentimentEl) {
        avgSentimentEl.textContent = stats.avg_sentiment || 0;
    }
    if (activeHotspotsEl) {
        // 安全地访问by_status.active
        const byStatus = stats.by_status || {};
        activeHotspotsEl.textContent = byStatus.active || 0;
    }
}

// 创建简单图表
function createSimpleCharts(stats) {
    // 类型分布图
    createSimplePieChart('type-chart', stats.by_type || {}, '热点类型分布');
    
    // 级别分布图
    createSimpleBarChart('level-chart', stats.by_level || {}, '热度级别分布');
}

// 创建简单饼图
function createSimplePieChart(containerId, data, title) {
    console.log(`创建饼图: ${containerId}, 标题: ${title}, 数据:`, data);
    
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`找不到容器元素: ${containerId}`);
        return;
    }
    
    const colors = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#06b6d4'];
    let html = `<h4 style="text-align: center; margin-bottom: 1rem;">${title}</h4>`;
    
    let total = 0;
    for (let key in data) {
        total += data[key];
    }
    
    console.log(`总数据量: ${total}`);
    
    if (total === 0) {
        html += '<p style="text-align: center; color: #666;">暂无数据</p>';
    } else {
        let colorIndex = 0;
        for (let key in data) {
            const percentage = total > 0 ? ((data[key] / total) * 100).toFixed(1) : 0;
            const color = colors[colorIndex % colors.length];
            html += `
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <div style="width: 20px; height: 20px; background: ${color}; border-radius: 50%; margin-right: 0.5rem;"></div>
                    <span style="flex: 1;">${key}</span>
                    <span style="font-weight: bold;">${data[key]} (${percentage}%)</span>
                </div>
            `;
            colorIndex++;
        }
    }
    
    container.innerHTML = html;
    console.log(`饼图 ${containerId} 创建完成`);
}

// 更新统计摘要信息
function updateStatisticsSummary(data) {
    console.log('更新统计摘要信息:', data);
    
    // 查找或创建统计摘要容器
    let summaryContainer = document.getElementById('statistics-summary');
    if (!summaryContainer) {
        // 如果不存在，在统计分析页面顶部创建
        const statisticsContent = document.getElementById('statistics-content');
        if (statisticsContent) {
            const dashboardContent = statisticsContent.querySelector('.dashboard-content');
            if (dashboardContent) {
                const summaryHtml = `
                    <div id="statistics-summary" style="margin-bottom: 2rem; padding: 1.5rem; background: #f8f9fa; border-radius: 0.5rem;">
                        <h4 style="margin-bottom: 1rem; color: #2c3e50;">数据概览</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                            <div style="text-align: center; padding: 1rem; background: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                                <div style="font-size: 2rem; font-weight: bold; color: #4f46e5;">${data.total_count}</div>
                                <div style="color: #666;">总热点数</div>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                                <div style="font-size: 2rem; font-weight: bold; color: #10b981;">${data.avg_heat}</div>
                                <div style="color: #666;">平均热度</div>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                                <div style="font-size: 2rem; font-weight: bold; color: #f59e0b;">${data.avg_sentiment}</div>
                                <div style="color: #666;">平均情感分数</div>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                                <div style="font-size: 2rem; font-weight: bold; color: #ef4444;">${Object.keys(data.by_type).length}</div>
                                <div style="color: #666;">热点类型</div>
                            </div>
                        </div>
                    </div>
                `;
                dashboardContent.insertAdjacentHTML('afterbegin', summaryHtml);
                summaryContainer = document.getElementById('statistics-summary');
            }
        }
    }
    
    if (summaryContainer) {
        console.log('统计摘要容器已更新');
    }
}

// 创建简单柱状图
function createSimpleBarChart(containerId, data, title) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const colors = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444'];
    let html = `<h4 style="text-align: center; margin-bottom: 1rem;">${title}</h4>`;
    
    let maxValue = 0;
    for (let key in data) {
        if (data[key] > maxValue) maxValue = data[key];
    }
    
    let colorIndex = 0;
    for (let key in data) {
        const percentage = maxValue > 0 ? ((data[key] / maxValue) * 100) : 0;
        const color = colors[colorIndex % colors.length];
        html += `
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span>${getLevelLabel(key)}</span>
                    <span style="font-weight: bold;">${data[key]}</span>
                </div>
                <div style="background: #f1f5f9; height: 20px; border-radius: 10px; overflow: hidden;">
                    <div style="background: ${color}; height: 100%; width: ${percentage}%; transition: width 0.3s ease;"></div>
                </div>
            </div>
        `;
        colorIndex++;
    }
    
    container.innerHTML = html;
}

// 加载最新热点
function loadLatestHotspots() {
    fetch('/api/hotspots?page=1&per_page=5')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderLatestHotspots(data.data.hotspots);
            }
        })
        .catch(error => {
            console.error('加载最新热点失败:', error);
            showError('加载最新热点失败');
        });
}

// 渲染最新热点
function renderLatestHotspots(hotspots) {
    const tbody = document.getElementById('latest-hotspots');
    tbody.innerHTML = '';
    
    if (hotspots.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading">暂无数据</td></tr>';
        return;
    }
    
    hotspots.forEach(hotspot => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <a href="#" onclick="viewHotspotDetail('${hotspot.hotspot_id}')" style="color: #4f46e5; text-decoration: none;">
                    ${hotspot.title}
                </a>
            </td>
            <td><span class="badge badge-primary">${getTypeLabel(hotspot.hotspot_type)}</span></td>
            <td>${hotspot.source}</td>
            <td><span style="font-weight: bold; color: ${getHeatColor(hotspot.heat_score)};">${hotspot.heat_score}</span></td>
            <td><span class="badge ${getSentimentClass(hotspot.sentiment_score)}">${getSentimentLabel(hotspot.sentiment_score)}</span></td>
            <td><span class="badge badge-success">${getStatusLabel(hotspot.status)}</span></td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="viewHotspotDetail('${hotspot.hotspot_id}')">
                    👁️
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// 全局排序变量（已在顶部声明）

// 加载热点列表
function loadHotspots(page = 1) {
    currentPage = page;
    
    const params = new URLSearchParams({
        page: page,
        per_page: 20,
        sort_by: currentSortBy,
        sort_order: currentSortOrder
    });
    
    // 添加筛选参数
    const type = document.getElementById('filter-type')?.value;
    const level = document.getElementById('filter-level')?.value;
    const source = document.getElementById('filter-source')?.value;
    const minHeat = document.getElementById('filter-min-heat')?.value;
    
    if (type) params.append('hotspot_type', type);
    if (level) params.append('hotspot_level', level);
    if (source) params.append('source', source);
    if (minHeat) params.append('min_heat_score', minHeat);
    
    const url = `/api/hotspots?${params}`;
    console.log('请求URL:', url);
    
    fetch(url)
        .then(response => {
            console.log('响应状态:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('响应数据:', data);
            if (data.success) {
                renderHotspotsTable(data.data.hotspots);
                renderPagination(data.data.pagination);
            } else {
                console.error('API返回错误:', data.error);
                showError('加载热点列表失败: ' + (data.error || '未知错误'));
            }
        })
        .catch(error => {
            console.error('加载热点列表失败:', error);
            showError('加载热点列表失败: ' + error.message);
        });
}

// 渲染热点表格
function renderHotspotsTable(hotspots) {
    const tbody = document.getElementById('hotspots-table');
    tbody.innerHTML = '';
    
    if (hotspots.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="loading">暂无数据</td></tr>';
        return;
    }
    
    hotspots.forEach(hotspot => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <a href="#" onclick="viewHotspotDetail('${hotspot.hotspot_id}')" style="color: #4f46e5; text-decoration: none;">
                    ${hotspot.title}
                </a>
            </td>
            <td><span class="badge badge-primary">${getTypeLabel(hotspot.hotspot_type)}</span></td>
            <td><span class="badge ${getLevelClass(hotspot.hotspot_level)}">${getLevelLabel(hotspot.hotspot_level)}</span></td>
            <td>${hotspot.source}</td>
            <td><span style="font-weight: bold; color: ${getHeatColor(hotspot.heat_score)};">${hotspot.heat_score}</span></td>
            <td><span class="badge ${getSentimentClass(hotspot.sentiment_score)}">${getSentimentLabel(hotspot.sentiment_score)}</span></td>
            <td><span class="badge ${getStatusClass(hotspot.status)}">${getStatusLabel(hotspot.status)}</span></td>
            <td>${formatDateTime(hotspot.publish_time)}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="viewHotspotDetail('${hotspot.hotspot_id}')">
                    👁️
                </button>
                <button class="btn btn-sm btn-secondary" onclick="deleteHotspot('${hotspot.hotspot_id}')">
                    🗑️
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// 排序函数
function sortHotspots(sortBy) {
    console.log('排序函数调用:', sortBy, '当前排序:', currentSortBy, currentSortOrder);
    
    if (currentSortBy === sortBy) {
        // 如果点击的是当前排序列，切换排序方向
        currentSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';
    } else {
        // 如果是新的排序列，默认降序
        currentSortBy = sortBy;
        currentSortOrder = 'desc';
    }
    
    console.log('排序后:', currentSortBy, currentSortOrder);
    
    // 更新表头排序指示器
    updateSortIndicators();
    
    // 重新加载数据
    loadHotspots(1);
}

// 更新数据
function updateData() {
    const button = event.target;
    const originalText = button.textContent;
    
    // 显示加载状态
    button.textContent = '更新中...';
    button.disabled = true;
    
    fetch('/api/collect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(data.data.message || '数据更新成功');
            // 刷新当前页面数据
            if (currentView === 'dashboard') {
                loadDashboard();
            } else if (currentView === 'hotspots') {
                loadHotspots(1);
            } else if (currentView === 'statistics') {
                loadStatistics();
            }
        } else {
            showError(data.error || '数据更新失败');
        }
    })
    .catch(error => {
        console.error('数据更新失败:', error);
        showError('数据更新失败');
    })
    .finally(() => {
        // 恢复按钮状态
        button.textContent = originalText;
        button.disabled = false;
    });
}

// 获取更新状态
function getUpdateStatus() {
    fetch('/api/update-status')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const status = data.data;
            let message = `更新状态:\n`;
            message += `运行状态: ${status.is_running ? '运行中' : '已停止'}\n`;
            message += `总数据量: ${status.total_data || 0} 条\n`;
            message += `今日数据: ${status.today_data || 0} 条\n`;
            message += `最后更新: ${status.last_update || '未知'}`;
            
            if (status.error) {
                message += `\n错误: ${status.error}`;
            }
            
            alert(message);
        } else {
            showError('获取更新状态失败');
        }
    })
    .catch(error => {
        console.error('获取更新状态失败:', error);
        showError('获取更新状态失败');
    });
}

// 更新排序指示器
function updateSortIndicators() {
    // 清除所有排序指示器
    document.querySelectorAll('.sort-indicator').forEach(indicator => {
        indicator.textContent = '';
    });
    
    // 设置当前排序列的指示器
    const currentIndicator = document.querySelector(`[data-sort="${currentSortBy}"] .sort-indicator`);
    if (currentIndicator) {
        currentIndicator.textContent = currentSortOrder === 'asc' ? ' ↑' : ' ↓';
    }
}

// 渲染分页
function renderPagination(pagination) {
    const paginationEl = document.getElementById('pagination');
    paginationEl.innerHTML = '';
    
    const { page, pages, total, per_page } = pagination;
    
    // 显示总数信息
    const totalInfo = document.createElement('div');
    totalInfo.className = 'pagination-info';
    totalInfo.style.cssText = 'margin-bottom: 1rem; color: #666; font-size: 0.9rem;';
    const start = (page - 1) * per_page + 1;
    const end = Math.min(page * per_page, total);
    totalInfo.textContent = `显示第 ${start}-${end} 条，共 ${total} 条数据`;
    paginationEl.appendChild(totalInfo);
    
    // 上一页
    if (page > 1) {
        const prevLink = document.createElement('a');
        prevLink.className = 'page-link';
        prevLink.href = '#';
        prevLink.textContent = '上一页';
        prevLink.onclick = () => loadHotspots(page - 1);
        paginationEl.appendChild(prevLink);
    }
    
    // 页码
    for (let i = Math.max(1, page - 2); i <= Math.min(pages, page + 2); i++) {
        const link = document.createElement('a');
        link.className = `page-link ${i === page ? 'active' : ''}`;
        link.href = '#';
        link.textContent = i;
        link.onclick = () => loadHotspots(i);
        paginationEl.appendChild(link);
    }
    
    // 下一页
    if (page < pages) {
        const nextLink = document.createElement('a');
        nextLink.className = 'page-link';
        nextLink.href = '#';
        nextLink.textContent = '下一页';
        nextLink.onclick = () => loadHotspots(page + 1);
        paginationEl.appendChild(nextLink);
    }
}

// 筛选热点
function filterHotspots() {
    loadHotspots(1);
}

// 查看热点详情
function viewHotspotDetail(hotspotId) {
    console.log('查看热点详情:', hotspotId);
    
    fetch(`/api/hotspots/${hotspotId}`)
        .then(response => {
            console.log('热点详情响应状态:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('热点详情数据:', data);
            if (data.success) {
                showHotspotModal(data.data);
            } else {
                console.error('API返回错误:', data.error);
                showError('加载热点详情失败: ' + (data.error || '未知错误'));
            }
        })
        .catch(error => {
            console.error('加载热点详情失败:', error);
            showError('加载热点详情失败: ' + error.message);
        });
}

// 显示热点模态框
function showHotspotModal(hotspot) {
    const modalBody = document.getElementById('hotspot-modal-body');
    
    // 构建详细内容HTML
    let detailedContent = '';
    if (hotspot.detailed_content) {
        detailedContent = `<div style="margin-top: 1rem; padding: 1rem; background-color: #f8f9fa; border-radius: 0.5rem;">
            <h5>详细内容</h5>
            <p>${hotspot.detailed_content}</p>
        </div>`;
    }
    
    // 构建分析内容HTML
    let analysisContent = '';
    if (hotspot.analysis) {
        analysisContent = `<div style="margin-top: 1rem; padding: 1rem; background-color: #e3f2fd; border-radius: 0.5rem;">
            <h5>分析</h5>
            <p>${hotspot.analysis}</p>
        </div>`;
    }
    
    // 构建影响内容HTML
    let impactContent = '';
    if (hotspot.impact) {
        impactContent = `<div style="margin-top: 1rem; padding: 1rem; background-color: #f3e5f5; border-radius: 0.5rem;">
            <h5>市场影响</h5>
            <p>${hotspot.impact}</p>
        </div>`;
    }
    
    // 构建相关新闻HTML
    let relatedNewsContent = '';
    if (hotspot.related_news && hotspot.related_news.length > 0) {
        relatedNewsContent = `<div style="margin-top: 1rem; padding: 1rem; background-color: #fff3e0; border-radius: 0.5rem;">
            <h5>相关新闻</h5>
            <ul style="margin: 0; padding-left: 1.5rem;">
                ${hotspot.related_news.map(news => `<li>${news}</li>`).join('')}
            </ul>
        </div>`;
    }
    
    modalBody.innerHTML = `
        <div style="margin-bottom: 1rem;">
            <h4 style="color: #2c3e50; margin-bottom: 0.5rem;">${hotspot.title}</h4>
            <p style="color: #666; margin-top: 0.5rem; line-height: 1.6;">${hotspot.content}</p>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
            <div>
                <p><strong>类型:</strong> <span class="badge badge-primary">${getTypeLabel(hotspot.hotspot_type)}</span></p>
                <p><strong>级别:</strong> <span class="badge ${getLevelClass(hotspot.hotspot_level)}">${getLevelLabel(hotspot.hotspot_level)}</span></p>
                <p><strong>来源:</strong> ${hotspot.source}</p>
                <p><strong>状态:</strong> <span class="badge ${getStatusClass(hotspot.status)}">${getStatusLabel(hotspot.status)}</span></p>
            </div>
            <div>
                <p><strong>热度:</strong> <span style="font-weight: bold; color: ${getHeatColor(hotspot.heat_score)};">${hotspot.heat_score}</span></p>
                <p><strong>情感:</strong> <span class="badge ${getSentimentClass(hotspot.sentiment_score)}">${getSentimentLabel(hotspot.sentiment_score)}</span></p>
                <p><strong>发布时间:</strong> ${formatDateTime(hotspot.publish_time)}</p>
                <p><strong>更新时间:</strong> ${formatDateTime(hotspot.update_date)}</p>
            </div>
        </div>
        
        <div style="margin-top: 1rem; padding: 1rem; background-color: #f5f5f5; border-radius: 0.5rem;">
            <p><strong>关键词:</strong> ${hotspot.keywords.join(', ')}</p>
            <p><strong>相关公司:</strong> ${hotspot.related_companies.length > 0 ? hotspot.related_companies.join(', ') : '无'}</p>
            <p><strong>相关行业:</strong> ${hotspot.related_industries.join(', ')}</p>
        </div>
        
        ${detailedContent}
        ${analysisContent}
        ${impactContent}
        ${relatedNewsContent}
        
        <div style="margin-top: 1rem; text-align: center;">
            <a href="${hotspot.url}" target="_blank" class="btn btn-primary">查看原文</a>
        </div>
    `;
    
    document.getElementById('hotspotModal').style.display = 'block';
}

// 关闭模态框
function closeModal() {
    document.getElementById('hotspotModal').style.display = 'none';
}

// 删除热点
function deleteHotspot(hotspotId) {
    if (confirm('确定要删除这个热点吗？')) {
        fetch(`/api/hotspots/${hotspotId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSuccess('删除成功');
                loadHotspots(currentPage);
            } else {
                showError('删除失败: ' + data.error);
            }
        })
        .catch(error => {
            console.error('删除热点失败:', error);
            showError('删除失败');
        });
    }
}

// 开始采集
function startCollection() {
    fetch('/api/collect', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess('采集成功: ' + data.data.message);
            addCollectionLog('采集完成: ' + data.data.message);
            document.getElementById('last-collection-time').textContent = new Date().toLocaleString();
            document.getElementById('collection-status').style.display = 'block';
        } else {
            showError('采集失败: ' + data.error);
            addCollectionLog('采集失败: ' + data.error);
        }
    })
    .catch(error => {
        console.error('采集失败:', error);
        showError('采集失败');
        addCollectionLog('采集失败: ' + error.message);
    });
}

// 停止采集
function stopCollection() {
    addCollectionLog('停止采集');
}

// 添加采集日志
function addCollectionLog(message) {
    const logContainer = document.getElementById('collection-log');
    const logEntry = document.createElement('div');
    logEntry.innerHTML = `<small style="color: #666;">${new Date().toLocaleString()}</small> - ${message}`;
    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
}

// 保存设置
function saveSettings() {
    showSuccess('设置保存成功');
}

// 编辑热点
function editHotspot() {
    showError('编辑功能暂未实现');
}

// 显示成功消息
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success';
    successDiv.textContent = message;
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// 显示错误消息
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 3000);
}

// 工具函数
function getTypeLabel(type) {
    const labels = {
        'news': '新闻',
        'policy': '政策',
        'industry': '行业',
        'company': '公司',
        'market': '市场',
        'economy': '经济'
    };
    return labels[type] || type;
}

function getLevelLabel(level) {
    const labels = {
        'low': '低热度',
        'medium': '中等热度',
        'high': '高热度',
        'very_high': '极高热度'
    };
    return labels[level] || level;
}

function getStatusLabel(status) {
    const labels = {
        'active': '活跃',
        'declining': '下降',
        'expired': '过期'
    };
    return labels[status] || status;
}

function getSentimentLabel(score) {
    if (score > 0.3) return '正面';
    if (score < -0.3) return '负面';
    return '中性';
}

function getLevelClass(level) {
    const classes = {
        'low': 'badge-secondary',
        'medium': 'badge-info',
        'high': 'badge-warning',
        'very_high': 'badge-danger'
    };
    return classes[level] || 'badge-secondary';
}

function getStatusClass(status) {
    const classes = {
        'active': 'badge-success',
        'declining': 'badge-warning',
        'expired': 'badge-secondary'
    };
    return classes[status] || 'badge-secondary';
}

function getSentimentClass(score) {
    if (score > 0.3) return 'badge-success';
    if (score < -0.3) return 'badge-danger';
    return 'badge-secondary';
}

function getHeatColor(score) {
    if (score >= 80) return '#dc3545';
    if (score >= 60) return '#ffc107';
    return '#28a745';
}

function formatDateTime(dateString) {
    if (!dateString) return '未知';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
}

// 加载其他页面数据
function loadStatistics() {
    console.log('开始加载统计分析数据...');
    
    // 加载统计分析数据
    fetch('/api/statistics')
        .then(response => {
            console.log('统计分析响应状态:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('统计分析数据:', data);
            if (data.success) {
                // 转换关键词数据格式
                const keywordsData = {};
                data.data.top_keywords.forEach(([key, value]) => {
                    keywordsData[key] = value;
                });
                console.log('关键词数据:', keywordsData);
                
                // 转换公司数据格式
                const companiesData = {};
                data.data.top_companies.forEach(([key, value]) => {
                    companiesData[key] = value;
                });
                console.log('公司数据:', companiesData);
                
                // 创建图表
                createSimplePieChart('keywords-chart', keywordsData, '关键词统计');
                createSimplePieChart('companies-chart', companiesData, '相关公司统计');
                
                // 添加统计摘要信息
                updateStatisticsSummary(data.data);
                
                console.log('统计分析图表创建完成');
            } else {
                console.error('统计分析API返回错误:', data.error);
                showError('加载统计数据失败: ' + (data.error || '未知错误'));
            }
        })
        .catch(error => {
            console.error('加载统计数据失败:', error);
            showError('加载统计数据失败: ' + error.message);
        });
}

function loadCollection() {
    // 加载采集页面数据
    document.getElementById('collection-status').style.display = 'none';
}

function loadSettings() {
    // 加载设置页面数据
} 

// 排名相关功能
function showRankings() {
    hideAllContent();
    document.getElementById('rankings-content').style.display = 'block';
    updateActiveNav('rankings');
    loadRankings();
}

function showRankingTab(tabName) {
    console.log('showRankingTab called with:', tabName);
    
    // 隐藏所有排名表格
    document.querySelectorAll('.ranking-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // 移除所有标签页的active状态
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 显示选中的标签页
    let elementId;
    if (tabName === 'industries') {
        elementId = 'industry-rankings';
    } else if (tabName === 'companies') {
        elementId = 'company-rankings';
    } else if (tabName === 'trends') {
        elementId = 'trend-rankings';
    } else {
        elementId = tabName + '-rankings';
    }
    
    console.log('Looking for element with ID:', elementId);
    const element = document.getElementById(elementId);
    console.log('Found element:', element);
    
    if (element) {
        element.style.display = 'block';
        console.log('Element display set to block');
        // 加载对应的排名数据
        loadRankingData(tabName);
    } else {
        console.error('找不到排名元素:', elementId);
        // 尝试查找所有可能的元素
        console.log('Available ranking elements:');
        document.querySelectorAll('[id*="ranking"]').forEach(el => {
            console.log('-', el.id);
        });
    }
    
    // 设置按钮激活状态
    if (event && event.target) {
        event.target.classList.add('active');
    }
}

function loadRankings() {
    loadRankingData('industries');
}

function loadRankingData(type) {
    const url = `/api/rankings/${type}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayRankingData(type, data.data.rankings);
            } else {
                console.error('加载排名数据失败:', data.error);
                showError('加载排名数据失败: ' + data.error);
            }
        })
        .catch(error => {
            console.error('加载排名数据失败:', error);
            showError('加载排名数据失败: ' + error.message);
        });
}

function displayRankingData(type, rankings) {
    let tbodyId;
    if (type === 'industries') {
        tbodyId = 'industry-ranking-body';
    } else if (type === 'companies') {
        tbodyId = 'company-ranking-body';
    } else if (type === 'trends') {
        tbodyId = 'trend-ranking-body';
    } else {
        tbodyId = type + '-ranking-body';
    }
    
    const tbody = document.getElementById(tbodyId);
    
    if (!tbody) {
        console.error('找不到表格体元素:', tbodyId);
        return;
    }
    
    tbody.innerHTML = '';
    
    if (rankings.length === 0) {
        let colspan = 5; // 默认5列
        if (type === 'companies') {
            colspan = 6; // 公司排名有6列
        } else if (type === 'trends') {
            colspan = 5; // 趋势排名有5列
        }
        tbody.innerHTML = `<tr><td colspan="${colspan}" style="text-align: center; color: #666;">暂无排名数据</td></tr>`;
        return;
    }
    
    rankings.forEach((item, index) => {
        const row = document.createElement('tr');
        
        if (type === 'industries') {
            row.innerHTML = `
                <td>${index + 1}</td>
                <td><strong>${item.industry || '未知行业'}</strong></td>
                <td><span class="heat-score">${item.heat_score || 0}</span></td>
                <td>${item.count || 0}</td>
                <td><span class="trend-badge ${item.trend || 'unknown'}">${getTrendText(item.trend)}</span></td>
            `;
        } else if (type === 'companies') {
            row.innerHTML = `
                <td>${index + 1}</td>
                <td><strong>${item.company || '未知公司'}</strong></td>
                <td><span class="heat-score">${item.heat_score || 0}</span></td>
                <td>${item.count || 0}</td>
                <td>${item.industry || '未知行业'}</td>
                <td><span class="trend-badge ${item.trend || 'unknown'}">${getTrendText(item.trend)}</span></td>
            `;
        } else if (type === 'trends') {
            row.innerHTML = `
                <td>${index + 1}</td>
                <td><strong>${item.trend || '未知趋势'}</strong></td>
                <td><span class="heat-score">${item.heat_score || 0}</span></td>
                <td>${item.count || 0}</td>
                <td><span class="category-badge">${item.category || '未分类'}</span></td>
            `;
        }
        
        tbody.appendChild(row);
    });
}

function getTrendText(trend) {
    if (!trend) return '未知';
    
    switch (trend) {
        case 'up': return '上升';
        case 'down': return '下降';
        case 'stable': return '稳定';
        default: return '未知';
    }
}

function refreshRankings() {
    const activeTab = document.querySelector('.tab-btn.active');
    if (activeTab) {
        const tabName = activeTab.getAttribute('onclick').match(/'([^']+)'/)[1];
        loadRankingData(tabName);
    }
}

// 更新导航激活状态
function updateActiveNav(page) {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const navItem = document.querySelector(`[onclick*="${page}"]`);
    if (navItem) {
        navItem.classList.add('active');
    }
}

// 加载热度排名数据
function loadRankings() {
    // 默认加载行业排名
    loadRankingData('industries');
}

// 加载分析数据
function loadAnalysis() {
    // 加载分析数据
    fetch('/api/statistics')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateAnalysisCharts(data.data);
            }
        })
        .catch(error => {
            console.error('加载分析数据失败:', error);
            showError('加载分析数据失败');
        });
}

// 更新分析图表
function updateAnalysisCharts(data) {
    // 这里可以添加更详细的分析图表
    console.log('更新分析图表:', data);
}

 