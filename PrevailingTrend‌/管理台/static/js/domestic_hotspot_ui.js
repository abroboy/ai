/**
 * 国内热点数据模块 - UI构建部分
 */

// 构建国内热点模块HTML
function buildDomesticHotspotModuleHTML(hotspotData, stats) {
  return `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">国内热点数据 <span class="badge bg-danger">实时</span></h4>
      <div class="row">
        <div class="col-md-8">
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-light d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">国内财经热点</h5>
              <div class="btn-group">
                <button class="btn btn-sm btn-outline-primary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                  类别筛选
                </button>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="#" onclick="filterByCategory('all')">全部类别</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByCategory('货币政策')">货币政策</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByCategory('经济数据')">经济数据</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByCategory('资本市场')">资本市场</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByCategory('房地产')">房地产</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByCategory('金融科技')">金融科技</a></li>
                  <li><a class="dropdown-item" href="#" onclick="filterByCategory('产业发展')">产业发展</a></li>
                </ul>
              </div>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-hover table-striped mb-0">
                  <thead class="table-light">
                    <tr>
                      <th scope="col">ID</th>
                      <th scope="col">热点标题</th>
                      <th scope="col">来源</th>
                      <th scope="col">日期</th>
                      <th scope="col">影响力</th>
                      <th scope="col">区域</th>
                      <th scope="col">类别</th>
                    </tr>
                  </thead>
                  <tbody id="domestic-hotspot-table">
                    ${hotspotData.map(item => `
                      <tr>
                        <td>${item.id}</td>
                        <td><a href="#" class="text-decoration-none" onclick="showDomesticHotspotDetail(${item.id})">${item.title}</a></td>
                        <td>${item.source}</td>
                        <td>${item.date}</td>
                        <td>
                          <div class="progress" style="height: 6px;">
                            <div class="progress-bar bg-${getImpactColor(item.impact)}" role="progressbar" style="width: ${item.impact}%"></div>
                          </div>
                          <small class="text-muted">${item.impact}%</small>
                        </td>
                        <td><span class="badge bg-${getRegionColor(item.region)}">${item.region}</span></td>
                        <td>${item.category}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
            <div class="card-footer bg-light">
              <div class="d-flex justify-content-between align-items-center">
                <small class="text-muted">最后更新: <span id="domestic-hotspot-last-updated">${new Date().toLocaleString()}</span></small>
                <div>
                  <button class="btn btn-sm btn-primary" onclick="refreshDomesticHotspotData()">
                    <i class="bi bi-arrow-clockwise"></i> 刷新数据
                  </button>
                  <button class="btn btn-sm btn-outline-secondary" onclick="exportDomesticHotspotData()">
                    <i class="bi bi-download"></i> 导出
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">类别分布</h5>
            </div>
            <div class="card-body">
              <div id="category-chart" style="height: 300px;"></div>
            </div>
          </div>
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">国内热点监测</h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-primary mb-0">${stats.total_count || 0}</h3>
                    <small class="text-muted">今日热点</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-success mb-0">${Object.keys(stats.categories || {}).length}</h3>
                    <small class="text-muted">类别覆盖</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-danger mb-0">${stats.high_impact_count || 0}</h3>
                    <small class="text-muted">高影响力</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="border rounded p-3 text-center">
                    <h3 class="text-warning mb-0">${Math.round(stats.avg_impact || 0)}</h3>
                    <small class="text-muted">平均影响力</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 热点详情模态框 -->
      <div class="modal fade" id="domesticHotspotDetailModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="domesticHotspotDetailTitle">热点详情</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="domesticHotspotDetailContent">
              <!-- 详情内容将通过JS动态填充 -->
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
              <button type="button" class="btn btn-primary">生成分析报告</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}