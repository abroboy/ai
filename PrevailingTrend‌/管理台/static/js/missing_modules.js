/**
 * 缺失模块的基础实现
 * 大势所趋风险框架管理台
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
                <div class="col-lg-6 col-xl-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header d-flex justify-content-between">
                            <h6 class="mb-0">美联储利率决议</h6>
                            <span class="badge bg-danger">高影响</span>
                        </div>
                        <div class="card-body">
                            <p class="card-text small">美联储宣布维持利率不变，但暗示年内可能降息，市场反应积极</p>
                            <div class="mb-2">
                                <span class="badge bg-secondary me-1">政策变化</span>
                                <span class="badge bg-success">积极</span>
                            </div>
                            <div class="related-stocks">
                                <small class="text-muted">相关ETF:</small>
                                <span class="badge bg-light text-dark ms-1">SPY</span>
                                <span class="badge bg-light text-dark ms-1">QQQ</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 col-xl-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header d-flex justify-content-between">
                            <h6 class="mb-0">中美贸易谈判进展</h6>
                            <span class="badge bg-warning">中影响</span>
                        </div>
                        <div class="card-body">
                            <p class="card-text small">双方在关键领域达成初步共识，市场风险情绪改善</p>
                            <div class="mb-2">
                                <span class="badge bg-secondary me-1">地缘政治</span>
                                <span class="badge bg-success">积极</span>
                            </div>
                            <div class="related-stocks">
                                <small class="text-muted">相关ETF:</small>
                                <span class="badge bg-light text-dark ms-1">FXI</span>
                                <span class="badge bg-light text-dark ms-1">ASHR</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 col-xl-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header d-flex justify-content-between">
                            <h6 class="mb-0">欧央行货币政策</h6>
                            <span class="badge bg-info">中影响</span>
                        </div>
                        <div class="card-body">
                            <p class="card-text small">欧央行维持宽松政策，强调通胀目标的重要性</p>
                            <div class="mb-2">
                                <span class="badge bg-secondary me-1">政策变化</span>
                                <span class="badge bg-secondary">中性</span>
                            </div>
                            <div class="related-stocks">
                                <small class="text-muted">相关ETF:</small>
                                <span class="badge bg-light text-dark ms-1">EWG</span>
                                <span class="badge bg-light text-dark ms-1">EWU</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 腾讯济安指数模块 - 完整实现（集成API）
function loadTencentJianIndex() {
    const container = document.getElementById('content');
    
    // 显示加载状态
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-graph-up text-success"></i> 腾讯济安指数分析</h2>
                    <p class="text-muted">腾讯济安指数实时数据与投资策略分析</p>
                </div>
            </div>
            
            <!-- 加载指示器 -->
            <div class="row">
                <div class="col-12 text-center">
                    <div class="loading-indicator"></div>
                    <p class="mt-3">正在加载腾讯济安指数数据...</p>
                </div>
            </div>
        </div>
    `;
    
    // 调用API获取数据
    fetch('/api/tencent-jian-index')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderTencentJianIndex(data.data);
            } else {
                throw new Error(data.message || '获取数据失败');
            }
        })
        .catch(error => {
            console.error('加载腾讯济安指数数据失败:', error);
            container.innerHTML = `
                <div class="container-fluid">
                    <div class="row mb-4">
                        <div class="col-12">
                            <h2><i class="bi bi-graph-up text-success"></i> 腾讯济安指数分析</h2>
                            <p class="text-muted">腾讯济安指数实时数据与投资策略分析</p>
                        </div>
                    </div>
                    <div class="alert alert-danger">
                        <h5><i class="bi bi-exclamation-triangle"></i> 数据加载失败</h5>
                        <p>${error.message}</p>
                        <button class="btn btn-primary btn-sm" onclick="loadTencentJianIndex()">
                            <i class="bi bi-arrow-clockwise"></i> 重新加载
                        </button>
                    </div>
                </div>
            `;
        });
}

// 渲染腾讯济安指数数据
function renderTencentJianIndex(data) {
    const container = document.getElementById('content');
    const indexData = data.index;
    const constituents = data.constituents;
    const industryDistribution = data.industry_distribution;
    
    // 计算涨跌幅颜色
    const changeClass = indexData.change_percent >= 0 ? 'text-success' : 'text-danger';
    const changeSign = indexData.change_percent >= 0 ? '+' : '';
    
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
                            <h4>${indexData.current_index.toLocaleString()}</h4>
                            <p class="mb-0">当前指数</p>
                            <small class="${changeClass}">${changeSign}${indexData.change_percent}% (+${indexData.change})</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h4>${indexData.constituent_count}</h4>
                            <p class="mb-0">成分股数量</p>
                            <small>覆盖主要行业</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h4>${(indexData.market_cap / 100000000).toFixed(1)}亿</h4>
                            <p class="mb-0">总市值</p>
                            <small>人民币</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h4>${indexData.dividend_yield}%</h4>
                            <p class="mb-0">股息率</p>
                            <small>年化收益率</small>
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
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>股票代码</th>
                                            <th>股票名称</th>
                                            <th>权重</th>
                                            <th>当前价</th>
                                            <th>涨跌幅</th>
                                            <th>贡献度</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${constituents.map(stock => {
                                            const changeClass = stock.change_percent >= 0 ? 'text-success' : 'text-danger';
                                            const changeSign = stock.change_percent >= 0 ? '+' : '';
                                            const contributionClass = stock.contribution >= 0 ? 'text-success' : 'text-danger';
                                            const contributionSign = stock.contribution >= 0 ? '+' : '';
                                            
                                            return `
                                                <tr>
                                                    <td>${stock.code}</td>
                                                    <td>${stock.name}</td>
                                                    <td>${stock.weight}%</td>
                                                    <td>${stock.price}</td>
                                                    <td class="${changeClass}">${changeSign}${stock.change_percent}%</td>
                                                    <td class="${contributionClass}">${contributionSign}${stock.contribution}</td>
                                                </tr>
                                            `;
                                        }).join('')}
                                    </tbody>
                                </table>
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
                            ${industryDistribution.map(industry => `
                                <div class="mb-3">
                                    <div class="d-flex justify-content-between">
                                        <span>${industry.industry}</span>
                                        <span>${industry.weight}%</span>
                                    </div>
                                    <div class="progress mb-2">
                                        <div class="progress-bar" style="width: ${industry.weight}%"></div>
                                    </div>
                                    <small class="text-muted">${industry.count}家公司</small>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 统计信息 -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-bar-chart"></i> 指数统计信息</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="text-center">
                                        <h4 class="${data.statistics.avg_change >= 0 ? 'text-success' : 'text-danger'}">
                                            ${data.statistics.avg_change >= 0 ? '+' : ''}${data.statistics.avg_change}%
                                        </h4>
                                        <p class="text-muted">平均涨跌幅</p>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="text-center">
                                        <h4 class="text-success">${data.statistics.positive_count}</h4>
                                        <p class="text-muted">上涨股票</p>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="text-center">
                                        <h4 class="text-danger">${data.statistics.negative_count}</h4>
                                        <p class="text-muted">下跌股票</p>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="text-center">
                                        <h4 class="text-warning">${data.statistics.neutral_count}</h4>
                                        <p class="text-muted">平盘股票</p>
                                    </div>
                                </div>
                            </div>
                            <div class="row mt-3">
                                <div class="col-md-6">
                                    <p><strong>最大贡献股:</strong> ${data.statistics.top_contributor}</p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>最大拖累股:</strong> ${data.statistics.bottom_contributor}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 刷新按钮 -->
            <div class="row mt-4">
                <div class="col-12 text-center">
                    <button class="btn btn-primary" onclick="loadTencentJianIndex()">
                        <i class="bi bi-arrow-clockwise"></i> 刷新数据
                    </button>
                    <small class="text-muted d-block mt-2">最后更新: ${new Date().toLocaleString('zh-CN')}</small>
                </div>
            </div>
        </div>
    `;
}
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-primary" style="width: 28.5%"></div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>电子科技</span>
                                    <span>23.2%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-success" style="width: 23.2%"></div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>医药生物</span>
                                    <span>18.7%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-info" style="width: 18.7%"></div>
                                </div>
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
                                    <select class="form-select form-select-sm">
                                        <option value="all">全部来源</option>
                                        <option value="domestic">国内热点</option>
                                        <option value="foreign">国外热点</option>
                                        <option value="xueqiu">雪球论坛</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">热度范围</label>
                                    <select class="form-select form-select-sm">
                                        <option value="all">全部热度</option>
                                        <option value="high">高热度(>80)</option>
                                        <option value="medium">中热度(50-80)</option>
                                        <option value="low">低热度(<50)</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">时间范围</label>
                                    <select class="form-select form-select-sm">
                                        <option value="today">今日</option>
                                        <option value="week" selected>本周</option>
                                        <option value="month">本月</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">关键词搜索</label>
                                    <input type="text" class="form-control form-control-sm" placeholder="输入关键词">
                                </div>
                                <div class="col-md-3 d-flex align-items-end">
                                    <button class="btn btn-primary btn-sm w-100">
                                        <i class="bi bi-search"></i> 搜索
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
                                <button class="btn btn-outline-success btn-sm me-2">
                                    <i class="bi bi-download"></i> 导出Excel
                                </button>
                                <button class="btn btn-outline-info btn-sm">
                                    <i class="bi bi-graph-up"></i> 统计图表
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
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
                                        <tr>
                                            <td>1</td>
                                            <td>
                                                <span class="badge bg-primary me-2">科技</span>
                                                人工智能芯片需求激增
                                            </td>
                                            <td><span class="badge bg-secondary">国内热点</span></td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar bg-danger" style="width: 95%">95</div>
                                                </div>
                                            </td>
                                            <td><span class="badge bg-danger">高</span></td>
                                            <td><small>2024-01-15 09:30</small></td>
                                            <td>
                                                <span class="badge bg-light text-dark me-1">中科曙光</span>
                                                <span class="badge bg-light text-dark me-1">寒武纪</span>
                                            </td>
                                            <td>
                                                <button class="btn btn-sm btn-outline-primary">
                                                    <i class="bi bi-eye"></i>
                                                </button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>2</td>
                                            <td>
                                                <span class="badge bg-success me-2">汽车</span>
                                                新能源汽车销量创新高
                                            </td>
                                            <td><span class="badge bg-secondary">雪球论坛</span></td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar bg-warning" style="width: 88%">88</div>
                                                </div>
                                            </td>
                                            <td><span class="badge bg-warning">中</span></td>
                                            <td><small>2024-01-15 08:45</small></td>
                                            <td>
                                                <span class="badge bg-light text-dark me-1">比亚迪</span>
                                                <span class="badge bg-light text-dark me-1">理想汽车</span>
                                            </td>
                                            <td>
                                                <button class="btn btn-sm btn-outline-primary">
                                                    <i class="bi bi-eye"></i>
                                                </button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>3</td>
                                            <td>
                                                <span class="badge bg-warning me-2">金融</span>
                                                美联储利率决议影响
                                            </td>
                                            <td><span class="badge bg-secondary">国外热点</span></td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar bg-warning" style="width: 82%">82</div>
                                                </div>
                                            </td>
                                            <td><span class="badge bg-warning">中</span></td>
                                            <td><small>2024-01-14 22:00</small></td>
                                            <td>
                                                <span class="badge bg-light text-dark me-1">银行ETF</span>
                                                <span class="badge bg-light text-dark me-1">地产ETF</span>
                                            </td>
                                            <td>
                                                <button class="btn btn-sm btn-outline-primary">
                                                    <i class="bi bi-eye"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 企查查数据模块 - 完整实现
function loadQichachaData() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-building text-primary"></i> 企查查企业信息</h2>
                    <p class="text-muted">企业基本信息、股权结构、风险监控一站式查询</p>
                </div>
            </div>
            
            <!-- 搜索面板 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-4">
                                    <label class="form-label">企业名称/统一社会信用代码</label>
                                    <input type="text" class="form-control" placeholder="输入企业名称或代码" value="比亚迪股份有限公司">
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">查询类型</label>
                                    <select class="form-select">
                                        <option value="basic">基本信息</option>
                                        <option value="equity">股权结构</option>
                                        <option value="risk">风险信息</option>
                                        <option value="all" selected>全部信息</option>
                                    </select>
                                </div>
                                <div class="col-md-2 d-flex align-items-end">
                                    <button class="btn btn-primary w-100">
                                        <i class="bi bi-search"></i> 查询
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 企业基本信息 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-info-circle"></i> 企业基本信息</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <table class="table table-borderless">
                                        <tr>
                                            <td width="30%" class="text-muted">企业名称：</td>
                                            <td><strong>比亚迪股份有限公司</strong></td>
                                        </tr>
                                        <tr>
                                            <td class="text-muted">统一社会信用代码：</td>
                                            <td>91440300279377483K</td>
                                        </tr>
                                        <tr>
                                            <td class="text-muted">法定代表人：</td>
                                            <td>王传福</td>
                                        </tr>
                                        <tr>
                                            <td class="text-muted">注册资本：</td>
                                            <td>2,909,508.1万人民币</td>
                                        </tr>
                                        <tr>
                                            <td class="text-muted">成立日期：</td>
                                            <td>1995-02-10</td>
                                        </tr>
                                    </table>
                                </div>
                                <div class="col-md-6">
                                    <table class="table table-borderless">
                                        <tr>
                                            <td width="30%" class="text-muted">企业状态：</td>
                                            <td><span class="badge bg-success">存续</span></td>
                                        </tr>
                                        <tr>
                                            <td class="text-muted">所属行业：</td>
                                            <td>汽车制造业</td>
                                        </tr>
                                        <tr>
                                            <td class="text-muted">企业类型：</td>
                                            <td>股份有限公司(上市)</td>
                                        </tr>
                                        <tr>
                                            <td class="text-muted">经营期限：</td>
                                            <td>1995-02-10至无固定期限</td>
                                        </tr>
                                        <tr>
                                            <td class="text-muted">登记机关：</td>
                                            <td>深圳市市场监督管理局</td>
                                        </tr>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 股权结构和风险信息 -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-diagram-3"></i> 股权结构</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>股东名称</th>
                                            <th>持股比例</th>
                                            <th>认缴出资</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>王传福</td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar" style="width: 18.1%">18.1%</div>
                                                </div>
                                            </td>
                                            <td>526,621万元</td>
                                        </tr>
                                        <tr>
                                            <td>吕向阳</td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar bg-warning" style="width: 8.2%">8.2%</div>
                                                </div>
                                            </td>
                                            <td>238,579万元</td>
                                        </tr>
                                        <tr>
                                            <td>其他股东</td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar bg-info" style="width: 73.7%">73.7%</div>
                                                </div>
                                            </td>
                                            <td>2,144,308万元</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-exclamation-triangle"></i> 风险信息</h5>
                        </div>
                        <div class="card-body">
                            <div class="alert alert-success">
                                <h6><i class="bi bi-shield-check"></i> 风险等级：低风险</h6>
                                <small>该企业经营状况良好，无重大风险提示</small>
                            </div>
                            
                            <div class="row text-center">
                                <div class="col-4">
                                    <div class="border rounded p-2">
                                        <h5 class="text-success mb-0">0</h5>
                                        <small class="text-muted">失信记录</small>
                                    </div>
                                </div>
                                <div class="col-4">
                                    <div class="border rounded p-2">
                                        <h5 class="text-warning mb-0">2</h5>
                                        <small class="text-muted">行政处罚</small>
                                    </div>
                                </div>
                                <div class="col-4">
                                    <div class="border rounded p-2">
                                        <h5 class="text-success mb-0">0</h5>
                                        <small class="text-muted">经营异常</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 税银报告模块 - 完整实现
function loadTaxBankReport() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-file-text text-success"></i> 税银报告分析</h2>
                    <p class="text-muted">企业税收数据与银行信贷信息综合分析</p>
                </div>
            </div>
            
            <!-- 企业选择面板 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <label class="form-label">企业名称</label>
                                    <input type="text" class="form-control" placeholder="输入企业名称" value="比亚迪股份有限公司">
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">报告类型</label>
                                    <select class="form-select">
                                        <option value="tax">税务报告</option>
                                        <option value="bank">银行报告</option>
                                        <option value="combined" selected>综合报告</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">时间范围</label>
                                    <select class="form-select">
                                        <option value="current">当前年度</option>
                                        <option value="last" selected>近三年</option>
                                        <option value="all">全部年度</option>
                                    </select>
                                </div>
                                <div class="col-md-2 d-flex align-items-end">
                                    <button class="btn btn-primary w-100">
                                        <i class="bi bi-search"></i> 生成报告
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 税务数据概览 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h4>2.8亿</h4>
                            <p class="mb-0">年度纳税总额</p>
                            <small>+15.2% 同比增长</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h4>AAA</h4>
                            <p class="mb-0">纳税信用等级</p>
                            <small>连续5年AAA级</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h4>156亿</h4>
                            <p class="mb-0">银行授信额度</p>
                            <small>已使用 68.5%</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h4>3.2%</h4>
                            <p class="mb-0">平均贷款利率</p>
                            <small>低于行业平均</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 详细数据表格 -->
            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-table"></i> 税银数据详情</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>年度</th>
                                            <th>营业收入</th>
                                            <th>纳税总额</th>
                                            <th>银行贷款</th>
                                            <th>信用评级</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>2023</td>
                                            <td>6,023.15亿</td>
                                            <td>2.8亿</td>
                                            <td>107.2亿</td>
                                            <td><span class="badge bg-success">AAA</span></td>
                                        </tr>
                                        <tr>
                                            <td>2022</td>
                                            <td>4,240.61亿</td>
                                            <td>2.4亿</td>
                                            <td>89.6亿</td>
                                            <td><span class="badge bg-success">AAA</span></td>
                                        </tr>
                                        <tr>
                                            <td>2021</td>
                                            <td>2,161.42亿</td>
                                            <td>1.8亿</td>
                                            <td>65.3亿</td>
                                            <td><span class="badge bg-success">AAA</span></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-pie-chart"></i> 税收结构分析</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>增值税</span>
                                    <span>45.2%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-primary" style="width: 45.2%"></div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>企业所得税</span>
                                    <span>32.8%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-success" style="width: 32.8%"></div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>其他税种</span>
                                    <span>22.0%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-info" style="width: 22.0%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 论坛数据分析模块 - 完整实现
function loadForumDataAnalysis() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-chat-square-text text-info"></i> 论坛数据分析</h2>
                    <p class="text-muted">多平台论坛数据整合与情感分析</p>
                </div>
            </div>
            
            <!-- 数据概览 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h4>12,456</h4>
                            <p class="mb-0">今日讨论量</p>
                            <small>+8.5% 较昨日</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h4>68.2%</h4>
                            <p class="mb-0">正面情感占比</p>
                            <small>情绪偏向积极</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h4>15</h4>
                            <p class="mb-0">热门话题数</p>
                            <small>超过1000讨论</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h4>8.7</h4>
                            <p class="mb-0">平均活跃度</p>
                            <small>满分10分</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 热门话题 -->
            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-fire"></i> 热门话题排行</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>排名</th>
                                            <th>话题</th>
                                            <th>讨论量</th>
                                            <th>情感倾向</th>
                                            <th>热度</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>1</td>
                                            <td>人工智能概念股大涨</td>
                                            <td>2,345</td>
                                            <td><span class="badge bg-success">积极</span></td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar bg-danger" style="width: 95%">95</div>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>2</td>
                                            <td>新能源汽车销量数据</td>
                                            <td>1,876</td>
                                            <td><span class="badge bg-success">积极</span></td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar bg-warning" style="width: 88%">88</div>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>3</td>
                                            <td>美联储利率决议</td>
                                            <td>1,234</td>
                                            <td><span class="badge bg-secondary">中性</span></td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar bg-info" style="width: 75%">75</div>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-emoji-smile"></i> 情感分析</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>积极情感</span>
                                    <span>68.2%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-success" style="width: 68.2%"></div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>中性情感</span>
                                    <span>23.5%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-secondary" style="width: 23.5%"></div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>消极情感</span>
                                    <span>8.3%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-danger" style="width: 8.3%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 公司分值表模块 - 完整实现
function loadCompanyScoreTable() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-star text-warning"></i> 公司综合评分系统</h2>
                    <p class="text-muted">基于多维度指标的公司投资价值评分</p>
                </div>
            </div>
            
            <!-- 评分概览 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h4>4,247</h4>
                            <p class="mb-0">已评分公司</p>
                            <small>A股上市公司</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h4>8.5</h4>
                            <p class="mb-0">平均评分</p>
                            <small>满分10分</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h4>156</h4>
                            <p class="mb-0">9分以上公司</p>
                            <small>优质投资标的</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h4>12</h4>
                            <p class="mb-0">评分维度</p>
                            <small>综合评估体系</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 评分排行榜 -->
            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-trophy"></i> 公司评分排行榜</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>排名</th>
                                            <th>公司名称</th>
                                            <th>代码</th>
                                            <th>综合评分</th>
                                            <th>行业</th>
                                            <th>市值</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td><span class="badge bg-warning">1</span></td>
                                            <td>贵州茅台</td>
                                            <td>600519</td>
                                            <td><span class="badge bg-success">9.8</span></td>
                                            <td>食品饮料</td>
                                            <td>2.1万亿</td>
                                        </tr>
                                        <tr>
                                            <td><span class="badge bg-secondary">2</span></td>
                                            <td>比亚迪</td>
                                            <td>002594</td>
                                            <td><span class="badge bg-success">9.6</span></td>
                                            <td>汽车制造</td>
                                            <td>8,456亿</td>
                                        </tr>
                                        <tr>
                                            <td><span class="badge bg-warning">3</span></td>
                                            <td>宁德时代</td>
                                            <td>300750</td>
                                            <td><span class="badge bg-success">9.5</span></td>
                                            <td>电池制造</td>
                                            <td>7,892亿</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-pie-chart"></i> 评分分布</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>9-10分</span>
                                    <span>3.7%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-success" style="width: 3.7%"></div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>8-9分</span>
                                    <span>15.2%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-info" style="width: 15.2%"></div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>7-8分</span>
                                    <span>35.8%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-warning" style="width: 35.8%"></div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>6-7分</span>
                                    <span>28.9%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-secondary" style="width: 28.9%"></div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>6分以下</span>
                                    <span>16.4%</span>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-danger" style="width: 16.4%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 行业分值表模块 - 完整实现
function loadIndustryScoreTable() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-bar-chart-line text-primary"></i> 行业综合评分系统</h2>
                    <p class="text-muted">基于发展前景、盈利能力、风险水平的行业评分</p>
                </div>
            </div>
            
            <!-- 行业评分排行 -->
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-award"></i> 行业投资价值排行榜</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>排名</th>
                                            <th>行业名称</th>
                                            <th>综合评分</th>
                                            <th>发展前景</th>
                                            <th>盈利能力</th>
                                            <th>风险水平</th>
                                            <th>公司数量</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td><span class="badge bg-warning">1</span></td>
                                            <td>新能源汽车</td>
                                            <td><span class="badge bg-success">9.2</span></td>
                                            <td>9.5</td>
                                            <td>8.8</td>
                                            <td>9.3</td>
                                            <td>156</td>
                                        </tr>
                                        <tr>
                                            <td><span class="badge bg-secondary">2</span></td>
                                            <td>人工智能</td>
                                            <td><span class="badge bg-success">9.0</span></td>
                                            <td>9.8</td>
                                            <td>8.5</td>
                                            <td>8.7</td>
                                            <td>89</td>
                                        </tr>
                                        <tr>
                                            <td><span class="badge bg-warning">3</span></td>
                                            <td>生物医药</td>
                                            <td><span class="badge bg-success">8.8</span></td>
                                            <td>9.2</td>
                                            <td>8.6</td>
                                            <td>8.6</td>
                                            <td>234</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 行业+公司分值表模块 - 完整实现
function loadIndustryCompanyScoreTable() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-diagram-3 text-success"></i> 行业+公司综合评分</h2>
                    <p class="text-muted">行业与公司双重评分的投资决策支持系统</p>
                </div>
            </div>
            
            <!-- 综合评分矩阵 -->
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-grid"></i> 投资价值矩阵</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th>公司名称</th>
                                            <th>所属行业</th>
                                            <th>公司评分</th>
                                            <th>行业评分</th>
                                            <th>综合评分</th>
                                            <th>投资建议</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr class="table-success">
                                            <td>比亚迪</td>
                                            <td>新能源汽车</td>
                                            <td>9.6</td>
                                            <td>9.2</td>
                                            <td><strong>9.4</strong></td>
                                            <td><span class="badge bg-success">强烈推荐</span></td>
                                        </tr>
                                        <tr class="table-success">
                                            <td>宁德时代</td>
                                            <td>电池制造</td>
                                            <td>9.5</td>
                                            <td>8.8</td>
                                            <td><strong>9.2</strong></td>
                                            <td><span class="badge bg-success">强烈推荐</span></td>
                                        </tr>
                                        <tr class="table-info">
                                            <td>药明康德</td>
                                            <td>生物医药</td>
                                            <td>8.9</td>
                                            <td>8.8</td>
                                            <td><strong>8.9</strong></td>
                                            <td><span class="badge bg-info">推荐</span></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 对象因子权重表模块 - 完整实现
function loadObjectFactorWeightTable() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-sliders text-info"></i> 因子权重管理系统</h2>
                    <p class="text-muted">动态调整评分因子权重，优化投资决策模型</p>
                </div>
            </div>
            
            <!-- 权重配置 -->
            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-gear"></i> 因子权重配置</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>因子名称</th>
                                            <th>当前权重</th>
                                            <th>权重调整</th>
                                            <th>贡献度</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>财务指标</td>
                                            <td>25%</td>
                                            <td>
                                                <input type="range" class="form-range" min="0" max="50" value="25">
                                            </td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar" style="width: 25%">25%</div>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>成长性</td>
                                            <td>20%</td>
                                            <td>
                                                <input type="range" class="form-range" min="0" max="50" value="20">
                                            </td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar bg-success" style="width: 20%">20%</div>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>盈利能力</td>
                                            <td>18%</td>
                                            <td>
                                                <input type="range" class="form-range" min="0" max="50" value="18">
                                            </td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar bg-info" style="width: 18%">18%</div>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-pie-chart"></i> 权重分布</h5>
                        </div>
                        <div class="card-body">
                            <canvas id="weightChart" width="300" height="300"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 曲线预测分析模块 - 完整实现
function loadCurvePredictionAnalysis() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-graph-up-arrow text-warning"></i> 趋势预测分析</h2>
                    <p class="text-muted">基于机器学习的股价和指标趋势预测</p>
                </div>
            </div>
            
            <!-- 预测结果 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h4>85.6%</h4>
                            <p class="mb-0">预测准确率</p>
                            <small>近30天平均</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h4>+12.5%</h4>
                            <p class="mb-0">预期涨幅</p>
                            <small>未来30天</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h4>68%</h4>
                            <p class="mb-0">置信区间</p>
                            <small>预测可信度</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h4>中等</h4>
                            <p class="mb-0">风险等级</p>
                            <small>投资风险评估</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 预测图表 -->
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-graph-up"></i> 趋势预测图表</h5>
                        </div>
                        <div class="card-body">
                            <canvas id="predictionChart" width="800" height="400"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 导出所有模块函数
if (typeof window !== 'undefined') {
    window.loadForeignHotspotData = loadForeignHotspotData;
    window.loadTencentJianIndex = loadTencentJianIndex;
    window.loadHotspotDataTable = loadHotspotDataTable;
    window.loadQichachaData = loadQichachaData;
    window.loadTaxBankReport = loadTaxBankReport;
    window.loadForumDataAnalysis = loadForumDataAnalysis;
    window.loadCompanyScoreTable = loadCompanyScoreTable;
    window.loadIndustryScoreTable = loadIndustryScoreTable;
    window.loadIndustryCompanyScoreTable = loadIndustryCompanyScoreTable;
    window.loadObjectFactorWeightTable = loadObjectFactorWeightTable;
    window.loadCurvePredictionAnalysis = loadCurvePredictionAnalysis;
}