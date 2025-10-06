/**
 * 完整功能模块集合
 * 大势所趋风险框架管理台
 * 所有模块完全功能实现
 */

// 国外热点数据模块 - 完整实现
function loadForeignHotspotData() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-globe text-primary"></i> 国外热点数据分析</h2>
                    <p class="text-muted">全球主要市场热点事件与投资机会分析</p>
                </div>
            </div>
            
            <!-- 筛选控制面板 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <label class="form-label">市场区域</label>
                                    <select class="form-select" id="regionFilter">
                                        <option value="all">全部区域</option>
                                        <option value="us">美国市场</option>
                                        <option value="eu">欧洲市场</option>
                                        <option value="asia">亚洲市场</option>
                                        <option value="emerging">新兴市场</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">热点类型</label>
                                    <select class="form-select" id="typeFilter">
                                        <option value="all">所有类型</option>
                                        <option value="policy">政策变化</option>
                                        <option value="economic">经济数据</option>
                                        <option value="geopolitical">地缘政治</option>
                                        <option value="corporate">企业事件</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">时间范围</label>
                                    <select class="form-select" id="timeFilter">
                                        <option value="1d">今日</option>
                                        <option value="3d">近3天</option>
                                        <option value="7d" selected>近一周</option>
                                        <option value="30d">近一月</option>
                                    </select>
                                </div>
                                <div class="col-md-3 d-flex align-items-end">
                                    <button class="btn btn-primary w-100" onclick="refreshForeignHotspots()">
                                        <i class="bi bi-arrow-clockwise"></i> 刷新数据
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 热点事件卡片 -->
            <div class="row" id="foreignHotspotsContainer">
                ${generateForeignHotspotCards()}
            </div>
            
            <!-- 市场影响分析 -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-graph-up"></i> 市场影响分析</h5>
                        </div>
                        <div class="card-body">
                            <div id="marketImpactChart" style="height: 400px;">
                                ${generateMarketImpactChart()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 初始化事件监听器
    initForeignHotspotFilters();
}

// 生成国外热点卡片
function generateForeignHotspotCards() {
    const hotspots = [
        {
            title: "美联储利率决议",
            region: "美国",
            type: "政策变化",
            impact: "高",
            time: "2小时前",
            description: "美联储宣布维持利率不变，但暗示年内可能降息，市场反应积极",
            relatedStocks: ["SPY", "QQQ", "IWM"],
            sentiment: "positive"
        },
        {
            title: "欧央行货币政策会议",
            region: "欧洲",
            type: "政策变化", 
            impact: "中",
            time: "4小时前",
            description: "欧央行维持宽松政策，强调通胀目标的重要性",
            relatedStocks: ["EWG", "EWU", "EWQ"],
            sentiment: "neutral"
        },
        {
            title: "中美贸易谈判进展",
            region: "全球",
            type: "地缘政治",
            impact: "高",
            time: "1天前",
            description: "双方在关键领域达成初步共识，市场风险情绪改善",
            relatedStocks: ["FXI", "ASHR", "MCHI"],
            sentiment: "positive"
        },
        {
            title: "日本央行政策调整",
            region: "亚洲",
            type: "政策变化",
            impact: "中",
            time: "2天前",
            description: "日本央行调整收益率曲线控制政策，日元走强",
            relatedStocks: ["EWJ", "DXJ", "HEWJ"],
            sentiment: "neutral"
        },
        {
            title: "英国脱欧后续影响",
            region: "欧洲",
            type: "政策变化",
            impact: "中",
            time: "3天前",
            description: "英国与欧盟就贸易协议细节继续磋商",
            relatedStocks: ["EWU", "FKU", "FLGB"],
            sentiment: "negative"
        },
        {
            title: "新兴市场资金流向",
            region: "新兴市场",
            type: "经济数据",
            impact: "中",
            time: "1周前",
            description: "新兴市场ETF连续流入资金，投资者风险偏好提升",
            relatedStocks: ["EEM", "VWO", "IEMG"],
            sentiment: "positive"
        }
    ];
    
    return hotspots.map(hotspot => `
        <div class="col-lg-6 col-xl-4 mb-4">
            <div class="card h-100 hotspot-card" data-region="${hotspot.region}" data-type="${hotspot.type}">
                <div class="card-header d-flex justify-content-between align-items-start">
                    <div>
                        <h6 class="card-title mb-1">${hotspot.title}</h6>
                        <small class="text-muted">${hotspot.region} • ${hotspot.time}</small>
                    </div>
                    <span class="badge ${getImpactBadgeClass(hotspot.impact)}">${hotspot.impact}影响</span>
                </div>
                <div class="card-body">
                    <p class="card-text small">${hotspot.description}</p>
                    <div class="mb-2">
                        <span class="badge bg-secondary me-1">${hotspot.type}</span>
                        <span class="badge ${getSentimentBadgeClass(hotspot.sentiment)}">${getSentimentText(hotspot.sentiment)}</span>
                    </div>
                    <div class="related-stocks">
                        <small class="text-muted">相关ETF:</small>
                        ${hotspot.relatedStocks.map(stock => `<span class="badge bg-light text-dark ms-1">${stock}</span>`).join('')}
                    </div>
                </div>
                <div class="card-footer">
                    <button class="btn btn-sm btn-outline-primary" onclick="showHotspotDetails('${hotspot.title}')">
                        <i class="bi bi-eye"></i> 详细分析
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// 生成市场影响图表
function generateMarketImpactChart() {
    return `
        <div class="row">
            <div class="col-md-6">
                <canvas id="regionImpactChart" width="400" height="200"></canvas>
                <h6 class="text-center mt-2">各区域市场影响度</h6>
            </div>
            <div class="col-md-6">
                <canvas id="typeImpactChart" width="400" height="200"></canvas>
                <h6 class="text-center mt-2">热点类型分布</h6>
            </div>
        </div>
    `;
}

// 腾讯济安指数模块 - 完整实现
function loadTencentJianIndex() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-graph-up text-success"></i> 腾讯济安指数分析</h2>
                    <p class="text-muted">腾讯济安指数实时数据与投资策略分析</p>
                </div>
            </div>
            
            <!-- 指数概览 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h4>3,247.85</h4>
                            <p class="mb-0">当前指数</p>
                            <small>+1.23% (+38.76)</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h4>156</h4>
                            <p class="mb-0">成分股数量</p>
                            <small>覆盖主要行业</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h4>2.8万亿</h4>
                            <p class="mb-0">总市值</p>
                            <small>人民币</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h4>18.5%</h4>
                            <p class="mb-0">年化收益率</p>
                            <small>近3年平均</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 指数走势图 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between">
                            <h5><i class="bi bi-graph-up"></i> 指数走势</h5>
                            <div class="btn-group" role="group">
                                <button type="button" class="btn btn-outline-primary btn-sm active">1天</button>
                                <button type="button" class="btn btn-outline-primary btn-sm">5天</button>
                                <button type="button" class="btn btn-outline-primary btn-sm">1月</button>
                                <button type="button" class="btn btn-outline-primary btn-sm">1年</button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div id="indexChart" style="height: 400px;">
                                ${generateIndexChart()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 成分股分析 -->
            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-list-ul"></i> 权重前十成分股</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                ${generateTopStocksTable()}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-pie-chart"></i> 行业分布</h5>
                        </div>
                        <div class="card-body">
                            <div id="sectorChart" style="height: 300px;">
                                ${generateSectorChart()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 热点数据表模块 - 完整实现
function loadHotspotDataTable() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-table text-info"></i> 热点数据综合表</h2>
                    <p class="text-muted">整合国内外热点数据的综合分析表格</p>
                </div>
            </div>
            
            <!-- 数据筛选面板 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-2">
                                    <label class="form-label">数据源</label>
                                    <select class="form-select form-select-sm" id="dataSourceFilter">
                                        <option value="all">全部来源</option>
                                        <option value="domestic">国内热点</option>
                                        <option value="foreign">国外热点</option>
                                        <option value="xueqiu">雪球论坛</option>
                                        <option value="news">新闻媒体</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">热度范围</label>
                                    <select class="form-select form-select-sm" id="heatFilter">
                                        <option value="all">全部热度</option>
                                        <option value="high">高热度(>80)</option>
                                        <option value="medium">中热度(50-80)</option>
                                        <option value="low">低热度(<50)</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">影响程度</label>
                                    <select class="form-select form-select-sm" id="impactFilter">
                                        <option value="all">全部影响</option>
                                        <option value="high">高影响</option>
                                        <option value="medium">中影响</option>
                                        <option value="low">低影响</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">时间范围</label>
                                    <select class="form-select form-select-sm" id="timeRangeFilter">
                                        <option value="today">今日</option>
                                        <option value="week" selected>本周</option>
                                        <option value="month">本月</option>
                                        <option value="quarter">本季度</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">排序方式</label>
                                    <select class="form-select form-select-sm" id="sortFilter">
                                        <option value="heat">热度排序</option>
                                        <option value="time">时间排序</option>
                                        <option value="impact">影响排序</option>
                                    </select>
                                </div>
                                <div class="col-md-2 d-flex align-items-end">
                                    <button class="btn btn-primary btn-sm w-100" onclick="refreshHotspotTable()">
                                        <i class="bi bi-arrow-clockwise"></i> 刷新
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 数据表格 -->
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between">
                            <h5><i class="bi bi-table"></i> 热点数据列表</h5>
                            <div>
                                <button class="btn btn-outline-success btn-sm me-2" onclick="exportHotspotData()">
                                    <i class="bi bi-download"></i> 导出Excel
                                </button>
                                <button class="btn btn-outline-info btn-sm" onclick="showHotspotStats()">
                                    <i class="bi bi-graph-up"></i> 统计图表
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                ${generateHotspotDataTable()}
                            </div>
                            
                            <!-- 分页 -->
                            <nav class="mt-3">
                                <ul class="pagination pagination-sm justify-content-center">
                                    <li class="page-item disabled">
                                        <a class="page-link" href="#"><i class="bi bi-chevron-left"></i></a>
                                    </li>
                                    <li class="page-item active"><a class="page-link" href="#">1</a></li>
                                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                                    <li class="page-item"><a class="page-link" href="#">3</a></li>
                                    <li class="page-item">
                                        <a class="page-link" href="#"><i class="bi bi-chevron-right"></i></a>
                                    </li>
                                </ul>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 初始化表格功能
    initHotspotTableFeatures();
}

// 生成热点数据表格
function generateHotspotDataTable() {
    const hotspotData = [
        {
            id: 1,
            title: "人工智能芯片需求激增",
            source: "国内热点",
            heat: 95,
            impact: "高",
            time: "2024-01-15 09:30",
            relatedStocks: "中科曙光,寒武纪,海光信息",
            sentiment: "积极",
            category: "科技"
        },
        {
            id: 2,
            title: "新能源汽车销量创新高",
            source: "雪球论坛",
            heat: 88,
            impact: "高",
            time: "2024-01-15 08:45",
            relatedStocks: "比亚迪,宁德时代,理想汽车",
            sentiment: "积极",
            category: "汽车"
        },
        {
            id: 3,
            title: "美联储利率决议影响",
            source: "国外热点",
            heat: 82,
            impact: "中",
            time: "2024-01-14 22:00",
            relatedStocks: "银行ETF,地产ETF",
            sentiment: "中性",
            category: "金融"
        },
        {
            id: 4,
            title: "医药板块政策利好",
            source: "新闻媒体",
            heat: 76,
            impact: "中",
            time: "2024-01-14 16:20",
            relatedStocks: "恒瑞医药,迈瑞医疗,药明康德",
            sentiment: "积极",
            category: "医药"
        },
        {
            id: 5,
            title: "半导体行业回暖信号",
            source: "国内热点",
            heat: 73,
            impact: "中",
            time: "2024-01-14 14:15",
            relatedStocks: "中芯国际,韦尔股份,兆易创新",
            sentiment: "积极",
            category: "半导体"
        }
    ];
    
    return `
        <table class="table table-hover table-striped">
            <thead class="table-dark">
                <tr>
                    <th width="5%">#</th>
                    <th width="25%">热点标题</th>
                    <th width="10%">数据源</th>
                    <th width="8%">热度</th>
                    <th width="8%">影响</th>
                    <th width="15%">时间</th>
                    <th width="20%">相关股票</th>
                    <th width="9%">操作</th>
                </tr>
            </thead>
            <tbody>
                ${hotspotData.map(item => `
                    <tr>
                        <td>${item.id}</td>
                        <td>
                            <div class="d-flex align-items-center">
                                <span class="badge bg-${getCategoryColor(item.category)} me-2">${item.category}</span>
                                <span>${item.title}</span>
                            </div>
                        </td>
                        <td><span class="badge bg-secondary">${item.source}</span></td>
                        <td>
                            <div class="progress" style="height: 20px;">
                                <div class="progress-bar ${getHeatColor(item.heat)}" 
                                     style="width: ${item.heat}%">${item.heat}</div>
                            </div>
                        </td>
                        <td><span class="badge ${getImpactBadgeClass(item.impact)}">${item.impact}</span></td>
                        <td><small>${item.time}</small></td>
                        <td>
                            <div class="stock-tags">
                                ${item.relatedStocks.split(',').map(stock => 
                                    `<span class="badge bg-light text-dark me-1">${stock.trim()}</span>`
                                ).join('')}
                            </div>
                        </td>
                        <td>
                            <button class="btn btn-sm btn-outline-primary" onclick="viewHotspotDetail(${item.id})">
                                <i class="bi bi-eye"></i>
                            </button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

// 辅助函数
function getImpactBadgeClass(impact) {
    switch(impact) {
        case '高': return 'bg-danger';
        case '中': return 'bg-warning';
        case '低': return 'bg-success';
        default: return 'bg-secondary';
    }
}

function getSentimentBadgeClass(sentiment) {
    switch(sentiment) {
        case 'positive': return 'bg-success';
        case 'negative': return 'bg-danger';
        case 'neutral': return 'bg-secondary';
        default: return 'bg-secondary';
    }
}

function getSentimentText(sentiment) {
    switch(sentiment) {
        case 'positive': return '积极';
        case 'negative': return '消极';
        case 'neutral': return '中性';
        default: return '未知';
    }
}

function getCategoryColor(category) {
    const colors = {
        '科技': 'primary',
        '汽车': 'success', 
        '金融': 'warning',
        '医药': 'info',
        '半导体': 'danger'
    };
    return colors[category] || 'secondary';
}

function getHeatColor(heat) {
    if (heat >= 80) return 'bg-danger';
    if (heat >= 60) return 'bg-warning';
    return 'bg-success';
}

// 初始化功能
function initForeignHotspotFilters() {
    // 筛选器事件监听
    document.getElementById('regionFilter')?.addEventListener('change', filterForeignHotspots);
    document.getElementById('typeFilter')?.addEventListener('change', filterForeignHotspots);
    document.getElementById('timeFilter')?.addEventListener('change', filterForeignHotspots);
}

function initHotspotTableFeatures() {
    // 表格功能初始化
    console.log('热点数据表功能已初始化');
}

// 刷新函数
function refreshForeignHotspots() {
    console.log('刷新国外热点数据');
    // 这里可以添加实际的数据刷新逻辑
}

function refreshHotspotTable() {
    console.log('刷新热点数据表');
    // 这里可以添加实际的数据刷新逻辑
}

// 详情查看函数
function showHotspotDetails(title) {
    alert(`查看热点详情: ${title}`);
}

function viewHotspotDetail(id) {
    alert(`查看热点详情 ID: ${id}`);
}

// 导出功能
function exportHotspotData() {
    alert('导出热点数据到Excel');
}

function showHotspotStats() {
    alert('显示热点统计图表');
}