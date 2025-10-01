/**
 * 雪球等论坛热点数据模块
 * 提供雪球论坛热点数据的展示和分析功能
 */

// 全局变量
let xueqiuHotspotData = null;
let currentPage = 1;
const itemsPerPage = 10;

// 初始化雪球热点数据模块
function initXueqiuHotspotModule() {
    console.log('初始化雪球热点数据模块...');
    
    // 创建模块HTML结构
    createXueqiuHotspotHTML();
    
    // 加载数据
    loadXueqiuHotspotData();
    
    // 绑定事件
    bindXueqiuHotspotEvents();
}

// 创建雪球热点数据HTML结构
function createXueqiuHotspotHTML() {
    const container = document.querySelector('.main');
    if (!container) return;
    
    container.innerHTML = `
        <div class="xueqiu-hotspot-container">
            <!-- 头部标题 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h4 class="mb-0">
                                <i class="bi bi-chat-dots"></i> 雪球等论坛热点数据
                                <span class="badge bg-success ms-2">实时更新</span>
                            </h4>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 控制面板 -->
            <div class="control-panel mb-4">
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <div class="btn-group" role="group">
                            <button type="button" class="btn btn-outline-primary active" data-view="topics">
                                <i class="bi bi-chat-text"></i> 热点话题
                            </button>
                            <button type="button" class="btn btn-outline-primary" data-view="stocks">
                                <i class="bi bi-graph-up"></i> 热门股票
                            </button>
                            <button type="button" class="btn btn-outline-primary" data-view="sentiment">
                                <i class="bi bi-emoji-smile"></i> 市场情绪
                            </button>
                        </div>
                    </div>
                    <div class="col-md-6 text-end">
                        <button class="btn btn-success btn-sm" onclick="refreshXueqiuData()">
                            <i class="bi bi-arrow-clockwise"></i> 刷新数据
                        </button>
                        <button class="btn btn-info btn-sm" onclick="exportXueqiuData()">
                            <i class="bi bi-download"></i> 导出数据
                        </button>
                    </div>
                </div>
            </div>

            <!-- 数据概览卡片 -->
            <div class="overview-cards mb-4">
                <div class="row">
                    <div class="col-md-3">
                        <div class="card text-center overview-card">
                            <div class="card-body">
                                <div class="overview-icon text-primary">
                                    <i class="bi bi-chat-dots"></i>
                                </div>
                                <h3 id="total-topics">-</h3>
                                <p class="text-muted mb-0">热点话题</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center overview-card">
                            <div class="card-body">
                                <div class="overview-icon text-success">
                                    <i class="bi bi-graph-up"></i>
                                </div>
                                <h3 id="trending-stocks">-</h3>
                                <p class="text-muted mb-0">热门股票</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center overview-card">
                            <div class="card-body">
                                <div class="overview-icon text-warning">
                                    <i class="bi bi-emoji-smile"></i>
                                </div>
                                <h3 id="sentiment-score">-</h3>
                                <p class="text-muted mb-0">情绪指数</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center overview-card">
                            <div class="card-body">
                                <div class="overview-icon text-info">
                                    <i class="bi bi-eye"></i>
                                </div>
                                <h3 id="total-views">-</h3>
                                <p class="text-muted mb-0">总浏览量</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 主要内容区域 -->
            <div class="main-content">
                <!-- 热点话题视图 -->
                <div id="topics-view" class="content-view">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">热点话题列表</h5>
                        </div>
                        <div class="card-body">
                            <div id="topics-list" class="topics-list">
                                <!-- 话题列表将在这里动态生成 -->
                            </div>
                            <div id="topics-pagination" class="pagination-container">
                                <!-- 分页将在这里生成 -->
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 热门股票视图 -->
                <div id="stocks-view" class="content-view" style="display: none;">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">热门股票排行</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-striped table-hover">
                                    <thead class="table-dark">
                                        <tr>
                                            <th>排名</th>
                                            <th>股票代码</th>
                                            <th>股票名称</th>
                                            <th>当前价格</th>
                                            <th>涨跌幅</th>
                                            <th>成交量</th>
                                            <th>讨论热度</th>
                                            <th>情绪指数</th>
                                        </tr>
                                    </thead>
                                    <tbody id="stocks-table-body">
                                        <!-- 股票数据将在这里动态生成 -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 市场情绪视图 -->
                <div id="sentiment-view" class="content-view" style="display: none;">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header">
                                    <h5 class="mb-0">情绪分布</h5>
                                </div>
                                <div class="card-body">
                                    <canvas id="sentiment-chart" width="400" height="300"></canvas>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header">
                                    <h5 class="mb-0">关键词趋势</h5>
                                </div>
                                <div class="card-body">
                                    <canvas id="keywords-chart" width="400" height="300"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 加载指示器 -->
            <div id="loading-indicator" class="text-center" style="display: none;">
                <div class="loading-indicator"></div>
                <p class="mt-2">正在加载数据...</p>
            </div>
        </div>
    `;
}