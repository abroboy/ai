/**
 * 全球资金流向数据分析模块
 */

// 数据验证功能
function validateGlobalData(data) {
  if (!data || !Array.isArray(data)) {
    return { valid: false, message: '数据格式无效' };
  }
  
  const requiredFields = ['region', 'inflow', 'outflow', 'netFlow', 'change'];
  
  for (let i = 0; i < data.length; i++) {
    const item = data[i];
    for (const field of requiredFields) {
      if (!(field in item)) {
        return { valid: false, message: `缺少必需字段: ${field}` };
      }
      if (typeof item[field] !== 'number' && field !== 'region') {
        return { valid: false, message: `字段 ${field} 必须是数字类型` };
      }
    }
  }
  
  return { valid: true, message: '数据验证通过' };
}

// 数据统计分析
function analyzeGlobalData(data) {
  if (!data || data.length === 0) return null;
  
  const analysis = {
    totalRegions: data.length,
    totalInflow: data.reduce((sum, item) => sum + item.inflow, 0),
    totalOutflow: data.reduce((sum, item) => sum + item.outflow, 0),
    totalNetFlow: data.reduce((sum, item) => sum + item.netFlow, 0),
    avgChange: data.reduce((sum, item) => sum + item.change, 0) / data.length,
    
    // 流入流出地区统计
    inflowRegions: data.filter(item => item.netFlow > 0).length,
    outflowRegions: data.filter(item => item.netFlow < 0).length,
    
    // 最值统计
    maxInflow: Math.max(...data.map(item => item.netFlow)),
    minInflow: Math.min(...data.map(item => item.netFlow)),
    maxChange: Math.max(...data.map(item => Math.abs(item.change))),
    
    // 波动性分析
    volatility: calculateVolatility(data.map(item => item.change)),
    
    // 地区排名
    topInflowRegions: [...data].sort((a, b) => b.netFlow - a.netFlow).slice(0, 5),
    topOutflowRegions: [...data].sort((a, b) => a.netFlow - b.netFlow).slice(0, 5),
    
    // 趋势分析
    trend: analyzeTrend(data)
  };
  
  return analysis;
}

// 计算波动性
function calculateVolatility(changes) {
  const mean = changes.reduce((sum, val) => sum + val, 0) / changes.length;
  const variance = changes.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / changes.length;
  return Math.sqrt(variance);
}

// 趋势分析
function analyzeTrend(data) {
  const positiveCount = data.filter(item => item.change > 0).length;
  const negativeCount = data.filter(item => item.change < 0).length;
  
  if (positiveCount > negativeCount * 1.5) {
    return { direction: 'up', strength: 'strong', description: '强劲上升趋势' };
  } else if (positiveCount > negativeCount) {
    return { direction: 'up', strength: 'weak', description: '温和上升趋势' };
  } else if (negativeCount > positiveCount * 1.5) {
    return { direction: 'down', strength: 'strong', description: '强劲下降趋势' };
  } else if (negativeCount > positiveCount) {
    return { direction: 'down', strength: 'weak', description: '温和下降趋势' };
  } else {
    return { direction: 'sideways', strength: 'neutral', description: '横向整理' };
  }
}

// 生成分析报告
function generateAnalysisReport(data) {
  const analysis = analyzeGlobalData(data);
  if (!analysis) return '';
  
  const report = `
    <div class="analysis-report">
      <h5 class="mb-3">全球资金流向分析报告</h5>
      
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h6 class="card-title">基础统计</h6>
              <ul class="list-unstyled mb-0">
                <li>监控地区: ${analysis.totalRegions} 个</li>
                <li>总流入: ${analysis.totalInflow.toFixed(1)} 亿美元</li>
                <li>总流出: ${analysis.totalOutflow.toFixed(1)} 亿美元</li>
                <li>净流入: ${analysis.totalNetFlow >= 0 ? '+' : ''}${analysis.totalNetFlow.toFixed(1)} 亿美元</li>
                <li>平均变化率: ${analysis.avgChange >= 0 ? '+' : ''}${analysis.avgChange.toFixed(2)}%</li>
              </ul>
            </div>
          </div>
        </div>
        
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h6 class="card-title">市场分布</h6>
              <ul class="list-unstyled mb-0">
                <li>净流入地区: ${analysis.inflowRegions} 个</li>
                <li>净流出地区: ${analysis.outflowRegions} 个</li>
                <li>最大净流入: ${analysis.maxInflow.toFixed(1)} 亿美元</li>
                <li>最大净流出: ${analysis.minInflow.toFixed(1)} 亿美元</li>
                <li>波动性: ${analysis.volatility.toFixed(2)}%</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h6 class="card-title">主要流入地区</h6>
              <ol class="mb-0">
                ${analysis.topInflowRegions.map(region => 
                  `<li>${region.region}: +${region.netFlow.toFixed(1)} 亿美元</li>`
                ).join('')}
              </ol>
            </div>
          </div>
        </div>
        
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h6 class="card-title">主要流出地区</h6>
              <ol class="mb-0">
                ${analysis.topOutflowRegions.map(region => 
                  `<li>${region.region}: ${region.netFlow.toFixed(1)} 亿美元</li>`
                ).join('')}
              </ol>
            </div>
          </div>
        </div>
      </div>
      
      <div class="alert alert-info">
        <h6 class="alert-heading">趋势分析</h6>
        <p class="mb-0">${analysis.trend.description}</p>
      </div>
      
      <div class="text-muted small">
        <i class="bi bi-clock"></i> 报告生成时间: ${new Date().toLocaleString('zh-CN')}
      </div>
    </div>
  `;
  
  return report;
}

// 显示分析报告模态框
function showAnalysisReportModal() {
  if (!currentGlobalData || !currentGlobalData.data) {
    showNotification('没有可分析的数据', 'warning');
    return;
  }
  
  const reportContent = generateAnalysisReport(currentGlobalData.data);
  
  const modal = `
    <div class="modal fade" id="analysisReportModal" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-graph-up me-2"></i>数据分析报告
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            ${reportContent}
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
            <button type="button" class="btn btn-primary" onclick="exportAnalysisReport()">
              <i class="bi bi-download"></i> 导出报告
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 移除现有模态框
  const existingModal = document.getElementById('analysisReportModal');
  if (existingModal) {
    existingModal.remove();
  }
  
  // 添加新模态框
  document.body.insertAdjacentHTML('beforeend', modal);
  
  // 显示模态框
  const modalInstance = new bootstrap.Modal(document.getElementById('analysisReportModal'));
  modalInstance.show();
}

// 导出分析报告
function exportAnalysisReport() {
  if (!currentGlobalData || !currentGlobalData.data) return;
  
  const analysis = analyzeGlobalData(currentGlobalData.data);
  const reportData = {
    title: '全球资金流向分析报告',
    generateTime: new Date().toISOString(),
    summary: analysis,
    rawData: currentGlobalData.data
  };
  
  const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `全球资金流向分析报告_${new Date().toLocaleDateString('zh-CN')}.json`;
  link.click();
  
  showNotification('分析报告导出成功', 'success');
}