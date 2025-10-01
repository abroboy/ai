/**
 * 公司属性表模块
 * 大势所趋风险框架管理台 - 第二层模块
 */

// 加载公司属性表模块
function loadCompanyAttributes() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-5">
      <div class="loading-indicator"></div>
      <p class="mt-3">正在加载公司属性表数据...</p>
    </div>
  `;
  
  // 直接加载模块内容，使用AKShare数据源
  renderCompanyAttributesModule(contentArea);
}

// 渲染公司属性表模块内容
function renderCompanyAttributesModule(container) {
  // 使用AKShare数据源获取公司数据
  fetch('/api/listed-companies?dataSource=akshare&page=0&size=500')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP错误! 状态码: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.success && data.data && data.data.content) {
        const companiesData = data.data.content;
        // 处理公司数据，转换为公司属性表所需格式
        const companies = processCompanyData(companiesData);
        renderCompanyAttributesContent(container, companies);
      } else {
        container.innerHTML = `
          <div class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill"></i> 无法加载公司属性数据: ${data.message || '未知错误'}
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

// 处理公司数据，转换为属性表所需格式
function processCompanyData(companiesData) {
  // 从AKShare数据中提取所需字段
  return companiesData.map((company, index) => ({
    id: index + 1,
    name: company.stockName,
    industry: company.industryName || '未知行业',
    region: getRegionFromCode(company.stockCode),
    marketCap: parseFloat(company.totalMarketValue || 0).toFixed(2),
    employees: Math.floor(Math.random() * 50000) + 1000, // 模拟员工数
    riskLevel: calculateRiskLevel(company.peRatio, company.pbRatio)
  }));
}

// 根据股票代码获取地区信息
function getRegionFromCode(stockCode) {
  if (stockCode.startsWith('6')) return '上海';
  if (stockCode.startsWith('0') || stockCode.startsWith('3')) return '深圳';
  return '未知地区';
}

// 计算风险等级
function calculateRiskLevel(peRatio, pbRatio) {
  const pe = parseFloat(peRatio || 0);
  const pb = parseFloat(pbRatio || 0);
  
  if (pe > 50 || pb > 5) return '高';
  if (pe > 30 || pb > 3) return '中';
  if (pe > 15 || pb > 1.5) return '中低';
  return '低';
}

// 渲染公司属性内容
function renderCompanyAttributesContent(container, companies) {
  
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">公司属性表 <span class="badge bg-danger">实时</span></h4>
      
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
    `;
    
    modalContent.innerHTML = detailContent;
  } else {
    modalTitle.textContent = '公司不存在';
    modalContent.innerHTML = `
      <div class="alert alert-danger text-center py-4">
        <i class="bi bi-exclamation-circle-fill me-2"></i>
        未找到ID为 ${companyId} 的公司信息
      </div>
    `;
  }
} catch (error) {
  modalTitle.textContent = '加载失败';
  modalContent.innerHTML = `
    <div class="alert alert-danger text-center py-4">
      <i class="bi bi-exclamation-circle-fill me-2"></i>
      获取公司详情失败: ${error.message}
    </div>
  `;
}
});
}

// 处理公司详情数据
function processCompanyDetail(companyItem, companyId) {
  const pe = parseFloat(companyItem.peRatio || 0);
  const pb = parseFloat(companyItem.pbRatio || 0);
  const riskLevel = calculateRiskLevel(pe, pb);
  
  // 生成模拟的财务数据和风险因素
  return {
    id: companyId,
    name: companyItem.stockName,
    industry: companyItem.industryName || '未知行业',
    region: getRegionFromCode(companyItem.stockCode),
    marketCap: parseFloat(companyItem.totalMarketValue || 0).toFixed(2),
    employees: Math.floor(Math.random() * 50000) + 1000,
    riskLevel: riskLevel,
    financials: {
      revenue: (Math.random() * 1000 + 100).toFixed(1),
      profit: (Math.random() * 200 + 50).toFixed(1),
      assets: (Math.random() * 2000 + 200).toFixed(1),
      liabilities: (Math.random() * 1000 + 100).toFixed(1)
    },
    riskFactors: [
      { name: "政策风险", level: getRandomRiskLevel(), impact: (Math.random() * 2 + 2).toFixed(1) },
      { name: "市场风险", level: getRandomRiskLevel(), impact: (Math.random() * 2 + 2).toFixed(1) },
      { name: "技术风险", level: getRandomRiskLevel(), impact: (Math.random() * 2 + 2).toFixed(1) },
      { name: "管理风险", level: getRandomRiskLevel(), impact: (Math.random() * 2 + 2).toFixed(1) }
    ],
    recentEvents: generateRecentEvents()
  };
}

// 生成随机风险等级
function getRandomRiskLevel() {
  const levels = ['低', '中低', '中', '高'];
  return levels[Math.floor(Math.random() * levels.length)];
}

// 生成最近事件
function generateRecentEvents() {
  const eventTypes = [
    '发布新产品', '高管变动', '季度财报发布', '战略合作', 
    '融资活动', '并购重组', '股权激励', '产品更新'
  ];
  const impacts = ['正面', '负面', '中性'];
  const events = [];
  
  for (let i = 0; i < 3; i++) {
    const date = new Date();
    date.setDate(date.getDate() - Math.floor(Math.random() * 90));
    const formattedDate = date.toISOString().split('T')[0];
    
    events.push({
      date: formattedDate,
      event: eventTypes[Math.floor(Math.random() * eventTypes.length)],
      impact: impacts[Math.floor(Math.random() * impacts.length)]
    });
  }
  
  // 按日期排序（最新的在前）
  events.sort((a, b) => new Date(b.date) - new Date(a.date));
  return events;
}
      
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
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-5">
      <div class="loading-indicator"></div>
      <p class="mt-3">正在刷新公司属性数据...</p>
    </div>
  `;
  
  // 重新渲染模块，使用AKShare数据源
  renderCompanyAttributesModule(contentArea);
}

// 导出公司数据
function exportCompanyData() {
  // 实际应用中应该生成CSV或Excel文件
  console.log('导出公司数据');
  alert('数据导出功能将在后续版本中实现');
}

// 显示公司详情
function showCompanyDetail(companyId) {
  const modalTitle = document.getElementById('companyDetailTitle');
  const modalContent = document.getElementById('companyDetailContent');
  
  // 显示加载状态
  modalTitle.textContent = '正在加载公司详情...';
  modalContent.innerHTML = `
    <div class="text-center py-4">
      <div class="loading-indicator"></div>
      <p class="mt-2">正在获取公司详细信息...</p>
    </div>
  `;
  
  // 显示模态框
  const modal = new bootstrap.Modal(document.getElementById('companyDetailModal'));
  modal.show();
  
  // 从API获取公司详情数据
  fetch('/api/listed-companies?dataSource=akshare&page=0&size=500')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP错误! 状态码: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.success && data.data && data.data.content) {
        // 找到对应ID的公司
        const companiesData = data.data.content;
        const companyItem = companiesData[companyId - 1]; // 假设ID从1开始
        
        if (companyItem) {
          // 处理公司详情数据
          const companyDetail = processCompanyDetail(companyItem, companyId);
          
          // 更新模态框标题
          modalTitle.textContent = `${companyDetail.name} 详情`;
          
          // 构建详情内容
          const detailContent = `
            <div class="mb-4">
              <div class="d-flex justify-content-between mb-3">
                <div>
                  <span class="badge bg-${companyDetail.riskLevel === '低' ? 'success' : companyDetail.riskLevel === '中' ? 'warning' : companyDetail.riskLevel === '中低' ? 'info' : 'danger'} me-2">
                    ${companyDetail.riskLevel}风险`}]}}}
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