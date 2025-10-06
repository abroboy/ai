/**
 * 国内热点数据模块
 */

const domesticHotspotData = {
    lastUpdate: new Date().toISOString(),
    data: [
        {
            id: 'dom_001',
            title: 'A股市场回暖',
            category: 'A股',
            heat: 95,
            change: '+2.8%',
            description: '沪深两市放量上涨',
            timestamp: new Date(Date.now() - 1000 * 60 * 10).toISOString()
        },
        {
            id: 'dom_002',
            title: '房地产政策利好',
            category: '房地产',
            heat: 87,
            change: '+1.5%',
            description: '多地出台支持政策',
            timestamp: new Date(Date.now() - 1000 * 60 * 25).toISOString()
        },
        {
            id: 'dom_003',
            title: '消费板块复苏',
            category: '消费',
            heat: 82,
            change: '+1.2%',
            description: '节假日消费数据亮眼',
            timestamp: new Date(Date.now() - 1000 * 60 * 40).toISOString()
        }
    ]
};

// 导出数据
if (typeof module !== 'undefined' && module.exports) {
    module.exports = domesticHotspotData;
} else if (typeof window !== 'undefined') {
    window.domesticHotspotData = domesticHotspotData;
}