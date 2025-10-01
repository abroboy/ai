/*
 * 上市公司或行业分类模块 - CSV版本
 * 大势所趋风险框架管理台
 */

// 加载上市公司或行业分类模块
function loadWindIndustryClassification() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载上市公司全景数据...</p>
    </div>
  `;
  
  // 直接加载CSV股票数据
  loadCSVStockData();
}

// 不再使用的函数 - 保留以防其他地方调用
function renderWindIndustryModule(container) {
  loadCSVStockData();
}

// 从CSV数据准备图表数据 - 不再使用，但保留以防调用
function prepareChartDataFromCSV(industries) {
  return { categories: [], series: [] };
}

// 初始化行业图表 - 不再使用，但保留以防调用
function initIndustryChart(data) {
  console.log('Chart initialization skipped');
}

// 创建图表 - 不再使用，但保留以防调用
function createChart(data) {
  console.log('Chart creation skipped');
}

// 加载Bootstrap的JS - 不再使用，但保留以防调用
function loadBootstrapJS() {
  console.log('Bootstrap JS loading skipped');
}

// 搜索行业 - 不再使用，但保留以防调用
function searchIndustry() {
  console.log('Industry search skipped');
}

// 刷新行业数据 - 不再使用，但保留以防调用
function refreshIndustryData() {
  loadCSVStockData();
}

// 导出行业数据 - 不再使用，但保留以防调用
function exportIndustryData() {
  console.log('Industry data export skipped');
}

// 从CSV数据构建行业模块HTML - 不再使用，但保留以防调用
function buildIndustryModuleHTMLFromCSV(industries, statsData) {
  return '';
}

// 加载并渲染 CSV 股票数据
function loadCSVStockData() {
  const container = document.getElementById('content');
  if (!container) return;

  // 清空内容区域，只显示股票数据
  container.innerHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">国内上市公司全景</h4>
      <div id="csv-stock-card" class="card shadow-sm mb-4">
        <div class="card-header bg-light d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">股票数据</h5>
          <div class="d-flex gap-2">
            <input id="csv-search" type="text" placeholder="搜索 代码/名称" class="form-control form-control-sm" style="width:220px;">
            <button class="btn btn-sm btn-outline-primary" id="csv-search-btn"><i class="bi bi-search"></i> 搜索</button>
            <button class="btn btn-sm btn-outline-secondary" id="csv-reset-btn"><i class="bi bi-x-circle"></i> 重置</button>
          </div>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive" style="max-height: 580px; overflow: auto;">
            <table class="table table-hover table-striped mb-0">
              <thead id="csv-thead" class="table-light sticky-top"></thead>
              <tbody id="csv-tbody"></tbody>
            </table>
          </div>
        </div>
        <div class="card-footer bg-light d-flex justify-content-between">
          <small class="text-muted">数据来源：enhanced CSV文件 | 最后更新: <span id="data-last-updated">${new Date().toLocaleString()}</span></small>
          <div id="csv-stats" class="text-muted"></div>
        </div>
      </div>
    </div>
  `;

  // 直接读取本地CSV文件
  fetch('/api/akshare_test_enhanced_ak_stock_zh_a_new.csv')
    .then(response => {
      if (!response.ok) {
        throw new Error('无法加载CSV文件');
      }
      return response.text();
    })
    .then(csvText => {
      // 解析CSV文本
      const rows = parseCSV(csvText);
      // 转换为表格数据
      const tableData = convertCSVToTableData(rows);
      // 渲染表格
      renderCSVTable(tableData);

      // 绑定检索
      const searchInput = document.getElementById('csv-search');
      const searchBtn = document.getElementById('csv-search-btn');
      const resetBtn = document.getElementById('csv-reset-btn');
      if (searchBtn && resetBtn) {
        searchBtn.onclick = () => {
          const q = (searchInput?.value || '').trim().toLowerCase();
          const allTr = document.querySelectorAll('#csv-tbody tr');
          allTr.forEach(tr => {
            const code = (tr.getAttribute('data-code') || '').toLowerCase();
            const name = (tr.getAttribute('data-name') || '').toLowerCase();
            tr.style.display = (code.includes(q) || name.includes(q)) ? '' : 'none';
          });
        };
        resetBtn.onclick = () => {
          if (searchInput) searchInput.value = '';
          const allTr = document.querySelectorAll('#csv-tbody tr');
          allTr.forEach(tr => tr.style.display = '');
        };
      }
    })
    .catch((err) => {
      console.error('加载CSV数据失败:', err);
      const thead = document.getElementById('csv-thead');
      const tbody = document.getElementById('csv-tbody');
      if (thead && tbody) {
        thead.innerHTML = '<tr><th>错误</th></tr>';
        tbody.innerHTML = `<tr><td class="text-danger">无法加载CSV股票数据: ${err.message}</td></tr>`;
      }
    });
}

// 解析CSV文本为二维数组
function parseCSV(csvText) {
  const lines = csvText.split('\n');
  const result = [];
  
  // 跳过第一行标题行
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line) {
      // 简单的CSV解析，假设没有包含逗号的字段
      result.push(line.split(','));
    }
  }
  
  return result;
}

// 将CSV数据转换为表格数据对象
function convertCSVToTableData(csvRows) {
  const result = [];
  
  csvRows.forEach(row => {
    // 从CSV行数据创建表格数据对象
    // 根据CSV文件结构，列的顺序是：
    // 0: 市场+代码 (如bj920000)
    // 1: 代码 (如920000)
    // 2: 公司名称 (如安徽凤凰)
    // 3: 今开
    // 4: 最高
    // 5: 最低
    // 6: 成交量
    // 7: 成交额
    // 8: 总市值
    // 9: 换手率
    
    result.push({
      symbol: row[0],
      code: row[1],
      name: row[2],
      open: parseFloat(row[3]) || 0,
      high: parseFloat(row[4]) || 0,
      low: parseFloat(row[5]) || 0,
      volume: parseFloat(row[6]) || 0,
      amount: parseFloat(row[7]) || 0,
      mktcap: parseFloat(row[8]) || 0,
      turnoverratio: parseFloat(row[9]) || 0,
      // 根据代码前缀判断市场
      market: row[0].startsWith('bj') ? '北交所' : 
              row[0].startsWith('sh') ? '上交所' : 
              row[0].startsWith('sz') ? '深交所' : '未知'
    });
  });
  
  return result;
}

// 渲染CSV表格
function renderCSVTable(rows) {
  const thead = document.getElementById('csv-thead');
  const tbody = document.getElementById('csv-tbody');
  const stats = document.getElementById('csv-stats');
  if (!thead || !tbody) return;
  
  // 添加CSS样式确保数值水平显示
  const style = document.createElement('style');
  style.textContent = `
    /* 确保表格单元格内容水平显示 */
    #csv-tbody td {
      white-space: nowrap; /* 不换行 */
      text-align: right; /* 数值右对齐 */
      vertical-align: middle; /* 垂直居中 */
      max-width: 120px; /* 设置最大宽度 */
    }
    /* 公司名称等文本内容左对齐 */
    #csv-tbody td:nth-child(3) {
      text-align: left;
      max-width: 150px;
    }
    /* 股票代码列居中 */
    #csv-tbody td:nth-child(1),
    #csv-tbody td:nth-child(2) {
      text-align: center;
    }
    /* 表头样式 */
    #csv-thead th {
      text-align: center;
      vertical-align: middle;
      white-space: nowrap;
    }
  `;
  document.head.appendChild(style);

  // 定义中文列名映射
  const columnMap = {
    'symbol': '股票代码',
    'code': '代码',
    'name': '公司名称',
    'market': '市场',
    'open': '今开(元)',
    'high': '最高(元)',
    'low': '最低(元)',
    'volume': '成交量',
    'amount': '成交额',
    'mktcap': '总市值(亿元)',
    'turnoverratio': '换手率(%)'
  };

  // 使用标准字段顺序
  const standardColumns = ['symbol', 'code', 'name', 'market', 'open', 'high', 'low', 'volume', 'amount', 'mktcap', 'turnoverratio'];
  
  // 表头 - 显示中文名称
  thead.innerHTML = `
    <tr>
      ${standardColumns.map(c => `<th>${columnMap[c] || c}</th>`).join('')}
    </tr>
  `;

  // 表体
  const frag = document.createDocumentFragment();
  rows.forEach(r => {
    const tr = document.createElement('tr');
    tr.setAttribute('data-code', String(r['code'] || r['symbol'] || ''));
    tr.setAttribute('data-name', String(r['name'] || ''));
    tr.innerHTML = standardColumns.map(c => {
      const v = r[c];
      // 规范化展示
      if (v === null || typeof v === 'undefined' || (typeof v === 'number' && v === 0 && c !== 'open' && c !== 'high' && c !== 'low')) {
        return '<td>-</td>';
      }
      if (typeof v === 'number') {
        // 格式化数字显示
        if (c === 'volume' || c === 'amount') {
          return `<td>${v.toLocaleString()}</td>`;
        } else if (c === 'mktcap') {
          return `<td>${v.toFixed(2)}</td>`; // 已经是亿元单位
        } else if (c === 'turnoverratio') {
          return `<td>${v.toFixed(2)}</td>`;
        } else if (c === 'open' || c === 'high' || c === 'low') {
          return `<td>${v.toFixed(2)}</td>`;
        } else {
          return `<td>${Number.isFinite(v) ? v : ''}</td>`;
        }
      }
      return `<td>${String(v)}</td>`;
    }).join('');
    frag.appendChild(tr);
  });
  tbody.innerHTML = '';
  tbody.appendChild(frag);

  if (stats) {
    stats.textContent = `共 ${rows.length} 条记录，${standardColumns.length} 列`;
  }
}

// 显示行业详情
function showIndustryDetail(industryCode) {
  alert('行业详情功能：' + industryCode + ' 将在后续版本中实现');
}

// 查看行业公司列表
function viewCompanies(industryCode) {
  alert('查看公司列表功能：' + industryCode + ' 将在后续版本中实现');
}

document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是上市公司或行业分类模块，则自动加载
  if (window.location.hash === '#wind-industry') {
    loadWindIndustryClassification();
  }
});