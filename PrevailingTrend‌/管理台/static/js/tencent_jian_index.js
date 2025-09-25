/**
 * 腾讯济安指数模块
 * 大势所趋风险框架管理台
 */

// 加载腾讯济安指数模块
function loadTencentJianIndex() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载腾讯济安指数数据...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderTencentJianIndexModule(contentArea);
  }, 800);
}

// 渲染腾讯济安指数模块内容
function renderTencentJianIndexModule(container) {
  // 模拟腾讯济安指数数据
  const jianIndexData = {
    currentIndex: 78.5,
    previousIndex: 76.2,
    change: 2.3,
    updateTime: "2025-09-23 09:30",
    historicalData: [
      { date: "2025-09-16", value: 75.8 },
      { date: "2025-09-17", value: 74.6 },
      { date: "2025-09-18", value: 75.2 },
      { date: "2025-09-19", value: 76.5 },
      { date: "2025-09-20", value: 76.8 },
      { date: "2025-09-21", value: 76.2 },
      { date: "2025-09-22", value: 77.4 },
      { date: "2025-09-23", value: 78.5 }
    ],
    components: [
      { name: "市场信心", value: 82.3, change: 3.1, weight: 0.25 },
      { name: "经济基本面", value: 76.8, change: 1.5, weight: 0.20 },
      { name: "政策环境", value: 84.5, change: 2.8, weight: 0.15 },
      { name: "风险偏好", value: 72.4, change: 1.9, weight: 0.15 },
      { name: "流动性", value: 79.2, change: 2.7, weight: 0.15 },
      { name: "外部环境", value: 68.7, change: -0.8, weight: 0.10 }
    ],
    marketSegments: [
      { name: "股票市场", value: 80.2, change: 2.8 },
      { name: "债券市场", value: 75.6, change: 1.2 },
      { name: "商品市场", value: 72.8, change: 3.5 },
      { name: "外汇市场", value: 76.4, change: 0.9 },
      { name: "房地产市场", value: 68.5, change: -1.2 }
    ],
    riskFactors: [
      { name: "通胀风险", level: "中等", trend: "上升", impact: 3.5 },
      { name: "流动性风险", level: "低", trend: "稳定", impact: 2.1 },
      { name: "信用风险", level: "中等", trend: "下降", impact: 2.8 },
      { name: "市场波动风险", level: "高", trend: "上升", impact: 4.2 },
      { name: "政策风险", level: "低", trend: "稳定", impact: 2.3 }
    ],
    outlook: {
      shortTerm: "短期内济安指数有望继续上升，市场信心增强，但需关注市场波动风险。",
      mediumTerm: "中期来看，济安指数可能在80-85区间波动，经济基本面改善将提供支撑。",
      longTerm: "长期展望保持谨慎乐观，政策环境和外部因素是主要不确定性来源。"
    }
  };
  
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">腾讯济安指数</h4>
      
      <!-- 指数概览卡片 -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card shadow-sm">
            <div class="card-header bg-light d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">济安指数概览</h5>
              <span class="badge bg-primary">实时更新</span>
            </div>
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-6 text-center">
                  <div class="display-4 fw-bold text-primary">${jianIndexData.currentIndex}</div>
                  <div class="d-flex justify-content-center align-items-center">
                    <span class="${jianIndexData.change >= 0 ? 'text-success' : 'text-danger'} me-2">
                      <i class="bi bi-${jianIndexData.change >= 0 ? 'arrow-up' : 'arrow-down'}"></i>
                      ${jianIndexData.change >= 0 ? '+' : ''}${jianIndexData.change.toFixed(1)}
                    </span>
                    <span class="text-muted small">较上期</span>
                  </div>
                  <div class="text-muted small mt-2">更新时间: ${jianIndexData.updateTime}</div>
                </div>
                <div class="col-md-6">
                  <div class="progress mb-3" style="height: 25px;">
                    <div class="progress-bar bg-danger" role="progressbar" style="width: 20%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                      <span class="fw-bold">风险</span>
                    </div>
                    <div class="progress-bar bg-warning" role="progressbar" style="width: 20%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                      <span class="fw-bold">警惕</span>
                    </div>
                    <div class="progress-bar bg-info" role="progressbar" style="width: 20%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                      <span class="fw-bold">中性</span>
                    </div>
                    <div class="progress-bar bg-success" role="progressbar" style="width: 20%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                      <span class="fw-bold">良好</span>
                    </div>
                    <div class="progress-bar bg-primary" role="progressbar" style="width: 20%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                      <span class="fw-bold">优秀</span>
                    </div>
                  </div>
                  <div class="position-relative" style="height: 30px;">
                    <div class="position-absolute" style="left: calc(${jianIndexData.currentIndex}% - 10px); top: 0;">
                      <i class="bi bi-caret-down-fill text-dark fs-4"></i>
                    </div>
                  </div>
                  <div class="d-flex justify-content-between text-muted small">
                    <span>0</span>
                    <span>20</span>
                    <span>40</span>
                    <span>60</span>
                    <span>80</span>
                    <span>100</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">历史趋势</h5>
            </div>
            <div class="card-body">
              <div id="jian-index-trend-chart" style="height: 200px;"></div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 指数构成和市场细分 -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">指数构成</h5>
            </div>
            <div class="card-body">
              <div id="jian-index-components-chart" style="height: 300px;"></div>
            </div>
            <div class="card-footer bg-light">
              <div class="table-responsive">
                <table class="table table-sm mb-0">
                  <thead>
                    <tr>
                      <th>构成因子</th>
                      <th>数值</th>
                      <th>变化</th>
                      <th>权重</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${jianIndexData.components.map(component => `
                      <tr>
                        <td>${component.name}</td>
                        <td>${component.value.toFixed(1)}</td>
                        <td class="${component.change >= 0 ? 'text-success' : 'text-danger'}">
                          ${component.change >= 0 ? '+' : ''}${component.change.toFixed(1)}
                        </td>
                        <td>${(component.weight * 100).toFixed(0)}%</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">市场细分指数</h5>
            </div>
            <div class="card-body">
              <div id="market-segments-chart" style="height: 300px;"></div>
            </div>
            <div class="card-footer bg-light">
              <div class="table-responsive">
                <table class="table table-sm mb-0">
                  <thead>
                    <tr>
                      <th>市场</th>
                      <th>指数值</th>
                      <th>变化</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${jianIndexData.marketSegments.map(segment => `
                      <tr>
                        <td>${segment.name}</td>
                        <td>${segment.value.toFixed(1)}</td>
                        <td class="${segment.change >= 0 ? 'text-success' : 'text-danger'}">
                          ${segment.change >= 0 ? '+' : ''}${segment.change.toFixed(1)}
                        </td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 风险因素和展望 -->
      <div class="row">
        <div class="col-md-6">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">风险因素</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table">
                  <thead>
                    <tr>
                      <th>风险因素</th>
                      <th>风险等级</th>
                      <th>趋势</th>
                      <th>影响程度</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${jianIndexData.riskFactors.map(factor => `
                      <tr>
                        <td>${factor.name}</td>
                        <td>
                          <span class="badge bg-${factor.level === '高' ? 'danger' : factor.level === '中等' ? 'warning' : 'success'}">
                            ${factor.level}
                          </span>
                        </td>
                        <td>
                          <span class="${factor.trend === '上升' ? 'text-danger' : factor.trend === '下降' ? 'text-success' : 'text-muted'}">
                            ${factor.trend === '上升' ? '<i class="bi bi-arrow-up"></i>' : factor.trend === '下降' ? '<i class="bi bi-arrow-down"></i>' : '<i class="bi bi-dash"></i>'}
                            ${factor.trend}
                          </span>
                        </td>
                        <td>
                          <div class="progress" style="height: 6px;">
                            <div class="progress-bar bg-${factor.impact > 4 ? 'danger' : factor.impact > 3 ? 'warning' : 'info'}" 
                                 role="progressbar" 
                                 style="width: ${factor.impact * 20}%" 
                                 aria-valuenow="${factor.impact}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="5">
                            </div>
                          </div>
                        </td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">济安指数展望</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <h6 class="fw-bold">短期展望</h6>
                <p>${jianIndexData.outlook.shortTerm}</p>
              </div>
              <div class="mb-3">
                <h6 class="fw-bold">中期展望</h6>
                <p>${jianIndexData.outlook.mediumTerm}</p>
              </div>
              <div>
                <h6 class="fw-bold">长期展望</h6>
                <p>${jianIndexData.outlook.longTerm}</p>
              </div>
            </div>
            <div class="card-footer bg-light">
              <button class="btn btn-primary" onclick="generateJianIndexReport()">
                <i class="bi bi-file-earmark-text"></i> 生成济安指数分析报告
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
  initJianIndexCharts(jianIndexData);
}

// 初始化济安指数相关图表
function initJianIndexCharts(data) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createJianIndexCharts(data);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createJianIndexCharts(data);
  }
}

// 创建济安指数相关图表
function createJianIndexCharts(data) {
  // 创建历史趋势图表
  const trendChartDom = document.getElementById('jian-index-trend-chart');
  if (trendChartDom) {
    const trendChart = echarts.init(trendChartDom);
    
    const trendOption = {
      tooltip: {
        trigger: 'axis',
        formatter: '{b}: {c}'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: data.historicalData.map(item => item.date)
      },
      yAxis: {
        type: 'value',
        min: function(value) {
          return Math.floor(value.min - 5);
        },
        max: function(value) {
          return Math.ceil(value.max + 5);
        }
      },
      series: [
        {
          name: '济安指数',
          type: 'line',
          data: data.historicalData.map(item => item.value),
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
    
    trendChart.setOption(trendOption);
    
    // 响应窗口大小变化
    window.addEventListener('resize', function() {
      trendChart.resize();
    });
  }
  
  // 创建指数构成图表
  const componentsChartDom = document.getElementById('jian-index-components-chart');
  if (componentsChartDom) {
    const componentsChart = echarts.init(componentsChartDom);
    
    const componentsOption = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center',
        data: data.components.map(item => item.name)
      },
      series: [
        {
          name: '指数构成',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '18',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: data.components.map(item => {
            return {
              name: item.name,
              value: item.value * item.weight
            };
          })
        }
      ]
    };
    
    componentsChart.setOption(componentsOption);
    
    // 响应窗口大小变化
    window.addEventListener('resize', function() {
      componentsChart.resize();
    });
  }
  
  // 创建市场细分图表
  const segmentsChartDom = document.getElementById('market-segments-chart');
  if (segmentsChartDom) {
    const segmentsChart = echarts.init(segmentsChartDom);
    
    const segmentsOption = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        min: 0,
        max: 100
      },
      yAxis: {
        type: 'category',
        data: data.marketSegments.map(item => item.name)
      },
      series: [
        {
          name: '指数值',
          type: 'bar',
          data: data.marketSegments.map(item => {
            // 根据指数值设置不同的颜色
            let color;
            if (item.value >= 80) color = '#4caf50';
            else if (item.value >= 60) color = '#2196f3';
            else if (item.value >= 40) color = '#ff9800';
            else color = '#f44336';
            
            return {
              value: item.value,
              itemStyle: {
                color: color
              },
              label: {
                show: true,
                position: 'right',
                formatter: '{c}'
              }
            };
          }),
          barWidth: '60%'
        }
      ]
    };
    
    segmentsChart.setOption(segmentsOption);
    
    // 响应窗口大小变化
    window.addEventListener('resize', function() {
      segmentsChart.resize();
    });
  }
}

// 生成济安指数分析报告
function generateJianIndexReport() {
  alert('济安指数分析报告生成功能将在后续版本中实现');
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是腾讯济安指数模块，则自动加载
  if (window.location.hash === '#tencent-jian') {
    loadTencentJianIndex();
  }
});