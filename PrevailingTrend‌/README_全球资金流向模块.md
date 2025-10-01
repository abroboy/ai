# 全球资金流向模块

## 功能概述

全球资金流向模块是大势所趋风险框架管理台的核心功能之一，提供实时的资金流向数据监控和分析功能。

## 主要功能

### 1. 数据展示
- **实时数据概览**: 显示主力净流入、超大单净流入、大单净流入等关键指标
- **趋势图表**: 提供资金流向的时间序列图表分析
- **分布图表**: 展示不同类型资金的分布情况
- **详细数据表**: 提供完整的历史数据查询和分页功能

### 2. 数据来源
- 支持从CSV文件读取历史数据
- 提供API接口服务，支持实时数据获取
- 自动降级机制：API不可用时自动切换到CSV数据源

### 3. 交互功能
- 数据刷新和导出
- 时间范围筛选（7天、30天、90天）
- 分页浏览
- 响应式设计，支持移动端

## 文件结构

```
管理台/
├── static/
│   ├── js/
│   │   └── global_capital_flow.js     # 主要JavaScript逻辑
│   └── css/
│       ├── style.css                  # 基础样式
│       └── global_capital_flow.css    # 模块专用样式
├── api/
│   ├── global_capital_flow_api.py     # API服务器
│   ├── akshare_test_ak_stock_market_fund_flow.csv    # 市场数据
│   └── akshare_test_ak_stock_individual_fund_flow.csv # 个股数据
├── index.html                         # 主页面
├── start_api_server.py               # API服务启动器
└── README_全球资金流向模块.md         # 本文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install flask flask-cors pandas
```

### 2. 启动API服务

```bash
python start_api_server.py
```

或者直接启动API服务：

```bash
cd api
python global_capital_flow_api.py
```

### 3. 访问管理台

打开浏览器访问 `index.html`，点击"全球资金流向"模块即可使用。

## API接口

### 基础URL
```
http://localhost:5001
```

### 接口列表

#### 1. 获取市场资金流向数据
```
GET /api/global_capital_flow/market_data
```

参数：
- `days` (可选): 获取最近N天的数据，默认30天

响应示例：
```json
{
    "success": true,
    "message": "数据获取成功",
    "data": [
        {
            "date": "2025-09-30",
            "shanghai_close": 3882.78,
            "shanghai_change": 0.52,
            "main_net_inflow": -37912899584.0,
            "super_large_inflow": -21874024448.0,
            ...
        }
    ],
    "total": 30
}
```

#### 2. 获取个股资金流向数据
```
GET /api/global_capital_flow/individual_data
```

#### 3. 获取资金流向汇总数据
```
GET /api/global_capital_flow/summary
```

#### 4. 健康检查
```
GET /api/global_capital_flow/health
```

## 数据字段说明

### 市场数据字段
- `date`: 日期
- `shanghai_close`: 上证指数收盘价
- `shanghai_change`: 上证指数涨跌幅
- `shenzhen_close`: 深证指数收盘价
- `shenzhen_change`: 深证指数涨跌幅
- `main_net_inflow`: 主力净流入金额
- `main_net_inflow_ratio`: 主力净流入占比
- `super_large_inflow`: 超大单净流入金额
- `super_large_inflow_ratio`: 超大单净流入占比
- `large_inflow`: 大单净流入金额
- `large_inflow_ratio`: 大单净流入占比
- `medium_inflow`: 中单净流入金额
- `medium_inflow_ratio`: 中单净流入占比
- `small_inflow`: 小单净流入金额
- `small_inflow_ratio`: 小单净流入占比

## 技术特性

### 前端技术
- **JavaScript ES6+**: 使用现代JavaScript语法
- **Chart.js**: 图表绘制库
- **Bootstrap 5**: UI框架
- **响应式设计**: 支持各种屏幕尺寸

### 后端技术
- **Flask**: Python Web框架
- **Pandas**: 数据处理库
- **CORS支持**: 跨域请求支持

### 数据处理
- **CSV解析**: 支持CSV格式数据读取
- **数据转换**: 自动处理数据类型转换
- **错误处理**: 完善的异常处理机制

## 自定义配置

### 修改API端口
在 `api/global_capital_flow_api.py` 文件中修改：
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # 修改port参数
```

### 修改数据文件路径
在 `api/global_capital_flow_api.py` 文件中修改：
```python
MARKET_FUND_FLOW_FILE = 'your_market_data.csv'
INDIVIDUAL_FUND_FLOW_FILE = 'your_individual_data.csv'
```

### 修改图表样式
在 `static/css/global_capital_flow.css` 文件中自定义样式。

## 故障排除

### 1. API服务无法启动
- 检查Python环境和依赖包是否正确安装
- 确认端口5001未被占用
- 查看控制台错误信息

### 2. 数据无法加载
- 确认CSV数据文件存在且格式正确
- 检查API服务是否正常运行
- 查看浏览器控制台错误信息

### 3. 图表不显示
- 确认Chart.js库已正确加载
- 检查数据格式是否正确
- 查看浏览器控制台错误信息

## 扩展开发

### 添加新的数据源
1. 在API中添加新的数据加载函数
2. 创建对应的API接口
3. 在前端JavaScript中调用新接口

### 添加新的图表类型
1. 在JavaScript中添加新的图表渲染函数
2. 在HTML中添加对应的canvas元素
3. 在CSS中添加样式

### 添加数据导出功能
1. 在API中添加数据导出接口
2. 在前端添加导出按钮和处理逻辑

## 版本历史

- **v1.0.0** (2025-10-01): 初始版本，包含基础功能
  - 数据展示和图表
  - API接口服务
  - 响应式设计

## 联系方式

如有问题或建议，请联系开发团队。