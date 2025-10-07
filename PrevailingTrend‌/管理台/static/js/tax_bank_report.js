// 税银报告模块 - 完整实现
function loadTaxBankReport() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-file-text text-success"></i> 税银报告分析</h2>
                    <p class="text-muted">企业税收数据与银行信贷信息综合分析</p>
                </div>
            </div>
            
            <!-- 企业选择面板 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <label class="form-label">企业名称</label>
                                    <input type="text" class="form-control" id="companyName" placeholder="输入企业名称" value="比亚迪股份有限公司">
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">报告类型</label>
                                    <select class="form-select" id="reportType">
                                        <option value="tax">税务报告</option>
                                        <option value="bank">银行报告</option>
                                        <option value="combined" selected>综合报告</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">时间范围</label>
                                    <select class="form-select" id="timeRange">
                                        <option value="current">当前年度</option>
                                        <option value="last" selected>近三年</option>
                                        <option value="all">全部年度</option>
                                    </select>
                                </div>
                                <div class="col-md-2 d-flex align-items-end">
                                    <button class="btn btn-primary w-100" onclick="generateTaxBankReport()">
                                        <i class="bi bi-search"></i> 生成报告
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 税务数据分析 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-calculator"></i> 税务数据分析</h5>
                        </div>
                        <div class="card-body" id="taxAnalysis">
                            <div class="text-center text-muted py-5">
                                <i class="bi bi-calculator display-4"></i>
                                <p class="mt-3">请选择企业并生成报告</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 银行信贷分析 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-bank"></i> 银行信贷分析</h5>
                        </div>
                        <div class="card-body" id="bankAnalysis">
                            <div class="text-center text-muted py-5">
                                <i class="bi bi-bank display-4"></i>
                                <p class="mt-3">银行信贷信息将在此显示</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 综合评估 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-graph-up"></i> 综合评估</h5>
                        </div>
                        <div class="card-body" id="comprehensiveAssessment">
                            <div class="text-center text-muted py-5">
                                <i class="bi bi-graph-up display-4"></i>
                                <p class="mt-3">综合评估结果将在此显示</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 生成税银报告
function generateTaxBankReport() {
    const companyName = document.getElementById('companyName').value;
    const reportType = document.getElementById('reportType').value;
    const timeRange = document.getElementById('timeRange').value;
    
    if (!companyName.trim()) {
        alert('请输入企业名称');
        return;
    }
    
    // 显示加载状态
    document.getElementById('taxAnalysis').innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-success" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-2">正在生成税银报告...</p>
        </div>
    `;
    
    // 模拟API调用
    setTimeout(() => {
        // 模拟税务数据分析
        const taxAnalysis = `
            <div class="row">
                <div class="col-md-6">
                    <h6>近三年纳税情况（万元）</h6>
                    <table class="table table-sm table-bordered">
                        <thead class="table-light">
                            <tr>
                                <th>年度</th>
                                <th>增值税</th>
                                <th>企业所得税</th>
                                <th>其他税种</th>
                                <th>合计</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>2024</td>
                                <td>1,245.6</td>
                                <td>892.3</td>
                                <td>156.8</td>
                                <td><strong>2,294.7</strong></td>
                            </tr>
                            <tr>
                                <td>2023</td>
                                <td>1,087.2</td>
                                <td>765.4</td>
                                <td>142.1</td>
                                <td><strong>1,994.7</strong></td>
                            </tr>
                            <tr>
                                <td>2022</td>
                                <td>923.8</td>
                                <td>654.9</td>
                                <td>128.3</td>
                                <td><strong>1,707.0</strong></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="col-md-6">
                    <h6>税务风险评估</h6>
                    <div class="alert alert-success">
                        <i class="bi bi-check-circle"></i> <strong>税务合规性：优秀</strong>
                        <p class="mb-0 mt-2">企业纳税记录良好，无重大税务违规记录</p>
                    </div>
                    <div class="alert alert-info">
                        <i class="bi bi-info-circle"></i> <strong>税收优惠：正常享受</strong>
                        <p class="mb-0 mt-2">符合高新技术企业税收优惠政策</p>
                    </div>
                </div>
            </div>
        `;
        
        // 模拟银行信贷分析
        const bankAnalysis = `
            <div class="row">
                <div class="col-md-6">
                    <h6>银行授信情况</h6>
                    <table class="table table-sm table-bordered">
                        <thead class="table-light">
                            <tr>
                                <th>银行名称</th>
                                <th>授信额度（万元）</th>
                                <th>已使用额度</th>
                                <th>利率</th>
                                <th>状态</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>工商银行</td>
                                <td>50,000</td>
                                <td>28,500</td>
                                <td>4.35%</td>
                                <td><span class="badge bg-success">正常</span></td>
                            </tr>
                            <tr>
                                <td>建设银行</td>
                                <td>30,000</td>
                                <td>15,200</td>
                                <td>4.25%</td>
                                <td><span class="badge bg-success">正常</span></td>
                            </tr>
                            <tr>
                                <td>招商银行</td>
                                <td>20,000</td>
                                <td>8,700</td>
                                <td>4.15%</td>
                                <td><span class="badge bg-success">正常</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="col-md-6">
                    <h6>信贷风险评估</h6>
                    <div class="alert alert-success">
                        <i class="bi bi-shield-check"></i> <strong>信用评级：AAA</strong>
                        <p class="mb-0 mt-2">企业信用状况良好，还款记录正常</p>
                    </div>
                    <div class="alert alert-warning">
                        <i class="bi bi-exclamation-triangle"></i> <strong>负债率：65.2%</strong>
                        <p class="mb-0 mt-2">负债率略高，需关注现金流状况</p>
                    </div>
                </div>
            </div>
        `;
        
        // 模拟综合评估
        const comprehensiveAssessment = `
            <div class="row">
                <div class="col-md-4">
                    <div class="card border-success">
                        <div class="card-body text-center">
                            <div class="text-success">
                                <i class="bi bi-award display-4"></i>
                                <h5 class="mt-2">综合评分</h5>
                                <h3 class="text-success">88.5</h3>
                                <p class="mb-0">良好</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-8">
                    <h6>评估维度</h6>
                    <div class="progress mb-2" style="height: 20px;">
                        <div class="progress-bar bg-success" role="progressbar" style="width: 92%">税务合规性 92%</div>
                    </div>
                    <div class="progress mb-2" style="height: 20px;">
                        <div class="progress-bar bg-info" role="progressbar" style="width: 85%">银行信用 85%</div>
                    </div>
                    <div class="progress mb-2" style="height: 20px;">
                        <div class="progress-bar bg-warning" role="progressbar" style="width: 76%">财务健康度 76%</div>
                    </div>
                    <div class="progress mb-2" style="height: 20px;">
                        <div class="progress-bar bg-primary" role="progressbar" style="width: 89%">经营稳定性 89%</div>
                    </div>
                </div>
            </div>
            <div class="mt-3">
                <h6>评估建议：</h6>
                <ul>
                    <li>企业税务合规性良好，可继续保持</li>
                    <li>银行信用状况优秀，融资能力较强</li>
                    <li>建议关注负债率，优化财务结构</li>
                    <li>经营稳定性较好，具备持续发展能力</li>
                </ul>
            </div>
        `;
        
        // 根据报告类型显示相应信息
        if (reportType === 'tax' || reportType === 'combined') {
            document.getElementById('taxAnalysis').innerHTML = taxAnalysis;
        }
        
        if (reportType === 'bank' || reportType === 'combined') {
            document.getElementById('bankAnalysis').innerHTML = bankAnalysis;
        }
        
        if (reportType === 'combined') {
            document.getElementById('comprehensiveAssessment').innerHTML = comprehensiveAssessment;
        }
        
    }, 1500);
}