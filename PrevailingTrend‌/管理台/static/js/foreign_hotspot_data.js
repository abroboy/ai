/**
 * 国外热点数据模块
 */

// 国外热点数据
const foreignHotspotData = {
    lastUpdate: new Date().toISOString(),
    data: [
        {
            id: 'us_tech',
            title: '美股科技股反弹',
            category: '美股市场',
            heat: 95,
            change: '+2.3%',
            description: '纳斯达克指数上涨，科技股领涨',
            timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString()
        },
        {
            id: 'eu_energy',
            title: '欧洲能源股波动',
            category: '欧洲市场',
            heat: 88,
            change: '-1.2%',
            description: '天然气价格波动影响能源股',
            timestamp: new Date(Date.now() - 1000 * 60 * 45).toISOString()
        },
        {
            id: 'jp_yen',
            title: '日元汇率变动',
            category: '外汇市场',
            heat: 82,
            change: '+0.8%',
            description: '美日汇率波动加剧',
            timestamp: new Date(Date.now() - 1000 * 60 * 60).toISOString()
        }
    ]
};

// 导出数据
if (typeof module !== 'undefined' && module.exports) {
    module.exports = foreignHotspotData;
} else if (typeof window !== 'undefined') {
    window.foreignHotspotData = foreignHotspotData;
}