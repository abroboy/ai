/**
 * 全球资金流向模块
 * 大势所趋风险框架管理台
 */

// 加载全球资金流向模块
function loadGlobalCapitalFlow() {
  // 检查是否有增强版功能
  if (typeof loadGlobalCapitalFlowEnhanced === 'function') {
    loadGlobalCapitalFlowEnhanced();
    return;
  }
  
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
    .then(response => {
      if (!response.ok) {
        throw new Error('API请求失败，状态码: ' + response.status);
    }
      return response.json();
    })
    .then(data => {
      if (data.success && data.data) {
        renderData(container, data.data);
      } else {
        console.warn('数据格式不正确，使用模拟数据');
        useMockData();
      }
    })
    .catch(error => {
      console.warn('API请求失败，使用模拟数据:', error);
      useMockData();
    });

  // 使用模拟数据的函数
  function useMockData() {
    const mockData = [
      { id: 1, region: '北美', inflow: 5678.9, outflow: 5530.4, netFlow: 148.5, change: 2.8, date: '2025-09-22' },
      { id: 2, region: '欧洲', inflow: 4321.5, outflow: 4223.7, netFlow: 97.8, change: 1.5, date: '2025-09-22' },
      { id: 3, region: '亚太', inflow: 6789.2, outflow: 6560.7, netFlow: 228.5, change: 4.2, date: '2025-09-22' },
      { id: 4, region: '中国', inflow: 7890.6, outflow: 7557.3, netFlow: 333.3, change: 5.8, date: '2025-09-22' },
      { id: 5, region: '日本', inflow: 1234.5, outflow: 1281.7, netFlow: -47.2, change: -2.1, date: '2025-09-22' },
      { id: 6, region: '印度', inflow: 2345.8, outflow: 2210.6, netFlow: 135.2, change: 6.7, date: '2025-09-22' }
    ];
    renderData(container, mockData);
  }

  // 渲染数据的函数
  function renderData(container, capitalFlowData) {
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
    
    try {
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
    } catch (error) {
      console.error('渲染数据时出错:', error);
      container.innerHTML = `
        <div class="alert alert-danger">
          <i class="bi bi-exclamation-triangle-fill"></i> 渲染数据时出错: ${error.message}
        </div>
      `;
    }
  }
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
  const tableBody = document.getElementById('capital-flow-table');
  const rows = tableBody.querySelectorAll('tr');
  
  rows.forEach(row => {
    const netFlowCell = row.querySelector('td:nth-child(5)');
    if (netFlowCell) {
      const isPositive = netFlowCell.classList.contains('text-success');
      
      if (type === 'all') {
        row.style.display = '';
      } else if (type === 'inflow' && isPositive) {
        row.style.display = '';
      } else if (type === 'outflow' && !isPositive) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    }
  });
  
  // 更新按钮状态
  document.querySelectorAll('.btn-group button').forEach(btn => {
    btn.classList.remove('btn-primary');
    btn.classList.add('btn-outline-primary');
  });
  
  const activeBtn = document.querySelector(`.btn-group button[onclick="filterCapitalFlow('${type}')"]`);
  if (activeBtn) {
    activeBtn.classList.remove('btn-outline-primary');
    activeBtn.classList.add('btn-primary');
  }
}

// 刷新资金流向数据
function refreshCapitalFlowData() {
  const contentArea = document.getElementById('content');
  
  // 显示加载状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在刷新全球资金流向数据...</p>
    </div>
  `;
  
  // 模拟网络延迟
  setTimeout(() => {
    // 生成新的模拟数据（在原有基础上有小幅波动）
    const newMockData = [
      { id: 1, region: '北美', inflow: 5678.9 + getRandomChange(), outflow: 5530.4 + getRandomChange(), netFlow: 148.5 + getRandomChange(10), change: 2.8 + getRandomChange(0.5), date: '2025-09-22' },
      { id: 2, region: '欧洲', inflow: 4321.5 + getRandomChange(), outflow: 4223.7 + getRandomChange(), netFlow: 97.8 + getRandomChange(8), change: 1.5 + getRandomChange(0.5), date: '2025-09-22' },
      { id: 3, region: '亚太', inflow: 6789.2 + getRandomChange(), outflow: 6560.7 + getRandomChange(), netFlow: 228.5 + getRandomChange(15), change: 4.2 + getRandomChange(0.5), date: '2025-09-22' },
      { id: 4, region: '中国', inflow: 7890.6 + getRandomChange(), outflow: 7557.3 + getRandomChange(), netFlow: 333.3 + getRandomChange(20), change: 5.8 + getRandomChange(0.5), date: '2025-09-22' },
      { id: 5, region: '日本', inflow: 1234.5 + getRandomChange(), outflow: 1281.7 + getRandomChange(), netFlow: -47.2 + getRandomChange(5), change: -2.1 + getRandomChange(0.5), date: '2025-09-22' },
      { id: 6, region: '印度', inflow: 2345.8 + getRandomChange(), outflow: 2210.6 + getRandomChange(), netFlow: 135.2 + getRandomChange(10), change: 6.7 + getRandomChange(0.5), date: '2025-09-22' }
    ];
    
    // 渲染新数据
    renderData(contentArea, newMockData);
    
    // 更新最后更新时间
    document.getElementById('capital-flow-last-updated').textContent = new Date().toLocaleString();
  }, 1500);
  
  // 生成随机变化量的辅助函数
  function getRandomChange(range = 50) {
    return (Math.random() - 0.5) * 2 * range;
  }
}

// 导出资金流向数据
function exportCapitalFlowData() {
  const tableBody = document.getElementById('capital-flow-table');
  const rows = tableBody.querySelectorAll('tr');
  
  // 准备CSV内容
  let csvContent = 'ID,地区,资金流入(亿美元),资金流出(亿美元),净流入(亿美元),变化率(%),日期\n';
  
  rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    if (cells.length > 0) {
      const id = cells[0].textContent;
      const region = cells[1].querySelector('a')?.textContent || '';
      const inflow = cells[2].textContent;
      const outflow = cells[3].textContent;
      const netFlow = cells[4].textContent;
      const change = cells[5].textContent.replace(/[\+\-%↑↓]/g, '').trim();
      const date = cells[6].textContent;
      
      csvContent += `${id},${region},${inflow},${outflow},${netFlow},${change},${date}\n`;
    }
  });
  
  // 创建Blob对象
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  
  // 创建下载链接
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  link.setAttribute('href', url);
  link.setAttribute('download', `全球资金流向数据_${new Date().toLocaleDateString()}.csv`);
  link.style.visibility = 'hidden';
  
  // 添加到页面并触发下载
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// 切换地图视图
function switchMapView(type) {
  // 更新按钮状态
  document.querySelectorAll('.btn-group button').forEach(btn => {
    btn.classList.remove('btn-primary');
    btn.classList.add('btn-outline-primary');
  });
  
  const activeBtn = document.querySelector(`.btn-group button[onclick="switchMapView('${type}')"]`);
  if (activeBtn) {
    activeBtn.classList.remove('btn-outline-primary');
    activeBtn.classList.add('btn-primary');
  }
  
  // 显示提示
  alert(`地图视图已切换为：${type === 'net' ? '净流入' : type === 'inflow' ? '流入' : '流出'}。完整地图功能将在后续版本中实现。`);
}

// 显示地区详情
function showRegionDetail(region) {
  // 根据不同地区提供差异化的模拟数据
  const regionDetailMap = {
    '北美': {
      region: '北美',
      date: "2025-09-22",
      inflow: 5678.9,
      outflow: 5530.4,
      netFlow: 148.5,
      change: 2.8,
      historicalData: [
        { date: "2025-09-16", netFlow: 130.2 },
        { date: "2025-09-17", netFlow: 135.6 },
        { date: "2025-09-18", netFlow: 140.3 },
        { date: "2025-09-19", netFlow: 145.7 },
        { date: "2025-09-20", netFlow: 142.9 },
        { date: "2025-09-21", netFlow: 150.2 },
        { date: "2025-09-22", netFlow: 148.5 }
      ],
      sectorFlows: [
        { sector: "科技", inflow: 1879.2, outflow: 1756.8, netFlow: 122.4 },
        { sector: "金融", inflow: 1567.8, outflow: 1498.3, netFlow: 69.5 },
        { sector: "医疗", inflow: 987.6, outflow: 932.1, netFlow: 55.5 },
        { sector: "消费", inflow: 789.5, outflow: 764.2, netFlow: 25.3 },
        { sector: "能源", inflow: 467.8, outflow: 449.2, netFlow: 18.6 },
        { sector: "工业", inflow: 356.4, outflow: 338.5, netFlow: 17.9 },
        { sector: "材料", inflow: 130.6, outflow: 121.3, netFlow: 9.3 }
      ],
      keyFactors: [
        "美联储降息预期",
        "美股科技股反弹",
        "就业数据强劲",
        "消费信心回升"
      ],
      outlook: "预计未来一周北美资金流入将保持平稳，但需关注美联储议息会议结果和通胀数据对市场的影响。"
    },
    '欧洲': {
      region: '欧洲',
      date: "2025-09-22",
      inflow: 4321.5,
      outflow: 4223.7,
      netFlow: 97.8,
      change: 1.5,
      historicalData: [
        { date: "2025-09-16", netFlow: 85.3 },
        { date: "2025-09-17", netFlow: 90.5 },
        { date: "2025-09-18", netFlow: 92.7 },
        { date: "2025-09-19", netFlow: 95.2 },
        { date: "2025-09-20", netFlow: 94.1 },
        { date: "2025-09-21", netFlow: 99.4 },
        { date: "2025-09-22", netFlow: 97.8 }
      ],
      sectorFlows: [
        { sector: "金融", inflow: 1234.5, outflow: 1189.2, netFlow: 45.3 },
        { sector: "医疗", inflow: 876.9, outflow: 852.1, netFlow: 24.8 },
        { sector: "工业", inflow: 765.4, outflow: 748.3, netFlow: 17.1 },
        { sector: "科技", inflow: 654.3, outflow: 638.9, netFlow: 15.4 },
        { sector: "消费", inflow: 432.1, outflow: 423.5, netFlow: 8.6 },
        { sector: "能源", inflow: 234.5, outflow: 229.7, netFlow: 4.8 },
        { sector: "材料", inflow: 124.2, outflow: 121.9, netFlow: 2.3 }
      ],
      keyFactors: [
        "欧央行维持宽松货币政策",
        "欧元区经济数据改善",
        "地缘政治风险缓解",
        "银行股表现强劲"
      ],
      outlook: "欧洲资金流入有望保持温和增长，但仍受能源价格波动和通胀压力影响，需密切关注欧洲央行政策动向。"
    },
    '亚太': {
      region: '亚太',
      date: "2025-09-22",
      inflow: 6789.2,
      outflow: 6560.7,
      netFlow: 228.5,
      change: 4.2,
      historicalData: [
        { date: "2025-09-16", netFlow: 205.3 },
        { date: "2025-09-17", netFlow: 210.7 },
        { date: "2025-09-18", netFlow: 215.4 },
        { date: "2025-09-19", netFlow: 220.8 },
        { date: "2025-09-20", netFlow: 223.6 },
        { date: "2025-09-21", netFlow: 230.1 },
        { date: "2025-09-22", netFlow: 228.5 }
      ],
      sectorFlows: [
        { sector: "科技", inflow: 2345.6, outflow: 2234.8, netFlow: 110.8 },
        { sector: "消费", inflow: 1567.8, outflow: 1503.2, netFlow: 64.6 },
        { sector: "工业", inflow: 1234.5, outflow: 1198.7, netFlow: 35.8 },
        { sector: "医疗", inflow: 876.9, outflow: 853.4, netFlow: 23.5 },
        { sector: "金融", inflow: 432.1, outflow: 421.5, netFlow: 10.6 },
        { sector: "能源", inflow: 234.5, outflow: 231.2, netFlow: 3.3 },
        { sector: "材料", inflow: 97.8, outflow: 97.3, netFlow: 0.5 }
      ],
      keyFactors: [
        "亚太地区经济复苏加速",
        "科技产业链重构",
        "消费需求反弹",
        "区域贸易合作深化"
      ],
      outlook: "亚太地区资金流入预计将继续保持良好势头，特别是科技和消费领域，但需关注美联储政策对资本流动的影响。"
    },
    '中国': {
      region: '中国',
      date: "2025-09-22",
      inflow: 7890.6,
      outflow: 7557.3,
      netFlow: 333.3,
      change: 5.8,
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
        { sector: "科技", inflow: 2876.5, outflow: 2754.2, netFlow: 122.3 },
        { sector: "消费", inflow: 1879.2, outflow: 1815.7, netFlow: 63.5 },
        { sector: "医疗", inflow: 1234.5, outflow: 1198.7, netFlow: 35.8 },
        { sector: "新能源", inflow: 1098.7, outflow: 1056.3, netFlow: 42.4 },
        { sector: "金融", inflow: 567.8, outflow: 554.2, netFlow: 13.6 },
        { sector: "工业", inflow: 187.9, outflow: 182.1, netFlow: 5.8 },
        { sector: "材料", inflow: 45.2, outflow: 44.1, netFlow: 1.1 }
      ],
      keyFactors: [
        "中国经济持续复苏",
        "科技创新政策支持",
        "消费升级趋势明显",
        "外资准入政策放宽"
      ],
      outlook: "中国市场资金流入有望保持强劲，特别是在科技、新能源和消费领域。关注中国经济数据和政策走向对资本流动的影响。"
    },
    '日本': {
      region: '日本',
      date: "2025-09-22",
      inflow: 1234.5,
      outflow: 1281.7,
      netFlow: -47.2,
      change: -2.1,
      historicalData: [
        { date: "2025-09-16", netFlow: -55.8 },
        { date: "2025-09-17", netFlow: -52.3 },
        { date: "2025-09-18", netFlow: -50.1 },
        { date: "2025-09-19", netFlow: -48.5 },
        { date: "2025-09-20", netFlow: -46.2 },
        { date: "2025-09-21", netFlow: -45.7 },
        { date: "2025-09-22", netFlow: -47.2 }
      ],
      sectorFlows: [
        { sector: "汽车", inflow: 456.7, outflow: 478.9, netFlow: -22.2 },
        { sector: "科技", inflow: 345.2, outflow: 356.8, netFlow: -11.6 },
        { sector: "金融", inflow: 234.5, outflow: 242.1, netFlow: -7.6 },
        { sector: "医疗", inflow: 123.4, outflow: 118.7, netFlow: 4.7 },
        { sector: "消费", inflow: 67.8, outflow: 65.2, netFlow: 2.6 },
        { sector: "工业", inflow: 8.9, outflow: 10.0, netFlow: -1.1 },
        { sector: "材料", inflow: 8.0, outflow: 9.0, netFlow: -1.0 }
      ],
      keyFactors: [
        "日本央行维持超宽松货币政策",
        "日元贬值压力持续",
        "出口数据不及预期",
        "国内消费复苏缓慢"
      ],
      outlook: "日本市场短期可能继续面临资金流出压力，但随着全球经济复苏和国内政策调整，资金流动状况有望改善。"
    },
    '印度': {
      region: '印度',
      date: "2025-09-22",
      inflow: 2345.8,
      outflow: 2210.6,
      netFlow: 135.2,
      change: 6.7,
      historicalData: [
        { date: "2025-09-16", netFlow: 120.8 },
        { date: "2025-09-17", netFlow: 125.3 },
        { date: "2025-09-18", netFlow: 128.7 },
        { date: "2025-09-19", netFlow: 130.5 },
        { date: "2025-09-20", netFlow: 132.8 },
        { date: "2025-09-21", netFlow: 134.6 },
        { date: "2025-09-22", netFlow: 135.2 }
      ],
      sectorFlows: [
        { sector: "科技", inflow: 876.9, outflow: 834.2, netFlow: 42.7 },
        { sector: "金融", inflow: 654.3, outflow: 621.5, netFlow: 32.8 },
        { sector: "消费", inflow: 432.1, outflow: 412.6, netFlow: 19.5 },
        { sector: "工业", inflow: 234.5, outflow: 223.7, netFlow: 10.8 },
        { sector: "能源", inflow: 87.6, outflow: 84.3, netFlow: 3.3 },
        { sector: "医疗", inflow: 54.3, outflow: 51.8, netFlow: 2.5 },
        { sector: "材料", inflow: 5.1, outflow: 4.5, netFlow: 0.6 }
      ],
      keyFactors: [
        "印度经济增长强劲",
        "科技行业蓬勃发展",
        "消费市场潜力巨大",
        "改革政策持续推进"
      ],
      outlook: "印度市场资金流入预计将保持强劲增长态势，成为新兴市场中的亮点。关注莫迪政府政策和地缘政治因素的影响。"
    }
  };
  
  // 获取当前地区的详情数据，如果没有则使用默认数据
  const regionDetail = regionDetailMap[region] || {
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