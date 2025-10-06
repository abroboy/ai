/**
 * 全球资金流向工具函数模块
 */

// 表格操作函数
function sortTableByNetFlow() {
  const tbody = document.getElementById('realtime-data-table');
  if (!tbody) return;
  
  const rows = Array.from(tbody.querySelectorAll('tr'));
  
  rows.sort((a, b) => {
    const aValue = parseFloat(a.cells[1].textContent.replace(/[+,]/g, ''));
    const bValue = parseFloat(b.cells[1].textContent.replace(/[+,]/g, ''));
    return bValue - aValue;
  });
  
  rows.forEach(row => tbody.appendChild(row));
}

function filterPositiveFlow() {
  const rows = document.querySelectorAll('#realtime-data-table tr');
  rows.forEach(row => {
    const netFlowCell = row.cells[1];
    const isPositive = netFlowCell.classList.contains('text-success');
    row.style.display = isPositive ? '' : 'none';
  });
}

function filterNegativeFlow() {
  const rows = document.querySelectorAll('#realtime-data-table tr');
  rows.forEach(row => {
    const netFlowCell = row.cells[1];
    const isNegative = netFlowCell.classList.contains('text-danger');
    row.style.display = isNegative ? '' : 'none';
  });
}

function showAllRegions() {
  const rows = document.querySelectorAll('#realtime-data-table tr');
  rows.forEach(row => {
    row.style.display = '';
  });
}

// 数据导出功能
function exportGlobalData() {
  if (!currentGlobalData) {
    alert('没有可导出的数据');
    return;
  }
  
  const data = currentGlobalData.data;
  let csvContent = 'ID,地区,资金流入(亿美元),资金流出(亿美元),净流入(亿美元),变化率(%),日期\n';
  
  data.forEach((item, index) => {
    csvContent += `${index + 1},${item.region},${item.inflow},${item.outflow},${item.netFlow},${item.change},${item.date}\n`;
  });
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  link.setAttribute('href', url);
  link.setAttribute('download', `全球资金流向数据_${new Date().toLocaleDateString()}.csv`);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  // 显示成功提示
  showNotification('数据导出成功', 'success');
}

// 刷新数据功能
function refreshGlobalData() {
  if (typeof loadGlobalCapitalFlowEnhanced === 'function') {
    loadGlobalCapitalFlowEnhanced();
  } else {
    loadGlobalCapitalFlow();
  }
}

// 全屏功能
function toggleMapFullscreen() {
  const mapCard = document.querySelector('#global-capital-map').closest('.card');
  if (!mapCard) return;
  
  if (!document.fullscreenElement) {
    mapCard.requestFullscreen().then(() => {
      mapCard.style.height = '100vh';
      document.getElementById('global-capital-map').style.height = 'calc(100vh - 120px)';
      
      // 重新调整地图大小
      setTimeout(() => {
        if (mapInstance) {
          mapInstance.invalidateSize();
        }
      }, 100);
    }).catch(err => {
      console.error('无法进入全屏模式:', err);
      showNotification('全屏模式不可用', 'warning');
    });
  } else {
    document.exitFullscreen();
  }
}

// 监听全屏退出事件
document.addEventListener('fullscreenchange', () => {
  if (!document.fullscreenElement) {
    const mapCard = document.querySelector('#global-capital-map').closest('.card');
    if (mapCard) {
      mapCard.style.height = '';
      document.getElementById('global-capital-map').style.height = '500px';
      
      // 重新调整地图大小
      setTimeout(() => {
        if (mapInstance) {
          mapInstance.invalidateSize();
        }
      }, 100);
    }
  }
});

// 显示地区详情模态框
function showRegionDetailModal(regionName) {
  if (!currentGlobalData) return;
  
  const regionData = currentGlobalData.data.find(item => item.region === regionName);
  if (!regionData) return;
  
  // 创建模态框HTML
  const modalHTML = `
    <div class="modal fade" id="regionDetailModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-geo-alt-fill me-2"></i>
              ${regionData.region} - 资金流向详情
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row mb-4">
              <div class="col-md-4">
                <div class="card text-center">
                  <div class="card-body">
                    <h3 class="text-primary">${regionData.inflow.toFixed(1)}</h3>
                    <p class="text-muted mb-0">资金流入(亿美元)</p>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="card text-center">
                  <div class="card-body">
                    <h3 class="text-primary">${regionData.outflow.toFixed(1)}</h3>
                    <p class="text-muted mb-0">资金流出(亿美元)</p>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="card text-center">
                  <div class="card-body">
                    <h3 class="${regionData.netFlow >= 0 ? 'text-success' : 'text-danger'}">
                      ${regionData.netFlow >= 0 ? '+' : ''}${regionData.netFlow.toFixed(1)}
                    </h3>
                    <p class="text-muted mb-0">净流入(亿美元)</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="alert ${regionData.netFlow >= 0 ? 'alert-success' : 'alert-danger'}">
              <h6 class="alert-heading">
                <i class="bi bi-${regionData.netFlow >= 0 ? 'arrow-up' : 'arrow-down'}-circle-fill me-2"></i>
                ${regionData.netFlow >= 0 ? '资金净流入' : '资金净流出'}地区
              </h6>
              <p class="mb-0">
                当前变化率: <strong>${regionData.change >= 0 ? '+' : ''}${regionData.change.toFixed(1)}%</strong>
                <i class="bi bi-${regionData.change >= 0 ? 'arrow-up' : 'arrow-down'} ms-1"></i>
              </p>
            </div>
            
            <div class="row">
              <div class="col-md-6">
                <h6>关键指标</h6>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item d-flex justify-content-between">
                    <span>流入流出比</span>
                    <strong>${(regionData.inflow / regionData.outflow).toFixed(2)}</strong>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>净流入占比</span>
                    <strong>${((regionData.netFlow / regionData.inflow) * 100).toFixed(1)}%</strong>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>更新日期</span>
                    <strong>${regionData.date}</strong>
                  </li>
                </ul>
              </div>
              <div class="col-md-6">
                <h6>风险评估</h6>
                <div class="progress mb-2">
                  <div class="progress-bar ${regionData.change >= 0 ? 'bg-success' : 'bg-danger'}" 
                       style="width: ${Math.min(100, Math.abs(regionData.change) * 10)}%">
                    ${Math.abs(regionData.change).toFixed(1)}%
                  </div>
                </div>
                <small class="text-muted">基于变化率的波动性评估</small>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
            <button type="button" class="btn btn-primary" onclick="focusOnRegion('${regionData.region}')">
              <i class="bi bi-geo-alt me-1"></i>定位到地图
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 移除现有模态框
  const existingModal = document.getElementById('regionDetailModal');
  if (existingModal) {
    existingModal.remove();
  }
  
  // 添加新模态框
  document.body.insertAdjacentHTML('beforeend', modalHTML);
  
  // 显示模态框
  const modal = new bootstrap.Modal(document.getElementById('regionDetailModal'));
  modal.show();
}

// 聚焦到地区
function focusOnRegion(regionName) {
  // 关闭模态框
  const modal = bootstrap.Modal.getInstance(document.getElementById('regionDetailModal'));
  if (modal) {
    modal.hide();
  }
  
  // 聚焦到地图上的地区
  selectRegionOnMap(regionName);
}

// 通知功能
function showNotification(message, type = 'info') {
  const alertClass = {
    'success': 'alert-success',
    'warning': 'alert-warning',
    'danger': 'alert-danger',
    'info': 'alert-info'
  }[type] || 'alert-info';
  
  const notification = document.createElement('div');
  notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
  notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
  notification.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  
  document.body.appendChild(notification);
  
  // 3秒后自动移除
  setTimeout(() => {
    if (notification.parentNode) {
      notification.remove();
    }
  }, 3000);
}