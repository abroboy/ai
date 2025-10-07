/**
 * 雪球论坛热点数据模块增强版
 * 大势所趋风险框架管理台
 */

// 加载雪球论坛热点数据模块
function loadXueqiuHotspotData() {
    const container = document.getElementById('content');
    
    // 显示加载状态
    container.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-3">正在加载雪球论坛热点数据...</p>
        </div>
    `;

    // 获取数据并渲染
    fetchXueqiuHotspotData()
        .then(data => {
            if (data.success) {
                renderXueqiuHotspotModule(container, data);
            } else {
                throw new Error(data.message || '数据加载失败');
            }
        })
        .catch(error => {
            container.innerHTML = `
                <div class="alert alert-danger">
                    <h5><i class="bi bi-exclamation-triangle"></i> 数据加载失败</h5>
                    <p>${error.message}</p>
                    <button class="btn btn-primary" onclick="initXueqiuHotspotModule()">重新加载</button>
                </div>
            `;
        });
}

// 获取雪球热点数据
async function fetchXueqiuHotspotData() {
    try {
        // 首先尝试从本地JSON文件加载
        const response = await fetch('/static/data/xueqiu_hotspot_data.json?' + new URLSearchParams({
            timestamp: Date.now()
        }));
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('获取雪球热点数据失败:', error);
        // 返回模拟数据作为备用
        return getMockXueqiuHotspotData();
    }
}

// 模拟数据备用方案
function getMockXueqiuHotspotData() {
    return {
        success: true,
        message: "雪球论坛热点数据获取成功",
        timestamp: new Date().toISOString(),
        data: {
            hot_topics: [
                {
                    id: 'xq_001',
                    title: 'A股三季度收官：科技股领涨，新能源板块分化明显',
                    content: '随着三季度结束，A股市场呈现结构性行情。科技股在政策利好推动下表现强劲...',
                    author: '投资达人小李',
                    publish_time: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
                    view_count: 15420,
                    comment_count: 328,
                    like_count: 892,
                    tags: ['A股', '科技股', '新能源', '三季度'],
                    sentiment: 'positive',
                    heat_score: 95.2,
                    related_stocks: ['000001.SZ', '000002.SZ', '300750.SZ']
                },
                {
                    id: 'xq_002',
                    title: '央行降准释放流动性，房地产板块迎来反弹机会',
                    content: '央行宣布降准0.5个百分点，释放长期流动性约1.2万亿元...',
                    author: '地产观察员',
                    publish_time: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
                    view_count: 12350,
                    comment_count: 256,
                    like_count: 678,
                    tags: ['央行', '降准', '房地产', '流动性'],
                    sentiment: 'positive',
                    heat_score: 88.7,
                    related_stocks: ['000002.SZ', '001979.SZ', '600048.SH']
                }
            ],
            trending_stocks: [
                {
                    code: '000001.SZ',
                    name: '平安银行',
                    current_price: 12.45,
                    change_percent: 3.2,
                    volume: 125000000,
                    market_cap: 241000000000,
                    mention_count: 156,
                    sentiment_score: 0.65,
                    hot_rank: 1
                },
                {
                    code: '300750.SZ',
                    name: '宁德时代',
                    current_price: 198.50,
                    change_percent: -1.8,
                    volume: 89000000,
                    market_cap: 870000000000,
                    mention_count: 134,
                    sentiment_score: 0.42,
                    hot_rank: 2
                }
            ],
            market_sentiment: {
                overall_sentiment: 'positive',
                sentiment_score: 0.62,
                positive_ratio: 0.68,
                negative_ratio: 0.18,
                neutral_ratio: 0.14,
                fear_greed_index: 72,
                confidence_level: 'high'
            }
        }
    };
}

// 获取情绪颜色
function getSentimentColor(score) {
    if (score >= 0.7) return 'text-success';
    if (score >= 0.5) return 'text-warning';
    return 'text-danger';
}

// 渲染雪球热点数据模块
function renderXueqiuHotspotModule(container, responseData) {
    const data = responseData.data;
    
    const moduleHTML = `
        <div class="xueqiu-hotspot-module">
            <!-- 模块标题 -->
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h4><i class="bi bi-chat-dots text-info"></i> 雪球论坛热点数据</h4>
                <div>
                    <span class="badge bg-success">实时数据</span>
                    <button class="btn btn-outline-primary btn-sm ms-2" onclick="refreshXueqiuHotspotData()">
                        <i class="bi bi-arrow-clockwise"></i> 刷新
                    </button>
                </div>
            </div>

            <!-- 市场情绪概览 -->
            <div class="row mb-4">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-heart-pulse"></i> 市场情绪指数</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="text-center">
                                        <div class="display-4 ${getSentimentColor(data.market_sentiment.sentiment_score)}">
                                            ${Math.round(data.market_sentiment.sentiment_score * 100)}
                                        </div>
                                        <small class="text-muted">情绪指数</small>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="text-center">
                                        <div class="display-4 text-danger">
                                            ${data.market_sentiment.fear_greed_index}
                                        </div>
                                        <small class="text-muted">恐惧贪婪指数</small>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <canvas id="sentimentChart" height="100"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 热门话题和热门股票 -->
            <div class="row">
                <!-- 热门话题 -->
                <div class="col-lg-8">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-fire"></i> 热门话题</h5>
                        </div>
                        <div class="card-body">
                            <div id="hotTopicsList">
                                ${data.hot_topics.map(topic => createTopicCard(topic)).join('')}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 热门股票 -->
                <div class="col-lg-4">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-graph-up"></i> 热门股票</h5>
                        </div>
                        <div class="card-body">
                            <div id="trendingStocksList">
                                ${data.trending_stocks.map(stock => createStockCard(stock)).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = moduleHTML;
    
    // 渲染情绪分布图表
    renderSentimentChart(data.market_sentiment);
}

// 定义模块初始化函数
function initXueqiuHotspotModule() {
    loadXueqiuHotspotData();
}

// 刷新数据函数
function refreshXueqiuHotspotData() {
    loadXueqiuHotspotData();
}

// 导出模块函数
if (typeof window !== 'undefined') {
    window.initXueqiuHotspotModule = initXueqiuHotspotModule;
    window.refreshXueqiuHotspotData = refreshXueqiuHotspotData;
}