/**
 * K线图插件 - 独立组件
 * 使用方法：
 * 1. 引入LightweightCharts库
 * 2. 引入此插件文件
 * 3. 创建容器元素
 * 4. 调用 KlineChart.create(container, options)
 */

class KlineChart {
    constructor(container, options = {}) {
        this.container = container;
        this.options = this.mergeOptions(options);
        this.chart = null;
        this.candles = null; // Changed from candlestickSeries to candles
        this.volumeSeries = null;
        this.resizeObserver = null;
        this.isInitialized = false;
        
        this.init();
    }
    
    // 合并选项
    mergeOptions(options = {}) {
        const defaults = {
            width: 800,
            height: 500,  // 增加高度以容纳分离的成交量
            theme: 'light',
            colors: {
                background: '#ffffff',
                text: '#333333',
                grid: '#e1e5e9',
                border: '#d1d5db',
                up: '#f56565',      // 红色，上涨
                down: '#48bb78',    // 绿色，下跌
                volume: '#4299e1',  // 蓝色，成交量
                volumeUp: '#f56565', // 红色，上涨成交量
                volumeDown: '#48bb78', // 绿色，下跌成交量
                ma5: '#ff6b6b',     // 5日均线
                ma10: '#4ecdc4',    // 10日均线
                ma20: '#45b7d1',    // 20日均线
                ma30: '#96ceb4'     // 30日均线
            },
            showGrid: true,
            showCrosshair: true,
            showVolume: true,
            showMA: true,           // 显示均线
            maPeriods: [5, 10, 20, 30], // 均线周期
            volumeHeight: 0.2,      // 成交量区域高度比例
            apiEndpoint: '/api/stock/{code}/kline',
            autoResize: true
        };
        
        return { ...defaults, ...options };
    }
    
    // 初始化图表
    init() {
        if (this.isInitialized) {
            console.warn('K线图已经初始化过了');
            return;
        }
        
        if (typeof LightweightCharts === 'undefined') {
            this.showError('LightweightCharts库未加载');
            return;
        }
        
        try {
            this.setupContainer();
            this.createChart();
            this.setupResize();
            
            // 验证所有必要的组件都已创建
            if (!this.chart || !this.candles) {
                throw new Error('图表组件创建失败');
            }
            
            this.isInitialized = true;
            console.log('K线图初始化完成');
        } catch (error) {
            this.showError('图表初始化失败: ' + error.message);
            console.error('K线图初始化失败:', error);
            this.isInitialized = false;
        }
    }
    
    // 设置容器
    setupContainer() {
        this.container.style.width = this.options.width + 'px';
        this.container.style.height = this.options.height + 'px';
        this.container.style.border = '1px solid #d1d5db';
        this.container.style.borderRadius = '4px';
        this.container.style.backgroundColor = this.options.colors.background;
        this.container.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)';
        this.container.style.fontFamily = 'Microsoft YaHei, Arial, sans-serif';
        this.container.innerHTML = '';
    }
    
    // 创建图表
    createChart() {
        // 检查LightweightCharts库是否可用
        if (typeof LightweightCharts === 'undefined') {
            throw new Error('LightweightCharts库未加载');
        }
        
        const chartOptions = {
            width: this.container.clientWidth || this.options.width,
            height: this.options.height,
            layout: {
                backgroundColor: this.options.colors.background,
                textColor: this.options.colors.text,
                fontSize: 12,
                fontFamily: 'Microsoft YaHei, Arial, sans-serif'
            },
            grid: {
                vertLines: {
                    color: this.options.showGrid ? this.options.colors.grid : 'transparent',
                    style: LightweightCharts.LineStyle.Solid,
                },
                horzLines: {
                    color: this.options.showGrid ? this.options.colors.grid : 'transparent',
                    style: LightweightCharts.LineStyle.Solid,
                },
            },
            crosshair: {
                mode: this.options.showCrosshair ? LightweightCharts.CrosshairMode.Normal : LightweightCharts.CrosshairMode.Hidden,
                vertLine: {
                    color: '#2962FF',
                    width: 1,
                    style: LightweightCharts.LineStyle.Solid,
                    labelBackgroundColor: '#2962FF',
                },
                horzLine: {
                    color: '#2962FF',
                    width: 1,
                    style: LightweightCharts.LineStyle.Solid,
                    labelBackgroundColor: '#2962FF',
                },
            },
            rightPriceScale: {
                borderColor: this.options.colors.border,
                scaleMargins: {
                    top: 0.1,
                    bottom: this.options.showVolume ? 0.3 : 0.1, // 为成交量留出空间
                },
                visible: true,
                autoScale: true,
            },
            timeScale: {
                borderColor: this.options.colors.border,
                timeVisible: true,
                secondsVisible: false,
                rightOffset: 12,
                barSpacing: 3,
                fixLeftEdge: true,
                lockVisibleTimeRangeOnResize: true,
                rightBarStaysOnScroll: true,
                borderVisible: false,
                visible: true,
                tickMarkFormatter: (time) => {
                    const date = new Date(time * 1000);
                    return date.getMonth() + 1 + '/' + date.getDate();
                },
            },
            handleScroll: {
                mouseWheel: true,
                pressedMouseMove: true,
                horzTouchDrag: true,
                vertTouchDrag: true,
            },
            handleScale: {
                axisPressedMouseMove: true,
                mouseWheel: true,
                pinch: true,
            },
        };

        try {
            this.chart = LightweightCharts.createChart(this.container, chartOptions);
            
            // 验证图表创建是否成功
            if (!this.chart || typeof this.chart.addCandlestickSeries !== 'function') {
                throw new Error('图表创建失败或addCandlestickSeries方法不可用');
            }
            
            // 创建K线系列
            this.candles = this.chart.addCandlestickSeries({
                upColor: this.options.colors.up,
                downColor: this.options.colors.down,
                borderVisible: false,
                wickUpColor: this.options.colors.up,
                wickDownColor: this.options.colors.down,
                priceFormat: {
                    type: 'price',
                    precision: 2,
                    minMove: 0.01,
                },
            });

            // 创建均线系列
            this.maSeries = {};
            if (this.options.showMA) {
                const maColors = [
                    this.options.colors.ma5,
                    this.options.colors.ma10,
                    this.options.colors.ma20,
                    this.options.colors.ma30
                ];
                
                this.options.maPeriods.forEach((period, index) => {
                    this.maSeries[period] = this.chart.addLineSeries({
                        color: maColors[index],
                        lineWidth: 1,
                        lineType: LightweightCharts.LineType.Solid,
                        priceFormat: {
                            type: 'price',
                            precision: 2,
                            minMove: 0.01,
                        },
                        title: `MA${period}`,
                    });
                });
            }

            // 创建成交量系列（分离显示）
            if (this.options.showVolume) {
                this.volumeSeries = this.chart.addHistogramSeries({
                    color: this.options.colors.volume,
                    priceFormat: {
                        type: 'volume',
                    },
                    priceScaleId: 'volume', // 独立的成交量价格轴
                    scaleMargins: {
                        top: 0.8, // 成交量显示在底部
                        bottom: 0,
                    },
                    priceLineVisible: false,
                    lastValueVisible: false,
                });
                
                // 创建独立的成交量价格轴
                this.chart.priceScale('volume').applyOptions({
                    scaleMargins: {
                        top: 0.8,
                        bottom: 0,
                    },
                    borderVisible: false,
                    drawTicks: false,
                });
            }

            console.log('K线图实例创建成功:', this);
            return true;
        } catch (error) {
            console.error('创建K线图失败:', error);
            throw new Error('图表创建失败或addCandlestickSeries方法不可用');
        }
    }
    
    // 设置响应式调整
    setupResize() {
        if (!this.options.autoResize) return;
        
        this.resizeObserver = new ResizeObserver(entries => {
            if (entries.length === 0 || entries[0].target !== this.container) {
                return;
            }
            const newRect = entries[0].contentRect;
            this.chart.applyOptions({ 
                height: newRect.height, 
                width: newRect.width 
            });
        });
        
        this.resizeObserver.observe(this.container);
    }
    
    // 加载数据
    async loadData(stockCode) {
        if (!this.isInitialized) {
            console.error('图表未初始化');
            return false;
        }
        
        try {
            const url = this.options.apiEndpoint.replace('{code}', stockCode);
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success && data.data) {
                this.setData(data.data);
                return true;
            } else {
                throw new Error(data.message || '获取数据失败');
            }
        } catch (error) {
            this.showError('数据加载失败: ' + error.message);
            console.error('K线数据加载失败:', error);
            return false;
        }
    }
    
    // 设置数据
    setData(data) {
        if (!this.isInitialized) {
            console.error('图表未初始化');
            return;
        }
        
        if (!this.candles) {
            console.error('K线系列未创建');
            return;
        }
        
        try {
            // 设置K线数据
            if (data.candles && data.candles.length > 0) {
                this.candles.setData(data.candles);
                
                // 计算并设置均线数据
                if (this.options.showMA && this.maSeries) {
                    this.calculateAndSetMA(data.candles);
                }
            }
            
            // 设置成交量数据，根据涨跌设置颜色
            if (this.options.showVolume && data.volumes && data.volumes.length > 0) {
                // 处理成交量数据，根据涨跌设置颜色
                const processedVolumes = data.volumes.map((volume, index) => {
                    const candle = data.candles[index];
                    if (candle) {
                        const isUp = candle.close >= candle.open;
                        return {
                            ...volume,
                            color: isUp ? this.options.colors.volumeUp : this.options.colors.volumeDown
                        };
                    }
                    return volume;
                });
                
                this.volumeSeries.setData(processedVolumes);
            }
            
            console.log('K线数据设置成功');
        } catch (error) {
            this.showError('数据设置失败: ' + error.message);
            console.error('K线数据设置失败:', error);
        }
    }
    
    // 计算均线数据
    calculateAndSetMA(candles) {
        if (!candles || candles.length === 0) return;
        
        this.options.maPeriods.forEach(period => {
            const maData = this.calculateMA(candles, period);
            if (this.maSeries[period]) {
                this.maSeries[period].setData(maData);
            }
        });
    }
    
    // 计算指定周期的移动平均线
    calculateMA(candles, period) {
        const maData = [];
        
        for (let i = period - 1; i < candles.length; i++) {
            let sum = 0;
            for (let j = 0; j < period; j++) {
                sum += candles[i - j].close;
            }
            const ma = sum / period;
            
            maData.push({
                time: candles[i].time,
                value: parseFloat(ma.toFixed(2))
            });
        }
        
        return maData;
    }
    
    // 更新数据
    async updateData(stockCode) {
        const success = await this.loadData(stockCode);
        if (success) {
            console.log('K线数据更新成功');
        }
        return success;
    }
    
    // 显示错误信息
    showError(message) {
        this.container.innerHTML = `
            <div style="
                padding: 20px; 
                text-align: center; 
                color: #666;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
            ">
                <div style="font-size: 24px; margin-bottom: 10px;">⚠️</div>
                <div>${message}</div>
            </div>
        `;
    }
    
    // 显示加载状态
    showLoading() {
        this.container.innerHTML = `
            <div style="
                padding: 20px; 
                text-align: center; 
                color: #666;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
            ">
                <div style="font-size: 24px; margin-bottom: 10px;">📊</div>
                <div>加载K线图中...</div>
            </div>
        `;
    }
    
    // 销毁图表
    destroy() {
        if (this.resizeObserver) {
            this.resizeObserver.disconnect();
        }
        
        if (this.chart) {
            this.chart.remove();
        }
        
        this.isInitialized = false;
        console.log('K线图已销毁');
    }
    
    // 获取图表实例
    getChart() {
        return this.chart;
    }
    
    // 获取K线系列
    getCandlestickSeries() {
        return this.candles;
    }
    
    // 获取成交量系列
    getVolumeSeries() {
        return this.volumeSeries;
    }
}

// 静态方法：创建K线图实例
KlineChart.create = function(container, options = {}) {
    return new KlineChart(container, options);
};

// 静态方法：检查依赖
KlineChart.checkDependencies = function() {
    if (typeof LightweightCharts === 'undefined') {
        console.error('缺少依赖: LightweightCharts库未加载');
        return false;
    }
    return true;
};

// 导出到全局
window.KlineChart = KlineChart; 