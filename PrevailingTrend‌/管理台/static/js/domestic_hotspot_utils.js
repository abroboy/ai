/**
 * 国内热点工具函数模块
 */

// 格式化时间
function formatHotspotTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) {
        return '刚刚';
    } else if (diff < 3600000) {
        return Math.floor(diff / 60000) + '分钟前';
    } else if (diff < 86400000) {
        return Math.floor(diff / 3600000) + '小时前';
    } else {
        return date.toLocaleDateString();
    }
}

// 计算热度等级
function getHeatLevel(heat) {
    if (heat >= 90) return 'hot';
    if (heat >= 70) return 'warm';
    if (heat >= 50) return 'normal';
    return 'cold';
}

// 格式化变化百分比
function formatChange(change) {
    const num = parseFloat(change);
    if (num > 0) {
        return `+${change}`;
    }
    return change;
}

// 导出工具函数
window.HotspotUtils = {
    formatTime: formatHotspotTime,
    getHeatLevel: getHeatLevel,
    formatChange: formatChange
};