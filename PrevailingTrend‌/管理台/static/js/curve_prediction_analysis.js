/**
 * 曲线预测分析模块 - 第六层模块
 * 大势所趋风险框架管理台
 */

// 从权重分析导入数据
function importFromWeightAnalysis() {
  if (!window.appData || !window.appData.weightData) {
    alert('没有可用的权重分析数据，请先在权重分析模块中导出数据');
    return;
  }

  // 转换数据格式
  const weightData = window.appData.weightData;
  const convertedData = convertWeightToPredictionData(weightData);
  
  // 存储转换后的数据
  window.appData.predictionData = convertedData;
  
  // 提示用户
  const toastHTML = `
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
      <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header bg-success text-white">
          <strong class="me-auto">数据导入成功</strong>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          已成功导入${convertedData.length}条预测数据
        </div>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', toastHTML);
  
  // 3秒后自动移除提示
  setTimeout(() => {
    const toast = document.querySelector('.toast.show');
    if (toast) {
      toast.remove();
    }
  }, 3000);
  
  // 重新渲染模块
  renderCurvePredictionAnalysisModule(document.getElementById('content'));
}

// 转换权重数据为预测数据
function convertWeightToPredictionData(weightData) {
  return weightData.map(item => {
    // 根据权重计算预测基准值
    let baseValue = item.weight * 0.9;
    
    // 根据风险等级调整基准值
    if (item.originalRiskLevel === '高') baseValue -= 5;
    else if (item.originalRiskLevel === '中高') baseValue -= 2;
    else if (item.originalRiskLevel === '中低') baseValue += 2;
    else if (item.originalRiskLevel === '低') baseValue += 5;
    
    return {
      id: item.id,
      name: item.name,
      category: item.category,
      baseValue: baseValue,
      weight: item.weight,
      originalRiskLevel: item.originalRiskLevel
    };
  });
}

// 加载曲线预测分析模块
function loadCurvePredictionAnalysis() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载曲线预测分析数据...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderCurvePredictionAnalysisModule(contentArea);
  }, 800);
}

// 渲染曲线预测分析模块内容
function renderCurvePredictionAnalysisModule(container) {
  // 获取预测数据
  const predictionData = getPredictionData();
  
  // 构建模块HTML
  const moduleHTML = buildPredictionModuleHTML(predictionData);
  
  // 更新容器内容
  container.innerHTML = moduleHTML;
  
  // 初始化Bootstrap组件
  initBootstrapComponents();
  
  // 初始化图表
  initPredictionCharts(predictionData);
  
  // 初始化交互功能
  initPredictionInteractions();
}

// 获取预测数据
function getPredictionData() {
  // 模拟数据获取
  return {
    historicalData: [95.2, 95.8, 96.3, 95.9, 96.5],
    predictedData: [96.5, 97.2, 97.8, 98.3],
    confidenceInterval: {
      lower: [95.8, 96.4, 97.0, 97.5],
      upper: [97.2, 98.0, 98.6, 99.1]
    },
    accuracy: 0.85,
    modelParameters: {
      alpha: 0.05,
      beta: 0.1,
      gamma: 0.3
    }
  };
}

// 初始化Bootstrap组件
function initBootstrapComponents() {
  // 检查是否已加载Bootstrap
  if (typeof bootstrap === 'undefined') {
    // 如果没有加载Bootstrap JS，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js';
    document.head.appendChild(script);
  }
}

// 初始化预测图表
function initPredictionCharts(data) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createPredictionTrendChart(data);
      createAccuracyTrendChart(data);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createPredictionTrendChart(data);
    createAccuracyTrendChart(data);
  }
}

// 创建预测趋势图表
function createPredictionTrendChart(data) {
  const chartDom = document.getElementById('prediction-trend-chart');
  if (!chartDom) return;
  
  const myChart = echarts.init(chartDom);
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        let result = params[0].axisValue + '<br/>';
        params.forEach(function(item) {
          result += item.marker + ' ' + item.seriesName + ': ' + item.value + '<br/>';
        });
        return result;
      }
    },
    legend: {
      data: ['历史数据', '预测值', '置信区间']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['T-4', 'T-3', 'T-2', 'T-1', 'T', 'T+1', 'T+2', 'T+3', 'T+4']
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '{value}'
      }
    },
    series: [
      {
        name: '历史数据',
        type: 'line',
        data: [...data.historicalData, null, null, null, null],
        smooth: true,
        lineStyle: {
          width: 3
        }
      },
      {
        name: '预测值',
        type: 'line',
        data: [null, null, null, null, data.historicalData[data.historicalData.length-1], ...data.predictedData],
        smooth: true,
        lineStyle: {
          width: 3,
          type: 'dashed'
        }
      },
      {
        name: '置信区间',
        type: 'line',
        data: [null, null, null, null, data.historicalData[data.historicalData.length-1], ...data.confidenceInterval.upper],
        lineStyle: {
          opacity: 0
        },
        stack: 'confidence',
        symbol: 'none',
        areaStyle: {
          color: '#ccc',
          opacity: 0.3
        }
      },
      {
        name: '置信区间',
        type: 'line',
        data: [null, null, null, null, data.historicalData[data.historicalData.length-1], ...data.confidenceInterval.lower],
        lineStyle: {
          opacity: 0
        },
        areaStyle: {
          color: '#ccc',
          opacity: 0.3
        },
        stack: 'confidence',
        symbol: 'none'
      }
    ]
  };
  myChart.setOption(option);
}

// 创建准确率趋势图表
function createAccuracyTrendChart(data) {
  // 实现准确率趋势图表
}

// 初始化交互功能
function initPredictionInteractions() {
  // 绑定预测类型切换事件
  const predictionTypeSelect = document.getElementById('prediction-type');
  if (predictionTypeSelect) {
    predictionTypeSelect.addEventListener('change', function() {
      // 更新预测目标下拉框
      updatePredictionTargets(this.value);
    });
  }
  
  // 绑定预测模型切换事件
  const predictionModelSelect = document.getElementById('prediction-model');
  if (predictionModelSelect) {
    predictionModelSelect.addEventListener('change', function() {
      // 更新模型描述
      updateModelDescription(this.value);
    });
  }
  
  // 绑定情景分析开关事件
  const enableScenariosSwitch = document.getElementById('enable-scenarios');
  if (enableScenariosSwitch) {
    enableScenariosSwitch.addEventListener('change', function() {
      // 更新情景分析区域的显示状态
      toggleScenariosSection(this.checked);
    });
  }
}

// 运行预测
function runPrediction() {
  // 显示加载状态
  const runButton = document.querySelector('button[onclick="runPrediction()"]');
  if (runButton) {
    const originalText = runButton.innerHTML;
    runButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 预测中...';
    runButton.disabled = true;
    
    // 模拟预测过程
    setTimeout(() => {
      // 恢复按钮状态
      runButton.innerHTML = originalText;
      runButton.disabled = false;
      
      // 更新图表
      const predictionData = getPredictionData();
      createPredictionTrendChart(predictionData);
      
      // 显示成功提示
      showToast('预测完成', '预测分析已成功完成，结果已更新。', 'success');
    }, 2000);
  }
}

// 显示提示消息
function showToast(title, message, type = 'info') {
  // 创建Toast元素
  const toastContainer = document.createElement('div');
  toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
  toastContainer.style.zIndex = '5';
  
  const toastElement = document.createElement('div');
  toastElement.className = `toast align-items-center text-white bg-${type} border-0`;
  toastElement.setAttribute('role', 'alert');
  toastElement.setAttribute('aria-live', 'assertive');
  toastElement.setAttribute('aria-atomic', 'true');
  
  toastElement.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">
        <strong>${title}</strong>: ${message}
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  `;
  
  toastContainer.appendChild(toastElement);
  document.body.appendChild(toastContainer);
  
  // 显示Toast
  const toast = new bootstrap.Toast(toastElement, {
    autohide: true,
    delay: 3000
  });
  toast.show();
  
  // 自动移除
  toastElement.addEventListener('hidden.bs.toast', function () {
    document.body.removeChild(toastContainer);
  });
}

// 构建预测模块HTML
function buildPredictionModuleHTML(data) {
  return `
    <div class="card mb-4">
      <div class="card-header bg-primary text-white">
        <h5 class="mb-0">曲线预测分析</h5>
      </div>
      <div class="card-body">
        <div class="row mb-3">
          <div class="col-md-4">
            <label for="prediction-type" class="form-label">预测类型</label>
            <select id="prediction-type" class="form-select">
              <option value="stock">个股预测</option>
              <option value="industry">行业预测</option>
              <option value="composite">综合预测</option>
            </select>
          </div>
          <div class="col-md-4">
            <label for="prediction-target" class="form-label">预测目标</label>
            <select id="prediction-target" class="form-select">
              <option value="600519">贵州茅台</option>
              <option value="000858">五粮液</option>
              <option value="600036">招商银行</option>
            </select>
          </div>
          <div class="col-md-4">
            <label for="prediction-model" class="form-label">预测模型</label>
            <select id="prediction-model" class="form-select">
              <option value="arima">ARIMA模型</option>
              <option value="lstm">LSTM神经网络</option>
              <option value="ensemble">集成模型</option>
            </select>
          </div>
        </div>
        
        <div class="row mb-3">
          <div class="col-md-12">
            <div id="prediction-trend-chart" style="height: 400px;"></div>
          </div>
        </div>
        
        <div class="row">
          <div class="col-md-6">
            <div class="card">
              <div class="card-header">
                <h6 class="mb-0">预测控制面板</h6>
              </div>
              <div class="card-body">
                <div class="d-grid gap-2">
                  <button class="btn btn-primary" onclick="runPrediction()">运行预测</button>
                  <button class="btn btn-outline-primary" onclick="exportPredictionResults('excel')">导出Excel</button>
                  <button class="btn btn-outline-primary" onclick="exportPredictionResults('pdf')">导出PDF</button>
                  <button class="btn btn-outline-success" onclick="importFromWeightAnalysis()">从权重分析导入</button>
                  <button class="btn btn-outline-secondary" onclick="sharePredictionResults()">分享结果</button>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card">
              <div class="card-header">
                <div class="d-flex justify-content-between align-items-center">
                  <h6 class="mb-0">预测参数</h6>
                  <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="enable-scenarios">
                    <label class="form-check-label" for="enable-scenarios">情景分析</label>
                  </div>
                </div>
              </div>
              <div class="card-body">
                <div class="mb-3">
                  <label class="form-label">预测时间范围</label>
                  <div class="btn-group btn-group-sm w-100">
                    <button type="button" class="btn btn-outline-primary active" onclick="switchChartView('1m')">1个月</button>
                    <button type="button" class="btn btn-outline-primary" onclick="switchChartView('3m')">3个月</button>
                    <button type="button" class="btn btn-outline-primary" onclick="switchChartView('6m')">6个月</button>
                  </div>
                </div>
                <div class="mb-3">
                  <label class="form-label">模型参数</label>
                  <div class="small text-muted">
                    α: ${data.modelParameters.alpha}, β: ${data.modelParameters.beta}, γ: ${data.modelParameters.gamma}
                  </div>
                </div>
                <div class="mb-3">
                  <label class="form-label">预测准确率</label>
                  <div class="progress">
                    <div class="progress-bar bg-success" role="progressbar" style="width: ${data.accuracy * 100}%" aria-valuenow="${data.accuracy * 100}" aria-valuemin="0" aria-valuemax="100">${(data.accuracy * 100).toFixed(1)}%</div>
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