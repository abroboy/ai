/**
 * 雪球热点数据模块
 */

const xueqiuHotspotData = {
    lastUpdate: new Date().toISOString(),
    data: [
        {
            id: 'xq_001',
            title: '科技股反弹行情',
            category: '科技',
            heat: 92,
            change: '+3.2%',
            description: '人工智能概念股领涨',
            timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString()
        },
        {
            id: 'xq_002',
            title: '新能源汽车板块',
            category: '新能源',
            heat: 88,
            change: '+2.1%',
            description: '电池技术突破推动板块上涨',
            timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString()
        },
        {
            id: 'xq_003',
            title: '医药生物热点',
            category: '医药',
            heat: 85,
            change: '+1.8%',
            description: '创新药获批利好消息',
            timestamp: new Date(Date.now() - 1000 * 60 * 45).toISOString()
        }
    ]
};

// 导出数据
if (typeof module !== 'undefined' && module.exports) {
    module.exports = xueqiuHotspotData;
} else if (typeof window !== 'undefined') {
    window.xueqiuHotspotData = xueqiuHotspotData;
}