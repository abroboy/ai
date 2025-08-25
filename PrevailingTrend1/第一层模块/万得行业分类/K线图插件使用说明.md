# K线图插件使用说明

## 概述

K线图插件是一个独立的、可复用的JavaScript组件，用于在网页中显示股票K线图。该插件基于LightweightCharts库构建，提供了简洁的API和丰富的配置选项。

## 功能特性

- ✅ **独立组件**: 不依赖特定框架，可在任何网页中使用
- ✅ **主题定制**: 支持浅色和深色主题
- ✅ **响应式设计**: 自动适应容器大小变化
- ✅ **高性能**: 基于LightweightCharts库，渲染速度快
- ✅ **易于集成**: 简单的API接口
- ✅ **数据可视化**: 支持K线图和成交量显示
- ✅ **实时更新**: 支持数据实时更新

## 快速开始

### 1. 引入依赖

```html
<!-- 引入LightweightCharts库 -->
<script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>

<!-- 引入K线图插件 -->
<script src="/static/js/kline-plugin.js"></script>
```

### 2. 创建容器

```html
<div id="chartContainer"></div>
```

### 3. 初始化图表

```javascript
// 创建图表实例
const chart = KlineChart.create(document.getElementById('chartContainer'), {
    height: 400,
    theme: 'light'
});

// 加载数据
chart.loadData('000001');
```

## API 参考

### KlineChart.create(container, options)

创建K线图实例。

**参数:**
- `container` (HTMLElement): 图表容器元素
- `options` (Object): 配置选项

**返回值:**
- `KlineChart`: 图表实例

### 配置选项

```javascript
const options = {
    width: '100%',           // 图表宽度
    height: 400,             // 图表高度
    theme: 'light',          // 主题: 'light' | 'dark'
    showVolume: true,        // 是否显示成交量
    showGrid: true,          // 是否显示网格
    showCrosshair: true,     // 是否显示十字线
    colors: {                // 颜色配置
        up: '#26a69a',       // 上涨颜色
        down: '#ef5350',     // 下跌颜色
        grid: '#f0f0f0',     // 网格颜色
        background: '#ffffff', // 背景颜色
        text: '#333333'      // 文字颜色
    },
    apiEndpoint: '/api/stock/{code}/kline', // API端点
    autoResize: true         // 自动调整大小
};
```

### 实例方法

#### loadData(stockCode)

加载指定股票的数据。

**参数:**
- `stockCode` (String): 股票代码

**返回值:**
- `Promise<Boolean>`: 加载是否成功

```javascript
const success = await chart.loadData('000001');
if (success) {
    console.log('数据加载成功');
}
```

#### updateData(stockCode)

更新指定股票的数据。

**参数:**
- `stockCode` (String): 股票代码

**返回值:**
- `Promise<Boolean>`: 更新是否成功

```javascript
const success = await chart.updateData('000001');
if (success) {
    console.log('数据更新成功');
}
```

#### setData(data)

直接设置图表数据。

**参数:**
- `data` (Object): 数据对象，格式如下：

```javascript
const data = {
    candles: [
        {
            time: 1753372800,    // 时间戳
            open: 12.33,         // 开盘价
            high: 12.46,         // 最高价
            low: 12.32,          // 最低价
            close: 12.35         // 收盘价
        }
        // ... 更多数据
    ],
    volumes: [
        {
            time: 1753372800,    // 时间戳
            value: 1108267,      // 成交量
            color: '#26a69a'     // 颜色（可选）
        }
        // ... 更多数据
    ]
};
```

#### destroy()

销毁图表实例，释放资源。

```javascript
chart.destroy();
```

#### getChart()

获取底层LightweightCharts实例。

**返回值:**
- `Chart`: LightweightCharts实例

#### getCandlestickSeries()

获取K线系列。

**返回值:**
- `CandlestickSeries`: K线系列实例

#### getVolumeSeries()

获取成交量系列。

**返回值:**
- `HistogramSeries`: 成交量系列实例

### 静态方法

#### KlineChart.checkDependencies()

检查依赖是否已加载。

**返回值:**
- `Boolean`: 依赖是否完整

```javascript
if (KlineChart.checkDependencies()) {
    console.log('依赖检查通过');
} else {
    console.error('缺少依赖');
}
```

## 使用示例

### 基本使用

```html
<!DOCTYPE html>
<html>
<head>
    <title>K线图示例</title>
</head>
<body>
    <div id="chartContainer" style="width: 800px; height: 400px;"></div>
    
    <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
    <script src="/static/js/kline-plugin.js"></script>
    <script>
        // 创建图表
        const chart = KlineChart.create(document.getElementById('chartContainer'), {
            height: 400,
            theme: 'light'
        });
        
        // 加载数据
        chart.loadData('000001');
    </script>
</body>
</html>
```

### 高级配置

```javascript
// 深色主题配置
const darkChart = KlineChart.create(container, {
    height: 500,
    theme: 'dark',
    showVolume: true,
    showGrid: false,
    colors: {
        up: '#00ff88',
        down: '#ff4444',
        background: '#1a1a1a',
        text: '#ffffff'
    }
});

// 自定义API端点
const customChart = KlineChart.create(container, {
    apiEndpoint: '/api/custom/stock/{code}/kline'
});
```

### 事件处理

```javascript
const chart = KlineChart.create(container, options);

// 监听数据加载完成
chart.loadData('000001').then(success => {
    if (success) {
        console.log('数据加载完成');
        
        // 获取图表实例进行自定义操作
        const chartInstance = chart.getChart();
        const candlestickSeries = chart.getCandlestickSeries();
        
        // 添加技术指标等
        // ...
    }
});
```

## 数据格式

### K线数据格式

```javascript
{
    time: 1753372800,    // Unix时间戳（秒）
    open: 12.33,         // 开盘价
    high: 12.46,         // 最高价
    low: 12.32,          // 最低价
    close: 12.35         // 收盘价
}
```

### 成交量数据格式

```javascript
{
    time: 1753372800,    // Unix时间戳（秒）
    value: 1108267,      // 成交量
    color: '#26a69a'     // 颜色（可选，根据涨跌自动设置）
}
```

## 主题配置

### 浅色主题（默认）

```javascript
{
    colors: {
        up: '#26a69a',       // 绿色
        down: '#ef5350',     // 红色
        grid: '#f0f0f0',     // 浅灰色
        background: '#ffffff', // 白色
        text: '#333333'      // 深灰色
    }
}
```

### 深色主题

```javascript
{
    colors: {
        up: '#00ff88',       // 亮绿色
        down: '#ff4444',     // 亮红色
        grid: '#333333',     // 深灰色
        background: '#1a1a1a', // 深色
        text: '#ffffff'      // 白色
    }
}
```

## 错误处理

```javascript
try {
    const chart = KlineChart.create(container, options);
    const success = await chart.loadData('000001');
    
    if (!success) {
        console.error('数据加载失败');
    }
} catch (error) {
    console.error('图表创建失败:', error);
}
```

## 性能优化

1. **避免频繁创建销毁**: 重用图表实例
2. **合理设置数据量**: 避免一次性加载过多数据
3. **使用防抖**: 在窗口调整时避免频繁重绘
4. **及时销毁**: 页面卸载时调用destroy()方法

## 浏览器兼容性

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 演示页面

访问以下页面查看完整演示：

- 基本演示: http://127.0.0.1:5001/kline-demo
- 测试页面: http://127.0.0.1:5001/kline-test

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本K线图显示
- 支持成交量显示
- 支持主题切换
- 支持响应式设计

## 许可证

MIT License 