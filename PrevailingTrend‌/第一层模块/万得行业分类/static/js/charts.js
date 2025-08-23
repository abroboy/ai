// 图表相关JavaScript
let trendChart = null;
let pieChart = null;

// 初始化图表
function initCharts() {
    initTrendChart();
    initPieChart();
}

// 初始化趋势图表
function initTrendChart() {
    const ctx = document.getElementById('trendChart');
    if (!ctx) return;
    
    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
            datasets: [{
                label: '行业数量',
                data: [120, 135, 142, 158, 165, 180],
                borderColor: '#4f46e5',
                backgroundColor: 'rgba(79, 70, 229, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: '股票数量',
                data: [1200, 1350, 1420, 1580, 1650, 1800],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// 初始化饼图
function initPieChart() {
    const ctx = document.getElementById('pieChart');
    if (!ctx) return;
    
    pieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['一级行业', '二级行业'],
            datasets: [{
                data: [30, 150],
                backgroundColor: [
                    '#4f46e5',
                    '#10b981'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        }
    });
}

// 更新图表数据
function updateCharts(period = 30) {
    // 这里可以根据实际数据更新图表
    console.log('更新图表，周期:', period);
}

// 页面加载完成后初始化图表
document.addEventListener('DOMContentLoaded', function() {
    // 延迟初始化，确保DOM完全加载
    setTimeout(initCharts, 100);
}); 