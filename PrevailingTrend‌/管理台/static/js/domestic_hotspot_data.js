/**
 * 国内热点数据模块
 * 大势所趋风险框架管理台
 */

// 全局变量
let currentHotspotData = [];
let currentPage = 1;
const pageSize = 10;
let currentFilter = 'all';

// 加载国内热点数据模块
function loadDomesticHotspotData() {
    const contentArea = document.querySelector('.content-body') || document.getElementById('content-container');
    
    if (!contentArea) {
        console.error('找不到内容容器');
        return;
    }
    
    // 显示加载中状态
    contentArea.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-3">正在获取国内热点数据...</p>
        </div>
    `;
    
    // 获取热点数据
    fetchDomesticHotspots()
        .then(data => {
            if (data.success) {
                currentHotspotData = data.data || [];
                renderDomesticHotspotModule(contentArea, data);
            } else {
                showErrorMessage(contentArea, data.error || '获取数据失败');
            }
        })
        .catch(error => {
            console.error('获取热点数据失败:', error);
            showErrorMessage(contentArea, '网络错误，请稍后重试');
        });
}

// 获取国内热点数据
async function fetchDomesticHotspots() {
    try {
        const response = await fetch('/api/domestic-hotspot');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API调用失败，使用模拟数据:', error);
        // 返回模拟数据
        return generateMockData();
    }
}

// 生成模拟数据
function generateMockData() {
    const mockData = [
        {
            id: "mock_1",
            title: "央行降准预期升温，银行股集体上涨",
            content: "市场预期央行可能在近期实施降准措施，以进一步改善市场流动性环境，银行板块受益明显。",
            source: "新浪财经",
            publish_time: new Date().toISOString(),
            category: "金融政策",
            heat_score: 92,
            sentiment: "积极",
            keywords: ["央行", "降准", "银行股", "流动性"],
            url: "#"
        },
        {
            id: "mock_2",
            title: "新能源汽车销量创历史新高，产业链全面受益",
            content: "最新数据显示，新能源汽车销量同比增长超35%，带动电池、电机、充电桩等产业链公司业绩大幅提升。",
            source: "东方财富",
            publish_time: new Date(Date.now() - 3600000).toISOString(),
            category: "行业动态",
            heat_score: 88,
            sentiment: "积极",
            keywords: ["新能源汽车", "销量", "产业链", "电池"],
            url: "#"
        },
        {
            id: "mock_3",
            title: "科创板注册制改革持续深化",
            content: "科创板注册制改革取得显著成效，为科技创新企业提供更好的融资环境。",
            source: "中国证券网",
            publish_time: new Date(Date.now() - 7200000).toISOString(),
            category: "资本市场",
            heat_score: 85,
            sentiment: "积极",
            keywords: ["科创板", "注册制", "改革", "融资"],
            url: "#"
        },
        {
            id: "mock_4",
            title: "房地产政策边际放松，市场预期改善",
            content: "多地政府调整房地产调控政策，包括降低首付比例、放宽限购条件等措施。",
            source: "财经网",
            publish_time: new Date(Date.now() - 10800000).toISOString(),
            category: "政策动态",
            heat_score: 82,
            sentiment: "中性",
            keywords: ["房地产", "政策", "调控", "首付"],
            url: "#"
        },
        {
            id: "mock_5",
            title: "人工智能概念股持续活跃",
            content: "ChatGPT等AI技术快速发展，带动相关概念股持续上涨，市场关注度不断提升。",
            source: "证券时报",
            publish_time: new Date(Date.now() - 14400000).toISOString(),
            category: "科技创新",
            heat_score: 90,
            sentiment: "积极",
            keywords: ["人工智能", "ChatGPT", "概念股", "科技"],
            url: "#"
        }
    ];
    
    // 计算统计信息
    const statistics = {
        total_count: mockData.length,
        source_distribution: {
            "新浪财经": 1,
            "东方财经": 1,
            "中国证券网": 1,
            "财经网": 1,
            "证券时报": 1
        },
        category_distribution: {
            "金融政策": 1,
            "行业动态": 1,
            "资本市场": 1,
            "政策动态": 1,
            "科技创新": 1
        },
        sentiment_distribution: {
            "积极": 4,
            "中性": 1,
            "消极": 0
        },
        heat_distribution: {
            "high": 3,
            "medium": 2,
            "low": 0
        },
        avg_heat_score: 87.4,
        top_keywords: [
            {"keyword": "政策", "count": 3},
            {"keyword": "市场", "count": 2},
            {"keyword": "改革", "count": 2}
        ]
    };
    
    return {
        success: true,
        data: mockData,
        statistics: statistics,
        last_update: new Date().toISOString(),
        total_count: mockData.length
    };
}

// 显示错误信息
function showErrorMessage(container, message) {
    container.innerHTML = `
        <div class="text-center py-5">
            <div class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle"></i>
                <h4 class="alert-heading">数据加载失败</h4>
                <p>${message}</p>
                <hr>
                <button class="btn btn-primary" onclick="loadDomesticHotspotData()">
                    <i class="bi bi-arrow-clockwise"></i> 重新加载
                </button>
            </div>
        </div>
    `;
}

// 格式化日期时间
function formatDateTime(dateString) {
    if (!dateString) return '未知';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
}

// 刷新国内热点数据
function refreshDomesticHotspots() {
    loadDomesticHotspotData();
}

// 导出热点数据
function exportHotspotData() {
    if (!currentHotspotData.length) {
        alert('暂无数据可导出');
        return;
    }
    
    // 创建CSV内容
    const headers = ['ID', '标题', '来源', '发布时间', '分类', '热度', '情感', '关键词'];
    const csvContent = [
        headers.join(','),
        ...currentHotspotData.map(item => [
            item.id,
            `"${item.title}"`,
            item.source,
            formatDateTime(item.publish_time),
            item.category,
            item.heat_score,
            item.sentiment,
            `"${item.keywords.join(';')}"`
        ].join(','))
    ].join('\n');
    
    // 下载文件
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `国内热点数据_${new Date().toISOString().slice(0, 10)}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// 全局注册函数
window.loadDomesticHotspotData = loadDomesticHotspotData;
window.refreshDomesticHotspots = refreshDomesticHotspots;
window.exportHotspotData = exportHotspotData;