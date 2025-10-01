// 国内热点数据模块 - 自包含实现
function loadEnhancedDomesticHotspotData() {
    const contentArea = document.querySelector(".content-area");
    if (!contentArea) return;
    
    // 显示加载状态
    contentArea.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-3">正在加载国内上市公司数据...</p>
        </div>
    `;

    // 从后端API获取真实数据
    function fetchRealData() {
        return fetch('/api/listed-companies?page=0&size=10000&sortBy=stockCode&sortDir=asc')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    return data.data.content;
                } else {
                    console.error('获取数据失败:', data.error);
                    // 如果API调用失败，返回空数组
                    return [];
                }
            })
            .catch(error => {
                console.error('获取数据时发生错误:', error);
                // 网络错误时，返回空数组
                return [];
            });
    }
    
    // 加载统计数据
    function fetchStatistics() {
        return fetch('/api/listed-companies/stats')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    return data.data;
                } else {
                    console.error('获取统计数据失败:', data.error);
                    return null;
                }
            })
            .catch(error => {
                console.error('获取统计数据时发生错误:', error);
                return null;
            });
    }

    // 同时获取数据和统计信息
    Promise.all([fetchRealData(), fetchStatistics()])
        .then(([companiesData, statisticsData]) => {
            // 存储数据到全局变量，便于分页操作
            window.marketData = companiesData;
            window.statisticsData = statisticsData;
            
            // 使用Web Worker处理大量数据
            if (window.Worker) {
                // 创建内联Worker用于数据处理
                const workerBlob = new Blob([`
                    self.onmessage = function(e) {
                        const { companies, statistics } = e.data;
                        
                        // 处理数据（转换数值类型）
                        const processedCompanies = companies.map(company => {
                            // 确保所有数字字段转换为适当的类型
                            return {
                                ...company,
                                latestPrice: company.latestPrice ? (typeof company.latestPrice === 'string' ? company.latestPrice : company.latestPrice.toString()) : '0.00',
                                priceChangeRate: company.priceChangeRate ? (typeof company.priceChangeRate === 'string' ? company.priceChangeRate : company.priceChangeRate.toString()) : '0.00',
                                totalMarketValue: company.totalMarketValue ? (typeof company.totalMarketValue === 'string' ? company.totalMarketValue : company.totalMarketValue.toString()) : '0.00',
                                peRatio: company.peRatio ? (typeof company.peRatio === 'string' ? company.peRatio : company.peRatio.toString()) : '0.00',
                                pbRatio: company.pbRatio ? (typeof company.pbRatio === 'string' ? company.pbRatio : company.pbRatio.toString()) : '0.00'
                            };
                        });
                        
                        // 返回处理后的数据
                        self.postMessage({ companies: processedCompanies, statistics });
                    };
                `], { type: 'application/javascript' });
                
                const workerUrl = URL.createObjectURL(workerBlob);
                const worker = new Worker(workerUrl);
                
                worker.onmessage = function(e) {
                    const { companies, statistics } = e.data;
                    // 使用处理后的数据渲染页面
                    renderData(companies, statistics, 1); // 默认显示第1页
                    
                    // 清理Worker
                    worker.terminate();
                    URL.revokeObjectURL(workerUrl);
                };
                
                worker.onerror = function(error) {
                    console.error('Web Worker 处理错误:', error);
                    // 降级处理：直接使用原始数据
                    renderData(companiesData, statisticsData, 1);
                    worker.terminate();
                    URL.revokeObjectURL(workerUrl);
                };
                
                // 发送数据给Worker处理
                worker.postMessage({ companies: companiesData, statistics: statisticsData });
            } else {
                // 浏览器不支持Worker，直接使用原始数据
                renderData(companiesData, statisticsData, 1);
            }
        })
        .catch(error => {
            console.error('数据加载失败:', error);
            contentArea.innerHTML = `
                <div class="text-center py-5">
                    <div class="alert alert-danger" role="alert">
                        数据加载失败，请稍后重试
                    </div>
                    <button class="btn btn-primary mt-3" onclick="loadEnhancedDomesticHotspotData()">
                        重新加载
                    </button>
                </div>
            `;
        });
}

// 刷新上市公司数据
function refreshListedCompanyData() {
    const contentArea = document.querySelector(".content-area");
    if (!contentArea) return;
    
    // 显示加载状态
    contentArea.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">刷新中...</span>
            </div>
            <p class="mt-3">正在刷新国内上市公司数据...</p>
        </div>
    `;
    
    // 调用后端刷新数据接口
    fetch('/api/listed-companies/refresh')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 刷新成功后重新加载数据
                loadEnhancedDomesticHotspotData();
            } else {
                alert('数据刷新失败: ' + (data.error || '未知错误'));
                loadEnhancedDomesticHotspotData();
            }
        })
        .catch(error => {
            console.error('刷新数据时发生错误:', error);
            alert('数据刷新失败，请稍后重试');
            loadEnhancedDomesticHotspotData();
        });
}

// 分页配置
const PAGE_SIZE = 50; // 每页显示的公司数量，增加到50条以显示更多数据

// 当前排序状态
let currentSortField = 'totalMarketValue'; // 默认按市值排序
let currentSortDirection = 'desc'; // 默认降序

// 排序函数 - 优化以处理大量数据
function sortData(data, field, direction) {
    // 创建索引数组而不是复制整个数据集
    const indices = Array.from({ length: data.length }, (_, i) => i);
    
    // 排序索引
    indices.sort((a, b) => {
        let valueA = data[a][field];
        let valueB = data[b][field];
        
        // 数值型字段特殊处理
        if (field === 'latestPrice' || field === 'totalMarketValue' || field === 'priceChangeRate' || 
            field === 'peRatio' || field === 'pbRatio') {
            valueA = parseFloat(valueA) || 0;
            valueB = parseFloat(valueB) || 0;
        } else if (field === 'stockCode') {
            // 股票代码排序 - 确保按数字大小排序而不是字符串
            valueA = valueA.toString();
            valueB = valueB.toString();
        }
        
        if (direction === 'asc') {
            return valueA > valueB ? 1 : valueA < valueB ? -1 : 0;
        } else {
            return valueA < valueB ? 1 : valueA > valueB ? -1 : 0;
        }
    });
    
    // 使用索引创建排序后的数据视图
    return indices.map(i => data[i]);
}

// 切换排序
function toggleSort(field) {
    if (currentSortField === field) {
        // 切换排序方向
        currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        // 新字段默认降序
        currentSortField = field;
        currentSortDirection = 'desc';
    }
    
    // 重新渲染数据 - 尝试保持在当前页
    if (window.marketData) {
        const currentPageToKeep = window.currentPage || 1;
        renderData(window.marketData, window.statisticsData, currentPageToKeep);
    }
}

// 渲染逻辑（表格式，带分页和排序）- 优化以处理大量数据
function renderData(data, statisticsData, currentPage = 1) {
    const contentArea = document.querySelector(".content-area");
    if (!contentArea) return;
    
    // 显示加载中状态
    const loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'text-center py-3';
    loadingIndicator.innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">排序中...</span>
        </div>
        <p class="mt-2">正在处理数据...</p>
    `;
    contentArea.innerHTML = '';
    contentArea.appendChild(loadingIndicator);
    
    // 使用setTimeout让浏览器有机会渲染加载指示器
    setTimeout(() => {
        if (!data || data.length === 0) {
            contentArea.innerHTML = `
                <div class="text-center py-10">
                    <p class="text-muted">暂无数据</p>
                    <button class="btn btn-primary mt-3" onclick="refreshListedCompanyData()">
                        刷新数据
                    </button>
                </div>
            `;
            return;
        }
        
        // 按当前排序条件排序
        const sortedData = sortData(data, currentSortField, currentSortDirection);
        
        // 计算分页
        const totalPages = Math.ceil(sortedData.length / PAGE_SIZE);
        currentPage = Math.max(1, Math.min(currentPage, totalPages)); // 确保页码在有效范围内
        window.currentPage = currentPage;
        
        // 获取当前页的数据
        const startIndex = (currentPage - 1) * PAGE_SIZE;
        const endIndex = Math.min(startIndex + PAGE_SIZE, sortedData.length);
        const currentPageData = sortedData.slice(startIndex, endIndex);
        
        // 格式化数字显示
        const formatNumber = (num, decimals = 2) => {
            if (!num) return '-';
            return parseFloat(num).toFixed(decimals);
        };
        
        // 根据股票代码获取市场名称
        const getMarketName = (stockCode) => {
            if (!stockCode) return '-';
            
            if (stockCode.startsWith('6')) {
                return '沪市';
            } else if (stockCode.startsWith('0')) {
                return '深市';
            } else if (stockCode.startsWith('3')) {
                return '创业板';
            } else if (stockCode.startsWith('688')) {
                return '科创板';
            }
            return '其他';
        };
        
        // 构建统计信息卡片
        let statsHtml = '';
        if (statisticsData) {
            statsHtml = `
            <div class="row mb-4">
                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card bg-light border-primary">
                        <div class="card-body">
                            <h5 class="card-title text-primary">上市公司总数</h5>
                            <p class="card-text display-4">${statisticsData.totalCount || 0}</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card bg-light border-success">
                        <div class="card-body">
                            <h5 class="card-title text-success">活跃公司</h5>
                            <p class="card-text display-4">${statisticsData.activeCount || 0}</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card bg-light border-warning">
                        <div class="card-body">
                            <h5 class="card-title text-warning">停牌公司</h5>
                            <p class="card-text display-4">${statisticsData.suspendedCount || 0}</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card bg-light border-info">
                        <div class="card-body">
                            <h5 class="card-title text-info">行业数量</h5>
                            <p class="card-text display-4">${statisticsData.industryCount || 0}</p>
                        </div>
                    </div>
                </div>
            </div>`;
        }
        
        // 构建HTML
        let html = `
            <div class="market-header">
                <h2><i class="bi bi-graph-up"></i> 国内上市公司全景</h2>
                <p class="text-muted">共 ${data.length} 家公司 • 最后更新: ${new Date().toLocaleString()}</p>
                <div class="d-flex flex-wrap justify-content-between align-items-center gap-3 mb-3">
                    ${statsHtml}
                    <div class="d-flex flex-wrap gap-2">
                        <div class="form-inline">
                            <label for="pageSizeSelect" class="me-2">每页显示:</label>
                            <select id="pageSizeSelect" class="form-select form-select-sm" style="width: auto;" onchange="changePageSize(this.value)">
                                <option value="20" ${PAGE_SIZE === 20 ? 'selected' : ''}>20条</option>
                                <option value="50" ${PAGE_SIZE === 50 ? 'selected' : ''}>50条</option>
                                <option value="100" ${PAGE_SIZE === 100 ? 'selected' : ''}>100条</option>
                                <option value="200" ${PAGE_SIZE === 200 ? 'selected' : ''}>200条</option>
                            </select>
                        </div>
                        <button class="btn btn-primary btn-sm" onclick="refreshListedCompanyData()">
                            <i class="bi bi-arrow-repeat"></i> 刷新数据
                        </button>
                        <div class="input-group" style="max-width: 300px;">
                            <input type="text" id="searchInput" class="form-control" placeholder="搜索公司名称或代码..." 
                                   onkeyup="if(event.key === 'Enter') searchCompanies()">
                            <button class="btn btn-outline-secondary" type="button" onclick="searchCompanies()">
                                <i class="bi bi-search"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="table-responsive" style="overflow-x: auto; max-width: 100%;">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th scope="col" class="sortable" onclick="toggleSort('stockCode')">
                                股票代码 ${getSortIcon('stockCode')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('companyName')">
                                公司名称 ${getSortIcon('companyName')}
                            </th>
                            <th scope="col">市场</th>
                            <th scope="col" class="sortable" onclick="toggleSort('industry')">
                                行业 ${getSortIcon('industry')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('latestPrice')">
                                最新价(元) ${getSortIcon('latestPrice')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('priceChangeRate')">
                                涨跌幅(%) ${getSortIcon('priceChangeRate')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('totalMarketValue')">
                                市值(亿元) ${getSortIcon('totalMarketValue')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('peRatio')">
                                PE ${getSortIcon('peRatio')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('pbRatio')">
                                PB ${getSortIcon('pbRatio')}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        // 构建表格行HTML
        currentPageData.forEach(item => {
            // 涨跌样式
            const priceChangeClass = parseFloat(item.priceChangeRate) >= 0 ? 'text-danger' : 'text-success';
            const priceChangeIcon = parseFloat(item.priceChangeRate) >= 0 ? '↑' : '↓';
            
            html += `
                <tr>
                    <td title="${item.stockCode || '-'}">${item.stockCode || '-'}</td>
                    <td title="${item.companyName || '-'}"><strong>${item.companyName || '-'}</strong></td>
                    <td>${getMarketName(item.stockCode)}</td>
                    <td title="${item.industry || '-'}">${item.industry || '-'}</td>
                    <td title="${formatNumber(item.latestPrice)}">${formatNumber(item.latestPrice)}</td>
                    <td class="${priceChangeClass}" title="${formatNumber(item.priceChangeRate)}%">
                        <strong>${priceChangeIcon} ${formatNumber(item.priceChangeRate)}</strong>
                    </td>
                    <td title="${formatNumber(item.totalMarketValue, 2)}">${formatNumber(item.totalMarketValue, 2)}</td>
                    <td title="${formatNumber(item.peRatio, 2)}">${formatNumber(item.peRatio, 2)}</td>
                    <td title="${formatNumber(item.pbRatio, 2)}">${formatNumber(item.pbRatio, 2)}</td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
            </div>
        `;
        
        // 添加分页控件
        html += `
            <nav aria-label="市场数据分页" class="mt-4">
                <ul class="pagination justify-content-center">
                    <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                        <a class="page-link" href="#" onclick="changePage(${currentPage - 1}); return false;">上一页</a>
                    </li>
        `;
        
        // 显示页码
        const maxVisiblePages = 5; // 最多显示的页码数
        let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
        let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
        
        // 调整起始页，确保显示足够的页码
        if (endPage - startPage + 1 < maxVisiblePages) {
            startPage = Math.max(1, endPage - maxVisiblePages + 1);
        }
        
        // 添加第一页链接
        if (startPage > 1) {
            html += `
                <li class="page-item">
                    <a class="page-link" href="#" onclick="changePage(1); return false;">1</a>
                </li>
            `;
            if (startPage > 2) {
                html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
        }
        
        // 添加页码
        for (let i = startPage; i <= endPage; i++) {
            html += `
                <li class="page-item ${i === currentPage ? 'active' : ''}">
                    <a class="page-link" href="#" onclick="changePage(${i}); return false;">${i}</a>
                </li>
            `;
        }
        
        // 添加最后一页链接
        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
            html += `
                <li class="page-item">
                    <a class="page-link" href="#" onclick="changePage(${totalPages}); return false;">${totalPages}</a>
                </li>
            `;
        }
        
        html += `
                    <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                        <a class="page-link" href="#" onclick="changePage(${currentPage + 1}); return false;">下一页</a>
                    </li>
                </ul>
            </nav>
            <div class="text-center text-muted">
                <small>显示 ${startIndex + 1} - ${endIndex} 条，共 ${sortedData.length} 条</small>
            </div>
        `;
        
        // 更新DOM
        contentArea.innerHTML = html;
    }, 10);
}

// 获取排序图标
function getSortIcon(field) {
    if (currentSortField !== field) {
        return '<i class="bi bi-arrow-down-up text-muted"></i>';
    }
    
    return currentSortDirection === 'asc' 
        ? '<i class="bi bi-sort-up-alt"></i>' 
        : '<i class="bi bi-sort-down"></i>';
}

// 切换页面函数
function changePage(pageNumber) {
    if (!window.marketData) return;
    renderData(window.marketData, window.statisticsData, pageNumber);
    // 滚动到页面顶部
    window.scrollTo({top: 0, behavior: 'smooth'});
}

// 更改每页显示数量
function changePageSize(size) {
    window.PAGE_SIZE = parseInt(size);
    if (window.marketData) {
        renderData(window.marketData, window.statisticsData, 1);
    }
}

// 搜索公司
function searchCompanies() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput || !window.marketData) return;
    
    const searchTerm = searchInput.value.trim().toLowerCase();
    
    if (searchTerm === '') {
        // 如果搜索框为空，显示所有数据
        renderData(window.marketData, window.statisticsData, 1);
        return;
    }
    
    // 过滤数据 - 增强搜索功能，同时搜索公司名称、代码和行业
    const filteredData = window.marketData.filter(item => 
        (item.companyName && item.companyName.toLowerCase().includes(searchTerm)) || 
        (item.stockCode && item.stockCode.toLowerCase().includes(searchTerm)) ||
        (item.industry && item.industry.toLowerCase().includes(searchTerm))
    );
    
    // 显示过滤后的数据
    if (filteredData.length > 0) {
        renderData(filteredData, window.statisticsData, 1);
        
        // 添加搜索结果提示
        const resultInfo = document.createElement('div');
        resultInfo.className = 'alert alert-info mt-3 text-center';
        resultInfo.innerHTML = `找到 ${filteredData.length} 条符合条件的记录`;
        resultInfo.setAttribute('id', 'searchResultAlert');
        
        const contentArea = document.querySelector('.content-area');
        if (contentArea) {
            // 移除之前的提示
            const oldAlert = contentArea.querySelector('#searchResultAlert');
            if (oldAlert) oldAlert.remove();
            
            const marketHeader = contentArea.querySelector('.market-header');
            if (marketHeader) {
                marketHeader.appendChild(resultInfo);
            }
        }
    } else {
        const contentArea = document.querySelector(".content-area");
        if (contentArea) {
            contentArea.innerHTML = `
                <div class="market-header">
                    <h2><i class="bi bi-graph-up"></i> 国内上市公司全景</h2>
                    <p class="text-muted">共 ${window.marketData.length} 家公司 • 最后更新: ${new Date().toLocaleString()}</p>
                    <div class="d-flex flex-wrap justify-content-between align-items-center gap-3 mb-3">
                        <div class="d-flex flex-wrap gap-2">
                            <div class="form-inline">
                                <label for="pageSizeSelect" class="me-2">每页显示:</label>
                                <select id="pageSizeSelect" class="form-select form-select-sm" style="width: auto;" onchange="changePageSize(this.value)">
                                    <option value="20" ${PAGE_SIZE === 20 ? 'selected' : ''}>20条</option>
                                    <option value="50" ${PAGE_SIZE === 50 ? 'selected' : ''}>50条</option>
                                    <option value="100" ${PAGE_SIZE === 100 ? 'selected' : ''}>100条</option>
                                    <option value="200" ${PAGE_SIZE === 200 ? 'selected' : ''}>200条</option>
                                </select>
                            </div>
                            <button class="btn btn-primary btn-sm" onclick="refreshListedCompanyData()">
                                <i class="bi bi-arrow-repeat"></i> 刷新数据
                            </button>
                            <div class="input-group" style="max-width: 300px;">
                                <input type="text" id="searchInput" class="form-control" placeholder="搜索公司名称、代码或行业..." 
                                       value="${searchTerm}" onkeyup="if(event.key === 'Enter') searchCompanies()">
                                <button class="btn btn-outline-secondary" type="button" onclick="searchCompanies()">
                                    <i class="bi bi-search"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="alert alert-info">
                    <h4>未找到匹配结果</h4>
                    <p>没有找到与 "${searchTerm}" 匹配的公司名称、代码或行业。</p>
                    <button class="btn btn-primary mt-2" onclick="document.getElementById('searchInput').value = ''; searchCompanies();">
                        显示所有公司
                    </button>
                </div>
            `;
        }
    }
}

// 全局注册
window.loadEnhancedDomesticHotspotData = loadEnhancedDomesticHotspotData;
window.changePage = changePage;
window.toggleSort = toggleSort;
window.changePageSize = changePageSize;
window.searchCompanies = searchCompanies;
window.PAGE_SIZE = PAGE_SIZE;

// 页面加载后自动执行
document.addEventListener("DOMContentLoaded", () => {
    setTimeout(loadEnhancedDomesticHotspotData, 100);
});

// 添加样式
document.addEventListener("DOMContentLoaded", () => {
    // 检查是否已存在样式
    if (!document.getElementById('market-data-styles')) {
        const styleElement = document.createElement('style');
        styleElement.id = 'market-data-styles';
        styleElement.textContent = `
            .market-header {
                margin-bottom: 1.5rem;
            }
            .sortable {
                cursor: pointer;
                user-select: none;
                position: relative;
            }
            .sortable:hover {
                background-color: rgba(0, 0, 0, 0.7);
            }
            .table th, .table td {
                vertical-align: middle;
            }
            .progress {
                margin-bottom: 0;
            }
            /* 优化表格显示 */
            .table {
                table-layout: auto;
            }
            .table td {
                white-space: normal;
                word-break: break-word;
                max-width: 200px;
                padding: 8px 12px; /* 增加单元格内边距，提高可读性 */
            }
            /* 列宽调整 */
            .table th:nth-child(1), .table td:nth-child(1) { min-width: 80px; }
            .table th:nth-child(2), .table td:nth-child(2) { min-width: 120px; }
            .table th:nth-child(3), .table td:nth-child(3) { min-width: 100px; }
            .table th:nth-child(4), .table td:nth-child(4) { min-width: 100px; }
            .table th:nth-child(5), .table td:nth-child(5) { min-width: 100px; }
            .table th:nth-child(6), .table td:nth-child(6) { min-width: 180px; }
            .table th:nth-child(7), .table td:nth-child(7) { min-width: 120px; }
            .table th:nth-child(8), .table td:nth-child(8) { min-width: 120px; }
        `;
        document.head.appendChild(styleElement);
    }
});