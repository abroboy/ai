// 对象因子权重表模块 - 完整实现
function loadObjectFactorWeightTable() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-sliders text-info"></i> 因子权重管理系统</h2>
                    <p class="text-muted">动态调整评分因子权重，优化投资决策模型</p>
                </div>
            </div>
            
            <!-- 权重概览 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h4>12</h4>
                            <p class="mb-0">因子总数</p>
                            <small>可配置因子</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h4>85.3%</h4>
                            <p class="mb-0">模型准确率</p>
                            <small>当前权重配置</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h4>4.2</h4>
                            <p class="mb-0">平均贡献度</p>
                            <small>因子平均贡献</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h4>3</h4>
                            <p class="mb-0">高权重因子</p>
                            <small>权重≥15%</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 权重配置面板 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5 class="mb-0"><i class="bi bi-gear"></i> 因子权重配置</h5>
                            <div>
                                <button class="btn btn-sm btn-outline-primary" onclick="resetWeights()">
                                    <i class="bi bi-arrow-clockwise"></i> 重置权重
                                </button>
                                <button class="btn btn-sm btn-outline-success" onclick="saveWeights()">
                                    <i class="bi bi-check-lg"></i> 保存配置
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <thead class="table-light">
                                        <tr>
                                            <th>因子名称</th>
                                            <th>因子类型</th>
                                            <th>当前权重</th>
                                            <th>权重调整</th>
                                            <th>贡献度</th>
                                            <th>操作</th>
                                        </tr>
                                    </thead>
                                    <tbody id="factorWeightTableBody">
                                        <tr>
                                            <td colspan="6" class="text-center text-muted py-5">
                                                <i class="bi bi-sliders display-4"></i>
                                                <p class="mt-3">正在加载因子权重数据...</p>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 权重分布图表 -->
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-pie-chart"></i> 权重分布饼图</h5>
                        </div>
                        <div class="card-body">
                            <div id="weightPieChart" style="height: 300px;">
                                <div class="text-center text-muted py-5">
                                    <i class="bi bi-pie-chart display-4"></i>
                                    <p class="mt-3">权重分布图表将在此显示</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-bar-chart"></i> 贡献度分析</h5>
                        </div>
                        <div class="card-body">
                            <div id="contributionBarChart" style="height: 300px;">
                                <div class="text-center text-muted py-5">
                                    <i class="bi bi-bar-chart display-4"></i>
                                    <p class="mt-3">贡献度分析图表将在此显示</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 加载初始数据
    loadFactorWeightData();
}

// 加载因子权重数据
function loadFactorWeightData() {
    const tableBody = document.getElementById('factorWeightTableBody');
    
    tableBody.innerHTML = `
        <tr>
            <td colspan="6" class="text-center py-4">
                <div class="spinner-border text-info" role="status">
                    <span class="visually-hidden">加载中...</span>
                </div>
                <p class="mt-2">正在获取因子权重数据...</p>
            </td>
        </tr>
    `;
    
    // 模拟API调用
    setTimeout(() => {
        const factorData = [
            {
                name: "财务指标",
                type: "定量因子",
                currentWeight: 25,
                contribution: 28.5,
                action: "调整"
            },
            {
                name: "成长性",
                type: "定量因子",
                currentWeight: 20,
                contribution: 22.3,
                action: "调整"
            },
            {
                name: "估值水平",
                type: "定量因子",
                currentWeight: 15,
                contribution: 18.7,
                action: "调整"
            },
            {
                name: "盈利能力",
                type: "定量因子",
                currentWeight: 12,
                contribution: 14.2,
                action: "调整"
            },
            {
                name: "行业前景",
                type: "定性因子",
                currentWeight: 10,
                contribution: 8.9,
                action: "调整"
            },
            {
                name: "管理团队",
                type: "定性因子",
                currentWeight: 8,
                contribution: 5.4,
                action: "调整"
            },
            {
                name: "市场地位",
                type: "定性因子",
                currentWeight: 6,
                contribution: 4.8,
                action: "调整"
            },
            {
                name: "创新能力",
                type: "定性因子",
                currentWeight: 4,
                contribution: 3.2,
                action: "调整"
            }
        ];
        
        let tableHTML = '';
        factorData.forEach(factor => {
            const weightColor = factor.currentWeight >= 20 ? 'success' : 
                              factor.currentWeight >= 10 ? 'warning' : 'info';
            const contributionColor = factor.contribution >= 20 ? 'success' : 
                                    factor.contribution >= 10 ? 'warning' : 'info';
            
            tableHTML += `
                <tr>
                    <td><strong>${factor.name}</strong></td>
                    <td><span class="badge bg-secondary">${factor.type}</span></td>
                    <td>
                        <span class="badge bg-${weightColor}">${factor.currentWeight}%</span>
                    </td>
                    <td>
                        <input type="range" class="form-range" min="0" max="30" value="${factor.currentWeight}" 
                               onchange="updateFactorWeight('${factor.name}', this.value)">
                        <small class="text-muted">${factor.currentWeight}%</small>
                    </td>
                    <td>
                        <div class="progress" style="height: 20px;">
                            <div class="progress-bar bg-${contributionColor}" role="progressbar" 
                                 style="width: ${factor.contribution}%">
                                ${factor.contribution}%
                            </div>
                        </div>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="analyzeFactor('${factor.name}')">
                            <i class="bi bi-graph-up"></i> 分析
                        </button>
                    </td>
                </tr>
            `;
        });
        
        tableBody.innerHTML = tableHTML;
    }, 1000);
}

// 更新因子权重
function updateFactorWeight(factorName, newWeight) {
    console.log(`更新因子 ${factorName} 的权重为: ${newWeight}%`);
    // 实际实现中这里应该调用API更新权重
}

// 分析因子
function analyzeFactor(factorName) {
    alert(`分析因子: ${factorName}`);
    // 实际实现中这里应该显示因子分析详情
}

// 重置权重
function resetWeights() {
    if (confirm('确定要重置所有因子权重为默认值吗？')) {
        const tableBody = document.getElementById('factorWeightTableBody');
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4">
                    <div class="spinner-border text-info" role="status">
                        <span class="visually-hidden">加载中...</span>
                    </div>
                    <p class="mt-2">正在重置权重配置...</p>
                </td>
            </tr>
        `;
        
        setTimeout(() => {
            loadFactorWeightData();
            alert('权重已重置为默认值');
        }, 800);
    }
}

// 保存权重配置
function saveWeights() {
    const tableBody = document.getElementById('factorWeightTableBody');
    const rows = tableBody.querySelectorAll('tr');
    
    let weights = {};
    rows.forEach(row => {
        const factorName = row.cells[0].textContent.trim();
        const weightInput = row.querySelector('input[type="range"]');
        if (weightInput) {
            weights[factorName] = parseInt(weightInput.value);
        }
    });
    
    // 显示保存状态
    tableBody.innerHTML = `
        <tr>
            <td colspan="6" class="text-center py-4">
                <div class="spinner-border text-success" role="status">
                    <span class="visually-hidden">加载中...</span>
                </div>
                <p class="mt-2">正在保存权重配置...</p>
            </td>
        </tr>
    `;
    
    setTimeout(() => {
        loadFactorWeightData();
        alert('权重配置已成功保存！');
        console.log('保存的权重配置:', weights);
    }, 1000);
}