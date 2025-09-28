/**
 * 雪球等论坛热点数据模块
 * 大势所趋风险框架管理台
 */

// 加载雪球等论坛热点数据模块
function loadForumHotspotData() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载雪球等论坛热点数据...</p>
    </div>
  `;
  
  // 加载模块内容
  renderForumHotspotModule(contentArea);
}

// 渲染雪球等论坛热点数据模块内容
function renderForumHotspotModule(container) {
  // 从API获取论坛热点数据
  fetch('/api/forum-hotspot')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data) {
        const hotTopics = data.data;
        
        // 平台分布数据（用于图表）
        const platforms = [...new Set(hotTopics.map(item => item.platform))];
        const platformCounts = platforms.map(platform => {
          return hotTopics.filter(item => item.platform === platform).length;
        });
        
        const platformData = {
          platforms: platforms,
          values: platformCounts
        };
        
        // 构建模块HTML
        const moduleHTML = buildForumHotspotModuleHTML(hotTopics);
        container.innerHTML = moduleHTML;
        
        // 初始化图表
        initPlatformChart(platformData);
        
        // 加载Bootstrap的Modal组件
        loadBootstrapJS();
        
        // 更新最后更新时间
        document.getElementById('forum-hotspot-last-updated').textContent = new Date().toLocaleString();
      } else {
        container.innerHTML = `
          <div class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill"></i> 无法加载论坛热点数据: ${data.message || '未知错误'}
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

// 构建雪球等论坛热点模块HTML
function buildForumHotspotModuleHTML(hotTopics) {
  return `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">雪球等论坛热点数据 <span class="badge bg-danger">实时</span></h4>
      <div class="row">
        <div class="col-md-8">
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-light d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">热门讨论话题</h5>
              <div class="btn-group">
                <button class="btn btn-sm btn-outline-primary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                  平台筛选
                </button>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="#" onclick="filterByPlatform('all')">全部平台</a></li>
                  ${[...new Set(hotTopics.map(item => item.platform))].map(platform => `
                    <li><a class="dropdown-item" href="#" onclick="filterByPlatform('${platform}')">${platform}</a></li>
                  `).join('')}
                </ul>
              </div>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-hover table-striped mb-0">
                  <thead class="table-light">
                    <tr>
                      <th scope="col">ID</th>
                      <th scope="col">话题标题</th>
                      <th scope="col">平台</th>
                      <th scope="col">作者</th>
                      <th scope="col">日期</th>
                      <th scope="col">浏览量</th>
                      <th scope="col">评论数</th>
                      <th scope="col">情感倾向</th>
                    </tr>
                  </thead>
                  <tbody id="forum-hotspot-table">
                    ${hotTopics.map(item => `
                      <tr>
                        <td>${item.id}</td>
                        <td><a href="#" class="text-decoration-none" onclick="showTopicDetail(${item.id})">${item.title}</a></td>
                        <td>${item.platform}</td>
                        <td>${item.author}</td>
                        <td>${item.date}</td>
                        <td>${item.views.toLocaleString()}</td>
                        <td>${item.comments}</td>
                        <td>
                          <div class="d-flex align-items-center">
                            <div class="progress flex-grow-1 me-2" style="height: 6px;">
                              <div class="progress-bar bg-${getSentimentColor(item.sentiment)}" role="progressbar" 
                                style="width: ${Math.abs(item.sentiment) * 100}%"></div>
                            </div>
                            <span class="badge bg-${getSentimentColor(item.sentiment)}">${formatSentiment(item.sentiment)}</span>
                          </div>
                        </td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
            <div class="card-footer bg-light">
              <div class="d-flex justify-content-between align-items-center">
                <small class="text-muted">最后更新: <span id="forum-hotspot-last-updated">${new Date().toLocaleString()}</span></small>
                <div>
                  <button class="btn btn-sm btn-primary" onclick="refreshForumData()">
                    <i class="bi bi-arrow-clockwise"></i> 刷新数据
                  </button>
                  <button class="btn btn-sm btn-outline-secondary" onclick="exportForumData()">
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
              <h5 class="card-title mb-0">平台分布</h5>
            </div>
            <div class="card-body">
              <div id="platform-chart" style="height: 300px;"></div>
            </div>
          </div>
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">热点话题分析</h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-primary mb-0">${hotTopics.length}</h3>
                    <small class="text-muted">热门话题</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-success mb-0">${hotTopics.filter(item => item.sentiment >= 0.2).length}</h3>
                    <small class="text-muted">积极情绪</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-danger mb-0">${hotTopics.filter(item => item.sentiment < -0.2).length}</h3>
                    <small class="text-muted">消极情绪</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-warning mb-0">${hotTopics.filter(item => item.sentiment >= -0.2 && item.sentiment < 0.2).length}</h3>
                    <small class="text-muted">中性情绪</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 话题详情模态框 -->
      <div class="modal fade" id="topicDetailModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="topicDetailTitle">话题详情</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="topicDetailContent">
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

// 初始化平台分布图表
function initPlatformChart(data) {
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
  const chartDom = document.getElementById('platform-chart');
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
      data: data.platforms
    },
    series: [
      {
        name: '平台分布',
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
        data: data.platforms.map((platform, index) => {
          return {
            value: data.values[index],
            name: platform
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

// 根据情感倾向获取颜色
function getSentimentColor(sentiment) {
  if (sentiment >= 0.6) return 'success';
  if (sentiment >= 0.2) return 'info';
  if (sentiment >= -0.2) return 'warning';
  return 'danger';
}

// 格式化情感倾向显示
function formatSentiment(sentiment) {
  if (sentiment >= 0.6) return '积极';
  if (sentiment >= 0.2) return '偏积极';
  if (sentiment >= -0.2) return '中性';
  if (sentiment >= -0.6) return '偏消极';
  return '消极';
}

// 按平台筛选数据
function filterByPlatform(platform) {
  // 实际应用中应该根据平台过滤数据
  console.log('按平台筛选:', platform);
  alert('平台筛选功能将在后续版本中实现');
}

// 刷新论坛热点数据
function refreshForumData() {
  const contentArea = document.getElementById('content');
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在刷新论坛热点数据...</p>
    </div>
  `;
  
  // 重新渲染模块
  renderForumHotspotModule(contentArea);
}

// 导出论坛热点数据
function exportForumData() {
  // 实际应用中应该生成CSV或Excel文件
  console.log('导出论坛热点数据');
  alert('数据导出功能将在后续版本中实现');
}

// 显示话题详情
function showTopicDetail(id) {
  // 模拟获取话题详情数据
  const topicDetail = {
    id: id,
    title: "新能源汽车行业未来发展前景如何？",
    platform: "雪球",
    author: "价值投资者",
    date: "2025-09-22",
    views: 12580,
    comments: 356,
    sentiment: 0.78,
    content: "随着全球碳中和目标的推进，新能源汽车行业正迎来前所未有的发展机遇。中国作为全球最大的新能源汽车市场，产销量连续多年位居世界第一。但随着市场竞争加剧，行业也面临着技术迭代、补贴退坡、充电基础设施不足等挑战。未来几年，随着电池技术突破、自动驾驶技术成熟，新能源汽车有望迎来新一轮增长。",
    keyComments: [
      { user: "电池研究员", content: "固态电池是未来发展方向，能量密度有望提升30%以上，但量产仍需3-5年时间。", likes: 89 },
      { user: "汽车行业分析师", content: "市场已经从政策驱动转向市场驱动，消费者购买意愿明显提升，渗透率将持续提高。", likes: 76 },
      { user: "投资老手", content: "关注产业链中的细分龙头，特别是在电池材料、电控系统等领域具有技术壁垒的企业。", likes: 65 },
      { user: "理性思考者", content: "需警惕产能过剩风险，目前多家车企扩产计划激进，未来竞争将更加激烈。", likes: 52 }
    ],
    relatedStocks: [
      { code: "300750.SZ", name: "宁德时代", price: 345.67, change: 2.35 },
      { code: "002594.SZ", name: "比亚迪", price: 278.90, change: 1.56 },
      { code: "600733.SH", name: "北汽蓝谷", price: 12.45, change: -0.32 },
      { code: "601689.SH", name: "拓普集团", price: 56.78, change: 0.87 },
      { code: "688116.SH", name: "天奈科技", price: 89.23, change: 3.21 }
    ]
  };
  
  // 更新模态框内容
  document.getElementById('topicDetailTitle').textContent = topicDetail.title;
  
  const detailContent = `
    <div class="mb-4">
      <div class="d-flex justify-content-between mb-3">
        <div>
          <span class="badge bg-primary me-2">${topicDetail.platform}</span>
          <span class="badge bg-${getSentimentColor(topicDetail.sentiment)}">${formatSentiment(topicDetail.sentiment)}</span>
        </div>
        <div class="text-muted small">
          作者: ${topicDetail.author} | 发布日期: ${topicDetail.date} | 浏览量: ${topicDetail.views.toLocaleString()} | 评论数: ${topicDetail.comments}
        </div>
      </div>
      
      <div class="alert alert-light">
        <h6 class="fw-bold">话题内容</h6>
        <p>${topicDetail.content}</p>
      </div>
      
      <div class="card mb-3">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">热门评论</h6>
        </div>
        <div class="card-body p-0">
          <div class="list-group list-group-flush">
            ${topicDetail.keyComments.map(comment => `
              <div class="list-group-item">
                <div class="d-flex justify-content-between">
                  <div class="fw-bold">${comment.user}</div>
                  <div class="text-muted small"><i class="bi bi-hand-thumbs-up"></i> ${comment.likes}</div>
                </div>
                <p class="mb-0 mt-1">${comment.content}</p>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">相关股票</h6>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-sm mb-0">
              <thead>
                <tr>
                  <th>代码</th>
                  <th>名称</th>
                  <th>最新价</th>
                  <th>涨跌幅</th>
                </tr>
              </thead>
              <tbody>
                ${topicDetail.relatedStocks.map(stock => `
                  <tr>
                    <td>${stock.code}</td>
                    <td>${stock.name}</td>
                    <td>${stock.price.toFixed(2)}</td>
                    <td class="${stock.change >= 0 ? 'text-danger' : 'text-success'}">${stock.change >= 0 ? '+' : ''}${stock.change.toFixed(2)}%</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  `;
  
  document.getElementById('topicDetailContent').innerHTML = detailContent;
  
  // 显示模态框
  const modal = new bootstrap.Modal(document.getElementById('topicDetailModal'));
  modal.show();
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是雪球等论坛热点数据模块，则自动加载
  if (window.location.hash === '#forum-hotspot') {
    loadForumHotspotData();
  }
});