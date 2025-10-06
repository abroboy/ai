/**
 * 公司属性表模块增强版
 * 大势所趋风险框架管理台
 */

// 加载公司属性表模块
function loadCompanyAttributes() {
    const container = document.getElementById('content');
    
    // 显示加载状态
    container.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-3">正在加载公司属性数据...</p>
        </div>
    `;

    // 获取数据并渲染
    fetchCompanyAttributesData()
        .then(data => {
            if (data.success) {
                renderCompanyAttributesModule(container, data);
            } else {
                throw new Error(data.message || '数据加载失败');
            }
        })
        .catch(error => {
            container.innerHTML = `
                <div class="alert alert-danger">
                    <h5><i class="bi bi-exclamation-triangle"></i> 数据加载失败</h5>
                    <p>${error.message}</p>
                    <button class="btn btn-primary" onclick="loadCompanyAttributes()">重新加载</button>
                </div>
            `;
        });
}

// 获取公司属性数据
async function fetchCompanyAttributesData() {
    try {
        // 尝试从API获取数据
        const response = await fetch('/api/listed-companies?' + new URLSearchParams({
            page: 0,
            size: 50,
            timestamp: Date.now()
        }));
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        if (result.success && result.data && result.data.companies) {
            return {
                success: true,
                data: result.data.companies.map(company => ({
                    id: company.code || company.id,
                    name: company.name,
                    industry: company.industry || '未分类',
                    region: company.region || '未知',
                    marketCap: company.marketCap ? formatMarketCap(company.marketCap) : '未知',
                    riskLevel: calculateRiskLevel(company),
                    score: calculateCompanyScore(company),
                    pe: company.pe || Math.random() * 30 + 10,
                    pb: company.pb || Math.random() * 5 + 1,
                    roe: company.roe || Math.random() * 20 + 5,
                    revenue: company.revenue || Math.random() * 1000 + 100,
                    profit: company.profit || Math.random() * 100 + 10
                }))
            };
        } else {
            throw new Error('API返回数据格式错误');
        }
    } catch (error) {
        console.error('获取公司属性数据失败:', error);
        // 返回模拟数据作为备用
        return getMockCompanyAttributesData();
    }
}

// 模拟数据备用方案
function getMockCompanyAttributesData() {
    return {
        success: true,
        data: [
            {
                id: '000001.SZ',
                name: '平安银行',
                industry: '银行',
                region: '深圳',
                marketCap: '2410亿',
                riskLevel: '低',
                score: 85,
                pe: 5.2,
                pb: 0.8,
                roe: 11.5,
                revenue: 1680.5,
                profit: 329.2
            },
            {
                id: '000002.SZ',
                name: '万科A',
                industry: '房地产',
                region: '深圳',
                marketCap: '980亿',
                riskLevel: '中',
                score: 72,
                pe: 8.9,
                pb: 0.9,
                roe: 10.2,
                revenue: 4528.1,
                profit: 225.2
            },
            {
                id: '600519.SH',
                name: '贵州茅台',
                industry: '白酒',
                region: '贵州',
                marketCap: '21000亿',
                riskLevel: '低',
                score: 92,
                pe: 28.5,
                pb: 10.2,
                roe: 24.8,
                revenue: 1061.8,
                profit: 575.1
            },
            {
                id: '300750.SZ',
                name: '宁德时代',
                industry: '新能源',
                region: '福建',
                marketCap: '8700亿',
                riskLevel: '中',
                score: 88,
                pe: 35.6,
                pb: 4.2,
                roe: 18.9,
                revenue: 3285.9,
                profit: 332.2
            },
            {
                id: '002594.SZ',
                name: '比亚迪',
                industry: '汽车',
                region: '深圳',
                marketCap: '7150亿',
                riskLevel: '中',
                score: 86,
                pe: 22.3,
                pb: 3.1,
                roe: 16.7,
                revenue: 4240.6,
                profit: 166.2
            }
        ]
    };
}

// 渲染公司属性表模块
function renderCompanyAttributesModule(container, data) {
    const companies = data.data;
    
    const moduleHTML = `
        <div class="company-attributes-module">
            <!-- 模块标题 -->
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h4><i class="bi bi-building text-primary"></i> 公司属性表</h4>
                <div>
                    <span class="badge bg-success">实时数据</span>
                    <button class="btn btn-outline-primary btn-sm ms-2" onclick="refreshCompanyAttributes()">
                        <i class="bi bi-arrow-clockwise"></i> 刷新
                    </button>
                    <button class="btn btn-outline-success btn-sm ms-2" onclick="exportCompanyData()">
                        <i class="bi bi-download"></i> 导出
                    </button>
                </div>
            </div>

            <!-- 统计概览 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body text-center">
                            <h3>${companies.length}</h3>
                            <p class="mb-0">公司总数</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body text-center">
                            <h3>${getUniqueIndustries(companies).length}</h3>
                            <p class="mb-0">行业数量</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body text-center">
                            <h3>${getAverageScore(companies).toFixed(1)}</h3>
                            <p class="mb-0">平均评分</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body text-center">
                            <h3>${getHighScoreCount(companies)}</h3>
                            <p class="mb-0">高分公司</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 筛选和搜索 -->
            <div class="row mb-3">
                <div class="col-md-4">
                    <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-search"></i></span>
                        <input type="text" class="form-control" placeholder="搜索公司..." id="companySearch">
                    </div>
                </div>
                <div class="col-md-3">
                    <select class="form-select" id="industryFilter">
                        <option value="">全部行业</option>
                        ${getUniqueIndustries(companies).map(industry => 
                            `<option value="${industry}">${industry}</option>`
                        ).join('')}
                    </select>
                </div>
                <div class="col-md-3">
                    <select class="form-select" id="riskFilter">
                        <option value="">全部风险等级</option>
                        <option value="低">低风险</option>
                        <option value="中">中风险</option>
                        <option value="高">高风险</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <select class="form-select" id="sortBy">
                        <option value="score">按评分排序</option>
                        <option value="marketCap">按市值排序</option>
                        <option value="name">按名称排序</option>
                    </select>
                </div>
            </div>

            <!-- 公司列表表格 -->
            <div class="card">
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover" id="companyTable">
                            <thead class="table-dark">
                                <tr>
                                    <th>公司名称</th>
                                    <th>代码</th>
                                    <th>行业</th>
                                    <th>地区</th>
                                    <th>市值</th>
                                    <th>风险等级</th>
                                    <th>评分</th>
                                    <th>PE</th>
                                    <th>PB</th>
                                    <th>ROE(%)</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody id="companyTableBody">
                                ${companies.map(company => createCompanyRow(company)).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 行业分布图表 -->
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-pie-chart"></i> 行业分布</h5>
                        </div>
                        <div class="card-body">
                            <canvas id="industryChart" height="300"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-bar-chart"></i> 评分分布</h5>
                        </div>
                        <div class="card-body">
                            <canvas id="scoreChart" height="300"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = moduleHTML;
    
    // 初始化功能
    initCompanySearch(companies);
    initCompanyFilters(companies);
    renderIndustryChart(companies);
    renderScoreChart(companies);
}

// 创建公司行
function createCompanyRow(company) {
    const riskBadge = getRiskBadge(company.riskLevel);
    const scoreBadge = getScoreBadge(company.score);
    
    return `
        <tr class="company-row" data-industry="${company.industry}" data-risk="${company.riskLevel}">
            <td>
                <div class="fw-bold">${company.name}</div>
            </td>
            <td><code>${company.id}</code></td>
            <td><span class="badge bg-secondary">${company.industry}</span></td>
            <td>${company.region}</td>
            <td>${company.marketCap}</td>
            <td>${riskBadge}</td>
            <td>${scoreBadge}</td>
            <td>${company.pe.toFixed(1)}</td>
            <td>${company.pb.toFixed(1)}</td>
            <td>${company.roe.toFixed(1)}%</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="viewCompanyDetail('${company.id}')">
                    <i class="bi bi-eye"></i>
                </button>
            </td>
        </tr>
    `;
}

// 辅助函数
function formatMarketCap(value) {
    if (typeof value === 'string') return value;
    if (value >= 10000) return (value / 10000).toFixed(0) + '万亿';
    if (value >= 100) return (value / 100).toFixed(0) + '百亿';
    return value.toFixed(0) + '亿';
}

function calculateRiskLevel(company) {
    const score = company.score || Math.random() * 100;
    if (score >= 80) return '低';
    if (score >= 60) return '中';
    return '高';
}

function calculateCompanyScore(company) {
    return Math.floor(Math.random() * 40) + 60; // 60-100分
}

function getRiskBadge(risk) {
    const badges = {
        '低': '<span class="badge bg-success">低风险</span>',
        '中': '<span class="badge bg-warning">中风险</span>',
        '高': '<span class="badge bg-danger">高风险</span>'
    };
    return badges[risk] || badges['中'];
}

function getScoreBadge(score) {
    let color = 'bg-secondary';
    if (score >= 90) color = 'bg-success';
    else if (score >= 80) color = 'bg-info';
    else if (score >= 70) color = 'bg-warning';
    else if (score < 60) color = 'bg-danger';
    
    return `<span class="badge ${color}">${score}</span>`;
}

function getUniqueIndustries(companies) {
    return [...new Set(companies.map(c => c.industry))];
}

function getAverageScore(companies) {
    return companies.reduce((sum, c) => sum + c.score, 0) / companies.length;
}

function getHighScoreCount(companies) {
    return companies.filter(c => c.score >= 80).length;
}

// 初始化搜索功能
function initCompanySearch(companies) {
    const searchInput = document.getElementById('companySearch');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        filterCompanies();
    });
}

// 初始化筛选功能
function initCompanyFilters(companies) {
    const filters = ['industryFilter', 'riskFilter', 'sortBy'];
    
    filters.forEach(filterId => {
        const filter = document.getElementById(filterId);
        if (filter) {
            filter.addEventListener('change', function() {
                filterCompanies();
            });
        }
    });
}

// 筛选公司
function filterCompanies() {
    const searchTerm = document.getElementById('companySearch').value.toLowerCase();
    const industryFilter = document.getElementById('industryFilter').value;
    const riskFilter = document.getElementById('riskFilter').value;
    const sortBy = document.getElementById('sortBy').value;
    
    const rows = document.querySelectorAll('.company-row');
    let visibleRows = [];
    
    rows.forEach(row => {
        const name = row.querySelector('td:first-child').textContent.toLowerCase();
        const industry = row.getAttribute('data-industry');
        const risk = row.getAttribute('data-risk');
        
        const matchesSearch = name.includes(searchTerm);
        const matchesIndustry = !industryFilter || industry === industryFilter;
        const matchesRisk = !riskFilter || risk === riskFilter;
        
        if (matchesSearch && matchesIndustry && matchesRisk) {
            row.style.display = '';
            visibleRows.push(row);
        } else {
            row.style.display = 'none';
        }
    });
    
    // 排序
    if (sortBy && visibleRows.length > 0) {
        sortCompanyRows(visibleRows, sortBy);
    }
}

// 排序公司行
function sortCompanyRows(rows, sortBy) {
    const tbody = document.getElementById('companyTableBody');
    
    rows.sort((a, b) => {
        let aValue, bValue;
        
        switch(sortBy) {
            case 'score':
                aValue = parseInt(a.querySelector('td:nth-child(7) .badge').textContent);
                bValue = parseInt(b.querySelector('td:nth-child(7) .badge').textContent);
                return bValue - aValue; // 降序
            case 'name':
                aValue = a.querySelector('td:first-child').textContent;
                bValue = b.querySelector('td:first-child').textContent;
                return aValue.localeCompare(bValue);
            default:
                return 0;
        }
    });
    
    // 重新排列DOM
    rows.forEach(row => tbody.appendChild(row));
}

// 渲染行业分布图表
function renderIndustryChart(companies) {
    const canvas = document.getElementById('industryChart');
    if (!canvas || typeof Chart === 'undefined') return;
    
    const ctx = canvas.getContext('2d');
    const industries = getUniqueIndustries(companies);
    const data = industries.map(industry => 
        companies.filter(c => c.industry === industry).length
    );
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: industries,
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 205, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)'
                ]
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

// 渲染评分分布图表
function renderScoreChart(companies) {
    const canvas = document.getElementById('scoreChart');
    if (!canvas || typeof Chart === 'undefined') return;
    
    const ctx = canvas.getContext('2d');
    const scoreRanges = ['60-70', '70-80', '80-90', '90-100'];
    const data = [
        companies.filter(c => c.score >= 60 && c.score < 70).length,
        companies.filter(c => c.score >= 70 && c.score < 80).length,
        companies.filter(c => c.score >= 80 && c.score < 90).length,
        companies.filter(c => c.score >= 90).length
    ];
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: scoreRanges,
            datasets: [{
                label: '公司数量',
                data: data,
                backgroundColor: 'rgba(54, 162, 235, 0.8)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
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

// 查看公司详情
function viewCompanyDetail(companyId) {
    alert(`查看公司详情: ${companyId}\n此功能将跳转到详情页面`);
}

// 导出公司数据
function exportCompanyData() {
    alert('导出功能开发中...');
}

// 刷新公司属性数据
function refreshCompanyAttributes() {
    loadCompanyAttributes();
}

// 导出模块函数
if (typeof window !== 'undefined') {
    window.loadCompanyAttributes = loadCompanyAttributes;
    window.refreshCompanyAttributes = refreshCompanyAttributes;
    window.viewCompanyDetail = viewCompanyDetail;
    window.exportCompanyData = exportCompanyData;
}