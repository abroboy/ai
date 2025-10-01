/**
 * 国内热点数据模块
 * 大势所趋风险框架管理台
 */

// 加载国内热点数据模块
function loadDomesticHotspotData() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载国内热点数据...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderDomesticHotspotModule(contentArea);
  }, 800);
}

// 渲染国内热点数据模块内容
function renderDomesticHotspotModule(container) {
  // 从API获取国内热点数据
  fetch('/api/domestic-hotspot')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data) {
        const hotspotData = data.data;
        const stats = data.stats || {};
        
        // 类别分布数据（用于图表）
        const categories = Object.keys(stats.categories || {});
        const categoryCounts = Object.values(stats.categories || {});
        
        const categoryData = {
          categories: categories,
          values: categoryCounts
        };
        
        // 构建模块HTML
        const moduleHTML = buildDomesticHotspotModuleHTML(hotspotData, stats);
        container.innerHTML = moduleHTML;
        
        // 初始化图表
        initCategoryChart(categoryData);
        
        // 加载Bootstrap的Modal组件
        loadBootstrapJS();
        
        // 更新最后更新时间
        document.getElementById('domestic-hotspot-last-updated').textContent = new Date().toLocaleString();
      } else {
        container.innerHTML = `
          <div class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill"></i> 无法加载国内热点数据: ${data.message || '未知错误'}
          </div>
        `;
      }
    })
    .catch(error => {
      // 如果API不可用，使用模拟数据
      console.warn('API不可用，使用模拟数据:', error);
      renderWithMockData(container);
    });
}

// 使用模拟数据渲染
function renderWithMockData(container) {
  // 模拟国内热点数据
  const hotspotData = [
    { id: 1, title: "央行宣布降准0.25个百分点 释放流动性约5000亿元", source: "人民银行", date: "2025-10-01", impact: 95, region: "全国", category: "货币政策" },
    { id: 2, title: "国家发改委：前三季度GDP同比增长5.2%", source: "国家发改委", date: "2025-09-30", impact: 88, region: "全国", category: "经济数据" },
    { id: 3, title: "科创板注册制改革再深化 新增行业覆盖范围", source: "上海证券交易所", date: "2025-09-29", impact: 82, region: "上海", category: "资本市场" },
    { id: 4, title: "新能源汽车产销量连续9个月保持增长", source: "中汽协", date: "2025-09-28", impact: 79, region: "全国", category: "产业发展" },
    { id: 5, title: "房地产市场调控政策优化 一线城市限购松绑", source: "住建部", date: "2025-09-27", impact: 85, region: "一线城市", category: "房地产" }
  ];
  
  // 模拟统计数据
  const stats = {
    total_count: 5,
    high_impact_count: 3,
    categories: {
      "货币政策": 1,
      "经济数据": 1,
      "资本市场": 1,
      "产业发展": 1,
      "房地产": 1
    },
    avg_impact: 85.8
  };
  
  // 类别分布数据（用于图表）
  const categoryData = {
    categories: Object.keys(stats.categories),
    values: Object.values(stats.categories)
  };
  
  // 构建模块HTML
  const moduleHTML = buildDomesticHotspotModuleHTML(hotspotData, stats);
  container.innerHTML = moduleHTML;
  
  // 初始化图表
  initCategoryChart(categoryData);
  
  // 加载Bootstrap的Modal组件
  loadBootstrapJS();
  
  // 显示数据来源提示
  const alertDiv = document.createElement('div');
  alertDiv.className = 'alert alert-warning alert-dismissible fade show mt-3';
  alertDiv.innerHTML = `
    <i class="bi bi-exclamation-triangle-fill"></i> 当前显示为模拟数据，请连接真实数据源以获取最新信息。
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  container.insertBefore(alertDiv, container.firstChild);
}