/**
 * 财务三表模块
 * 大势所趋风险框架管理台 - 第三层模块
 */

// 加载财务三表模块
function loadFinancialStatements() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载财务三表数据...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderFinancialStatementsModule(contentArea);
  }, 800);
}

// 渲染财务三表模块内容
function renderFinancialStatementsModule(container) {
  // 模拟财务数据
  const financialData = {
    companyName: "示例科技有限公司",
    period: "2025年第三季度",
    balanceSheet: {
      assets: 1250000000,
      liabilities: 750000000,
      equity: 500000000
    },
    incomeStatement: {
      revenue: 450000000,
      cost: 280000000,
      profit: 120000000
    },
    cashFlow: {
      operating: 85000000,
      investing: -35000000,
      financing: 20000000
    },
    ratios: {
      currentRatio: 1.8,
      debtToEquity: 1.5,
      grossMargin: 0.38,
      roe: 0.24
    },
    history: [
      { period: "2025Q2", revenue: 420000000, profit: 110000000, assets: 1200000000 },
      { period: "2025Q1", revenue: 380000000, profit: 95000000, assets: 1150000000 },
      { period: "2024Q4", revenue: 400000000, profit: 105000000, assets: 1100000000 }
    ]
  };
  
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">财务三表分析 - ${financialData.companyName}</h4>
      <p class="text-muted mb-4">${financialData.period}</p>
      
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">资产负债表</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label text-muted small">总资产</label>
                <p class="fw-bold">${(financialData.balanceSheet.assets / 100000000).toFixed(2)} 亿元</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small">总负债</label>
                <p class="fw-bold">${(financialData.balanceSheet.liabilities / 100000000).toFixed(2)} 亿元</p>
              </div>
              <div>
                <label class="form-label text-muted small">所有者权益</label>
                <p class="fw-bold">${(financialData.balanceSheet.equity / 100000000).toFixed(2)} 亿元</p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">利润表</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label text-muted small">营业收入</label>
                <p class="fw-bold">${(financialData.incomeStatement.revenue / 100000000).toFixed(2)} 亿元</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small">营业成本</label>
                <p class="fw-bold">${(financialData.incomeStatement.cost / 100000000).toFixed(2)} 亿元</p>
              </div>
              <div>
                <label class="form-label text-muted small">净利润</label>
                <p class="fw-bold">${(financialData.incomeStatement.profit / 100000000).toFixed(2)} 亿元</p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">现金流量表</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label text-muted small">经营活动现金流</label>
                <p class="fw-bold">${(financialData.cashFlow.operating / 10000000).toFixed(2)} 千万元</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small">投资活动现金流</label>
                <p class="fw-bold">${(financialData.cashFlow.investing / 10000000).toFixed(2)} 千万元</p>
              </div>
              <div>
                <label class="form-label text-muted small">筹资活动现金流</label>
                <p class="fw-bold">${(financialData.cashFlow.financing / 10000000).toFixed(2)} 千万元</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card shadow-sm mb-4">
        <div class="card-header bg-light">
          <h5 class="card-title mb-0">财务比率</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-3">
              <div class="text-center">
                <div class="display-4 fw-bold">${financialData.ratios.currentRatio}</div>
                <small class="text-muted">流动比率</small>
              </div>
            </div>
            <div class="col-md-3">
              <div class="text-center">
                <div class="display-4 fw-bold">${financialData.ratios.debtToEquity}</div>
                <small class="text-muted">资产负债率</small>
              </div>
            </div>
            <div class="col-md-3">
              <div class="text-center">
                <div class="display-4 fw-bold">${(financialData.ratios.grossMargin * 100).toFixed(0)}%</div>
                <small class="text-muted">毛利率</small>
              </div>
            </div>
            <div class="col-md-3">
              <div class="text-center">
                <div class="display-4 fw-bold">${(financialData.ratios.roe * 100).toFixed(0)}%</div>
                <small class="text-muted">净资产收益率</small>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card shadow-sm">
        <div class="card-header bg-light">
          <h5 class="card-title mb-0">历史财务趋势</h5>
        </div>
        <div class="card-body">
          <div id="financial-trend-chart" style="height: 400px;"></div>
        </div>
      </div>
    </div>
  `;
  
  // 更新容器内容
  container.innerHTML = moduleHTML;
  
  // 初始化图表
  initFinancialTrendChart(financialData);
}

// 初始化财务趋势图表
function initFinancialTrendChart(data) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createFinancialTrendChart(data);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createFinancialTrendChart(data);
  }
}

// 创建财务趋势图表
function createFinancialTrendChart(data) {
  const chartDom = document.getElementById('financial-trend-chart');
  if (!chartDom) return;
  
  const myChart = echarts.init(chartDom);
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999'
        }
      }
    },
    legend: {
      data: ['营业收入', '净利润', '总资产']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        data: data.history.map(item => item.period),
        axisPointer: {
          type: 'shadow'
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: '金额(亿元)',
        min: 0,
        axisLabel: {
          formatter: '{value}'
        }
      },
      {
        type: 'value',
        name: '金额(亿元)',
        min: 0,
        axisLabel: {
          formatter: '{value}'
        }
      }
    ],
    series: [
      {
        name: '营业收入',
        type: 'bar',
        data: data.history.map(item => (item.revenue / 100000000).toFixed(2)),
        barWidth: '30%'
      },
      {
        name: '净利润',
        type: 'bar',
        data: data.history.map(item => (item.profit / 100000000).toFixed(2)),
        barWidth: '30%'
      },
      {
        name: '总资产',
        type: 'line',
        yAxisIndex: 1,
        data: data.history.map(item => (item.assets / 100000000).toFixed(2)),
        smooth: true,
        lineStyle: {
          width: 3
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
  // 如果当前页面是财务三表模块，则自动加载
  if (window.location.hash === '#financial-statements') {
    loadFinancialStatements();
  }
});