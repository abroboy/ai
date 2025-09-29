/**
 * 国内股票数据模块
 * 用于获取和展示国内A股市场数据
 */

// 全局变量
let stockData = [];
let industryData = {};
let sortField = 'heat_score';
let sortDirection = 'desc';
let currentFilter = '';
let lastUpdateTime = '';

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化页面
    initPage();
    
    // 加载数据
    loadDomesticStockData();
    
    // 绑定事件
    bindEvents();
});

/**
 * 加载国内股票数据
 */
function loadDomesticStockData() {
    // 显示加载状态
    document.getElementById('stockTableBody').innerHTML = `
        <tr>
            <td colspan="9" class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">加载中...</span>
                </div>
                <p class="mt-2">正在加载数据，请稍候...</p>
            </td>
        </tr>
    `;
    
    // 发起API请求
    fetch('/api/domestic/hotspots')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 更新数据
                stockData = data.data;
                lastUpdateTime = new Date().toLocaleString();
                
                // 处理数据
                processStockData();
                
                // 更新UI
                updateMarketOverview();
                renderStockTable();
                renderCharts();
            } else {
                // 显示错误信息
                document.getElementById('stockTableBody').innerHTML = `
                    <tr>
                        <td colspan="9" class="text-center text-danger">
                            <i class="bi bi-exclamation-triangle"></i>
                            <p class="mt-2">加载数据失败: ${data.message}</p>
                            <button class="btn btn-sm btn-outline-primary mt-2" onclick="loadDomesticStockData()">
                                <i class="bi bi-arrow-clockwise"></i> 重试
                            </button>
                        </td>
                    </tr>
                `;
            }
        })
        .catch(error => {
            // 显示错误信息
            document.getElementById('stockTableBody').innerHTML = `
                <tr>
                    <td colspan="9" class="text-center text-danger">
                        <i class="bi bi-exclamation-triangle"></i>
                        <p class="mt-2">网络错误: ${error.message}</p>
                        <button class="btn btn-sm btn-outline-primary mt-2" onclick="loadDomesticStockData()">
                            <i class="bi bi-arrow-clockwise"></i> 重试
                        </button>
                    </td>
                </tr>
            `;
        });
}

/**
 * 处理股票数据
 */
function processStockData() {
    // 重置行业数据
    industryData = {};
    
    // 处理每条股票数据
    stockData.forEach(stock => {
        // 处理行业数据
        if (!industryData[stock.industry]) {
            industryData[stock.industry] = {
                name: stock.industry,
                count: 0,
                upCount: 0,
                downCount: 0,
                totalMarketCap: 0,
                avgChange: 0,
                stocks: []
            };
        }
        
        // 更新行业统计
        const industry = industryData[stock.industry];
        industry.count++;
        industry.stocks.push(stock);
        
        if (stock.change_percent > 0) {
            industry.upCount++;
        } else if (stock.change_percent < 0) {
            industry.downCount++;
        }
        
        industry.totalMarketCap += stock.market_cap;
        industry.avgChange += stock.change_percent;
    });
    
    // 计算行业平均涨跌幅
    Object.values(industryData).forEach(industry => {
        industry.avgChange = industry.avgChange / industry.count;
    });
}

/**
 * 更新市场概览
 */
function updateMarketOverview() {
    // 计算统计数据
    const totalStocks = stockData.length;
    const upStocks = stockData.filter(stock => stock.change_percent > 0).length;
    const downStocks = stockData.filter(stock => stock.change_percent < 0).length;
    const flatStocks = totalStocks - upStocks - downStocks;
    
    // 计算市场情绪
    let sentiment = '中性';
    const upRatio = upStocks / totalStocks;
    if (upRatio > 0.6) {
        sentiment = '非常乐观';
    } else if (upRatio > 0.5) {
        sentiment = '乐观';
    } else if (upRatio < 0.4) {
        sentiment = '悲观';
    } else if (upRatio < 0.3) {
        sentiment = '非常悲观';
    }
    
    // 更新UI
    document.getElementById('total-stocks').textContent = totalStocks;
    document.getElementById('up-stocks').innerHTML = `<span class="text-success">${upStocks} (${(upRatio * 100).toFixed(1)}%)</span>`;
    document.getElementById('down-stocks').innerHTML = `<span class="text-danger">${downStocks} (${((downStocks / totalStocks) * 100).toFixed(1)}%)</span>`;
    document.getElementById('market-sentiment').textContent = sentiment;
}

/**
 * 渲染股票表格
 */
function renderStockTable() {
    // 获取表格体
    const tableBody = document.getElementById('stockTableBody');
    
    // 应用排序
    const sortedData = [...stockData].sort((a, b) => {
        if (sortDirection === 'asc') {
            return a[sortField] > b[sortField] ? 1 : -1;
        } else {
            return a[sortField] < b[sortField] ? 1 : -1;
        }
    });
    
    // 生成表格内容
    let html = '';
    sortedData.forEach(stock => {
        // 检查是否符合筛选条件
        if (!matchesFilter(stock)) return;
        
        // 生成行
        html += `
            <tr>
                <td>${stock.code}</td>
                <td>${stock.name}</td>
                <td>${stock.industry}</td>
                <td>${formatPrice(stock.price)}</td>
                <td>${formatChangePercent(stock.change_percent)}</td>
                <td>${formatVolume(stock.volume)}</td>
                <td>${formatMarketCap(stock.market_cap)}</td>
                <td>${formatHeatScore(stock.heat_score)}</td>
                <td>${formatSentiment(stock.sentiment)}</td>
            </tr>
        `;
    });
    
    // 更新表格
    if (html) {
        tableBody.innerHTML = html;
    } else {
        tableBody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center">
                    <p class="my-3">没有符合条件的数据</p>
                </td>
            </tr>
        `;
    }
}

/**
 * 检查股票是否符合筛选条件
 * @param {Object} stock 股票数据
 * @returns {boolean} 是否符合筛选条件
 */
function matchesFilter(stock) {
    // 获取筛选条件
    const industryFilter = document.getElementById('industryFilter').value;
    const changeFilter = document.getElementById('changeFilter').value;
    const marketCapFilter = document.getElementById('marketCapFilter').value;
    const searchText = document.getElementById('searchInput').value.toLowerCase();
    
    // 检查行业筛选
    if (industryFilter && stock.industry !== industryFilter) {
        return false;
    }
    
    // 检查涨跌幅筛选
    if (changeFilter) {
        switch (changeFilter) {
            case 'up':
                if (stock.change_percent <= 0) return false;
                break;
            case 'down':
                if (stock.change_percent >= 0) return false;
                break;
            case 'up5':
                if (stock.change_percent < 5) return false;
                break;
            case 'down5':
                if (stock.change_percent > -5) return false;
                break;
        }
    }
    
    // 检查市值筛选
    if (marketCapFilter) {
        switch (marketCapFilter) {
            case 'large':
                if (stock.market_cap < 100000000000) return false;
                break;
            case 'medium':
                if (stock.market_cap < 10000000000 || stock.market_cap > 100000000000) return false;
                break;
            case 'small':
                if (stock.market_cap > 10000000000) return false;
                break;
        }
    }
    
    // 检查搜索文本
    if (searchText) {
        if (!stock.code.toLowerCase().includes(searchText) && 
            !stock.name.toLowerCase().includes(searchText)) {
            return false;
        }
    }
    
    return true;
}

/**
 * 格式化价格
 * @param {number} price 价格
 * @returns {string} 格式化后的价格
 */
function formatPrice(price) {
    return price.toFixed(2);
}

/**
 * 格式化涨跌幅
 * @param {number} changePercent 涨跌幅
 * @returns {string} 格式化后的涨跌幅
 */
function formatChangePercent(changePercent) {
    const formattedValue = changePercent.toFixed(2) + '%';
    if (changePercent > 0) {
        return `<span class="text-success">+${formattedValue}</span>`;
    } else if (changePercent < 0) {
        return `<span class="text-danger">${formattedValue}</span>`;
    } else {
        return `<span>${formattedValue}</span>`;
    }
}

/**
 * 格式化成交量
 * @param {number} volume 成交量
 * @returns {string} 格式化后的成交量
 */
function formatVolume(volume) {
    if (volume >= 100000000) {
        return (volume / 100000000).toFixed(2) + '亿手';
    } else if (volume >= 10000) {
        return (volume / 10000).toFixed(2) + '万手';
    } else {
        return volume.toString() + '手';
    }
}

/**
 * 格式化市值
 * @param {number} marketCap 市值
 * @returns {string} 格式化后的市值
 */
function formatMarketCap(marketCap) {
    if (marketCap >= 100000000000) {
        return (marketCap / 100000000000).toFixed(2) + '千亿';
    } else if (marketCap >= 100000000) {
        return (marketCap / 100000000).toFixed(2) + '亿';
    } else {
        return (marketCap / 10000).toFixed(2) + '万';
    }
}

/**
 * 格式化热度分数
 * @param {number} heatScore 热度分数
 * @returns {string} 格式化后的热度分数
 */
function formatHeatScore(heatScore) {
    // 热度等级
    let heatLevel = '';
    if (heatScore >= 80) {
        heatLevel = '<span class="badge bg-danger">极热</span>';
    } else if (heatScore >= 60) {
        heatLevel = '<span class="badge bg-warning text-dark">热门</span>';
    } else if (heatScore >= 40) {
        heatLevel = '<span class="badge bg-info">关注</span>';
    } else if (heatScore >= 20) {
        heatLevel = '<span class="badge bg-secondary">一般</span>';
    } else {
        heatLevel = '<span class="badge bg-light text-dark">冷门</span>';
    }
    
    return `${heatScore.toFixed(0)} ${heatLevel}`;
}

/**
 * 格式化情绪
 * @param {string} sentiment 情绪
 * @returns {string} 格式化后的情绪
 */
function formatSentiment(sentiment) {
    // 情绪标签
    switch (sentiment) {
        case '非常乐观':
            return '<span class="badge bg-success">非常乐观</span>';
        case '乐观':
            return '<span class="badge bg-success">乐观</span>';
        case '中性':
            return '<span class="badge bg-secondary">中性</span>';
        case '悲观':
            return '<span class="badge bg-danger">悲观</span>';
        case '非常悲观':
            return '<span class="badge bg-danger">非常悲观</span>';
        default:
            return '<span class="badge bg-secondary">未知</span>';
    }
}

/**
 * 渲染图表
 */
function renderCharts() {
    renderIndustryChart();
    renderChangeDistributionChart();
}

/**
 * 渲染行业分布图表
 */
function renderIndustryChart() {
    // 获取图表容器
    const chartContainer = document.getElementById('industryChart');
    if (!chartContainer) return;
    
    // 准备数据
    const industries = Object.values(industryData)
        .sort((a, b) => b.totalMarketCap - a.totalMarketCap)
        .slice(0, 10); // 取市值前10的行业
    
    const categories = industries.map(industry => industry.name);
    const marketCapData = industries.map(industry => parseFloat((industry.totalMarketCap / 100000000).toFixed(2)));
    const stockCountData = industries.map(industry => industry.count);
    
    // 创建图表
    const chart = echarts.init(chartContainer);
    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            formatter: function(params) {
                const industry = params[0].name;
                const marketCap = params[0].value;
                const stockCount = params[1].value;
                
                return `
                    <div style="font-weight: bold; margin-bottom: 5px;">${industry}</div>
                    <div>总市值: ${marketCap}亿元</div>
                    <div>公司数量: ${stockCount}家</div>
                    <div>平均市值: ${(marketCap / stockCount).toFixed(2)}亿元/家</div>
                `;
            }
        },
        legend: {
            data: ['总市值(亿元)', '公司数量']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: categories,
                axisLabel: {
                    interval: 0,
                    rotate: 30
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '总市值(亿元)',
                position: 'left'
            },
            {
                type: 'value',
                name: '公司数量',
                position: 'right'
            }
        ],
        series: [
            {
                name: '总市值(亿元)',
                type: 'bar',
                data: marketCapData,
                itemStyle: {
                    color: '#5470c6'
                }
            },
            {
                name: '公司数量',
                type: 'line',
                yAxisIndex: 1,
                data: stockCountData,
                itemStyle: {
                    color: '#91cc75'
                }
            }
        ]
    };
    
    chart.setOption(option);
    
    // 窗口大小变化时重绘图表
    window.addEventListener('resize', function() {
        chart.resize();
    });
}

/**
 * 渲染涨跌分布图表
 */
function renderChangeDistributionChart() {
    // 获取图表容器
    const chartContainer = document.getElementById('changeDistributionChart');
    if (!chartContainer) return;
    
    // 准备数据
    const ranges = [
        {min: -100, max: -10, label: '跌幅>10%'},
        {min: -10, max: -5, label: '跌幅5%-10%'},
        {min: -5, max: -3, label: '跌幅3%-5%'},
        {min: -3, max: -1, label: '跌幅1%-3%'},
        {min: -1, max: 0, label: '跌幅<1%'},
        {min: 0, max: 1, label: '涨幅<1%'},
        {min: 1, max: 3, label: '涨幅1%-3%'},
        {min: 3, max: 5, label: '涨幅3%-5%'},
        {min: 5, max: 10, label: '涨幅5%-10%'},
        {min: 10, max: 100, label: '涨幅>10%'}
    ];
    
    // 统计每个区间的股票数量
    const data = ranges.map(range => {
        const count = stockData.filter(stock => 
            stock.change_percent >= range.min && 
            stock.change_percent < range.max
        ).length;
        
        return {
            name: range.label,
            value: count,
            itemStyle: {
                color: range.min < 0 ? '#c23531' : '#91cc75'
            }
        };
    });
    
    // 创建图表
    const chart = echarts.init(chartContainer);
    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            right: 10,
            top: 'center',
            data: ranges.map(range => range.label)
        },
        series: [
            {
                name: '涨跌分布',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '18',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: data
            }
        ]
    };
    
    chart.setOption(option);
    
    // 窗口大小变化时重绘图表
    window.addEventListener('resize', function() {
        chart.resize();
    });
}

/**
 * 绑定事件
 */
function bindEvents() {
    // 刷新按钮点击事件
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            loadDomesticStockData();
        });
    }
    
    // 搜索按钮点击事件
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            renderStockTable();
        });
    }
    
    // 搜索输入框回车事件
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                renderStockTable();
            }
        });
    }
    
    // 表格排序点击事件
    const sortableHeaders = document.querySelectorAll('.sortable');
    sortableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const field = this.getAttribute('data-field');
            
            // 切换排序方向
            if (sortField === field) {
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                sortField = field;
                sortDirection = 'desc';
            }
            
            // 更新排序图标
            updateSortIcons();
            
            // 重新渲染表格
            renderStockTable();
        });
    });
    
    // 应用筛选按钮点击事件
    const applyFilterBtn = document.getElementById('applyFilterBtn');
    if (applyFilterBtn) {
        applyFilterBtn.addEventListener('click', function() {
            // 关闭模态框
            const filterModal = bootstrap.Modal.getInstance(document.getElementById('filterModal'));
            if (filterModal) {
                filterModal.hide();
            }
            
            // 重新渲染表格
            renderStockTable();
        });
    }
    
    // 填充行业筛选下拉框
    const industryFilter = document.getElementById('industryFilter');
    if (industryFilter && Object.keys(industryData).length > 0) {
        // 清空现有选项
        while (industryFilter.options.length > 1) {
            industryFilter.remove(1);
        }
        
        // 添加行业选项
        const industries = Object.keys(industryData).sort();
        industries.forEach(industry => {
            const option = document.createElement('option');
            option.value = industry;
            option.textContent = industry;
            industryFilter.appendChild(option);
        });
    }
}

/**
 * 更新排序图标
 */
function updateSortIcons() {
    // 移除所有排序图标
    document.querySelectorAll('.sortable').forEach(header => {
        header.classList.remove('sort-asc', 'sort-desc');
    });
    
    // 添加当前排序图标
    const currentHeader = document.querySelector(`.sortable[data-field="${sortField}"]`);
    if (currentHeader) {
        currentHeader.classList.add(sortDirection === 'asc' ? 'sort-asc' : 'sort-desc');
    }
}

/**
 * 初始化页面
 */
function initPage() {
    // 创建页面结构
    const container = document.getElementById('content-container');
    if (!container) return;
    
    container.innerHTML = `
        <div class="row mb-4">
            <div class="col-md-8">
                <h2>国内股票市场数据</h2>
                <p class="text-muted">实时监控A股市场动态，提供股票行情、行业分析和热点追踪</p>
            </div>
            <div class="col-md-4 text-end">
                <div class="btn-group">
                    <button id="refreshBtn" class="btn btn-primary">
                        <i class="bi bi-arrow-clockwise"></i> 刷新数据
                    </button>
                    <button class="btn btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#filterModal">
                        <i class="bi bi-funnel"></i> 筛选
                    </button>
                </div>
            </div>
        </div>
        
        <div class="row mb-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="card-title mb-0">市场概览</h5>
                    </div>
                    <div class="card-body">
                        <div class="row" id="market-overview">
                            <div class="col-md-3 text-center">
                                <h3 id="total-stocks">--</h3>
                                <p>监控股票数</p>
                            </div>
                            <div class="col-md-3 text-center">
                                <h3 id="up-stocks">--</h3>
                                <p>上涨股票</p>
                            </div>
                            <div class="col-md-3 text-center">
                                <h3 id="down-stocks">--</h3>
                                <p>下跌股票</p>
                            </div>
                            <div class="col-md-3 text-center">
                                <h3 id="market-sentiment">--</h3>
                                <p>市场情绪</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mb-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0">股票列表</h5>
                        <div class="input-group" style="width: 300px;">
                            <input type="text" id="searchInput" class="form-control" placeholder="搜索股票代码或名称...">
                            <button class="btn btn-outline-secondary" type="button" id="searchBtn">
                                <i class="bi bi-search"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover" id="stockTable">
                                <thead>
                                    <tr>
                                        <th class="sortable" data-field="code">代码</th>
                                        <th class="sortable" data-field="name">名称</th>
                                        <th class="sortable" data-field="industry">行业</th>
                                        <th class="sortable" data-field="price">价格</th>
                                        <th class="sortable" data-field="change_percent">涨跌幅</th>
                                        <th class="sortable" data-field="volume">成交量</th>
                                        <th class="sortable" data-field="market_cap">市值</th>
                                        <th class="sortable" data-field="heat_score">热度</th>
                                        <th class="sortable" data-field="sentiment">情绪</th>
                                    </tr>
                                </thead>
                                <tbody id="stockTableBody">
                                    <tr>
                                        <td colspan="9" class="text-center">
                                            <div class="spinner-border text-primary" role="status">
                                                <span class="visually-hidden">加载中...</span>
                                            </div>
                                            <p class="mt-2">正在加载数据，请稍候...</p>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h5 class="card-title mb-0">行业分布</h5>
                    </div>
                    <div class="card-body">
                        <div id="industryChart" style="height: 400px;"></div>
                    </div>
                </div>
            </div>
            <div class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h5 class="card-title mb-0">涨跌分布</h5>
                    </div>
                    <div class="card-body">
                        <div id="changeDistributionChart" style="height: 400px;"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 筛选模态框 -->
        <div class="modal fade" id="filterModal" tabindex="-1" aria-labelledby="filterModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="filterModalLabel">筛选条件</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="industryFilter" class="form-label">行业</label>
                            <select class="form-select" id="industryFilter">
                                <option value="">全部行业</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="changeFilter" class="form-label">涨跌幅</label>
                            <select class="form-select" id="changeFilter">
                                <option value="">全部</option>
                                <option value="up">上涨</option>
                                <option value="down">下跌</option>
                                <option value="up5">上涨超过5%</option>
                                <option value="down5">下跌超过5%</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="marketCapFilter" class="form-label">市值范围</label>
                            <select class="form-select" id="marketCapFilter">
                                <option value="">全部</option>
                                <option value="large">大盘股 (>1000亿)</option>
                                <option value="medium">中盘股 (100亿-1000亿)</option>
                                <option value="small">小盘股 (<100亿)</option>
                            </select>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                        <button type="button" class="btn btn-primary" id="applyFilterBtn">应用筛选</button>
                    </div>
                </div>
            </div>
        </div>
    `;
}