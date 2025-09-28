/**
 * 全球资金流向模块
 * 大势所趋风险框架管理台
 */

// 加载全球资金流向模块
function loadGlobalCapitalFlow() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载全球资金流向数据...</p>
    </div>
  `;
  
  // 加载模块内容
  renderGlobalCapitalFlowModule(contentArea);
}

// 渲染全球资金流向模块内容
function renderGlobalCapitalFlowModule(container) {
  // 从API获取全球资金流向数据
  fetch('/api/global-capital-flow')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data) {
        const capitalFlowData = data.data;
        
        // 处理历史资金流向数据（用于图表）
        // 为了简化，我们从现有数据中提取一些用于图表展示
        const historicalData = {
          dates: ['2025-09-16', '2025-09-17', '2025-09-18', '2025-09-19', '2025-09-20', '2025-09-21', '2025-09-22'],
          regions: ['北美', '欧洲', '亚太', '中国', '日本', '印度'],
          series: [
            { name: '北美', data: [480.5, 495.2, 510.8, 502.3, 515.7, 508.4, 510.9] },
            { name: '欧洲', data: [-145.7, -158.3, -172.5, -165.8, -160.2, -172.6, -169.1] },
            { name: '亚太', data: [345.2, 352.8, 360.5, 372.1, 365.8, 370.2, 368.7] },
            { name: '中国', data: [310.5, 318.7, 325.4, 330.2, 328.7, 335.6, 333.3] },
            { name: '日本', data: [-52.3, -48.7, -45.2, -50.8, -52.1, -49.5, -47.2] },
            { name: '印度', data: [120.8, 125.3, 128.7, 130.5, 132.8, 134.6, 135.2] }
          ]
        };
        
        // 计算概览数据
        const inflowRegions = capitalFlowData.filter(item => item.netFlow >= 0).length;
        const outflowRegions = capitalFlowData.filter(item => item.netFlow < 0).length;
        const totalInflow = capitalFlowData.filter(item => item.netFlow >= 0).reduce((sum, item) => sum + item.netFlow, 0);
        const totalOutflow = capitalFlowData.filter(item => item.netFlow < 0).reduce((sum, item) => sum + Math.abs(item.netFlow), 0);
        
        // 构建模块HTML
        const moduleHTML = `
          <div class="mb-4">
            <h4 class="fw-bold text-primary mb-3">全球资金流向 <span class="badge bg-danger">实时</span></h4>
            <div class="row">
              <div class="col-md-8">
                <div class="card shadow-sm mb-4">
                  <div class="card-header bg-light d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0">全球资金流向表</h5>
                    <div class="btn-group">
                      <button class="btn btn-sm btn-outline-primary" onclick="filterCapitalFlow('all')">全部</button>
                      <button class="btn btn-sm btn-outline-success" onclick="filterCapitalFlow('inflow')">净流入</button>
                      <button class="btn btn-sm btn-outline-danger" onclick="filterCapitalFlow('outflow')">净流出</button>
                    </div>
                  </div>
                  <div class="card-body p-0">
                    <div class="table-responsive">
                      <table class="table table-hover table-striped mb-0">
                        <thead class="table-light">
                          <tr>
                            <th scope="col">ID</th>
                            <th scope="col">地区</th>
                            <th scope="col">资金流入(亿美元)</th>
                            <th scope="col">资金流出(亿美元)</th>
                            <th scope="col">净流入(亿美元)</th>
                            <th scope="col">变化率(%)</th>
                            <th scope="col">日期</th>
                          </tr>
                        </thead>
                        <tbody id="capital-flow-table">
                          ${capitalFlowData.map(item => `
                            <tr>
                              <td>${item.id}</td>
                              <td><a href="#" class="text-decoration-none" onclick="showRegionDetail('${item.region}')">${item.region}</a></td>
                              <td>${item.inflow.toFixed(1)}</td>
                              <td>${item.outflow.toFixed(1)}</td>
                              <td class="${item.netFlow >= 0 ? 'text-success' : 'text-danger'} fw-bold">${item.netFlow.toFixed(1)}</td>
                              <td>
                                <div class="d-flex align-items-center">
                                  <span class="${item.change >= 0 ? 'text-success' : 'text-danger'}">
                                    ${item.change >= 0 ? '+' : ''}${item.change.toFixed(1)}%
                                    <i class="bi bi-${item.change >= 0 ? 'arrow-up' : 'arrow-down'}"></i>
                                  </span>
                                </div>
                              </td>
                              <td>${item.date}</td>
                            </tr>
                          `).join('')}
                        </tbody>
                      </table>
                    </div>
                  </div>
                  <div class="card-footer bg-light">
                    <div class="d-flex justify-content-between align-items-center">
                      <small class="text-muted">最后更新: <span id="capital-flow-last-updated">${new Date().toLocaleString()}</span></small>
                      <div>
                        <button class="btn btn-sm btn-primary" onclick="refreshCapitalFlowData()">
                          <i class="bi bi-arrow-clockwise"></i> 刷新数据
                        </button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="exportCapitalFlowData()">
                          <i class="bi bi-download"></i> 导出
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="card shadow-sm mb-4">
                  <div class="card-header bg-light">
                    <h5 class="card-title mb-0">资金流向概览</h5>
                  </div>
                  <div class="card-body">
                    <div class="row g-3">
                      <div class="col-6">
                        <div class="border rounded p-3 text-center">
                          <h3 class="text-success mb-0">${inflowRegions}</h3>
                          <small class="text-muted">净流入地区</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="border rounded p-3 text-center">
                          <h3 class="text-danger mb-0">${outflowRegions}</h3>
                          <small class="text-muted">净流出地区</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="border rounded p-3 text-center">
                          <h3 class="text-primary mb-0">${totalInflow.toFixed(1)}</h3>
                          <small class="text-muted">净流入总额(亿美元)</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="border rounded p-3 text-center">
                          <h3 class="text-primary mb-0">${totalOutflow.toFixed(1)}</h3>
                          <small class="text-muted">净流出总额(亿美元)</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="card shadow-sm">
                  <div class="card-header bg-light">
                    <h5 class="card-title mb-0">历史资金流向趋势</h5>
                  </div>
                  <div class="card-body">
                    <div id="capital-flow-chart" style="height: 300px;"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 地区详情模态框 -->
            <div class="modal fade" id="regionDetailModal" tabindex="-1" aria-hidden="true">
              <div class="modal-dialog modal-lg">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" id="regionDetailTitle">地区资金流向详情</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body" id="regionDetailContent">
                    <!-- 详情内容将通过JS动态填充 -->
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                    <button type="button" class="btn btn-primary">生成分析报告</button>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 全球资金流向地图 -->
            <div class="card shadow-sm mt-4">
              <div class="card-header bg-light d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">全球资金流向地图</h5>
                <div class="btn-group">
                  <button class="btn btn-sm btn-outline-primary" onclick="switchMapView('net')">净流入</button>
                  <button class="btn btn-sm btn-outline-primary" onclick="switchMapView('inflow')">流入</button>
                  <button class="btn btn-sm btn-outline-primary" onclick="switchMapView('outflow')">流出</button>
                </div>
              </div>
              <div class="card-body">
                <div id="global-capital-map" style="height: 500px;">
                  <div class="text-center py-5">
                    <p class="text-muted">全球资金流向地图将在后续版本中实现</p>
                    <button class="btn btn-outline-primary" onclick="alert('地图功能将在后续版本中实现')">
                      <i class="bi bi-globe"></i> 加载地图
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
        
        // 更新容器内容
        container.innerHTML = moduleHTML;
        
        // 初始化图表
        initCapitalFlowChart(historicalData);
        
        // 加载Bootstrap的Modal组件
        loadBootstrapJS();
      } else {
        container.innerHTML = `
          <div class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill"></i> 无法加载全球资金流向数据: ${data.message || '未知错误'}
          </div>
        `;
      }
    })
    .catch(error => {
      container.innerHTML = `
        <div class="alert alert-danger">
          <i class="bi bi-exclamation-triangle-fill"></i> 请求失败: ${error.message}
        </div>
      `;
    });
}

// 初始化资金流向图表
function initCapitalFlowChart(data) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createChart(data);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createChart(data);
  }
}

// 创建图表
function createChart(data) {
  const chartDom = document.getElementById('capital-flow-chart');
  const myChart = echarts.init(chartDom);
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        let result = params[0].axisValue + '<br/>';
        params.forEach(param => {
          const color = param.value >= 0 ? 'green' : 'red';
          const sign = param.value >= 0 ? '+' : '';
          result += `${param.marker} ${param.seriesName}: <span style="color:${color}">${sign}${param.value.toFixed(1)}</span><br/>`;
        });
        return result;
      }
    },
    legend: {
      data: data.regions,
      type: 'scroll',
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: data.dates
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '{value}'
      }
    },
    series: data.series.map(item => {
      return {
        name: item.name,
        type: 'line',
        data: item.data,
        smooth: true,
        lineStyle: {
          width: 2
        },
        areaStyle: {
          opacity: 0.1
        },
        emphasis: {
          focus: 'series'
        }
      };
    })
  };
  
  myChart.setOption(option);
  
  // 响应窗口大小变化
  window.addEventListener('resize', function() {
    myChart.resize();
  });
}

// 加载Bootstrap的JS
function loadBootstrapJS() {
  if (typeof bootstrap === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js';
    document.head.appendChild(script);
  }
}

// 按类型筛选资金流向数据
function filterCapitalFlow(type) {
  // 实际应用中应该根据类型过滤数据
  console.log('按类型筛选:', type);
  alert('筛选功能将在后续版本中实现');
}

// 刷新资金流向数据
function refreshCapitalFlowData() {
  // 实际应用中应该重新请求数据
  console.log('刷新资金流向数据');
  alert('数据刷新功能将在后续版本中实现');
}

// 导出资金流向数据
function exportCapitalFlowData() {
  // 实际应用中应该生成CSV或Excel文件
  console.log('导出资金流向数据');
  alert('数据导出功能将在后续版本中实现');
}

// 切换地图视图
function switchMapView(type) {
  // 实际应用中应该切换地图显示模式
  console.log('切换地图视图:', type);
  alert('地图视图切换功能将在后续版本中实现');
}

// 显示地区详情
function showRegionDetail(region) {
  // 模拟获取地区详情数据
  const regionDetail = {
    region: region,
    date: "2025-09-22",
    inflow: 1567.8,
    outflow: 1234.5,
    netFlow: 333.3,
    change: 4.7,
    historicalData: [
      { date: "2025-09-16", netFlow: 310.5 },
      { date: "2025-09-17", netFlow: 318.7 },
      { date: "2025-09-18", netFlow: 325.4 },
      { date: "2025-09-19", netFlow: 330.2 },
      { date: "2025-09-20", netFlow: 328.7 },
      { date: "2025-09-21", netFlow: 335.6 },
      { date: "2025-09-22", netFlow: 333.3 }
    ],
    sectorFlows: [
      { sector: "科技", inflow: 456.7, outflow: 345.6, netFlow: 111.1 },
      { sector: "金融", inflow: 345.2, outflow: 298.7, netFlow: 46.5 },
      { sector: "医疗", inflow: 234.5, outflow: 187.3, netFlow: 47.2 },
      { sector: "消费", inflow: 198.7, outflow: 156.4, netFlow: 42.3 },
      { sector: "能源", inflow: 167.8, outflow: 145.2, netFlow: 22.6 },
      { sector: "工业", inflow: 123.4, outflow: 87.6, netFlow: 35.8 },
      { sector: "材料", inflow: 41.5, outflow: 13.7, netFlow: 27.8 }
    ],
    keyFactors: [
      "央行货币政策调整",
      "外商直接投资增加",
      "股票市场表现强劲",
      "债券市场收益率上升"
    ],
    outlook: "预计未来一周资金流入将保持稳定，但增速可能放缓。关注央行政策动向和全球市场波动对资金流向的影响。"
  };
  
  // 更新模态框标题
  document.getElementById('regionDetailTitle').textContent = `${region} 资金流向详情`;
  
  // 构建详情内容
  const detailContent = `
    <div class="mb-4">
      <div class="d-flex justify-content-between mb-3">
        <div>
          <span class="badge bg-${regionDetail.netFlow >= 0 ? 'success' : 'danger'} me-2">
            ${regionDetail.netFlow >= 0 ? '净流入' : '净流出'}
          </span>
          <span class="badge bg-secondary">${regionDetail.date}</span>
        </div>
        <div class="text-muted small">
          变化率: <span class="${regionDetail.change >= 0 ? 'text-success' : 'text-danger'}">
            ${regionDetail.change >= 0 ? '+' : ''}${regionDetail.change.toFixed(1)}%
          </span>
        </div>
      </div>
      
      <div class="row mb-3">
        <div class="col-md-4">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">资金流入</h6>
            </div>
            <div class="card-body text-center">
              <h3 class="text-primary">${regionDetail.inflow.toFixed(1)}</h3>
              <small class="text-muted">亿美元</small>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">资金流出</h6>
            </div>
            <div class="card-body text-center">
              <h3 class="text-primary">${regionDetail.outflow.toFixed(1)}</h3>
              <small class="text-muted">亿美元</small>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">净流入</h6>
            </div>
            <div class="card-body text-center">
              <h3 class="${regionDetail.netFlow >= 0 ? 'text-success' : 'text-danger'}">
                ${regionDetail.netFlow.toFixed(1)}
              </h3>
              <small class="text-muted">亿美元</small>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card mb-3">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">行业资金流向</h6>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-sm mb-0">
              <thead>
                <tr>
                  <th>行业</th>
                  <th>流入(亿美元)</th>
                  <th>流出(亿美元)</th>
                  <th>净流入(亿美元)</th>
                </tr>
              </thead>
              <tbody>
                ${regionDetail.sectorFlows.map(sector => `
                  <tr>
                    <td>${sector.sector}</td>
                    <td>${sector.inflow.toFixed(1)}</td>
                    <td>${sector.outflow.toFixed(1)}</td>
                    <td class="${sector.netFlow >= 0 ? 'text-success' : 'text-danger'} fw-bold">
                      ${sector.netFlow.toFixed(1)}
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      <div class="row mb-3">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">关键影响因素</h6>
            </div>
            <div class="card-body">
              <ul class="mb-0">
                ${regionDetail.keyFactors.map(factor => `<li>${factor}</li>`).join('')}
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">未来展望</h6>
            </div>
            <div class="card-body">
              <p class="mb-0">${regionDetail.outlook}</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">历史资金流向趋势</h6>
        </div>
        <div class="card-body">
          <div id="region-history-chart" style="height: 250px;"></div>
        </div>
      </div>
    </div>
  `;
  
  document.getElementById('regionDetailContent').innerHTML = detailContent;
  
  // 显示模态框
  const modal = new bootstrap.Modal(document.getElementById('regionDetailModal'));
  modal.show();
  
  // 初始化历史趋势图表
  setTimeout(() => {
    const chartDom = document.getElementById('region-history-chart');
    if (chartDom && typeof echarts !== 'undefined') {
      const myChart = echarts.init(chartDom);
      
      const option = {
        tooltip: {
          trigger: 'axis',
          formatter: function(params) {
            const param = params[0];
            const color = param.value >= 0 ? 'green' : 'red';
            const sign = param.value >= 0 ? '+' : '';
            return `${param.axisValue}<br/>${param.marker} 净流入: <span style="color:${color}">${sign}${param.value.toFixed(1)}</span> 亿美元`;
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: regionDetail.historicalData.map(item => item.date)
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value}'
          }
        },
        series: [
          {
            name: '净流入',
            type: 'line',
            data: regionDetail.historicalData.map(item => item.netFlow),
            smooth: true,
            lineStyle: {
              width: 3,
              color: '#4a90e2'
            },
            areaStyle: {
              opacity: 0.2,
              color: '#4a90e2'
            },
            markPoint: {
              data: [
                { type: 'max', name: '最大值' },
                { type: 'min', name: '最小值' }
              ]
            }
          }
        ]
      };
      
      myChart.setOption(option);
      
      // 响应窗口大小变化
      window.addEventListener('resize', function() {
        myChart.resize();
      });
    }
  }, 500);
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是全球资金流向模块，则自动加载
  if (window.location.hash === '#global-capital') {
    loadGlobalCapitalFlow();
  }
});