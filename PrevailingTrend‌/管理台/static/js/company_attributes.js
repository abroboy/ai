/**
 * 公司属性表模块
 * 大势所趋风险框架管理台 - 第二层模块
 */

// 加载公司属性表模块
function loadCompanyAttributes() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载公司属性表数据...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderCompanyAttributesModule(contentArea);
  }, 800);
}

// 渲染公司属性表模块内容
function renderCompanyAttributesModule(container) {
  // 模拟公司属性数据
  const companies = [
    { id: 1, name: "腾讯控股", industry: "互联网", region: "深圳", marketCap: 3500, employees: 108000, riskLevel: "中低" },
    { id: 2, name: "阿里巴巴", industry: "互联网", region: "杭州", marketCap: 2800, employees: 254000, riskLevel: "中" },
    { id: 3, name: "贵州茅台", industry: "白酒", region: "贵州", marketCap: 2200, employees: 42000, riskLevel: "低" },
    { id: 4, name: "中国平安", industry: "金融", region: "深圳", marketCap: 1800, employees: 364000, riskLevel: "中高" },
    { id: 5, name: "宁德时代", industry: "新能源", region: "福建", marketCap: 1200, employees: 88000, riskLevel: "中" },
    { id: 6, name: "美团", industry: "互联网", region: "北京", marketCap: 950, employees: 92000, riskLevel: "中高" },
    { id: 7, name: "京东", industry: "电商", region: "北京", marketCap: 850, employees: 460000, riskLevel: "中" },
    { id: 8, name: "中国移动", industry: "通信", region: "北京", marketCap: 1500, employees: 456000, riskLevel: "低" },
    { id: 9, name: "比亚迪", industry: "汽车", region: "深圳", marketCap: 1100, employees: 288000, riskLevel: "中" },
    { id: 10, name: "拼多多", industry: "电商", region: "上海", marketCap: 900, employees: 12000, riskLevel: "高" }
  ];
  
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">公司属性表</h4>
      
      <div class="card shadow-sm mb-4">
        <div class="card-header bg-light d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">公司属性总览</h5>
          <div class="btn-group">
            <button class="btn btn-sm btn-outline-primary" onclick="filterCompanies('all')">全部</button>
            <button class="btn btn-sm btn-outline-success" onclick="filterCompanies('lowRisk')">低风险</button>
            <button class="btn btn-sm btn-outline-warning" onclick="filterCompanies('mediumRisk')">中风险</button>
            <button class="btn btn-sm btn-outline-danger" onclick="filterCompanies('highRisk')">高风险</button>
          </div>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover table-striped mb-0">
              <thead class="table-light">
                <tr>
                  <th scope="col">ID</th>
                  <th scope="col">公司名称</th>
                  <th scope="col">行业</th>
                  <th scope="col">地区</th>
                  <th scope="col">市值(亿美元)</th>
                  <th scope="col">员工数</th>
                  <th scope="col">风险等级</th>
                </tr>
              </thead>
              <tbody id="company-table">
                ${companies.map(company => `
                  <tr>
                    <td>${company.id}</td>
                    <td><a href="#" class="text-decoration-none" onclick="showCompanyDetail(${company.id})">${company.name}</a></td>
                    <td>${company.industry}</td>
                    <td>${company.region}</td>
                    <td>${company.marketCap}</td>
                    <td>${company.employees.toLocaleString()}</td>
                    <td>
                      <span class="badge bg-${company.riskLevel === '低' ? 'success' : company.riskLevel === '中' ? 'warning' : company.riskLevel === '中低' ? 'info' : 'danger'}">
                        ${company.riskLevel}
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
            <small class="text-muted">共 ${companies.length} 家公司</small>
            <div>
              <button class="btn btn-sm btn-primary" onclick="refreshCompanyData()">
                <i class="bi bi-arrow-clockwise"></i> 刷新数据
              </button>
              <button class="btn btn-sm btn-outline-secondary" onclick="exportCompanyData()">
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
              <h5 class="card-title mb-0">行业分布</h5>
            </div>
            <div class="card-body">
              <div id="industry-chart" style="height: 300px;"></div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">风险等级分布</h5>
            </div>
            <div class="card-body">
              <div id="risk-chart" style="height: 300px;"></div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 公司详情模态框 -->
      <div class="modal fade" id="companyDetailModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="companyDetailTitle">公司详情</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="companyDetailContent">
              <!-- 详情内容将通过JS动态填充 -->
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
              <button type="button" class="btn btn-primary">生成风险报告</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 更新容器内容
  container.innerHTML = moduleHTML;
  
  // 初始化图表
  initCompanyCharts(companies);
}

// 初始化公司属性相关图表
function initCompanyCharts(companies) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createCompanyCharts(companies);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createCompanyCharts(companies);
  }
}

// 创建公司属性相关图表
function createCompanyCharts(companies) {
  // 行业分布数据
  const industryData = {};
  companies.forEach(company => {
    if (!industryData[company.industry]) {
      industryData[company.industry] = 0;
    }
    industryData[company.industry]++;
  });
  
  // 风险等级分布数据
  const riskData = {};
  companies.forEach(company => {
    if (!riskData[company.riskLevel]) {
      riskData[company.riskLevel] = 0;
    }
    riskData[company.riskLevel]++;
  });
  
  // 创建行业分布图表
  const industryChartDom = document.getElementById('industry-chart');
  if (industryChartDom) {
    const industryChart = echarts.init(industryChartDom);
    
    const industryOption = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center',
        data: Object.keys(industryData)
      },
      series: [
        {
          name: '行业分布',
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
          data: Object.keys(industryData).map(industry => {
            return {
              name: industry,
              value: industryData[industry]
            };
          })
        }
      ]
    };
    
    industryChart.setOption(industryOption);
    
    // 响应窗口大小变化
    window.addEventListener('resize', function() {
      industryChart.resize();
    });
  }
  
  // 创建风险等级分布图表
  const riskChartDom = document.getElementById('risk-chart');
  if (riskChartDom) {
    const riskChart = echarts.init(riskChartDom);
    
    const riskOption = {
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
        data: Object.keys(riskData)
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '公司数量',
          type: 'bar',
          data: Object.keys(riskData).map(riskLevel => {
            // 根据风险等级设置不同的颜色
            let color;
            if (riskLevel === '低') color = '#4caf50';
            else if (riskLevel === '中低') color = '#2196f3';
            else if (riskLevel === '中') color = '#ff9800';
            else if (riskLevel === '中高') color = '#ff5722';
            else color = '#f44336';
            
            return {
              value: riskData[riskLevel],
              itemStyle: {
                color: color
              }
            };
          }),
          barWidth: '60%'
        }
      ]
    };
    
    riskChart.setOption(riskOption);
    
    // 响应窗口大小变化
    window.addEventListener('resize', function() {
      riskChart.resize();
    });
  }
}

// 按风险等级筛选公司
function filterCompanies(type) {
  // 实际应用中应该根据类型过滤数据
  console.log('按风险等级筛选:', type);
  alert('筛选功能将在后续版本中实现');
}

// 刷新公司数据
function refreshCompanyData() {
  // 实际应用中应该重新请求数据
  console.log('刷新公司数据');
  alert('数据刷新功能将在后续版本中实现');
}

// 导出公司数据
function exportCompanyData() {
  // 实际应用中应该生成CSV或Excel文件
  console.log('导出公司数据');
  alert('数据导出功能将在后续版本中实现');
}

// 显示公司详情
function showCompanyDetail(companyId) {
  // 模拟获取公司详情数据
  const companyDetail = {
    id: companyId,
    name: "示例公司",
    industry: "互联网",
    region: "深圳",
    marketCap: 3500,
    employees: 108000,
    riskLevel: "中低",
    financials: {
      revenue: 560.2,
      profit: 120.5,
      assets: 890.7,
      liabilities: 450.3
    },
    riskFactors: [
      { name: "政策风险", level: "中", impact: 3.2 },
      { name: "市场风险", level: "中", impact: 3.5 },
      { name: "技术风险", level: "低", impact: 2.1 },
      { name: "管理风险", level: "中低", impact: 2.8 }
    ],
    recentEvents: [
      { date: "2025-09-15", event: "发布新产品", impact: "正面" },
      { date: "2025-08-28", event: "高管变动", impact: "中性" },
      { date: "2025-07-10", event: "季度财报发布", impact: "正面" }
    ]
  };
  
  // 更新模态框标题
  document.getElementById('companyDetailTitle').textContent = `${companyDetail.name} 详情`;
  
  // 构建详情内容
  const detailContent = `
    <div class="mb-4">
      <div class="d-flex justify-content-between mb-3">
        <div>
          <span class="badge bg-${companyDetail.riskLevel === '低' ? 'success' : companyDetail.riskLevel === '中' ? 'warning' : companyDetail.riskLevel === '中低' ? 'info' : 'danger'} me-2">
            ${companyDetail.riskLevel}风险
          </span>
          <span class="badge bg-secondary">ID: ${companyDetail.id}</span>
        </div>
        <div class="text-muted small">
          行业: ${companyDetail.industry} | 地区: ${companyDetail.region}
        </div>
      </div>
      
      <div class="row mb-3">
        <div class="col-md-4">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">市值</h6>
            </div>
            <div class="card-body text-center">
              <h3 class="text-primary">${companyDetail.marketCap}</h3>
              <small class="text-muted">亿美元</small>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">员工数</h6>
            </div>
            <div class="card-body text-center">
              <h3 class="text-primary">${companyDetail.employees.toLocaleString()}</h3>
              <small class="text-muted">人</small>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">财务指标</h6>
            </div>
            <div class="card-body">
              <div class="d-flex justify-content-between small mb-1">
                <span>营收:</span>
                <span>${companyDetail.financials.revenue} 亿美元</span>
              </div>
              <div class="d-flex justify-content-between small mb-1">
                <span>利润:</span>
                <span>${companyDetail.financials.profit} 亿美元</span>
              </div>
              <div class="d-flex justify-content-between small">
                <span>资产负债率:</span>
                <span>${(companyDetail.financials.liabilities / companyDetail.financials.assets * 100).toFixed(1)}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card mb-3">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">风险因素</h6>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-sm mb-0">
              <thead>
                <tr>
                  <th>风险因素</th>
                  <th>风险等级</th>
                  <th>影响程度</th>
                </tr>
              </thead>
              <tbody>
                ${companyDetail.riskFactors.map(factor => `
                  <tr>
                    <td>${factor.name}</td>
                    <td>
                      <span class="badge bg-${factor.level === '高' ? 'danger' : factor.level === '中' ? 'warning' : factor.level === '中低' ? 'info' : 'success'}">
                        ${factor.level}
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
      
      <div class="card">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">近期事件</h6>
        </div>
        <div class="card-body">
          <ul class="list-group list-group-flush">
            ${companyDetail.recentEvents.map(event => `
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <span class="badge bg-secondary me-2">${event.date}</span>
                  ${event.event}
                </div>
                <span class="badge bg-${event.impact === '正面' ? 'success' : event.impact === '负面' ? 'danger' : 'secondary'}">
                  ${event.impact}
                </span>
              </li>
            `).join('')}
          </ul>
        </div>
      </div>
    </div>
  `;
  
  document.getElementById('companyDetailContent').innerHTML = detailContent;
  
  // 显示模态框
  const modal = new bootstrap.Modal(document.getElementById('companyDetailModal'));
  modal.show();
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是公司属性表模块，则自动加载
  if (window.location.hash === '#company-attributes') {
    loadCompanyAttributes();
  }
});