/**
 * 全球资金流向图表功能模块
 */

// 初始化趋势图表
function initializeTrendChart(historicalData) {
  if (typeof echarts === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js';
    script.onload = () => createTrendChart(historicalData);
    document.head.appendChild(script);
  } else {
    createTrendChart(historicalData);
  }
}

// 创建趋势图表
function createTrendChart(data) {
  const chartContainer = document.getElementById('capital-flow-trend-chart');
  if (!chartContainer) return;
  
  globalCapitalFlowChart = echarts.init(chartContainer);
  
  const option = {
    title: {
      text: '近7日资金流向趋势',
      textStyle: { fontSize: 14, color: '#333' },
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#ddd',
      borderWidth: 1,
      textStyle: { color: '#333' },
      formatter: function(params) {
        let result = `<div style="font-weight: bold; margin-bottom: 5px;">${params[0].axisValue}</div>`;
        params.forEach(param => {
          const color = param.value >= 0 ? '#28a745' : '#dc3545';
          const sign = param.value >= 0 ? '+' : '';
          result += `<div style="margin: 2px 0;">
            ${param.marker} ${param.seriesName}: 
            <span style="color:${color}; font-weight: bold;">${sign}${param.value.toFixed(1)} 亿美元</span>
          </div>`;
        });
        return result;
      }
    },
    legend: {
      type: 'scroll',
      bottom: 0,
      textStyle: { fontSize: 10 },
      itemWidth: 12,
      itemHeight: 8
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
      boundaryGap: false,
      data: data.dates,
      axisLabel: { 
        fontSize: 10,
        color: '#666'
      },
      axisLine: {
        lineStyle: { color: '#ddd' }
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: { 
        formatter: '{value}',
        fontSize: 10,
        color: '#666'
      },
      axisLine: {
        lineStyle: { color: '#ddd' }
      },
      splitLine: {
        lineStyle: { color: '#f0f0f0' }
      }
    },
    series: data.series.slice(0, 6).map((item, index) => {
      const colors = ['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8', '#6f42c1'];
      return {
        name: item.name,
        type: 'line',
        data: item.data,
        smooth: true,
        lineStyle: { 
          width: 2,
          color: colors[index % colors.length]
        },
        itemStyle: {
          color: colors[index % colors.length]
        },
        areaStyle: {
          opacity: 0.1,
          color: colors[index % colors.length]
        },
        emphasis: { 
          focus: 'series',
          lineStyle: { width: 3 }
        },
        markPoint: {
          data: [
            { type: 'max', name: '最大值' },
            { type: 'min', name: '最小值' }
          ]
        },
        markLine: {
          data: [
            { type: 'average', name: '平均值' }
          ]
        }
      };
    })
  };
  
  globalCapitalFlowChart.setOption(option);
  
  // 响应窗口大小变化
  const resizeHandler = () => {
    if (globalCapitalFlowChart) {
      globalCapitalFlowChart.resize();
    }
  };
  
  window.addEventListener('resize', resizeHandler);
  
  // 添加图表事件监听
  globalCapitalFlowChart.on('click', function(params) {
    if (params.componentType === 'series') {
      showSeriesDetail(params.seriesName, params.data, params.dataIndex);
    }
  });
  
  // 添加工具栏
  const toolboxOption = {
    toolbox: {
      feature: {
        saveAsImage: {
          title: '保存为图片',
          name: '资金流向趋势图'
        },
        dataZoom: {
          title: {
            zoom: '区域缩放',
            back: '区域缩放还原'
          }
        },
        magicType: {
          type: ['line', 'bar'],
          title: {
            line: '切换为折线图',
            bar: '切换为柱状图'
          }
        },
        restore: {
          title: '还原'
        }
      },
      right: 10,
      top: 10
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100
      },
      {
        start: 0,
        end: 100,
        height: 20,
        bottom: 40
      }
    ]
  };
  
  // 合并工具栏配置
  globalCapitalFlowChart.setOption(toolboxOption, true);
  
  // 响应窗口大小变化
  const chartResizeHandler = () => {
    if (globalCapitalFlowChart) {
      globalCapitalFlowChart.resize();
    }
  };
  
  window.addEventListener('resize', chartResizeHandler);
  
  // 清理函数
  window.cleanupGlobalChart = () => {
    window.removeEventListener('resize', chartResizeHandler);
    if (globalCapitalFlowChart) {
      globalCapitalFlowChart.dispose();
      globalCapitalFlowChart = null;
    }
  };
}