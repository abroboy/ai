/**
 * 万得行业分类模块
 * 大势所趋风险框架管理台
 */

// 加载万得行业分类模块
function loadWindIndustryClassification() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载万得行业分类数据...</p>
    </div>
  `;
  
  // 加载模块内容
  renderWindIndustryModule(contentArea);
}

// 渲染万得行业分类模块内容
function renderWindIndustryModule(container) {
  // 从API获取行业分类数据
  fetch('/api/wind-industries')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data) {
        const industryData = data.data;
        
        // 行业市值分布数据（用于图表）
        // 这里需要根据实际数据计算分布
        const categories = [...new Set(industryData.map(item => item.industryName))];
        const marketCapData = {
          categories: categories.slice(0, 10), // 取前10个行业
          series: [
            {
              name: '市值占比',
              data: Array(10).fill(0).map(() => Math.random() * 20) // 模拟数据
            }
          ]
        };
        
        // 构建模块HTML
        const moduleHTML = buildIndustryModuleHTML(industryData);
        container.innerHTML = moduleHTML;
        
        // 初始化图表
        initIndustryChart(marketCapData);
        
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
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c}%'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      data: data.categories
    },
    series: [
      {
        name: '市值占比',
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
        data: data.categories.map((name, index) => {
          return {
            value: data.series[0].data[index],
            name: name
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

// 搜索行业
function searchIndustry() {
  const searchTerm = document.getElementById('industry-search').value.trim().toLowerCase();
  if (!searchTerm) {
    alert('请输入搜索关键词');
    return;
  }
  
  // 实际应用中应该根据搜索词过滤数据
  console.log('搜索行业:', searchTerm);
  alert('搜索功能将在后续版本中实现');
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
  // 实际应用中应该生成CSV或Excel文件
  console.log('导出行业数据');
  alert('数据导出功能将在后续版本中实现');
}

// 显示行业详情
function showIndustryDetail(id) {
  // 模拟获取行业详情数据
  const industryDetail = {
    id: id,
    name: "石油天然气",
    level: 2,
    parentName: "能源",
    companies: 78,
    marketCap: 5432.18,
    description: "石油天然气行业包括从事石油和天然气勘探、开采、炼制、销售等业务的公司，以及为石油天然气行业提供设备、技术和服务的公司。",
    subIndustries: [
      { name: "石油天然气设备与服务", companies: 35, marketCap: 2345.67 },
      { name: "石油天然气钻探", companies: 43, marketCap: 3086.51 }
    ],
    keyMetrics: {
      peRatio: 12.5,
      pbRatio: 1.8,
      roe: 15.2,
      dividendYield: 4.5
    },
    trends: [
      "全球能源转型加速，传统石油公司面临转型压力",
      "天然气作为过渡能源，中期需求仍将保持增长",
      "碳中和政策推动行业减排技术投入增加",
      "油气价格波动加剧，企业风险管理能力受到考验"
    ]
  };
  
  // 更新模态框内容
  document.getElementById('industryDetailTitle').textContent = industryDetail.name + ' (' + industryDetail.id + ')';
  
  const detailContent = `
    <div class="mb-4">
      <div class="d-flex justify-content-between mb-3">
        <div>
          <span class="badge bg-primary me-2">Level ${industryDetail.level}</span>
          <span class="badge bg-secondary">${industryDetail.parentName}</span>
        </div>
        <div class="text-muted small">
          公司数量: ${industryDetail.companies} | 总市值: ${industryDetail.marketCap.toFixed(2)}亿元
        </div>
      </div>
      
      <div class="alert alert-light">
        <h6 class="fw-bold">行业描述</h6>
        <p>${industryDetail.description}</p>
      </div>
      
      <div class="row mb-3">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">子行业</h6>
            </div>
            <div class="card-body p-0">
              <table class="table table-sm mb-0">
                <thead>
                  <tr>
                    <th>名称</th>
                    <th>公司数量</th>
                    <th>总市值(亿元)</th>
                  </tr>
                </thead>
                <tbody>
                  ${industryDetail.subIndustries.map(sub => `
                    <tr>
                      <td>${sub.name}</td>
                      <td>${sub.companies}</td>
                      <td>${sub.marketCap.toFixed(2)}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">行业关键指标</h6>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-6 mb-3">
                  <div class="d-flex justify-content-between">
                    <span>市盈率(PE):</span>
                    <span class="fw-bold">${industryDetail.keyMetrics.peRatio}</span>
                  </div>
                </div>
                <div class="col-6 mb-3">
                  <div class="d-flex justify-content-between">
                    <span>市净率(PB):</span>
                    <span class="fw-bold">${industryDetail.keyMetrics.pbRatio}</span>
                  </div>
                </div>
                <div class="col-6 mb-3">
                  <div class="d-flex justify-content-between">
                    <span>净资产收益率(ROE):</span>
                    <span class="fw-bold">${industryDetail.keyMetrics.roe}%</span>
                  </div>
                </div>
                <div class="col-6 mb-3">
                  <div class="d-flex justify-content-between">
                    <span>股息率:</span>
                    <span class="fw-bold">${industryDetail.keyMetrics.dividendYield}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">行业趋势</h6>
        </div>
        <div class="card-body">
          <ul class="mb-0">
            ${industryDetail.trends.map(trend => `<li>${trend}</li>`).join('')}
          </ul>
        </div>
      </div>
    </div>
  `;
  
  document.getElementById('industryDetailContent').innerHTML = detailContent;
  
  // 显示模态框
  const modal = new bootstrap.Modal(document.getElementById('industryDetailModal'));
  modal.show();
}

// 查看行业公司列表
function viewCompanies(industryId) {
  // 模拟获取行业公司列表数据
  const industryName = {
    "6101010000": "石油天然气",
    "6101020000": "煤炭",
    "6101030000": "新能源"
  }[industryId] || "未知行业";
  
  // 模拟公司数据
  const companies = [
    { code: "601857.SH", name: "中国石油", price: 6.32, change: 0.15, marketCap: 1156.78, pe: 8.5, pb: 0.9 },
    { code: "600028.SH", name: "中国石化", price: 4.76, change: -0.08, marketCap: 578.32, pe: 9.2, pb: 0.8 },
    { code: "600256.SH", name: "广汇能源", price: 3.45, change: 0.22, marketCap: 223.56, pe: 10.5, pb: 1.2 },
    { code: "601808.SH", name: "中海油服", price: 15.23, change: 0.56, marketCap: 217.89, pe: 12.3, pb: 1.5 },
    { code: "600583.SH", name: "海油工程", price: 5.67, change: -0.12, marketCap: 125.43, pe: 15.8, pb: 1.1 },
    { code: "002353.SZ", name: "杰瑞股份", price: 28.45, change: 1.23, marketCap: 272.34, pe: 18.7, pb: 2.3 },
    { code: "300164.SZ", name: "通源石油", price: 4.32, change: -0.05, marketCap: 35.67, pe: 22.5, pb: 1.8 },
    { code: "300084.SZ", name: "海默科技", price: 6.78, change: 0.34, marketCap: 26.54, pe: 25.6, pb: 2.1 }
  ];
  
  // 更新模态框标题
  document.getElementById('companiesModalTitle').textContent = industryName + ' - 公司列表';
  
  // 构建公司列表内容
  const companiesContent = `
    <div class="mb-3">
      <div class="input-group">
        <input type="text" class="form-control" placeholder="搜索公司名称或代码" id="company-search">
        <button class="btn btn-outline-primary" type="button">
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
        <tbody>
          ${companies.map(company => `
            <tr>
              <td>${company.code}</td>
              <td>${company.name}</td>
              <td>${company.price.toFixed(2)}</td>
              <td class="${company.change >= 0 ? 'text-danger' : 'text-success'}">${company.change >= 0 ? '+' : ''}${company.change.toFixed(2)}</td>
              <td>${company.marketCap.toFixed(2)}</td>
              <td>${company.pe.toFixed(1)}</td>
              <td>${company.pb.toFixed(1)}</td>
              <td>
                <button class="btn btn-sm btn-outline-primary">
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
        <span class="text-muted">共 ${companies.length} 家公司</span>
      </div>
      <nav>
        <ul class="pagination pagination-sm mb-0">
          <li class="page-item disabled"><a class="page-link" href="#">上一页</a></li>
          <li class="page-item active"><a class="page-link" href="#">1</a></li>
          <li class="page-item"><a class="page-link" href="#">2</a></li>
          <li class="page-item"><a class="page-link" href="#">3</a></li>
          <li class="page-item"><a class="page-link" href="#">下一页</a></li>
        </ul>
      </nav>
    </div>
  `;
  
  document.getElementById('companiesModalContent').innerHTML = companiesContent;
  
  // 显示模态框
  const modal = new bootstrap.Modal(document.getElementById('companiesModal'));
  modal.show();
}

// 构建行业模块HTML
function buildIndustryModuleHTML(industryData) {
  // 按照行业层级分组
  const level1Industries = industryData.filter(item => item.industryLevel === 1);
  const level2Industries = industryData.filter(item => item.industryLevel === 2);
  
  return `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">万得行业分类 <span class="badge bg-danger">实时</span></h4>
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
                      <th scope="col">操作</th>
                    </tr>
                  </thead>
                  <tbody id="industry-data-table">
                    ${level1Industries.map(item => `
                      <tr>
                        <td>${item.industryCode}</td>
                        <td>
                          <div style="padding-left: 0px;">
                            <a href="#" class="text-decoration-none" onclick="showIndustryDetail('${item.industryCode}')">${item.industryName}</a>
                          </div>
                        </td>
                        <td>${item.industryLevel}</td>
                        <td>${item.parentIndustryCode ? industryData.find(parent => parent.industryCode === item.parentIndustryCode)?.industryName || '-' : '-'}</td>
                        <td>-</td>
                        <td>-</td>
                        <td>
                          <button class="btn btn-sm btn-outline-primary" onclick="viewCompanies('${item.industryCode}')">
                            <i class="bi bi-list-ul"></i> 查看公司
                          </button>
                        </td>
                      </tr>
                      ${level2Industries.filter(sub => sub.parentIndustryCode === item.industryCode).map(subItem => `
                        <tr>
                          <td>${subItem.industryCode}</td>
                          <td>
                            <div style="padding-left: 20px;">
                              <i class="bi bi-dash"></i> 
                              <a href="#" class="text-decoration-none" onclick="showIndustryDetail('${subItem.industryCode}')">${subItem.industryName}</a>
                            </div>
                          </td>
                          <td>${subItem.industryLevel}</td>
                          <td>${subItem.parentIndustryCode ? industryData.find(parent => parent.industryCode === subItem.parentIndustryCode)?.industryName || '-' : '-'}</td>
                          <td>-</td>
                          <td>-</td>
                          <td>
                            <button class="btn btn-sm btn-outline-primary" onclick="viewCompanies('${subItem.industryCode}')">
                              <i class="bi bi-list-ul"></i> 查看公司
                            </button>
                          </td>
                        </tr>
                      `).join('')}
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
              <h5 class="card-title mb-0">行业市值分布</h5>
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
                    <h3 class="text-primary mb-0">${level1Industries.length}</h3>
                    <small class="text-muted">一级行业</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-success mb-0">${level2Industries.length}</h3>
                    <small class="text-muted">二级行业</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-info mb-0">-</h3>
                    <small class="text-muted">三级行业</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-warning mb-0">-</h3>
                    <small class="text-muted">上市公司</small>
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
              <button type="button" class="btn btn-primary">生成行业报告</button>
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
              <button type="button" class="btn btn-primary">导出公司列表</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是万得行业分类模块，则自动加载
  if (window.location.hash === '#wind-industry') {
    loadWindIndustryClassification();
  }
});