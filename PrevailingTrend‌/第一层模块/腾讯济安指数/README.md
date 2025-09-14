# 腾讯济安指数模块
数据都需要动态，最新的数据。 按照日期分布。

## 模块概述

腾讯济安指数模块负责收集、分析和处理腾讯济安指数相关数据，包括指数数据、成分股信息、历史走势等。该模块为整个大势所趋风险框架提供指数分析基础。

## 功能特性

- **指数数据采集**: 实时采集腾讯济安指数数据
- **成分股管理**: 管理指数成分股信息
- **历史数据分析**: 分析指数历史走势
- **技术指标计算**: 计算各种技术指标
- **风险分析**: 分析指数风险特征
- **相关性分析**: 分析与其他指数的相关性

## 项目结构

```
腾讯济安指数/
├── __init__.py              # 模块初始化
├── README.md               # 项目说明
├── requirements.txt        # 依赖包列表
├── config.py              # 配置文件
├── main.py                # 主程序入口
├── models/                # 数据模型
│   ├── __init__.py
│   └── index_model.py     # 指数数据模型
├── core/                  # 核心业务逻辑
│   ├── __init__.py
│   ├── index_collector.py    # 指数数据采集器
│   ├── index_analyzer.py     # 指数数据分析器
│   └── index_manager.py      # 指数数据管理器
├── api/                   # API接口
│   ├── __init__.py
│   └── index_api.py       # 指数数据API
├── utils/                 # 工具类
│   ├── __init__.py
│   ├── logger.py          # 日志管理
│   └── database.py        # 数据库管理
└── tests/                 # 测试文件
    ├── __init__.py
    └── test_index.py      # 指数数据测试
```

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
java -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置设置

```bash
# 复制配置文件
cp config.example.py config.py
# 编辑配置文件
vim config.py
```

### 3. 运行程序

```bash
# 启动指数数据采集
java main.py --action collect

# 启动指数数据分析
java main.py --action analyze

# 启动API服务
java main.py --action api
```

## 数据模型

### IndexModel - 指数数据模型

```java
@dataclass
class IndexModel:
    index_code: str         # 指数代码
    index_name: str         # 指数名称
    current_value: float    # 当前值
    change_value: float     # 涨跌值
    change_rate: float      # 涨跌幅
    open_value: float       # 开盘值
    high_value: float       # 最高值
    low_value: float        # 最低值
    volume: int             # 成交量
    turnover: float         # 成交额
    pe_ratio: float         # 市盈率
    pb_ratio: float         # 市净率
    dividend_yield: float   # 股息率
    update_time: datetime   # 更新时间
    trading_date: date      # 交易日期
```

## API接口

### 指数数据接口

- `GET /api/index/current` - 获取当前指数数据
- `GET /api/index/history` - 获取历史指数数据
- `GET /api/index/components` - 获取成分股信息
- `GET /api/index/statistics` - 获取统计信息
- `GET /api/index/analysis` - 获取分析结果
- `POST /api/index/collect` - 触发数据采集

## 配置说明

### 数据源配置

```java
# 腾讯济安指数数据源
TENCENT_INDEX_SOURCES = {
    "base_url": "https://stock.gtimg.cn/",
    "api_endpoints": {
        "current": "data/index.php",
        "history": "data/history.php",
        "components": "data/components.php"
    }
}

# 数据采集配置
COLLECTION_CONFIG = {
    "interval": 60,  # 采集间隔（秒）
    "retry_times": 3,  # 重试次数
    "timeout": 30   # 超时时间
}
```

## 使用示例

### 数据采集

```java
from 腾讯济安指数 import IndexCollector

# 创建采集器
collector = IndexCollector()

# 采集当前指数数据
current_data = collector.collect_current_index()

# 采集历史指数数据
history_data = collector.collect_history_index()

# 采集成分股数据
components_data = collector.collect_components()
```

### 数据分析

```java
from 腾讯济安指数 import IndexAnalyzer

# 创建分析器
analyzer = IndexAnalyzer()

# 技术指标分析
technical_indicators = analyzer.calculate_technical_indicators(history_data)

# 风险分析
risk_analysis = analyzer.analyze_risk(history_data)

# 相关性分析
correlation_analysis = analyzer.analyze_correlation(history_data)
```

### 数据管理

```java
from 腾讯济安指数 import IndexManager

# 创建管理器
manager = IndexManager()

# 保存指数数据
manager.save_index_data(index_data)

# 查询历史数据
history_data = manager.get_history_data(start_date, end_date)

# 更新成分股信息
manager.update_components(components_data)
```

## 监控和维护

### 日志监控

```bash
# 查看采集日志
tail -f logs/index_collector.log

# 查看分析日志
tail -f logs/index_analyzer.log

# 查看API日志
tail -f logs/index_api.log
```

### 数据监控

```bash
# 检查数据质量
java -m 腾讯济安指数.scripts.monitor --check data_quality

# 检查采集状态
java -m 腾讯济安指数.scripts.monitor --check collection_status

# 检查API状态
java -m 腾讯济安指数.scripts.monitor --check api_status
```

## 开发指南

### 添加新的指数

1. 在配置文件中添加新指数配置
2. 实现相应的数据采集逻辑
3. 添加分析算法
4. 更新测试用例

### 扩展分析功能

1. 在分析器中添加新的分析方法
2. 实现技术指标计算
3. 添加风险分析算法
4. 更新API接口

### 自定义配置

1. 修改配置文件中的参数
2. 添加环境变量支持
3. 更新文档说明

## 故障排除

### 常见问题

1. **数据采集失败**
   - 检查网络连接
   - 验证API接口
   - 查看错误日志

2. **数据异常**
   - 检查数据格式
   - 验证数据完整性
   - 查看数据日志

3. **分析结果异常**
   - 检查输入数据
   - 验证算法参数
   - 查看分析日志

### 性能优化

1. **采集性能**
   - 使用异步采集
   - 实现缓存机制
   - 优化网络请求

2. **分析性能**
   - 使用向量化计算
   - 实现并行处理
   - 优化算法效率

3. **存储性能**
   - 使用数据库索引
   - 实现数据分区
   - 优化查询语句

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。 