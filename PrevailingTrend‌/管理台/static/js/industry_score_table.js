// 行业分值表模块 - 完整实现
function loadIndustryScoreTable() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-bar-chart-line text-primary"></i> 行业综合评分系统</h2>
                    <p class="text-muted">基于发展前景、盈利能力、风险水平的行业评分</p>
                </div>
            </div>
            
            <!-- 行业概览 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h4>28</h4>
                            <p class="mb-0">行业总数</p>
                            <small>申万一级行业</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h4>8.2</h4>
                            <p class="mb-0">平均评分</p>
                            <small>满分10分</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h4>6</h4>
                            <p class="mb-0">高评分行业</p>
                            <small>评分≥8.5</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h4>4</h4>
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
                                <div class="col-md-3">
                                    <label class="form-label">行业分类</label>
                                    <select class="form-select form-select-sm" id="industryCategory">
                                        <option value="all">全部行业</option>
                                        <option value="emerging">新兴行业</option>
                                        <option value="traditional">传统行业</option>
                                        <option value="cyclical">周期性行业</option>
                                        <option value="defensive">防御性行业</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">评分范围</label>
                                    <select class="form-select form-select-sm" id="scoreRange">
                                        <option value="all">全部评分</option>
                                        <option value="high">高评分(8.5-10)</option>
                                        <option value="medium">中评分(7-8.5)</option>
                                        <option value="low">低评分(<7)</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">风险偏好</label>
                                    <select class="form-select form-select-sm" id="riskPreference">
                                        <option value="all">全部风险</option>
                                        <option value="low">低风险</option>
                                        <option value="medium">中风险</option>
                                        <option value="high">高风险</option>
                                    </select>
                                </div>
                                <div class="col-md-3 d-flex align-items-end">
                                    <button class="btn btn-primary btn-sm w-100" onclick="filterIndustries()">
                                        <i class="bi bi-funnel"></i> 筛选
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 行业评分排行 -->
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5 class="mb-0"><i class="bi bi-award"></i> 行业投资价值排行榜</h5>
                            <div>
                                <button class="btn btn-sm btn-outline-primary" onclick="refreshIndustryData()">
                                    <i class="bi bi-arrow-clockwise"></i> 刷新数据
                                </button>
                                <button class="btn btn-sm btn-outline-success" onclick="exportIndustryData()">
                                    <i class="bi bi-download"></i> 导出
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-striped table-hover">
                                    <thead class="table-light">
                                        <tr>
                                            <th>排名</th>
                                            <th>行业名称</th>
                                            <th>综合评分</th>
                                            <th>发展前景</th>
                                            <th>盈利能力</th>
                                            <th>风险水平</th>
                                            <th>公司数量</th>
                                            <th>投资建议</th>
                                            <th>操作</th>
                                        </tr>
                                    </thead>
                                    <tbody id="industryTableBody">
                                        <tr>
                                            <td colspan="9" class="text-center text-muted py-5">
                                                <i class="bi bi-bar-chart-line display-4"></i>
                                                <p class="mt-3">正在加载行业评分数据...</p>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 行业分布图表 -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-pie-chart"></i> 行业评分分布</h5>
                        </div>
                        <div class="card-body">
                            <div id="industryChart" style="height: 300px;">
                                <div class="text-center text-muted py-5">
                                    <i class="bi bi-pie-chart display-4"></i>
                                    <p class="mt-3">行业评分分布图表将在此显示</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 加载初始数据
    loadIndustryData();
}

// 加载行业数据
function loadIndustryData() {
    const tableBody = document.getElementById('industryTableBody');
    
    tableBody.innerHTML = `
        <tr>
            <td colspan="9" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">加载中...</span>
                </div>
                <p class="mt-2">正在获取行业评分数据...</p>
            </td>
        </tr>
    `;
    
    // 模拟API调用
    setTimeout(() => {
        const industryData = [
            {
                rank: 1,
                name: "新能源汽车",
                totalScore: 9.2,
                developmentProspect: 9.5,
                profitability: 8.8,
                riskLevel: 9.3,
                companyCount: 156,
                recommendation: "强烈推荐",
                action: "查看详情"
            },
            {
                rank: 2,
                name: "人工智能",
                totalScore: 9.0,
                developmentProspect: 9.8,
                profitability: 8.5,
                riskLevel: 8.7,
                companyCount: 89,
                recommendation: "推荐",
                action: "查看详情"
            },
            {
                rank: 3,
                name: "生物医药",
                totalScore: 8.8,
                developmentProspect: 9.2,
                profitability: 8.9,
                riskLevel: 8.3,
                companyCount: 124,
                recommendation: "推荐",
                action: "查看详情"
            },
            {
                rank: 4,
                name: "半导体",
                totalScore: 8.6,
                developmentProspect: 9.0,
                profitability: 8.4,
                riskLevel: 8.5,
                companyCount: 78,
                recommendation: "谨慎推荐",
                action: "查看详情"
            },
            {
                rank: 5,
                name: "云计算",
                totalScore: 8.5,
                developmentProspect: 9.1,
                profitability: 8.3,
                riskLevel: 8.1,
                companyCount: 67,
                recommendation: "谨慎推荐",
                action: "查看详情"
            },
            {
                rank: 6,
                name: "消费电子",
                totalScore: 8.3,
                developmentProspect: 8.7,
                profitability: 8.6,
                riskLevel: 7.8,
                companyCount: 92,
                recommendation: "中性",
                action: "查看详情"
            },
            {
                rank: 7,
                name: "金融科技",
                totalScore: 8.1,
                developmentProspect: 8.9,
                profitability: 8.2,
                riskLevel: 7.5,
                companyCount: 45,
                recommendation: "中性",
                action: "查看详情"
            },
            {
                rank: 8,
                name: "传统能源",
                totalScore: 7.8,
                developmentProspect: 7.5,
                profitability: 8.0,
                riskLevel: 7.9,
                companyCount: 56,
                recommendation: "谨慎",
                action: "查看详情"
            }
        ];
        
        let tableHTML = '';
        industryData.forEach(industry => {
            const scoreColor = industry.totalScore >= 8.5 ? 'success' : 
                             industry.totalScore >= 7.5 ? 'warning' : 'danger';
            const recommendationColor = industry.recommendation === '强烈推荐' ? 'success' :
                                      industry.recommendation === '推荐' ? 'info' :
                                      industry.recommendation === '谨慎推荐' ? 'warning' : 'secondary';
            
            tableHTML += `
                <tr>
                    <td><span class="badge bg-primary">${industry.rank}</span></td>
                    <td><strong>${industry.name}</strong></td>
                    <td>
                        <span class="badge bg-${scoreColor}">${industry.totalScore}</span>
                        <div class="progress mt-1" style="height: 5px;">
                            <div class="progress-bar bg-${scoreColor}" role="progressbar" style="width: ${industry.totalScore * 10}%"></div>
                        </div>
                    </td>
                    <td>${industry.developmentProspect}</td>
                    <td>${industry.profitability}</td>
                    <td>
                        <span class="badge ${industry.riskLevel >= 8.5 ? 'bg-success' : industry.riskLevel >= 7.5 ? 'bg-warning' : 'bg-danger'}">
                            ${industry.riskLevel}
                        </span>
                    </td>
                    <td>${industry.companyCount}</td>
                    <td><span class="badge bg-${recommendationColor}">${industry.recommendation}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="viewIndustryDetail('${industry.name}')">
                            <i class="bi bi-eye"></i> 详情
                        </button>
                    </td>
                </tr>
            `;
        });
        
        tableBody.innerHTML = tableHTML;
    }, 1000);
}

// 筛选行业
function filterIndustries() {
    const category = document.getElementById('industryCategory').value;
    const scoreRange = document.getElementById('scoreRange').value;
    const riskPreference = document.getElementById('riskPreference').value;
    
    // 显示筛选状态
    const tableBody = document.getElementById('industryTableBody');
    tableBody.innerHTML = `
        <tr>
            <td colspan="9" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">加载中...</span>
                </div>
                <p class="mt-2">正在筛选行业数据...</p>
            </td>
        </tr>
    `;
    
    setTimeout(() => {
        loadIndustryData(); // 重新加载数据（实际应用中应该根据筛选条件过滤）
    }, 500);
}

// 刷新数据
function refreshIndustryData() {
    loadIndustryData();
}

// 导出数据
function exportIndustryData() {
    alert('行业数据导出功能即将完成...');
    // 实际实现中这里应该调用导出API
}

// 查看行业详情
function viewIndustryDetail(industryName) {
    alert(`查看行业详情: ${industryName}`);
    // 实际实现中这里应该跳转到行业详情页面或显示模态框
}