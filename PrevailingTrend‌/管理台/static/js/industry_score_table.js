/**
 * 行业分值表模块
 * 大势所趋风险框架管理台 - 第四层模块
 */

// 加载行业分值表模块
function loadIndustryScoreTable() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载行业分值表数据...</p>
    </div>
  `;
  
  // 从API获取行业分值表数据
  fetch('/api/industry-score-table')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data) {
        const industryData = data.data;
        renderIndustryScoreTableModule(contentArea, industryData);
      } else {
        contentArea.innerHTML = `
          <div class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill"></i> 无法加载行业分值表数据: ${data.message || '未知错误'}
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

// 渲染行业分值表模块内容
function renderIndustryScoreTableModule(container, industryData) {
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">行业分值表 <span class="badge bg-danger">实时</span></h4>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <p class="text-muted mb-0">最后更新时间: ${industryData.updateTime}</p>
        <div class="btn-group">
          <button class="btn btn-outline-primary btn-sm" onclick="exportIndustryScoreTable('excel')">
            <i class="bi bi-file-earmark-excel me-1"></i> 导出Excel
          </button>
          <button class="btn btn-outline-primary btn-sm" onclick="exportIndustryScoreTable('pdf')">
            <i class="bi bi-file-earmark-pdf me-1"></i> 导出PDF
          </button>
        </div>
      </div>
      
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body text-center">
              <h1 class="display-4 fw-bold">${industryData.totalIndustries}</h1>
              <p class="text-muted">评分行业总数</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body text-center">
              <h1 class="display-4 fw-bold">${industryData.averageScore.toFixed(1)}</h1>
              <p class="text-muted">平均分值</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <h6 class="card-title mb-3">评分因素权重</h6>
              ${industryData.scoreFactors.map(factor => `
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
              <div id="industry-score-distribution-chart" style="height: 300px;"></div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">行业评分查询</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="输入行业代码或名称" id="industry-search-input">
                  <button class="btn btn-primary" type="button" onclick="searchIndustryScore()">
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
                      <th>分值</th>
                      <th>变化</th>
                      <th>公司数</th>
                    </tr>
                  </thead>
                  <tbody id="industry-search-results">
                    <tr>
                      <td colspan="5" class="text-center text-muted">请输入行业代码或名称进行查询</td>
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
              <h5 class="card-title mb-0">评分最高行业</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>排名</th>
                      <th>代码</th>
                      <th>名称</th>
                      <th>分值</th>
                      <th>变化</th>
                      <th>公司数</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${industryData.topIndustries.map(industry => `
                      <tr>
                        <td>${industry.rank}</td>
                        <td>${industry.code}</td>
                        <td>${industry.name}</td>
                        <td><span class="fw-bold">${industry.score.toFixed(1)}</span></td>
                        <td>
                          <span class="${industry.change >= 0 ? 'text-success' : 'text-danger'}">
                            ${industry.change >= 0 ? '+' : ''}${industry.change.toFixed(1)}
                          </span>
                        </td>
                        <td>${industry.companies}</td>
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
              <h5 class="card-title mb-0">评分最低行业</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>排名</th>
                      <th>代码</th>
                      <th>名称</th>
                      <th>分值</th>
                      <th>变化</th>
                      <th>公司数</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${industryData.bottomIndustries.map(industry => `
                      <tr>
                        <td>${industry.rank}</td>
                        <td>${industry.code}</td>
                        <td>${industry.name}</td>
                        <td><span class="fw-bold">${industry.score.toFixed(1)}</span></td>
                        <td>
                          <span class="${industry.change >= 0 ? 'text-success' : 'text-danger'}">
                            ${industry.change >= 0 ? '+' : ''}${industry.change.toFixed(1)}
                          </span>
                        </td>
                        <td>${industry.companies}</td>
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
              <h5 class="card-title mb-0">涨幅最大行业</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>代码</th>
                      <th>名称</th>
                      <th>分值</th>
                      <th>变化</th>
                      <th>公司数</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${industryData.biggestGainers.map(industry => `
                      <tr>
                        <td>${industry.code}</td>
                        <td>${industry.name}</td>
                        <td><span class="fw-bold">${industry.score.toFixed(1)}</span></td>
                        <td>
                          <span class="text-success">
                            +${industry.change.toFixed(1)}
                          </span>
                        </td>
                        <td>${industry.companies}</td>
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
              <h5 class="card-title mb-0">跌幅最大行业</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>代码</th>
                      <th>名称</th>
                      <th>分值</th>
                      <th>变化</th>
                      <th>公司数</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${industryData.biggestLosers.map(industry => `
                      <tr>
                        <td>${industry.code}</td>
                        <td>${industry.name}</td>
                        <td><span class="fw-bold">${industry.score.toFixed(1)}</span></td>
                        <td>
                          <span class="text-danger">
                            ${industry.change.toFixed(1)}
                          </span>
                        </td>
                        <td>${industry.companies}</td>
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
  initIndustryScoreDistributionChart(industryData);
  
  // 初始化搜索功能
  initIndustrySearch(industryData);
}

// 初始化分值分布图表
function initIndustryScoreDistributionChart(data) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createIndustryScoreDistributionChart(data);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createIndustryScoreDistributionChart(data);
  }
}

// 创建分值分布图表
function createIndustryScoreDistributionChart(data) {
  const chartDom = document.getElementById('industry-score-distribution-chart');
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

// 初始化行业搜索功能
function initIndustrySearch() {
  // 模拟搜索功能，实际项目中应该通过API获取数据
  window.searchIndustryScore = function() {
    const searchInput = document.getElementById('industry-search-input');
    const searchResults = document.getElementById('industry-search-results');
    
    if (!searchInput || !searchResults) return;
    
    const searchTerm = searchInput.value.trim();
    
    if (searchTerm === '') {
      searchResults.innerHTML = '<tr><td colspan="5" class="text-center text-muted">请输入行业代码或名称进行查询</td></tr>';
      return;
    }
    
    // 模拟搜索延迟
    searchResults.innerHTML = '<tr><td colspan="5" class="text-center"><div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div> 正在搜索...</td></tr>';
    
    setTimeout(() => {
      // 模拟搜索结果
      const mockResults = [
        { code: "BK0438", name: "半导体", score: 94.5, change: 1.2, companies: 85 },
        { code: "BK0475", name: "新能源", score: 92.8, change: 0.5, companies: 102 },
        { code: "BK0428", name: "医疗器械", score: 91.2, change: 0.8, companies: 76 }
      ];
      
      if (mockResults.length > 0) {
        searchResults.innerHTML = mockResults.map(industry => `
          <tr>
            <td>${industry.code}</td>
            <td>${industry.name}</td>
            <td><span class="fw-bold">${industry.score.toFixed(1)}</span></td>
            <td>
              <span class="${industry.change >= 0 ? 'text-success' : 'text-danger'}">
                ${industry.change >= 0 ? '+' : ''}${industry.change.toFixed(1)}
              </span>
            </td>
            <td>${industry.companies}</td>
          </tr>
        `).join('');
      } else {
        searchResults.innerHTML = '<tr><td colspan="5" class="text-center text-muted">未找到匹配的行业</td></tr>';
      }
    }, 800);
  };
}

// 导出行业分值表
window.exportIndustryScoreTable = function(format) {
  // 模拟导出功能，实际项目中应该实现真正的导出逻辑
  alert(`正在导出${format === 'excel' ? 'Excel' : 'PDF'}格式的行业分值表...`);
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是行业分值表模块，则自动加载
  if (window.location.hash === '#industry-score-table') {
    loadIndustryScoreTable();
  }
});