/**
 * 企查查数据模块
 * 大势所趋风险框架管理台 - 第三层模块
 */

// 加载企查查数据模块
function loadQichachaData() {
  const contentArea = document.getElementById('content');
  
  // 显示加载中状态
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载企查查数据...</p>
    </div>
  `;
  
  // 模拟API请求延迟
  setTimeout(() => {
    // 加载模块内容
    renderQichachaDataModule(contentArea);
  }, 800);
}

// 渲染企查查数据模块内容
function renderQichachaDataModule(container) {
  // 模拟企查查数据
  const qichachaData = {
    companyName: "示例科技有限公司",
    regNumber: "91310101MA1FPX1234",
    legalPerson: "张三",
    regCapital: "1000万元人民币",
    establishDate: "2018-05-20",
    status: "存续",
    industry: "科技推广和应用服务业",
    address: "上海市浦东新区张江高科技园区",
    shareholders: [
      { name: "张三", ratio: "40%", type: "自然人" },
      { name: "李四", ratio: "30%", type: "自然人" },
      { name: "北京投资有限公司", ratio: "30%", type: "企业法人" }
    ],
    changes: [
      { date: "2023-03-15", type: "注册资本变更", before: "500万元", after: "1000万元" },
      { date: "2022-08-10", type: "股东变更", before: "王五", after: "李四" },
      { date: "2021-12-05", type: "地址变更", before: "北京市海淀区", after: "上海市浦东新区" }
    ],
    riskInfo: {
      lawsuits: 2,
      courtAnnouncements: 1,
      executions: 0,
      abnormalOperations: 0,
      penalties: 1
    },
    relatedCompanies: [
      { name: "上海关联公司", relation: "同一法人", risk: "低" },
      { name: "深圳分公司", relation: "分支机构", risk: "中" }
    ]
  };
  
  // 构建模块HTML
  const moduleHTML = `
    <div class="mb-4">
      <h4 class="fw-bold text-primary mb-3">企查查数据</h4>
      
      <div class="card shadow-sm mb-4">
        <div class="card-header bg-light">
          <h5 class="card-title mb-0">企业基本信息</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-6">
              <div class="mb-3">
                <label class="form-label text-muted small">企业名称</label>
                <p class="fw-bold">${qichachaData.companyName}</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small">法定代表人</label>
                <p class="fw-bold">${qichachaData.legalPerson}</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small">注册资本</label>
                <p class="fw-bold">${qichachaData.regCapital}</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="mb-3">
                <label class="form-label text-muted small">成立日期</label>
                <p class="fw-bold">${qichachaData.establishDate}</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small">企业状态</label>
                <p class="fw-bold">
                  <span class="badge bg-${qichachaData.status === '存续' ? 'success' : 'danger'}">
                    ${qichachaData.status}
                  </span>
                </p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small">所属行业</label>
                <p class="fw-bold">${qichachaData.industry}</p>
              </div>
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label text-muted small">注册地址</label>
            <p class="fw-bold">${qichachaData.address}</p>
          </div>
        </div>
      </div>
      
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">股东信息</h5>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-sm mb-0">
                  <thead>
                    <tr>
                      <th>股东名称</th>
                      <th>持股比例</th>
                      <th>类型</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${qichachaData.shareholders.map(shareholder => `
                      <tr>
                        <td>${shareholder.name}</td>
                        <td>${shareholder.ratio}</td>
                        <td>${shareholder.type}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-light">
              <h5 class="card-title mb-0">变更记录</h5>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-sm mb-0">
                  <thead>
                    <tr>
                      <th>变更日期</th>
                      <th>变更事项</th>
                      <th>变更前</th>
                      <th>变更后</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${qichachaData.changes.map(change => `
                      <tr>
                        <td>${change.date}</td>
                        <td>${change.type}</td>
                        <td>${change.before}</td>
                        <td>${change.after}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card shadow-sm mb-4">
        <div class="card-header bg-light">
          <h5 class="card-title mb-0">风险信息</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-3">
              <div class="text-center">
                <div class="display-4 fw-bold">${qichachaData.riskInfo.lawsuits}</div>
                <small class="text-muted">法律诉讼</small>
              </div>
            </div>
            <div class="col-md-3">
              <div class="text-center">
                <div class="display-4 fw-bold">${qichachaData.riskInfo.courtAnnouncements}</div>
                <small class="text-muted">法院公告</small>
              </div>
            </div>
            <div class="col-md-3">
              <div class="text-center">
                <div class="display-4 fw-bold">${qichachaData.riskInfo.executions}</div>
                <small class="text-muted">被执行</small>
              </div>
            </div>
            <div class="col-md-3">
              <div class="text-center">
                <div class="display-4 fw-bold">${qichachaData.riskInfo.penalties}</div>
                <small class="text-muted">行政处罚</small>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card shadow-sm">
        <div class="card-header bg-light">
          <h5 class="card-title mb-0">关联企业</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-sm mb-0">
              <thead>
                <tr>
                  <th>企业名称</th>
                  <th>关联关系</th>
                  <th>风险等级</th>
                </tr>
              </thead>
              <tbody>
                ${qichachaData.relatedCompanies.map(company => `
                  <tr>
                    <td>${company.name}</td>
                    <td>${company.relation}</td>
                    <td>
                      <span class="badge bg-${company.risk === '低' ? 'success' : company.risk === '中' ? 'warning' : 'danger'}">
                        ${company.risk}
                      </span>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 更新容器内容
  container.innerHTML = moduleHTML;
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是企查查数据模块，则自动加载
  if (window.location.hash === '#qichacha-data') {
    loadQichachaData();
  }
});