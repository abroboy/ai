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
            <p class="mt-3">正在加载国内热点数据...</p>
        </div>
    `;

    // 自包含数据生成 - 扩展到5000+条数据
    function generateFullDataset() {
        // 扩展行业和公司名称列表，使数据更加多样化
        const industries = [
            '科技', '金融', '医疗', '消费', '能源', '制造', '地产', '公用事业',
            '农业', '教育', '交通', '物流', '传媒', '通信', '零售', '旅游',
            '餐饮', '文化', '体育', '娱乐', '环保', '新能源', '互联网', '电子商务'
        ];
        
        // 扩展公司名称列表
        const companyPrefixes = ['中国', '国际', '环球', '东方', '西部', '南方', '北方', '华夏', '亚太', '欧美'];
        const companySuffixes = ['科技', '集团', '控股', '股份', '信息', '网络', '电子', '数据', '软件', '硬件'];
        const companyMiddles = ['通信', '电子', '医药', '金融', '能源', '食品', '建筑', '汽车', '服装', '教育'];
        
        // 生成5000+条数据
        const totalCompanies = 5200;
        const result = [];
        
        for (let i = 0; i < totalCompanies; i++) {
            // 生成更多样化的公司名称
            let companyName;
            if (i < 100) {
                // 前100家使用知名公司名称
                const famousCompanies = [
                    '阿里巴巴', '腾讯', '美团', '京东', '拼多多', '百度', '网易', '小米', 
                    '中国平安', '招商银行', '中信证券', '贵州茅台', '五粮液', '格力电器', 
                    '海尔智家', '比亚迪', '宁德时代', '中国石油', '中国石化', '中国移动'
                ];
                companyName = famousCompanies[i % famousCompanies.length];
            } else {
                // 其余公司使用组合名称
                const prefix = companyPrefixes[Math.floor(Math.random() * companyPrefixes.length)];
                const middle = companyMiddles[Math.floor(Math.random() * companyMiddles.length)];
                const suffix = companySuffixes[Math.floor(Math.random() * companySuffixes.length)];
                companyName = `${prefix}${middle}${suffix}`;
            }
            
            // 生成股票代码 (沪市600/601/603/605，深市000/001/002/003，创业板300/301，科创板688)
            let stockCode;
            const codeType = Math.floor(Math.random() * 10);
            if (codeType < 4) {
                // 沪市A股
                const prefix = ['600', '601', '603', '605'][Math.floor(Math.random() * 4)];
                stockCode = prefix + String(Math.floor(Math.random() * 1000)).padStart(3, '0');
            } else if (codeType < 7) {
                // 深市A股
                const prefix = ['000', '001', '002', '003'][Math.floor(Math.random() * 4)];
                stockCode = prefix + String(Math.floor(Math.random() * 1000)).padStart(3, '0');
            } else if (codeType < 9) {
                // 创业板
                const prefix = ['300', '301'][Math.floor(Math.random() * 2)];
                stockCode = prefix + String(Math.floor(Math.random() * 1000)).padStart(3, '0');
            } else {
                // 科创板
                stockCode = '688' + String(Math.floor(Math.random() * 1000)).padStart(3, '0');
            }
            
            // 生成价格和涨跌幅
            // 根据不同板块设置不同价格范围
            let basePrice;
            if (stockCode.startsWith('688')) {
                // 科创板股票价格普遍较高
                basePrice = Math.random() * 150 + 50;
            } else if (stockCode.startsWith('300') || stockCode.startsWith('301')) {
                // 创业板价格中等
                basePrice = Math.random() * 100 + 30;
            } else {
                // 主板价格范围更广
                basePrice = Math.random() * 80 + 5;
            }
            
            const price = basePrice.toFixed(2);
            
            // 涨跌幅 (-10% ~ +10%)，贴近涨跌停板
            let change;
            const limitProb = Math.random();
            if (limitProb < 0.05) {
                // 5%概率涨停
                change = '10.00';
            } else if (limitProb < 0.1) {
                // 5%概率跌停
                change = '-10.00';
            } else if (limitProb < 0.3) {
                // 20%概率大幅波动
                change = (Math.random() * 8 - 4).toFixed(2);
            } else {
                // 70%概率小幅波动
                change = (Math.random() * 4 - 2).toFixed(2);
            }
            
            // 数据来源更加多样化
            const sources = ['东方财富', '同花顺', '雪球', '新浪财经', '腾讯财经', '证券时报', '中国证券报', '上证报'];
            const source = sources[Math.floor(Math.random() * sources.length)];
            
            // 热度分数 - 与涨跌幅、成交量相关
            const absChange = Math.abs(parseFloat(change));
            const volumeFactor = Math.random() * 30; // 模拟成交量因素
            const heatScore = Math.min(100, absChange * 5 + volumeFactor + Math.random() * 20);
            
            // 发布时间 - 过去24小时内随机时间
            const publishTime = new Date(Date.now() - Math.random() * 86400000).toISOString();
            
            // 行业分类 - 根据股票代码范围进行一些关联
            let category;
            if (i < 100) {
                // 前100家公司使用固定行业
                category = industries[i % industries.length];
            } else {
                // 根据股票代码首位数字关联一些行业
                const firstDigit = parseInt(stockCode[3]);
                const industryIndex = (firstDigit + i) % industries.length;
                category = industries[industryIndex];
            }
            
            result.push({
                id: stockCode,
                name: companyName,
                category: category,
                price: price,
                change: change,
                source: source,
                heatScore: heatScore.toFixed(1),
                publishTime: publishTime
            });
        }
        
        return result;
    }

    // 模拟异步加载 - 使用Web Worker处理大量数据
    if (window.Worker) {
        // 创建内联Worker
        const workerBlob = new Blob([`
            self.onmessage = function(e) {
                if (e.data === 'generate') {
                    // 复制数据生成函数到Worker中
                    ${generateFullDataset.toString()}
                    
                    // 生成数据
                    const data = generateFullDataset();
                    
                    // 返回生成的数据
                    self.postMessage(data);
                }
            };
        `], { type: 'application/javascript' });
        
        const workerUrl = URL.createObjectURL(workerBlob);
        const worker = new Worker(workerUrl);
        
        worker.onmessage = function(e) {
            // 存储数据到全局变量，便于分页操作
            window.marketData = e.data;
            renderData(e.data, 1); // 默认显示第1页
            
            // 清理Worker
            worker.terminate();
            URL.revokeObjectURL(workerUrl);
        };
        
        worker.onerror = function(error) {
            contentArea.innerHTML = `
                <div class="alert alert-danger">
                    <h4>数据加载失败</h4>
                    <p>Worker错误: ${error.message}</p>
                    <button class="btn btn-primary mt-2" onclick="loadEnhancedDomesticHotspotData()">
                        重试加载
                    </button>
                </div>
            `;
            
            // 清理Worker
            worker.terminate();
            URL.revokeObjectURL(workerUrl);
        };
        
        // 启动数据生成
        worker.postMessage('generate');
    } else {
        // 浏览器不支持Worker，回退到主线程处理
        setTimeout(() => {
            try {
                const fullData = generateFullDataset();
                // 存储数据到全局变量，便于分页操作
                window.marketData = fullData;
                renderData(fullData, 1); // 默认显示第1页
            } catch (e) {
                contentArea.innerHTML = `
                    <div class="alert alert-danger">
                        <h4>数据加载失败</h4>
                        <p>${e.message}</p>
                        <button class="btn btn-primary mt-2" onclick="loadEnhancedDomesticHotspotData()">
                            重试加载
                        </button>
                    </div>
                `;
            }
        }, 800);
    }
}

// 分页配置
const PAGE_SIZE = 50; // 每页显示的公司数量，增加到50条以显示更多数据

// 当前排序状态
let currentSortField = 'heatScore'; // 默认按热度排序
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
        if (field === 'price' || field === 'heatScore') {
            valueA = parseFloat(valueA);
            valueB = parseFloat(valueB);
        } else if (field === 'change') {
            // 特殊处理涨跌幅，确保正确排序（去除%和正负号）
            valueA = parseFloat(valueA);
            valueB = parseFloat(valueB);
        } else if (field === 'publishTime') {
            // 日期时间排序
            valueA = new Date(valueA).getTime();
            valueB = new Date(valueB).getTime();
        } else if (field === 'id') {
            // 股票代码排序 - 确保按数字大小排序而不是字符串
            valueA = valueA.toString();
            valueB = valueB.toString();
        }
        
        // 处理相等的情况，使用热度作为次要排序条件
        if (valueA === valueB && field !== 'heatScore') {
            const heatA = parseFloat(data[a]['heatScore']);
            const heatB = parseFloat(data[b]['heatScore']);
            return direction === 'asc' ? heatA - heatB : heatB - heatA;
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
        renderData(window.marketData, currentPageToKeep);
    }
}

// 渲染逻辑（表格式，带分页和排序）- 优化以处理大量数据
function renderData(data, currentPage = 1) {
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
        // 按当前排序条件排序
        const sortedData = sortData(data, currentSortField, currentSortDirection);
        
        // 计算分页
        const totalPages = Math.ceil(sortedData.length / PAGE_SIZE);
        currentPage = Math.max(1, Math.min(currentPage, totalPages)); // 确保页码在有效范围内
        
        // 获取当前页的数据
        const startIndex = (currentPage - 1) * PAGE_SIZE;
        const endIndex = Math.min(startIndex + PAGE_SIZE, sortedData.length);
        const currentPageData = sortedData.slice(startIndex, endIndex);
        
        // 构建HTML
        let html = `
            <div class="market-header">
                <h2><i class="bi bi-graph-up"></i> 国内上市公司全景</h2>
                <p class="text-muted">共 ${data.length} 家公司 • 最后更新: ${new Date().toLocaleString()}</p>
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div class="form-inline">
                        <label for="pageSizeSelect" class="me-2">每页显示:</label>
                        <select id="pageSizeSelect" class="form-select form-select-sm" style="width: auto;" onchange="changePageSize(this.value)">
                            <option value="20" ${PAGE_SIZE === 20 ? 'selected' : ''}>20条</option>
                            <option value="50" ${PAGE_SIZE === 50 ? 'selected' : ''}>50条</option>
                            <option value="100" ${PAGE_SIZE === 100 ? 'selected' : ''}>100条</option>
                            <option value="200" ${PAGE_SIZE === 200 ? 'selected' : ''}>200条</option>
                        </select>
                    </div>
                    <div class="input-group" style="max-width: 300px;">
                        <input type="text" id="searchInput" class="form-control" placeholder="搜索公司名称或代码..." 
                               onkeyup="if(event.key === 'Enter') searchCompanies()">
                        <button class="btn btn-outline-secondary" type="button" onclick="searchCompanies()">
                            <i class="bi bi-search"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div class="table-responsive" style="overflow-x: auto; max-width: 100%;">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th scope="col" class="sortable" onclick="toggleSort('id')">
                                代码 ${getSortIcon('id')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('name')">
                                公司名称 ${getSortIcon('name')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('category')">
                                行业 ${getSortIcon('category')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('price')">
                                当前价格 ${getSortIcon('price')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('change')">
                                涨跌幅 ${getSortIcon('change')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('heatScore')">
                                热度 ${getSortIcon('heatScore')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('source')">
                                数据来源 ${getSortIcon('source')}
                            </th>
                            <th scope="col" class="sortable" onclick="toggleSort('publishTime')">
                                更新时间 ${getSortIcon('publishTime')}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        // 构建表格行HTML
        currentPageData.forEach(item => {
            const changeValue = parseFloat(item.change);
            const changeClass = changeValue > 0 ? 'text-success' : (changeValue < 0 ? 'text-danger' : 'text-muted');
            const changeIcon = changeValue > 0 ? '↑' : (changeValue < 0 ? '↓' : '-');
            
            html += `
                <tr>
                    <td title="${item.id}">${item.id}</td>
                    <td title="${item.name}"><strong>${item.name}</strong></td>
                    <td title="${item.category}">${item.category}</td>
                    <td title="¥${item.price}">¥${item.price}</td>
                    <td class="${changeClass}" title="${changeIcon} ${Math.abs(changeValue)}%"><strong>${changeIcon} ${Math.abs(changeValue)}%</strong></td>
                    <td>
                        <div class="progress" style="height: 20px;" title="热度: ${item.heatScore}">
                            <div class="progress-bar bg-${parseFloat(item.heatScore) > 70 ? 'danger' : parseFloat(item.heatScore) > 50 ? 'warning' : 'success'}" 
                                 role="progressbar" 
                                 style="width: ${Math.min(100, item.heatScore)}%" 
                                 aria-valuenow="${item.heatScore}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100">
                                ${Math.round(parseFloat(item.heatScore))}
                            </div>
                        </div>
                    </td>
                    <td title="${item.source}">${item.source}</td>
                    <td title="${new Date(item.publishTime).toLocaleString()}">${new Date(item.publishTime).toLocaleTimeString()}</td>
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
    renderData(window.marketData, pageNumber);
    // 滚动到页面顶部
    window.scrollTo({top: 0, behavior: 'smooth'});
}

// 更改每页显示数量
function changePageSize(size) {
    window.PAGE_SIZE = parseInt(size);
    if (window.marketData) {
        renderData(window.marketData, 1);
    }
}

// 搜索公司
function searchCompanies() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput || !window.marketData) return;
    
    const searchTerm = searchInput.value.trim().toLowerCase();
    
    if (searchTerm === '') {
        // 如果搜索框为空，显示所有数据
        renderData(window.marketData, 1);
        return;
    }
    
    // 过滤数据 - 增强搜索功能，同时搜索公司名称、代码和行业
    const filteredData = window.marketData.filter(item => 
        item.name.toLowerCase().includes(searchTerm) || 
        item.id.toLowerCase().includes(searchTerm) ||
        item.category.toLowerCase().includes(searchTerm)
    );
    
    // 显示过滤后的数据
    if (filteredData.length > 0) {
        renderData(filteredData, 1);
    } else {
        const contentArea = document.querySelector(".content-area");
        if (contentArea) {
            contentArea.innerHTML = `
                <div class="market-header">
                    <h2><i class="bi bi-graph-up"></i> 国内上市公司全景</h2>
                    <p class="text-muted">共 ${window.marketData.length} 家公司 • 最后更新: ${new Date().toLocaleString()}</p>
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div class="form-inline">
                            <label for="pageSizeSelect" class="me-2">每页显示:</label>
                            <select id="pageSizeSelect" class="form-select form-select-sm" style="width: auto;" onchange="changePageSize(this.value)">
                                <option value="20" ${PAGE_SIZE === 20 ? 'selected' : ''}>20条</option>
                                <option value="50" ${PAGE_SIZE === 50 ? 'selected' : ''}>50条</option>
                                <option value="100" ${PAGE_SIZE === 100 ? 'selected' : ''}>100条</option>
                                <option value="200" ${PAGE_SIZE === 200 ? 'selected' : ''}>200条</option>
                            </select>
                        </div>
                        <div class="input-group" style="max-width: 300px;">
                            <input type="text" id="searchInput" class="form-control" placeholder="搜索公司名称或代码..." 
                                   value="${searchTerm}" onkeyup="if(event.key === 'Enter') searchCompanies()">
                            <button class="btn btn-outline-secondary" type="button" onclick="searchCompanies()">
                                <i class="bi bi-search"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="alert alert-info">
                    <h4>未找到匹配结果</h4>
                    <p>没有找到与 "${searchTerm}" 匹配的公司名称或代码。</p>
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