/**
 * 公司分值表模块
 * 大势所趋风险框架管理台 - 第四层模块
 */

// 从深度分析导入数据
function importFromDeepAnalysis() {
  if (!window.appData || !window.appData.hotspotData) {
    alert('没有可用的深度分析数据，请先在深度分析模块中导出数据');
    return;
  }

  // 转换数据格式
  const hotspotData = window.appData.hotspotData;
  const convertedData = convertHotspotToScoreData(hotspotData);
  
  // 存储转换后的数据
  window.appData.scoreData = convertedData;
  
  // 提示用户
  const toastHTML = `
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
      <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header bg-success text-white">
          <strong class="me-auto">数据导入成功</strong>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          已成功导入${convertedData.length}条评分数据
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
  
  // 重新渲染模块
  renderCompanyScoreTableModule(document.getElementById('content'));
}

// 转换热点数据为评分数据
function convertHotspotToScoreData(hotspotData) {
  return hotspotData.map(item => {
    // 根据热度、趋势和风险等级计算初步分值
    let score = item.heat * 0.7;
    if (item.trend === '上升') score += 5;
    else if (item.trend === '下降') score -= 5;
    
    if (item.riskLevel === '高') score -= 10;
    else if (item.riskLevel === '中高') score -= 5;
    else if (item.riskLevel === '中低') score += 5;
    else if (item.riskLevel === '低') score += 10;
    
    // 确保分值在0-100范围内
    score = Math.max(0, Math.min(100, score));
    
    return {
      id: item.id,
      name: item.name,
      category: item.category,
      score: score,
      source: item.source,
      originalHeat: item.heat,
      originalTrend: item.trend,
      originalRiskLevel: item.riskLevel
    };
  });
}

// 加载公司分值表模块
function loadCompanyScoreTable() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载公司分值表数据...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderCompanyScoreTableModule(contentArea);
  }, 800);
}

// 渲染公司分值表模块内容
function renderCompanyScoreTableModule(container) {
  // 模拟公司分值数据
  const scoreData = {
    updateTime: "2025-09-25 14:30:00",
    totalCompanies: 3500,
    averageScore: 68.5,
    scoreDistribution: {
      "90-100": 320,
      "80-89": 680,
      "70-79": 950,
      "60-69": 780,
      "50-59": 420,
      "0-49": 350
    },
    topCompanies: [
      { rank: 1, code: "600519", name: "贵州茅台", industry: "白酒", score: 96.8, change: 0.5 },
      { rank: 2, code: "000858", name: "五粮液", industry: "白酒", score: 94.2, change: 0.3 },
      { rank: 3, code: "601318", name: "中国平安", industry: "保险", score: 93.5, change: -0.2 },
      { rank: 4, code: "600036", name: "招商银行", industry: "银行", score: 92.7, change: 0.8 },
      { rank: 5, code: "000333", name: "美的集团", industry: "家电", score: 91.9, change: 1.2 }
    ],
    bottomCompanies: [
      { rank: 3496, code: "002456", name: "某某科技", industry: "电子", score: 32.5, change: -2.8 },
      { rank: 3497, code: "600123", name: "某某股份", industry: "制造", score: 31.8, change: -1.5 },
      { rank: 3498, code: "300789", name: "某某生物", industry: "医药", score: 30.2, change: -3.2 },
      { rank: 3499, code: "002789", name: "某某通信", industry: "通信", score: 28.5, change: -4.5 },
      { rank: 3500, code: "600321", name: "某某能源", industry: "能源", score: 25.3, change: -5.2 }
    ],
    biggestGainers: [
      { code: "300059", name: "某某电子", industry: "电子", score: 78.5, change: 8.7 },
      { code: "002230", name: "某某科技", industry: "计算机", score: 75.2, change: 7.9 },
      { code: "600882", name: "某某汽车", industry: "汽车", score: 82.3, change: 7.5 },
      { code: "300750", name: "某某医疗", industry: "医疗", score: 79.8, change: 7.2 },
      { code: "002415", name: "某某材料", industry: "材料", score: 76.5, change: 6.8 }
    ],
    biggestLosers: [
      { code: "002789", name: "某某通信", industry: "通信", score: 28.5, change: -4.5 },
      { code: "600321", name: "某某能源", industry: "能源", score: 25.3, change: -5.2 },
      { code: "300125", name: "某某网络", industry: "传媒", score: 35.8, change: -5.5 },
      { code: "002156", name: "某某金融", industry: "金融", score: 42.3, change: -6.2 },
      { code: "600721", name: "某某地产", industry: "房地产", score: 38.7, change: -7.5 }
    ],
    scoreFactors: [
      { factor: "财务状况", weight: 30 },
      { factor: "市场表现", weight: 25 },
      { factor: "行业地位", weight: 20 },
      { factor: "风险因素", weight: 15 },
      { factor: "社会评价", weight: 10 }
    ]
  };
  
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">公司分值表</h4>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <p class="text-muted mb-0">最后更新时间: ${scoreData.updateTime}</p>
        <div class="btn-group">
          <button class="btn btn-outline-primary btn-sm" onclick="exportCompanyScoreTable('excel')">
            <i class="bi bi-file-earmark-excel me-1"></i> 导出Excel
          </button>
          <button class="btn btn-outline-primary btn-sm" onclick="exportCompanyScoreTable('pdf')">
            <i class="bi bi-file-earmark-pdf me-1"></i> 导出PDF
          </button>
          <button class="btn btn-outline-success btn-sm" onclick="importFromDeepAnalysis()">
            <i class="bi bi-arrow-down-circle me-1"></i> 从深度分析导入
          </button>
        </div>
      </div>
      
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body text-center">
              <h1 class="display-4 fw-bold">${scoreData.totalCompanies.toLocaleString()}</h1>
              <p class="text-muted">评分公司总数</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body text-center">
              <h1 class="display-4 fw-bold">${scoreData.averageScore.toFixed(1)}</h1>
              <p class="text-muted">平均分值</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <h6 class="card-title mb-3">评分因素权重</h6>
              ${scoreData.scoreFactors.map(factor => `
                <div class="mb-2">
                  <div class="d-flex justify-content-between mb-1">
                    <span>${factor.factor}</span>
                    <span class="fw-bold">${factor.weight}%</span>
                  </div>
                  <div class="progress" style="height: 6px;">
                    <div class="progress-bar" role="progressbar" style="width: ${factor.weight}%;" aria-valuenow="${factor.weight}" aria-valuemin="0" aria-valuemax="100"></div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      </div>
      
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">分值分布</h5>
            </div>
            <div class="card-body">
              <div id="score-distribution-chart" style="height: 300px;"></div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">公司评分查询</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="输入公司代码或名称" id="company-search-input">
                  <button class="btn btn-primary" type="button" onclick="searchCompanyScore()">
                    <i class="bi bi-search"></i> 查询
                  </button>
                </div>
              </div>
              <div class="table-responsive">
                <table class="table table-hover table-sm">
                  <thead>
                    <tr>
                      <th>代码</th>
                      <th>名称</th>
                      <th>行业</th>
                      <th>分值</th>
                      <th>变化</th>
                    </tr>
                  </thead>
                  <tbody id="company-search-results">
                    <tr>
                      <td colspan="5" class="text-center text-muted">请输入公司代码或名称进行查询</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">评分最高公司</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>排名</th>
                      <th>代码</th>
                      <th>名称</th>
                      <th>行业</th>
                      <th>分值</th>
                      <th>变化</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${scoreData.topCompanies.map(company => `
                      <tr>
                        <td>${company.rank}</td>
                        <td>${company.code}</td>
                        <td>${company.name}</td>
                        <td>${company.industry}</td>
                        <td><span class="fw-bold">${company.score.toFixed(1)}</span></td>
                        <td>
                          <span class="${company.change >= 0 ? 'text-success' : 'text-danger'}">
                            ${company.change >= 0 ? '+' : ''}${company.change.toFixed(1)}
                          </span>
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
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">评分最低公司</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>排名</th>
                      <th>代码</th>
                      <th>名称</th>
                      <th>行业</th>
                      <th>分值</th>
                      <th>变化</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${scoreData.bottomCompanies.map(company => `
                      <tr>
                        <td>${company.rank}</td>
                        <td>${company.code}</td>
                        <td>${company.name}</td>
                        <td>${company.industry}</td>
                        <td><span class="fw-bold">${company.score.toFixed(1)}</span></td>
                        <td>
                          <span class="${company.change >= 0 ? 'text-success' : 'text-danger'}">
                            ${company.change >= 0 ? '+' : ''}${company.change.toFixed(1)}
                          </span>
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
      
      <div class="row">
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">涨幅最大公司</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>代码</th>
                      <th>名称</th>
                      <th>行业</th>
                      <th>分值</th>
                      <th>变化</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${scoreData.biggestGainers.map(company => `
                      <tr>
                        <td>${company.code}</td>
                        <td>${company.name}</td>
                        <td>${company.industry}</td>
                        <td><span class="fw-bold">${company.score.toFixed(1)}</span></td>
                        <td>
                          <span class="text-success">
                            +${company.change.toFixed(1)}
                          </span>
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
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">跌幅最大公司</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>代码</th>
                      <th>名称</th>
                      <th>行业</th>
                      <th>分值</th>
                      <th>变化</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${scoreData.biggestLosers.map(company => `
                      <tr>
                        <td>${company.code}</td>
                        <td>${company.name}</td>
                        <td>${company.industry}</td>
                        <td><span class="fw-bold">${company.score.toFixed(1)}</span></td>
                        <td>
                          <span class="text-danger">
                            ${company.change.toFixed(1)}
                          </span>
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
    </div>
  `;
  
  // 更新容器内容
  container.innerHTML = moduleHTML;
  
  // 初始化图表
  initScoreDistributionChart(scoreData);
  
  // 初始化搜索功能
  initCompanySearch(scoreData);
}

// 初始化分值分布图表
function initScoreDistributionChart(data) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createScoreDistributionChart(data);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createScoreDistributionChart(data);
  }
}

// 创建分值分布图表
function createScoreDistributionChart(data) {
  const chartDom = document.getElementById('score-distribution-chart');
  if (!chartDom) return;
  
  const myChart = echarts.init(chartDom);
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      data: Object.keys(data.scoreDistribution)
    },
    series: [
      {
        name: '分值分布',
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

// 初始化公司搜索功能
function initCompanySearch() {
  // 模拟搜索功能，实际项目中应该通过API获取数据
  window.searchCompanyScore = function() {
    const searchInput = document.getElementById('company-search-input');
    const searchResults = document.getElementById('company-search-results');
    
    if (!searchInput || !searchResults) return;
    
    const searchTerm = searchInput.value.trim();
    
    if (searchTerm === '') {
      searchResults.innerHTML = '<tr><td colspan="5" class="text-center text-muted">请输入公司代码或名称进行查询</td></tr>';
      return;
    }
    
    // 模拟搜索延迟
    searchResults.innerHTML = '<tr><td colspan="5" class="text-center"><div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div> 正在搜索...</td></tr>';
    
    setTimeout(() => {
      // 模拟搜索结果
      const mockResults = [
        { code: "600519", name: "贵州茅台", industry: "白酒", score: 96.8, change: 0.5 },
        { code: "600036", name: "招商银行", industry: "银行", score: 92.7, change: 0.8 },
        { code: "601318", name: "中国平安", industry: "保险", score: 93.5, change: -0.2 }
      ];
      
      if (mockResults.length > 0) {
        searchResults.innerHTML = mockResults.map(company => `
          <tr>
            <td>${company.code}</td>
            <td>${company.name}</td>
            <td>${company.industry}</td>
            <td><span class="fw-bold">${company.score.toFixed(1)}</span></td>
            <td>
              <span class="${company.change >= 0 ? 'text-success' : 'text-danger'}">
                ${company.change >= 0 ? '+' : ''}${company.change.toFixed(1)}
              </span>
            </td>
          </tr>
        `).join('');
      } else {
        searchResults.innerHTML = '<tr><td colspan="5" class="text-center text-muted">未找到匹配的公司</td></tr>';
      }
    }, 800);
  };
}

// 导出公司分值表
window.exportCompanyScoreTable = function(format) {
  // 模拟导出功能，实际项目中应该实现真正的导出逻辑
  alert(`正在导出${format === 'excel' ? 'Excel' : 'PDF'}格式的公司分值表...`);
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是公司分值表模块，则自动加载
  if (window.location.hash === '#company-score-table') {
    loadCompanyScoreTable();
  }
});