/**
 * 热点数据表模块
 * 大势所趋风险框架管理台 - 第二层模块
 */

// 获取当前热点数据
function getCurrentHotspotData() {
  return [
    { id: 1, name: "AI技术突破", source: "国内热点", category: "科技", heat: 95, trend: "上升", riskLevel: "中" },
    { id: 2, name: "新能源政策", source: "国外热点", category: "政策", heat: 88, trend: "上升", riskLevel: "低" },
    { id: 3, name: "金融市场波动", source: "全球资金", category: "金融", heat: 92, trend: "波动", riskLevel: "高" },
    { id: 4, name: "消费复苏", source: "国内热点", category: "经济", heat: 76, trend: "上升", riskLevel: "中低" },
    { id: 5, name: "地缘政治", source: "国外热点", category: "政治", heat: 85, trend: "上升", riskLevel: "高" },
    { id: 6, name: "医疗创新", source: "雪球论坛", category: "医疗", heat: 72, trend: "稳定", riskLevel: "中" },
    { id: 7, name: "房地产政策", source: "国内热点", category: "政策", heat: 83, trend: "波动", riskLevel: "中高" },
    { id: 8, name: "芯片短缺", source: "国外热点", category: "科技", heat: 78, trend: "下降", riskLevel: "中" },
    { id: 9, name: "碳中和进展", source: "全球资金", category: "环保", heat: 81, trend: "上升", riskLevel: "中低" },
    { id: 10, name: "数字货币", source: "雪球论坛", category: "金融", heat: 89, trend: "波动", riskLevel: "高" }
  ];
}

// 导出数据到深度分析模块
function exportToDeepAnalysis() {
  // 获取当前热点数据
  const hotspotData = getCurrentHotspotData();
  
  // 存储到全局数据总线
  window.appData = window.appData || {};
  window.appData.hotspotData = hotspotData;
  
  // 提示用户
  const toastHTML = `
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
      <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header bg-success text-white">
          <strong class="me-auto">数据导出成功</strong>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          热点数据已准备好，可以切换到"深度分析"模块进行进一步分析
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
}

// 获取当前热点数据
function getCurrentHotspotData() {
  return [
    { id: 1, name: "AI技术突破", source: "国内热点", category: "科技", heat: 95, trend: "上升", riskLevel: "中" },
    { id: 2, name: "新能源政策", source: "国外热点", category: "政策", heat: 88, trend: "上升", riskLevel: "低" },
    { id: 3, name: "金融市场波动", source: "全球资金", category: "金融", heat: 92, trend: "波动", riskLevel: "高" },
    { id: 4, name: "消费复苏", source: "国内热点", category: "经济", heat: 76, trend: "上升", riskLevel: "中低" },
    { id: 5, name: "地缘政治", source: "国外热点", category: "政治", heat: 85, trend: "上升", riskLevel: "高" },
    { id: 6, name: "医疗创新", source: "雪球论坛", category: "医疗", heat: 72, trend: "稳定", riskLevel: "中" },
    { id: 7, name: "房地产政策", source: "国内热点", category: "政策", heat: 83, trend: "波动", riskLevel: "中高" },
    { id: 8, name: "芯片短缺", source: "国外热点", category: "科技", heat: 78, trend: "下降", riskLevel: "中" },
    { id: 9, name: "碳中和进展", source: "全球资金", category: "环保", heat: 81, trend: "上升", riskLevel: "中低" },
    { id: 10, name: "数字货币", source: "雪球论坛", category: "金融", heat: 89, trend: "波动", riskLevel: "高" }
  ];
}

// 加载热点数据表模块
function loadHotspotDataTable() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载热点数据表...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderHotspotDataTableModule(contentArea);
  }, 800);
}

// 渲染热点数据表模块内容
function renderHotspotDataTableModule(container) {
  // 模拟热点数据
  const hotspotData = [
    { id: 1, name: "AI技术突破", source: "国内热点", category: "科技", heat: 95, trend: "上升", riskLevel: "中" },
    { id: 2, name: "新能源政策", source: "国外热点", category: "政策", heat: 88, trend: "上升", riskLevel: "低" },
    { id: 3, name: "金融市场波动", source: "全球资金", category: "金融", heat: 92, trend: "波动", riskLevel: "高" },
    { id: 4, name: "消费复苏", source: "国内热点", category: "经济", heat: 76, trend: "上升", riskLevel: "中低" },
    { id: 5, name: "地缘政治", source: "国外热点", category: "政治", heat: 85, trend: "上升", riskLevel: "高" },
    { id: 6, name: "医疗创新", source: "雪球论坛", category: "医疗", heat: 72, trend: "稳定", riskLevel: "中" },
    { id: 7, name: "房地产政策", source: "国内热点", category: "政策", heat: 83, trend: "波动", riskLevel: "中高" },
    { id: 8, name: "芯片短缺", source: "国外热点", category: "科技", heat: 78, trend: "下降", riskLevel: "中" },
    { id: 9, name: "碳中和进展", source: "全球资金", category: "环保", heat: 81, trend: "上升", riskLevel: "中低" },
    { id: 10, name: "数字货币", source: "雪球论坛", category: "金融", heat: 89, trend: "波动", riskLevel: "高" }
  ];
  
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">热点数据表</h4>
      
      <div class="card shadow-sm mb-4">
        <div class="card-header bg-light d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">热点数据总览</h5>
          <div class="btn-group">
            <button class="btn btn-sm btn-outline-primary" onclick="filterHotspots('all')">全部</button>
            <button class="btn btn-sm btn-outline-success" onclick="filterHotspots('rising')">上升趋势</button>
            <button class="btn btn-sm btn-outline-warning" onclick="filterHotspots('volatile')">波动</button>
            <button class="btn btn-sm btn-outline-danger" onclick="filterHotspots('highRisk')">高风险</button>
            <button class="btn btn-sm btn-primary" onclick="exportToDeepAnalysis()">
              <i class="bi bi-arrow-right-circle"></i> 导出到深度分析
            </button>
          </div>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover table-striped mb-0">
              <thead class="table-light">
                <tr>
                  <th scope="col">ID</th>
                  <th scope="col">热点名称</th>
                  <th scope="col">来源</th>
                  <th scope="col">类别</th>
                  <th scope="col">热度</th>
                  <th scope="col">趋势</th>
                  <th scope="col">风险等级</th>
                </tr>
              </thead>
              <tbody id="hotspot-table">
                ${hotspotData.map(hotspot => `
                  <tr>
                    <td>${hotspot.id}</td>
                    <td><a href="#" class="text-decoration-none" onclick="showHotspotDetail(${hotspot.id})">${hotspot.name}</a></td>
                    <td>${hotspot.source}</td>
                    <td>${hotspot.category}</td>
                    <td>
                      <div class="progress" style="height: 20px;">
                        <div class="progress-bar bg-${hotspot.heat > 90 ? 'danger' : hotspot.heat > 80 ? 'warning' : 'success'}" 
                             role="progressbar" 
                             style="width: ${hotspot.heat}%" 
                             aria-valuenow="${hotspot.heat}" 
                             aria-valuemin="0" 
                             aria-valuemax="100">
                          ${hotspot.heat}
                        </div>
                      </div>
                    </td>
                    <td>
                      <span class="badge bg-${hotspot.trend === '上升' ? 'success' : hotspot.trend === '下降' ? 'danger' : 'warning'}">
                        ${hotspot.trend}
                      </span>
                    </td>
                    <td>
                      <span class="badge bg-${hotspot.riskLevel === '低' ? 'success' : hotspot.riskLevel === '中' ? 'warning' : hotspot.riskLevel === '中低' ? 'info' : 'danger'}">
                        ${hotspot.riskLevel}
                      </span>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
        <div class="card-footer bg-light">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <span class="badge bg-secondary me-2">数据来源:</span>
              <span class="badge bg-info me-2">国内热点</span>
              <span class="badge bg-info me-2">国外热点</span>
              <span class="badge bg-info">雪球论坛</span>
            </div>
            <div>
              <button class="btn btn-sm btn-primary" onclick="refreshHotspotData()">
                <i class="bi bi-arrow-clockwise"></i> 刷新数据
              </button>
              <button class="btn btn-sm btn-outline-secondary ms-2" onclick="exportHotspotData()">
                <i class="bi bi-download"></i> 导出
              </button>
            </div>
          </div>
        </div>
          <div class="d-flex justify-content-between align-items-center">
            <small class="text-muted">共 ${hotspotData.length} 条热点数据</small>
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
      
      <div class="row">
        <div class="col-md-6">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">热点来源分布</h5>
            </div>
            <div class="card-body">
              <div id="hotspot-source-chart" style="height: 300px;"></div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">热点类别分布</h5>
            </div>
            <div class="card-body">
              <div id="hotspot-category-chart" style="height: 300px;"></div>
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
  initHotspotCharts(hotspotData);
}

// 初始化热点数据相关图表
function initHotspotCharts(hotspots) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createHotspotCharts(hotspots);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createHotspotCharts(hotspots);
  }
}

// 创建热点数据相关图表
function createHotspotCharts(hotspots) {
  // 热点来源分布数据
  const sourceData = {};
  hotspots.forEach(hotspot => {
    if (!sourceData[hotspot.source]) {
      sourceData[hotspot.source] = 0;
    }
    sourceData[hotspot.source]++;
  });
  
  // 热点类别分布数据
  const categoryData = {};
  hotspots.forEach(hotspot => {
    if (!categoryData[hotspot.category]) {
      categoryData[hotspot.category] = 0;
    }
    categoryData[hotspot.category]++;
  });
  
  // 创建热点来源分布图表
  const sourceChartDom = document.getElementById('hotspot-source-chart');
  if (sourceChartDom) {
    const sourceChart = echarts.init(sourceChartDom);
    
    const sourceOption = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center',
        data: Object.keys(sourceData)
      },
      series: [
        {
          name: '热点来源',
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
          data: Object.keys(sourceData).map(source => {
            return {
              name: source,
              value: sourceData[source]
            };
          })
        }
      ]
    };
    
    sourceChart.setOption(sourceOption);
    
    // 响应窗口大小变化
    window.addEventListener('resize', function() {
      sourceChart.resize();
    });
  }
  
  // 创建热点类别分布图表
  const categoryChartDom = document.getElementById('hotspot-category-chart');
  if (categoryChartDom) {
    const categoryChart = echarts.init(categoryChartDom);
    
    const categoryOption = {
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
        type: 'category',
        data: Object.keys(categoryData)
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '热点数量',
          type: 'bar',
          data: Object.keys(categoryData).map(category => {
            return {
              value: categoryData[category],
              itemStyle: {
                color: getCategoryColor(category)
              }
            };
          }),
          barWidth: '60%'
        }
      ]
    };
    
    categoryChart.setOption(categoryOption);
    
    // 响应窗口大小变化
    window.addEventListener('resize', function() {
      categoryChart.resize();
    });
  }
}

// 获取类别对应的颜色
function getCategoryColor(category) {
  const colors = {
    '科技': '#4a90e2',
    '政策': '#7ed321',
    '金融': '#f5a623',
    '经济': '#bd10e0',
    '政治': '#d0021b',
    '医疗': '#50e3c2',
    '环保': '#4a4a4a'
  };
  return colors[category] || '#8b572a';
}

// 按条件筛选热点数据
function filterHotspots(type) {
  // 实际应用中应该根据类型过滤数据
  console.log('按条件筛选热点数据:', type);
  alert('筛选功能将在后续版本中实现');
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
function showHotspotDetail(hotspotId) {
  // 模拟获取热点详情数据
  const hotspotDetail = {
    id: hotspotId,
    name: "示例热点",
    source: "国内热点",
    category: "科技",
    heat: 95,
    trend: "上升",
    riskLevel: "中",
    description: "这是一个示例热点描述，详细说明了该热点的背景、影响范围和潜在风险。",
    relatedCompanies: [
      { name: "腾讯控股", impact: "正面", relevance: 85 },
      { name: "阿里巴巴", impact: "中性", relevance: 78 },
      { name: "百度", impact: "正面", relevance: 72 }
    ],
    timeline: [
      { date: "2025-09-15", event: "首次报道", impact: "初始" },
      { date: "2025-09-18", event: "政策响应", impact: "增强" },
      { date: "2025-09-20", event: "市场反应", impact: "扩散" }
    ],
    riskAnalysis: "该热点主要风险在于技术不确定性，但市场接受度较高，整体风险可控。"
  };
  
  // 更新模态框标题
  document.getElementById('hotspotDetailTitle').textContent = `${hotspotDetail.name} 详情`;
  
  // 构建详情内容
  const detailContent = `
    <div class="mb-4">
      <div class="d-flex justify-content-between mb-3">
        <div>
          <span class="badge bg-${hotspotDetail.riskLevel === '低' ? 'success' : hotspotDetail.riskLevel === '中' ? 'warning' : hotspotDetail.riskLevel === '中低' ? 'info' : 'danger'} me-2">
            ${hotspotDetail.riskLevel}风险
          </span>
          <span class="badge bg-secondary">ID: ${hotspotDetail.id}</span>
        </div>
        <div class="text-muted small">
          来源: ${hotspotDetail.source} | 类别: ${hotspotDetail.category}
        </div>
      </div>
      
      <div class="row mb-3">
        <div class="col-md-4">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">热度</h6>
            </div>
            <div class="card-body text-center">
              <div class="display-4 fw-bold text-primary">${hotspotDetail.heat}</div>
              <small class="text-muted">热度指数</small>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">趋势</h6>
            </div>
            <div class="card-body text-center">
              <div class="display-4">
                <span class="badge bg-${hotspotDetail.trend === '上升' ? 'success' : hotspotDetail.trend === '下降' ? 'danger' : 'warning'} fs-4">
                  ${hotspotDetail.trend}
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">相关公司</h6>
            </div>
            <div class="card-body">
              <div class="d-flex justify-content-between small mb-1">
                <span>${hotspotDetail.relatedCompanies[0].name}:</span>
                <span>${hotspotDetail.relatedCompanies[0].impact} (${hotspotDetail.relatedCompanies[0].relevance})</span>
              </div>
              <div class="d-flex justify-content-between small mb-1">
                <span>${hotspotDetail.relatedCompanies[1].name}:</span>
                <span>${hotspotDetail.relatedCompanies[1].impact} (${hotspotDetail.relatedCompanies[1].relevance})</span>
              </div>
              <div class="d-flex justify-content-between small">
                <span>${hotspotDetail.relatedCompanies[2].name}:</span>
                <span>${hotspotDetail.relatedCompanies[2].impact} (${hotspotDetail.relatedCompanies[2].relevance})</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card mb-3">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">热点描述</h6>
        </div>
        <div class="card-body">
          <p>${hotspotDetail.description}</p>
        </div>
      </div>
      
      <div class="card mb-3">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">时间线</h6>
        </div>
        <div class="card-body">
          <ul class="list-group list-group-flush">
            ${hotspotDetail.timeline.map(event => `
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <span class="badge bg-secondary me-2">${event.date}</span>
                  ${event.event}
                </div>
                <span class="badge bg-${event.impact === '增强' ? 'success' : event.impact === '扩散' ? 'warning' : 'secondary'}">
                  ${event.impact}
                </span>
              </li>
            `).join('')}
          </ul>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">风险分析</h6>
        </div>
        <div class="card-body">
          <p>${hotspotDetail.riskAnalysis}</p>
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
  // 如果当前页面是热点数据表模块，则自动加载
  if (window.location.hash === '#hotspot-data') {
    loadHotspotDataTable();
  }
});