/**
 * 财务三表模块
 * 大势所趋风险框架管理台
 */

// 加载财务三表模块
function loadFinancialStatements() {
    const container = document.getElementById('content');
    
    // 显示加载状态
    container.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-3">正在加载财务三表数据...</p>
        </div>
    `;

    // 获取数据并渲染
    fetchFinancialStatementsData()
        .then(data => {
            if (data.success) {
                renderFinancialStatementsModule(container, data);
            } else {
                throw new Error(data.message || '数据加载失败');
            }
        })
        .catch(error => {
            container.innerHTML = `
                <div class="alert alert-danger">
                    <h5><i class="bi bi-exclamation-triangle"></i> 数据加载失败</h5>
                    <p>${error.message}</p>
                    <button class="btn btn-primary" onclick="loadFinancialStatements()">重新加载</button>
                </div>
            `;
        });
}

// 获取财务三表数据
async function fetchFinancialStatementsData() {
    try {
        // TODO: 实际API调用
        // const response = await fetch('/api/financial-statements');
        // return await response.json();
        
        // 暂时返回模拟数据
        return getMockFinancialStatementsData();
    } catch (error) {
        console.error('获取财务三表数据失败:', error);
        return getMockFinancialStatementsData();
    }
}

// 模拟财务三表数据
function getMockFinancialStatementsData() {
    return {
        success: true,
        data: {
            company: {
                code: '000001.SZ',
                name: '平安银行',
                industry: '银行业'
            },
            balanceSheet: {
                title: '资产负债表',
                period: '2023年度',
                assets: [
                    { name: '现金及央行存款', value: 2856.78 },
                    { name: '发放贷款和垫款', value: 28567.89 },
                    { name: '交易性金融资产', value: 3456.78 },
                    { name: '债权投资', value: 4567.89 },
                    { name: '固定资产', value: 234.56 },
                    { name: '其他资产', value: 567.89 }
                ],
                liabilities: [
                    { name: '吸收存款', value: 32567.89 },
                    { name: '应付债券', value: 2345.67 },
                    { name: '同业存放', value: 2345.67 },
                    { name: '其他负债', value: 1234.56 }
                ],
                equity: [
                    { name: '股本', value: 194.41 },
                    { name: '资本公积', value: 1456.78 },
                    { name: '未分配利润', value: 1147.15 },
                    { name: '其他权益', value: 703.68 }
                ]
            },
            incomeStatement: {
                title: '利润表',
                period: '2023年度',
                revenue: [
                    { name: '利息净收入', value: 1234.56 },
                    { name: '手续费及佣金净收入', value: 456.78 },
                    { name: '投资收益', value: 234.56 },
                    { name: '其他收入', value: 237.01 }
                ],
                expenses: [
                    { name: '业务及管理费', value: 789.12 },
                    { name: '信用减值损失', value: 456.78 },
                    { name: '税金及附加', value: 23.45 }
                ],
                profit: [
                    { name: '营业利润', value: 858.99 },
                    { name: '利润总额', value: 867.34 },
                    { name: '净利润', value: 650.51 }
                ]
            },
            cashFlowStatement: {
                title: '现金流量表',
                period: '2023年度',
                operating: [
                    { name: '经营活动现金流入', value: 5147.11 },
                    { name: '经营活动现金流出', value: 4892.33 },
                    { name: '经营活动净现金流', value: 254.78 }
                ],
                investing: [
                    { name: '投资活动现金流入', value: 1234.56 },
                    { name: '投资活动现金流出', value: 1456.78 },
                    { name: '投资活动净现金流', value: -222.22 }
                ],
                financing: [
                    { name: '筹资活动现金流入', value: 2345.67 },
                    { name: '筹资活动现金流出', value: 2123.45 },
                    { name: '筹资活动净现金流', value: 222.22 }
                ]
            }
        }
    };
}

// 渲染财务三表模块
function renderFinancialStatementsModule(container, data) {
    const { company, balanceSheet, incomeStatement, cashFlowStatement } = data.data;
    
    const moduleHTML = `
        <div class="financial-statements-module">
            <!-- 模块标题 -->
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h4><i class="bi bi-file-earmark-spreadsheet text-success"></i> 财务三表</h4>
                <div>
                    <span class="badge bg-info">${company.name} (${company.code})</span>
                    <button class="btn btn-outline-primary btn-sm ms-2" onclick="refreshFinancialStatements()">
                        <i class="bi bi-arrow-clockwise"></i> 刷新
                    </button>
                </div>
            </div>

            <!-- 公司信息 -->
            <div class="card mb-4">
                <div class="card-body">
                    <h5>${company.name} 财务报表概览</h5>
                    <p class="text-muted">股票代码: ${company.code} | 行业: ${company.industry} | 报告期: ${balanceSheet.period}</p>
                </div>
            </div>

            <!-- 三表导航 -->
            <ul class="nav nav-tabs mb-4" id="financialTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="balance-tab" data-bs-toggle="tab" data-bs-target="#balance" type="button">
                        <i class="bi bi-bar-chart"></i> 资产负债表
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="income-tab" data-bs-toggle="tab" data-bs-target="#income" type="button">
                        <i class="bi bi-graph-up"></i> 利润表
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="cashflow-tab" data-bs-toggle="tab" data-bs-target="#cashflow" type="button">
                        <i class="bi bi-cash-stack"></i> 现金流量表
                    </button>
                </li>
            </ul>

            <!-- 三表内容 -->
            <div class="tab-content" id="financialTabContent">
                <!-- 资产负债表 -->
                <div class="tab-pane fade show active" id="balance" role="tabpanel">
                    ${renderBalanceSheet(balanceSheet)}
                </div>
                
                <!-- 利润表 -->
                <div class="tab-pane fade" id="income" role="tabpanel">
                    ${renderIncomeStatement(incomeStatement)}
                </div>
                
                <!-- 现金流量表 -->
                <div class="tab-pane fade" id="cashflow" role="tabpanel">
                    ${renderCashFlowStatement(cashFlowStatement)}
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = moduleHTML;
}

// 渲染资产负债表
function renderBalanceSheet(data) {
    const assetsTotal = data.assets.reduce((sum, item) => sum + item.value, 0);
    const liabilitiesTotal = data.liabilities.reduce((sum, item) => sum + item.value, 0);
    const equityTotal = data.equity.reduce((sum, item) => sum + item.value, 0);
    
    return `
        <div class="row">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h6><i class="bi bi-plus-circle"></i> 资产</h6>
                    </div>
                    <div class="card-body">
                        ${data.assets.map(item => `
                            <div class="d-flex justify-content-between mb-2">
                                <span>${item.name}</span>
                                <strong>${item.value.toFixed(2)}亿</strong>
                            </div>
                        `).join('')}
                        <hr>
                        <div class="d-flex justify-content-between">
                            <strong>资产总计</strong>
                            <strong class="text-primary">${assetsTotal.toFixed(2)}亿</strong>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header bg-danger text-white">
                        <h6><i class="bi bi-dash-circle"></i> 负债</h6>
                    </div>
                    <div class="card-body">
                        ${data.liabilities.map(item => `
                            <div class="d-flex justify-content-between mb-2">
                                <span>${item.name}</span>
                                <strong>${item.value.toFixed(2)}亿</strong>
                            </div>
                        `).join('')}
                        <hr>
                        <div class="d-flex justify-content-between">
                            <strong>负债总计</strong>
                            <strong class="text-danger">${liabilitiesTotal.toFixed(2)}亿</strong>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h6><i class="bi bi-wallet2"></i> 所有者权益</h6>
                    </div>
                    <div class="card-body">
                        ${data.equity.map(item => `
                            <div class="d-flex justify-content-between mb-2">
                                <span>${item.name}</span>
                                <strong>${item.value.toFixed(2)}亿</strong>
                            </div>
                        `).join('')}
                        <hr>
                        <div class="d-flex justify-content-between">
                            <strong>权益总计</strong>
                            <strong class="text-success">${equityTotal.toFixed(2)}亿</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 渲染利润表
function renderIncomeStatement(data) {
    const revenueTotal = data.revenue.reduce((sum, item) => sum + item.value, 0);
    const expensesTotal = data.expenses.reduce((sum, item) => sum + item.value, 0);
    
    return `
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h6><i class="bi bi-arrow-up-circle"></i> 收入</h6>
                    </div>
                    <div class="card-body">
                        ${data.revenue.map(item => `
                            <div class="d-flex justify-content-between mb-2">
                                <span>${item.name}</span>
                                <strong>${item.value.toFixed(2)}亿</strong>
                            </div>
                        `).join('')}
                        <hr>
                        <div class="d-flex justify-content-between">
                            <strong>收入总计</strong>
                            <strong class="text-success">${revenueTotal.toFixed(2)}亿</strong>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-warning text-white">
                        <h6><i class="bi bi-arrow-down-circle"></i> 费用</h6>
                    </div>
                    <div class="card-body">
                        ${data.expenses.map(item => `
                            <div class="d-flex justify-content-between mb-2">
                                <span>${item.name}</span>
                                <strong>${item.value.toFixed(2)}亿</strong>
                            </div>
                        `).join('')}
                        <hr>
                        <div class="d-flex justify-content-between">
                            <strong>费用总计</strong>
                            <strong class="text-warning">${expensesTotal.toFixed(2)}亿</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h6><i class="bi bi-calculator"></i> 利润情况</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            ${data.profit.map(item => `
                                <div class="col-md-4">
                                    <div class="text-center">
                                        <h4 class="text-info">${item.value.toFixed(2)}亿</h4>
                                        <p class="mb-0">${item.name}</p>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 渲染现金流量表
function renderCashFlowStatement(data) {
    return `
        <div class="row">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h6><i class="bi bi-briefcase"></i> 经营活动</h6>
                    </div>
                    <div class="card-body">
                        ${data.operating.map(item => `
                            <div class="d-flex justify-content-between mb-2">
                                <span>${item.name}</span>
                                <strong class="${item.value >= 0 ? 'text-success' : 'text-danger'}">
                                    ${item.value.toFixed(2)}亿
                                </strong>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h6><i class="bi bi-graph-up"></i> 投资活动</h6>
                    </div>
                    <div class="card-body">
                        ${data.investing.map(item => `
                            <div class="d-flex justify-content-between mb-2">
                                <span>${item.name}</span>
                                <strong class="${item.value >= 0 ? 'text-success' : 'text-danger'}">
                                    ${item.value.toFixed(2)}亿
                                </strong>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header bg-warning text-white">
                        <h6><i class="bi bi-bank"></i> 筹资活动</h6>
                    </div>
                    <div class="card-body">
                        ${data.financing.map(item => `
                            <div class="d-flex justify-content-between mb-2">
                                <span>${item.name}</span>
                                <strong class="${item.value >= 0 ? 'text-success' : 'text-danger'}">
                                    ${item.value.toFixed(2)}亿
                                </strong>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 刷新财务三表数据
function refreshFinancialStatements() {
    loadFinancialStatements();
}

// 导出模块函数
if (typeof window !== 'undefined') {
    window.loadFinancialStatements = loadFinancialStatements;
    window.refreshFinancialStatements = refreshFinancialStatements;
}