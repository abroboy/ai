/**
 * 全球资金流向对比功能模块
 */

// 数据对比功能
function compareRegions(region1, region2) {
  if (!currentGlobalData || !currentGlobalData.data) return;
  
  const data1 = currentGlobalData.data.find(item => item.region === region1);
  const data2 = currentGlobalData.data.find(item => item.region === region2);
  
  if (!data1 || !data2) {
    showNotification('找不到指定地区的数据', 'warning');
    return;
  }
  
  const comparison = {
    region1: data1,
    region2: data2,
    differences: {
      inflowDiff: data1.inflow - data2.inflow,
      outflowDiff: data1.outflow - data2.outflow,
      netFlowDiff: data1.netFlow - data2.netFlow,
      changeDiff: data1.change - data2.change
    },
    ratios: {
      inflowRatio: data2.inflow !== 0 ? data1.inflow / data2.inflow : 0,
      outflowRatio: data2.outflow !== 0 ? data1.outflow / data2.outflow : 0,
      netFlowRatio: data2.netFlow !== 0 ? data1.netFlow / data2.netFlow : 0
    }
  };
  
  showComparisonModal(comparison);
}

// 显示对比结果模态框
function showComparisonModal(comparison) {
  const modal = `
    <div class="modal fade" id="comparisonModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-bar-chart me-2"></i>地区对比分析
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="row mb-4">
              <div class="col-md-6">
                <h6 class="text-primary">${comparison.region1.region}</h6>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item d-flex justify-content-between">
                    <span>资金流入</span>
                    <strong class="text-info">${comparison.region1.inflow.toFixed(1)} 亿美元</strong>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>资金流出</span>
                    <strong class="text-info">${comparison.region1.outflow.toFixed(1)} 亿美元</strong>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>净流入</span>
                    <strong class="${comparison.region1.netFlow >= 0 ? 'text-success' : 'text-danger'}">
                      ${comparison.region1.netFlow >= 0 ? '+' : ''}${comparison.region1.netFlow.toFixed(1)} 亿美元
                    </strong>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>变化率</span>
                    <strong class="${comparison.region1.change >= 0 ? 'text-success' : 'text-danger'}">
                      ${comparison.region1.change >= 0 ? '+' : ''}${comparison.region1.change.toFixed(1)}%
                    </strong>
                  </li>
                </ul>
              </div>
              
              <div class="col-md-6">
                <h6 class="text-success">${comparison.region2.region}</h6>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item d-flex justify-content-between">
                    <span>资金流入</span>
                    <strong class="text-info">${comparison.region2.inflow.toFixed(1)} 亿美元</strong>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>资金流出</span>
                    <strong class="text-info">${comparison.region2.outflow.toFixed(1)} 亿美元</strong>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>净流入</span>
                    <strong class="${comparison.region2.netFlow >= 0 ? 'text-success' : 'text-danger'}">
                      ${comparison.region2.netFlow >= 0 ? '+' : ''}${comparison.region2.netFlow.toFixed(1)} 亿美元
                    </strong>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>变化率</span>
                    <strong class="${comparison.region2.change >= 0 ? 'text-success' : 'text-danger'}">
                      ${comparison.region2.change >= 0 ? '+' : ''}${comparison.region2.change.toFixed(1)}%
                    </strong>
                  </li>
                </ul>
              </div>
            </div>
            
            <div class="card">
              <div class="card-header">
                <h6 class="mb-0">对比分析</h6>
              </div>
              <div class="card-body">
                <div class="row">
                  <div class="col-md-6">
                    <h6>差值分析</h6>
                    <ul class="list-unstyled">
                      <li>流入差值: <span class="${comparison.differences.inflowDiff >= 0 ? 'text-success' : 'text-danger'}">
                        ${comparison.differences.inflowDiff >= 0 ? '+' : ''}${comparison.differences.inflowDiff.toFixed(1)} 亿美元
                      </span></li>
                      <li>流出差值: <span class="${comparison.differences.outflowDiff >= 0 ? 'text-success' : 'text-danger'}">
                        ${comparison.differences.outflowDiff >= 0 ? '+' : ''}${comparison.differences.outflowDiff.toFixed(1)} 亿美元
                      </span></li>
                      <li>净流入差值: <span class="${comparison.differences.netFlowDiff >= 0 ? 'text-success' : 'text-danger'}">
                        ${comparison.differences.netFlowDiff >= 0 ? '+' : ''}${comparison.differences.netFlowDiff.toFixed(1)} 亿美元
                      </span></li>
                      <li>变化率差值: <span class="${comparison.differences.changeDiff >= 0 ? 'text-success' : 'text-danger'}">
                        ${comparison.differences.changeDiff >= 0 ? '+' : ''}${comparison.differences.changeDiff.toFixed(1)}%
                      </span></li>
                    </ul>
                  </div>
                  
                  <div class="col-md-6">
                    <h6>比率分析</h6>
                    <ul class="list-unstyled">
                      <li>流入比率: <strong>${comparison.ratios.inflowRatio.toFixed(2)}</strong></li>
                      <li>流出比率: <strong>${comparison.ratios.outflowRatio.toFixed(2)}</strong></li>
                      <li>净流入比率: <strong>${comparison.ratios.netFlowRatio.toFixed(2)}</strong></li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="mt-3">
              <div id="comparison-chart" style="height: 300px;"></div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
            <button type="button" class="btn btn-primary" onclick="exportComparisonData()">
              <i class="bi bi-download"></i> 导出对比数据
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 移除现有模态框
  const existingModal = document.getElementById('comparisonModal');
  if (existingModal) {
    existingModal.remove();
  }
  
  // 添加新模态框
  document.body.insertAdjacentHTML('beforeend', modal);
  
  // 显示模态框
  const modalInstance = new bootstrap.Modal(document.getElementById('comparisonModal'));
  modalInstance.show();
  
  // 创建对比图表
  setTimeout(() => {
    createComparisonChart(comparison.region1, comparison.region2);
  }, 500);
}

// 导出对比数据
function exportComparisonData() {
  // 这里可以实现导出对比数据的功能
  showNotification('对比数据导出功能开发中...', 'info');
}

// 批量对比功能
function batchCompareRegions(regions) {
  if (!regions || regions.length < 2) {
    showNotification('请选择至少两个地区进行对比', 'warning');
    return;
  }
  
  const comparisonData = regions.map(regionName => {
    return currentGlobalData.data.find(item => item.region === regionName);
  }).filter(Boolean);
  
  if (comparisonData.length < 2) {
    showNotification('找不到足够的地区数据', 'warning');
    return;
  }
  
  showBatchComparisonModal(comparisonData);
}

// 显示批量对比模态框
function showBatchComparisonModal(data) {
  const modal = `
    <div class="modal fade" id="batchComparisonModal" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-graph-up me-2"></i>批量地区对比
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="row mb-3">
              <div class="col-12">
                <div id="batch-comparison-chart" style="height: 400px;"></div>
              </div>
            </div>
            
            <div class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>地区</th>
                    <th>资金流入</th>
                    <th>资金流出</th>
                    <th>净流入</th>
                    <th>变化率</th>
                    <th>排名</th>
                  </tr>
                </thead>
                <tbody>
                  ${data.sort((a, b) => b.netFlow - a.netFlow).map((item, index) => `
                    <tr>
                      <td><strong>${item.region}</strong></td>
                      <td class="text-info">${item.inflow.toFixed(1)} 亿美元</td>
                      <td class="text-info">${item.outflow.toFixed(1)} 亿美元</td>
                      <td class="${item.netFlow >= 0 ? 'text-success' : 'text-danger'}">
                        ${item.netFlow >= 0 ? '+' : ''}${item.netFlow.toFixed(1)} 亿美元
                      </td>
                      <td class="${item.change >= 0 ? 'text-success' : 'text-danger'}">
                        ${item.change >= 0 ? '+' : ''}${item.change.toFixed(1)}%
                      </td>
                      <td>
                        <span class="badge ${index < 3 ? 'bg-warning' : 'bg-secondary'}">
                          第 ${index + 1} 名
                        </span>
                      </td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
            <button type="button" class="btn btn-primary" onclick="exportBatchComparisonData()">
              <i class="bi bi-download"></i> 导出数据
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 移除现有模态框
  const existingModal = document.getElementById('batchComparisonModal');
  if (existingModal) {
    existingModal.remove();
  }
  
  // 添加新模态框
  document.body.insertAdjacentHTML('beforeend', modal);
  
  // 显示模态框
  const modalInstance = new bootstrap.Modal(document.getElementById('batchComparisonModal'));
  modalInstance.show();
  
  // 创建批量对比图表
  setTimeout(() => {
    createBatchComparisonChart(data);
  }, 500);
}

// 创建批量对比图表
function createBatchComparisonChart(data) {
  const chartContainer = document.getElementById('batch-comparison-chart');
  if (!chartContainer) return;
  
  const chart = echarts.init(chartContainer);
  
  const option = {
    title: {
      text: '地区资金流向对比',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['流入', '流出', '净流入'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.region),
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '亿美元'
    },
    series: [
      {
        name: '流入',
        type: 'bar',
        data: data.map(item => item.inflow),
        itemStyle: { color: '#007bff' }
      },
      {
        name: '流出',
        type: 'bar',
        data: data.map(item => item.outflow),
        itemStyle: { color: '#dc3545' }
      },
      {
        name: '净流入',
        type: 'line',
        data: data.map(item => item.netFlow),
        itemStyle: { color: '#28a745' },
        lineStyle: { width: 3 }
      }
    ]
  };
  
  chart.setOption(option);
}

// 导出批量对比数据
function exportBatchComparisonData() {
  showNotification('批量对比数据导出功能开发中...', 'info');
}