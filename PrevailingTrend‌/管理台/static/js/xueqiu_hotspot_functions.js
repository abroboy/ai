/**
 * 雪球热点数据模块 - 功能函数
 */

// 加载雪球热点数据
async function loadXueqiuHotspotData() {
    try {
        showLoading(true);
        
        // 从JSON文件加载数据
        const response = await fetch('static/data/xueqiu_hotspot_data.json');
        const data = await response.json();
        
        if (data.success) {
            xueqiuHotspotData = data.data;
            updateOverviewCards();
            renderTopicsView();
            renderStocksView();
            renderSentimentView();
        } else {
            throw new Error(data.message || '数据加载失败');
        }
        
    } catch (error) {
        console.error('加载雪球热点数据失败:', error);
        showError('数据加载失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 更新概览卡片
function updateOverviewCards() {
    if (!xueqiuHotspotData) return;
    
    const totalTopics = xueqiuHotspotData.hot_topics.length;
    const trendingStocks = xueqiuHotspotData.trending_stocks.length;
    const sentimentScore = Math.round(xueqiuHotspotData.market_sentiment.sentiment_score * 100);
    const totalViews = xueqiuHotspotData.hot_topics.reduce((sum, topic) => sum + topic.view_count, 0);
    
    document.getElementById('total-topics').textContent = totalTopics;
    document.getElementById('trending-stocks').textContent = trendingStocks;
    document.getElementById('sentiment-score').textContent = sentimentScore;
    document.getElementById('total-views').textContent = formatNumber(totalViews);
}

// 渲染话题视图
function renderTopicsView() {
    if (!xueqiuHotspotData) return;
    
    const topicsList = document.getElementById('topics-list');
    const topics = xueqiuHotspotData.hot_topics;
    
    let html = '';
    topics.forEach(topic => {
        const sentimentClass = topic.sentiment === 'positive' ? 'success' : 
                              topic.sentiment === 'negative' ? 'danger' : 'warning';
        
        html += `
            <div class="topic-item mb-3">
                <div class="card">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-8">
                                <h6 class="card-title">${topic.title}</h6>
                                <p class="card-text text-muted">${topic.content.substring(0, 150)}...</p>
                                <div class="topic-meta">
                                    <span class="badge bg-${sentimentClass}">${getSentimentText(topic.sentiment)}</span>
                                    <span class="text-muted ms-2">
                                        <i class="bi bi-person"></i> ${topic.author}
                                    </span>
                                    <span class="text-muted ms-2">
                                        <i class="bi bi-clock"></i> ${topic.publish_time}
                                    </span>
                                </div>
                                <div class="topic-tags mt-2">
                                    ${topic.tags.map(tag => `<span class="badge bg-light text-dark me-1">#${tag}</span>`).join('')}
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="topic-stats">
                                    <div class="stat-item">
                                        <i class="bi bi-eye text-primary"></i>
                                        <span>${formatNumber(topic.view_count)}</span>
                                    </div>
                                    <div class="stat-item">
                                        <i class="bi bi-chat text-success"></i>
                                        <span>${topic.comment_count}</span>
                                    </div>
                                    <div class="stat-item">
                                        <i class="bi bi-heart text-danger"></i>
                                        <span>${topic.like_count}</span>
                                    </div>
                                    <div class="stat-item">
                                        <i class="bi bi-fire text-warning"></i>
                                        <span>${topic.heat_score}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    topicsList.innerHTML = html;
}

// 渲染股票视图
function renderStocksView() {
    if (!xueqiuHotspotData) return;
    
    const tableBody = document.getElementById('stocks-table-body');
    const stocks = xueqiuHotspotData.trending_stocks;
    
    let html = '';
    stocks.forEach((stock, index) => {
        const changeClass = stock.change_percent > 0 ? 'text-success' : 
                           stock.change_percent < 0 ? 'text-danger' : 'text-muted';
        const changeIcon = stock.change_percent > 0 ? '↑' : 
                          stock.change_percent < 0 ? '↓' : '→';
        
        html += `
            <tr>
                <td><span class="badge bg-primary">${stock.hot_rank}</span></td>
                <td><code>${stock.code}</code></td>
                <td><strong>${stock.name}</strong></td>
                <td>¥${stock.current_price.toFixed(2)}</td>
                <td class="${changeClass}">
                    ${changeIcon} ${Math.abs(stock.change_percent).toFixed(2)}%
                </td>
                <td>${formatNumber(stock.volume)}</td>
                <td>
                    <span class="badge bg-warning">${stock.mention_count}</span>
                </td>
                <td>
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar ${getSentimentProgressClass(stock.sentiment_score)}" 
                             style="width: ${stock.sentiment_score * 100}%">
                            ${Math.round(stock.sentiment_score * 100)}
                        </div>
                    </div>
                </td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = html;
}

// 渲染情绪视图
function renderSentimentView() {
    if (!xueqiuHotspotData) return;
    
    // 渲染情绪分布图
    renderSentimentChart();
    
    // 渲染关键词趋势图
    renderKeywordsChart();
}

// 绑定事件
function bindXueqiuHotspotEvents() {
    // 视图切换按钮
    document.querySelectorAll('[data-view]').forEach(button => {
        button.addEventListener('click', function() {
            const view = this.dataset.view;
            switchView(view);
            
            // 更新按钮状态
            document.querySelectorAll('[data-view]').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// 切换视图
function switchView(viewName) {
    // 隐藏所有视图
    document.querySelectorAll('.content-view').forEach(view => {
        view.style.display = 'none';
    });
    
    // 显示指定视图
    const targetView = document.getElementById(viewName + '-view');
    if (targetView) {
        targetView.style.display = 'block';
    }
}

// 工具函数
function getSentimentText(sentiment) {
    switch(sentiment) {
        case 'positive': return '积极';
        case 'negative': return '消极';
        case 'neutral': return '中性';
        default: return '未知';
    }
}

function getSentimentProgressClass(score) {
    if (score >= 0.7) return 'bg-success';
    if (score >= 0.4) return 'bg-warning';
    return 'bg-danger';
}

function formatNumber(num) {
    if (num >= 100000000) {
        return (num / 100000000).toFixed(1) + '亿';
    } else if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万';
    }
    return num.toString();
}

function showLoading(show) {
    const indicator = document.getElementById('loading-indicator');
    if (indicator) {
        indicator.style.display = show ? 'block' : 'none';
    }
}

function showError(message) {
    alert('错误: ' + message);
}

// 刷新数据
function refreshXueqiuData() {
    loadXueqiuHotspotData();
}

// 导出数据
function exportXueqiuData() {
    if (!xueqiuHotspotData) {
        alert('暂无数据可导出');
        return;
    }
    
    const dataStr = JSON.stringify(xueqiuHotspotData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `雪球热点数据_${new Date().toISOString().slice(0, 10)}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
}

// 渲染图表函数
function renderSentimentChart() {
    const ctx = document.getElementById('sentiment-chart');
    if (!ctx || !xueqiuHotspotData) return;
    
    const sentiment = xueqiuHotspotData.market_sentiment;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['积极', '消极', '中性'],
            datasets: [{
                data: [
                    sentiment.positive_ratio * 100,
                    sentiment.negative_ratio * 100,
                    sentiment.neutral_ratio * 100
                ],
                backgroundColor: ['#28a745', '#dc3545', '#ffc107']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function renderKeywordsChart() {
    const ctx = document.getElementById('keywords-chart');
    if (!ctx || !xueqiuHotspotData) return;
    
    const keywords = xueqiuHotspotData.keyword_trends;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: keywords.map(k => k.keyword),
            datasets: [{
                label: '提及次数',
                data: keywords.map(k => k.mention_count),
                backgroundColor: '#007bff'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}