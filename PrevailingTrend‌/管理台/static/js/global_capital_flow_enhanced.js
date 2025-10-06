/**
 * 全球资金流向增强版主模块
 */

// 全局变量
let globalCapitalFlowChart = null;
let currentGlobalData = null;
let enhancedMapInstance = null;
let selectedRegion = null;

// 加载增强版全球资金流向模块
function loadGlobalCapitalFlowEnhanced() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载全球资金流向数据...</p>
    </div>
  `;
  
  // 加载增强版内容
  renderEnhancedGlobalCapitalFlow(contentArea);
}

// 渲染增强版全球资金流向界面
function renderEnhancedGlobalCapitalFlow(container) {
  const enhancedHTML = `
    <div class="container-fluid">
      <!-- 标题和控制面板 -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-0">
                <i class="bi bi-globe2 text-primary me-2"></i>
                全球资金流向地图 <span class="badge bg-success">增强版</span>
              </h2>
              <p class="text-muted mb-0">实时监控全球主要市场资金流向变化</p>
            </div>
            <div class="btn-group">
              <button class="btn btn-outline-primary btn-sm" onclick="refreshGlobalData()" 
                      title="刷新数据">
                <i class="bi bi-arrow-clockwise"></i>
              </button>
              <button class="btn btn-outline-success btn-sm" onclick="exportGlobalData()" 
                      title="导出数据">
                <i class="bi bi-download"></i>
              </button>
              <button class="btn btn-outline-info btn-sm" onclick="toggleMapFullscreen()" 
                      title="全屏显示">
                <i class="bi bi-fullscreen"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 关键指标卡片 -->
      <div class="row mb-4" id="key-metrics-cards">
        <!-- 动态生成 -->
      </div>

      <!-- 地图和图表区域 -->
      <div class="row mb-4">
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="bi bi-map me-2"></i>全球资金流向地图
              </h5>
              <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-primary active" onclick="setMapView('flow')">
                  资金流向
                </button>
                <button class="btn btn-outline-info" onclick="setMapView('heat')">
                  热力图
                </button>
              </div>
            </div>
            <div class="card-body p-0">
              <div id="global-capital-map" style="height: 500px; width: 100%;"></div>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">
                <i class="bi bi-graph-up me-2"></i>趋势图表
              </h5>
            </div>
            <div class="card-body">
              <div id="capital-flow-trend-chart" style="height: 400px;"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 数据表格区域 -->
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="bi bi-table me-2"></i>实时数据表格
              </h5>
              <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-secondary" onclick="sortTableByNetFlow()" 
                        title="按净流入排序">
                  <i class="bi bi-sort-numeric-down"></i>
                </button>
                <button class="btn btn-outline-success" onclick="filterPositiveFlow()" 
                        title="显示净流入">
                  <i class="bi bi-arrow-up-circle"></i>
                </button>
                <button class="btn btn-outline-danger" onclick="filterNegativeFlow()" 
                        title="显示净流出">
                  <i class="bi bi-arrow-down-circle"></i>
                </button>
                <button class="btn btn-outline-primary" onclick="showAllRegions()" 
                        title="显示全部">
                  <i class="bi bi-eye"></i>
                </button>
              </div>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th onclick="sortTable(0)" style="cursor: pointer;">
                        地区/市场 <i class="bi bi-arrow-down-up"></i>
                      </th>
                      <th onclick="sortTable(1)" style="cursor: pointer;">
                        净流入(亿美元) <i class="bi bi-arrow-down-up"></i>
                      </th>
                      <th onclick="sortTable(2)" style="cursor: pointer;">
                        变化率(%) <i class="bi bi-arrow-down-up"></i>
                      </th>
                      <th onclick="sortTable(3)" style="cursor: pointer;">
                        资金流入 <i class="bi bi-arrow-down-up"></i>
                      </th>
                      <th onclick="sortTable(4)" style="cursor: pointer;">
                        资金流出 <i class="bi bi-arrow-down-up"></i>
                      </th>
                      <th>更新时间</th>
                      <th>操作</th>
                    </tr>
                  </thead>
                  <tbody id="realtime-data-table">
                    <!-- 动态生成 -->
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  
  container.innerHTML = enhancedHTML;
  
  // 加载数据和初始化组件
  fetchGlobalCapitalFlowData();
  
  // 初始化增强功能
  setTimeout(() => {
    initializeEnhancedFeatures();
  }, 1000);
}

// 获取全球资金流向数据
async function fetchGlobalCapitalFlowData() {
  try {
    const response = await fetch('/api/global-capital-flow');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    currentGlobalData = data;
    
    // 渲染各个组件
    renderKeyMetricsCards(data.summary);
    renderRealtimeDataTable(data.data);
    initializeWorldMap(data.data);
    
    // 如果有历史数据，渲染趋势图
    if (data.historical) {
      initializeTrendChart(data.historical);
    }
    
  } catch (error) {
    console.error('获取全球资金流向数据失败:', error);
    showNotification('数据加载失败，显示模拟数据', 'warning');
    
    // 使用模拟数据
    const mockData = generateMockGlobalData();
    currentGlobalData = mockData;
    renderKeyMetricsCards(mockData.summary);
    renderRealtimeDataTable(mockData.data);
    initializeWorldMap(mockData.data);
    initializeTrendChart(mockData.historical);
  }
}

// 渲染关键指标卡片
function renderKeyMetricsCards(summary) {
  const container = document.getElementById('key-metrics-cards');
  if (!container || !summary) return;
  
  const cards = [
    {
      title: '全球净流入',
      value: `${summary.totalNetInflow >= 0 ? '+' : ''}${summary.totalNetInflow.toFixed(1)}`,
      unit: '亿美元',
      icon: 'bi-globe2',
      color: summary.totalNetInflow >= 0 ? 'success' : 'danger',
      change: summary.totalChange
    },
    {
      title: '活跃市场',
      value: summary.activeMarkets,
      unit: '个',
      icon: 'bi-graph-up',
      color: 'info',
      change: null
    },
    {
      title: '最大净流入',
      value: `+${summary.maxInflow.toFixed(1)}`,
      unit: '亿美元',
      icon: 'bi-arrow-up-circle',
      color: 'success',
      change: null
    },
    {
      title: '最大净流出',
      value: `${summary.maxOutflow.toFixed(1)}`,
      unit: '亿美元',
      icon: 'bi-arrow-down-circle', 
      color: 'danger',
      change: null
    }
  ];
  
  const cardsHTML = cards.map(card => `
    <div class="col-lg-3 col-md-6 mb-3">
      <div class="card border-0 shadow-sm">
        <div class="card-body text-center">
          <div class="d-flex align-items-center justify-content-center mb-2">
            <div class="rounded-circle bg-${card.color}-subtle p-3">
              <i class="${card.icon} text-${card.color} fs-4"></i>
            </div>
          </div>
          <h3 class="text-${card.color} mb-1">${card.value}</h3>
          <p class="text-muted mb-1">${card.title}</p>
          <small class="text-muted">${card.unit}</small>
          ${card.change !== null ? `
            <div class="mt-2">
              <span class="badge bg-${card.change >= 0 ? 'success' : 'danger'}-subtle text-${card.change >= 0 ? 'success' : 'danger'}">
                ${card.change >= 0 ? '+' : ''}${card.change.toFixed(1)}%
              </span>
            </div>
          ` : ''}
        </div>
      </div>
    </div>
  `).join('');
  
  container.innerHTML = cardsHTML;
}

// 渲染实时数据表格
function renderRealtimeDataTable(data) {
  const tbody = document.getElementById('realtime-data-table');
  if (!tbody || !data) return;
  
  const rows = data.map((item, index) => `
    <tr onclick="showRegionDetailModal('${item.region}')" style="cursor: pointer;">
      <td>
        <div class="d-flex align-items-center">
          <div class="flag-icon me-2" style="width: 24px; height: 16px; background: linear-gradient(45deg, #007bff, #28a745); border-radius: 2px;"></div>
          <strong>${item.region}</strong>
        </div>
      </td>
      <td class="${item.netFlow >= 0 ? 'text-success' : 'text-danger'}">
        <strong>${item.netFlow >= 0 ? '+' : ''}${item.netFlow.toFixed(1)}</strong>
      </td>
      <td>
        <span class="badge bg-${item.change >= 0 ? 'success' : 'danger'}-subtle text-${item.change >= 0 ? 'success' : 'danger'}">
          ${item.change >= 0 ? '+' : ''}${item.change.toFixed(1)}%
        </span>
      </td>
      <td class="text-success">+${item.inflow.toFixed(1)}</td>
      <td class="text-danger">-${item.outflow.toFixed(1)}</td>
      <td>
        <small class="text-muted">${item.date}</small>
      </td>
      <td>
        <button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); selectRegionOnMap('${item.region}')" title="定位">
          <i class="bi bi-geo-alt"></i>
        </button>
      </td>
    </tr>
  `).join('');
  
  tbody.innerHTML = rows;
}

// 生成模拟数据
function generateMockGlobalData() {
  const regions = [
    { name: '北美', lat: 45.0, lng: -100.0, code: 'NA' },
    { name: '欧洲', lat: 50.0, lng: 10.0, code: 'EU' },
    { name: '亚太', lat: 35.0, lng: 120.0, code: 'AP' },
    { name: '日本', lat: 36.2048, lng: 138.2529, code: 'JP' },
    { name: '中国', lat: 35.8617, lng: 104.1954, code: 'CN' },
    { name: '新兴市场', lat: -15.0, lng: -50.0, code: 'EM' },
    { name: '英国', lat: 55.3781, lng: -3.4360, code: 'GB' },
    { name: '德国', lat: 51.1657, lng: 10.4515, code: 'DE' },
    { name: '法国', lat: 46.2276, lng: 2.2137, code: 'FR' },
    { name: '韩国', lat: 35.9078, lng: 127.7669, code: 'KR' },
    { name: '印度', lat: 20.5937, lng: 78.9629, code: 'IN' },
    { name: '巴西', lat: -14.2350, lng: -51.9253, code: 'BR' }
  ];
  
  const data = regions.map(regionInfo => {
    const inflow = Math.random() * 1000 + 100;
    const outflow = Math.random() * 800 + 50;
    const netFlow = inflow - outflow;
    const change = (Math.random() - 0.5) * 20;
    
    return {
      region: regionInfo.name,
      lat: regionInfo.lat,
      lng: regionInfo.lng,
      code: regionInfo.code,
      inflow,
      outflow,
      netFlow,
      change,
      date: new Date().toLocaleDateString('zh-CN'),
      volume: inflow + outflow,
      volatility: Math.abs(change),
      trend: change >= 0 ? 'up' : 'down'
    };
  });
  
  const summary = {
    totalNetInflow: data.reduce((sum, item) => sum + item.netFlow, 0),
    totalChange: (Math.random() - 0.5) * 10,
    activeMarkets: data.length,
    maxInflow: Math.max(...data.map(item => item.netFlow)),
    maxOutflow: Math.min(...data.map(item => item.netFlow))
  };
  
  // 生成历史数据
  const dates = [];
  const series = [];
  
  for (let i = 6; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    dates.push(date.toLocaleDateString('zh-CN'));
  }
  
  regions.slice(0, 6).forEach(region => {
    const regionSeries = {
      name: region,
      data: dates.map(() => (Math.random() - 0.5) * 500)
    };
    series.push(regionSeries);
  });
  
  return {
    data,
    summary,
    historical: { dates, series }
  };
}

// 设置地图视图模式
function setMapView(mode) {
  const buttons = document.querySelectorAll('.btn-group button');
  buttons.forEach(btn => btn.classList.remove('active'));
  
  event.target.classList.add('active');
  
  if (enhancedMapInstance) {
    // 根据模式更新地图显示
    updateMapView(mode);
  }
}

// 表格排序功能
function sortTable(columnIndex) {
  const table = document.querySelector('#realtime-data-table').closest('table');
  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  
  // 获取当前排序状态
  const isAscending = table.dataset.sortOrder !== 'asc';
  table.dataset.sortOrder = isAscending ? 'asc' : 'desc';
  
  rows.sort((a, b) => {
    let aValue = a.cells[columnIndex].textContent.trim();
    let bValue = b.cells[columnIndex].textContent.trim();
    
    // 处理数字列
    if (columnIndex > 0 && columnIndex < 5) {
      aValue = parseFloat(aValue.replace(/[+,%]/g, ''));
      bValue = parseFloat(bValue.replace(/[+,%]/g, ''));
    }
    
    if (aValue < bValue) return isAscending ? -1 : 1;
    if (aValue > bValue) return isAscending ? 1 : -1;
    return 0;
  });
  
  rows.forEach(row => tbody.appendChild(row));
}

// 更新地图视图
function updateMapView(mode) {
  if (!enhancedMapInstance || !currentGlobalData) return;
  
  // 清除现有标记
  enhancedMapInstance.eachLayer(layer => {
    if (layer instanceof L.CircleMarker) {
      enhancedMapInstance.removeLayer(layer);
    }
  });
  
  // 根据模式重新添加数据点
  addDataPointsToMapByType(currentGlobalData.data, mode);
}

// 实时数据更新
function startRealTimeUpdates() {
  setInterval(() => {
    if (currentGlobalData && currentGlobalData.data) {
      // 模拟数据更新
      currentGlobalData.data.forEach(item => {
        const changeRate = (Math.random() - 0.5) * 0.1; // ±5%的变化
        item.netFlow *= (1 + changeRate);
        item.change = changeRate * 100;
        item.date = new Date().toLocaleTimeString('zh-CN');
      });
      
      // 更新显示
      renderRealtimeDataTable(currentGlobalData.data);
      renderKeyMetricsCards(calculateSummary(currentGlobalData.data));
      
      // 更新地图
      if (enhancedMapInstance) {
        updateMapView(currentMapView || 'net');
      }
    }
  }, 30000); // 每30秒更新一次
}

// 计算汇总数据
function calculateSummary(data) {
  const totalNetInflow = data.reduce((sum, item) => sum + item.netFlow, 0);
  const totalChange = data.reduce((sum, item) => sum + item.change, 0) / data.length;
  const activeMarkets = data.length;
  const maxInflow = Math.max(...data.map(item => item.netFlow));
  const maxOutflow = Math.min(...data.map(item => item.netFlow));
  
  return {
    totalNetInflow,
    totalChange,
    activeMarkets,
    maxInflow,
    maxOutflow
  };
}

// 数据筛选功能
function filterDataByRegion(regionName) {
  const rows = document.querySelectorAll('#realtime-data-table tr');
  rows.forEach(row => {
    const regionCell = row.cells[0];
    const matches = regionCell.textContent.toLowerCase().includes(regionName.toLowerCase());
    row.style.display = matches ? '' : 'none';
  });
}

// 搜索功能
function searchRegions(searchTerm) {
  if (!searchTerm) {
    showAllRegions();
    return;
  }
  
  const rows = document.querySelectorAll('#realtime-data-table tr');
  rows.forEach(row => {
    const regionText = row.cells[0].textContent.toLowerCase();
    const matches = regionText.includes(searchTerm.toLowerCase());
    row.style.display = matches ? '' : 'none';
  });
}

// 初始化增强功能
function initializeEnhancedFeatures() {
  // 启动实时更新
  startRealTimeUpdates();
  
  // 添加搜索框
  addSearchBox();
  
  // 添加快捷操作
  addQuickActions();
  
  // 初始化键盘快捷键
  initializeKeyboardShortcuts();
}

// 添加搜索框
function addSearchBox() {
  const cardHeader = document.querySelector('#realtime-data-table').closest('.card').querySelector('.card-header');
  if (!cardHeader) return;
  
  const searchHTML = `
    <div class="input-group input-group-sm" style="width: 200px;">
      <input type="text" class="form-control" placeholder="搜索地区..." 
             onkeyup="searchRegions(this.value)" id="region-search">
      <button class="btn btn-outline-secondary" onclick="document.getElementById('region-search').value=''; showAllRegions();">
        <i class="bi bi-x"></i>
      </button>
    </div>
  `;
  
  cardHeader.insertAdjacentHTML('beforeend', searchHTML);
}

// 添加快捷操作
function addQuickActions() {
  const container = document.querySelector('.container-fluid');
  if (!container) return;
  
  const quickActionsHTML = `
    <div class="row mb-3">
      <div class="col-12">
        <div class="card bg-light">
          <div class="card-body py-2">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex gap-2">
                <button class="btn btn-sm btn-outline-primary" onclick="autoRefresh()" title="自动刷新">
                  <i class="bi bi-arrow-repeat"></i> 自动刷新
                </button>
                <button class="btn btn-sm btn-outline-success" onclick="exportToExcel()" title="导出Excel">
                  <i class="bi bi-file-earmark-excel"></i> Excel
                </button>
                <button class="btn btn-sm btn-outline-info" onclick="shareData()" title="分享数据">
                  <i class="bi bi-share"></i> 分享
                </button>
              </div>
              <div class="text-muted small">
                <i class="bi bi-clock"></i> 最后更新: <span id="last-update-time">${new Date().toLocaleTimeString('zh-CN')}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  
  container.insertAdjacentHTML('afterbegin', quickActionsHTML);
}

// 初始化键盘快捷键
function initializeKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey) {
      switch(e.key) {
        case 'r':
          e.preventDefault();
          refreshGlobalData();
          break;
        case 'e':
          e.preventDefault();
          exportGlobalData();
          break;
        case 'f':
          e.preventDefault();
          document.getElementById('region-search')?.focus();
          break;
      }
    }
  });
}

// 自动刷新功能
let autoRefreshInterval = null;
function autoRefresh() {
  if (autoRefreshInterval) {
    clearInterval(autoRefreshInterval);
    autoRefreshInterval = null;
    showNotification('自动刷新已停止', 'info');
  } else {
    autoRefreshInterval = setInterval(() => {
      refreshGlobalData();
      document.getElementById('last-update-time').textContent = new Date().toLocaleTimeString('zh-CN');
    }, 60000); // 每分钟刷新
    showNotification('自动刷新已启动', 'success');
  }
}

// 导出Excel功能
function exportToExcel() {
  if (!currentGlobalData) {
    showNotification('没有可导出的数据', 'warning');
    return;
  }
  
  // 这里可以集成第三方Excel导出库
  showNotification('Excel导出功能开发中...', 'info');
}

// 分享数据功能
function shareData() {
  if (navigator.share) {
    navigator.share({
      title: '全球资金流向数据',
      text: '查看最新的全球资金流向分析',
      url: window.location.href
    });
  } else {
    // 复制链接到剪贴板
    navigator.clipboard.writeText(window.location.href).then(() => {
      showNotification('链接已复制到剪贴板', 'success');
    });
  }
}