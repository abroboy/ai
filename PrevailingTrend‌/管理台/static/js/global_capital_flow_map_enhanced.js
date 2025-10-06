/**
 * 全球资金流向地图增强功能模块
 */

// 关闭地区详情面板
function closeRegionDetailPanel() {
  const panel = document.getElementById('region-detail-panel');
  if (panel) {
    panel.style.display = 'none';
  }
}

// 关注地区功能
function trackRegion(regionName) {
  let trackedRegions = JSON.parse(localStorage.getItem('trackedRegions') || '[]');
  
  if (!trackedRegions.includes(regionName)) {
    trackedRegions.push(regionName);
    localStorage.setItem('trackedRegions', JSON.stringify(trackedRegions));
    showNotification(`已关注 ${regionName}`, 'success');
  } else {
    showNotification(`${regionName} 已在关注列表中`, 'info');
  }
}

// 添加地图事件监听
function addMapEventListeners() {
  if (!mapInstance) return;
  
  // 地图移动事件
  mapInstance.on('moveend', () => {
    const center = mapInstance.getCenter();
    const zoom = mapInstance.getZoom();
    console.log(`地图中心: ${center.lat.toFixed(4)}, ${center.lng.toFixed(4)}, 缩放级别: ${zoom}`);
  });
  
  // 地图点击事件
  mapInstance.on('click', (e) => {
    const { lat, lng } = e.latlng;
    console.log(`点击位置: ${lat.toFixed(4)}, ${lng.toFixed(4)}`);
    
    // 关闭详情面板
    closeRegionDetailPanel();
  });
  
  // 地图缩放事件
  mapInstance.on('zoomend', () => {
    const zoom = mapInstance.getZoom();
    
    // 根据缩放级别调整标记大小
    mapInstance.eachLayer(layer => {
      if (layer instanceof L.CircleMarker) {
        const baseRadius = layer.options.baseRadius || 15;
        const newRadius = Math.max(5, baseRadius * (zoom / 5));
        layer.setRadius(newRadius);
      }
    });
  });
}

// 添加热力图功能
function addHeatmapLayer(data) {
  if (typeof L.heatLayer === 'undefined') {
    // 加载热力图插件
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/leaflet.heat@0.2.0/dist/leaflet-heat.js';
    script.onload = () => createHeatmapLayer(data);
    document.head.appendChild(script);
  } else {
    createHeatmapLayer(data);
  }
}

// 创建热力图图层
function createHeatmapLayer(data) {
  const heatData = data.map(item => [
    item.lat,
    item.lng,
    Math.abs(item.netFlow) / 100 // 标准化强度值
  ]).filter(point => point[0] && point[1]);
  
  const heatLayer = L.heatLayer(heatData, {
    radius: 25,
    blur: 15,
    maxZoom: 10,
    gradient: {
      0.0: 'blue',
      0.5: 'lime',
      1.0: 'red'
    }
  });
  
  // 存储热力图图层引用
  mapInstance.heatLayer = heatLayer;
}

// 切换热力图显示
function toggleHeatmap() {
  if (!mapInstance.heatLayer) {
    addHeatmapLayer(currentMapData);
    return;
  }
  
  if (mapInstance.hasLayer(mapInstance.heatLayer)) {
    mapInstance.removeLayer(mapInstance.heatLayer);
  } else {
    mapInstance.addLayer(mapInstance.heatLayer);
  }
}

// 添加聚类功能
function addClusterLayer(data) {
  if (typeof L.markerClusterGroup === 'undefined') {
    // 加载聚类插件
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js';
    script.onload = () => {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://cdn.jsdelivr.net/npm/leaflet.markercluster@1.5.3/dist/MarkerCluster.css';
      document.head.appendChild(link);
      
      const defaultLink = document.createElement('link');
      defaultLink.rel = 'stylesheet';
      defaultLink.href = 'https://cdn.jsdelivr.net/npm/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css';
      document.head.appendChild(defaultLink);
      
      createClusterLayer(data);
    };
    document.head.appendChild(script);
  } else {
    createClusterLayer(data);
  }
}

// 创建聚类图层
function createClusterLayer(data) {
  const markers = L.markerClusterGroup({
    chunkedLoading: true,
    maxClusterRadius: 50
  });
  
  data.forEach(item => {
    if (item.lat && item.lng) {
      const marker = L.marker([item.lat, item.lng]);
      const popupContent = createMapPopup(item);
      marker.bindPopup(popupContent);
      markers.addLayer(marker);
    }
  });
  
  mapInstance.clusterLayer = markers;
}

// 地图测量工具
function addMeasureTool() {
  let measureControl = false;
  
  const measureButton = L.control({ position: 'topleft' });
  measureButton.onAdd = function() {
    const div = L.DomUtil.create('div', 'leaflet-bar');
    div.innerHTML = '<a href="#" title="测量距离"><i class="bi bi-rulers"></i></a>';
    
    L.DomEvent.on(div, 'click', function(e) {
      L.DomEvent.preventDefault(e);
      toggleMeasure();
    });
    
    return div;
  };
  
  measureButton.addTo(mapInstance);
  
  function toggleMeasure() {
    if (!measureControl) {
      measureControl = true;
      mapInstance.on('click', measureClick);
      showNotification('点击地图开始测量', 'info');
    } else {
      measureControl = false;
      mapInstance.off('click', measureClick);
      // 清除测量线
      mapInstance.eachLayer(layer => {
        if (layer instanceof L.Polyline && layer.options.measureLine) {
          mapInstance.removeLayer(layer);
        }
      });
      showNotification('测量工具已关闭', 'info');
    }
  }
  
  let measurePoints = [];
  function measureClick(e) {
    measurePoints.push(e.latlng);
    
    if (measurePoints.length > 1) {
      const line = L.polyline(measurePoints, {
        color: 'red',
        weight: 3,
        measureLine: true
      }).addTo(mapInstance);
      
      const distance = mapInstance.distance(measurePoints[0], measurePoints[measurePoints.length - 1]);
      const distanceText = distance > 1000 ? 
        `${(distance / 1000).toFixed(2)} km` : 
        `${distance.toFixed(0)} m`;
        
      line.bindPopup(`距离: ${distanceText}`).openPopup();
    }
  }
}

// 地图绘制工具
function addDrawingTools() {
  const drawingButton = L.control({ position: 'topleft' });
  drawingButton.onAdd = function() {
    const div = L.DomUtil.create('div', 'leaflet-bar');
    div.innerHTML = '<a href="#" title="绘制工具"><i class="bi bi-pencil"></i></a>';
    
    L.DomEvent.on(div, 'click', function(e) {
      L.DomEvent.preventDefault(e);
      toggleDrawingMode();
    });
    
    return div;
  };
  
  drawingButton.addTo(mapInstance);
  
  let drawingMode = false;
  let drawnItems = new L.FeatureGroup();
  mapInstance.addLayer(drawnItems);
  
  function toggleDrawingMode() {
    if (!drawingMode) {
      drawingMode = true;
      mapInstance.on('click', drawPoint);
      showNotification('绘制模式已启用，点击地图添加标记', 'info');
    } else {
      drawingMode = false;
      mapInstance.off('click', drawPoint);
      showNotification('绘制模式已关闭', 'info');
    }
  }
  
  function drawPoint(e) {
    const marker = L.marker(e.latlng, {
      draggable: true
    });
    
    marker.bindPopup(`
      <div>
        <p>自定义标记</p>
        <button onclick="removeMarker(this)" class="btn btn-sm btn-danger">删除</button>
      </div>
    `);
    
    drawnItems.addLayer(marker);
  }
  
  // 全局函数，用于删除标记
  window.removeMarker = function(button) {
    const popup = button.closest('.leaflet-popup');
    if (popup) {
      const marker = popup._source;
      if (marker) {
        drawnItems.removeLayer(marker);
      }
    }
  };
}

// 地图导出功能
function exportMapAsImage() {
  // 使用html2canvas库导出地图
  if (typeof html2canvas === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
    script.onload = () => performExport();
    document.head.appendChild(script);
  } else {
    performExport();
  }
  
  function performExport() {
    const mapElement = document.getElementById('global-capital-map');
    
    html2canvas(mapElement).then(canvas => {
      const link = document.createElement('a');
      link.download = `全球资金流向地图_${new Date().toLocaleDateString('zh-CN')}.png`;
      link.href = canvas.toDataURL();
      link.click();
      
      showNotification('地图导出成功', 'success');
    }).catch(error => {
      console.error('地图导出失败:', error);
      showNotification('地图导出失败', 'danger');
    });
  }
}

// 地图打印功能
function printMap() {
  const mapElement = document.getElementById('global-capital-map');
  const printWindow = window.open('', '_blank');
  
  printWindow.document.write(`
    <html>
      <head>
        <title>全球资金流向地图</title>
        <style>
          body { margin: 0; padding: 20px; }
          .map-container { width: 100%; height: 600px; }
          .header { text-align: center; margin-bottom: 20px; }
          .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #666; }
        </style>
      </head>
      <body>
        <div class="header">
          <h2>全球资金流向地图</h2>
          <p>生成时间: ${new Date().toLocaleString('zh-CN')}</p>
        </div>
        <div class="map-container">
          ${mapElement.outerHTML}
        </div>
        <div class="footer">
          <p>数据来源: 全球资金流向监控系统</p>
        </div>
      </body>
    </html>
  `);
  
  printWindow.document.close();
  printWindow.focus();
  
  setTimeout(() => {
    printWindow.print();
    printWindow.close();
  }, 1000);
}