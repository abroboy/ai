/**
 * 雪球热点数据辅助函数
 * 大势所趋风险框架管理台
 */

// 创建话题卡片
function createTopicCard(topic) {
    const timeAgo = getTimeAgo(topic.publish_time);
    const sentimentBadge = getSentimentBadge(topic.sentiment);
    
    return `
        <div class="topic-item mb-3 p-3 border rounded">
            <div class="d-flex justify-content-between align-items-start mb-2">
                <div class="topic-tags">
                    ${topic.tags.map(tag => `<span class="badge bg-secondary me-1">${tag}</span>`).join('')}
                </div>
                <div class="topic-stats">
                    ${sentimentBadge}
                    <span class="badge bg-warning text-dark">${topic.heat_score.toFixed(1)}°</span>
                </div>
            </div>
            
            <h6 class="topic-title">${topic.title}</h6>
            <p class="topic-content text-muted small">${topic.content}</p>
            
            <div class="d-flex justify-content-between align-items-center">
                <div class="topic-author">
                    <small class="text-muted">
                        <i class="bi bi-person"></i> ${topic.author} · ${timeAgo}
                    </small>
                </div>
                <div class="topic-engagement">
                    <small class="text-muted">
                        <i class="bi bi-eye"></i> ${formatNumber(topic.view_count)}
                        <i class="bi bi-chat ms-2"></i> ${topic.comment_count}
                        <i class="bi bi-heart ms-2"></i> ${topic.like_count}
                    </small>
                </div>
            </div>
            
            ${topic.related_stocks && topic.related_stocks.length > 0 ? `
                <div class="related-stocks mt-2">
                    <small class="text-muted">相关股票: </small>
                    ${topic.related_stocks.map(stock => `<span class="badge bg-info text-white me-1">${stock}</span>`).join('')}
                </div>
            ` : ''}
        </div>
    `;
}

// 创建股票卡片
function createStockCard(stock) {
    const changeColor = stock.change_percent >= 0 ? 'text-success' : 'text-danger';
    const changeIcon = stock.change_percent >= 0 ? 'bi-arrow-up' : 'bi-arrow-down';
    
    return `
        <div class="stock-item mb-2 p-2 border rounded">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <div class="fw-bold">${stock.name}</div>
                    <small class="text-muted">${stock.code}</small>
                </div>
                <div class="text-end">
                    <div class="fw-bold">¥${stock.current_price}</div>
                    <small class="${changeColor}">
                        <i class="bi ${changeIcon}"></i> ${stock.change_percent.toFixed(1)}%
                    </small>
                </div>
            </div>
            <div class="mt-1">
                <small class="text-muted">
                    讨论: ${stock.mention_count} · 
                    情绪: ${(stock.sentiment_score * 100).toFixed(0)}%
                </small>
            </div>
        </div>
    `;
}

// 获取情绪颜色
function getSentimentColor(score) {
    if (score >= 0.7) return 'text-success';
    if (score >= 0.5) return 'text-warning';
    return 'text-danger';
}

// 获取情绪徽章
function getSentimentBadge(sentiment) {
    const badges = {
        'positive': '<span class="badge bg-success">积极</span>',
        'negative': '<span class="badge bg-danger">消极</span>',
        'neutral': '<span class="badge bg-secondary">中性</span>'
    };
    return badges[sentiment] || badges['neutral'];
}

// 格式化数字
function formatNumber(num) {
    if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万';
    }
    return num.toString();
}

// 获取时间差描述
function getTimeAgo(timestamp) {
    const now = new Date();
    const time = new Date(timestamp);
    const diffMinutes = Math.floor((now - time) / (1000 * 60));
    
    if (diffMinutes < 1) return '刚刚';
    if (diffMinutes < 60) return `${diffMinutes}分钟前`;
    if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}小时前`;
    return `${Math.floor(diffMinutes / 1440)}天前`;
}

// 渲染情绪分布图表
function renderSentimentChart(sentiment) {
    const canvas = document.getElementById('sentimentChart');
    if (!canvas || typeof Chart === 'undefined') return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['积极', '中性', '消极'],
            datasets: [{
                data: [
                    sentiment.positive_ratio * 100,
                    sentiment.neutral_ratio * 100,
                    sentiment.negative_ratio * 100
                ],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.8)',
                    'rgba(108, 117, 125, 0.8)',
                    'rgba(220, 53, 69, 0.8)'
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(108, 117, 125, 1)',
                    'rgba(220, 53, 69, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: '市场情绪分布'
                },
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// 刷新雪球热点数据
function refreshXueqiuHotspotData() {
    initXueqiuHotspotModule();
}

// 导出函数
if (typeof window !== 'undefined') {
    window.createTopicCard = createTopicCard;
    window.createStockCard = createStockCard;
    window.getSentimentColor = getSentimentColor;
    window.getSentimentBadge = getSentimentBadge;
    window.formatNumber = formatNumber;
    window.getTimeAgo = getTimeAgo;
    window.renderSentimentChart = renderSentimentChart;
    window.refreshXueqiuHotspotData = refreshXueqiuHotspotData;
}