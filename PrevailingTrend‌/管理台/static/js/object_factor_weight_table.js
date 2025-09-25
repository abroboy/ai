/**
 * 对象因子权重表模块
 * 大势所趋风险框架管理台 - 第五层模块
 */

// 从评分系统导入数据
function importFromScoreSystem() {
  if (!window.appData || !window.appData.scoreData) {
    alert('没有可用的评分系统数据，请先在评分系统模块中导出数据');
    return;
  }

  // 转换数据格式
  const scoreData = window.appData.scoreData;
  const convertedData = convertScoreToWeightData(scoreData);
  
  // 存储转换后的数据
  window.appData.weightData = convertedData;
  
  // 提示用户
  const toastHTML = `
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
      <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header bg-success text-white">
          <strong class="me-auto">数据导入成功</strong>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          已成功导入${convertedData.length}条权重数据
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
  renderObjectFactorWeightTableModule(document.getElementById('content'));
}

// 转换评分数据为权重数据
function convertScoreToWeightData(scoreData) {
  return scoreData.map(item => {
    // 根据评分计算初始权重
    let weight = item.score * 0.8;
    
    // 根据趋势调整权重
    if (item.originalTrend === '上升') weight += 5;
    else if (item.originalTrend === '下降') weight -= 5;
    
    // 确保权重在合理范围内
    weight = Math.max(5, Math.min(100, weight));
    
    return {
      id: item.id,
      name: item.name,
      category: item.category,
      weight: weight,
      score: item.score,
      originalTrend: item.originalTrend,
      originalRiskLevel: item.originalRiskLevel
    };
  });
}

// 加载对象因子权重表模块
function loadObjectFactorWeightTable() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载对象因子权重表数据...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderObjectFactorWeightTableModule(contentArea);
  }, 800);
}

// 渲染对象因子权重表模块内容
function renderObjectFactorWeightTableModule(container) {
  // 模拟权重数据
  const weightData = {
    updateTime: "2025-09-25 14:30:00",
    objectTypes: ["公司", "行业", "市场"],
    currentObjectType: "公司",
    factorCategories: [
      {
        name: "财务因子",
        factors: [
          { id: "F001", name: "净利润增长率", weight: 25, description: "反映公司盈利能力的增长情况" },
          { id: "F002", name: "资产负债率", weight: 15, description: "反映公司的负债水平和偿债能力" },
          { id: "F003", name: "ROE", weight: 20, description: "反映公司的净资产收益率" },
          { id: "F004", name: "毛利率", weight: 10, description: "反映公司的盈利能力" },
          { id: "F005", name: "经营现金流", weight: 15, description: "反映公司的现金流状况" },
          { id: "F006", name: "营收增长率", weight: 15, description: "反映公司的业务增长情况" }
        ],
        totalWeight: 100
      },
      {
        name: "市场因子",
        factors: [
          { id: "M001", name: "市盈率", weight: 20, description: "反映公司的估值水平" },
          { id: "M002", name: "市净率", weight: 15, description: "反映公司的净资产估值水平" },
          { id: "M003", name: "股价波动率", weight: 25, description: "反映公司股价的波动情况" },
          { id: "M004", name: "相对大盘表现", weight: 20, description: "反映公司相对于大盘的表现" },
          { id: "M005", name: "成交量变化", weight: 20, description: "反映公司股票的交易活跃度" }
        ],
        totalWeight: 100
      },
      {
        name: "行业因子",
        factors: [
          { id: "I001", name: "行业景气度", weight: 30, description: "反映行业的整体发展状况" },
          { id: "I002", name: "行业竞争格局", weight: 25, description: "反映行业的竞争情况" },
          { id: "I003", name: "政策支持度", weight: 20, description: "反映行业的政策支持情况" },
          { id: "I004", name: "行业成长性", weight: 25, description: "反映行业的未来发展潜力" }
        ],
        totalWeight: 100
      },
      {
        name: "风险因子",
        factors: [
          { id: "R001", name: "流动性风险", weight: 20, description: "反映公司的短期偿债能力" },
          { id: "R002", name: "经营风险", weight: 25, description: "反映公司的经营稳定性" },
          { id: "R003", name: "财务风险", weight: 20, description: "反映公司的财务健康状况" },
          { id: "R004", name: "市场风险", weight: 15, description: "反映公司面临的市场环境风险" },
          { id: "R005", name: "政策风险", weight: 20, description: "反映公司面临的政策变动风险" }
        ],
        totalWeight: 100
      },
      {
        name: "社会评价因子",
        factors: [
          { id: "S001", name: "媒体评价", weight: 25, description: "反映公司在媒体中的评价情况" },
          { id: "S002", name: "社交媒体情绪", weight: 30, description: "反映公司在社交媒体中的情绪倾向" },
          { id: "S003", name: "分析师评级", weight: 25, description: "反映专业分析师对公司的评级" },
          { id: "S004", name: "ESG评分", weight: 20, description: "反映公司的环境、社会和治理表现" }
        ],
        totalWeight: 100
      }
    ],
    objectWeights: {
      "公司": [
        { category: "财务因子", weight: 35 },
        { category: "市场因子", weight: 25 },
        { category: "行业因子", weight: 15 },
        { category: "风险因子", weight: 15 },
        { category: "社会评价因子", weight: 10 }
      ],
      "行业": [
        { category: "财务因子", weight: 20 },
        { category: "市场因子", weight: 15 },
        { category: "行业因子", weight: 40 },
        { category: "风险因子", weight: 15 },
        { category: "社会评价因子", weight: 10 }
      ],
      "市场": [
        { category: "财务因子", weight: 15 },
        { category: "市场因子", weight: 40 },
        { category: "行业因子", weight: 20 },
        { category: "风险因子", weight: 15 },
        { category: "社会评价因子", weight: 10 }
      ]
    },
    presetTemplates: [
      { id: "T001", name: "成长型", description: "适合评估高成长性公司" },
      { id: "T002", name: "价值型", description: "适合评估稳定价值型公司" },
      { id: "T003", name: "防御型", description: "适合评估抗风险能力强的公司" },
      { id: "T004", name: "周期型", description: "适合评估周期性行业公司" }
    ],
    simulationResults: {
      beforeScore: 85.2,
      afterScore: 82.7,
      changedFactors: [
        { id: "F001", name: "净利润增长率", oldWeight: 25, newWeight: 20, impact: -1.5 },
        { id: "M003", name: "股价波动率", oldWeight: 25, newWeight: 30, impact: -1.0 }
      ]
    }
  };
  
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">对象因子权重表</h4>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <p class="text-muted mb-0">最后更新时间: ${weightData.updateTime}</p>
        <div class="btn-group">
          <button class="btn btn-outline-primary btn-sm" onclick="saveWeightSettings()">
            <i class="bi bi-save me-1"></i> 保存设置
          </button>
          <button class="btn btn-outline-primary btn-sm" onclick="exportWeightSettings('excel')">
            <i class="bi bi-file-earmark-excel me-1"></i> 导出Excel
          </button>
          <button class="btn btn-outline-success btn-sm" onclick="importFromScoreSystem()">
            <i class="bi bi-arrow-down-circle me-1"></i> 从评分系统导入
          </button>
        </div>
      </div>
      
      <div class="row mb-4">
        <div class="col-md-8">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">权重设置</h5>
                <div>
                  <div class="btn-group me-2">
                    ${weightData.objectTypes.map(type => `
                      <button class="btn btn-sm ${type === weightData.currentObjectType ? 'btn-primary' : 'btn-outline-primary'}" 
                              onclick="switchObjectType('${type}')">
                        ${type}
                      </button>
                    `).join('')}
                  </div>
                  <div class="dropdown d-inline-block">
                    <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" id="templateDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                      模板
                    </button>
                    <ul class="dropdown-menu" aria-labelledby="templateDropdown">
                      ${weightData.presetTemplates.map(template => `
                        <li><a class="dropdown-item" href="#" onclick="applyTemplate('${template.id}')">${template.name} - ${template.description}</a></li>
                      `).join('')}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-body">
              <div class="mb-4">
                <h6 class="mb-3">对象类别权重分配</h6>
                <div class="table-responsive">
                  <table class="table table-sm">
                    <thead>
                      <tr>
                        <th>因子类别</th>
                        <th style="width: 50%;">权重</th>
                        <th class="text-end">百分比</th>
                      </tr>
                    </thead>
                    <tbody>
                      ${weightData.objectWeights[weightData.currentObjectType].map(item => `
                        <tr>
                          <td>${item.category}</td>
                          <td>
                            <div class="d-flex align-items-center">
                              <input type="range" class="form-range me-2" min="0" max="100" value="${item.weight}" 
                                     oninput="updateCategoryWeight('${item.category}', this.value)">
                              <input type="number" class="form-control form-control-sm" style="width: 60px;" min="0" max="100" value="${item.weight}"
                                     oninput="updateCategoryWeight('${item.category}', this.value)">
                            </div>
                          </td>
                          <td class="text-end fw-bold">${item.weight}%</td>
                        </tr>
                      `).join('')}
                    </tbody>
                    <tfoot>
                      <tr>
                        <td>总计</td>
                        <td></td>
                        <td class="text-end fw-bold">100%</td>
                      </tr>
                    </tfoot>
                  </table>
                </div>
              </div>
              
              <div class="accordion" id="factorAccordion">
                ${weightData.factorCategories.map((category, index) => `
                  <div class="accordion-item">
                    <h2 class="accordion-header" id="heading${index}">
                      <button class="accordion-button ${index === 0 ? '' : 'collapsed'}" type="button" data-bs-toggle="collapse" 
                              data-bs-target="#collapse${index}" aria-expanded="${index === 0 ? 'true' : 'false'}" aria-controls="collapse${index}">
                        ${category.name} (总权重: ${category.totalWeight}%)
                      </button>
                    </h2>
                    <div id="collapse${index}" class="accordion-collapse collapse ${index === 0 ? 'show' : ''}" 
                         aria-labelledby="heading${index}" data-bs-parent="#factorAccordion">
                      <div class="accordion-body">
                        <div class="table-responsive">
                          <table class="table table-sm">
                            <thead>
                              <tr>
                                <th>因子ID</th>
                                <th>因子名称</th>
                                <th>描述</th>
                                <th style="width: 30%;">权重</th>
                                <th class="text-end">百分比</th>
                              </tr>
                            </thead>
                            <tbody>
                              ${category.factors.map(factor => `
                                <tr>
                                  <td>${factor.id}</td>
                                  <td>${factor.name}</td>
                                  <td><small class="text-muted">${factor.description}</small></td>
                                  <td>
                                    <div class="d-flex align-items-center">
                                      <input type="range" class="form-range me-2" min="0" max="100" value="${factor.weight}" 
                                             oninput="updateFactorWeight('${category.name}', '${factor.id}', this.value)">
                                      <input type="number" class="form-control form-control-sm" style="width: 60px;" min="0" max="100" value="${factor.weight}"
                                             oninput="updateFactorWeight('${category.name}', '${factor.id}', this.value)">
                                    </div>
                                  </td>
                                  <td class="text-end fw-bold">${factor.weight}%</td>
                                </tr>
                              `).join('')}
                            </tbody>
                            <tfoot>
                              <tr>
                                <td colspan="4">总计</td>
                                <td class="text-end fw-bold">${category.totalWeight}%</td>
                              </tr>
                            </tfoot>
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">权重可视化</h5>
            </div>
            <div class="card-body">
              <div id="category-weight-chart" style="height: 250px;"></div>
            </div>
          </div>
          
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">权重影响模拟</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label">选择模拟对象</label>
                <select class="form-select" id="simulation-object">
                  <option value="600519">贵州茅台 (600519)</option>
                  <option value="000858">五粮液 (000858)</option>
                  <option value="601318">中国平安 (601318)</option>
                  <option value="BK0438">半导体行业 (BK0438)</option>
                  <option value="BK0475">新能源行业 (BK0475)</option>
                </select>
              </div>
              <button class="btn btn-primary w-100 mb-3" onclick="runWeightSimulation()">
                <i class="bi bi-play-circle me-1"></i> 运行模拟
              </button>
              
              <div id="simulation-result" class="border rounded p-3 bg-light">
                <h6 class="mb-3">模拟结果</h6>
                <div class="d-flex justify-content-between mb-3">
                  <div class="text-center">
                    <div class="fw-bold fs-4">${weightData.simulationResults.beforeScore.toFixed(1)}</div>
                    <div class="text-muted">调整前分数</div>
                  </div>
                  <div class="text-center">
                    <i class="bi bi-arrow-right fs-4"></i>
                  </div>
                  <div class="text-center">
                    <div class="fw-bold fs-4 ${weightData.simulationResults.afterScore > weightData.simulationResults.beforeScore ? 'text-success' : 'text-danger'}">
                      ${weightData.simulationResults.afterScore.toFixed(1)}
                    </div>
                    <div class="text-muted">调整后分数</div>
                  </div>
                </div>
                
                <h6 class="mb-2">主要影响因素:</h6>
                <ul class="list-group list-group-flush">
                  ${weightData.simulationResults.changedFactors.map(factor => `
                    <li class="list-group-item px-0 py-2">
                      <div class="d-flex justify-content-between">
                        <div>${factor.name}</div>
                        <div class="${factor.impact >= 0 ? 'text-success' : 'text-danger'}">
                          ${factor.impact >= 0 ? '+' : ''}${factor.impact.toFixed(1)}
                        </div>
                      </div>
                      <div class="small text-muted">
                        权重: ${factor.oldWeight}% → ${factor.newWeight}%
                      </div>
                    </li>
                  `).join('')}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 更新容器内容
  container.innerHTML = moduleHTML;
  
  // 初始化Bootstrap组件
  initBootstrapComponents();
  
  // 初始化图表
  initWeightCharts(weightData);
  
  // 初始化交互功能
  initWeightInteractions(weightData);
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

// 初始化权重图表
function initWeightCharts(data) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createCategoryWeightChart(data);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createCategoryWeightChart(data);
  }
}

// 创建类别权重图表
function createCategoryWeightChart(data) {
  const chartDom = document.getElementById('category-weight-chart');
  if (!chartDom) return;
  
  const myChart = echarts.init(chartDom);
  
  const currentObjectWeights = data.objectWeights[data.currentObjectType];
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}%'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: {
        fontSize: 12
      }
    },
    series: [
      {
        name: '类别权重',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 5,
          borderColor: '#fff',
          borderWidth: 1
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '14',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: currentObjectWeights.map(item => ({
          name: item.category,
          value: item.weight
        }))
      }
    ]
  };
  
  myChart.setOption(option);
  
  // 响应窗口大小变化
  window.addEventListener('resize', function() {
    myChart.resize();
  });
  
  // 存储图表实例，以便后续更新
  window.categoryWeightChart = myChart;
}

// 初始化权重交互功能
function initWeightInteractions(data) {
  // 切换对象类型
  window.switchObjectType = function(type) {
    // 模拟切换对象类型，实际项目中应该重新加载数据
    alert(`已切换到${type}对象类型，正在加载相应的权重设置...`);
  };
  
  // 应用模板
  window.applyTemplate = function(templateId) {
    // 模拟应用模板，实际项目中应该加载模板数据
    const template = data.presetTemplates.find(t => t.id === templateId);
    if (template) {
      alert(`正在应用${template.name}模板: ${template.description}`);
    }
  };
  
  // 更新类别权重
  window.updateCategoryWeight = function(category, value) {
    // 模拟更新类别权重，实际项目中应该更新数据并重新计算总权重
    console.log(`更新${category}类别权重为${value}%`);
    
    // 如果图表已初始化，则更新图表
    if (window.categoryWeightChart) {
      const option = window.categoryWeightChart.getOption();
      const dataIndex = option.series[0].data.findIndex(item => item.name === category);
      if (dataIndex !== -1) {
        option.series[0].data[dataIndex].value = parseInt(value);
        window.categoryWeightChart.setOption(option);
      }
    }
  };
  
  // 更新因子权重
  window.updateFactorWeight = function(category, factorId, value) {
    // 模拟更新因子权重，实际项目中应该更新数据并重新计算总权重
    console.log(`更新${category}类别下的${factorId}因子权重为${value}%`);
  };
  
  // 运行权重模拟
  window.runWeightSimulation = function() {
    const simulationObject = document.getElementById('simulation-object');
    if (simulationObject) {
      const selectedObject = simulationObject.value;
      const selectedObjectText = simulationObject.options[simulationObject.selectedIndex].text;
      
      // 模拟运行权重模拟，实际项目中应该通过API获取模拟结果
      alert(`正在为${selectedObjectText}运行权重影响模拟...`);
      
      // 模拟更新结果UI
      setTimeout(() => {
        const simulationResult = document.getElementById('simulation-result');
        if (simulationResult) {
          // 生成随机模拟结果
          const beforeScore = Math.round((80 + Math.random() * 15) * 10) / 10;
          const scoreDiff = Math.round((Math.random() * 8 - 4) * 10) / 10;
          const afterScore = beforeScore + scoreDiff;
          
          // 更新UI
          simulationResult.innerHTML = `
            <h6 class="mb-3">模拟结果</h6>
            <div class="d-flex justify-content-between mb-3">
              <div class="text-center">
                <div class="fw-bold fs-4">${beforeScore.toFixed(1)}</div>
                <div class="text-muted">调整前分数</div>
              </div>
              <div class="text-center">
                <i class="bi bi-arrow-right fs-4"></i>
              </div>
              <div class="text-center">
                <div class="fw-bold fs-4 ${afterScore > beforeScore ? 'text-success' : 'text-danger'}">
                  ${afterScore.toFixed(1)}
                </div>
                <div class="text-muted">调整后分数</div>
              </div>
            </div>
            
            <h6 class="mb-2">主要影响因素:</h6>
            <ul class="list-group list-group-flush">
              <li class="list-group-item px-0 py-2">
                <div class="d-flex justify-content-between">
                  <div>净利润增长率</div>
                  <div class="${scoreDiff >= 0 ? 'text-success' : 'text-danger'}">
                    ${scoreDiff >= 0 ? '+' : ''}${(scoreDiff * 0.6).toFixed(1)}
                  </div>
                </div>
                <div class="small text-muted">
                  权重: 25% → ${scoreDiff >= 0 ? '30%' : '20%'}
                </div>
              </li>
              <li class="list-group-item px-0 py-2">
                <div class="d-flex justify-content-between">
                  <div>行业景气度</div>
                  <div class="${scoreDiff >= 0 ? 'text-success' : 'text-danger'}">
                    ${scoreDiff >= 0 ? '+' : ''}${(scoreDiff * 0.4).toFixed(1)}
                  </div>
                </div>
                <div class="small text-muted">
                  权重: 20% → ${scoreDiff >= 0 ? '25%' : '15%'}
                </div>
              </li>
            </ul>
          `;
        }
      }, 1000);
    }
  };
  
  // 保存权重设置
  window.saveWeightSettings = function() {
    // 模拟保存权重设置，实际项目中应该通过API保存数据
    alert('正在保存权重设置...');
    
    // 模拟保存成功
    setTimeout(() => {
      alert('权重设置已成功保存！');
    }, 800);
  };
  
  // 导出权重设置
  window.exportWeightSettings = function(format) {
    // 模拟导出功能，实际项目中应该实现真正的导出逻辑
    alert(`正在导出${format === 'excel' ? 'Excel' : 'PDF'}格式的权重设置...`);
  };
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是对象因子权重表模块，则自动加载
  if (window.location.hash === '#object-factor-weight-table') {
    loadObjectFactorWeightTable();
  }
});