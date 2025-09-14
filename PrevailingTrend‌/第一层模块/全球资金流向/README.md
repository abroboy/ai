# 全球资金流向分析系统
数据都需要动态，最新的数据。 按照日期分布。
## 项目概述

全球资金流向分析系统是一个专门用于监控、分析和预测全球资金流向的综合平台。系统能够实时收集全球主要市场的资金流向数据，通过先进的算法进行分析，并提供直观的可视化展示和趋势预测。

要求：
数据拉取和展示做下分离。
 


## 主要功能

### 1. 数据收集
- **多数据源支持**: 外汇、股票、债券、大宗商品市场
- **实时数据采集**: 24/7不间断数据收集
- **数据质量保证**: 自动数据验证和清洗

### 2. 资金流向分析
- **全球趋势分析**: 分析全球整体资金流向趋势
- **市场分类分析**: 按地区、资产类别进行分析
- **行业板块分析**: 识别领涨领跌行业
- **技术指标计算**: RSI、MACD、布林带等

### 3. 趋势分析
- **短期趋势**: 7天趋势分析
- **中期趋势**: 30天趋势分析
- **长期趋势**: 90天趋势分析
- **趋势强度评估**: 量化趋势可靠性

### 4. 可视化展示
- **交互式图表**: 支持缩放、平移等操作
- **多种图表类型**: 柱状图、折线图、热力图、饼图
- **实时更新**: 数据变化时图表自动更新
- **移动端适配**: 支持手机和平板访问

### 5. 预测分析
- **趋势预测**: 预测未来资金流向趋势
- **市场预测**: 预测市场整体走势
- **行业预测**: 预测各行业表现
- **风险评估**: 量化预测风险

## 系统架构

```
全球资金流向分析系统/
├── config.py              # 配置文件
├── app.py                 # Flask Web应用
├── start.py               # 系统启动脚本
├── test_system.py         # 系统测试脚本
├── requirements.txt       # 依赖包列表
├── models/                # 数据模型
│   ├── __init__.py
│   ├── flow_model.py      # 资金流向数据模型
│   └── trend_model.py     # 趋势分析数据模型
├── core/                  # 核心功能模块
│   ├── __init__.py
│   ├── data_collector.py  # 数据收集器
│   ├── flow_analyzer.py   # 资金流向分析器
│   ├── trend_analyzer.py  # 趋势分析器
│   ├── visualizer.py      # 可视化器
│   └── predictor.py       # 预测器
├── utils/                 # 工具模块
│   ├── __init__.py
│   ├── database.py        # 数据库管理
│   └── logger.py          # 日志管理
├── api/                   # API接口
│   ├── __init__.py
│   └── flow_api.py        # 资金流向API
├── templates/             # 网页模板
│   ├── index.html         # 首页
│   └── dashboard.html     # 仪表盘
├── static/                # 静态文件
│   ├── charts/            # 图表文件
│   └── reports/           # 报告文件
└── logs/                  # 日志文件
```

## 安装和配置

### 1. 环境要求
- java 3.8+
- MySQL 5.7+
- 8GB+ RAM
- 100GB+ 存储空间

### 2. 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd 全球资金流向

# 2. 创建虚拟环境
java -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置数据库
# 编辑 config.py 中的数据库配置

# 5. 创建环境变量文件
cp env.example .env
# 编辑 .env 文件，填入数据库连接信息
```

### 3. 数据库配置

在 `config.py` 中配置数据库连接信息：

```java
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'your_username',
    'password': 'your_password',
    'database': 'prevailing_trend',
    'charset': 'utf8mb4'
}
```

## 使用方法

### 1. 启动系统

```bash
# 方式1: 使用启动脚本
java start.py

# 方式2: 直接启动Flask应用
java app.py
```

### 2. 访问系统

- **首页**: http://localhost:5003/
- **仪表盘**: http://localhost:5003/dashboard
- **API文档**: http://localhost:5003/api/

### 3. 系统测试

```bash
# 运行系统测试
java test_system.py
```

## API接口

### 数据收集
- `POST /api/collect_data` - 收集资金流向数据

### 分析接口
- `GET /api/analyze_flow` - 分析资金流向
- `GET /api/analyze_market` - 分析市场走势
- `GET /api/analyze_sector` - 分析行业表现

### 可视化接口
- `POST /api/create_charts` - 创建图表

### 预测接口
- `POST /api/predict` - 生成预测

### 系统状态
- `GET /api/status` - 获取系统状态

## 数据模型

### GlobalFlowData (全球资金流向数据)
- 时间戳、资产类型、资产名称、代码
- 价格数据（开高低收、成交量）
- 资金流向指标（净流入、流向比率、相对强度等）
- 市场情绪指标（恐慌贪婪指数、市场情绪）

### MarketFlowData (市场资金流向汇总)
- 市场类型、市场名称
- 总净流入、总成交量、平均流向比率
- 分类资金流向（股票、债券、外汇、大宗商品）
- 市场情绪、风险等级、趋势指标

### AssetFlowData (资产类别资金流向)
- 资产类别、类别名称
- 资金流向统计（总流入、总流出、净流入）
- 相对指标（流向比率、市场份额、相对表现）
- 风险指标（波动率、夏普比率、最大回撤）

## 配置说明

### 数据源配置
```java
DATA_SOURCES = {
    'forex': {
        'api_key': 'your_api_key',
        'base_url': 'https://api.exchangerate-api.com/v4/latest/',
        'currencies': ['USD', 'EUR', 'CNY', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF']
    },
    'stock_markets': {
        'us_markets': ['^GSPC', '^DJI', '^IXIC'],
        'asia_markets': ['^N225', '^HSI', '^KS11'],
        'europe_markets': ['^GDAXI', '^FCHI', '^FTSE']
    }
}
```

### 分析配置
```java
FLOW_ANALYSIS_CONFIG = {
    'time_windows': {
        'short_term': 7,      # 短期：7天
        'medium_term': 30,    # 中期：30天
        'long_term': 90       # 长期：90天
    },
    'thresholds': {
        'significant_flow': 0.05,   # 显著资金流向阈值（5%）
        'extreme_flow': 0.10,       # 极端资金流向阈值（10%）
        'trend_change': 0.03        # 趋势变化阈值（3%）
    }
}
```

## 监控和维护

### 1. 日志监控
- 日志文件位置: `logs/global_flow_analysis.log`
- 日志级别: INFO, WARNING, ERROR
- 日志轮转: 自动按大小轮转

### 2. 性能监控
- 数据库连接池监控
- API响应时间监控
- 内存和CPU使用率监控

### 3. 数据备份
- 定期数据库备份
- 配置文件备份
- 日志文件备份

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否启动
   - 验证连接参数是否正确
   - 确认网络连接正常

2. **数据收集失败**
   - 检查API密钥是否有效
   - 验证网络连接
   - 查看API配额是否超限

3. **图表生成失败**
   - 检查静态文件目录权限
   - 验证Plotly库是否正确安装
   - 确认数据格式是否正确

### 调试模式

```bash
# 启用调试模式
export FLASK_ENV=development
java app.py
```

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 基础数据收集功能
- 资金流向分析功能
- 可视化展示功能
- Web界面

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- 项目地址: [GitHub Repository URL]

## 致谢

感谢所有为这个项目做出贡献的开发者和用户。