// 板块轮动预测模块 - 现代化设计版本
function loadSectorRotationPrediction() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <!-- 页面标题和操作栏 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h2 class="mb-2"><i class="bi bi-arrow-repeat text-primary"></i> 智能板块轮动预测</h2>
                            <p class="text-muted mb-0">基于宏观经济、资金流向和市场情绪的多维度板块轮动分析</p>
                        </div>
                        <div class="btn-group">
                            <button class="btn btn-outline-primary" onclick="refreshSectorData()">
                                <i class="bi bi-arrow-clockwise"></i> 刷新数据
                            </button>
                            <button class="btn btn-outline-success" onclick="exportSectorRotationReport()">
                                <i class="bi bi-download"></i> 导出报告
                            </button>
                            <button class="btn btn-outline-info" onclick="toggleAdvancedView()">
                                <i class="bi bi-gear"></i> 高级视图
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 实时状态指示器 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card border-0 shadow-sm">
                        <div class="card-body p-3">
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="d-flex align-items-center">
                                    <div class="status-indicator status-active me-3"></div>
                                    <div>
                                        <h6 class="mb-0">实时轮动监测</h6>
                                        <small class="text-muted">最后更新: <span id="lastUpdateTime">${new Date().toLocaleString('zh-CN')}</span></small>
                                    </div>
                                </div>
                                <div class="d-flex gap-3">
                                    <div class="text-center">
                                        <div class="fw-bold text-success">↑ 领涨板块</div>
                                        <small class="text-muted" id="leadingUpSectors">资源、能源、基建</small>
                                    </div>
                                    <div class="text-center">
                                        <div class="fw-bold text-danger">↓ 领跌板块</div>
                                        <small class="text-muted" id="leadingDownSectors">科技、机器人、新能源</small>
                                    </div>
                                    <div class="text-center">
                                        <div class="fw-bold text-warning">↔ 震荡板块</div>
                                        <small class="text-muted" id="neutralSectors">金融、消费、医药</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 多时间维度预测 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card shadow-sm">
                        <div class="card-header bg-gradient-info text-white">
                            <h5 class="mb-0"><i class="bi bi-calendar-range"></i> 多时间维度板块轮动预测</h5>
                        </div>
                        <div class="card-body">
                            <!-- 时间维度选择器 -->
                            <div class="mb-4">
                                <div class="btn-group w-100" role="group">
                                    <input type="radio" class="btn-check" name="timeframe" id="timeframe-30d" autocomplete="off" checked onchange="changeTimeframe('30d')">
                                    <label class="btn btn-outline-primary" for="timeframe-30d">30天预测</label>
                                    
                                    <input type="radio" class="btn-check" name="timeframe" id="timeframe-90d" autocomplete="off" onchange="changeTimeframe('90d')">
                                    <label class="btn btn-outline-primary" for="timeframe-90d">90天预测</label>
                                    
                                    <input type="radio" class="btn-check" name="timeframe" id="timeframe-180d" autocomplete="off" onchange="changeTimeframe('180d')">
                                    <label class="btn btn-outline-primary" for="timeframe-180d">180天预测</label>
                                    
                                    <input type="radio" class="btn-check" name="timeframe" id="timeframe-360d" autocomplete="off" onchange="changeTimeframe('360d')">
                                    <label class="btn btn-outline-primary" for="timeframe-360d">360天预测</label>
                                </div>
                            </div>
                            
                            <!-- 预测结果展示 -->
                            <div id="sectorRotationPrediction">
                                <div class="text-center py-4">
                                    <div class="spinner-border text-info" role="status">
                                        <span class="visually-hidden">加载中...</span>
                                    </div>
                                    <p class="mt-3">正在分析板块轮动趋势...</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 多时间维度预测 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card shadow-sm">
                        <div class="card-header bg-gradient-info text-white">
                            <h5 class="mb-0"><i class="bi bi-calendar-range"></i> 多时间维度板块轮动预测</h5>
                        </div>
                        <div class="card-body">
                            <!-- 时间维度选择器 -->
                            <div class="mb-4">
                                <div class="btn-group w-100" role="group">
                                    <input type="radio" class="btn-check" name="timeframe" id="timeframe-30d" autocomplete="off" checked onchange="changeTimeframe('30d')">
                                    <label class="btn btn-outline-primary" for="timeframe-30d">30天预测</label>
                                    
                                    <input type="radio" class="btn-check" name="timeframe" id="timeframe-90d" autocomplete="off" onchange="changeTimeframe('90d')">
                                    <label class="btn btn-outline-primary" for="timeframe-90d">90天预测</label>
                                    
                                    <input type="radio" class="btn-check" name="timeframe" id="timeframe-180d" autocomplete="off" onchange="changeTimeframe('180d')">
                                    <label class="btn btn-outline-primary" for="timeframe-180d">180天预测</label>
                                    
                                    <input type="radio" class="btn-check" name="timeframe" id="timeframe-360d" autocomplete="off" onchange="changeTimeframe('360d')">
                                    <label class="btn btn-outline-primary" for="timeframe-360d">360天预测</label>
                                </div>
                            </div>
                            
                            <!-- 预测结果展示 -->
                            <div class="row">
                                <div class="col-md-8">
                                    <div id="sectorRotationPrediction">
                                        <div class="text-center py-4">
                                            <div class="spinner-border text-info" role="status">
                                                <span class="visually-hidden">加载中...</span>
                                            </div>
                                            <p class="mt-3">正在分析板块轮动趋势...</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card bg-light">
                                        <div class="card-header">
                                            <h6 class="mb-0"><i class="bi bi-info-circle"></i> 预测说明</h6>
                                        </div>
                                        <div class="card-body">
                                            <small class="text-muted">
                                                <p><strong>概率解读：</strong></p>
                                                <ul class="mb-2">
                                                    <li>80%+：高度确定性</li>
                                                    <li>60%-79%：中等确定性</li>
                                                    <li>40%-59%：低确定性</li>
                                                    <li>0%-39%：不确定性高</li>
                                                </ul>
                                                <p><strong>数据来源：</strong></p>
                                                <ul>
                                                    <li>历史轮动规律</li>
                                                    <li>宏观经济指标</li>
                                                    <li>资金流向数据</li>
                                                    <li>市场情绪分析</li>
                                                </ul>
                                            </small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 投资策略和风险控制 -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="card shadow-sm h-100">
                        <div class="card-header bg-gradient-success text-white">
                            <h5 class="mb-0"><i class="bi bi-lightning-charge"></i> 智能投资策略建议</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <label class="form-label">风险偏好选择：</label>
                                <div class="btn-group w-100" role="group">
                                    <input type="radio" class="btn-check" name="riskPreference" id="risk-conservative" autocomplete="off" checked onchange="updateInvestmentStrategy()">
                                    <label class="btn btn-outline-success" for="risk-conservative">保守型</label>
                                    
                                    <input type="radio" class="btn-check" name="riskPreference" id="risk-balanced" autocomplete="off" onchange="updateInvestmentStrategy()">
                                    <label class="btn btn-outline-warning" for="risk-balanced">平衡型</label>
                                    
                                    <input type="radio" class="btn-check" name="riskPreference" id="risk-aggressive" autocomplete="off" onchange="updateInvestmentStrategy()">
                                    <label class="btn btn-outline-danger" for="risk-aggressive">激进型</label>
                                </div>
                            </div>
                            <div id="investmentStrategy">
                                <div class="text-center py-4">
                                    <div class="spinner-border text-warning" role="status">
                                        <span class="visually-hidden">加载中...</span>
                                    </div>
                                    <p class="mt-3">正在生成投资策略...</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card shadow-sm h-100">
                        <div class="card-header bg-gradient-warning text-dark">
                            <h5 class="mb-0"><i class="bi bi-shield-check"></i> 风险控制与监控</h5>
                        </div>
                        <div class="card-body">
                            <div class="risk-indicators">
                                <div class="risk-item mb-3">
                                    <div class="d-flex justify-content-between align-items-center mb-1">
                                        <span class="fw-bold">市场波动风险</span>
                                        <span class="badge bg-success">低风险</span>
                                    </div>
                                    <div class="progress" style="height: 6px;">
                                        <div class="progress-bar bg-success" style="width: 25%"></div>
                                    </div>
                                </div>
                                <div class="risk-item mb-3">
                                    <div class="d-flex justify-content-between align-items-center mb-1">
                                        <span class="fw-bold">板块轮动风险</span>
                                        <span class="badge bg-warning">中风险</span>
                                    </div>
                                    <div class="progress" style="height: 6px;">
                                        <div class="progress-bar bg-warning" style="width: 55%"></div>
                                    </div>
                                </div>
                                <div class="risk-item mb-3">
                                    <div class="d-flex justify-content-between align-items-center mb-1">
                                        <span class="fw-bold">政策变化风险</span>
                                        <span class="badge bg-danger">高风险</span>
                                    </div>
                                    <div class="progress" style="height: 6px;">
                                        <div class="progress-bar bg-danger" style="width: 75%"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="alert alert-info mt-3">
                                <small>
                                    <i class="bi bi-info-circle"></i>
                                    <strong>风险提示：</strong> 当前市场处于快速轮动阶段，建议密切关注政策变化和资金流向。
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 板块轮动历史分析 -->
            <div class="row">
                <div class="col-12">
                    <div class="card shadow-sm">
                        <div class="card-header bg-gradient-dark text-white">
                            <h5 class="mb-0"><i class="bi bi-clock-history"></i> 板块轮动历史分析</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <div class="input-group">
                                    <span class="input-group-text"><i class="bi bi-search"></i></span>
                                    <input type="text" class="form-control" placeholder="搜索板块或时间段..." id="historySearch" onkeyup="filterHistoryTable()">
                                    <button class="btn btn-outline-secondary" type="button" onclick="clearHistorySearch()">清除</button>
                                </div>
                            </div>
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead class="table-light">
                                        <tr>
                                            <th>时间段 <i class="bi bi-sort-alpha-down" onclick="sortHistoryTable('period')"></i></th>
                                            <th>领涨板块 <i class="bi bi-sort-numeric-down" onclick="sortHistoryTable('upChange')"></i></th>
                                            <th>涨幅</th>
                                            <th>领跌板块 <i class="bi bi-sort-numeric-down" onclick="sortHistoryTable('downChange')"></i></th>
                                            <th>跌幅</th>
                                            <th>轮动原因</th>
                                            <th>操作</th>
                                        </tr>
                                    </thead>
                                    <tbody id="sectorRotationHistory">
                                        <tr>
                                            <td colspan="7" class="text-center py-4">
                                                <div class="spinner-border text-primary" role="status">
                                                    <span class="visually-hidden">加载中...</span>
                                                </div>
                                                <p class="mt-2">正在加载历史数据...</p>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <small class="text-muted">共 <span id="historyCount">0</span> 条记录</small>
                                <div class="btn-group">
                                    <button class="btn btn-sm btn-outline-primary" onclick="exportHistoryData()">
                                        <i class="bi bi-download"></i> 导出数据
                                    </button>
                                    <button class="btn btn-sm btn-outline-secondary" onclick="loadSectorRotationHistory()">
                                        <i class="bi bi-arrow-clockwise"></i> 刷新
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 初始化板块轮动分析
    setTimeout(() => {
        generateSectorRotationHeatmap();
        generateSectorRotationPrediction();
        generateInvestmentStrategy();
        loadSectorRotationHistory();
    }, 1000);
}

// 生成板块轮动热力图
function generateSectorRotationHeatmap() {
    const heatmapDiv = document.getElementById('sectorRotationHeatmap');
    
    // 板块轮动数据
    const sectors = [
        { name: '资源能源', current: 85, trend: '上涨', momentum: '强' },
        { name: '金融银行', current: 65, trend: '震荡', momentum: '中' },
        { name: '科技成长', current: 35, trend: '下跌', momentum: '弱' },
        { name: '消费医药', current: 55, trend: '震荡', momentum: '中' },
        { name: '基建制造', current: 70, trend: '上涨', momentum: '强' },
        { name: '新能源', current: 45, trend: '下跌', momentum: '弱' },
        { name: '传媒娱乐', current: 60, trend: '震荡', momentum: '中' },
        { name: '国防军工', current: 75, trend: '上涨', momentum: '强' }
    ];
    
    let heatmapHTML = `
        <div class="sector-heatmap">
            <div class="row">
    `;
    
    sectors.forEach(sector => {
        const intensity = sector.current;
        let colorClass = '';
        if (intensity >= 70) colorClass = 'bg-success';
        else if (intensity >= 50) colorClass = 'bg-warning';
        else colorClass = 'bg-danger';
        
        let trendIcon = '';
        if (sector.trend === '上涨') trendIcon = '↑';
        else if (sector.trend === '下跌') trendIcon = '↓';
        else trendIcon = '↔';
        
        heatmapHTML += `
            <div class="col-md-3 mb-3">
                <div class="card sector-card ${colorClass} text-white">
                    <div class="card-body text-center">
                        <h6 class="card-title">${sector.name}</h6>
                        <div class="display-4 fw-bold">${intensity}%</div>
                        <div class="mt-2">
                            <span class="badge bg-light text-dark">${trendIcon} ${sector.trend}</span>
                            <span class="badge bg-info">${sector.momentum}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    heatmapHTML += `
            </div>
            <div class="mt-3">
                <div class="legend d-flex justify-content-center">
                    <span class="badge bg-success me-2">强势板块 (70-100%)</span>
                    <span class="badge bg-warning me-2">中性板块 (50-69%)</span>
                    <span class="badge bg-danger">弱势板块 (0-49%)</span>
                </div>
            </div>
        </div>
    `;
    
    heatmapDiv.innerHTML = heatmapHTML;
}

// 生成板块轮动预测（多时间维度）
function generateSectorRotationPrediction(timeframe = '30d') {
    const predictionDiv = document.getElementById('sectorRotationPrediction');
    
    // 根据时间维度生成不同的预测数据
    const predictionsByTimeframe = {
        '30d': [
            { sector: '资源能源', probability: 85, trend: '继续上涨', reason: '大宗商品价格支撑', momentum: '强' },
            { sector: '基建制造', probability: 78, trend: '稳步上涨', reason: '政策利好推动', momentum: '强' },
            { sector: '国防军工', probability: 72, trend: '震荡上行', reason: '地缘政治因素', momentum: '中' },
            { sector: '金融银行', probability: 65, trend: '区间震荡', reason: '估值修复完成', momentum: '中' },
            { sector: '消费医药', probability: 58, trend: '温和反弹', reason: '消费复苏预期', momentum: '弱' },
            { sector: '科技成长', probability: 42, trend: '继续调整', reason: '估值压力较大', momentum: '弱' },
            { sector: '新能源', probability: 38, trend: '弱势震荡', reason: '产能过剩担忧', momentum: '弱' },
            { sector: '传媒娱乐', probability: 55, trend: '底部企稳', reason: '行业整顿结束', momentum: '中' }
        ],
        '90d': [
            { sector: '资源能源', probability: 82, trend: '高位震荡', reason: '价格回调压力', momentum: '中' },
            { sector: '基建制造', probability: 75, trend: '持续上涨', reason: '基建投资加速', momentum: '强' },
            { sector: '国防军工', probability: 68, trend: '稳步上行', reason: '国防预算增加', momentum: '中' },
            { sector: '金融银行', probability: 62, trend: '温和上涨', reason: '利率政策预期', momentum: '中' },
            { sector: '消费医药', probability: 65, trend: '明显反弹', reason: '消费旺季到来', momentum: '强' },
            { sector: '科技成长', probability: 48, trend: '底部反弹', reason: '估值修复机会', momentum: '中' },
            { sector: '新能源', probability: 45, trend: '企稳回升', reason: '政策扶持加码', momentum: '中' },
            { sector: '传媒娱乐', probability: 58, trend: '震荡上行', reason: '内容监管放松', momentum: '中' }
        ],
        '180d': [
            { sector: '资源能源', probability: 75, trend: '震荡调整', reason: '供需平衡变化', momentum: '中' },
            { sector: '基建制造', probability: 70, trend: '稳定增长', reason: '长期政策支持', momentum: '中' },
            { sector: '国防军工', probability: 65, trend: '持续向好', reason: '战略需求稳定', momentum: '中' },
            { sector: '金融银行', probability: 68, trend: '稳步上涨', reason: '经济复苏预期', momentum: '强' },
            { sector: '消费医药', probability: 72, trend: '强势反弹', reason: '消费升级趋势', momentum: '强' },
            { sector: '科技成长', probability: 55, trend: '触底反弹', reason: '新技术突破', momentum: '中' },
            { sector: '新能源', probability: 52, trend: '逐步回暖', reason: '技术成本下降', momentum: '中' },
            { sector: '传媒娱乐', probability: 62, trend: '持续改善', reason: '数字化转型加速', momentum: '中' }
        ],
        '360d': [
            { sector: '资源能源', probability: 65, trend: '周期波动', reason: '全球经济周期', momentum: '弱' },
            { sector: '基建制造', probability: 72, trend: '长期向好', reason: '新基建投资', momentum: '中' },
            { sector: '国防军工', probability: 70, trend: '稳定增长', reason: '国家安全需求', momentum: '中' },
            { sector: '金融银行', probability: 75, trend: '价值回归', reason: '金融改革深化', momentum: '强' },
            { sector: '消费医药', probability: 78, trend: '持续增长', reason: '人口结构变化', momentum: '强' },
            { sector: '科技成长', probability: 68, trend: '重新崛起', reason: '创新驱动发展', momentum: '强' },
            { sector: '新能源', probability: 65, trend: '长期向好', reason: '碳中和目标', momentum: '中' },
            { sector: '传媒娱乐', probability: 70, trend: '数字化转型', reason: '技术融合发展', momentum: '中' }
        ]
    };
    
    const predictions = predictionsByTimeframe[timeframe] || predictionsByTimeframe['30d'];
    const timeframeLabels = {
        '30d': '未来30天',
        '90d': '未来90天', 
        '180d': '未来180天',
        '360d': '未来360天'
    };
    
    let predictionHTML = `
        <div class="prediction-container">
            <div class="alert alert-info mb-3">
                <i class="bi bi-info-circle"></i>
                <strong>${timeframeLabels[timeframe]}板块轮动预测</strong> - 基于历史规律和当前市场环境分析
            </div>
            
            <!-- 预测数据表格 -->
            <div class="table-responsive">
                <table class="table table-hover table-bordered">
                    <thead class="table-primary">
                        <tr>
                            <th width="15%">板块名称</th>
                            <th width="10%">预测概率</th>
                            <th width="15%">趋势方向</th>
                            <th width="40%">原因分析</th>
                            <th width="10%">动量强度</th>
                            <th width="10%">操作</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    predictions.forEach(pred => {
        let probabilityClass = '';
        let trendIcon = '';
        let momentumBadge = '';
        
        if (pred.probability >= 70) probabilityClass = 'table-success';
        else if (pred.probability >= 50) probabilityClass = 'table-warning';
        else probabilityClass = 'table-danger';
        
        if (pred.trend.includes('上涨')) trendIcon = '📈';
        else if (pred.trend.includes('下跌') || pred.trend.includes('调整')) trendIcon = '📉';
        else trendIcon = '↔';
        
        if (pred.momentum === '强') momentumBadge = 'badge bg-success';
        else if (pred.momentum === '中') momentumBadge = 'badge bg-warning';
        else momentumBadge = 'badge bg-danger';
        
        predictionHTML += `
                        <tr class="${probabilityClass}">
                            <td><strong>${pred.sector}</strong></td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar ${probabilityClass.replace('table-', 'bg-')}" 
                                         style="width: ${pred.probability}%">
                                        ${pred.probability}%
                                    </div>
                                </div>
                            </td>
                            <td>
                                <span class="trend-indicator">${trendIcon}</span>
                                ${pred.trend}
                            </td>
                            <td><small class="text-muted">${pred.reason}</small></td>
                            <td><span class="${momentumBadge}">${pred.momentum}</span></td>
                            <td>
                                <button class="btn btn-sm btn-outline-primary" onclick="viewSectorDetails('${pred.sector}')">
                                    <i class="bi bi-eye"></i>
                                </button>
                            </td>
                        </tr>
        `;
    });
    
    predictionHTML += `
                    </tbody>
                </table>
            </div>
            
            <!-- 统计摘要 -->
            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h6 class="card-title">强势板块</h6>
                            <div class="display-6 text-success">${predictions.filter(p => p.probability >= 70).length}</div>
                            <small class="text-muted">概率≥70%</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h6 class="card-title">中性板块</h6>
                            <div class="display-6 text-warning">${predictions.filter(p => p.probability >= 50 && p.probability < 70).length}</div>
                            <small class="text-muted">概率50-69%</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h6 class="card-title">弱势板块</h6>
                            <div class="display-6 text-danger">${predictions.filter(p => p.probability < 50).length}</div>
                            <small class="text-muted">概率<50%</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-3 text-center">
                <small class="text-muted">
                    <i class="bi bi-lightbulb"></i>
                    预测概率基于历史数据、市场情绪和宏观经济指标综合分析
                </small>
            </div>
        </div>
    `;
    
    predictionDiv.innerHTML = predictionHTML;
}

// 查看板块详情
function viewSectorDetails(sectorName) {
    alert(`查看 ${sectorName} 板块详情

详细分析报告正在生成中...`);
}

// 生成投资策略建议（基于风险偏好）
function generateInvestmentStrategy(riskPreference = 'risk-balanced') {
    const strategyDiv = document.getElementById('investmentStrategy');
    
    const strategies = {
        'risk-conservative': {
            level: '保守型',
            allocation: {
                '金融银行': 30,
                '消费医药': 30,
                '资源能源': 15,
                '基建制造': 10,
                '现金': 15
            },
            rationale: '防御为主，稳健增长，等待市场机会',
            risk: '低风险低收益',
            timeframe: '6-12个月',
            expectedReturn: '5-8%',
            maxDrawdown: '-8%以内',
            suitableFor: '风险承受能力较低，追求稳定收益的投资者'
        },
        'risk-balanced': {
            level: '平衡型',
            allocation: {
                '资源能源': 25,
                '基建制造': 20,
                '金融银行': 20,
                '消费医药': 20,
                '现金': 15
            },
            rationale: '均衡配置，攻守兼备，把握轮动机会',
            risk: '中等风险中等收益',
            timeframe: '3-6个月',
            expectedReturn: '8-15%',
            maxDrawdown: '-15%以内',
            suitableFor: '风险承受能力中等，追求平衡收益的投资者'
        },
        'risk-aggressive': {
            level: '激进型',
            allocation: {
                '资源能源': 40,
                '基建制造': 30,
                '国防军工': 20,
                '现金': 10
            },
            rationale: '紧跟强势板块，追求高收益，把握市场热点',
            risk: '高风险高收益',
            timeframe: '1-3个月',
            expectedReturn: '15-25%',
            maxDrawdown: '-25%以内',
            suitableFor: '风险承受能力较强，追求高收益的投资者'
        }
    };
    
    const strategy = strategies[riskPreference] || strategies['risk-balanced'];
    
    let strategyHTML = `
        <div class="strategy-detail">
            <div class="alert alert-${riskPreference === 'risk-conservative' ? 'success' : riskPreference === 'risk-balanced' ? 'warning' : 'danger'} mb-3">
                <div class="d-flex justify-content-between align-items-center">
                    <h6 class="mb-0"><i class="bi bi-${riskPreference === 'risk-conservative' ? 'shield-check' : riskPreference === 'risk-balanced' ? 'scale' : 'lightning'}"></i> ${strategy.level}投资策略</h6>
                    <span class="badge bg-${riskPreference === 'risk-conservative' ? 'success' : riskPreference === 'risk-balanced' ? 'warning' : 'danger'}">${strategy.risk}</span>
                </div>
            </div>
            
            <!-- 资产配置饼图 -->
            <div class="mb-4">
                <h6 class="mb-3"><i class="bi bi-pie-chart"></i> 资产配置比例</h6>
                <div class="allocation-chart">
                    ${Object.entries(strategy.allocation).map(([sector, percent]) => `
                        <div class="allocation-item mb-2">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="sector-name">${sector}</span>
                                <div class="d-flex align-items-center">
                                    <div class="progress me-2" style="width: 120px; height: 8px;">
                                        <div class="progress-bar bg-primary" style="width: ${percent}%"></div>
                                    </div>
                                    <span class="fw-bold">${percent}%</span>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <!-- 策略详情 -->
            <div class="row">
                <div class="col-md-6">
                    <div class="card bg-light mb-3">
                        <div class="card-body">
                            <h6 class="card-title"><i class="bi bi-graph-up"></i> 策略指标</h6>
                            <div class="mb-2">
                                <small class="text-muted">预期收益率:</small>
                                <div class="fw-bold text-success">${strategy.expectedReturn}</div>
                            </div>
                            <div class="mb-2">
                                <small class="text-muted">最大回撤:</small>
                                <div class="fw-bold text-danger">${strategy.maxDrawdown}</div>
                            </div>
                            <div class="mb-2">
                                <small class="text-muted">建议持有期:</small>
                                <div class="fw-bold">${strategy.timeframe}</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card bg-light mb-3">
                        <div class="card-body">
                            <h6 class="card-title"><i class="bi bi-person-check"></i> 适用人群</h6>
                            <p class="small mb-0">${strategy.suitableFor}</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 投资逻辑 -->
            <div class="mb-3">
                <h6><i class="bi bi-lightbulb"></i> 投资逻辑</h6>
                <p class="small mb-0">${strategy.rationale}</p>
            </div>
            
            <!-- 操作按钮 -->
            <div class="d-flex gap-2">
                <button class="btn btn-primary btn-sm" onclick="applyStrategy('${strategy.level}')">
                    <i class="bi bi-check-circle"></i> 应用此策略
                </button>
                <button class="btn btn-outline-secondary btn-sm" onclick="simulateStrategy('${riskPreference}')">
                    <i class="bi bi-calculator"></i> 策略回测
                </button>
                <button class="btn btn-outline-info btn-sm" onclick="exportStrategy('${riskPreference}')">
                    <i class="bi bi-download"></i> 导出策略
                </button>
            </div>
        </div>
    `;
    
    strategyDiv.innerHTML = strategyHTML;
}

// 加载板块轮动历史
function loadSectorRotationHistory() {
    const historyTable = document.getElementById('sectorRotationHistory');
    
    const historyData = [
        {
            period: '2025年9月',
            leadingUp: '资源能源',
            upChange: '+15.2%',
            leadingDown: '科技成长',
            downChange: '-8.7%',
            reason: '大宗商品涨价，科技股估值回调'
        },
        {
            period: '2025年8月', 
            leadingUp: '基建制造',
            upChange: '+12.8%',
            leadingDown: '新能源',
            downChange: '-6.3%',
            reason: '基建投资加速，新能源产能过剩'
        },
        {
            period: '2025年7月',
            leadingUp: '国防军工',
            upChange: '+9.5%',
            leadingDown: '传媒娱乐',
            downChange: '-4.2%',
            reason: '地缘紧张局势，传媒监管加强'
        },
        {
            period: '2025年6月',
            leadingUp: '金融银行',
            upChange: '+7.3%',
            leadingDown: '消费医药',
            downChange: '-3.8%',
            reason: '利率政策预期，消费数据疲软'
        },
        {
            period: '2025年5月',
            leadingUp: '科技成长',
            upChange: '+18.6%',
            leadingDown: '资源能源',
            downChange: '-5.1%',
            reason: 'AI概念炒作，大宗商品调整'
        }
    ];
    
    let historyHTML = '';
    
    historyData.forEach(record => {
        historyHTML += `
            <tr>
                <td><strong>${record.period}</strong></td>
                <td><span class="badge bg-success">${record.leadingUp}</span></td>
                <td><span class="text-success">${record.upChange}</span></td>
                <td><span class="badge bg-danger">${record.leadingDown}</span></td>
                <td><span class="text-danger">${record.downChange}</span></td>
                <td><small class="text-muted">${record.reason}</small></td>
            </tr>
        `;
    });
    
    historyTable.innerHTML = historyHTML;
}

// 应用投资策略
function applyStrategy(strategyLevel) {
    alert(`已应用 ${strategyLevel} 投资策略！\n\n策略详情已保存，可在投资组合管理中查看具体配置建议。`);
    
    // 在实际应用中，这里会调用后端API保存策略配置
    console.log(`应用投资策略: ${strategyLevel}`);
}

// 交互功能函数
let currentTimeframe = '30d';
let currentHeatmapView = 'grid';
let autoRefreshInterval = null;

// 切换时间维度
function changeTimeframe(timeframe) {
    currentTimeframe = timeframe;
    console.log(`切换到时间维度: ${timeframe}`);
    generateSectorRotationPrediction(timeframe);
}

// 切换热力图视图
function toggleHeatmapView(view) {
    currentHeatmapView = view;
    console.log(`切换到热力图视图: ${view}`);
    generateSectorRotationHeatmap();
}

// 更新热力图显示
function updateHeatmapDisplay() {
    generateSectorRotationHeatmap();
}

// 切换自动刷新
function toggleAutoRefresh() {
    const autoRefreshCheckbox = document.getElementById('autoRefresh');
    if (autoRefreshCheckbox.checked) {
        autoRefreshInterval = setInterval(() => {
            refreshSectorData();
        }, 30000); // 30秒刷新一次
        console.log('开启自动刷新');
    } else {
        if (autoRefreshInterval) {
            clearInterval(autoRefreshInterval);
            autoRefreshInterval = null;
        }
        console.log('关闭自动刷新');
    }
}

// 刷新板块数据
function refreshSectorData() {
    console.log('刷新板块数据...');
    document.getElementById('lastUpdateTime').textContent = new Date().toLocaleString('zh-CN');
    generateSectorRotationHeatmap();
    generateSectorRotationPrediction(currentTimeframe);
    updateInvestmentStrategy();
    loadSectorRotationHistory();
}

// 切换高级视图
function toggleAdvancedView() {
    const advancedSections = document.querySelectorAll('.advanced-section');
    advancedSections.forEach(section => {
        if (section.style.display === 'none') {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    });
    console.log('切换高级视图');
}

// 更新投资策略
function updateInvestmentStrategy() {
    const riskPreference = document.querySelector('input[name="riskPreference"]:checked').id;
    generateInvestmentStrategy(riskPreference);
}

// 历史数据搜索和排序功能
let currentHistoryData = [];
let currentSortField = 'period';
let currentSortOrder = 'desc';

// 过滤历史表格
function filterHistoryTable() {
    const searchTerm = document.getElementById('historySearch').value.toLowerCase();
    const rows = document.querySelectorAll('#sectorRotationHistory tr');
    let visibleCount = 0;
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    document.getElementById('historyCount').textContent = visibleCount;
}

// 清除搜索
function clearHistorySearch() {
    document.getElementById('historySearch').value = '';
    filterHistoryTable();
}

// 排序历史表格
function sortHistoryTable(field) {
    if (currentSortField === field) {
        currentSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';
    } else {
        currentSortField = field;
        currentSortOrder = 'asc';
    }
    
    loadSectorRotationHistory(); // 重新加载时会自动排序
}

// 导出历史数据
function exportHistoryData() {
    alert(`历史数据导出功能正在开发中...

导出内容将包括：
- 板块轮动历史记录
- 涨跌幅数据
- 轮动原因分析
- 时间序列数据`);
}

// 策略模拟功能
function simulateStrategy(riskPreference) {
    const strategies = {
        'risk-conservative': { name: '保守型', return: '8.2%', maxDrawdown: '-6.5%' },
        'risk-balanced': { name: '平衡型', return: '15.7%', maxDrawdown: '-12.3%' },
        'risk-aggressive': { name: '激进型', return: '23.4%', maxDrawdown: '-18.9%' }
    };
    
    const strategy = strategies[riskPreference] || strategies['risk-balanced'];
    
    alert(`策略回测结果 - ${strategy.name}策略

📊 历史回测表现（过去12个月）：
• 年化收益率：${strategy.return}
• 最大回撤：${strategy.maxDrawdown}
• 夏普比率：1.8
• 胜率：72%

💡 回测说明：基于历史数据模拟，实际表现可能有所不同`);
}

// 导出策略
function exportStrategy(riskPreference) {
    const strategies = {
        'risk-conservative': '保守型投资策略',
        'risk-balanced': '平衡型投资策略', 
        'risk-aggressive': '激进型投资策略'
    };
    
    const strategyName = strategies[riskPreference] || '平衡型投资策略';
    
    alert(`正在导出 ${strategyName}...

导出文件将包含：
📋 详细的资产配置方案
📈 投资执行计划
📊 风险控制措施
🔄 调仓策略建议

文件格式：PDF/Excel`);
}

// 板块轮动预测分析报告
function generateSectorRotationReport() {
    const reportData = {
        currentSituation: {
            leadingSectors: ['资源能源', '基建制造', '国防军工'],
            laggingSectors: ['科技成长', '新能源', '传媒娱乐'],
            rotationSpeed: '快速轮动',
            marketSentiment: '谨慎乐观',
            updateTime: new Date().toLocaleString('zh-CN')
        },
        prediction: {
            timeframe: '未来1-3个月',
            expectedRotation: '从防御向周期轮动',
            keyFactors: [
                '大宗商品价格走势',
                '货币政策预期', 
                '地缘政治局势',
                '产业政策导向',
                '资金流向变化',
                '市场情绪指标'
            ],
            confidenceLevel: '高'
        },
        recommendations: {
            overweight: ['资源', '基建', '军工'],
            underweight: ['科技', '新能源'],
            neutral: ['金融', '消费'],
            cashAllocation: '10-15%'
        },
        riskAssessment: {
            overallRisk: '中等',
            marketRisk: '低',
            sectorRisk: '中高',
            policyRisk: '中'
        }
    };
    
    return reportData;
}

// 初始化模块时的额外设置
function initializeSectorRotationModule() {
    console.log('板块轮动预测模块初始化完成');
    
    // 设置默认时间维度
    changeTimeframe('30d');
    
    // 设置默认风险偏好
    updateInvestmentStrategy();
    
    // 更新实时状态
    document.getElementById('leadingUpSectors').textContent = '资源、能源、基建、军工';
    document.getElementById('leadingDownSectors').textContent = '科技、机器人、新能源';
    document.getElementById('neutralSectors').textContent = '金融、消费、医药、传媒';
    
    // 添加模块加载完成提示
    setTimeout(() => {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-success alert-dismissible fade show';
        alertDiv.innerHTML = `
            <i class="bi bi-check-circle"></i>
            <strong>板块轮动预测模块加载成功！</strong> 当前市场分析已更新至最新数据。
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('.container-fluid').insertBefore(alertDiv, document.querySelector('.container-fluid').firstChild);
    }, 1000);
}

// 修改模块初始化调用
setTimeout(() => {
    generateSectorRotationHeatmap();
    generateSectorRotationPrediction('30d');
    generateInvestmentStrategy('risk-balanced');
    loadSectorRotationHistory();
    initializeSectorRotationModule();
}, 1000);

// 导出板块轮动分析报告
function exportSectorRotationReport() {
    const report = generateSectorRotationReport();
    const reportText = `
板块轮动分析报告
生成时间: ${new Date().toLocaleString('zh-CN')}

当前市场状况:
- 领涨板块: ${report.currentSituation.leadingSectors.join(', ')}
- 领跌板块: ${report.currentSituation.laggingSectors.join(', ')}
- 轮动速度: ${report.currentSituation.rotationSpeed}
- 市场情绪: ${report.currentSituation.marketSentiment}

未来预测 (${report.prediction.timeframe}):
- 预期轮动方向: ${report.prediction.expectedRotation}
- 关键影响因素: ${report.prediction.keyFactors.join(', ')}

投资建议:
- 超配板块: ${report.recommendations.overweight.join(', ')}
- 低配板块: ${report.recommendations.underweight.join(', ')}
- 中性配置: ${report.recommendations.neutral.join(', ')}
    `;
    
    // 在实际应用中，这里会生成PDF或Excel文件
    alert(`板块轮动分析报告已生成！\n\n${reportText}`);
}

// 生成板块轮动预测数据
function generateSectorRotationPrediction(timeframe = '30d') {
    const predictionContainer = document.getElementById('sectorRotationPrediction');
    
    // 模拟板块轮动预测数据
    const sectorPredictions = [
        { name: '资源能源', probability: 85, trend: '继续上涨', reason: '大宗商品价格支撑', type: '周期', strength: '强' },
        { name: '基建制造', probability: 78, trend: '稳步上涨', reason: '政策利好推动', type: '周期', strength: '强' },
        { name: '国防军工', probability: 72, trend: '震荡上行', reason: '地缘政治因素', type: '防御', strength: '中' },
        { name: '医药生物', probability: 68, trend: '温和上涨', reason: '人口老龄化需求', type: '防御', strength: '中' },
        { name: '金融保险', probability: 65, trend: '企稳回升', reason: '估值修复预期', type: '金融', strength: '中' },
        { name: '消费零售', probability: 62, trend: '缓慢复苏', reason: '消费信心恢复', type: '消费', strength: '中' },
        { name: '科技成长', probability: 45, trend: '震荡调整', reason: '估值压力较大', type: '成长', strength: '弱' },
        { name: '新能源', probability: 38, trend: '继续调整', reason: '产能过剩担忧', type: '成长', strength: '弱' },
        { name: '机器人', probability: 25, trend: '大幅下跌', reason: '技术瓶颈限制', type: '成长', strength: '弱' }
    ];
    
    // 根据时间维度调整预测数据
    const timeframeFactors = {
        '30d': { factor: 1.0, label: '未来30天' },
        '90d': { factor: 0.9, label: '未来90天' },
        '180d': { factor: 0.8, label: '未来180天' },
        '360d': { factor: 0.7, label: '未来360天' }
    };
    
    const factor = timeframeFactors[timeframe] || timeframeFactors['30d'];
    
    // 生成预测表格HTML
    const tableHtml = `
        <div class="card">
            <div class="card-header bg-light">
                <div class="d-flex justify-content-between align-items-center">
                    <h6 class="mb-0">${factor.label}板块轮动预测</h6>
                    <div class="btn-group">
                        <button class="btn btn-sm btn-outline-primary" onclick="sortByProbability()">
                            <i class="bi bi-sort-numeric-down"></i> 按概率排序
                        </button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="filterByStrength('all')">
                            <i class="bi bi-filter"></i> 筛选强度
                        </button>
                    </div>
                </div>
            </div>
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead class="table-light">
                            <tr>
                                <th>板块名称</th>
                                <th>预测概率</th>
                                <th>趋势方向</th>
                                <th>主要因素</th>
                                <th>板块类型</th>
                                <th>强度</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${sectorPredictions.map(sector => {
                                const adjustedProbability = Math.round(sector.probability * factor.factor);
                                return `
                                <tr>
                                    <td><strong>${sector.name}</strong></td>
                                    <td>
                                        <div class="progress" style="height: 20px; width: 100px;">
                                            <div class="progress-bar ${adjustedProbability >= 70 ? 'bg-success' : adjustedProbability >= 50 ? 'bg-warning' : 'bg-danger'}" 
                                                 style="width: ${adjustedProbability}%">
                                                ${adjustedProbability}%
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <span class="badge ${sector.trend.includes('上涨') ? 'bg-success' : sector.trend.includes('调整') ? 'bg-warning' : 'bg-danger'}">
                                            ${sector.trend}
                                        </span>
                                    </td>
                                    <td><small class="text-muted">${sector.reason}</small></td>
                                    <td><span class="badge bg-secondary">${sector.type}</span></td>
                                    <td>
                                        <span class="badge ${sector.strength === '强' ? 'bg-success' : sector.strength === '中' ? 'bg-warning' : 'bg-danger'}">
                                            ${sector.strength}
                                        </span>
                                    </td>
                                </tr>
                                `;
                            }).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
    
    predictionContainer.innerHTML = tableHtml;
}

// 排序功能
function sortByProbability() {
    alert('排序功能已触发，将按概率从高到低排序');
}

// 筛选功能
function filterByStrength(strength) {
    alert(`筛选功能已触发，显示${strength === 'all' ? '全部' : strength}强度板块`);
}

// 切换时间维度
function changeTimeframe(timeframe) {
    generateSectorRotationPrediction(timeframe);
    document.getElementById('lastUpdateTime').textContent = new Date().toLocaleString('zh-CN');
}

// 生成投资策略
function generateInvestmentStrategy(riskPreference = 'risk-balanced') {
    const strategies = {
        'risk-conservative': {
            name: '保守型',
            allocation: {
                '资源能源': '25%',
                '基建制造': '20%',
                '国防军工': '15%',
                '医药生物': '15%',
                '金融保险': '15%',
                '现金': '10%'
            },
            description: '稳健配置，重点布局防御性板块'
        },
        'risk-balanced': {
            name: '平衡型',
            allocation: {
                '资源能源': '30%',
                '基建制造': '25%',
                '国防军工': '15%',
                '医药生物': '10%',
                '金融保险': '10%',
                '消费零售': '5%',
                '现金': '5%'
            },
            description: '均衡配置，兼顾周期与防御板块'
        },
        'risk-aggressive': {
            name: '激进型',
            allocation: {
                '资源能源': '35%',
                '基建制造': '30%',
                '国防军工': '15%',
                '科技成长': '10%',
                '新能源': '5%',
                '现金': '5%'
            },
            description: '积极配置，重点布局高增长板块'
        }
    };
    
    const strategy = strategies[riskPreference] || strategies['risk-balanced'];
    const strategyContainer = document.getElementById('investmentStrategy');
    
    strategyContainer.innerHTML = `
        <div class="alert alert-success">
            <h6><i class="bi bi-lightning-charge"></i> ${strategy.name}投资策略</h6>
            <p class="mb-2">${strategy.description}</p>
            <div class="mt-3">
                <h6>资产配置建议：</h6>
                <div class="row">
                    ${Object.entries(strategy.allocation).map(([sector, allocation]) => `
                        <div class="col-6 mb-2">
                            <small>${sector}: <span class="fw-bold text-primary">${allocation}</span></small>
                        </div>
                    `).join('')}
                </div>
            </div>
            <div class="mt-3">
                <button class="btn btn-sm btn-outline-primary me-2" onclick="simulateStrategy('${riskPreference}')">
                    <i class="bi bi-graph-up"></i> 策略回测
                </button>
                <button class="btn btn-sm btn-outline-success" onclick="exportStrategy('${riskPreference}')">
                    <i class="bi bi-download"></i> 导出策略
                </button>
            </div>
        </div>
    `;
}

// 初始化板块轮动预测模块
console.log('板块轮动预测模块加载完成');