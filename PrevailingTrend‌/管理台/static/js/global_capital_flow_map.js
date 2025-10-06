/**
 * 全球资金流向地图功能模块
 */

// 全局变量
let mapInstance = null;
let currentMapData = [];
let currentMapView = 'net';

// 初始化世界地图
function initializeWorldMap(data) {
  loadLeafletLibrary().then(() => {
    createWorldMap(data);
  });
}

// 加载Leaflet地图库
function loadLeafletLibrary() {
  return new Promise((resolve) => {
    if (typeof L !== 'undefined') {
      resolve();
      return;
    }
    
    // 加载CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(link);
    
    // 加载JS
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    script.onload = resolve;
    document.head.appendChild(script);
  });
}

// 创建世界地图
function createWorldMap(data) {
  const mapContainer = document.getElementById('global-capital-map');
  if (!mapContainer) return;
  
  mapContainer.innerHTML = '';
  currentMapData = data;
  
  // 初始化地图
  mapInstance = L.map('global-capital-map', {
    center: [20, 0],
    zoom: 2,
    zoomControl: true,
    scrollWheelZoom: true,
    doubleClickZoom: true,
    dragging: true
  });
  
  // 设置全局引用
  enhancedMapInstance = mapInstance;
  
  // 添加多个地图图层选项
  const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18
  });
  
  const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '© Esri',
    maxZoom: 18
  });
  
  // 默认使用OSM图层
  osmLayer.addTo(mapInstance);
  
  // 添加图层控制
  const baseLayers = {
    "标准地图": osmLayer,
    "卫星地图": satelliteLayer
  };
  
  L.control.layers(baseLayers).addTo(mapInstance);
  
  // 添加数据点
  addDataPointsToMap(data);
  
  // 添加图例
  addMapLegend();
  
  // 添加地图事件监听
  addMapEventListeners();
}

// 添加数据点到地图
function addDataPointsToMap(data) {
  data.forEach(item => {
    if (item.lat && item.lng) {
      const netFlow = item.netFlow;
      const radius = Math.max(8, Math.min(40, Math.abs(netFlow) / 15));
      const color = netFlow >= 0 ? '#28a745' : '#dc3545';
      const fillOpacity = Math.min(0.8, Math.abs(netFlow) / 300);
      
      // 创建圆形标记
      const circle = L.circleMarker([item.lat, item.lng], {
        radius: radius,
        fillColor: color,
        color: '#ffffff',
        weight: 2,
        opacity: 0.9,
        fillOpacity: fillOpacity
      }).addTo(mapInstance);
      
      // 添加弹出信息
      const popupContent = createMapPopup(item);
      circle.bindPopup(popupContent);
      
      // 点击事件
      circle.on('click', () => {
        showRegionDetailInPanel(item);
        highlightTableRow(item.region);
      });
      
      // 存储数据到标记
      circle.regionData = item;
    }
  });
}

// 创建地图弹窗内容
function createMapPopup(item) {
  const netFlow = item.netFlow;
  return `
    <div class="map-popup" style="min-width: 200px;">
      <h6 class="fw-bold mb-2 text-primary">${item.region}</h6>
      <div class="row g-1 small">
        <div class="col-5">资金流入:</div>
        <div class="col-7 text-info fw-bold">${item.inflow.toFixed(1)} 亿美元</div>
        <div class="col-5">资金流出:</div>
        <div class="col-7 text-info fw-bold">${item.outflow.toFixed(1)} 亿美元</div>
        <div class="col-5">净流入:</div>
        <div class="col-7 ${netFlow >= 0 ? 'text-success' : 'text-danger'} fw-bold">
          ${netFlow >= 0 ? '+' : ''}${netFlow.toFixed(1)} 亿美元
        </div>
        <div class="col-5">变化率:</div>
        <div class="col-7 ${item.change >= 0 ? 'text-success' : 'text-danger'} fw-bold">
          ${item.change >= 0 ? '+' : ''}${item.change.toFixed(1)}%
          <i class="bi bi-${item.change >= 0 ? 'arrow-up' : 'arrow-down'}"></i>
        </div>
      </div>
      <button class="btn btn-sm btn-primary mt-2 w-100" onclick="showRegionDetailModal('${item.region}')">
        <i class="bi bi-info-circle me-1"></i>查看详细信息
      </button>
    </div>
  `;
}

// 添加地图图例
function addMapLegend() {
  const legend = L.control({ position: 'bottomright' });
  
  legend.onAdd = function() {
    const div = L.DomUtil.create('div', 'map-legend');
    div.innerHTML = `
      <div class="bg-white p-3 rounded shadow" style="font-size: 12px; border: 1px solid #ddd;">
        <div class="fw-bold mb-2 text-dark">资金流向图例</div>
        <div class="d-flex align-items-center mb-2">
          <div style="width: 16px; height: 16px; border-radius: 50%; background: #28a745; margin-right: 8px; border: 2px solid #fff;"></div>
          <span>净流入地区</span>
        </div>
        <div class="d-flex align-items-center mb-2">
          <div style="width: 16px; height: 16px; border-radius: 50%; background: #dc3545; margin-right: 8px; border: 2px solid #fff;"></div>
          <span>净流出地区</span>
        </div>
        <div class="text-muted mt-2" style="font-size: 10px;">
          • 圆圈大小表示资金规模<br>
          • 点击圆圈查看详细信息
        </div>
      </div>
    `;
    return div;
  };
  
  legend.addTo(mapInstance);
}

// 切换地图视图
function switchMapView(type) {
  currentMapView = type;
  
  // 更新按钮状态
  document.querySelectorAll('.btn-group button[onclick*="switchMapView"]').forEach(btn => {
    btn.classList.remove('btn-primary');
    btn.classList.add('btn-outline-primary');
  });
  
  const activeBtn = document.querySelector(`button[onclick="switchMapView('${type}')"]`);
  if (activeBtn) {
    activeBtn.classList.remove('btn-outline-primary');
    activeBtn.classList.add('btn-primary');
  }
  
  // 重新绘制地图点
  if (mapInstance && currentMapData.length > 0) {
    // 清除现有标记
    mapInstance.eachLayer(layer => {
      if (layer instanceof L.CircleMarker) {
        mapInstance.removeLayer(layer);
      }
    });
    
    // 根据新视图重新添加数据点
    addDataPointsToMapByType(currentMapData, type);
  }
}

// 根据类型添加数据点
function addDataPointsToMapByType(data, type) {
  data.forEach(item => {
    if (item.lat && item.lng) {
      let value, color;
      
      switch(type) {
        case 'inflow':
          value = item.inflow;
          color = '#007bff';
          break;
        case 'outflow':
          value = item.outflow;
          color = '#fd7e14';
          break;
        default: // net
          value = item.netFlow;
          color = value >= 0 ? '#28a745' : '#dc3545';
      }
      
      const radius = Math.max(8, Math.min(40, Math.abs(value) / 15));
      const fillOpacity = Math.min(0.8, Math.abs(value) / 300);
      
      const circle = L.circleMarker([item.lat, item.lng], {
        radius: radius,
        fillColor: color,
        color: '#ffffff',
        weight: 2,
        opacity: 0.9,
        fillOpacity: fillOpacity
      }).addTo(mapInstance);
      
      const popupContent = createMapPopup(item);
      circle.bindPopup(popupContent);
      
      circle.on('click', () => {
        showRegionDetailInPanel(item);
        highlightTableRow(item.region);
      });
      
      circle.regionData = item;
    }
  });
}

// 选择地图上的地区
function selectRegionOnMap(regionName) {
  if (!mapInstance) return;
  
  // 找到对应的地区数据
  const regionData = currentMapData.find(item => item.region === regionName);
  if (!regionData || !regionData.lat || !regionData.lng) return;
  
  // 移动地图视角到该地区
  mapInstance.setView([regionData.lat, regionData.lng], 4);
  
  // 找到对应的标记并触发点击
  mapInstance.eachLayer(layer => {
    if (layer instanceof L.CircleMarker && layer.regionData && layer.regionData.region === regionName) {
      layer.openPopup();
      // 高亮效果
      layer.setStyle({
        weight: 4,
        color: '#ffff00'
      });
      
      // 2秒后恢复正常样式
      setTimeout(() => {
        layer.setStyle({
          weight: 2,
          color: '#ffffff'
        });
      }, 2000);
    }
  });
  
  // 显示地区详情
  showRegionDetailInPanel(regionData);
}

// 高亮表格行
function highlightTableRow(regionName) {
  // 移除之前的高亮
  document.querySelectorAll('#realtime-data-table tr').forEach(row => {
    row.classList.remove('table-warning');
  });
  
  // 添加新的高亮
  const targetRow = document.querySelector(`#realtime-data-table tr[data-region="${regionName}"]`);
  if (targetRow) {
    targetRow.classList.add('table-warning');
    targetRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

// 在面板中显示地区详情
function showRegionDetailInPanel(regionData) {
  let panel = document.getElementById('region-detail-panel');
  
  // 如果面板不存在，创建一个
  if (!panel) {
    const panelHTML = `
      <div id="region-detail-panel" class="position-fixed" style="top: 100px; right: 20px; width: 300px; z-index: 1000;">
        <div class="card shadow">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h6 class="mb-0">地区详情</h6>
            <button class="btn btn-sm btn-outline-secondary" onclick="closeRegionDetailPanel()">
              <i class="bi bi-x"></i>
            </button>
          </div>
          <div class="card-body" id="region-detail-content">
            <!-- 内容将在这里动态生成 -->
          </div>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', panelHTML);
    panel = document.getElementById('region-detail-panel');
  }
  
  const contentDiv = document.getElementById('region-detail-content');
  
  const detailHTML = `
    <div class="region-detail-content">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h6 class="fw-bold text-primary mb-0">${regionData.region}</h6>
        <span class="badge ${regionData.netFlow >= 0 ? 'bg-success' : 'bg-danger'}">
          ${regionData.netFlow >= 0 ? '净流入' : '净流出'}
        </span>
      </div>
      
      <div class="row g-2 mb-3">
        <div class="col-6">
          <div class="text-center p-2 bg-light rounded">
            <div class="text-primary fw-bold">${regionData.inflow.toFixed(1)}</div>
            <small class="text-muted">流入(亿美元)</small>
          </div>
        </div>
        <div class="col-6">
          <div class="text-center p-2 bg-light rounded">
            <div class="text-primary fw-bold">${regionData.outflow.toFixed(1)}</div>
            <small class="text-muted">流出(亿美元)</small>
          </div>
        </div>
      </div>
      
      <div class="mb-3">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <span class="small">净流入</span>
          <span class="${regionData.netFlow >= 0 ? 'text-success' : 'text-danger'} fw-bold">
            ${regionData.netFlow >= 0 ? '+' : ''}${regionData.netFlow.toFixed(1)} 亿美元
          </span>
        </div>
        <div class="progress" style="height: 6px;">
          <div class="progress-bar ${regionData.netFlow >= 0 ? 'bg-success' : 'bg-danger'}" 
               style="width: ${Math.min(100, Math.abs(regionData.netFlow) / 10)}%"></div>
        </div>
      </div>
      
      <div class="mb-3">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <span class="small">变化率</span>
          <span class="${regionData.change >= 0 ? 'text-success' : 'text-danger'} fw-bold">
            ${regionData.change >= 0 ? '+' : ''}${regionData.change.toFixed(1)}%
            <i class="bi bi-${regionData.change >= 0 ? 'arrow-up' : 'arrow-down'}"></i>
          </span>
        </div>
      </div>
      
      <div class="d-grid">
        <button class="btn btn-sm btn-outline-primary" onclick="showRegionDetailModal('${regionData.region}')">
          <i class="bi bi-zoom-in me-1"></i>查看完整分析
        </button>
      </div>
      
      <div class="text-muted small mt-2">
        <i class="bi bi-clock me-1"></i>更新时间: ${regionData.date}
      </div>
    </div>
  `;
  
  panel.innerHTML = detailHTML;
}