/**
 * 雪球等论坛数据模块
 * 大势所趋风险框架管理台 - 第三层模块
 */

// 加载雪球等论坛数据模块
function loadForumDataAnalysis() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载雪球等论坛数据分析...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderForumDataAnalysisModule(contentArea);
  }, 800);
}

// 渲染雪球等论坛数据模块内容
function renderForumDataAnalysisModule(container) {
  // 模拟论坛数据
  const forumData = {
    period: "2025年9月20日-2025年9月25日",
    summary: {
      totalPosts: 12458,
      totalComments: 87654,
      totalUsers: 5432,
      sentimentScore: 0.65
    },
    topStocks: [
      { code: "600519", name: "贵州茅台", mentions: 1245, sentiment: 0.82 },
      { code: "000858", name: "五粮液", mentions: 987, sentiment: 0.75 },
      { code: "601318", name: "中国平安", mentions: 876, sentiment: 0.45 },
      { code: "600036", name: "招商银行", mentions: 765, sentiment: 0.62 },
      { code: "000333", name: "美的集团", mentions: 654, sentiment: 0.58 }
    ],
    topTopics: [
      { topic: "新能源", mentions: 2345, sentiment: 0.78 },
      { topic: "半导体", mentions: 1876, sentiment: 0.72 },
      { topic: "人工智能", mentions: 1654, sentiment: 0.85 },
      { topic: "医药", mentions: 1432, sentiment: 0.65 },
      { topic: "消费", mentions: 1321, sentiment: 0.58 }
    ],
    sentimentTrend: [
      { date: "09-20", score: 0.62 },
      { date: "09-21", score: 0.65 },
      { date: "09-22", score: 0.68 },
      { date: "09-23", score: 0.64 },
      { date: "09-24", score: 0.63 },
      { date: "09-25", score: 0.65 }
    ],
    hotPosts: [
      { title: "新能源汽车行业深度分析", author: "价值投资者", views: 12500, comments: 876, sentiment: 0.75 },
      { title: "半导体产业链全景图", author: "芯片研究", views: 10200, comments: 765, sentiment: 0.82 },
      { title: "人工智能应用场景展望", author: "科技前沿", views: 9800, comments: 654, sentiment: 0.88 },
      { title: "医药行业投资机会", author: "医药研究员", views: 8500, comments: 543, sentiment: 0.65 },
      { title: "消费升级趋势分析", author: "消费洞察", views: 7800, comments: 432, sentiment: 0.72 }
    ]
  };
  
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">雪球等论坛数据分析</h4>
      <p class="text-muted mb-4">分析周期: ${forumData.period}</p>
      
      <div class="row mb-4">
        <div class="col-md-3">
          <div class="card shadow-sm h-100">
            <div class="card-body text-center">
              <h1 class="display-4 fw-bold">${forumData.summary.totalPosts.toLocaleString()}</h1>
              <p class="text-muted">总发帖量</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card shadow-sm h-100">
            <div class="card-body text-center">
              <h1 class="display-4 fw-bold">${forumData.summary.totalComments.toLocaleString()}</h1>
              <p class="text-muted">总评论量</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card shadow-sm h-100">
            <div class="card-body text-center">
              <h1 class="display-4 fw-bold">${forumData.summary.totalUsers.toLocaleString()}</h1>
              <p class="text-muted">活跃用户数</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card shadow-sm h-100">
            <div class="card-body text-center">
              <h1 class="display-4 fw-bold ${forumData.summary.sentimentScore > 0.6 ? 'text-success' : forumData.summary.sentimentScore > 0.4 ? 'text-warning' : 'text-danger'}">
                ${(forumData.summary.sentimentScore * 100).toFixed(0)}%
              </h1>
              <p class="text-muted">市场情绪指数</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">热门股票</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>代码</th>
                      <th>名称</th>
                      <th>提及次数</th>
                      <th>情绪指数</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${forumData.topStocks.map(stock => `
                      <tr>
                        <td>${stock.code}</td>
                        <td>${stock.name}</td>
                        <td>${stock.mentions}</td>
                        <td>
                          <div class="progress" style="height: 6px;">
                            <div class="progress-bar ${stock.sentiment > 0.6 ? 'bg-success' : stock.sentiment > 0.4 ? 'bg-warning' : 'bg-danger'}" 
                                 role="progressbar" 
                                 style="width: ${stock.sentiment * 100}%;" 
                                 aria-valuenow="${stock.sentiment * 100}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100"></div>
                          </div>
                          <small class="text-muted">${(stock.sentiment * 100).toFixed(0)}%</small>
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
              <h5 class="card-title mb-0">热门话题</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>话题</th>
                      <th>提及次数</th>
                      <th>情绪指数</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${forumData.topTopics.map(topic => `
                      <tr>
                        <td>${topic.topic}</td>
                        <td>${topic.mentions}</td>
                        <td>
                          <div class="progress" style="height: 6px;">
                            <div class="progress-bar ${topic.sentiment > 0.6 ? 'bg-success' : topic.sentiment > 0.4 ? 'bg-warning' : 'bg-danger'}" 
                                 role="progressbar" 
                                 style="width: ${topic.sentiment * 100}%;" 
                                 aria-valuenow="${topic.sentiment * 100}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100"></div>
                          </div>
                          <small class="text-muted">${(topic.sentiment * 100).toFixed(0)}%</small>
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
      
      <div class="card shadow-sm mb-4">
        <div class="card-header bg-light">
          <h5 class="card-title mb-0">市场情绪趋势</h5>
        </div>
        <div class="card-body">
          <div id="sentiment-trend-chart" style="height: 300px;"></div>
        </div>
      </div>
      
      <div class="card shadow-sm">
        <div class="card-header bg-light">
          <h5 class="card-title mb-0">热门帖子</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>标题</th>
                  <th>作者</th>
                  <th>浏览量</th>
                  <th>评论数</th>
                  <th>情绪指数</th>
                </tr>
              </thead>
              <tbody>
                ${forumData.hotPosts.map(post => `
                  <tr>
                    <td>${post.title}</td>
                    <td>${post.author}</td>
                    <td>${post.views.toLocaleString()}</td>
                    <td>${post.comments}</td>
                    <td>
                      <div class="progress" style="height: 6px;">
                        <div class="progress-bar ${post.sentiment > 0.6 ? 'bg-success' : post.sentiment > 0.4 ? 'bg-warning' : 'bg-danger'}" 
                             role="progressbar" 
                             style="width: ${post.sentiment * 100}%;" 
                             aria-valuenow="${post.sentiment * 100}" 
                             aria-valuemin="0" 
                             aria-valuemax="100"></div>
                      </div>
                      <small class="text-muted">${(post.sentiment * 100).toFixed(0)}%</small>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 更新容器内容
  container.innerHTML = moduleHTML;
  
  // 初始化图表
  initSentimentTrendChart(forumData);
}

// 初始化情绪趋势图表
function initSentimentTrendChart(data) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createSentimentTrendChart(data);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createSentimentTrendChart(data);
  }
}

// 创建情绪趋势图表
function createSentimentTrendChart(data) {
  const chartDom = document.getElementById('sentiment-trend-chart');
  if (!chartDom) return;
  
  const myChart = echarts.init(chartDom);
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        return params[0].name + '<br/>' + 
               params[0].marker + ' 情绪指数: ' + 
               (params[0].value * 100).toFixed(0) + '%';
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
      boundaryGap: false,
      data: data.sentimentTrend.map(item => item.date)
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 1,
      interval: 0.2,
      axisLabel: {
        formatter: function(value) {
          return (value * 100).toFixed(0) + '%';
        }
      }
    },
    series: [
      {
        name: '情绪指数',
        type: 'line',
        data: data.sentimentTrend.map(item => item.score),
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#5470c6'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgba(84, 112, 198, 0.5)'
            },
            {
              offset: 1,
              color: 'rgba(84, 112, 198, 0.1)'
            }
          ])
        },
        markLine: {
          data: [
            {
              name: '警戒线',
              yAxis: 0.4,
              lineStyle: {
                color: '#ff7675'
              },
              label: {
                formatter: '警戒线 (40%)',
                position: 'end'
              }
            }
          ]
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

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是雪球等论坛数据模块，则自动加载
  if (window.location.hash === '#forum-data-analysis') {
    loadForumDataAnalysis();
  }
});