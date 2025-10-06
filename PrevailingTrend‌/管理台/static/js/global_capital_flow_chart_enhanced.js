/**
 * 全球资金流向图表增强功能模块
 */

// 显示系列详情
function showSeriesDetail(seriesName, value, dataIndex) {
  const modal = `
    <div class="modal fade" id="seriesDetailModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">${seriesName} - 详细信息</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <p><strong>数值:</strong> ${value >= 0 ? '+' : ''}${value.toFixed(1)} 亿美元</p>
            <p><strong>日期索引:</strong> ${dataIndex}</p>
            <p><strong>趋势:</strong> ${value >= 0 ? '流入' : '流出'}</p>
            <div class="alert ${value >= 0 ? 'alert-success' : 'alert-danger'}">
              ${value >= 0 ? '资金净流入地区' : '资金净流出地区'}
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 移除现有模态框
  const existingModal = document.getElementById('seriesDetailModal');
  if (existingModal) {
    existingModal.remove();
  }
  
  // 添加新模态框
  document.body.insertAdjacentHTML('beforeend', modal);
  
  // 显示模态框
  const modalInstance = new bootstrap.Modal(document.getElementById('seriesDetailModal'));
  modalInstance.show();
}

// 创建对比图表
function createComparisonChart(region1Data, region2Data) {
  const chartContainer = document.getElementById('comparison-chart');
  if (!chartContainer) return;
  
  const comparisonChart = echarts.init(chartContainer);
  
  const option = {
    title: {
      text: '地区资金流向对比',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: [region1Data.name, region2Data.name],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['流入', '流出', '净流入']
    },
    yAxis: {
      type: 'value',
      name: '亿美元'
    },
    series: [
      {
        name: region1Data.name,
        type: 'bar',
        data: [region1Data.inflow, region1Data.outflow, region1Data.netFlow],
        itemStyle: {
          color: '#007bff'
        }
      },
      {
        name: region2Data.name,
        type: 'bar',
        data: [region2Data.inflow, region2Data.outflow, region2Data.netFlow],
        itemStyle: {
          color: '#28a745'
        }
      }
    ]
  };
  
  comparisonChart.setOption(option);
  return comparisonChart;
}

// 创建饼图
function createPieChart(data, containerId) {
  const chartContainer = document.getElementById(containerId);
  if (!chartContainer) return;
  
  const pieChart = echarts.init(chartContainer);
  
  // 准备饼图数据
  const pieData = data.map(item => ({
    name: item.region,
    value: Math.abs(item.netFlow),
    itemStyle: {
      color: item.netFlow >= 0 ? '#28a745' : '#dc3545'
    }
  }));
  
  const option = {
    title: {
      text: '资金流向分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} 亿美元 ({d}%)'
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 10,
      top: 20,
      bottom: 20
    },
    series: [
      {
        name: '资金流向',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['40%', '50%'],
        data: pieData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        label: {
          formatter: '{b}\n{c} 亿美元'
        }
      }
    ]
  };
  
  pieChart.setOption(option);
  return pieChart;
}

// 创建雷达图
function createRadarChart(data, containerId) {
  const chartContainer = document.getElementById(containerId);
  if (!chartContainer) return;
  
  const radarChart = echarts.init(chartContainer);
  
  // 选择前6个地区
  const topRegions = data.slice(0, 6);
  
  const option = {
    title: {
      text: '地区综合评估雷达图',
      left: 'center'
    },
    tooltip: {},
    radar: {
      name: {
        textStyle: {
          color: '#666',
          fontSize: 12
        }
      },
      indicator: [
        { name: '资金流入', max: Math.max(...topRegions.map(r => r.inflow)) },
        { name: '资金流出', max: Math.max(...topRegions.map(r => r.outflow)) },
        { name: '净流入', max: Math.max(...topRegions.map(r => Math.abs(r.netFlow))) },
        { name: '变化率', max: Math.max(...topRegions.map(r => Math.abs(r.change))) },
        { name: '波动性', max: 20 },
        { name: '活跃度', max: 100 }
      ]
    },
    series: topRegions.map((region, index) => ({
      name: region.region,
      type: 'radar',
      data: [
        {
          value: [
            region.inflow,
            region.outflow,
            Math.abs(region.netFlow),
            Math.abs(region.change),
            region.volatility || Math.abs(region.change),
            (region.inflow + region.outflow) / 20 // 活跃度计算
          ],
          name: region.region,
          itemStyle: {
            color: ['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8', '#6f42c1'][index]
          }
        }
      ]
    }))
  };
  
  radarChart.setOption(option);
  return radarChart;
}

// 创建散点图
function createScatterChart(data, containerId) {
  const chartContainer = document.getElementById(containerId);
  if (!chartContainer) return;
  
  const scatterChart = echarts.init(chartContainer);
  
  const scatterData = data.map(item => [
    item.inflow,
    item.outflow,
    Math.abs(item.netFlow),
    item.region
  ]);
  
  const option = {
    title: {
      text: '资金流入流出散点图',
      left: 'center'
    },
    tooltip: {
      formatter: function(params) {
        return `${params.data[3]}<br/>流入: ${params.data[0].toFixed(1)} 亿美元<br/>流出: ${params.data[1].toFixed(1)} 亿美元<br/>净额: ${params.data[2].toFixed(1)} 亿美元`;
      }
    },
    xAxis: {
      name: '资金流入 (亿美元)',
      nameLocation: 'middle',
      nameGap: 30
    },
    yAxis: {
      name: '资金流出 (亿美元)',
      nameLocation: 'middle',
      nameGap: 30
    },
    series: [
      {
        type: 'scatter',
        data: scatterData,
        symbolSize: function(data) {
          return Math.max(10, data[2] / 20);
        },
        itemStyle: {
          color: function(params) {
            const netFlow = params.data[0] - params.data[1];
            return netFlow >= 0 ? '#28a745' : '#dc3545';
          }
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };
  
  scatterChart.setOption(option);
  return scatterChart;
}

// 创建K线图（模拟资金流向波动）
function createCandlestickChart(data, containerId) {
  const chartContainer = document.getElementById(containerId);
  if (!chartContainer) return;
  
  const kChart = echarts.init(chartContainer);
  
  // 生成模拟K线数据
  const kData = [];
  const dates = [];
  
  for (let i = 0; i < 30; i++) {
    const date = new Date();
    date.setDate(date.getDate() - (29 - i));
    dates.push(date.toLocaleDateString('zh-CN'));
    
    const base = 100 + Math.random() * 200;
    const high = base + Math.random() * 50;
    const low = base - Math.random() * 50;
    const close = low + Math.random() * (high - low);
    
    kData.push([base, close, low, high]); // [开盘, 收盘, 最低, 最高]
  }
  
  const option = {
    title: {
      text: '资金流向波动图',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const data = params[0].data;
        return `日期: ${params[0].axisValue}<br/>
                开盘: ${data[0].toFixed(1)}<br/>
                收盘: ${data[1].toFixed(1)}<br/>
                最低: ${data[2].toFixed(1)}<br/>
                最高: ${data[3].toFixed(1)}`;
      }
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        type: 'candlestick',
        data: kData,
        itemStyle: {
          color: '#28a745',
          color0: '#dc3545',
          borderColor: '#28a745',
          borderColor0: '#dc3545'
        }
      }
    ]
  };
  
  kChart.setOption(option);
  return kChart;
}

// 图表主题切换
function switchChartTheme(theme) {
  const charts = [globalCapitalFlowChart];
  
  charts.forEach(chart => {
    if (chart) {
      chart.dispose();
      // 重新初始化图表
      const container = chart.getDom();
      const newChart = echarts.init(container, theme);
      // 重新设置配置
      // 这里需要保存原始配置并重新应用
    }
  });
}

// 图表数据导出
function exportChartData(chart, filename) {
  if (!chart) return;
  
  const option = chart.getOption();
  const data = {
    title: option.title[0].text,
    series: option.series,
    xAxis: option.xAxis,
    yAxis: option.yAxis,
    exportTime: new Date().toISOString()
  };
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${filename}_${new Date().toLocaleDateString('zh-CN')}.json`;
  link.click();
  
  showNotification('图表数据导出成功', 'success');
}

// 图表截图
function captureChart(chartId, filename) {
  const chart = echarts.getInstanceByDom(document.getElementById(chartId));
  if (!chart) return;
  
  const url = chart.getDataURL({
    type: 'png',
    pixelRatio: 2,
    backgroundColor: '#fff'
  });
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `${filename}_${new Date().toLocaleDateString('zh-CN')}.png`;
  link.click();
  
  showNotification('图表截图保存成功', 'success');
}