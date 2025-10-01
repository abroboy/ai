/**
 * 国内热点数据模块 - 工具函数
 */

// 根据影响力获取颜色
function getImpactColor(impact) {
  if (impact >= 85) return 'danger';
  if (impact >= 70) return 'warning';
  return 'success';
}

// 根据区域获取颜色
function getRegionColor(region) {
  const colorMap = {
    '全国': 'primary',
    '上海': 'success',
    '北京': 'danger',
    '深圳': 'warning',
    '广州': 'info',
    '一线城市': 'secondary',
    '试点地区': 'dark'
  };
  return colorMap[region] || 'secondary';
}

// 按类别筛选数据
function filterByCategory(category) {
  console.log('按类别筛选:', category);
  alert('类别筛选功能将在后续版本中实现');
}

// 刷新国内热点数据
function refreshDomesticHotspotData() {
  const contentArea = document.getElementById('content');
  contentArea.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在刷新国内热点数据...</p>
    </div>
  `;
  
  // 重新渲染模块
  renderDomesticHotspotModule(contentArea);
}

// 导出国内热点数据
function exportDomesticHotspotData() {
  console.log('导出国内热点数据');
  alert('数据导出功能将在后续版本中实现');
}

// 显示国内热点详情
function showDomesticHotspotDetail(id) {
  // 模拟获取热点详情数据
  const hotspotDetail = {
    id: id,
    title: "央行宣布降准0.25个百分点 释放流动性约5000亿元",
    source: "人民银行",
    date: "2025-10-01",
    impact: 95,
    region: "全国",
    category: "货币政策",
    content: "中国人民银行决定于10月15日下调金融机构存款准备金率0.25个百分点，此次降准将释放长期资金约5000亿元。这是央行今年第二次降准，旨在保持银行体系流动性合理充裕，支持实体经济发展。",
    relatedEvents: [
      "9月CPI同比上涨2.0%，处于温和区间",
      "前三季度GDP同比增长5.2%",
      "制造业PMI连续3个月回升"
    ],
    impactAnalysis: "此次降准将对金融市场和实体经济产生积极影响。一方面，释放的流动性将降低银行资金成本，有利于银行增加放贷；另一方面，将推动市场利率下行，降低企业融资成本，支持投资和消费。对股市而言，降准通常被视为利好消息，特别是对银行、地产等资金敏感行业。",
    marketReactions: [
      "A股三大指数集体上涨",
      "银行板块涨幅居前",
      "10年期国债收益率下降5个基点",
      "人民币汇率保持稳定"
    ]
  };
  
  // 更新模态框内容
  document.getElementById('domesticHotspotDetailTitle').textContent = hotspotDetail.title;
  
  const detailContent = `
    <div class="mb-4">
      <div class="d-flex justify-content-between mb-3">
        <div>
          <span class="badge bg-${getRegionColor(hotspotDetail.region)} me-2">${hotspotDetail.region}</span>
          <span class="badge bg-secondary">${hotspotDetail.category}</span>
        </div>
        <div class="text-muted small">
          来源: ${hotspotDetail.source} | 发布日期: ${hotspotDetail.date}
        </div>
      </div>
      
      <div class="alert alert-light">
        <h6 class="fw-bold">内容摘要</h6>
        <p>${hotspotDetail.content}</p>
      </div>
      
      <div class="row mb-3">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">相关事件</h6>
            </div>
            <div class="card-body">
              <ul class="mb-0">
                ${hotspotDetail.relatedEvents.map(event => `<li>${event}</li>`).join('')}
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="card-title mb-0">市场反应</h6>
            </div>
            <div class="card-body">
              <ul class="mb-0">
                ${hotspotDetail.marketReactions.map(reaction => `<li>${reaction}</li>`).join('')}
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header bg-light">
          <h6 class="card-title mb-0">影响分析</h6>
        </div>
        <div class="card-body">
          <p class="mb-0">${hotspotDetail.impactAnalysis}</p>
        </div>
      </div>
    </div>
  `;
  
  document.getElementById('domesticHotspotDetailContent').innerHTML = detailContent;
  
  // 显示模态框
  const modal = new bootstrap.Modal(document.getElementById('domesticHotspotDetailModal'));
  modal.show();
}

// 初始化类别分布图表
function initCategoryChart(data) {
  // 检查是否已加载ECharts
  if (typeof echarts === 'undefined') {
    // 如果没有加载ECharts，则动态加载
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = function() {
      // ECharts加载完成后初始化图表
      createCategoryChart(data);
    };
    document.head.appendChild(script);
  } else {
    // 如果已加载ECharts，直接初始化图表
    createCategoryChart(data);
  }
}

// 创建类别分布图表
function createCategoryChart(data) {
  const chartDom = document.getElementById('category-chart');
  if (!chartDom) return;
  
  const myChart = echarts.init(chartDom);
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      data: data.categories
    },
    series: [
      {
        name: '类别分布',
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data.categories.map((category, index) => {
          return {
            value: data.values[index],
            name: category
          };
        })
      }
    ]
  };
  
  myChart.setOption(option);
  
  // 响应窗口大小变化
  window.addEventListener('resize', function() {
    myChart.resize();
  });
}

// 加载Bootstrap的JS
function loadBootstrapJS() {
  if (typeof bootstrap === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js';
    document.head.appendChild(script);
  }
}