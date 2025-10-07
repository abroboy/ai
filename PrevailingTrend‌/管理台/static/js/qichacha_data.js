// 企查查数据模块 - 完整实现
function loadQichachaData() {
    const container = document.getElementById('content');
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-building text-primary"></i> 企查查企业信息</h2>
                    <p class="text-muted">企业基本信息、股权结构、风险监控一站式查询</p>
                </div>
            </div>
            
            <!-- 搜索面板 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-4">
                                    <label class="form-label">企业名称/统一社会信用代码</label>
                                    <input type="text" class="form-control" id="companySearch" placeholder="输入企业名称或代码" value="比亚迪股份有限公司">
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">查询类型</label>
                                    <select class="form-select" id="queryType">
                                        <option value="basic">基本信息</option>
                                        <option value="equity">股权结构</option>
                                        <option value="risk">风险信息</option>
                                        <option value="all" selected>全部信息</option>
                                    </select>
                                </div>
                                <div class="col-md-2 d-flex align-items-end">
                                    <button class="btn btn-primary w-100" onclick="searchCompany()">
                                        <i class="bi bi-search"></i> 查询
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 企业基本信息 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-info-circle"></i> 企业基本信息</h5>
                        </div>
                        <div class="card-body" id="companyBasicInfo">
                            <div class="text-center text-muted py-5">
                                <i class="bi bi-building display-4"></i>
                                <p class="mt-3">请输入企业名称进行查询</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 股权结构 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-diagram-3"></i> 股权结构</h5>
                        </div>
                        <div class="card-body" id="equityStructure">
                            <div class="text-center text-muted py-5">
                                <i class="bi bi-diagram-3 display-4"></i>
                                <p class="mt-3">股权结构信息将在此显示</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 风险信息 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-exclamation-triangle"></i> 风险监控</h5>
                        </div>
                        <div class="card-body" id="riskInfo">
                            <div class="text-center text-muted py-5">
                                <i class="bi bi-exclamation-triangle display-4"></i>
                                <p class="mt-3">风险监控信息将在此显示</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 搜索企业信息
function searchCompany() {
    const companyName = document.getElementById('companySearch').value;
    const queryType = document.getElementById('queryType').value;
    
    if (!companyName.trim()) {
        alert('请输入企业名称');
        return;
    }
    
    // 显示加载状态
    document.getElementById('companyBasicInfo').innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-2">正在查询企业信息...</p>
        </div>
    `;
    
    // 模拟API调用
    setTimeout(() => {
        // 模拟企业基本信息
        const basicInfo = `
            <div class="row">
                <div class="col-md-6">
                    <table class="table table-sm">
                        <tr><td><strong>企业名称</strong></td><td>${companyName}</td></tr>
                        <tr><td><strong>统一社会信用代码</strong></td><td>914403001922038216</td></tr>
                        <tr><td><strong>法定代表人</strong></td><td>王传福</td></tr>
                        <tr><td><strong>注册资本</strong></td><td>291.14亿元</td></tr>
                        <tr><td><strong>成立日期</strong></td><td>1995-02-10</td></tr>
                    </table>
                </div>
                <div class="col-md-6">
                    <table class="table table-sm">
                        <tr><td><strong>企业类型</strong></td><td>股份有限公司(上市)</td></tr>
                        <tr><td><strong>所属行业</strong></td><td>汽车制造业</td></tr>
                        <tr><td><strong>注册地址</strong></td><td>广东省深圳市坪山区比亚迪路3009号</td></tr>
                        <tr><td><strong>经营状态</strong></td><td><span class="badge bg-success">在业</span></td></tr>
                        <tr><td><strong>经营范围</strong></td><td>汽车、电动车及其零部件的研发、生产和销售等</td></tr>
                    </table>
                </div>
            </div>
        `;
        
        // 模拟股权结构
        const equityInfo = `
            <div class="table-responsive">
                <table class="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th>股东名称</th>
                            <th>持股比例</th>
                            <th>认缴出资额</th>
                            <th>股东类型</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>香港中央结算有限公司</td>
                            <td>28.74%</td>
                            <td>83.68亿股</td>
                            <td>境外法人</td>
                        </tr>
                        <tr>
                            <td>王传福</td>
                            <td>17.64%</td>
                            <td>51.36亿股</td>
                            <td>自然人</td>
                        </tr>
                        <tr>
                            <td>吕向阳</td>
                            <td>7.03%</td>
                            <td>20.46亿股</td>
                            <td>自然人</td>
                        </tr>
                        <tr>
                            <td>夏佐全</td>
                            <td>2.84%</td>
                            <td>8.27亿股</td>
                            <td>自然人</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
        
        // 模拟风险信息
        const riskInfo = `
            <div class="row">
                <div class="col-md-4">
                    <div class="card border-0">
                        <div class="card-body text-center">
                            <div class="text-success">
                                <i class="bi bi-check-circle display-4"></i>
                                <h5 class="mt-2">经营风险</h5>
                                <p class="mb-0">低风险</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0">
                        <div class="card-body text-center">
                            <div class="text-warning">
                                <i class="bi bi-exclamation-triangle display-4"></i>
                                <h5 class="mt-2">司法风险</h5>
                                <p class="mb-0">中风险</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0">
                        <div class="card-body text-center">
                            <div class="text-success">
                                <i class="bi bi-shield-check display-4"></i>
                                <h5 class="mt-2">信用风险</h5>
                                <p class="mb-0">低风险</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mt-3">
                <h6>风险详情：</h6>
                <ul>
                    <li>经营异常记录：0条</li>
                    <li>行政处罚记录：2条</li>
                    <li>司法诉讼记录：15条</li>
                    <li>股权冻结记录：0条</li>
                </ul>
            </div>
        `;
        
        // 根据查询类型显示相应信息
        if (queryType === 'basic' || queryType === 'all') {
            document.getElementById('companyBasicInfo').innerHTML = basicInfo;
        }
        
        if (queryType === 'equity' || queryType === 'all') {
            document.getElementById('equityStructure').innerHTML = equityInfo;
        }
        
        if (queryType === 'risk' || queryType === 'all') {
            document.getElementById('riskInfo').innerHTML = riskInfo;
        }
        
    }, 1000);
}