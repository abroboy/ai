/**
 * 全球资金流向模块
 * 提供全球资金流向数据的展示和分析功能
 */

// 全球资金流向主函数
function loadGlobalCapitalFlow() {
    const content = document.getElementById('content');
    
    // 显示加载状态
    content.innerHTML = `
        <div class="text-center py-5">
            <div class="loading-indicator"></div>
            <p class="mt-3">正在加载全球资金流向数据...</p>
        </div>
    `;
    
    // 模拟数据加载延迟
    setTimeout(() => {
        renderGlobalCapitalFlowInterface();
        loadCapitalFlowData();
    }, 800);
}

// 渲染全球资金流向界面
function renderGlobalCapitalFlowInterface() {
    const content = document.getElementById('content');
    
    content.innerHTML = `
        <div class="global-capital-flow-container">
            <!-- 头部控制面板 -->
            <div class="control-panel mb-4">
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <h4 class="mb-0">
                            <i class="bi bi-globe2"></i> 全球资金流向监控
                            <span class="realtime-badge ms-2">实时</span>
                        </h4>
                    </div>
                    <div class="col-md-6 text-end">
                        <div class="btn-group" role="group">
                            <button type="button" class="btn btn-outline-primary btn-sm" onclick="refreshCapitalFlowData()">
                                <i class="bi bi-arrow-clockwise"></i> 刷新
                            </button>
                            <button type="button" class="btn btn-outline-secondary btn-sm" onclick="exportCapitalFlowData()">
                                <i class="bi bi-download"></i> 导出
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 数据概览卡片 -->
            <div class="overview-cards mb-4">
                <div class="row">
                    <div class="col-md-3">
                        <div class="card overview-card">
                            <div class="card-body text-center">
                                <div class="overview-icon text-primary">
                                    <i class="bi bi-arrow-up-circle"></i>
                                </div>
                                <h5 class="card-title">主力净流入</h5>
                                <h3 class="text-primary" id="main-net-inflow">--</h3>
                                <small class="text-muted">今日累计</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card overview-card">
                            <div class="card-body text-center">
                                <div class="overview-icon text-success">
                                    <i class="bi bi-arrow-up-square"></i>
                                </div>
                                <h5 class="card-title">超大单净流入</h5>
                                <h3 class="text-success" id="super-large-inflow">--</h3>
                                <small class="text-muted">今日累计</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card overview-card">
                            <div class="card-body text-center">
                                <div class="overview-icon text-warning">
                                    <i class="bi bi-arrow-down-square"></i>
                                </div>
                                <h5 class="card-title">大单净流入</h5>
                                <h3 class="text-warning" id="large-inflow">--</h3>
                                <small class="text-muted">今日累计</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card overview-card">
                            <div class="card-body text-center">
                                <div class="overview-icon text-info">
                                    <i class="bi bi-graph-up"></i>
                                </div>
                                <h5 class="card-title">市场活跃度</h5>
                                <h3 class="text-info" id="market-activity">--</h3>
                                <small class="text-muted">综合指数</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 图表区域 -->
            <div class="charts-section mb-4">
                <div class="row">
                    <div class="col-md-8">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="mb-0">
                                    <i class="bi bi-bar-chart"></i> 资金流向趋势图
                                </h5>
                            </div>
                            <div class="card-body">
                                <canvas id="capitalFlowChart" width="400" height="200"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="mb-0">
                                    <i class="bi bi-pie-chart"></i> 资金分布
                                </h5>
                            </div>
                            <div class="card-body">
                                <canvas id="capitalDistributionChart" width="300" height="300"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 数据表格 -->
            <div class="data-table-section">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">
                            <i class="bi bi-table"></i> 详细数据表
                        </h5>
                        <div class="table-controls">
                            <select class="form-select form-select-sm" id="timeRangeSelect" onchange="filterDataByTimeRange()">
                                <option value="7">最近7天</option>
                                <option value="30" selected>最近30天</option>
                                <option value="90">最近90天</option>
                            </select>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover" id="capitalFlowTable">
                                <thead class="table-dark">
                                    <tr>
                                        <th>日期</th>
                                        <th>上证指数</th>
                                        <th>深证指数</th>
                                        <th>主力净流入</th>
                                        <th>超大单净流入</th>
                                        <th>大单净流入</th>
                                        <th>中单净流入</th>
                                        <th>小单净流入</th>
                                        <th>操作</th>
                                    </tr>
                                </thead>
                                <tbody id="capitalFlowTableBody">
                                    <!-- 数据将通过JavaScript动态加载 -->
                                </tbody>
                            </table>
                        </div>
                        <nav aria-label="数据分页">
                            <ul class="pagination justify-content-center" id="tablePagination">
                                <!-- 分页将通过JavaScript动态生成 -->
                            </ul>
                        </nav>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 加载资金流向数据
async function loadCapitalFlowData() {
    try {
        // 首先尝试从API加载数据
        let data = [];
        try {
            const apiResponse = await fetch('http://localhost:5001/api/global_capital_flow/market_data?days=120');
            const apiData = await apiResponse.json();
            
            if (apiData.success && apiData.data) {
                data = apiData.data.map(item => ({
                    '日期': item.date,
                    '上证-收盘价': item.shanghai_close,
                    '上证-涨跌幅': item.shanghai_change,
                    '深证-收盘价': item.shenzhen_close,
                    '深证-涨跌幅': item.shenzhen_change,
                    '主力净流入-净额': item.main_net_inflow,
                    '主力净流入-净占比': item.main_net_inflow_ratio,
                    '超大单净流入-净额': item.super_large_inflow,
                    '超大单净流入-净占比': item.super_large_inflow_ratio,
                    '大单净流入-净额': item.large_inflow,
                    '大单净流入-净占比': item.large_inflow_ratio,
                    '中单净流入-净额': item.medium_inflow,
                    '中单净流入-净占比': item.medium_inflow_ratio,
                    '小单净流入-净额': item.small_inflow,
                    '小单净流入-净占比': item.small_inflow_ratio
                }));
            }
        } catch (apiError) {
            console.log('API服务不可用，尝试从CSV文件加载数据:', apiError);
            
            // 如果API不可用，从CSV文件加载数据
            const response = await fetch('api/akshare_test_ak_stock_market_fund_flow.csv');
            const csvText = await response.text();
            
            // 解析CSV数据
            data = parseCSVData(csvText);
        }
        
        // 更新概览卡片
        updateOverviewCards(data);
        
        // 渲染图表
        renderCapitalFlowChart(data);
        renderCapitalDistributionChart(data);
        
        // 渲染数据表格
        renderDataTable(data);
        
    } catch (error) {
        console.error('加载资金流向数据失败:', error);
        showErrorMessage('数据加载失败，请稍后重试');
    }
}

// 解析CSV数据
function parseCSVData(csvText) {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',');
    const data = [];
    
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        const row = {};
        
        headers.forEach((header, index) => {
            row[header.trim()] = values[index] ? values[index].trim() : '';
        });
        
        data.push(row);
    }
    
    return data;
}

// 更新概览卡片
function updateOverviewCards(data) {
    if (data.length === 0) return;
    
    const latestData = data[data.length - 1];
    
    // 主力净流入
    const mainNetInflow = parseFloat(latestData['主力净流入-净额']) || 0;
    document.getElementById('main-net-inflow').textContent = formatCurrency(mainNetInflow);
    
    // 超大单净流入
    const superLargeInflow = parseFloat(latestData['超大单净流入-净额']) || 0;
    document.getElementById('super-large-inflow').textContent = formatCurrency(superLargeInflow);
    
    // 大单净流入
    const largeInflow = parseFloat(latestData['大单净流入-净额']) || 0;
    document.getElementById('large-inflow').textContent = formatCurrency(largeInflow);
    
    // 计算市场活跃度（基于成交量和流入流出比例）
    const marketActivity = calculateMarketActivity(data.slice(-7)); // 最近7天
    document.getElementById('market-activity').textContent = marketActivity.toFixed(1);
}

// 计算市场活跃度
function calculateMarketActivity(recentData) {
    if (recentData.length === 0) return 0;
    
    let totalVolume = 0;
    let positiveFlowDays = 0;
    
    recentData.forEach(day => {
        const mainFlow = parseFloat(day['主力净流入-净额']) || 0;
        totalVolume += Math.abs(mainFlow);
        if (mainFlow > 0) positiveFlowDays++;
    });
    
    const avgVolume = totalVolume / recentData.length;
    const positiveRatio = positiveFlowDays / recentData.length;
    
    // 活跃度计算公式（0-100分）
    return Math.min(100, (avgVolume / 1000000000) * 10 + positiveRatio * 50);
}

// 渲染资金流向趋势图
function renderCapitalFlowChart(data) {
    const ctx = document.getElementById('capitalFlowChart').getContext('2d');
    
    // 取最近30天数据
    const recentData = data.slice(-30);
    const labels = recentData.map(item => item['日期']);
    const mainFlowData = recentData.map(item => parseFloat(item['主力净流入-净额']) / 100000000); // 转换为亿元
    const superLargeFlowData = recentData.map(item => parseFloat(item['超大单净流入-净额']) / 100000000);
    const largeFlowData = recentData.map(item => parseFloat(item['大单净流入-净额']) / 100000000);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: '主力净流入',
                data: mainFlowData,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                tension: 0.1
            }, {
                label: '超大单净流入',
                data: superLargeFlowData,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                tension: 0.1
            }, {
                label: '大单净流入',
                data: largeFlowData,
                borderColor: 'rgb(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: '金额 (亿元)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: '日期'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: '资金流向趋势 (最近30天)'
                }
            }
        }
    });
}

// 渲染资金分布饼图
function renderCapitalDistributionChart(data) {
    const ctx = document.getElementById('capitalDistributionChart').getContext('2d');
    
    if (data.length === 0) return;
    
    const latestData = data[data.length - 1];
    const superLarge = Math.abs(parseFloat(latestData['超大单净流入-净额']) || 0);
    const large = Math.abs(parseFloat(latestData['大单净流入-净额']) || 0);
    const medium = Math.abs(parseFloat(latestData['中单净流入-净额']) || 0);
    const small = Math.abs(parseFloat(latestData['小单净流入-净额']) || 0);
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['超大单', '大单', '中单', '小单'],
            datasets: [{
                data: [superLarge, large, medium, small],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 205, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 205, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: '今日资金分布'
                }
            }
        }
    });
}

// 渲染数据表格
function renderDataTable(data, page = 1, pageSize = 10) {
    const tbody = document.getElementById('capitalFlowTableBody');
    const startIndex = (page - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    const pageData = data.slice(startIndex, endIndex);
    
    tbody.innerHTML = '';
    
    pageData.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row['日期']}</td>
            <td>${parseFloat(row['上证-收盘价']).toFixed(2)}</td>
            <td>${parseFloat(row['深证-收盘价']).toFixed(2)}</td>
            <td class="${getFlowClass(row['主力净流入-净额'])}">${formatCurrency(row['主力净流入-净额'])}</td>
            <td class="${getFlowClass(row['超大单净流入-净额'])}">${formatCurrency(row['超大单净流入-净额'])}</td>
            <td class="${getFlowClass(row['大单净流入-净额'])}">${formatCurrency(row['大单净流入-净额'])}</td>
            <td class="${getFlowClass(row['中单净流入-净额'])}">${formatCurrency(row['中单净流入-净额'])}</td>
            <td class="${getFlowClass(row['小单净流入-净额'])}">${formatCurrency(row['小单净流入-净额'])}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="viewDayDetail('${row['日期']}')">
                    <i class="bi bi-eye"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
    
    // 渲染分页
    renderPagination(data.length, page, pageSize);
}

// 渲染分页
function renderPagination(totalItems, currentPage, pageSize) {
    const totalPages = Math.ceil(totalItems / pageSize);
    const pagination = document.getElementById('tablePagination');
    
    pagination.innerHTML = '';
    
    // 上一页
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `<a class="page-link" href="#" onclick="changePage(${currentPage - 1})">上一页</a>`;
    pagination.appendChild(prevLi);
    
    // 页码
    for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === currentPage ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#" onclick="changePage(${i})">${i}</a>`;
        pagination.appendChild(li);
    }
    
    // 下一页
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
    nextLi.innerHTML = `<a class="page-link" href="#" onclick="changePage(${currentPage + 1})">下一页</a>`;
    pagination.appendChild(nextLi);
}

// 工具函数
function formatCurrency(value) {
    const num = parseFloat(value) || 0;
    if (Math.abs(num) >= 100000000) {
        return (num / 100000000).toFixed(2) + '亿';
    } else if (Math.abs(num) >= 10000) {
        return (num / 10000).toFixed(2) + '万';
    } else {
        return num.toFixed(2);
    }
}

function getFlowClass(value) {
    const num = parseFloat(value) || 0;
    return num >= 0 ? 'text-success' : 'text-danger';
}

function showErrorMessage(message) {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="alert alert-danger text-center">
            <i class="bi bi-exclamation-triangle"></i>
            <strong>错误：</strong> ${message}
        </div>
    `;
}

// 事件处理函数
function refreshCapitalFlowData() {
    loadCapitalFlowData();
}

function exportCapitalFlowData() {
    alert('导出功能开发中...');
}

function filterDataByTimeRange() {
    const timeRange = document.getElementById('timeRangeSelect').value;
    // 重新加载数据并应用时间过滤
    loadCapitalFlowData();
}

function changePage(page) {
    // 重新渲染当前页数据
    loadCapitalFlowData();
}

function viewDayDetail(date) {
    alert(`查看 ${date} 的详细数据功能开发中...`);
}

// 确保Chart.js库可用
if (typeof Chart === 'undefined') {
    // 动态加载Chart.js
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
    document.head.appendChild(script);
}