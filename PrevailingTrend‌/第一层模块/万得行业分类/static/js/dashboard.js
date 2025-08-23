// 万得行业分类仪表盘JavaScript
console.log('仪表盘JavaScript开始加载...');

// 全局变量
let currentLevel = 0;
let currentKeyword = '';
let currentPageNum = 1;
let pageSize = 10;
let totalRecords = 0;

// 数据缓存
let statsCache = null;
let industriesCache = null;
let lastStatsUpdate = 0;
let lastIndustriesUpdate = 0;
const CACHE_DURATION = 30000; // 30秒缓存

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM加载完成，开始初始化...');
    init();
});

// 初始化函数
function init() {
    console.log('开始初始化仪表盘...');
    
    // 绑定事件
    bindEvents();
    
    // 默认显示仪表盘页面，但不立即加载数据
    showPage('dashboard-overview');
    
    // 延迟加载数据，提高页面响应速度
    setTimeout(() => {
        loadStats();
        loadIndustries();
    }, 100);
    
    // 初始化图表
    setTimeout(initCharts, 800);
    
    console.log('仪表盘初始化完成');
}

// 绑定事件
function bindEvents() {
    console.log('绑定事件...');
    
    // 侧边栏切换
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            console.log('切换侧边栏');
            const sidebar = document.getElementById('sidebar');
            if (sidebar) {
                sidebar.classList.toggle('show');
            }
        });
    }
    
    // 全局搜索
    const globalSearch = document.getElementById('globalSearch');
    if (globalSearch) {
        globalSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                console.log('执行搜索:', this.value);
                searchIndustries();
            }
        });
    }
    
    // 导航菜单
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            console.log('点击导航:', href);
            handleNavigation(href, this);
        });
    });
}

// 处理导航
function handleNavigation(href, clickedElement) {
    console.log('处理导航:', href);
    
    // 移除所有活动状态
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // 添加当前活动状态
    clickedElement.classList.add('active');
    
    // 根据href切换内容
    switch(href) {
        case '#dashboard':
            showDashboard();
            break;
        case '#industries':
            showIndustries();
            break;
        case '#stocks':
            showStockMapping();
            break;
        case '#analytics':
            showDataAnalysis();
            break;
        case '#settings':
            showSystemSettings();
            break;
    }
}

// 页面管理
let currentActivePage = 'dashboard-overview';

// 显示指定页面
function showPage(pageId) {
    console.log('切换到页面:', pageId);
    
    // 隐藏所有页面
    const allPages = document.querySelectorAll('.page-content');
    allPages.forEach(page => {
        page.classList.remove('active');
    });
    
    // 显示目标页面
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
        currentActivePage = pageId;
        
        // 根据页面加载相应数据
        switch(pageId) {
            case 'dashboard-overview':
                updatePageTitle('仪表盘概览');
                // 避免重复加载数据
                if (!document.getElementById('total-industries').textContent || document.getElementById('total-industries').textContent === '-') {
                    loadStats();
                    loadIndustries();
                }
                break;
            case 'industries-management':
                updatePageTitle('行业管理');
                loadManagementStats();
                // 避免重复加载数据
                if (!document.getElementById('management-total-industries').textContent || document.getElementById('management-total-industries').textContent === '-') {
                    loadIndustries();
                }
                break;
            case 'stock-mapping':
                updatePageTitle('股票映射管理');
                loadStockMappingStats();
                break;
            case 'data-analysis':
                updatePageTitle('数据分析');
                loadAnalysisStats();
                break;
            case 'system-settings':
                updatePageTitle('系统设置');
                loadSystemStats();
                break;
        }
    }
}

// 显示仪表盘
function showDashboard() {
    showPage('dashboard-overview');
}

// 显示行业管理
function showIndustries() {
    showPage('industries-management');
}

// 显示股票映射
function showStockMapping() {
    showPage('stock-mapping');
}

// 显示数据分析
function showDataAnalysis() {
    showPage('data-analysis');
}

// 显示系统设置
function showSystemSettings() {
    showPage('system-settings');
}

// 显示股票映射
function showStocks() {
    console.log('显示股票映射');
    updatePageTitle('股票映射');
    showMessage('股票映射功能开发中...');
}

// 显示数据分析
function showAnalytics() {
    console.log('显示数据分析');
    updatePageTitle('数据分析');
    showMessage('数据分析功能开发中...');
}

// 显示系统设置
function showSettings() {
    console.log('显示系统设置');
    updatePageTitle('系统设置');
    showMessage('系统设置功能开发中...');
}

// 更新页面标题
function updatePageTitle(title) {
    const titleElement = document.querySelector('.page-title');
    if (titleElement) {
        titleElement.textContent = title;
    }
}

// 显示消息
function showMessage(message) {
    const tableBody = document.getElementById('industriesTableBody');
    if (tableBody) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-info">
                    <i class="fas fa-info-circle"></i> ${message}
                </td>
            </tr>
        `;
    }
}

// 加载统计数据
function loadStats() {
    console.log('加载统计数据...');
    
    // 检查缓存
    const now = Date.now();
    if (statsCache && (now - lastStatsUpdate) < CACHE_DURATION) {
        console.log('使用缓存的统计数据');
        updateStats(statsCache);
        return;
    }
    
    fetch('/api/stats')
        .then(response => {
            console.log('统计数据响应状态:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('统计数据:', data);
            if (data.success) {
                // 更新缓存
                statsCache = data.data;
                lastStatsUpdate = now;
                updateStats(data.data);
            } else {
                console.error('获取统计数据失败:', data.message);
            }
        })
        .catch(error => {
            console.error('加载统计失败:', error);
        });
}

// 更新统计数据
function updateStats(stats) {
    console.log('更新统计数据:', stats);
    
    const elements = {
        'total-industries': stats.total_industries || 0,
        'total-stocks': stats.total_stocks || 0,
        'level-1-count': stats.level_1_count || 0,
        'level-2-count': stats.level_2_count || 0
    };
    
    Object.keys(elements).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            // 添加动画效果
            element.style.opacity = '0.5';
            setTimeout(() => {
                element.textContent = elements[id];
                element.style.opacity = '1';
            }, 100);
        }
    });
}

// 加载行业管理页面统计数据
function loadManagementStats() {
    console.log('加载行业管理统计数据...');
    
    // 检查缓存
    const now = Date.now();
    if (statsCache && (now - lastStatsUpdate) < CACHE_DURATION) {
        console.log('使用缓存的统计数据');
        updateManagementStats(statsCache);
        return;
    }
    
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 更新缓存
                statsCache = data.data;
                lastStatsUpdate = now;
                updateManagementStats(data.data);
            }
        })
        .catch(error => {
            console.error('加载管理统计数据失败:', error);
        });
}

// 更新行业管理页面统计数据
function updateManagementStats(stats) {
    console.log('更新管理统计数据:', stats);
    
    const elements = {
        'management-total-industries': stats.total_industries || 0,
        'management-level-1-count': stats.level_1_count || 0,
        'management-level-2-count': stats.level_2_count || 0,
        'management-total-stocks': stats.total_stocks || 0
    };
    
    Object.keys(elements).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.style.opacity = '0.5';
            setTimeout(() => {
                element.textContent = elements[id];
                element.style.opacity = '1';
            }, 100);
        }
    });
    
    // 更新最近更新时间
    const lastUpdateElement = document.getElementById('last-update');
    if (lastUpdateElement) {
        const now = new Date();
        lastUpdateElement.textContent = now.toLocaleString('zh-CN');
    }
}

// 加载行业列表
function loadIndustries() {
    console.log('加载行业列表...');
    
    const tableBody = document.getElementById('industriesTableBody');
    if (!tableBody) {
        console.error('找不到表格体元素');
        return;
    }
    
    // 检查缓存
    const cacheKey = `${currentLevel}_${currentKeyword}_${currentPageNum}`;
    const now = Date.now();
    if (industriesCache && industriesCache.key === cacheKey && (now - lastIndustriesUpdate) < CACHE_DURATION) {
        console.log('使用缓存的行业列表数据');
        displayIndustries(industriesCache.data);
        return;
    }
    
    // 显示加载状态
    tableBody.innerHTML = `
        <tr>
            <td colspan="6" class="text-center">
                <div class="loading-spinner">
                    <i class="fas fa-spinner fa-spin"></i>
                    <span>加载中...</span>
                </div>
            </td>
        </tr>
    `;
    
    // 构建请求URL
    let url = `/api/industries?page=${currentPageNum}&page_size=${pageSize}`;
    
    if (currentLevel > 0) {
        url += `&level=${currentLevel}`;
    }
    if (currentKeyword) {
        url += `&keyword=${encodeURIComponent(currentKeyword)}`;
    }
    
    console.log('请求URL:', url);
    
    fetch(url)
        .then(response => {
            console.log('行业列表响应状态:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('行业列表数据:', data);
            if (data.success) {
                // 更新缓存
                industriesCache = {
                    key: cacheKey,
                    data: data.data
                };
                lastIndustriesUpdate = now;
                displayIndustries(data.data);
            } else {
                showError(data.message);
            }
        })
        .catch(error => {
            console.error('加载行业列表失败:', error);
            showError(error.message);
        });
}

// 显示错误信息
function showError(message) {
    const tableBody = document.getElementById('industriesTableBody');
    if (tableBody) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-danger">
                    <i class="fas fa-exclamation-triangle"></i> 加载失败: ${message}
                </td>
            </tr>
        `;
    }
}

// 显示行业列表
function displayIndustries(data) {
    console.log('显示行业列表:', data);
    
    const tableBody = document.getElementById('industriesTableBody');
    const industries = data.industries || [];
    totalRecords = data.total || 0;
    
    if (industries.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted">
                    <i class="fas fa-info-circle"></i> 暂无数据
                </td>
            </tr>
        `;
        return;
    }
    
    let html = '';
    industries.forEach(industry => {
        const levelText = industry.level === 1 ? '一级' : '二级';
        const levelBadge = industry.level === 1 ? 'bg-primary' : 'bg-success';
        
        html += `
            <tr>
                <td><strong>${industry.industry_code}</strong></td>
                <td>${industry.industry_name}</td>
                <td><span class="badge ${levelBadge}">${levelText}</span></td>
                <td>${industry.stock_count || 0}</td>
                <td><span class="badge bg-success">${industry.status || '正常'}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="showIndustryDetail('${industry.industry_code}')">
                        <i class="fas fa-eye"></i> 详情
                    </button>
                </td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = html;
    updatePagination(data.total_pages || 1);
    updatePaginationInfo();
}

// 更新分页信息
function updatePaginationInfo() {
    const startRecord = (currentPageNum - 1) * pageSize + 1;
    const endRecord = Math.min(currentPageNum * pageSize, totalRecords);
    
    const startElement = document.getElementById('startRecord');
    const endElement = document.getElementById('endRecord');
    const totalElement = document.getElementById('totalRecords');
    
    if (startElement) startElement.textContent = startRecord;
    if (endElement) endElement.textContent = endRecord;
    if (totalElement) totalElement.textContent = totalRecords;
}

// 更新分页控件
function updatePagination(totalPages) {
    const pagination = document.getElementById('pagination');
    if (!pagination) return;
    
    let html = '';
    
    // 上一页
    html += `
        <li class="page-item ${currentPageNum === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPageNum - 1}); return false;">
                <i class="fas fa-chevron-left"></i>
            </a>
        </li>
    `;
    
    // 页码 - 简化版本，不显示省略号
    const startPage = Math.max(1, currentPageNum - 1);
    const endPage = Math.min(totalPages, currentPageNum + 1);
    
    for (let i = startPage; i <= endPage; i++) {
        html += `
            <li class="page-item ${i === currentPageNum ? 'active' : ''}">
                <a class="page-link" href="#" onclick="changePage(${i}); return false;">${i}</a>
            </li>
        `;
    }
    
    // 下一页
    html += `
        <li class="page-item ${currentPageNum === totalPages ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPageNum + 1}); return false;">
                <i class="fas fa-chevron-right"></i>
            </a>
        </li>
    `;
    
    pagination.innerHTML = html;
}

// 切换分页
function changePage(page) {
    console.log('切换到第', page, '页');
    currentPageNum = page;
    loadIndustries();
}

// 搜索行业
function searchIndustries() {
    console.log('搜索行业');
    const searchInput = document.getElementById('globalSearch');
    currentKeyword = searchInput ? searchInput.value.trim() : '';
    currentPageNum = 1;
    console.log('搜索关键词:', currentKeyword);
    loadIndustries();
}

// 按层级筛选
function filterByLevel(level) {
    console.log('筛选层级:', level);
    currentLevel = level;
    currentPageNum = 1;
    loadIndustries();
}

// 刷新数据
function refreshData() {
    console.log('刷新数据');
    // 清除缓存
    statsCache = null;
    industriesCache = null;
    lastStatsUpdate = 0;
    lastIndustriesUpdate = 0;
    loadStats();
    loadIndustries();
}

// 显示行业详情
function showIndustryDetail(industryCode) {
    console.log('显示行业详情:', industryCode);
    
    const modal = new bootstrap.Modal(document.getElementById('industryModal'));
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    modalTitle.textContent = '行业详情 - ' + industryCode;
    modalBody.innerHTML = `
        <div class="loading-spinner">
            <i class="fas fa-spinner fa-spin"></i>
            <span>加载中...</span>
        </div>
    `;
    modal.show();
    
    fetch(`/api/industries/${industryCode}`)
        .then(response => response.json())
        .then(data => {
            console.log('行业详情数据:', data);
            if (data.success) {
                displayIndustryDetail(data.data);
            } else {
                modalBody.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i> 加载失败: ${data.message}
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('加载行业详情失败:', error);
            modalBody.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i> 加载失败: ${error.message}
                </div>
            `;
        });
}

// 显示行业详情内容
function displayIndustryDetail(data) {
    const modalBody = document.getElementById('modalBody');
    const industry = data.industry;
    const stocks = data.stocks || [];
    
    let html = `
        <div class="row">
            <div class="col-md-6">
                <h6 class="text-muted mb-3">行业信息</h6>
                <table class="table table-sm">
                    <tr>
                        <td class="fw-bold">行业代码</td>
                        <td>${industry.industry_code}</td>
                    </tr>
                    <tr>
                        <td class="fw-bold">行业名称</td>
                        <td>${industry.industry_name}</td>
                    </tr>
                    <tr>
                        <td class="fw-bold">层级</td>
                        <td>${industry.level === 1 ? '一级' : '二级'}</td>
                    </tr>
                    <tr>
                        <td class="fw-bold">状态</td>
                        <td><span class="badge bg-success">${industry.status || '正常'}</span></td>
                    </tr>
                </table>
            </div>
            <div class="col-md-6">
                <h6 class="text-muted mb-3">统计信息</h6>
                <div class="text-center">
                    <h3 class="text-primary mb-2">${stocks.length}</h3>
                    <p class="text-muted">关联股票数量</p>
                </div>
            </div>
        </div>
    `;
    
    if (stocks.length > 0) {
        html += `
            <hr>
            <h6 class="text-muted mb-3">关联股票 (${stocks.length}只)</h6>
            <div class="table-responsive">
                <table class="table table-sm table-striped">
                    <thead>
                        <tr>
                            <th>股票代码</th>
                            <th>股票名称</th>
                            <th>映射状态</th>
                            <th>置信度</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        stocks.forEach(stock => {
            html += `
                <tr>
                    <td>${stock.stock_code}</td>
                    <td>${stock.stock_name}</td>
                    <td><span class="badge bg-success">${stock.mapping_status || '正常'}</span></td>
                    <td>${stock.confidence || 100}%</td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
    } else {
        html += '<hr><p class="text-muted"><i class="fas fa-info-circle"></i> 暂无关联股票</p>';
    }
    
    modalBody.innerHTML = html;
}

// 行业管理功能函数
function showAddIndustryModal() {
    alert('添加行业功能开发中...');
}

function exportIndustries() {
    alert('导出数据功能开发中...');
}

function importIndustries() {
    alert('导入数据功能开发中...');
}

// 股票映射功能
let currentStockFilter = 'all';
let currentStockPage = 1;
let stockPageSize = 20;
let stockTotalRecords = 0;
let stockSearchKeyword = '';

function loadStockMappingStats() {
    console.log('加载股票映射统计数据...');
    
    // 加载股票统计数据
    fetch('/api/stocks/stats')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateStockMappingStats(data.data);
            } else {
                // 使用模拟数据
                const stats = {
                    total_mapped: 1250,
                    unmapped: 850,
                    sync_status: '已同步',
                    last_update: new Date().toLocaleString('zh-CN')
                };
                updateStockMappingStats(stats);
            }
        })
        .catch(error => {
            console.error('加载股票统计数据失败:', error);
            // 使用模拟数据
            const stats = {
                total_mapped: 1250,
                unmapped: 850,
                sync_status: '已同步',
                last_update: new Date().toLocaleString('zh-CN')
            };
            updateStockMappingStats(stats);
        });
    
    // 加载股票列表
    loadStocksList();
}

function updateStockMappingStats(stats) {
    const elements = {
        'stock-total-mapped': stats.total_mapped || 0,
        'stock-unmapped': stats.unmapped || 0,
        'stock-sync-status': stats.sync_status || '未知',
        'stock-last-update': stats.last_update || '-'
    };
    
    Object.keys(elements).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = elements[id];
        }
    });
}

// 加载股票列表
function loadStocksList() {
    console.log('加载股票列表...');
    
    const tableBody = document.getElementById('stocksTableBody');
    if (!tableBody) {
        console.error('找不到股票表格体元素');
        return;
    }
    
    // 显示加载状态
    tableBody.innerHTML = `
        <tr>
            <td colspan="7" class="text-center">
                <div class="loading-spinner">
                    <i class="fas fa-spinner fa-spin"></i>
                    <span>加载中...</span>
                </div>
            </td>
        </tr>
    `;
    
    // 构建请求URL
    let url = `/api/stocks?page=${currentStockPage}&page_size=${stockPageSize}`;
    
    if (currentStockFilter !== 'all') {
        url += `&filter=${currentStockFilter}`;
    }
    if (stockSearchKeyword) {
        url += `&keyword=${encodeURIComponent(stockSearchKeyword)}`;
    }
    
    console.log('请求股票列表URL:', url);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('股票列表数据:', data);
            if (data.success) {
                displayStocksList(data.data);
            } else {
                // 使用模拟数据
                displayStocksList(generateMockStocksData());
            }
        })
        .catch(error => {
            console.error('加载股票列表失败:', error);
            // 使用模拟数据
            displayStocksList(generateMockStocksData());
        });
}

// 生成模拟股票数据
function generateMockStocksData() {
    const stocks = [];
    const aStocks = [
        { code: '000001', name: '平安银行', market: 'A股', industry: '银行', mapped: true },
        { code: '000002', name: '万科A', market: 'A股', industry: '房地产', mapped: true },
        { code: '000858', name: '五粮液', market: 'A股', industry: '食品饮料', mapped: true },
        { code: '002415', name: '海康威视', market: 'A股', industry: '电子', mapped: false },
        { code: '600036', name: '招商银行', market: 'A股', industry: '银行', mapped: true },
        { code: '600519', name: '贵州茅台', market: 'A股', industry: '食品饮料', mapped: true },
        { code: '600887', name: '伊利股份', market: 'A股', industry: '食品饮料', mapped: false },
        { code: '000725', name: '京东方A', market: 'A股', industry: '电子', mapped: true },
        { code: '002594', name: '比亚迪', market: 'A股', industry: '汽车', mapped: true },
        { code: '300059', name: '东方财富', market: 'A股', industry: '金融', mapped: false }
    ];
    
    const hkStocks = [
        { code: '00700', name: '腾讯控股', market: '港股通', industry: '互联网', mapped: true },
        { code: '00941', name: '中国移动', market: '港股通', industry: '通信', mapped: true },
        { code: '02318', name: '中国平安', market: '港股通', industry: '保险', mapped: true },
        { code: '03988', name: '中国银行', market: '港股通', industry: '银行', mapped: false },
        { code: '01398', name: '工商银行', market: '港股通', industry: '银行', mapped: true },
        { code: '00388', name: '香港交易所', market: '港股通', industry: '金融', mapped: true },
        { code: '02020', name: '安踏体育', market: '港股通', industry: '服装', mapped: false },
        { code: '01024', name: '快手-W', market: '港股通', industry: '互联网', mapped: true },
        { code: '03690', name: '美团-W', market: '港股通', industry: '互联网', mapped: true },
        { code: '09988', name: '阿里巴巴-SW', market: '港股通', industry: '互联网', mapped: true }
    ];
    
    // 根据筛选条件返回数据
    if (currentStockFilter === 'a') {
        stocks.push(...aStocks);
    } else if (currentStockFilter === 'hk') {
        stocks.push(...hkStocks);
    } else {
        stocks.push(...aStocks, ...hkStocks);
    }
    
    // 根据映射状态筛选
    if (currentStockFilter === 'mapped') {
        return stocks.filter(stock => stock.mapped);
    } else if (currentStockFilter === 'unmapped') {
        return stocks.filter(stock => !stock.mapped);
    }
    
    return {
        stocks: stocks,
        total: stocks.length,
        page: currentStockPage,
        page_size: stockPageSize
    };
}

// 显示股票列表
function displayStocksList(data) {
    console.log('显示股票列表:', data);
    
    const tableBody = document.getElementById('stocksTableBody');
    const stocks = data.stocks || [];
    stockTotalRecords = data.total || stocks.length;
    
    if (stocks.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-muted">
                    <i class="fas fa-info-circle"></i> 暂无数据
                </td>
            </tr>
        `;
        updateStockPaginationInfo();
        return;
    }
    
    let html = '';
    stocks.forEach(stock => {
        const marketClass = stock.market === 'A股' ? 'stock-market-a' : 'stock-market-hk';
        const mappingClass = stock.mapped ? 'mapping-status-mapped' : 'mapping-status-unmapped';
        const mappingText = stock.mapped ? '已映射' : '未映射';
        
        html += `
            <tr>
                <td><strong>${stock.code}</strong></td>
                <td>${stock.name}</td>
                <td><span class="badge ${marketClass}">${stock.market}</span></td>
                <td>${stock.industry || '-'}</td>
                <td><span class="badge ${mappingClass}">${mappingText}</span></td>
                <td>${new Date().toLocaleDateString('zh-CN')}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editStockMapping('${stock.code}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-info" onclick="viewStockDetail('${stock.code}')">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = html;
    updateStockPaginationInfo();
    updateStockPagination();
}

// 更新股票分页信息
function updateStockPaginationInfo() {
    const startRecord = (currentStockPage - 1) * stockPageSize + 1;
    const endRecord = Math.min(currentStockPage * stockPageSize, stockTotalRecords);
    
    const startElement = document.getElementById('stockStartRecord');
    const endElement = document.getElementById('stockEndRecord');
    const totalElement = document.getElementById('stockTotalRecords');
    
    if (startElement) startElement.textContent = startRecord;
    if (endElement) endElement.textContent = endRecord;
    if (totalElement) totalElement.textContent = stockTotalRecords;
}

// 更新股票分页控件
function updateStockPagination() {
    const pagination = document.getElementById('stockPagination');
    if (!pagination) return;
    
    const totalPages = Math.ceil(stockTotalRecords / stockPageSize);
    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }
    
    let html = '';
    
    // 上一页
    html += `
        <li class="page-item ${currentStockPage === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changeStockPage(${currentStockPage - 1}); return false;">
                <i class="fas fa-chevron-left"></i>
            </a>
        </li>
    `;
    
    // 页码
    const startPage = Math.max(1, currentStockPage - 1);
    const endPage = Math.min(totalPages, currentStockPage + 1);
    
    for (let i = startPage; i <= endPage; i++) {
        html += `
            <li class="page-item ${i === currentStockPage ? 'active' : ''}">
                <a class="page-link" href="#" onclick="changeStockPage(${i}); return false;">${i}</a>
            </li>
        `;
    }
    
    // 下一页
    html += `
        <li class="page-item ${currentStockPage === totalPages ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changeStockPage(${currentStockPage + 1}); return false;">
                <i class="fas fa-chevron-right"></i>
            </a>
        </li>
    `;
    
    pagination.innerHTML = html;
}

// 切换股票页面
function changeStockPage(page) {
    console.log('切换到股票第', page, '页');
    currentStockPage = page;
    loadStocksList();
}

// 筛选股票
function filterStocks(filter) {
    console.log('筛选股票:', filter);
    currentStockFilter = filter;
    currentStockPage = 1;
    
    // 更新按钮状态
    document.querySelectorAll('.filter-controls .btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    loadStocksList();
}

// 搜索股票
function searchStocks() {
    const searchInput = document.getElementById('stockSearch');
    stockSearchKeyword = searchInput ? searchInput.value.trim() : '';
    currentStockPage = 1;
    console.log('搜索股票关键词:', stockSearchKeyword);
    loadStocksList();
}

function syncStockMapping() {
    alert('股票映射同步功能开发中...');
}

// 导出股票数据
function exportStockData() {
    alert('导出股票数据功能开发中...');
}

// 编辑股票映射
function editStockMapping(stockCode) {
    alert(`编辑股票映射: ${stockCode} - 功能开发中...`);
}

// 查看股票详情
function viewStockDetail(stockCode) {
    alert(`查看股票详情: ${stockCode} - 功能开发中...`);
}

// 批量导入映射
function importStockMapping() {
    alert('批量导入映射功能开发中...');
}

// 智能映射
function autoMapStocks() {
    alert('智能映射功能开发中...');
}

// 数据分析功能
function loadAnalysisStats() {
    console.log('加载数据分析统计数据...');
    
    // 模拟数据
    const stats = {
        total_reports: 15,
        analysis_period: '30天',
        trend_indicator: '上升',
        generated_reports: 8
    };
    
    updateAnalysisStats(stats);
}

function updateAnalysisStats(stats) {
    const elements = {
        'analysis-total': stats.total_reports || 0,
        'analysis-period': stats.analysis_period || '-',
        'analysis-trend': stats.trend_indicator || '-',
        'analysis-reports': stats.generated_reports || 0
    };
    
    Object.keys(elements).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = elements[id];
        }
    });
}

// 系统设置功能
function loadSystemStats() {
    console.log('加载系统设置数据...');
    // 系统设置页面不需要统计数据，主要是配置项
}

// 初始化图表
function initCharts() {
    console.log('初始化图表...');
    
    // 趋势图表
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx && typeof Chart !== 'undefined') {
        try {
            new Chart(trendCtx, {
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
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
            console.log('趋势图表初始化成功');
        } catch (error) {
            console.error('趋势图表初始化失败:', error);
        }
    }
    
    // 饼图
    const pieCtx = document.getElementById('pieChart');
    if (pieCtx && typeof Chart !== 'undefined') {
        try {
            new Chart(pieCtx, {
                type: 'doughnut',
                data: {
                    labels: ['一级行业', '二级行业'],
                    datasets: [{
                        data: [30, 150],
                        backgroundColor: ['#4f46e5', '#10b981'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
            console.log('饼图初始化成功');
        } catch (error) {
            console.error('饼图初始化失败:', error);
        }
    }
}

console.log('仪表盘JavaScript加载完成');
