// 腾讯济安指数模块 - 完整实现（集成API）
function loadTencentJianIndex() {
    const container = document.getElementById('content');
    
    // 显示加载状态
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-graph-up text-success"></i> 腾讯济安指数分析</h2>
                    <p class="text-muted">腾讯济安指数实时数据与投资策略分析</p>
                </div>
            </div>
            
            <!-- 加载指示器 -->
            <div class="row">
                <div class="col-12 text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">加载中...</span>
                    </div>
                    <p class="mt-3">正在加载腾讯济安指数数据...</p>
                </div>
            </div>
        </div>
    `;
    
    // 调用API获取数据
    fetch('/api/tencent-jian-index')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderTencentJianIndex(data.data);
            } else {
                throw new Error(data.message || '获取数据失败');
            }
        })
        .catch(error => {
            console.error('加载腾讯济安指数数据失败:', error);
            container.innerHTML = `
                <div class="container-fluid">
                    <div class="row mb-4">
                        <div class="col-12">
                            <h2><i class="bi bi-graph-up text-success"></i> 腾讯济安指数分析</h2>
                            <p class="text-muted">腾讯济安指数实时数据与投资策略分析</p>
                        </div>
                    </div>
                    <div class="alert alert-danger">
                        <h5><i class="bi bi-exclamation-triangle"></i> 数据加载失败</h5>
                        <p>${error.message}</p>
                        <button class="btn btn-primary btn-sm" onclick="loadTencentJianIndex()">
                            <i class="bi bi-arrow-clockwise"></i> 重新加载
                        </button>
                    </div>
                </div>
            `;
        });
}

// 渲染腾讯济安指数数据
function renderTencentJianIndex(data) {
    const container = document.getElementById('content');
    const indexData = data.index;
    const constituents = data.constituents;
    const industryDistribution = data.industry_distribution;
    
    // 计算涨跌幅颜色
    const changeClass = indexData.change_percent >= 0 ? 'text-success' : 'text-danger';
    const changeSign = indexData.change_percent >= 0 ? '+' : '';
    
    container.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-4">
                <div class="col-12">
                    <h2><i class="bi bi-graph-up text-success"></i> 腾讯济安指数分析</h2>
                    <p class="text-muted">腾讯济安指数实时数据与投资策略分析</p>
                </div>
            </div>
            
            <!-- 指数概览 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h4>${indexData.current_index.toLocaleString()}</h4>
                            <p class="mb-0">当前指数</p>
                            <small class="${changeClass}">${changeSign}${indexData.change_percent}% (+${indexData.change})</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h4>${indexData.constituent_count}</h4>
                            <p class="mb-0">成分股数量</p>
                            <small>覆盖主要行业</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h4>${(indexData.market_cap / 100000000).toFixed(1)}亿</h4>
                            <p class="mb-0">总市值</p>
                            <small>人民币</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h4>${indexData.dividend_yield}%</h4>
                            <p class="mb-0">股息率</p>
                            <small>年化收益率</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 成分股分析 -->
            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-list-ul"></i> 权重前十成分股</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>股票代码</th>
                                            <th>股票名称</th>
                                            <th>权重</th>
                                            <th>当前价</th>
                                            <th>涨跌幅</th>
                                            <th>贡献度</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${constituents.map(stock => {
                                            const changeClass = stock.change_percent >= 0 ? 'text-success' : 'text-danger';
                                            const changeSign = stock.change_percent >= 0 ? '+' : '';
                                            const contributionClass = stock.contribution >= 0 ? 'text-success' : 'text-danger';
                                            const contributionSign = stock.contribution >= 0 ? '+' : '';
                                            
                                            return `
                                                <tr>
                                                    <td>${stock.code}</td>
                                                    <td>${stock.name}</td>
                                                    <td>${stock.weight}%</td>
                                                    <td>${stock.price}</td>
                                                    <td class="${changeClass}">${changeSign}${stock.change_percent}%</td>
                                                    <td class="${contributionClass}">${contributionSign}${stock.contribution}</td>
                                                </tr>
                                            `;
                                        }).join('')}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-pie-chart"></i> 行业分布</h5>
                        </div>
                        <div class="card-body">
                            ${industryDistribution.map(industry => `
                                <div class="mb-3">
                                    <div class="d-flex justify-content-between">
                                        <span>${industry.industry}</span>
                                        <span>${industry.weight}%</span>
                                    </div>
                                    <div class="progress mb-2">
                                        <div class="progress-bar" style="width: ${industry.weight}%"></div>
                                    </div>
                                    <small class="text-muted">${industry.count}家公司</small>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 统计信息 -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="bi bi-bar-chart"></i> 指数统计信息</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="text-center">
                                        <h4 class="${data.statistics.avg_change >= 0 ? 'text-success' : 'text-danger'}">
                                            ${data.statistics.avg_change >= 0 ? '+' : ''}${data.statistics.avg_change}%
                                        </h4>
                                        <p class="text-muted">平均涨跌幅</p>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="text-center">
                                        <h4 class="text-success">${data.statistics.positive_count}</h4>
                                        <p class="text-muted">上涨股票</p>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="text-center">
                                        <h4 class="text-danger">${data.statistics.negative_count}</h4>
                                        <p class="text-muted">下跌股票</p>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="text-center">
                                        <h4 class="text-warning">${data.statistics.neutral_count}</h4>
                                        <p class="text-muted">平盘股票</p>
                                    </div>
                                </div>
                            </div>
                            <div class="row mt-3">
                                <div class="col-md-6">
                                    <p><strong>最大贡献股:</strong> ${data.statistics.top_contributor}</p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>最大拖累股:</strong> ${data.statistics.bottom_contributor}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 刷新按钮 -->
            <div class="row mt-4">
                <div class="col-12 text-center">
                    <button class="btn btn-primary" onclick="loadTencentJianIndex()">
                        <i class="bi bi-arrow-clockwise"></i> 刷新数据
                    </button>
                    <small class="text-muted d-block mt-2">最后更新: ${new Date().toLocaleString('zh-CN')}</small>
                </div>
            </div>
        </div>
    `;
}

// 导出函数
if (typeof window !== 'undefined') {
    window.loadTencentJianIndex = loadTencentJianIndex;
}