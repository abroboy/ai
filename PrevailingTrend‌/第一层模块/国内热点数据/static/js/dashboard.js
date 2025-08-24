/**
 * 国内热点数据管理台 JavaScript
 */

// 全局变量
let currentPage = 1;
let currentView = 'dashboard';

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
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
    document.getElementById('hotspots-content').style.display = 'block';
    currentView = 'hotspots';
    loadHotspots();
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
    document.getElementById('collection-content').style.display = 'block';
    currentView = 'collection';
    loadCollection();
}

// 显示系统设置
function showSettings() {
    hideAllContent();
    document.getElementById('settings-content').style.display = 'block';
    currentView = 'settings';
    loadSettings();
}

// 隐藏所有内容
function hideAllContent() {
    const contents = [
        'dashboard-content',
        'hotspots-content', 
        'statistics-content',
        'collection-content',
        'settings-content'
    ];
    
    contents.forEach(id => {
        document.getElementById(id).style.display = 'none';
    });
    
    // 清除所有导航激活状态
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // 设置当前导航为激活状态
    event.target.classList.add('active');
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
    document.getElementById('total-hotspots').textContent = stats.total_count;
    document.getElementById('avg-heat').textContent = stats.avg_heat;
    document.getElementById('avg-sentiment').textContent = stats.avg_sentiment;
    document.getElementById('active-hotspots').textContent = stats.by_status.active || 0;
}

// 创建简单图表
function createSimpleCharts(stats) {
    // 类型分布图
    createSimplePieChart('type-chart', stats.by_type, '热点类型分布');
    
    // 级别分布图
    createSimpleBarChart('level-chart', stats.by_level, '热度级别分布');
}

// 创建简单饼图
function createSimplePieChart(containerId, data, title) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const colors = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#06b6d4'];
    let html = `<h4 style="text-align: center; margin-bottom: 1rem;">${title}</h4>`;
    
    let total = 0;
    for (let key in data) {
        total += data[key];
    }
    
    let colorIndex = 0;
    for (let key in data) {
        const percentage = total > 0 ? ((data[key] / total) * 100).toFixed(1) : 0;
        const color = colors[colorIndex % colors.length];
        html += `
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="width: 20px; height: 20px; background: ${color}; border-radius: 50%; margin-right: 0.5rem;"></div>
                <span style="flex: 1;">${getTypeLabel(key)}</span>
                <span style="font-weight: bold;">${data[key]} (${percentage}%)</span>
            </div>
        `;
        colorIndex++;
    }
    
    container.innerHTML = html;
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

// 加载热点列表
function loadHotspots(page = 1) {
    currentPage = page;
    
    const params = new URLSearchParams({
        page: page,
        per_page: 20
    });
    
    // 添加筛选参数
    const type = document.getElementById('filter-type').value;
    const level = document.getElementById('filter-level').value;
    const source = document.getElementById('filter-source').value;
    const minHeat = document.getElementById('filter-min-heat').value;
    
    if (type) params.append('hotspot_type', type);
    if (level) params.append('hotspot_level', level);
    if (source) params.append('source', source);
    if (minHeat) params.append('min_heat_score', minHeat);
    
    fetch(`/api/hotspots?${params}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderHotspotsTable(data.data.hotspots);
                renderPagination(data.data.pagination);
            }
        })
        .catch(error => {
            console.error('加载热点列表失败:', error);
            showError('加载热点列表失败');
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

// 渲染分页
function renderPagination(pagination) {
    const paginationEl = document.getElementById('pagination');
    paginationEl.innerHTML = '';
    
    const { page, pages } = pagination;
    
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
    fetch(`/api/hotspots/${hotspotId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showHotspotModal(data.data);
            }
        })
        .catch(error => {
            console.error('加载热点详情失败:', error);
            showError('加载热点详情失败');
        });
}

// 显示热点模态框
function showHotspotModal(hotspot) {
    const modalBody = document.getElementById('hotspot-modal-body');
    modalBody.innerHTML = `
        <div style="margin-bottom: 1rem;">
            <h4>${hotspot.title}</h4>
            <p style="color: #666; margin-top: 0.5rem;">${hotspot.content}</p>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
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
        <div style="margin-top: 1rem;">
            <p><strong>关键词:</strong> ${hotspot.keywords.join(', ')}</p>
            <p><strong>相关公司:</strong> ${hotspot.related_companies.join(', ')}</p>
            <p><strong>相关行业:</strong> ${hotspot.related_industries.join(', ')}</p>
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
    // 加载统计分析数据
    fetch('/api/statistics')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                createSimplePieChart('keywords-chart', data.data.top_keywords.reduce((acc, [key, value]) => {
                    acc[key] = value;
                    return acc;
                }, {}), '关键词统计');
                
                createSimplePieChart('companies-chart', data.data.top_companies.reduce((acc, [key, value]) => {
                    acc[key] = value;
                    return acc;
                }, {}), '相关公司统计');
            }
        })
        .catch(error => {
            console.error('加载统计数据失败:', error);
            showError('加载统计数据失败');
        });
}

function loadCollection() {
    // 加载采集页面数据
    document.getElementById('collection-status').style.display = 'none';
}

function loadSettings() {
    // 加载设置页面数据
} 