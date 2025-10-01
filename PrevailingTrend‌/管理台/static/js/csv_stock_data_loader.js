/*
 * CSV股票数据加载器
 * 用于从CSV文件加载和显示股票数据
 */

// 加载并渲染 CSV 股票数据
function loadCSVStockData() {
  const container = document.getElementById('content');
  if (!container) return;

  // 如果已存在，避免重复插入
  if (!document.getElementById('csv-stock-card')) {
    const card = document.createElement('div');
    card.id = 'csv-stock-card';
    card.className = 'card shadow-sm mb-4';
    card.innerHTML = `
      <div class="card-header bg-light d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">CSV 股票数据 <span class="badge bg-success">实时</span></h5>
        <div class="d-flex gap-2">
          <input id="csv-search" type="text" placeholder="搜索 代码/名称" class="form-control form-control-sm" style="width:220px;">
          <button class="btn btn-sm btn-outline-primary" id="csv-search-btn"><i class="bi bi-search"></i> 搜索</button>
          <button class="btn btn-sm btn-outline-secondary" id="csv-reset-btn"><i class="bi bi-x-circle"></i> 重置</button>
          <button class="btn btn-sm btn-primary" id="csv-refresh-btn"><i class="bi bi-arrow-clockwise"></i> 刷新</button>
        </div>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive" style="max-height: 480px; overflow: auto;">
          <table class="table table-hover table-striped mb-0">
            <thead id="csv-thead" class="table-light sticky-top">
              <tr>
                <th>代码</th>
                <th>名称</th>
                <th>开盘价</th>
                <th>最高价</th>
                <th>最低价</th>
                <th>成交量</th>
                <th>成交额</th>
                <th>市值(亿)</th>
                <th>换手率(%)</th>
                <th>行业</th>
              </tr>
            </thead>
            <tbody id="csv-tbody"></tbody>
          </table>
        </div>
      </div>
      <div class="card-footer bg-light d-flex justify-content-between">
        <small class="text-muted">数据来源：CSV文件 | 实时更新</small>
        <div id="csv-stats" class="text-muted"></div>
      </div>
    `;
    container.prepend(card);
  }

  // 加载CSV数据
  loadCSVDataFromAPI();
}

// 从API加载CSV数据
function loadCSVDataFromAPI() {
  fetch('/api/listed-companies?page=0&size=1000')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data && data.data.content) {
        renderCSVTable(data.data.content);
        bindCSVSearchEvents();
      } else {
        showCSVError('无法加载CSV数据: ' + (data.message || '未知错误'));
      }
    })
    .catch(error => {
      showCSVError('请求失败: ' + error.message);
    });
}

// 渲染CSV表格
function renderCSVTable(stocks) {
  const tbody = document.getElementById('csv-tbody');
  const stats = document.getElementById('csv-stats');
  if (!tbody) return;

  const frag = document.createDocumentFragment();
  stocks.forEach(stock => {
    const tr = document.createElement('tr');
    tr.setAttribute('data-code', String(stock.code || ''));
    tr.setAttribute('data-name', String(stock.name || ''));
    tr.innerHTML = `
      <td>${stock.code || ''}</td>
      <td>${stock.name || ''}</td>
      <td>${formatNumber(stock.open)}</td>
      <td>${formatNumber(stock.high)}</td>
      <td>${formatNumber(stock.low)}</td>
      <td>${formatNumber(stock.volume, 0)}</td>
      <td>${formatNumber(stock.amount)}</td>
      <td>${formatNumber(stock.market_cap_billion)}</td>
      <td>${formatNumber(stock.turnoverratio)}</td>
      <td><span class="badge bg-secondary">${stock.industry || '未知'}</span></td>
    `;
    frag.appendChild(tr);
  });
  
  tbody.innerHTML = '';
  tbody.appendChild(frag);

  if (stats) {
    stats.textContent = `共 ${stocks.length} 条记录`;
  }
}

// 绑定CSV搜索事件
function bindCSVSearchEvents() {
  const searchInput = document.getElementById('csv-search');
  const searchBtn = document.getElementById('csv-search-btn');
  const resetBtn = document.getElementById('csv-reset-btn');
  const refreshBtn = document.getElementById('csv-refresh-btn');
  
  if (searchBtn) {
    searchBtn.onclick = () => {
      const q = (searchInput?.value || '').trim().toLowerCase();
      const allTr = document.querySelectorAll('#csv-tbody tr');
      allTr.forEach(tr => {
        const code = (tr.getAttribute('data-code') || '').toLowerCase();
        const name = (tr.getAttribute('data-name') || '').toLowerCase();
        tr.style.display = (code.includes(q) || name.includes(q)) ? '' : 'none';
      });
    };
  }
  
  if (resetBtn) {
    resetBtn.onclick = () => {
      if (searchInput) searchInput.value = '';
      const allTr = document.querySelectorAll('#csv-tbody tr');
      allTr.forEach(tr => tr.style.display = '');
    };
  }
  
  if (refreshBtn) {
    refreshBtn.onclick = () => {
      loadCSVDataFromAPI();
    };
  }
}

// 显示CSV错误信息
function showCSVError(message) {
  const tbody = document.getElementById('csv-tbody');
  if (tbody) {
    tbody.innerHTML = `<tr><td colspan="10" class="text-danger text-center">${message}</td></tr>`;
  }
}

// 格式化数字显示
function formatNumber(value, decimals = 2) {
  if (value === null || value === undefined || value === '') return '-';
  const num = parseFloat(value);
  if (isNaN(num)) return '-';
  return num.toLocaleString('zh-CN', { 
    minimumFractionDigits: decimals, 
    maximumFractionDigits: decimals 
  });
}