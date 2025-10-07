// 公司分值表模块 - 完整实现
function loadCompanyScoreTable() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-star text-warning"></i> 公司综合评分系统</h2>
                    <p class="text-muted">基于多维度指标的公司投资价值评分</p>
                </div>
            </div>
            
            <!-- 评分概览 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h4>4,247</h4>
                            <p class="mb-0">已评分公司</p>
                            <small>A股上市公司</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h4>8.5</h4>
                            <p class="mb-0">平均评分</p>
                            <small>满分10分</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h4>156</h4>
                            <p class="mb-0">9分以上公司</p>
                            <small>优质投资标的</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h4>12</h4>
                            <p class="mb-0">评分维度</p>
                            <small>综合评估体系</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 筛选面板 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-2">
                                    <label class="form-label">行业筛选</label>
                                    <select class="form-select form-select-sm" id="industryFilter">
                                        <option value="all">全部行业</option>
                                        <option value="technology">信息技术</option>
                                        <option value="finance">金融</option>
                                        <option value="manufacturing">制造业</option>
                                        <option value="healthcare">医疗保健</option>
                                        <option value="energy">能源</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">评分范围</label>
                                    <select class="form-select form-select-sm" id="scoreRange">
                                        <option value="all">全部评分</option>
                                        <option value="high">高评分(8-10)</option>
                                        <option value="medium">中评分(6-8)</option>
                                        <option value="low">低评分(<6)</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">搜索公司</label>
                                    <input type="text" class="form-control form-control-sm" id="companySearch" placeholder="输入公司名称或代码">
                                </div>
                                <div class="col-md-2 d-flex align-items-end">
                                    <button class="btn btn-primary btn-sm w-100" onclick="filterCompanies()">
                                        <i class="bi bi-funnel"></i> 筛选
                                    </button>
                                </div>
                                <div class="col-md-2 d-flex align-items-end">
                                    <button class="btn btn-outline-secondary btn-sm w-100" onclick="exportScoreData()">
                                        <i class="bi bi-download"></i> 导出数据
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 公司评分表格 -->
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5 class="mb-0"><i class="bi bi-table"></i> 公司评分排行榜</h5>
                            <div>
                                <button class="btn btn-sm btn-outline-primary" onclick="refreshScoreData()">
                                    <i class="bi bi-arrow-clockwise"></i> 刷新数据
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-striped table-hover">
                                    <thead class="table-light">
                                        <tr>
                                            <th>排名</th>
                                            <th>公司名称</th>
                                            <th>股票代码</th>
                                            <th>所属行业</th>
                                            <th>综合评分</th>
                                            <th>财务健康度</th>
                                            <th>成长潜力</th>
                                            <th>估值水平</th>
                                            <th>风险评级</th>
                                            <th>操作</th>
                                        </tr>
                                    </thead>
                                    <tbody id="scoreTableBody">
                                        <tr>
                                            <td colspan="10" class="text-center text-muted py-5">
                                                <i class="bi bi-star display-4"></i>
                                                <p class="mt-3">正在加载公司评分数据...</p>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 加载初始数据
    loadScoreData();
}

// 加载评分数据
function loadScoreData() {
    const tableBody = document.getElementById('scoreTableBody');
    
    tableBody.innerHTML = `
        <tr>
            <td colspan="10" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">加载中...</span>
                </div>
                <p class="mt-2">正在获取公司评分数据...</p>
            </td>
        </tr>
    `;
    
    // 模拟API调用
    setTimeout(() => {
        const sampleData = [
            {
                rank: 1,
                name: "贵州茅台",
                code: "600519",
                industry: "食品饮料",
                totalScore: 9.8,
                financialHealth: 9.5,
                growthPotential: 9.2,
                valuation: 8.9,
                riskRating: "低风险",
                action: "查看详情"
            },
            {
                rank: 2,
                name: "宁德时代",
                code: "300750",
                industry: "新能源",
                totalScore: 9.6,
                financialHealth: 9.3,
                growthPotential: 9.8,
                valuation: 8.7,
                riskRating: "中风险",
                action: "查看详情"
            },
            {
                rank: 3,
                name: "招商银行",
                code: "600036",
                industry: "金融",
                totalScore: 9.4,
                financialHealth: 9.6,
                growthPotential: 8.9,
                valuation: 9.1,
                riskRating: "低风险",
                action: "查看详情"
            },
            {
                rank: 4,
                name: "比亚迪",
                code: "002594",
                industry: "汽车制造",
                totalScore: 9.2,
                financialHealth: 8.8,
                growthPotential: 9.5,
                valuation: 8.6,
                riskRating: "中风险",
                action: "查看详情"
            },
            {
                rank: 5,
                name: "海康威视",
                code: "002415",
                industry: "信息技术",
                totalScore: 9.0,
                financialHealth: 9.1,
                growthPotential: 8.7,
                valuation: 9.0,
                riskRating: "中风险",
                action: "查看详情"
            }
        ];
        
        let tableHTML = '';
        sampleData.forEach(company => {
            tableHTML += `
                <tr>
                    <td><span class="badge bg-primary">${company.rank}</span></td>
                    <td><strong>${company.name}</strong></td>
                    <td>${company.code}</td>
                    <td><span class="badge bg-secondary">${company.industry}</span></td>
                    <td>
                        <div class="progress" style="height: 20px;">
                            <div class="progress-bar bg-success" role="progressbar" style="width: ${company.totalScore * 10}%">
                                ${company.totalScore}
                            </div>
                        </div>
                    </td>
                    <td>${company.financialHealth}</td>
                    <td>${company.growthPotential}</td>
                    <td>${company.valuation}</td>
                    <td><span class="badge ${company.riskRating === '低风险' ? 'bg-success' : 'bg-warning'}">${company.riskRating}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="viewCompanyDetail('${company.code}')">
                            <i class="bi bi-eye"></i> 详情
                        </button>
                    </td>
                </tr>
            `;
        });
        
        tableBody.innerHTML = tableHTML;
    }, 1000);
}

// 筛选公司
function filterCompanies() {
    const industry = document.getElementById('industryFilter').value;
    const scoreRange = document.getElementById('scoreRange').value;
    const searchTerm = document.getElementById('companySearch').value;
    
    // 显示筛选状态
    const tableBody = document.getElementById('scoreTableBody');
    tableBody.innerHTML = `
        <tr>
            <td colspan="10" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">加载中...</span>
                </div>
                <p class="mt-2">正在筛选数据...</p>
            </td>
        </tr>
    `;
    
    setTimeout(() => {
        loadScoreData(); // 重新加载数据（实际应用中应该根据筛选条件过滤）
    }, 500);
}

// 刷新数据
function refreshScoreData() {
    loadScoreData();
}

// 导出数据
function exportScoreData() {
    alert('数据导出功能即将完成...');
    // 实际实现中这里应该调用导出API
}

// 查看公司详情
function viewCompanyDetail(stockCode) {
    alert(`查看公司详情: ${stockCode}`);
    // 实际实现中这里应该跳转到公司详情页面或显示模态框
}