/*
 * 上市公司或行业分类模块
 * 大势所趋风险框架管理台
 */

// 加载上市公司或行业分类模块
function loadWindIndustryClassification() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载上市公司或行业分类数据...</p>
    </div>
  `;
  
  // 加载模块内容
  renderWindIndustryModule(contentArea);
}

// 渲染上市公司或行业分类模块内容
function renderWindIndustryModule(container) {
  // 直接从API获取上市公司数据，不入库
  fetch('/api/listed-companies?dataSource=akshare&page=0&size=500')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data && data.data.content) {
        const companiesData = data.data.content;
        
        // 对数据进行行业分类处理
        const industryMap = groupCompaniesByIndustry(companiesData);
        const industries = processIndustries(industryMap, companiesData);
        
        // 准备图表数据
        const chartData = prepareChartData(industries);
        
        // 构建模块HTML
        const moduleHTML = buildIndustryModuleHTML(industries, companiesData);
        container.innerHTML = moduleHTML;

        // 加载 AKShare 全量股票数据表格
        loadAkshareStockData();

        // 初始化图表
        initIndustryChart(chartData);
        
        // 加载Bootstrap的Modal组件
        loadBootstrapJS();
        
        // 更新最后更新时间
        document.getElementById('industry-last-updated').textContent = new Date().toLocaleString();
      } else {
        container.innerHTML = `
          <div class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill"></i> 无法加载行业数据: ${data.message || '未知错误'}
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

// 按行业对公司进行分组
function groupCompaniesByIndustry(companiesData) {
  const industryMap = new Map();
  
  companiesData.forEach(company => {
    const industry = company.industry || '未知行业';
    if (!industryMap.has(industry)) {
      industryMap.set(industry, []);
    }
    industryMap.get(industry).push(company);
  });
  
  return industryMap;
}

// 处理行业数据
function processIndustries(industryMap, companiesData) {
  const industries = [];
  let industryCode = 100000;
  
  industryMap.forEach((companies, industryName) => {
    // 计算行业统计数据
    const totalMarketCap = companies.reduce((sum, company) => sum + (parseFloat(company.totalMarketValue) || 0), 0);
    const avgPeRatio = companies.reduce((sum, company) => sum + (parseFloat(company.peRatio) || 0), 0) / companies.length;
    const avgPbRatio = companies.reduce((sum, company) => sum + (parseFloat(company.pbRatio) || 0), 0) / companies.length;
    
    industries.push({
      industryCode: industryCode.toString(),
      industryName: industryName,
      industryLevel: 1,
      parentIndustryCode: null,
      companyCount: companies.length,
      totalMarketCap: totalMarketCap,
      avgPeRatio: avgPeRatio,
      avgPbRatio: avgPbRatio,
      companies: companies
    });
    
    industryCode++;
  });
  
  // 按公司数量排序
  industries.sort((a, b) => b.companyCount - a.companyCount);
  
  return industries;
}

// 准备图表数据
function prepareChartData(industries) {
  // 取前10个行业用于图表展示
  const topIndustries = industries.slice(0, 10);
  
  const categories = topIndustries.map(item => item.industryName);
  const marketCapData = topIndustries.map(item => item.totalMarketCap);
  const companyCountData = topIndustries.map(item => item.companyCount);
  
  return {
    categories: categories,
    series: [
      {
        name: '总市值(亿元)',
        type: 'bar',
        data: marketCapData
      },
      {
        name: '公司数量',
        type: 'line',
        yAxisIndex: 1,
        data: companyCountData
      }
    ]
  };
}

// 初始化行业图表
function initIndustryChart(data) {
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
  const chartDom = document.getElementById('industry-chart');
  const myChart = echarts.init(chartDom);
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999'
        }
      }
    },
    legend: {
      data: ['总市值(亿元)', '公司数量']
    },
    xAxis: [
      {
        type: 'category',
        data: data.categories,
        axisPointer: {
          type: 'shadow'
        },
        axisLabel: {
          rotate: 45,
          interval: 0
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: '总市值(亿元)',
        min: 0,
        axisLabel: {
          formatter: '{value}'
        }
      },
      {
        type: 'value',
        name: '公司数量',
        min: 0,
        axisLabel: {
          formatter: '{value}'
        }
      }
    ],
    series: data.series
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

// 搜索行业
function searchIndustry() {
  const searchTerm = document.getElementById('industry-search').value.trim().toLowerCase();
  if (!searchTerm) {
    alert('请输入搜索关键词');
    return;
  }
  
  // 获取所有行业行
  const rows = document.querySelectorAll('#industry-data-table tr');
  
  // 过滤显示匹配的行
  rows.forEach(row => {
    const industryName = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
    const industryCode = row.querySelector('td:first-child').textContent.toLowerCase();
    
    if (industryName.includes(searchTerm) || industryCode.includes(searchTerm)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

// 刷新行业数据
function refreshIndustryData() {
  const contentArea = document.getElementById('content');
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在刷新行业数据...</p>
    </div>
  `;
  
  // 重新渲染模块
  renderWindIndustryModule(contentArea);
}

// 导出行业数据
function exportIndustryData() {
  // 获取行业数据
  const rows = document.querySelectorAll('#industry-data-table tr');
  let csvContent = '行业代码,行业名称,级别,公司数量,总市值(亿元),平均市盈率,平均市净率\n';
  
  rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    if (cells.length > 0) {
      const code = cells[0].textContent;
      const name = cells[1].querySelector('a')?.textContent || cells[1].textContent;
      const level = cells[2].textContent;
      const count = cells[4].textContent;
      const marketCap = cells[5].textContent;
      const pe = cells[6]?.textContent || '';
      const pb = cells[7]?.textContent || '';
      
      csvContent += `${code},${name},${level},${count},${marketCap},${pe},${pb}\n`;
    }
  });
  
  // 创建下载链接
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', 'industry_data_' + new Date().toISOString().slice(0,10) + '.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

// 显示行业详情
function showIndustryDetail(industryCode) {
  // 获取行业数据
  fetch('/api/listed-companies?dataSource=akshare&page=0&size=500')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data && data.data.content) {
        const companiesData = data.data.content;
        const industryMap = groupCompaniesByIndustry(companiesData);
        const industries = processIndustries(industryMap, companiesData);
        
        // 找到对应行业
        const industry = industries.find(item => item.industryCode === industryCode);
        
        if (industry) {
          // 更新模态框内容
          document.getElementById('industryDetailTitle').textContent = industry.industryName + ' (' + industry.industryCode + ')';
          
          const detailContent = `
            <div class="mb-4">
              <div class="d-flex justify-content-between mb-3">
                <div>
                  <span class="badge bg-primary me-2">Level ${industry.industryLevel}</span>
                  <span class="badge bg-secondary">${industry.parentIndustryCode ? '有上级行业' : '一级行业'}</span>
                </div>
                <div class="text-muted small">
                  公司数量: ${industry.companyCount} | 总市值: ${industry.totalMarketCap.toFixed(2)}亿元
                </div>
              </div>
              
              <div class="alert alert-light">
                <h6 class="fw-bold">行业描述</h6>
                <p>${getIndustryDescription(industry.industryName)}</p>
              </div>
              
              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="card">
                    <div class="card-header bg-light">
                      <h6 class="card-title mb-0">行业关键指标</h6>
                    </div>
                    <div class="card-body">
                      <div class="row">
                        <div class="col-6 mb-3">
                          <div class="d-flex justify-content-between">
                            <span>平均市盈率(PE):</span>
                            <span class="fw-bold">${industry.avgPeRatio.toFixed(2)}</span>
                          </div>
                        </div>
                        <div class="col-6 mb-3">
                          <div class="d-flex justify-content-between">
                            <span>平均市净率(PB):</span>
                            <span class="fw-bold">${industry.avgPbRatio.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="card">
                    <div class="card-header bg-light">
                      <h6 class="card-title mb-0">行业概览</h6>
                    </div>
                    <div class="card-body">
                      <ul class="mb-0">
                        <li>包含 ${industry.companyCount} 家上市公司</li>
                        <li>总市值达 ${industry.totalMarketCap.toFixed(2)} 亿元</li>
                        <li>行业平均市盈率为 ${industry.avgPeRatio.toFixed(2)}</li>
                        <li>行业平均市净率为 ${industry.avgPbRatio.toFixed(2)}</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          `;
          
          document.getElementById('industryDetailContent').innerHTML = detailContent;
          
          // 显示模态框
          const modal = new bootstrap.Modal(document.getElementById('industryDetailModal'));
          modal.show();
        }
      }
    })
    .catch(error => {
      alert('获取行业详情失败: ' + error.message);
    });
}

// 获取行业描述（简单的示例，实际应用中可以从数据库或配置文件中获取）
function getIndustryDescription(industryName) {
  const descriptions = {
    '指数': '包含各种市场指数，如上证指数、深证成指等，反映整体市场表现。',
    '金融': '包含银行、证券、保险等金融机构，是国民经济的重要组成部分。',
    '科技': '包含软件开发、硬件制造、互联网等高科技企业，代表创新与发展方向。',
    '医药': '包含制药、医疗器械、医疗服务等企业，关系人民健康与医疗保障。',
    '消费': '包含食品饮料、零售、家电等消费相关企业，受居民消费水平影响较大。',
    '能源': '包含石油、煤炭、电力等能源企业，是工业生产的基础。',
    '材料': '包含化工、钢铁、有色金属等原材料企业，处于产业链上游。',
    '工业': '包含机械制造、航空航天、国防军工等工业企业，是实体经济的支柱。',
    '房地产': '包含房地产开发、物业管理等企业，与宏观经济政策密切相关。',
    '公用事业': '包含水务、燃气、公共交通等公共服务企业，具有一定的公益性。'
  };
  
  return descriptions[industryName] || `该行业包含 ${industryName} 相关的上市公司，涵盖了该领域的主要企业。`;
}

// 查看行业公司列表
function viewCompanies(industryCode) {
  // 获取行业数据
  fetch('/api/listed-companies?dataSource=akshare&page=0&size=500')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data && data.data.content) {
        const companiesData = data.data.content;
        const industryMap = groupCompaniesByIndustry(companiesData);
        const industries = processIndustries(industryMap, companiesData);
        
        // 找到对应行业
        const industry = industries.find(item => item.industryCode === industryCode);
        
        if (industry) {
          // 更新模态框标题
          document.getElementById('companiesModalTitle').textContent = industry.industryName + ' - 公司列表';
          
          // 构建公司列表内容
          const companiesContent = `
            <div class="mb-3">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="搜索公司名称或代码" id="company-search">
                <button class="btn btn-outline-primary" type="button" onclick="searchCompanies('${industryCode}')">
                  <i class="bi bi-search"></i> 搜索
                </button>
              </div>
            </div>
            
            <div class="table-responsive">
              <table class="table table-hover table-striped">
                <thead class="table-light">
                  <tr>
                    <th scope="col">股票代码</th>
                    <th scope="col">公司名称</th>
                    <th scope="col">最新价</th>
                    <th scope="col">涨跌幅</th>
                    <th scope="col">市值(亿元)</th>
                    <th scope="col">市盈率</th>
                    <th scope="col">市净率</th>
                    <th scope="col">操作</th>
                  </tr>
                </thead>
                <tbody id="companies-data-table">
                  ${industry.companies.map(company => `
                    <tr>
                      <td>${company.stockCode}</td>
                      <td>${company.stockName}</td>
                      <td>${company.latestPrice}</td>
                      <td class="${parseFloat(company.priceChangeRate) >= 0 ? 'text-danger' : 'text-success'}">${parseFloat(company.priceChangeRate) >= 0 ? '+' : ''}${company.priceChangeRate}%</td>
                      <td>${company.totalMarketValue || 0}</td>
                      <td>${company.peRatio || 0}</td>
                      <td>${company.pbRatio || 0}</td>
                      <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="showCompanyDetail('${company.stockCode}')">
                          <i class="bi bi-graph-up"></i> 详情
                        </button>
                      </td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
            
            <div class="d-flex justify-content-between align-items-center mt-3">
              <div>
                <span class="text-muted">共 ${industry.companies.length} 家公司</span>
              </div>
              <button class="btn btn-sm btn-primary" onclick="exportCompaniesData('${industry.industryName}')">
                <i class="bi bi-download"></i> 导出列表
              </button>
            </div>
          `;
          
          document.getElementById('companiesModalContent').innerHTML = companiesContent;
          
          // 显示模态框
          const modal = new bootstrap.Modal(document.getElementById('companiesModal'));
          modal.show();
        }
      }
    })
    .catch(error => {
      alert('获取公司列表失败: ' + error.message);
    });
}

// 搜索公司
function searchCompanies(industryCode) {
  const searchTerm = document.getElementById('company-search').value.trim().toLowerCase();
  if (!searchTerm) {
    alert('请输入搜索关键词');
    return;
  }
  
  // 获取所有公司行
  const rows = document.querySelectorAll('#companies-data-table tr');
  
  // 过滤显示匹配的行
  rows.forEach(row => {
    const code = row.querySelector('td:first-child').textContent.toLowerCase();
    const name = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
    
    if (code.includes(searchTerm) || name.includes(searchTerm)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

// 显示公司详情
function showCompanyDetail(stockCode) {
  // 在实际应用中，可以调用更详细的公司信息接口
  alert('显示股票代码为 ' + stockCode + ' 的公司详情功能将在后续版本中实现');
}

// 导出公司数据
function exportCompaniesData(industryName) {
  // 获取公司数据
  const rows = document.querySelectorAll('#companies-data-table tr');
  let csvContent = '股票代码,公司名称,最新价,涨跌幅,市值(亿元),市盈率,市净率\n';
  
  rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    if (cells.length > 0) {
      const code = cells[0].textContent;
      const name = cells[1].textContent;
      const price = cells[2].textContent;
      const change = cells[3].textContent;
      const marketCap = cells[4].textContent;
      const pe = cells[5].textContent;
      const pb = cells[6].textContent;
      
      csvContent += `${code},${name},${price},${change},${marketCap},${pe},${pb}\n`;
    }
  });
  
  // 创建下载链接
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', industryName + '_companies_' + new Date().toISOString().slice(0,10) + '.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

// 构建行业模块HTML
function buildIndustryModuleHTML(industries, companiesData) {
  return `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">上市公司或行业分类 <span class="badge bg-danger">实时</span></h4>
      <div class="row">
        <div class="col-md-8">
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-light d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">行业分类体系</h5>
              <div class="input-group" style="width: 300px;">
                <input type="text" class="form-control form-control-sm" placeholder="搜索行业或代码" id="industry-search">
                <button class="btn btn-sm btn-outline-primary" type="button" onclick="searchIndustry()">
                  <i class="bi bi-search"></i>
                </button>
              </div>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive" style="max-height: 500px; overflow-y: auto;">
                <table class="table table-hover table-striped mb-0">
                  <thead class="table-light sticky-top">
                    <tr>
                      <th scope="col">行业代码</th>
                      <th scope="col">行业名称</th>
                      <th scope="col">级别</th>
                      <th scope="col">上级行业</th>
                      <th scope="col">公司数量</th>
                      <th scope="col">总市值(亿元)</th>
                      <th scope="col">平均市盈率</th>
                      <th scope="col">平均市净率</th>
                      <th scope="col">操作</th>
                    </tr>
                  </thead>
                  <tbody id="industry-data-table">
                    ${industries.map(item => `
                      <tr>
                        <td>${item.industryCode}</td>
                        <td>
                          <div style="padding-left: 0px;">
                            <a href="#" class="text-decoration-none" onclick="showIndustryDetail('${item.industryCode}')">${item.industryName}</a>
                          </div>
                        </td>
                        <td>${item.industryLevel}</td>
                        <td>${item.parentIndustryCode ? industries.find(parent => parent.industryCode === item.parentIndustryCode)?.industryName || '-' : '-'}</td>
                        <td>${item.companyCount}</td>
                        <td>${item.totalMarketCap.toFixed(2)}</td>
                        <td>${item.avgPeRatio.toFixed(2)}</td>
                        <td>${item.avgPbRatio.toFixed(2)}</td>
                        <td>
                          <button class="btn btn-sm btn-outline-primary" onclick="viewCompanies('${item.industryCode}')">
                            <i class="bi bi-list-ul"></i> 查看公司
                          </button>
                        </td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
            <div class="card-footer bg-light">
              <div class="d-flex justify-content-between align-items-center">
                <small class="text-muted">最后更新: <span id="industry-last-updated">${new Date().toLocaleString()}</span></small>
                <div>
                  <button class="btn btn-sm btn-primary" onclick="refreshIndustryData()">
                    <i class="bi bi-arrow-clockwise"></i> 刷新数据
                  </button>
                  <button class="btn btn-sm btn-outline-secondary" onclick="exportIndustryData()">
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
              <h5 class="card-title mb-0">行业分布统计</h5>
            </div>
            <div class="card-body">
              <div id="industry-chart" style="height: 300px;"></div>
            </div>
          </div>
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">行业分类统计</h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-primary mb-0">${industries.filter(item => item.industryLevel === 1).length}</h3>
                    <small class="text-muted">一级行业</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-success mb-0">${companiesData.length}</h3>
                    <small class="text-muted">上市公司</small>
                  </div>
                </div>
                <div class="col-12">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-info mb-0">${industries.reduce((sum, item) => sum + parseFloat(item.totalMarketCap), 0).toFixed(2)}</h3>
                    <small class="text-muted">总市值(亿元)</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 行业详情模态框 -->
      <div class="modal fade" id="industryDetailModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="industryDetailTitle">行业详情</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="industryDetailContent">
              <!-- 详情内容将通过JS动态填充 -->
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
              <button type="button" class="btn btn-primary" onclick="showCompanies('${industries[0]?.industryCode || ''}')">查看行业公司</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 公司列表模态框 -->
      <div class="modal fade" id="companiesModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="companiesModalTitle">行业公司列表</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="companiesModalContent">
              <!-- 公司列表内容将通过JS动态填充 -->
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

// 页面加载完成后初始化
/**
 * 加载并渲染 AKShare 全量股票数据（来自 akshare_stock_structure.txt）
 * 渲染位置：在 #content 顶部动态插入一个卡片区域
 */
function loadAkshareStockData() {
  const container = document.getElementById('content');
  if (!container) return;

  // 如果已存在，避免重复插入
  if (!document.getElementById('akshare-stock-card')) {
    const card = document.createElement('div');
    card.id = 'akshare-stock-card';
    card.className = 'card shadow-sm mb-4';
    card.innerHTML = `
      <div class="card-header bg-light d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">AKShare 全量股票数据</h5>
        <div class="d-flex gap-2">
          <input id="akshare-search" type="text" placeholder="搜索 代码/名称" class="form-control form-control-sm" style="width:220px;">
          <button class="btn btn-sm btn-outline-primary" id="akshare-search-btn"><i class="bi bi-search"></i> 搜索</button>
          <button class="btn btn-sm btn-outline-secondary" id="akshare-reset-btn"><i class="bi bi-x-circle"></i> 重置</button>
        </div>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive" style="max-height: 480px; overflow: auto;">
          <table class="table table-hover table-striped mb-0">
            <thead id="akshare-thead" class="table-light sticky-top"></thead>
            <tbody id="akshare-tbody"></tbody>
          </table>
        </div>
      </div>
      <div class="card-footer bg-light d-flex justify-content-between">
        <small class="text-muted">数据来源：AKShare | 文件：akshare_stock_structure.txt</small>
        <div id="akshare-stats" class="text-muted"></div>
      </div>
    `;
    container.prepend(card);
  }

  // 依次尝试多个资源路径
  const candidates = [
    'static/data/akshare_stock_structure.txt',
    '../akshare_stock_structure.txt'
  ];

  tryFetchTextSequentially(candidates)
    .then((rawText) => {
      const jsonText = extractJsonArrayFromText(rawText);
      const sanitized = sanitizeAkshareJson(jsonText);
      const rows = JSON.parse(sanitized);

      renderAkshareTable(rows);

      // 绑定检索
      const searchInput = document.getElementById('akshare-search');
      const searchBtn = document.getElementById('akshare-search-btn');
      const resetBtn = document.getElementById('akshare-reset-btn');
      if (searchBtn && resetBtn) {
        searchBtn.onclick = () => {
          const q = (searchInput?.value || '').trim().toLowerCase();
          const allTr = document.querySelectorAll('#akshare-tbody tr');
          allTr.forEach(tr => {
            const code = (tr.getAttribute('data-code') || '').toLowerCase();
            const name = (tr.getAttribute('data-name') || '').toLowerCase();
            tr.style.display = (code.includes(q) || name.includes(q)) ? '' : 'none';
          });
        };
        resetBtn.onclick = () => {
          if (searchInput) searchInput.value = '';
          const allTr = document.querySelectorAll('#akshare-tbody tr');
          allTr.forEach(tr => tr.style.display = '');
        };
      }
    })
    .catch((err) => {
      console.error('加载 AKShare 数据失败:', err);
      const thead = document.getElementById('akshare-thead');
      const tbody = document.getElementById('akshare-tbody');
      if (thead && tbody) {
        thead.innerHTML = '<tr><th>错误</th></tr>';
        tbody.innerHTML = `<tr><td class="text-danger">无法加载 akshare_stock_structure.txt，请将文件放到 static/data/ 目录或检查路径权限。</td></tr>`;
      }
    });
}

// 依次尝试多个 URL 获取文本
function tryFetchTextSequentially(urls) {
  return new Promise((resolve, reject) => {
    let index = 0;
    const attempt = () => {
      if (index >= urls.length) return reject(new Error('所有候选路径均加载失败'));
      fetch(urls[index])
        .then(r => {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.text();
        })
        .then(text => resolve(text))
        .catch(() => {
          index++;
          attempt();
        });
    };
    attempt();
  });
}

// 从文本中提取 JSON 数组片段（位于“=== 数据JSON结构 ===”之后的 [...]）
function extractJsonArrayFromText(text) {
  const marker = '=== 数据JSON结构 ===';
  const idx = text.indexOf(marker);
  const sub = idx >= 0 ? text.slice(idx + marker.length) : text;

  const start = sub.indexOf('[');
  if (start < 0) throw new Error('未找到 JSON 数组起始符号');
  // 简单括号计数匹配末尾
  let depth = 0;
  for (let i = start; i < sub.length; i++) {
    const ch = sub[i];
    if (ch === '[') depth++;
    if (ch === ']') {
      depth--;
      if (depth === 0) {
        return sub.slice(start, i + 1);
      }
    }
  }
  throw new Error('未能匹配完整的 JSON 数组');
}

// 将 NaN 替换为 null，使之成为合法 JSON
function sanitizeAkshareJson(jsonText) {
  // 仅替换非字符串上下文中的 NaN（粗略但有效：全局替换后再修正）
  return jsonText.replace(/\bNaN\b/g, 'null');
}

// 渲染表格（动态表头为所有键的并集）
function renderAkshareTable(rows) {
  const thead = document.getElementById('akshare-thead');
  const tbody = document.getElementById('akshare-tbody');
  const stats = document.getElementById('akshare-stats');
  if (!thead || !tbody) return;

  // 计算列集合
  const columnsSet = new Set();
  rows.forEach(r => Object.keys(r).forEach(k => columnsSet.add(k)));
  const columns = Array.from(columnsSet);

  // 表头
  thead.innerHTML = `
    <tr>
      ${columns.map(c => `<th>${c}</th>`).join('')}
    </tr>
  `;

  // 表体
  const frag = document.createDocumentFragment();
  rows.forEach(r => {
    const tr = document.createElement('tr');
    tr.setAttribute('data-code', String(r['代码'] ?? ''));
    tr.setAttribute('data-name', String(r['名称'] ?? ''));
    tr.innerHTML = columns.map(c => {
      const v = r[c];
      // 规范化展示
      if (v === null || typeof v === 'undefined') return '<td></td>';
      if (typeof v === 'number') return `<td>${Number.isFinite(v) ? v : ''}</td>`;
      return `<td>${String(v)}</td>`;
    }).join('');
    frag.appendChild(tr);
  });
  tbody.innerHTML = '';
  tbody.appendChild(frag);

  if (stats) {
    stats.textContent = `共 ${rows.length} 条记录，${columns.length} 列`;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是上市公司或行业分类模块，则自动加载
  if (window.location.hash === '#wind-industry') {
    loadWindIndustryClassification();
  }
});