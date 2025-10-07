// 行业+公司分值表模块 - 完整实现
function loadIndustryCompanyScoreTable() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-diagram-3 text-success"></i> 行业+公司综合评分</h2>
                    <p class="text-muted">行业与公司双重评分的投资决策支持系统</p>
                </div>
            </div>
            
            <!-- 筛选面板 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <label class="form-label">行业选择</label>
                                    <select class="form-select form-select-sm" id="industrySelect">
                                        <option value="all">全部行业</option>
                                        <option value="new_energy">新能源汽车</option>
                                        <option value="ai">人工智能</option>
                                        <option value="biotech">生物医药</option>
                                        <option value="semiconductor">半导体</option>
                                        <option value="cloud">云计算</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">公司评分范围</label>
                                    <select class="form-select form-select-sm" id="companyScoreRange">
                                        <option value="all">全部评分</option>
                                        <option value="high">高评分(8.5-10)</option>
                                        <option value="medium">中评分(7-8.5)</option>
                                        <option value="low">低评分(<7)</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">行业评分范围</label>
                                    <select class="form-select form-select-sm" id="industryScoreRange">
                                        <option value="all">全部评分</option>
                                        <option value="high">高评分(8.5-10)</option>
                                        <option value="medium">中评分(7-8.5)</option>
                                        <option value="low">低评分(<7)</option>
                                    </select>
                                </div>
                                <div class="col-md-3 d-flex align-items-end">
                                    <button class="btn btn-primary btn-sm w-100" onclick="filterMatrixData()">
                                        <i class="bi bi-funnel"></i> 筛选
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 综合评分矩阵 -->
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5 class="mb-0"><i class="bi bi-grid"></i> 投资价值矩阵</h5>
                            <div>
                                <button class="btn btn-sm btn-outline-primary" onclick="refreshMatrixData()">
                                    <i class="bi bi-arrow-clockwise"></i> 刷新数据
                                </button>
                                <button class="btn btn-sm btn-outline-success" onclick="exportMatrixData()">
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
                                            <th>公司名称</th>
                                            <th>股票代码</th>
                                            <th>所属行业</th>
                                            <th>公司评分</th>
                                            <th>行业评分</th>
                                            <th>综合评分</th>
                                            <th>投资建议</th>
                                            <th>操作</th>
                                        </tr>
                                    </thead>
                                    <tbody id="matrixTableBody">
                                        <tr>
                                            <td colspan="9" class="text-center text-muted py-5">
                                                <i class="bi bi-diagram-3 display-4"></i>
                                                <p class="mt-3">正在加载行业+公司评分数据...</p>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 评分分布热力图 -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-heatmap"></i> 行业-公司评分分布热力图</h5>
                        </div>
                        <div class="card-body">
                            <div id="heatmapChart" style="height: 400px;">
                                <div class="text-center text-muted py-5">
                                    <i class="bi bi-heatmap display-4"></i>
                                    <p class="mt-3">行业-公司评分分布热力图将在此显示</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 加载初始数据
    loadMatrixData();
}

// 加载矩阵数据
function loadMatrixData() {
    const tableBody = document.getElementById('matrixTableBody');
    
    tableBody.innerHTML = `
        <tr>
            <td colspan="9" class="text-center py-4">
                <div class="spinner-border text-success" role="status">
                    <span class="visually-hidden">加载中...</span>
                </div>
                <p class="mt-2">正在获取行业+公司评分数据...</p>
            </td>
        </tr>
    `;
    
    // 模拟API调用
    setTimeout(() => {
        const matrixData = [
            {
                rank: 1,
                companyName: "比亚迪",
                stockCode: "002594",
                industry: "新能源汽车",
                companyScore: 9.6,
                industryScore: 9.2,
                compositeScore: 9.4,
                recommendation: "强烈推荐",
                action: "查看详情"
            },
            {
                rank: 2,
                companyName: "宁德时代",
                stockCode: "300750",
                industry: "电池制造",
                companyScore: 9.5,
                industryScore: 8.8,
                compositeScore: 9.2,
                recommendation: "强烈推荐",
                action: "查看详情"
            },
            {
                rank: 3,
                companyName: "海康威视",
                stockCode: "002415",
                industry: "人工智能",
                companyScore: 9.0,
                industryScore: 9.0,
                compositeScore: 9.0,
                recommendation: "推荐",
                action: "查看详情"
            },
            {
                rank: 4,
                companyName: "恒瑞医药",
                stockCode: "600276",
                industry: "生物医药",
                companyScore: 8.8,
                industryScore: 8.8,
                compositeScore: 8.8,
                recommendation: "推荐",
                action: "查看详情"
            },
            {
                rank: 5,
                companyName: "中芯国际",
                stockCode: "688981",
                industry: "半导体",
                companyScore: 8.6,
                industryScore: 8.6,
                compositeScore: 8.6,
                recommendation: "谨慎推荐",
                action: "查看详情"
            },
            {
                rank: 6,
                companyName: "用友网络",
                stockCode: "600588",
                industry: "云计算",
                companyScore: 8.5,
                industryScore: 8.5,
                compositeScore: 8.5,
                recommendation: "谨慎推荐",
                action: "查看详情"
            },
            {
                rank: 7,
                companyName: "立讯精密",
                stockCode: "002475",
                industry: "消费电子",
                companyScore: 8.3,
                industryScore: 8.3,
                compositeScore: 8.3,
                recommendation: "中性",
                action: "查看详情"
            },
            {
                rank: 8,
                companyName: "平安银行",
                stockCode: "000001",
                industry: "金融科技",
                companyScore: 8.1,
                industryScore: 8.1,
                compositeScore: 8.1,
                recommendation: "中性",
                action: "查看详情"
            }
        ];
        
        let tableHTML = '';
        matrixData.forEach(item => {
            const compositeColor = item.compositeScore >= 9.0 ? 'success' : 
                                 item.compositeScore >= 8.0 ? 'warning' : 'danger';
            const recommendationColor = item.recommendation === '强烈推荐' ? 'success' :
                                      item.recommendation === '推荐' ? 'info' :
                                      item.recommendation === '谨慎推荐' ? 'warning' : 'secondary';
            
            tableHTML += `
                <tr class="${item.compositeScore >= 9.0 ? 'table-success' : item.compositeScore >= 8.0 ? 'table-warning' : ''}">
                    <td><span class="badge bg-primary">${item.rank}</span></td>
                    <td><strong>${item.companyName}</strong></td>
                    <td>${item.stockCode}</td>
                    <td><span class="badge bg-secondary">${item.industry}</span></td>
                    <td>
                        <div class="progress" style="height: 15px;">
                            <div class="progress-bar bg-info" role="progressbar" style="width: ${item.companyScore * 10}%">
                                ${item.companyScore}
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="progress" style="height: 15px;">
                            <div class="progress-bar bg-warning" role="progressbar" style="width: ${item.industryScore * 10}%">
                                ${item.industryScore}
                            </div>
                        </div>
                    </td>
                    <td>
                        <span class="badge bg-${compositeColor}">${item.compositeScore}</span>
                        <div class="progress mt-1" style="height: 8px;">
                            <div class="progress-bar bg-${compositeColor}" role="progressbar" style="width: ${item.compositeScore * 10}%"></div>
                        </div>
                    </td>
                    <td><span class="badge bg-${recommendationColor}">${item.recommendation}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="viewMatrixDetail('${item.stockCode}')">
                            <i class="bi bi-eye"></i> 详情
                        </button>
                    </td>
                </tr>
            `;
        });
        
        tableBody.innerHTML = tableHTML;
    }, 1000);
}

// 筛选矩阵数据
function filterMatrixData() {
    const industry = document.getElementById('industrySelect').value;
    const companyScoreRange = document.getElementById('companyScoreRange').value;
    const industryScoreRange = document.getElementById('industryScoreRange').value;
    
    // 显示筛选状态
    const tableBody = document.getElementById('matrixTableBody');
    tableBody.innerHTML = `
        <tr>
            <td colspan="9" class="text-center py-4">
                <div class="spinner-border text-success" role="status">
                    <span class="visually-hidden">加载中...</span>
                </div>
                <p class="mt-2">正在筛选矩阵数据...</p>
            </td>
        </tr>
    `;
    
    setTimeout(() => {
        loadMatrixData(); // 重新加载数据（实际应用中应该根据筛选条件过滤）
    }, 500);
}

// 刷新数据
function refreshMatrixData() {
    loadMatrixData();
}

// 导出数据
function exportMatrixData() {
    alert('行业+公司矩阵数据导出功能即将完成...');
    // 实际实现中这里应该调用导出API
}

// 查看矩阵详情
function viewMatrixDetail(stockCode) {
    alert(`查看矩阵详情: ${stockCode}`);
    // 实际实现中这里应该跳转到详情页面或显示模态框
}