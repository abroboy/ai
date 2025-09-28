/**
 * 行业+公司分值表模块
 * 大势所趋风险框架管理台 - 第四层模块
 */

// 加载行业+公司分值表模块
function loadIndustryCompanyScoreTable() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载行业+公司分值表数据...</p>
    </div>
  `;
  
  // 从API获取行业+公司分值表数据
  fetch('/api/industry-company-score-table')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data) {
        const industryData = data.data;
        renderIndustryCompanyScoreTableModule(contentArea, industryData);
      } else {
        contentArea.innerHTML = `
          <div class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill"></i> 无法加载行业+公司分值表数据: ${data.message || '未知错误'}
          </div>
        `;
      }
    })
    .catch(error => {
      contentArea.innerHTML = `
        <div class="alert alert-danger">
          <i class="bi bi-exclamation-triangle-fill"></i> 请求失败: ${error.message}
        </div>
      `;
    });
}

// 渲染行业+公司分值表模块内容
function renderIndustryCompanyScoreTableModule(container, industryData) {
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">行业+公司分值表 <span class="badge bg-danger">实时</span></h4>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <p class="text-muted mb-0">最后更新时间: ${industryData.selectedIndustryCompanies.updateTime}</p>
        <div class="btn-group">
          <button class="btn btn-outline-primary btn-sm" onclick="exportIndustryCompanyScoreTable('excel')">
            <i class="bi bi-file-earmark-excel me-1"></i> 导出Excel
          </button>
          <button class="btn btn-outline-primary btn-sm" onclick="exportIndustryCompanyScoreTable('pdf')">
            <i class="bi bi-file-earmark-pdf me-1"></i> 导出PDF
          </button>
        </div>
      </div>
      
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">行业选择</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="搜索行业" id="industry-filter-input">
                  <button class="btn btn-primary" type="button" onclick="filterIndustries()">
                    <i class="bi bi-search"></i>
                  </button>
                </div>
              </div>
              <div class="list-group" id="industry-list" style="max-height: 400px; overflow-y: auto;">
                ${industryData.industries.map(industry => `
                  <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center ${industry.code === industryData.selectedIndustryCompanies.industryCode ? 'active' : ''}" 
                     onclick="selectIndustry('${industry.code}')">
                    <div>
                      <div class="fw-bold">${industry.name}</div>
                      <small>${industry.code}</small>
                    </div>
                    <div class="text-end">
                      <span class="badge bg-primary rounded-pill">${industry.score.toFixed(1)}</span>
                      <div><small>${industry.companies}家公司</small></div>
                    </div>
                  </a>
                `).join('')}
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-8">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">${industryData.selectedIndustryCompanies.industryName} (${industryData.selectedIndustryCompanies.industryCode}) - 行业概览</h5>
                <span class="badge bg-primary fs-5">${industryData.selectedIndustryCompanies.industryScore.toFixed(1)}</span>
              </div>
            </div>
            <div class="card-body">
              <div class="row mb-4">
                <div class="col-md-6">
                  <div id="industry-company-score-distribution-chart" style="height: 250px;"></div>
                </div>
                <div class="col-md-6">
                  <h6 class="mb-3">行业平均财务指标</h6>
                  <div class="table-responsive">
                    <table class="table table-sm">
                      <tbody>
                        <tr>
                          <td>市盈率 (P/E)</td>
                          <td class="fw-bold text-end">${industryData.selectedIndustryCompanies.industryAvgFinancials.pe.toFixed(1)}</td>
                        </tr>
                        <tr>
                          <td>市净率 (P/B)</td>
                          <td class="fw-bold text-end">${industryData.selectedIndustryCompanies.industryAvgFinancials.pbr.toFixed(1)}</td>
                        </tr>
                        <tr>
                          <td>净资产收益率 (ROE)</td>
                          <td class="fw-bold text-end">${industryData.selectedIndustryCompanies.industryAvgFinancials.roe.toFixed(1)}%</td>
                        </tr>
                        <tr>
                          <td>净利润增长率</td>
                          <td class="fw-bold text-end">${industryData.selectedIndustryCompanies.industryAvgFinancials.netProfitGrowth.toFixed(1)}%</td>
                        </tr>
                        <tr>
                          <td>营收增长率</td>
                          <td class="fw-bold text-end">${industryData.selectedIndustryCompanies.industryAvgFinancials.revenueGrowth.toFixed(1)}%</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card shadow-sm mb-4">
        <div class="card-header bg-light">
          <div class="d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">${industryData.selectedIndustryCompanies.industryName}行业公司评分列表</h5>
            <div class="input-group" style="width: 300px;">
              <input type="text" class="form-control form-control-sm" placeholder="搜索公司" id="company-filter-input">
              <button class="btn btn-sm btn-primary" type="button" onclick="filterCompanies()">
                <i class="bi bi-search"></i>
              </button>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover table-sm" id="industry-companies-table">
              <thead>
                <tr>
                  <th onclick="sortCompaniesTable(0)">排名 <i class="bi bi-arrow-down-up"></i></th>
                  <th onclick="sortCompaniesTable(1)">代码 <i class="bi bi-arrow-down-up"></i></th>
                  <th onclick="sortCompaniesTable(2)">名称 <i class="bi bi-arrow-down-up"></i></th>
                  <th onclick="sortCompaniesTable(3)">评分 <i class="bi bi-arrow-down-up"></i></th>
                  <th onclick="sortCompaniesTable(4)">变化 <i class="bi bi-arrow-down-up"></i></th>
                  <th onclick="sortCompaniesTable(5)">市值(亿) <i class="bi bi-arrow-down-up"></i></th>
                  <th onclick="sortCompaniesTable(6)">市盈率 <i class="bi bi-arrow-down-up"></i></th>
                  <th onclick="sortCompaniesTable(7)">市净率 <i class="bi bi-arrow-down-up"></i></th>
                  <th>详情</th>
                </tr>
              </thead>
              <tbody>
                ${industryData.selectedIndustryCompanies.companies.map(company => `
                  <tr>
                    <td>${company.rank}</td>
                    <td>${company.code}</td>
                    <td>${company.name}</td>
                    <td><span class="fw-bold">${company.score.toFixed(1)}</span></td>
                    <td>
                      <span class="${company.change >= 0 ? 'text-success' : 'text-danger'}">
                        ${company.change >= 0 ? '+' : ''}${company.change.toFixed(1)}
                      </span>
                    </td>
                    <td>${company.marketCap.toFixed(1)}</td>
                    <td>${company.pe.toFixed(1)}</td>
                    <td>${company.pbr.toFixed(1)}</td>
                    <td>
                      <button class="btn btn-sm btn-outline-primary" onclick="showCompanyDetail('${company.code}')">
                        <i class="bi bi-info-circle"></i>
                      </button>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">行业内公司评分对比</h5>
            </div>
            <div class="card-body">
              <div id="industry-company-comparison-chart" style="height: 350px;"></div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">行业内公司评分变化趋势</h5>
            </div>
            <div class="card-body">
              <div id="industry-company-trend-chart" style="height: 350px;"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 更新容器内容
  container.innerHTML = moduleHTML;
  
  // 初始化图表
  initIndustryCompanyCharts(industryData.selectedIndustryCompanies);
  
  // 初始化交互功能
  initIndustryCompanyInteractions();
}

// 初始化行业公司图表
function initIndustryCompanyCharts(data) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createIndustryCompanyCharts(data);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createIndustryCompanyCharts(data);
  }
}

// 创建行业公司相关图表
function createIndustryCompanyCharts(data) {
  // 创建分值分布图表
  createScoreDistributionChart(data);
  
  // 创建公司评分对比图表
  createCompanyComparisonChart(data);
  
  // 创建公司评分趋势图表
  createCompanyTrendChart(data);
}

// 创建分值分布图表
function createScoreDistributionChart(data) {
  const chartDom = document.getElementById('industry-company-score-distribution-chart');
  if (!chartDom) return;
  
  const myChart = echarts.init(chartDom);
  
  const option = {
    title: {
      text: '公司评分分布',
      left: 'center',
      textStyle: {
        fontSize: 14
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      bottom: '0',
      left: 'center',
      itemWidth: 10,
      itemHeight: 10,
      textStyle: {
        fontSize: 12
      }
    },
    series: [
      {
        name: '分值分布',
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
            fontSize: '12',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: Object.entries(data.scoreDistribution).map(([range, count]) => {
          // 根据分数范围设置不同的颜色
          let color;
          if (range === '90-100') color = '#52c41a';
          else if (range === '80-89') color = '#73d13d';
          else if (range === '70-79') color = '#fadb14';
          else if (range === '60-69') color = '#fa8c16';
          else if (range === '50-59') color = '#fa541c';
          else color = '#f5222d';
          
          return {
            name: range,
            value: count,
            itemStyle: {
              color: color
            }
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

// 创建公司评分对比图表
function createCompanyComparisonChart(data) {
  const chartDom = document.getElementById('industry-company-comparison-chart');
  if (!chartDom) return;
  
  const myChart = echarts.init(chartDom);
  
  // 获取前10家公司数据
  const topCompanies = data.companies.slice(0, 10);
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      max: 100,
      axisLabel: {
        formatter: '{value}'
      }
    },
    yAxis: {
      type: 'category',
      data: topCompanies.map(company => company.name),
      axisLabel: {
        fontSize: 12
      }
    },
    series: [
      {
        name: '评分',
        type: 'bar',
        data: topCompanies.map(company => {
          // 根据分数设置不同的颜色
          let color;
          if (company.score >= 90) color = '#52c41a';
          else if (company.score >= 80) color = '#73d13d';
          else if (company.score >= 70) color = '#fadb14';
          else if (company.score >= 60) color = '#fa8c16';
          else if (company.score >= 50) color = '#fa541c';
          else color = '#f5222d';
          
          return {
            value: company.score,
            itemStyle: {
              color: color
            }
          };
        }),
        label: {
          show: true,
          position: 'right',
          formatter: '{c}'
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

// 创建公司评分趋势图表
function createCompanyTrendChart(data) {
  const chartDom = document.getElementById('industry-company-trend-chart');
  if (!chartDom) return;
  
  const myChart = echarts.init(chartDom);
  
  // 获取前5家公司数据
  const topCompanies = data.companies.slice(0, 5);
  
  // 模拟过去6个月的数据
  const months = ['4月', '5月', '6月', '7月', '8月', '9月'];
  const series = topCompanies.map(company => {
    // 生成模拟的历史数据
    const historicalData = [];
    let lastScore = company.score;
    
    // 从最近一个月往前推
    for (let i = 5; i >= 0; i--) {
      if (i === 5) {
        // 最后一个月使用当前分数
        historicalData.unshift(lastScore);
      } else {
        // 生成随机的历史分数变化
        const change = (Math.random() * 4 - 2); // -2到2之间的随机变化
        lastScore = Math.min(100, Math.max(0, lastScore - change)); // 确保分数在0-100之间
        historicalData.unshift(parseFloat(lastScore.toFixed(1)));
      }
    }
    
    return {
      name: company.name,
      type: 'line',
      data: historicalData,
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      emphasis: {
        focus: 'series'
      }
    };
  });
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: topCompanies.map(company => company.name),
      bottom: 0,
      textStyle: {
        fontSize: 12
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: months
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
    series: series
  };
  
  myChart.setOption(option);
  
  // 响应窗口大小变化
  window.addEventListener('resize', function() {
    myChart.resize();
  });
}

// 初始化行业公司交互功能
function initIndustryCompanyInteractions() {
  // 行业选择功能
  window.selectIndustry = function(industryCode) {
    // 模拟行业选择，实际项目中应该通过API获取数据
    alert(`已选择行业: ${industryCode}，正在加载该行业的公司数据...`);
    
    // 更新UI，实际项目中应该重新加载数据
    const industryItems = document.querySelectorAll('#industry-list a');
    industryItems.forEach(item => {
      if (item.textContent.includes(industryCode)) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });
  };
  
  // 行业过滤功能
  window.filterIndustries = function() {
    const filterInput = document.getElementById('industry-filter-input');
    if (!filterInput) return;
    
    const filterText = filterInput.value.toLowerCase().trim();
    const industryItems = document.querySelectorAll('#industry-list a');
    
    industryItems.forEach(item => {
      const industryText = item.textContent.toLowerCase();
      if (filterText === '' || industryText.includes(filterText)) {
        item.style.display = '';
      } else {
        item.style.display = 'none';
      }
    });
  };
  
  // 公司表格排序功能
  window.sortCompaniesTable = function(columnIndex) {
    // 模拟表格排序，实际项目中应该实现真正的排序逻辑
    alert(`正在按第${columnIndex + 1}列排序表格...`);
  };
  
  // 公司过滤功能
  window.filterCompanies = function() {
    const filterInput = document.getElementById('company-filter-input');
    if (!filterInput) return;
    
    const filterText = filterInput.value.toLowerCase().trim();
    
    // 模拟公司过滤，实际项目中应该实现真正的过滤逻辑
    if (filterText !== '') {
      alert(`正在搜索包含"${filterText}"的公司...`);
    }
  };
  
  // 显示公司详情
  window.showCompanyDetail = function(companyCode) {
    // 模拟显示公司详情，实际项目中应该通过API获取数据并显示详情
    alert(`正在加载公司详情: ${companyCode}`);
  };
  
  // 导出行业+公司分值表
  window.exportIndustryCompanyScoreTable = function(format) {
    // 模拟导出功能，实际项目中应该实现真正的导出逻辑
    alert(`正在导出${format === 'excel' ? 'Excel' : 'PDF'}格式的行业+公司分值表...`);
  };
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是行业+公司分值表模块，则自动加载
  if (window.location.hash === '#industry-company-score-table') {
    loadIndustryCompanyScoreTable();
  }
});