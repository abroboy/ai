/**
 * 全球资金流向简化地图实现
 * 使用散点图代替复杂的世界地图
 */

// 简化地图初始化
function initSimpleGlobalMap() {
    console.log('初始化简化全球资金流向地图...');
    
    const mapContainer = document.getElementById('global-capital-flow-map');
    if (!mapContainer) {
        console.error('地图容器未找到');
        return;
    }
    
    // 检查ECharts是否加载
    if (typeof echarts === 'undefined') {
        console.error('ECharts未加载');
        showMapError('ECharts库未加载，无法显示地图');
        return;
    }
    
    // 加载数据并初始化地图
    loadDataAndInitMap();
}

// 加载数据并初始化地图
async function loadDataAndInitMap() {
    try {
        console.log('加载全球资金流向数据...');
        
        const response = await fetch('/api/global-capital-flow');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const apiData = await response.json();
        console.log('API数据加载成功:', apiData.data?.length, '个地区');
        
        // 初始化简化地图
        initScatterMap(apiData);
        
        // 更新统计信息
        updateGlobalStats(apiData);
        
        // 更新数据表格
        updateDataTable(apiData.data || []);
        
    } catch (error) {
        console.error('数据加载失败:', error);
        showMapError('数据加载失败: ' + error.message);
    }
}

// 初始化散点地图
function initScatterMap(data) {
    const mapContainer = document.getElementById('global-capital-flow-map');
    
    try {
        // 销毁现有实例
        if (window.globalMapInstance) {
            window.globalMapInstance.dispose();
        }
        
        // 创建新实例
        window.globalMapInstance = echarts.init(mapContainer);
        
        // 准备散点数据
        const scatterData = (data.data || []).map(item => ({
            name: item.region,
            value: [item.lng || 0, item.lat || 0, Math.abs(item.netFlow)],
            netFlow: item.netFlow,
            inflow: item.inflow,
            outflow: item.outflow,
            change: item.change,
            itemStyle: {
                color: item.netFlow > 0 ? '#52c41a' : '#ff4d4f'
            }
        }));
        
        // 地图配置
        const option = {
            title: {
                text: '全球资金流向分布图',
                left: 'center',
                top: '5%',
                textStyle: {
                    fontSize: 18,
                    fontWeight: 'bold'
                }
            },
            tooltip: {
                trigger: 'item',
                backgroundColor: 'rgba(0,0,0,0.8)',
                borderColor: '#333',
                textStyle: {
                    color: '#fff'
                },
                formatter: function(params) {
                    const data = params.data;
                    return `
                        <div style="padding: 8px;">
                            <h4 style="margin: 0 0 8px 0; color: #fff;">${data.name}</h4>
                            <div style="margin: 4px 0;">净流入: <span style="color: ${data.netFlow > 0 ? '#52c41a' : '#ff4d4f'}">${data.netFlow > 0 ? '+' : ''}${data.netFlow} 亿美元</span></div>
                            <div style="margin: 4px 0;">流入: <span style="color: #52c41a">+${data.inflow} 亿美元</span></div>
                            <div style="margin: 4px 0;">流出: <span style="color: #ff4d4f">-${Math.abs(data.outflow)} 亿美元</span></div>
                            <div style="margin: 4px 0;">变化: <span style="color: ${data.change > 0 ? '#52c41a' : '#ff4d4f'}">${data.change > 0 ? '+' : ''}${data.change}%</span></div>
                        </div>
                    `;
                }
            },
            grid: {
                left: '10%',
                right: '10%',
                top: '15%',
                bottom: '15%'
            },
            xAxis: {
                type: 'value',
                name: '经度',
                nameLocation: 'middle',
                nameGap: 30,
                min: -180,
                max: 180,
                splitLine: {
                    show: true,
                    lineStyle: {
                        color: '#e0e0e0',
                        type: 'dashed'
                    }
                }
            },
            yAxis: {
                type: 'value',
                name: '纬度',
                nameLocation: 'middle',
                nameGap: 40,
                min: -60,
                max: 80,
                splitLine: {
                    show: true,
                    lineStyle: {
                        color: '#e0e0e0',
                        type: 'dashed'
                    }
                }
            },
            series: [
                {
                    type: 'scatter',
                    data: scatterData,
                    symbolSize: function(data) {
                        return Math.max(15, Math.min(50, Math.abs(data[2]) / 10 + 15));
                    },
                    itemStyle: {
                        opacity: 0.8,
                        borderWidth: 2,
                        borderColor: '#fff'
                    },
                    emphasis: {
                        itemStyle: {
                            opacity: 1,
                            borderWidth: 3,
                            shadowBlur: 10,
                            shadowColor: 'rgba(0,0,0,0.3)'
                        }
                    },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: '{b}',
                        fontSize: 11,
                        fontWeight: 'bold',
                        color: '#333'
                    }
                }
            ]
        };
        
        // 设置配置
        window.globalMapInstance.setOption(option);
        
        // 绑定点击事件
        window.globalMapInstance.on('click', function(params) {
            if (params.data) {
                showRegionDetail(params.data);
            }
        });
        
        // 响应式调整
        window.addEventListener('resize', function() {
            if (window.globalMapInstance) {
                window.globalMapInstance.resize();
            }
        });
        
        console.log('简化地图初始化完成，显示', scatterData.length, '个地区');
        
    } catch (error) {
        console.error('地图初始化失败:', error);
        showMapError('地图初始化失败: ' + error.message);
    }
}

// 更新全局统计
function updateGlobalStats(data) {
    try {
        const summary = data.summary || {};
        
        // 更新统计卡片
        updateStatElement('total-net-flow', summary.totalNetInflow || data.net_global_flow || 0);
        updateStatElement('active-markets', summary.activeMarkets || data.total_regions || 0);
        updateStatElement('total-inflow', data.total_inflow || 0);
        updateStatElement('total-outflow', Math.abs(data.total_outflow || 0));
        
        console.log('统计信息更新完成');
        
    } catch (error) {
        console.error('统计更新失败:', error);
    }
}

// 更新统计元素
function updateStatElement(id, value) {
    const element = document.getElementById(id);
    if (element) {
        if (typeof value === 'number') {
            element.textContent = value.toLocaleString('zh-CN', {
                minimumFractionDigits: 1,
                maximumFractionDigits: 1
            });
        } else {
            element.textContent = value;
        }
    }
}

// 更新数据表格
function updateDataTable(data) {
    const tableBody = document.querySelector('#capital-flow-table tbody');
    if (!tableBody) {
        console.log('数据表格容器未找到，跳过表格更新');
        return;
    }
    
    try {
        // 清空现有数据
        tableBody.innerHTML = '';
        
        // 按净流入排序
        const sortedData = [...data].sort((a, b) => b.netFlow - a.netFlow);
        
        // 添加新数据
        sortedData.forEach((item, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td><strong>${item.region}</strong></td>
                <td class="text-success">+${item.inflow.toLocaleString()}</td>
                <td class="text-danger">-${Math.abs(item.outflow).toLocaleString()}</td>
                <td class="${item.netFlow > 0 ? 'text-success' : 'text-danger'}">
                    <strong>${item.netFlow > 0 ? '+' : ''}${item.netFlow.toLocaleString()}</strong>
                </td>
                <td class="${item.change > 0 ? 'text-success' : 'text-danger'}">
                    ${item.change > 0 ? '+' : ''}${item.change}%
                </td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="showRegionDetail({name: '${item.region}', netFlow: ${item.netFlow}, inflow: ${item.inflow}, outflow: ${item.outflow}, change: ${item.change}})">
                        详情
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        });
        
        console.log('数据表格更新完成，显示', sortedData.length, '行数据');
        
    } catch (error) {
        console.error('表格更新失败:', error);
    }
}

// 显示地区详情
function showRegionDetail(data) {
    console.log('显示地区详情:', data.name);
    
    // 创建详情模态框
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${data.name} - 资金流向详情</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-6">
                            <div class="card text-success">
                                <div class="card-body text-center">
                                    <h4>+${data.inflow?.toLocaleString() || 0}</h4>
                                    <p>资金流入 (亿美元)</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="card text-danger">
                                <div class="card-body text-center">
                                    <h4>-${Math.abs(data.outflow || 0).toLocaleString()}</h4>
                                    <p>资金流出 (亿美元)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col-6">
                            <div class="card ${data.netFlow > 0 ? 'text-success' : 'text-danger'}">
                                <div class="card-body text-center">
                                    <h4>${data.netFlow > 0 ? '+' : ''}${data.netFlow?.toLocaleString() || 0}</h4>
                                    <p>净流入 (亿美元)</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="card ${data.change > 0 ? 'text-success' : 'text-danger'}">
                                <div class="card-body text-center">
                                    <h4>${data.change > 0 ? '+' : ''}${data.change || 0}%</h4>
                                    <p>变化幅度</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // 显示模态框
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    // 模态框关闭后删除元素
    modal.addEventListener('hidden.bs.modal', function() {
        document.body.removeChild(modal);
    });
}

// 显示地图错误
function showMapError(message) {
    const mapContainer = document.getElementById('global-capital-flow-map');
    if (mapContainer) {
        mapContainer.innerHTML = `
            <div class="alert alert-warning text-center" style="margin: 50px 20px;">
                <h5>⚠️ 地图加载失败</h5>
                <p>${message}</p>
                <button class="btn btn-primary" onclick="initSimpleGlobalMap()">重试</button>
            </div>
        `;
    }
}

// 刷新数据
function refreshGlobalCapitalFlow() {
    console.log('刷新全球资金流向数据...');
    loadDataAndInitMap();
}

// 页面加载完成后自动初始化
document.addEventListener('DOMContentLoaded', function() {
    // 检查是否在全球资金流向页面
    const mapContainer = document.getElementById('global-capital-flow-map');
    if (mapContainer) {
        console.log('检测到全球资金流向页面，开始初始化...');
        
        // 等待一下再初始化，确保所有资源加载完成
        setTimeout(() => {
            initSimpleGlobalMap();
        }, 500);
    }
});

// 导出函数到全局
window.initSimpleGlobalMap = initSimpleGlobalMap;
window.refreshGlobalCapitalFlow = refreshGlobalCapitalFlow;
window.showRegionDetail = showRegionDetail;