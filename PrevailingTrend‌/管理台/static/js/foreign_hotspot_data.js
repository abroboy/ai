/**
 * 国外热点数据模块
 * 大势所趋风险框架管理台
 */

// 加载国外热点数据模块
function loadForeignHotspotData() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载国外热点数据...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderForeignHotspotModule(contentArea);
  }, 800);
}

// 渲染国外热点数据模块内容
function renderForeignHotspotModule(container) {
  // 从API获取国外热点数据
  fetch('/api/foreign-hotspot')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data) {
        const hotspotData = data.data;
        
        // 区域分布数据（用于图表）
        const regions = [...new Set(hotspotData.map(item => item.region))];
        const regionCounts = regions.map(region => {
          return hotspotData.filter(item => item.region === region).length;
        });
        
        const regionData = {
          regions: regions,
          values: regionCounts
        };
        
        // 构建模块HTML
        const moduleHTML = buildForeignHotspotModuleHTML(hotspotData);
        container.innerHTML = moduleHTML;
        
        // 初始化图表
        initRegionChart(regionData);
        
        // 加载Bootstrap的Modal组件
        loadBootstrapJS();
        
        // 更新最后更新时间
        document.getElementById('foreign-hotspot-last-updated').textContent = new Date().toLocaleString();
      } else {
        container.innerHTML = `
          <div class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill"></i> 无法加载国外热点数据: ${data.message || '未知错误'}
          </div>
        `;
      }
    })
    .catch(error => {
      // 如果API不可用，使用模拟数据
      console.warn('API不可用，使用模拟数据:', error);
      renderWithMockData(container);
    });
}

// 使用模拟数据渲染
function renderWithMockData(container) {
  // 模拟国外热点数据
  const hotspotData = [
    { id: 1, title: "美联储加息预期升温", source: "Bloomberg", date: "2025-09-20", impact: 92, region: "北美", category: "货币政策" },
    { id: 2, title: "欧盟碳关税机制正式实施", source: "Reuters", date: "2025-09-19", impact: 85, region: "欧洲", category: "环保政策" },
    { id: 3, title: "日本央行调整收益率曲线控制政策", source: "Nikkei", date: "2025-09-18", impact: 78, region: "亚太", category: "货币政策" },
    { id: 4, title: "英国推出新一轮科技创新战略", source: "Financial Times", date: "2025-09-17", impact: 72, region: "欧洲", category: "产业政策" },
    { id: 5, title: "印度修订外商投资政策", source: "Economic Times", date: "2025-09-16", impact: 76, region: "亚太", category: "投资政策" },
    { id: 6, title: "巴西启动大规模基础设施建设计划", source: "Globo", date: "2025-09-15", impact: 68, region: "拉美", category: "基建政策" },
    { id: 7, title: "德国汽车产业转型加速", source: "Der Spiegel", date: "2025-09-14", impact: 83, region: "欧洲", category: "产业政策" },
    { id: 8, title: "沙特阿拉伯宣布新能源投资计划", source: "Al Jazeera", date: "2025-09-13", impact: 79, region: "中东", category: "能源政策" },
    { id: 9, title: "澳大利亚矿产资源税改革", source: "Australian Financial Review", date: "2025-09-12", impact: 74, region: "亚太", category: "税收政策" },
    { id: 10, title: "加拿大推出新的移民政策", source: "CBC News", date: "2025-09-11", impact: 65, region: "北美", category: "人口政策" }
  ];
  
  // 区域分布数据（用于图表）
  const regionData = {
    regions: ['北美', '欧洲', '亚太', '拉美', '中东', '非洲'],
    values: [25, 30, 28, 7, 6, 4]
  };
  
  // 构建模块HTML
  const moduleHTML = buildForeignHotspotModuleHTML(hotspotData);
  container.innerHTML = moduleHTML;
  
  // 初始化图表
  initRegionChart(regionData);
  
  // 加载Bootstrap的Modal组件
  loadBootstrapJS();
  
  // 显示数据来源提示
  const alertDiv = document.createElement('div');
  alertDiv.className = 'alert alert-warning alert-dismissible fade show mt-3';
  alertDiv.innerHTML = `
    <i class="bi bi-exclamation-triangle-fill"></i> 当前显示为模拟数据，请连接真实数据源以获取最新信息。
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  container.insertBefore(alertDiv, container.firstChild);
}

// 构建国外热点模块HTML
function buildForeignHotspotModuleHTML(hotspotData) {
  return `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">国外热点数据 <span class="badge bg-danger">实时</span></h4>
      <div class="row">
        <div class="col-md-8">
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-light d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">全球热点事件</h5>
              <div class="btn-group">
                <button class="btn btn-sm btn-outline-primary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                  区域筛选
                </button>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="#" onclick="filterByRegion('all')">全部区域</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByRegion('北美')">北美</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByRegion('欧洲')">欧洲</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByRegion('亚太')">亚太</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByRegion('拉美')">拉美</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByRegion('中东')">中东</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByRegion('非洲')">非洲</a></li>
                </ul>
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
                      <th scope="col">区域</th>
                      <th scope="col">类别</th>
                    </tr>
                  </thead>
                  <tbody id="foreign-hotspot-table">
                    ${hotspotData.map(item => `
                      <tr>
                        <td>${item.id}</td>
                        <td><a href="#" class="text-decoration-none" onclick="showForeignHotspotDetail(${item.id})">${item.title}</a></td>
                        <td>${item.source}</td>
                        <td>${item.date}</td>
                        <td>
                          <div class="progress" style="height: 6px;">
                            <div class="progress-bar bg-${getImpactColor(item.impact)}" role="progressbar" style="width: ${item.impact}%"></div>
                          </div>
                          <small class="text-muted">${item.impact}%</small>
                        </td>
                        <td><span class="badge bg-${getRegionColor(item.region)}">${item.region}</span></td>
                        <td>${item.category}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
            <div class="card-footer bg-light">
              <div class="d-flex justify-content-between align-items-center">
                <small class="text-muted">最后更新: <span id="foreign-hotspot-last-updated">${new Date().toLocaleString()}</span></small>
                <div>
                  <button class="btn btn-sm btn-primary" onclick="refreshForeignHotspotData()">
                    <i class="bi bi-arrow-clockwise"></i> 刷新数据
                  </button>
                  <button class="btn btn-sm btn-outline-secondary" onclick="exportForeignHotspotData()">
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
              <h5 class="card-title mb-0">区域分布</h5>
            </div>
            <div class="card-body">
              <div id="region-chart" style="height: 300px;"></div>
            </div>
          </div>
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">全球热点监测</h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-primary mb-0">${hotspotData.length}</h3>
                    <small class="text-muted">今日热点</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-success mb-0">${[...new Set(hotspotData.map(item => item.region))].length}</h3>
                    <small class="text-muted">区域覆盖</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-danger mb-0">${hotspotData.filter(item => item.impact >= 85).length}</h3>
                    <small class="text-muted">高影响力</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-warning mb-0">${hotspotData.filter(item => item.category.includes('政策')).length}</h3>
                    <small class="text-muted">政策相关</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 热点详情模态框 -->
      <div class="modal fade" id="foreignHotspotDetailModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="foreignHotspotDetailTitle">热点详情</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="foreignHotspotDetailContent">
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
}

// 初始化区域分布图表
function initRegionChart(data) {
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
  const chartDom = document.getElementById('region-chart');
  const myChart = echarts.init(chartDom);
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c}% ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      data: data.regions
    },
    series: [
      {
        name: '区域分布',
        type: 'pie',
        radius: ['50%', '70%'],
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
        data: data.regions.map((region, index) => {
          return {
            value: data.values[index],
            name: region
          };
        })
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

// 根据区域获取颜色
function getRegionColor(region) {
  const colorMap = {
    '北美': 'primary',
    '欧洲': 'success',
    '亚太': 'danger',
    '拉美': 'warning',
    '中东': 'info',
    '非洲': 'secondary'
  };
  return colorMap[region] || 'secondary';
}

// 按区域筛选数据
function filterByRegion(region) {
  // 实际应用中应该根据区域过滤数据
  console.log('按区域筛选:', region);
  alert('区域筛选功能将在后续版本中实现');
}

// 刷新国外热点数据
function refreshForeignHotspotData() {
  const contentArea = document.getElementById('content');
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在刷新国外热点数据...</p>
    </div>
  `;
  
  // 重新渲染模块
  renderForeignHotspotModule(contentArea);
}

// 导出国外热点数据
function exportForeignHotspotData() {
  // 实际应用中应该生成CSV或Excel文件
  console.log('导出国外热点数据');
  alert('数据导出功能将在后续版本中实现');
}

// 显示国外热点详情
function showForeignHotspotDetail(id) {
  // 模拟获取热点详情数据
  const hotspotDetail = {
    id: id,
    title: "美联储加息预期升温",
    source: "Bloomberg",
    date: "2025-09-20",
    impact: 92,
    region: "北美",
    category: "货币政策",
    content: "美联储官员在最新讲话中暗示，由于通胀压力持续，可能在未来三个月内再次加息。市场预期美联储将在11月会议上加息25个基点，年底前可能再加息一次。这一预期导致美元指数走强，全球金融市场波动加剧。",
    relatedEvents: [
      "美国8月CPI同比上涨3.2%，高于预期",
      "美联储主席鲍威尔发表鹰派言论",
      "美国劳动力市场保持韧性，失业率维持在低位"
    ],
    impactAnalysis: "美联储加息预期升温将对全球金融市场产生显著影响。一方面，美元走强可能导致新兴市场资本外流，加大这些国家的融资压力；另一方面，全球利率环境趋紧，将抑制经济增长，对高负债企业和国家形成压力。对中国而言，人民币汇率可能面临贬值压力，但也为中国出口提供一定支持。",
    marketReactions: [
      "美元指数上涨1.2%",
      "美国10年期国债收益率升至4.8%",
      "全球股市普遍下跌",
      "黄金价格下跌0.8%"
    ]
  };
  
  // 更新模态框内容
  document.getElementById('foreignHotspotDetailTitle').textContent = hotspotDetail.title;
  
  const detailContent = `
    <div class="mb-4">
      <div class="d-flex justify-content-between mb-3">
        <div>
          <span class="badge bg-${getRegionColor(hotspotDetail.region)} me-2">${hotspotDetail.region}</span>
          <span class="badge bg-secondary">${hotspotDetail.category}</span>
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
              <h6 class="card-title mb-0">相关事件</h6>
            </div>
            <div class="card-body">
              <ul class="mb-0">
                ${hotspotDetail.relatedEvents.map(event => `<li>${event}</li>`).join('')}
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">市场反应</h6>
            </div>
            <div class="card-body">
              <ul class="mb-0">
                ${hotspotDetail.marketReactions.map(reaction => `<li>${reaction}</li>`).join('')}
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
  
  document.getElementById('foreignHotspotDetailContent').innerHTML = detailContent;
  
  // 显示模态框
  const modal = new bootstrap.Modal(document.getElementById('foreignHotspotDetailModal'));
  modal.show();
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是国外热点数据模块，则自动加载
  if (window.location.hash === '#foreign-hotspot') {
    loadForeignHotspotData();
  }
});