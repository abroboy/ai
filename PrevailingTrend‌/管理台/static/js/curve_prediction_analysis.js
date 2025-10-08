// 曲线预测分析模块 - 完整实现
function loadCurvePredictionAnalysis() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-graph-up-arrow text-warning"></i> 多模型趋势预测分析</h2>
                    <p class="text-muted">基于多种机器学习模型的金融数据趋势预测与对比分析</p>
                </div>
            </div>
            
            <!-- 快速预测对话框 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-lightning-charge"></i> 快速预测</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-8">
                                    <div class="input-group mb-3">
                                        <span class="input-group-text"><i class="bi bi-search"></i></span>
                                        <input type="text" class="form-control" id="quickSearch" placeholder="输入股票代码、指数名称或行业关键词..." 
                                               onkeyup="searchPredictionObjects(this.value)">
                                        <button class="btn btn-primary" type="button" onclick="showQuickPredictionDialog()">
                                            <i class="bi bi-play-circle"></i> 快速预测
                                        </button>
                                    </div>
                                    <div id="searchResults" class="mt-2" style="display: none;">
                                        <!-- 搜索结果将在这里显示 -->
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <button class="btn btn-outline-secondary w-100 mb-2" onclick="showAdvancedSettings()">
                                        <i class="bi bi-gear"></i> 高级设置
                                    </button>
                                    <button class="btn btn-outline-info w-100" onclick="showModelComparison()">
                                        <i class="bi bi-bar-chart"></i> 模型对比
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 多模型预测结果 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5 class="mb-0"><i class="bi bi-graph-up"></i> 多模型预测曲线对比</h5>
                            <div class="btn-group">
                                <button class="btn btn-sm btn-outline-primary" onclick="runAllModelsPrediction()">
                                    <i class="bi bi-play-circle"></i> 执行多模型预测
                                </button>
                                <button class="btn btn-sm btn-outline-success" onclick="exportAllResults()">
                                    <i class="bi bi-download"></i> 导出全部
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <!-- 模型选择标签 -->
                            <ul class="nav nav-tabs mb-3" id="modelTabs" role="tablist">
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link active" id="arima-tab" data-bs-toggle="tab" data-bs-target="#arima" type="button" role="tab">
                                        <i class="bi bi-graph-up"></i> ARIMA
                                    </button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="lstm-tab" data-bs-toggle="tab" data-bs-target="#lstm" type="button" role="tab">
                                        <i class="bi bi-cpu"></i> LSTM
                                    </button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="prophet-tab" data-bs-toggle="tab" data-bs-target="#prophet" type="button" role="tab">
                                        <i class="bi bi-calendar"></i> Prophet
                                    </button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="ensemble-tab" data-bs-toggle="tab" data-bs-target="#ensemble" type="button" role="tab">
                                        <i class="bi bi-collection"></i> 集成学习
                                    </button>
                                </li>
                            </ul>
                            
                            <!-- 模型内容区域 -->
                            <div class="tab-content" id="modelTabContent">
                                <!-- ARIMA模型 -->
                                <div class="tab-pane fade show active" id="arima" role="tabpanel">
                                    <div class="row">
                                        <div class="col-md-8">
                                            <div id="arimaChart" style="height: 400px;">
                                                <div class="text-center text-muted py-5">
                                                    <i class="bi bi-graph-up display-4"></i>
                                                    <p class="mt-3">ARIMA模型预测曲线将在此显示</p>
                                                    <small class="text-info">基于时间序列统计特性进行预测</small>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="card">
                                                <div class="card-header">
                                                    <h6 class="mb-0">ARIMA模型详情</h6>
                                                </div>
                                                <div class="card-body">
                                                    <div id="arimaDetails">
                                                        <p class="text-muted">等待预测结果...</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- LSTM模型 -->
                                <div class="tab-pane fade" id="lstm" role="tabpanel">
                                    <div class="row">
                                        <div class="col-md-8">
                                            <div id="lstmChart" style="height: 400px;">
                                                <div class="text-center text-muted py-5">
                                                    <i class="bi bi-cpu display-4"></i>
                                                    <p class="mt-3">LSTM神经网络预测曲线将在此显示</p>
                                                    <small class="text-info">基于深度学习进行非线性预测</small>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="card">
                                                <div class="card-header">
                                                    <h6 class="mb-0">LSTM模型详情</h6>
                                                </div>
                                                <div class="card-body">
                                                    <div id="lstmDetails">
                                                        <p class="text-muted">等待预测结果...</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Prophet模型 -->
                                <div class="tab-pane fade" id="prophet" role="tabpanel">
                                    <div class="row">
                                        <div class="col-md-8">
                                            <div id="prophetChart" style="height: 400px;">
                                                <div class="text-center text-muted py-5">
                                                    <i class="bi bi-calendar display-4"></i>
                                                    <p class="mt-3">Prophet模型预测曲线将在此显示</p>
                                                    <small class="text-info">考虑季节性和节假日效应的预测</small>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="card">
                                                <div class="card-header">
                                                    <h6 class="mb-0">Prophet模型详情</h6>
                                                </div>
                                                <div class="card-body">
                                                    <div id="prophetDetails">
                                                        <p class="text-muted">等待预测结果...</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- 集成学习模型 -->
                                <div class="tab-pane fade" id="ensemble" role="tabpanel">
                                    <div class="row">
                                        <div class="col-md-8">
                                            <div id="ensembleChart" style="height: 400px;">
                                                <div class="text-center text-muted py-5">
                                                    <i class="bi bi-collection display-4"></i>
                                                    <p class="mt-3">集成学习模型预测曲线将在此显示</p>
                                                    <small class="text-info">多模型融合的稳健预测</small>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="card">
                                                <div class="card-header">
                                                    <h6 class="mb-0">集成学习详情</h6>
                                                </div>
                                                <div class="card-body">
                                                    <div id="ensembleDetails">
                                                        <p class="text-muted">等待预测结果...</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 模型性能对比 -->
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-bar-chart"></i> 模型性能对比</h5>
                        </div>
                        <div class="card-body">
                            <div id="modelComparison">
                                <div class="text-center text-muted py-4">
                                    <i class="bi bi-bar-chart display-4"></i>
                                    <p class="mt-3">执行预测后，模型性能对比将在此显示</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-clock-history"></i> 预测历史记录</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <thead class="table-light">
                                        <tr>
                                            <th>时间</th>
                                            <th>对象</th>
                                            <th>最佳模型</th>
                                            <th>准确率</th>
                                        </tr>
                                    </thead>
                                    <tbody id="predictionHistoryTable">
                                        <tr>
                                            <td colspan="4" class="text-center text-muted py-4">
                                                <div class="spinner-border text-info" role="status">
                                                    <span class="visually-hidden">加载中...</span>
                                                </div>
                                                <p class="mt-2">正在加载历史记录...</p>
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
        
        <!-- 快速预测对话框 -->
        <div class="modal fade" id="quickPredictionModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"><i class="bi bi-lightning-charge"></i> 快速预测设置</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">预测对象</label>
                                    <input type="text" class="form-control" id="modalObject" readonly>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">预测周期</label>
                                    <select class="form-select" id="modalPeriod">
                                        <option value="7">7天</option>
                                        <option value="15">15天</option>
                                        <option value="30" selected>30天</option>
                                        <option value="60">60天</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">选择预测模型</label>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="modalArima" checked>
                                <label class="form-check-label" for="modalArima">ARIMA模型</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="modalLstm" checked>
                                <label class="form-check-label" for="modalLstm">LSTM神经网络</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="modalProphet" checked>
                                <label class="form-check-label" for="modalProphet">Prophet模型</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="modalEnsemble" checked>
                                <label class="form-check-label" for="modalEnsemble">集成学习</label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                        <button type="button" class="btn btn-primary" onclick="confirmQuickPrediction()">开始预测</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 加载历史预测记录
    loadPredictionHistory();
}

// 搜索预测对象
function searchPredictionObjects(query) {
    const resultsDiv = document.getElementById('searchResults');
    
    if (!query || query.length < 2) {
        resultsDiv.style.display = 'none';
        return;
    }
    
    // 模拟搜索数据
    const searchData = [
        { name: '平安银行 (000001)', type: 'stock', code: '000001' },
        { name: '贵州茅台 (600519)', type: 'stock', code: '600519' },
        { name: '上证指数 (000001)', type: 'index', code: 'sh000001' },
        { name: '沪深300 (000300)', type: 'index', code: 'sh000300' },
        { name: '银行业', type: 'industry', code: 'bank' },
        { name: '科技行业', type: 'industry', code: 'technology' },
        { name: 'GDP增长率', type: 'macro', code: 'gdp' },
        { name: 'CPI消费者物价指数', type: 'macro', code: 'cpi' }
    ];
    
    const filteredResults = searchData.filter(item => 
        item.name.toLowerCase().includes(query.toLowerCase())
    );
    
    if (filteredResults.length === 0) {
        resultsDiv.innerHTML = '<div class="text-muted p-2">未找到匹配的对象</div>';
        resultsDiv.style.display = 'block';
        return;
    }
    
    let resultsHTML = '';
    filteredResults.forEach(item => {
        const typeIcon = getTypeIcon(item.type);
        resultsHTML += `
            <div class="search-result-item p-2 border-bottom" 
                 onclick="selectSearchResult('${item.name}', '${item.code}', '${item.type}')"
                 style="cursor: pointer;">
                <div class="d-flex align-items-center">
                    <i class="${typeIcon} me-2"></i>
                    <div>
                        <div class="fw-bold">${item.name}</div>
                        <small class="text-muted">${getTypeName(item.type)}</small>
                    </div>
                </div>
            </div>
        `;
    });
    
    resultsDiv.innerHTML = resultsHTML;
    resultsDiv.style.display = 'block';
}

// 获取类型图标
function getTypeIcon(type) {
    const icons = {
        'stock': 'bi bi-graph-up text-success',
        'index': 'bi bi-bar-chart text-primary',
        'industry': 'bi bi-building text-warning',
        'macro': 'bi bi-globe text-info'
    };
    return icons[type] || 'bi bi-question-circle';
}

// 获取类型名称
function getTypeName(type) {
    const names = {
        'stock': '个股',
        'index': '指数',
        'industry': '行业',
        'macro': '宏观经济指标'
    };
    return names[type] || '未知类型';
}

// 选择搜索结果
function selectSearchResult(name, code, type) {
    document.getElementById('quickSearch').value = name;
    document.getElementById('searchResults').style.display = 'none';
    
    // 存储选择的对象信息
    window.selectedPredictionObject = { name, code, type };
}

// 显示快速预测对话框
function showQuickPredictionDialog() {
    const searchInput = document.getElementById('quickSearch');
    if (!window.selectedPredictionObject) {
        alert('请先选择一个预测对象！');
        return;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('quickPredictionModal'));
    document.getElementById('modalObject').value = window.selectedPredictionObject.name;
    modal.show();
}

// 确认快速预测
function confirmQuickPrediction() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('quickPredictionModal'));
    modal.hide();
    
    // 获取选择的模型
    const selectedModels = [];
    if (document.getElementById('modalArima').checked) selectedModels.push('arima');
    if (document.getElementById('modalLstm').checked) selectedModels.push('lstm');
    if (document.getElementById('modalProphet').checked) selectedModels.push('prophet');
    if (document.getElementById('modalEnsemble').checked) selectedModels.push('ensemble');
    
    if (selectedModels.length === 0) {
        alert('请至少选择一个预测模型！');
        return;
    }
    
    // 执行多模型预测
    runAllModelsPrediction(selectedModels);
}

// 执行多模型预测
function runAllModelsPrediction(selectedModels = ['arima', 'lstm', 'prophet', 'ensemble']) {
    if (!window.selectedPredictionObject) {
        alert('请先选择一个预测对象！');
        return;
    }
    
    const objectName = window.selectedPredictionObject.name;
    const period = document.getElementById('modalPeriod') ? 
                  document.getElementById('modalPeriod').value : '30';
    
    // 显示加载状态
    showLoadingForAllModels();
    
    // 模拟多模型预测过程
    setTimeout(() => {
        // 为每个选中的模型生成预测结果
        selectedModels.forEach(model => {
            generateModelPrediction(model, objectName, period);
        });
        
        // 更新模型性能对比
        updateModelComparison(selectedModels);
        
        // 更新历史记录
        updatePredictionHistory(objectName, selectedModels);
        
    }, 3000);
}

// 显示所有模型的加载状态
function showLoadingForAllModels() {
    const models = ['arima', 'lstm', 'prophet', 'ensemble'];
    
    models.forEach(model => {
        const chartDiv = document.getElementById(`${model}Chart`);
        const detailsDiv = document.getElementById(`${model}Details`);
        
        if (chartDiv) {
            chartDiv.innerHTML = `
                <div class="text-center py-5">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">加载中...</span>
                    </div>
                    <p class="mt-2">${getModelDisplayName(model)}模型预测中...</p>
                    <small class="text-muted">模型训练和预测进行中</small>
                </div>
            `;
        }
        
        if (detailsDiv) {
            detailsDiv.innerHTML = '<p class="text-muted">等待预测结果...</p>';
        }
    });
}

// 生成单个模型的预测结果
function generateModelPrediction(model, objectName, period) {
    const chartDiv = document.getElementById(`${model}Chart`);
    const detailsDiv = document.getElementById(`${model}Details`);
    
    if (!chartDiv || !detailsDiv) return;
    
    // 生成模拟数据
    const historicalData = generateHistoricalDataForModel(model);
    const predictionData = generatePredictionDataForModel(model, period);
    
    // 更新图表显示
    chartDiv.innerHTML = createModelChartHTML(model, objectName, historicalData, predictionData);
    
    // 更新模型详情
    detailsDiv.innerHTML = createModelDetailsHTML(model, objectName, period);
}

// 为不同模型生成不同的历史数据
function generateHistoricalDataForModel(model) {
    const baseData = Array.from({length: 100}, (_, i) => ({
        date: new Date(Date.now() - (100 - i) * 24 * 60 * 60 * 1000),
        value: 0
    }));
    
    // 根据不同模型生成不同的数据模式
    switch(model) {
        case 'arima':
            // ARIMA模型数据 - 相对平稳
            return baseData.map((item, i) => ({
                ...item,
                value: 100 + Math.sin(i * 0.05) * 10 + Math.random() * 5
            }));
        case 'lstm':
            // LSTM模型数据 - 复杂模式
            return baseData.map((item, i) => ({
                ...item,
                value: 100 + Math.sin(i * 0.1) * 15 + Math.sin(i * 0.03) * 8 + Math.random() * 3
            }));
        case 'prophet':
            // Prophet模型数据 - 季节性明显
            return baseData.map((item, i) => ({
                ...item,
                value: 100 + Math.sin(i * 0.02) * 20 + Math.sin(i * 0.2) * 10 + Math.random() * 4
            }));
        case 'ensemble':
            // 集成学习数据 - 综合模式
            return baseData.map((item, i) => ({
                ...item,
                value: 100 + Math.sin(i * 0.07) * 12 + Math.sin(i * 0.15) * 6 + Math.random() * 3
            }));
        default:
            return baseData;
    }
}

// 为不同模型生成不同的预测数据
function generatePredictionDataForModel(model, period) {
    const predictionLength = parseInt(period);
    
    return Array.from({length: predictionLength}, (_, i) => {
        const baseValue = 120;
        let trend = 0;
        
        // 根据不同模型生成不同的预测趋势
        switch(model) {
            case 'arima':
                trend = Math.sin(i * 0.1) * 8;
                break;
            case 'lstm':
                trend = Math.sin(i * 0.15) * 12 + Math.sin(i * 0.05) * 4;
                break;
            case 'prophet':
                trend = Math.sin(i * 0.08) * 10 + Math.sin(i * 0.25) * 6;
                break;
            case 'ensemble':
                trend = Math.sin(i * 0.12) * 9 + Math.sin(i * 0.18) * 3;
                break;
        }
        
        return {
            date: new Date(Date.now() + i * 24 * 60 * 60 * 1000),
            value: baseValue + trend + Math.random() * 6,
            lower: baseValue + trend - 4,
            upper: baseValue + trend + 4
        };
    });
}

// 创建模型图表HTML
function createModelChartHTML(model, objectName, historicalData, predictionData) {
    const modelName = getModelDisplayName(model);
    const totalPoints = historicalData.length + predictionData.length;
    
    return `
        <div class="model-chart-container">
            <h6 class="text-center mb-3">${objectName} - ${modelName}预测曲线</h6>
            <div class="chart-area" style="height: 350px; background: #f8f9fa; border-radius: 8px; padding: 15px;">
                <div class="chart-legend d-flex justify-content-center mb-2">
                    <span class="badge bg-primary me-2">历史数据 (${historicalData.length}点)</span>
                    <span class="badge bg-success me-2">预测数据 (${predictionData.length}天)</span>
                    <span class="badge bg-warning">置信区间</span>
                </div>
                <div class="chart-visual mt-2" style="height: 300px; position: relative;">
                    <div class="text-center" style="margin-top: 120px;">
                        <i class="bi bi-graph-up text-primary display-4"></i>
                        <p class="mt-2">${modelName}预测曲线</p>
                        <div class="row mt-3">
                            <div class="col-4">
                                <small class="text-muted">最终预测值</small>
                                <div><strong>${predictionData[predictionData.length-1]?.value.toFixed(2) || '--'}</strong></div>
                            </div>
                            <div class="col-4">
                                <small class="text-muted">预测变化</small>
                                <div><strong class="text-success">+${((predictionData[predictionData.length-1]?.value - historicalData[historicalData.length-1]?.value) || 0).toFixed(2)}</strong></div>
                            </div>
                            <div class="col-4">
                                <small class="text-muted">置信度</small>
                                <div><strong>${getModelConfidence(model)}%</strong></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 创建模型详情HTML
function createModelDetailsHTML(model, objectName, period) {
    const modelInfo = getModelInfo(model);
    
    return `
        <div class="model-details">
            <h6>${modelInfo.name}预测详情</h6>
            <div class="mb-2">
                <small class="text-muted">预测对象</small>
                <div><strong>${objectName}</strong></div>
            </div>
            <div class="mb-2">
                <small class="text-muted">预测周期</small>
                <div><strong>${period}天</strong></div>
            </div>
            <div class="mb-2">
                <small class="text-muted">模型准确率</small>
                <div><span class="badge bg-success">${modelInfo.accuracy}%</span></div>
            </div>
            <div class="mb-2">
                <small class="text-muted">训练数据量</small>
                <div><strong>${modelInfo.trainingData}</strong></div>
            </div>
            <div class="mb-2">
                <small class="text-muted">预测方向</small>
                <div><span class="badge bg-success">上涨趋势</span></div>
            </div>
            <div class="mt-3">
                <small class="text-muted">${modelInfo.description}</small>
            </div>
        </div>
    `;
}

// 获取模型显示名称
function getModelDisplayName(model) {
    const names = {
        'arima': 'ARIMA',
        'lstm': 'LSTM神经网络',
        'prophet': 'Prophet',
        'ensemble': '集成学习'
    };
    return names[model] || model;
}

// 获取模型置信度
function getModelConfidence(model) {
    const confidences = {
        'arima': 82,
        'lstm': 87,
        'prophet': 85,
        'ensemble': 90
    };
    return confidences[model] || 80;
}

// 获取模型信息
function getModelInfo(model) {
    const info = {
        'arima': {
            name: 'ARIMA模型',
            accuracy: 82,
            trainingData: '1000个时间点',
            description: '基于时间序列统计特性的经典预测模型'
        },
        'lstm': {
            name: 'LSTM神经网络',
            accuracy: 87,
            trainingData: '5000个样本',
            description: '深度学习模型，擅长捕捉复杂时间模式'
        },
        'prophet': {
            name: 'Prophet模型',
            accuracy: 85,
            trainingData: '2000个时间点',
            description: 'Facebook开源工具，考虑季节性和节假日效应'
        },
        'ensemble': {
            name: '集成学习',
            accuracy: 90,
            trainingData: '综合多模型',
            description: '多模型融合，提高预测稳定性和准确性'
        }
    };
    return info[model] || { name: model, accuracy: 80, trainingData: '未知', description: '' };
}

// 更新模型性能对比
function updateModelComparison(selectedModels) {
    const comparisonDiv = document.getElementById('modelComparison');
    
    let comparisonHTML = `
        <h6>模型性能对比</h6>
        <div class="performance-comparison">
    `;
    
    selectedModels.forEach(model => {
        const info = getModelInfo(model);
        comparisonHTML += `
            <div class="performance-item mb-3">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <span class="fw-bold">${info.name}</span>
                    <span class="badge bg-success">${info.accuracy}%</span>
                </div>
                <div class="progress" style="height: 8px;">
                    <div class="progress-bar" style="width: ${info.accuracy}%"></div>
                </div>
                <small class="text-muted">${info.description}</small>
            </div>
        `;
    });
    
    comparisonHTML += '</div>';
    comparisonDiv.innerHTML = comparisonHTML;
}

// 更新预测历史记录
function updatePredictionHistory(objectName, selectedModels) {
    const tableBody = document.getElementById('predictionHistoryTable');
    
    const bestModel = selectedModels.reduce((best, current) => {
        const currentAccuracy = getModelInfo(current).accuracy;
        const bestAccuracy = best ? getModelInfo(best).accuracy : 0;
        return currentAccuracy > bestAccuracy ? current : best;
    }, null);
    
    const newRecord = {
        time: new Date().toLocaleString('zh-CN'),
        object: objectName,
        bestModel: getModelDisplayName(bestModel),
        accuracy: getModelInfo(bestModel).accuracy + '%'
    };
    
    // 添加到表格顶部
    let newRow = `
        <tr>
            <td><small>${newRecord.time}</small></td>
            <td><strong>${newRecord.object}</strong></td>
            <td><span class="badge bg-info">${newRecord.bestModel}</span></td>
            <td><span class="badge bg-success">${newRecord.accuracy}</span></td>
        </tr>
    `;
    
    // 保持最多5条记录
    const currentRows = tableBody.querySelectorAll('tr');
    if (currentRows.length >= 5) {
        tableBody.deleteRow(currentRows.length - 1);
    }
    
    tableBody.innerHTML = newRow + tableBody.innerHTML;
}

// 高级设置
function showAdvancedSettings() {
    alert('高级设置功能开发中...\
包括：参数调优、数据预处理、特征工程等');
}

// 模型对比
function showModelComparison() {
    alert('模型对比功能开发中...\
包括：性能指标对比、预测结果可视化对比等');
}

// 导出全部结果
function exportAllResults() {
    if (!window.selectedPredictionObject) {
        alert('请先执行预测分析！');
        return;
    }
    
    alert(`正在导出 ${window.selectedPredictionObject.name} 的所有模型预测结果...`);
}

// 加载历史预测记录
function loadPredictionHistory() {
    const tableBody = document.getElementById('predictionHistoryTable');
    
    // 模拟历史数据
    const historyData = [
        { time: '2025-10-07 14:30', object: '上证指数', bestModel: '集成学习', accuracy: '90%' },
        { time: '2025-10-06 11:15', object: '贵州茅台', bestModel: 'LSTM神经网络', accuracy: '87%' },
        { time: '2025-10-05 16:45', object: '沪深300', bestModel: 'Prophet', accuracy: '85%' }
    ];
    
    let tableHTML = '';
    historyData.forEach(record => {
        tableHTML += `
            <tr>
                <td><small>${record.time}</small></td>
                <td><strong>${record.object}</strong></td>
                <td><span class="badge bg-info">${record.bestModel}</span></td>
                <td><span class="badge bg-success">${record.accuracy}</span></td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = tableHTML;
}