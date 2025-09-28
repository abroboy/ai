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
  
  // 从API获取论坛数据分析数据
  fetch('/api/forum-data-analysis')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data) {
        const forumData = data.data;
        renderForumDataAnalysisModule(contentArea, forumData);
      } else {
        contentArea.innerHTML = `
          <div class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill"></i> 无法加载论坛数据分析数据: ${data.message || '未知错误'}
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

// 渲染雪球等论坛数据模块内容
function renderForumDataAnalysisModule(container, forumData) {
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">雪球等论坛数据分析 <span class="badge bg-danger">实时</span></h4>
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