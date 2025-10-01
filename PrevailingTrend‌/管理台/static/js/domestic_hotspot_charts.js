/**
 * 国内热点数据图表模块
 */

// 初始化分类分布图表
function initCategoryChart(categoryData) {
    const chartDom = document.getElementById('category-chart');
    if (!chartDom || typeof echarts === 'undefined') {
        console.warn('ECharts未加载或图表容器不存在');
        return;
    }
    
    const myChart = echarts.init(chartDom);
    
    const data = Object.entries(categoryData).map(([name, value]) => ({
        name,
        value
    }));
    
    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: Object.keys(categoryData)
        },
        series: [
            {
                name: '分类分布',
                type: 'pie',
                radius: '50%',
                data: data,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    
    myChart.setOption(option);
    
    // 响应窗口大小变化
    window.addEventListener('resize', function() {
        myChart.resize();
    });
}

// 初始化热度趋势图表
function initHeatTrendChart(trendData) {
    const chartDom = document.getElementById('heat-trend-chart');
    if (!chartDom || typeof echarts === 'undefined') {
        return;
    }
    
    const myChart = echarts.init(chartDom);
    
    const option = {
        title: {
            text: '热度趋势'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['热度值']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: trendData.map(item => item.time)
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: '热度值',
                type: 'line',
                stack: 'Total',
                data: trendData.map(item => item.value)
            }
        ]
    };
    
    myChart.setOption(option);
    
    window.addEventListener('resize', function() {
        myChart.resize();
    });
}

// 初始化情感分布图表
function initSentimentChart(sentimentData) {
    const chartDom = document.getElementById('sentiment-chart');
    if (!chartDom || typeof echarts === 'undefined') {
        return;
    }
    
    const myChart = echarts.init(chartDom);
    
    const option = {
        title: {
            text: '情感分布',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                name: '情感分布',
                type: 'pie',
                radius: '50%',
                data: [
                    { value: sentimentData.积极 || 0, name: '积极', itemStyle: { color: '#28a745' } },
                    { value: sentimentData.中性 || 0, name: '中性', itemStyle: { color: '#ffc107' } },
                    { value: sentimentData.消极 || 0, name: '消极', itemStyle: { color: '#dc3545' } }
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    
    myChart.setOption(option);
    
    window.addEventListener('resize', function() {
        myChart.resize();
    });
}