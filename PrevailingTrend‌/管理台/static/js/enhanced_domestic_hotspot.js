/**
 * 国内热点数据模块 - 增强版
 * 大势所趋风险框架管理台
 */

// 加载国内热点数据模块
function loadEnhancedDomesticHotspotData() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载国内热点数据...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderDomesticHotspotModule(contentArea);
  }, 800);
}

// 渲染国内热点数据模块内容
function renderDomesticHotspotModule(container) {
  // 模拟热点数据
  const hotspotData = [
    { id: 1, title: "新能源汽车产业政策调整", source: "国家发改委", date: "2025-09-20", impact: 85, trend: "上升", category: "产业政策" },
    { id: 2, title: "半导体国产化进程加速", source: "工信部", date: "2025-09-19", impact: 92, trend: "上升", category: "科技创新" },
    { id: 3, title: "数字人民币试点范围扩大", source: "央行", date: "2025-09-18", impact: 78, trend: "稳定", category: "金融政策" },
    { id: 4, title: "碳达峰碳中和行动方案发布", source: "生态环境部", date: "2025-09-17", impact: 83, trend: "上升", category: "环保政策" },
    { id: 5, title: "人工智能监管框架出台", source: "网信办", date: "2025-09-16", impact: 76, trend: "稳定", category: "科技监管" },
    { id: 6, title: "跨境电商新政实施", source: "商务部", date: "2025-09-15", impact: 71, trend: "下降", category: "贸易政策" },
    { id: 7, title: "医疗健康数据安全规范发布", source: "卫健委", date: "2025-09-14", impact: 68, trend: "稳定", category: "医疗政策" },
    { id: 8, title: "教育培训行业监管加强", source: "教育部", date: "2025-09-13", impact: 74, trend: "下降", category: "教育政策" },
    { id: 9, title: "房地产市场调控政策调整", source: "住建部", date: "2025-09-12", impact: 89, trend: "上升", category: "房地产政策" },
    { id: 10, title: "农业现代化示范区建设启动", source: "农业农村部", date: "2025-09-11", impact: 65, trend: "上升", category: "农业政策" }
  ];
  
  // 热点趋势数据（用于图表）
  const trendData = {
    categories: ['产业政策', '科技创新', '金融政策', '环保政策', '科技监管', '贸易政策', '医疗政策', '教育政策', '房地产政策', '农业政策'],
    series: [
      {name: '影响力指数', data: [85, 92, 78, 83, 76, 71, 68, 74, 89, 65]},
      {name: '关注度指数', data: [80, 88, 75, 79, 72, 68, 65, 70, 86, 60]}
    ]
  };
  
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">国内热点数据 <span class="badge bg-danger">实时</span></h4>
      <div class="row">
        <div class="col-md-8">
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-light d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">热点数据列表</h5>
              <div class="btn-group">
                <button class="btn btn-sm btn-outline-primary" onclick="filterHotspotData('all')">全部</button>
                <button class="btn btn-sm btn-outline-primary" onclick="filterHotspotData('上升')">上升趋势</button>
                <button class="btn btn-sm btn-outline-primary" onclick="filterHotspotData('下降')">下降趋势</button>
              </div>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-hover table-striped mb-0">
                  <thead class="table-light">
                    <tr>
                      <th scope="col">ID</th>
                      <th scope="col">热点标题</th>
                      <th scope="col">来源</th>
                      <th scope="col">日期</th>
                      <th scope="col">影响力</th>
                      <th scope="col">趋势</th>
                      <th scope="col">类别</th>
                    </tr>
                  </thead>
                  <tbody id="hotspot-data-table">
                    ${hotspotData.map(item => `
                      <tr>
                        <td>${item.id}</td>
                        <td><a href="#" class="text-decoration-none" onclick="showHotspotDetail(${item.id})">${item.title}</a></td>
                        <td>${item.source}</td>
                        <td>${item.date}</td>
                        <td>
                          <div class="progress" style="height: 6px;">
                            <div class="progress-bar bg-${getImpactColor(item.impact)}" role="progressbar" style="width: ${item.impact}%"></div>
                          </div>
                          <small class="text-muted">${item.impact}%</small>
                        </td>
                        <td>
                          <span class="badge bg-${getTrendColor(item.trend)}">${item.trend}</span>
                        </td>
                        <td>${item.category}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
            <div class="card-footer bg-light">
              <div class="d-flex justify-content-between align-items-center">
                <small class="text-muted">最后更新: 2025-09-23 09:45</small>
                <div>
                  <button class="btn btn-sm btn-primary" onclick="refreshHotspotData()">
                    <i class="bi bi-arrow-clockwise"></i> 刷新数据
                  </button>
                  <button class="btn btn-sm btn-outline-secondary" onclick="exportHotspotData()">
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
              <h5 class="card-title mb-0">热点影响力分布</h5>
            </div>
            <div class="card-body">
              <div id="hotspot-chart" style="height: 300px;"></div>
            </div>
          </div>
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">热点数据统计</h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-primary mb-0">10</h3>
                    <small class="text-muted">今日热点</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-success mb-0">6</h3>
                    <small class="text-muted">上升趋势</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-danger mb-0">2</h3>
                    <small class="text-muted">下降趋势</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-warning mb-0">2</h3>
                    <small class="text-muted">稳定趋势</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 热点详情模态框 -->
      <div class="modal fade" id="hotspotDetailModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="hotspotDetailTitle">热点详情</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="hotspotDetailContent">
              <!-- 详情内容将通过JS动态填充 -->
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
              <button type="button" class="btn btn-primary">生成分析报告</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 更新容器内容
  container.innerHTML = moduleHTML;
  
  // 初始化图表
  initHotspotChart(trendData);
  
  // 加载Bootstrap的Modal组件
  loadBootstrapJS();
}

// 初始化热点图表
function initHotspotChart(data) {
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
  const chartDom = document.getElementById('hotspot-chart');
  const myChart = echarts.init(chartDom);
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['影响力指数', '关注度指数']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      boundaryGap: [0, 0.01]
    },
    yAxis: {
      type: 'category',
      data: data.categories
    },
    series: [
      {
        name: '影响力指数',
        type: 'bar',
        data: data.series[0].data,
        itemStyle: {
          color: '#4a90e2'
        }
      },
      {
        name: '关注度指数',
        type: 'bar',
        data: data.series[1].data,
        itemStyle: {
          color: '#50e3c2'
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

// 加载Bootstrap的JS
function loadBootstrapJS() {
  if (typeof bootstrap === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js';
    document.head.appendChild(script);
  }
}

// 根据影响力获取颜色
function getImpactColor(impact) {
  if (impact >= 85) return 'danger';
  if (impact >= 70) return 'warning';
  return 'success';
}

// 根据趋势获取颜色
function getTrendColor(trend) {
  if (trend === '上升') return 'danger';
  if (trend === '下降') return 'success';
  return 'warning';
}

// 过滤热点数据
function filterHotspotData(filter) {
  // 实际应用中应该重新请求数据或过滤现有数据
  console.log('过滤热点数据:', filter);
  alert('过滤条件: ' + filter + '\n此功能将在后续版本中实现');
}

// 刷新热点数据
function refreshHotspotData() {
  // 实际应用中应该重新请求数据
  console.log('刷新热点数据');
  alert('数据刷新功能将在后续版本中实现');
}

// 导出热点数据
function exportHotspotData() {
  // 实际应用中应该生成CSV或Excel文件
  console.log('导出热点数据');
  alert('数据导出功能将在后续版本中实现');
}

// 显示热点详情
function showHotspotDetail(id) {
  // 模拟获取热点详情数据
  const hotspotDetail = {
    id: id,
    title: "新能源汽车产业政策调整",
    source: "国家发改委",
    date: "2025-09-20",
    impact: 85,
    trend: "上升",
    category: "产业政策",
    content: "国家发改委发布《关于促进新能源汽车产业高质量发展的指导意见》，提出到2030年，新能源汽车销量占比达到汽车总销量的50%以上。政策重点支持纯电动、氢燃料电池等技术路线，同时加大充电基础设施建设力度。",
    relatedPolicies: [
      "《新能源汽车产业发展规划（2021-2035年）》",
      "《关于完善新能源汽车推广应用财政补贴政策的通知》"
    ],
    impactAnalysis: "该政策将显著推动新能源汽车产业链发展，对上游锂电池、电机、电控等核心零部件企业形成利好。同时，传统燃油车企业面临转型压力增大，需加速电动化布局。",
    riskFactors: [
      "技术路线选择风险",
      "产能过剩风险",
      "补贴退坡带来的市场波动",
      "充电基础设施建设不足"
    ]
  };
  
  // 更新模态框内容
  document.getElementById('hotspotDetailTitle').textContent = hotspotDetail.title;
  
  const detailContent = `
    <div class="mb-4">
      <div class="d-flex justify-content-between mb-3">
        <div>
          <span class="badge bg-primary me-2">${hotspotDetail.category}</span>
          <span class="badge bg-${getTrendColor(hotspotDetail.trend)}">${hotspotDetail.trend}</span>
        </div>
        <div class="text-muted small">
          来源: ${hotspotDetail.source} | 发布日期: ${hotspotDetail.date}
        </div>
      </div>
      
      <div class="alert alert-light">
        <h6 class="fw-bold">内容摘要</h6>
        <p>${hotspotDetail.content}</p>
      </div>
      
      <div class="row mb-3">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">相关政策</h6>
            </div>
            <div class="card-body">
              <ul class="mb-0">
                ${hotspotDetail.relatedPolicies.map(policy => `<li>${policy}</li>`).join('')}
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">风险因素</h6>
            </div>
            <div class="card-body">
              <ul class="mb-0">
                ${hotspotDetail.riskFactors.map(risk => `<li>${risk}</li>`).join('')}
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">影响分析</h6>
        </div>
        <div class="card-body">
          <p class="mb-0">${hotspotDetail.impactAnalysis}</p>
        </div>
      </div>
    </div>
  `;
  
  document.getElementById('hotspotDetailContent').innerHTML = detailContent;
  
  // 显示模态框
  const modal = new bootstrap.Modal(document.getElementById('hotspotDetailModal'));
  modal.show();
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是国内热点数据模块，则自动加载
  if (window.location.hash === '#domestic-hotspot') {
    loadEnhancedDomesticHotspotData();
  }
});