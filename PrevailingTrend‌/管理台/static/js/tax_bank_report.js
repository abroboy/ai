/**
 * 税银报告模块
 * 大势所趋风险框架管理台 - 第三层模块
 */

// 加载税银报告模块
function loadTaxBankReport() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载税银报告数据...</p>
    </div>
  `;
  
  // 从API获取税银报告数据
  fetch('/api/tax-bank-report')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.data) {
        // 加载模块内容
        renderTaxBankReportModule(contentArea, data.data);
      } else {
        contentArea.innerHTML = `
          <div class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill"></i> 无法加载税银报告数据: ${data.message || '未知错误'}
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

// 渲染税银报告模块内容
function renderTaxBankReportModule(container, reportData) {
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">税银报告分析 - ${reportData.companyName} <span class="badge bg-danger">实时</span></h4>
      <p class="text-muted mb-4">${reportData.period}</p>
      
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">税务信息</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label text-muted small">纳税总额</label>
                <p class="fw-bold">${(reportData.taxInfo.totalTax / 10000).toFixed(2)} 万元</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small">纳税信用等级</label>
                <p class="fw-bold">${reportData.taxInfo.taxCompliance}</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small">欠税金额</label>
                <p class="fw-bold">${reportData.taxInfo.overdueTax} 元</p>
              </div>
              <div>
                <label class="form-label text-muted small">纳税信用积分</label>
                <p class="fw-bold">${reportData.taxInfo.taxCredits}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">银行信息</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label text-muted small">银行信用评级</label>
                <p class="fw-bold">${reportData.bankInfo.creditRating}</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small">贷款总额</label>
                <p class="fw-bold">${(reportData.bankInfo.loanAmount / 10000).toFixed(2)} 万元</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small">逾期贷款</label>
                <p class="fw-bold">${reportData.bankInfo.overdueLoan} 元</p>
              </div>
              <div>
                <label class="form-label text-muted small">授信额度</label>
                <p class="fw-bold">${(reportData.bankInfo.creditLines / 10000).toFixed(2)} 万元</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card shadow-sm mb-4">
        <div class="card-header bg-light">
          <h5 class="card-title mb-0">风险分析</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-4">
              <div class="text-center">
                <div class="display-4 fw-bold ${reportData.riskAssessment.taxRisk === '低风险' ? 'text-success' : reportData.riskAssessment.taxRisk === '中风险' ? 'text-warning' : 'text-danger'}">
                  ${reportData.riskAssessment.taxRisk}
                </div>
                <small class="text-muted">税务风险</small>
              </div>
            </div>
            <div class="col-md-4">
              <div class="text-center">
                <div class="display-4 fw-bold ${reportData.riskAssessment.financialRisk === '低风险' ? 'text-success' : reportData.riskAssessment.financialRisk === '中风险' ? 'text-warning' : 'text-danger'}">
                  ${reportData.riskAssessment.financialRisk}
                </div>
                <small class="text-muted">财务风险</small>
              </div>
            </div>
            <div class="col-md-4">
              <div class="text-center">
                <div class="display-4 fw-bold ${reportData.riskAssessment.overallRisk === '低风险' ? 'text-success' : reportData.riskAssessment.overallRisk === '中风险' ? 'text-warning' : 'text-danger'}">
                  ${reportData.riskAssessment.overallRisk}
                </div>
                <small class="text-muted">综合风险</small>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card shadow-sm">
        <div class="card-header bg-light">
          <h5 class="card-title mb-0">历史风险趋势</h5>
        </div>
        <div class="card-body">
          <div id="risk-trend-chart" style="height: 400px;"></div>
        </div>
      </div>
    </div>
  `;
  
  // 更新容器内容
  container.innerHTML = moduleHTML;
  
  // 初始化图表
  initRiskTrendChart(reportData);
}

// 初始化风险趋势图表
function initRiskTrendChart(data) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createRiskTrendChart(data);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createRiskTrendChart(data);
  }
}

// 创建风险趋势图表
function createRiskTrendChart(data) {
  const chartDom = document.getElementById('risk-trend-chart');
  if (!chartDom) return;
  
  const myChart = echarts.init(chartDom);
  
  // 风险等级映射为数值
  const riskLevelMap = { '低风险': 1, '中风险': 2, '高风险': 3 };
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        let result = params[0].name + '<br/>';
        params.forEach(function(item) {
          result += item.marker + ' ' + item.seriesName + ': ' + 
                   (item.value === 1 ? '低风险' : item.value === 2 ? '中风险' : '高风险') + '<br/>';
        });
        return result;
      }
    },
    legend: {
      data: ['税务风险', '财务风险', '综合风险']
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
      data: data.history.map(item => item.period)
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: function(value) {
          return value === 1 ? '低风险' : value === 2 ? '中风险' : '高风险';
        }
      },
      min: 0.5,
      max: 3.5,
      interval: 1
    },
    series: [
      {
        name: '税务风险',
        type: 'line',
        data: data.history.map(item => riskLevelMap[item.taxRisk]),
        smooth: true,
        lineStyle: {
          width: 3
        }
      },
      {
        name: '财务风险',
        type: 'line',
        data: data.history.map(item => riskLevelMap[item.financialRisk]),
        smooth: true,
        lineStyle: {
          width: 3
        }
      },
      {
        name: '综合风险',
        type: 'line',
        data: data.history.map(item => riskLevelMap[item.overallRisk]),
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
  // 如果当前页面是税银报告模块，则自动加载
  if (window.location.hash === '#tax-bank-report') {
    loadTaxBankReport();
  }
});