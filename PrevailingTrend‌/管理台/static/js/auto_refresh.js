/**
 * 自动刷新机制
 * 定期刷新管理台数据以确保实时性
 */

// 自动刷新配置
const AUTO_REFRESH_CONFIG = {
    interval: 300000, // 5分钟刷新一次（毫秒）
    enabled: true
};

// 初始化自动刷新
function initAutoRefresh() {
    if (!AUTO_REFRESH_CONFIG.enabled) {
        return;
    }
    
    // 设置定时器
    setInterval(() => {
        refreshAllData();
    }, AUTO_REFRESH_CONFIG.interval);
    
    console.log(`自动刷新已启用，刷新间隔: ${AUTO_REFRESH_CONFIG.interval / 1000}秒`);
}

// 刷新所有数据
function refreshAllData() {
    // 获取当前活动的模块
    const activeSection = document.querySelector(".content-section.active");
    if (!activeSection) return;
    
    const sectionId = activeSection.id.replace("-section", "");
    
    // 根据当前模块刷新对应数据
    switch (sectionId) {
        case "dashboard":
            fetchStats();
            renderCharts();
            break;
        case "industries":
            fetchIndustries(1);
            break;
        case "stocks":
            fetchStocks(1);
            break;
        default:
            // 对于其他模块，可以添加对应的刷新逻辑
            break;
    }
    
    console.log("数据已自动刷新:", new Date().toLocaleString());
}

// 手动触发刷新
function triggerManualRefresh() {
    refreshAllData();
    
    // 显示刷新提示
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-info alert-dismissible fade show';
    alertDiv.innerHTML = `
        <i class="bi bi-info-circle-fill"></i> 数据已手动刷新
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    
    document.body.appendChild(alertDiv);
    
    // 3秒后自动移除提示
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 3000);
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 初始化自动刷新
    initAutoRefresh();
    
    // 添加手动刷新按钮事件监听器
    const refreshBtn = document.getElementById('manual-refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', triggerManualRefresh);
    }
});