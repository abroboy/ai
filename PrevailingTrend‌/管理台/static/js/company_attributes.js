/**
 * 公司属性表模块
 * 大势所趋风险框架管理台
 */

// 加载公司属性表模块
function loadCompanyAttributes() {
  const container = document.getElementById('content');
  
  // 显示加载状态
  container.innerHTML = `
    <div class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-3">正在加载公司属性数据...</p>
    </div>
  `;

  // 模拟获取公司数据
  setTimeout(() => {
    try {
      // 模拟公司数据
      const companies = [
        {
          id: 'C001',
          name: '中国平安',
          industry: '保险',
          region: '深圳',
          marketCap: '1.2万亿',
          riskLevel: '低',
          score: 85
        },
        {
          id: 'C002', 
          name: '招商银行',
          industry: '银行',
          region: '深圳',
          marketCap: '8500亿',
          riskLevel: '低',
          score: 82
        },
        {
          id: 'C003',
          name: '贵州茅台',
          industry: '白酒',
          region: '贵州',
          marketCap: '2.1万亿',
          riskLevel: '中',
          score: 78
        }
      ];

      renderCompanyAttributes(companies);
    } catch (error) {
      console.error('加载公司属性数据失败:', error);
      container.innerHTML = `
        <div class="alert alert-danger">
          <i class="bi bi-exclamation-triangle-fill"></i> 加载失败: ${error.message}
        </div>
      `;
    }
  }, 1000);
}

// 渲染公司属性表
function renderCompanyAttributes(companies) {
  const container = document.getElementById('content');
  
  const moduleHTML = `
    <div class="company-attributes-module">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class="mb-0">
          <i class="bi bi-building"></i> 公司属性表
          <span class="badge bg-success ms-2">实时数据</span>
        </h3>
        <div>
          <button class="btn btn-primary btn-sm" onclick="refreshCompanyData()">
            <i class="bi bi-arrow-clockwise"></i> 刷新
          </button>
          <button class="btn btn-outline-secondary btn-sm" onclick="exportCompanyData()">
            <i class="bi bi-download"></i> 导出
          </button>
        </div>
      </div>

      <div class="row mb-3">
        <div class="col-md-6">
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-search"></i></span>
            <input type="text" class="form-control" placeholder="搜索公司名称或代码..." id="companySearch">
          </div>
        </div>
        <div class="col-md-3">
          <select class="form-select" id="industryFilter">
            <option value="">全部行业</option>
            <option value="银行">银行</option>
            <option value="保险">保险</option>
            <option value="白酒">白酒</option>
          </select>
        </div>
        <div class="col-md-3">
          <select class="form-select" id="riskFilter">
            <option value="">全部风险等级</option>
            <option value="低">低风险</option>
            <option value="中">中风险</option>
            <option value="高">高风险</option>
          </select>
        </div>
      </div>

      <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead class="table-dark">
            <tr>
              <th>公司代码</th>
              <th>公司名称</th>
              <th>行业</th>
              <th>地区</th>
              <th>市值</th>
              <th>风险等级</th>
              <th>评分</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            ${companies.map(company => `
              <tr>
                <td><code>${company.id}</code></td>
                <td><strong>${company.name}</strong></td>
                <td><span class="badge bg-info">${company.industry}</span></td>
                <td>${company.region}</td>
                <td>${company.marketCap}</td>
                <td>
                  <span class="badge bg-${getRiskBadgeColor(company.riskLevel)}">
                    ${company.riskLevel}风险
                  </span>
                </td>
                <td>
                  <div class="progress" style="width: 60px; height: 20px;">
                    <div class="progress-bar bg-${getScoreColor(company.score)}" 
                         style="width: ${company.score}%"
                         title="${company.score}分">
                      ${company.score}
                    </div>
                  </div>
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-primary" onclick="viewCompanyDetail('${company.id}')">
                    <i class="bi bi-eye"></i> 详情
                  </button>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>

      <div class="d-flex justify-content-between align-items-center mt-3">
        <small class="text-muted">共 ${companies.length} 家公司</small>
        <nav>
          <ul class="pagination pagination-sm mb-0">
            <li class="page-item disabled">
              <span class="page-link">上一页</span>
            </li>
            <li class="page-item active">
              <span class="page-link">1</span>
            </li>
            <li class="page-item disabled">
              <span class="page-link">下一页</span>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- 公司详情模态框 -->
    <div class="modal fade" id="companyDetailModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="companyDetailModalLabel">公司详情</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" id="companyDetailContent">
            <!-- 详情内容将在这里动态加载 -->
          </div>
        </div>
      </div>
    </div>
  `;

  container.innerHTML = moduleHTML;
  
  // 绑定搜索和筛选事件
  bindCompanyEvents();
}

// 获取风险等级徽章颜色
function getRiskBadgeColor(riskLevel) {
  switch(riskLevel) {
    case '低': return 'success';
    case '中': return 'warning';
    case '高': return 'danger';
    default: return 'secondary';
  }
}

// 获取评分颜色
function getScoreColor(score) {
  if (score >= 80) return 'success';
  if (score >= 60) return 'warning';
  return 'danger';
}

// 绑定事件
function bindCompanyEvents() {
  // 搜索功能
  const searchInput = document.getElementById('companySearch');
  if (searchInput) {
    searchInput.addEventListener('input', filterCompanies);
  }
  
  // 筛选功能
  const industryFilter = document.getElementById('industryFilter');
  const riskFilter = document.getElementById('riskFilter');
  
  if (industryFilter) {
    industryFilter.addEventListener('change', filterCompanies);
  }
  
  if (riskFilter) {
    riskFilter.addEventListener('change', filterCompanies);
  }
}

// 筛选公司
function filterCompanies() {
  // 这里可以实现筛选逻辑
  console.log('筛选公司数据...');
}

// 查看公司详情
function viewCompanyDetail(companyId) {
  const modal = new bootstrap.Modal(document.getElementById('companyDetailModal'));
  const modalTitle = document.getElementById('companyDetailModalLabel');
  const modalContent = document.getElementById('companyDetailContent');
  
  // 模拟获取公司详情
  const companyDetail = {
    id: companyId,
    name: '中国平安',
    industry: '保险',
    region: '深圳',
    marketCap: '1.2万亿',
    riskLevel: '低',
    score: 85
  };
  
  modalTitle.textContent = companyDetail.name + ' - 详细信息';
  modalContent.innerHTML = `
    <div class="row">
      <div class="col-md-6">
        <h6>基本信息</h6>
        <table class="table table-sm">
          <tr><td>公司代码</td><td>${companyDetail.id}</td></tr>
          <tr><td>公司名称</td><td>${companyDetail.name}</td></tr>
          <tr><td>所属行业</td><td>${companyDetail.industry}</td></tr>
          <tr><td>注册地区</td><td>${companyDetail.region}</td></tr>
        </table>
      </div>
      <div class="col-md-6">
        <h6>风险评估</h6>
        <table class="table table-sm">
          <tr><td>市值规模</td><td>${companyDetail.marketCap}</td></tr>
          <tr><td>风险等级</td><td><span class="badge bg-${getRiskBadgeColor(companyDetail.riskLevel)}">${companyDetail.riskLevel}风险</span></td></tr>
          <tr><td>综合评分</td><td>${companyDetail.score}分</td></tr>
        </table>
      </div>
    </div>
  `;
  
  modal.show();
}

// 刷新公司数据
function refreshCompanyData() {
  loadCompanyAttributes();
}

// 导出公司数据
function exportCompanyData() {
  alert('导出功能开发中...');
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 如果当前页面是公司属性表模块，则自动加载
  if (window.location.hash === '#company-attributes') {
    loadCompanyAttributes();
  }
});