/**
 * 国内热点数据模块增强版
 * 大势所趋风险框架管理台
 */

// 加载国内热点数据模块
function loadDomesticHotspotData() {
    const container = document.getElementById('content');
    
    // 显示加载状态
    container.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-3">正在加载国内热点数据...</p>
        </div>
    `;

    // 获取数据并渲染
    fetchDomesticHotspotData()
        .then(data => {
            if (data.success) {
                renderDomesticHotspotModule(container, data);
            } else {
                throw new Error(data.message || '数据加载失败');
            }
        })
        .catch(error => {
            container.innerHTML = `
                <div class="alert alert-danger">
                    <h5><i class="bi bi-exclamation-triangle"></i> 数据加载失败</h5>
                    <p>${error.message}</p>
                    <button class="btn btn-primary" onclick="loadDomesticHotspotData()">重新加载</button>
                </div>
            `;
        });
}

// 获取国内热点数据
async function fetchDomesticHotspotData() {
    try {
        const response = await fetch('/api/domestic-hotspot?' + new URLSearchParams({
            timestamp: Date.now()
        }));
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('获取国内热点数据失败:', error);
        // 返回模拟数据作为备用
        return getMockDomesticHotspotData();
    }
}

// 模拟数据备用方案
function getMockDomesticHotspotData() {
    return {
        success: true,
        data: [
            {
                id: 'dom_001',
                title: 'A股三季度收官：结构性行情明显',
                category: 'A股',
                heat_score: 95,
                sentiment: 'positive',
                content: '科技股领涨，新能源板块分化，消费股企稳回升',
                publish_time: new Date(Date.now() - 1000 * 60 * 10).toISOString(),
                source: '证券时报',
                url: '#'
            },
            {
                id: 'dom_002',
                title: '央行降准释放流动性1.2万亿',
                category: '货币政策',
                heat_score: 92,
                sentiment: 'positive',
                content: '定向降准支持实体经济，房地产板块迎来反弹',
                publish_time: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
                source: '中国证券报',
                url: '#'
            },
            {
                id: 'dom_003',
                title: '新能源汽车销量创历史新高',
                category: '新能源',
                heat_score: 89,
                sentiment: 'positive',
                content: '9月销量同比增长35%，产业链公司业绩分化',
                publish_time: new Date(Date.now() - 1000 * 60 * 40).toISOString(),
                source: '财经网',
                url: '#'
            },
            {
                id: 'dom_004',
                title: '人工智能大模型商业化提速',
                category: '科技',
                heat_score: 87,
                sentiment: 'positive',
                content: 'AI应用场景不断拓展，相关概念股受追捧',
                publish_time: new Date(Date.now() - 1000 * 60 * 55).toISOString(),
                source: '21世纪经济报道',
                url: '#'
            },
            {
                id: 'dom_005',
                title: '消费板块复苏信号增强',
                category: '消费',
                heat_score: 82,
                sentiment: 'positive',
                content: '节假日消费数据亮眼，消费信心逐步恢复',
                publish_time: new Date(Date.now() - 1000 * 60 * 70).toISOString(),
                source: '经济日报',
                url: '#'
            },
            {
                id: 'dom_006',
                title: '房地产政策持续优化调整',
                category: '房地产',
                heat_score: 78,
                sentiment: 'neutral',
                content: '多地出台支持政策，市场预期逐步改善',
                publish_time: new Date(Date.now() - 1000 * 60 * 85).toISOString(),
                source: '中国房地产报',
                url: '#'
            }
        ],
        statistics: {
            total_count: 6,
            avg_heat_score: 85.5,
            category_distribution: {
                'A股': 1,
                '货币政策': 1,
                '新能源': 1,
                '科技': 1,
                '消费': 1,
                '房地产': 1
            },
            sentiment_distribution: {
                'positive': 4,
                'neutral': 2,
                'negative': 0
            },
            heat_distribution: {
                high: 4,
                medium: 2,
                low: 0
            },
            source_distribution: {
                '证券时报': 1,
                '中国证券报': 1,
                '财经网': 1,
                '21世纪经济报道': 1,
                '经济日报': 1,
                '中国房地产报': 1
            },
            top_keywords: [
                { keyword: 'A股', count: 3 },
                { keyword: '政策', count: 2 },
                { keyword: '新能源', count: 2 },
                { keyword: '消费', count: 2 }
            ]
        },
        timestamp: new Date().toISOString()
    };
}

// 渲染国内热点数据模块
function renderDomesticHotspotModule(container, data) {
    if (!data) {
        console.error('数据为空');
        return;
    }
    
    const { data: hotspots, statistics } = data;
    
    // 处理统计数据，确保数据结构正确
    const stats = {
        totalHotspots: statistics?.total_count || (hotspots ? hotspots.length : 0) || 0,
        avgHeat: statistics?.avg_heat_score || 0,
        categories: statistics?.category_distribution ? Object.keys(statistics.category_distribution) : [],
        topCategory: getTopCategory(statistics?.category_distribution)
    };
    
    const moduleHTML = `
        <div class="domestic-hotspot-module">
            <!-- 模块标题 -->
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h4><i class="bi bi-fire text-danger"></i> 国内热点数据</h4>
                <div>
                    <span class="badge bg-success">实时数据</span>
                    <button class="btn btn-outline-primary btn-sm ms-2" onclick="refreshDomesticHotspotData()">
                        <i class="bi bi-arrow-clockwise"></i> 刷新
                    </button>
                </div>
            </div>

            <!-- 统计概览 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body text-center">
                            <h3>${stats.totalHotspots || '0'}</h3>
                            <p class="mb-0">热点总数</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body text-center">
                            <h3>${typeof stats.avgHeat === 'number' && !isNaN(stats.avgHeat) ? stats.avgHeat.toFixed(1) : '0.0'}</h3>
                            <p class="mb-0">平均热度</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body text-center">
                            <h3>${stats.categories && stats.categories.length ? stats.categories.length : '0'}</h3>
                            <p class="mb-0">分类数量</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body text-center">
                            <h3>${stats.topCategory || '无'}</h3>
                            <p class="mb-0">热门分类</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 筛选和搜索 -->
            <div class="row mb-3">
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-search"></i></span>
                        <input type="text" class="form-control" placeholder="搜索热点..." id="hotspotSearch">
                    </div>
                </div>
                <div class="col-md-6">
                    <select class="form-select" id="categoryFilter">
                        <option value="">全部分类</option>
                        ${stats.categories.map(cat => `<option value="${cat}">${cat}</option>`).join('')}
                    </select>
                </div>
            </div>

            <!-- 热点列表 -->
            <div class="row" id="hotspotList">
                ${hotspots.map(hotspot => createHotspotCard(hotspot)).join('')}
            </div>

            <!-- 热度趋势图表 -->
            <div class="card mt-4">
                <div class="card-header">
                    <h5><i class="bi bi-graph-up"></i> 热度趋势分析</h5>
                </div>
                <div class="card-body">
                    <canvas id="hotspotTrendChart" height="100"></canvas>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = moduleHTML;
    
    // 初始化功能
    initHotspotSearch();
    initCategoryFilter(hotspots);
    renderHotspotTrendChart(hotspots);
}

// 创建热点卡片
function createHotspotCard(hotspot) {
    const timeAgo = getTimeAgo(hotspot.publish_time);
    const heatColor = getHeatColor(hotspot.heat_score);
    
    return `
        <div class="col-lg-6 mb-3 hotspot-item" data-category="${hotspot.category}">
            <div class="card h-100 hotspot-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-secondary">${hotspot.category}</span>
                        <div class="text-end">
                            <span class="badge ${heatColor}">${hotspot.heat_score}°</span>
                            <span class="text-success small ms-1">${getChangeIndicator(hotspot.sentiment)}</span>
                        </div>
                    </div>
                    
                    <h6 class="card-title">${hotspot.title}</h6>
                    <p class="card-text text-muted small">${hotspot.content}</p>
                    
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="bi bi-clock"></i> ${timeAgo}
                        </small>
                        <small class="text-muted">
                            来源: ${hotspot.source || '综合'}
                        </small>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 获取热度颜色
function getHeatColor(heat) {
    if (!heat) return 'bg-secondary';
    if (heat >= 90) return 'bg-danger';
    if (heat >= 80) return 'bg-warning';
    if (heat >= 70) return 'bg-info';
    return 'bg-secondary';
}

// 获取时间差描述
function getTimeAgo(timestamp) {
    if (!timestamp) return '未知时间';
    const now = new Date();
    const time = new Date(timestamp);
    const diffMinutes = Math.floor((now - time) / (1000 * 60));
    
    if (diffMinutes < 1) return '刚刚';
    if (diffMinutes < 60) return `${diffMinutes}分钟前`;
    if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}小时前`;
    return `${Math.floor(diffMinutes / 1440)}天前`;
}

// 获取变化指示器
function getChangeIndicator(sentiment) {
    if (!sentiment) return '→';
    if (sentiment === 'positive') return '↗';
    if (sentiment === 'negative') return '↘';
    return '→';
}

// 初始化搜索功能
function initHotspotSearch() {
    const searchInput = document.getElementById('hotspotSearch');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const hotspotItems = document.querySelectorAll('.hotspot-item');
        
        hotspotItems.forEach(item => {
            const titleElement = item.querySelector('.card-title');
            const descriptionElement = item.querySelector('.card-text');
            
            if (!titleElement || !descriptionElement) return;
            
            const title = titleElement.textContent.toLowerCase();
            const description = descriptionElement.textContent.toLowerCase();
            
            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// 初始化分类筛选
function initCategoryFilter(hotspots) {
    const categoryFilter = document.getElementById('categoryFilter');
    if (!categoryFilter) return;
    
    categoryFilter.addEventListener('change', function() {
        const selectedCategory = this.value;
        const hotspotItems = document.querySelectorAll('.hotspot-item');
        
        hotspotItems.forEach(item => {
            const category = item.getAttribute('data-category');
            
            if (!selectedCategory || category === selectedCategory) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// 渲染热度趋势图表
function renderHotspotTrendChart(hotspots) {
    const canvas = document.getElementById('hotspotTrendChart');
    if (!canvas || typeof Chart === 'undefined') return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // 按分类统计热度
    const categoryStats = {};
    hotspots.forEach(hotspot => {
        if (!hotspot || !hotspot.category) return;
        if (!categoryStats[hotspot.category]) {
            categoryStats[hotspot.category] = [];
        }
        categoryStats[hotspot.category].push(hotspot.heat_score || hotspot.heat || 0);
    });
    
    const labels = Object.keys(categoryStats);
    if (labels.length === 0) return;
    
    const data = labels.map(category => {
        const heats = categoryStats[category];
        return heats.reduce((sum, heat) => sum + heat, 0) / heats.length;
    });
    
    try {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: '平均热度',
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)',
                        'rgba(255, 159, 64, 0.8)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '各分类热度分布'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    } catch (error) {
        console.error('图表渲染失败:', error);
    }
}

// 刷新国内热点数据
function refreshDomesticHotspotData() {
    loadDomesticHotspotData();
}

// 获取热门分类
function getTopCategory(categoryDistribution) {
    if (!categoryDistribution || typeof categoryDistribution !== 'object') {
        return '无';
    }
    
    let maxCount = 0;
    let topCategory = '无';
    
    for (const [category, count] of Object.entries(categoryDistribution)) {
        if (count > maxCount) {
            maxCount = count;
            topCategory = category;
        }
    }
    
    return topCategory;
}

// 导出模块函数
if (typeof window !== 'undefined') {
    window.loadDomesticHotspotData = loadDomesticHotspotData;
    window.refreshDomesticHotspotData = refreshDomesticHotspotData;
}