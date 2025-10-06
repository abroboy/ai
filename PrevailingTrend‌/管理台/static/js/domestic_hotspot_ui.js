/**
 * 国内热点UI模块
 */

// 初始化国内热点UI
function initDomesticHotspotUI() {
    console.log('初始化国内热点UI...');
    loadDomesticHotspotData();
}

// 加载国内热点数据
function loadDomesticHotspotData() {
    try {
        const data = window.domesticHotspotData || { data: [] };
        updateDomesticHotspotDisplay(data.data);
        console.log('国内热点数据加载完成');
    } catch (error) {
        console.error('国内热点数据加载失败:', error);
    }
}

// 更新国内热点显示
function updateDomesticHotspotDisplay(data) {
    const container = document.getElementById('domestic-hotspot-container');
    if (!container) return;
    
    container.innerHTML = data.map(item => `
        <div class="hotspot-item mb-2">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h6 class="mb-1">${item.title}</h6>
                    <small class="text-muted">${item.description}</small>
                </div>
                <div class="text-end">
                    <span class="badge bg-info">${item.category}</span>
                    <div class="text-success mt-1">${item.change}</div>
                </div>
            </div>
        </div>
    `).join('');
}

// 导出函数
window.initDomesticHotspotUI = initDomesticHotspotUI;