# 国内热点数据模块

## 模块概述

国内热点数据模块负责收集、分析和处理国内市场的热点信息，包括新闻热点、政策热点、市场热点等。该模块为整个大势所趋风险框架提供国内市场的热点信息基础。

## 功能特性

- **多源数据采集**: 支持新闻网站、政策发布平台、市场数据源等
- **热点识别**: 自动识别和分类热点信息
- **情感分析**: 对热点信息进行情感倾向分析
- **热度评估**: 评估热点信息的热度级别
- **关联分析**: 分析热点与公司、行业的关联关系
- **实时更新**: 支持实时数据更新和监控

## 项目结构

```
国内热点数据/
├── __init__.py              # 模块初始化
├── README.md               # 项目说明
├── requirements.txt        # 依赖包列表
├── config.py              # 配置文件
├── main.py                # 主程序入口
├── models/                # 数据模型
│   ├── __init__.py
│   └── hotspot_model.py   # 热点数据模型
├── core/                  # 核心业务逻辑
│   ├── __init__.py
│   ├── hotspot_collector.py   # 热点数据采集器
│   ├── hotspot_analyzer.py    # 热点数据分析器
│   └── hotspot_manager.py     # 热点数据管理器
├── api/                   # API接口
│   ├── __init__.py
│   └── hotspot_api.py     # 热点数据API
├── utils/                 # 工具类
│   ├── __init__.py
│   ├── logger.py          # 日志管理
│   └── database.py        # 数据库管理
└── tests/                 # 测试文件
    ├── __init__.py
    └── test_hotspot.py    # 热点数据测试
```

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv
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
# 启动热点数据采集
python main.py --action collect

# 启动热点数据分析
python main.py --action analyze

# 启动API服务
python main.py --action api
```

## 数据模型

### HotspotModel - 热点数据模型

```python
@dataclass
class HotspotModel:
    hotspot_id: str          # 热点ID
    title: str              # 热点标题
    content: str            # 热点内容
    hotspot_type: HotspotType  # 热点类型
    hotspot_level: HotspotLevel  # 热点级别
    status: HotspotStatus   # 热点状态
    source: str             # 数据来源
    url: Optional[str]      # 原始链接
    publish_time: Optional[datetime]  # 发布时间
    keywords: List[str]     # 关键词列表
    related_companies: List[str]  # 相关公司列表
    related_industries: List[str]  # 相关行业列表
    sentiment_score: Optional[float]  # 情感得分
    heat_score: Optional[float]  # 热度得分
```

## API接口

### 热点数据接口

- `GET /api/hotspots` - 获取热点列表
- `GET /api/hotspots/{id}` - 获取热点详情
- `GET /api/hotspots/search` - 搜索热点
- `GET /api/hotspots/statistics` - 获取统计信息
- `POST /api/hotspots/collect` - 触发数据采集

## 配置说明

### 数据源配置

```python
# 新闻网站配置
NEWS_SOURCES = [
    "http://www.xinhuanet.com/",
    "http://www.people.com.cn/",
    "http://www.cctv.com/"
]

# 政策发布平台配置
POLICY_SOURCES = [
    "http://www.gov.cn/",
    "http://www.ndrc.gov.cn/"
]

# 市场数据源配置
MARKET_SOURCES = [
    "http://www.sse.com.cn/",
    "http://www.szse.cn/"
]
```

### 采集配置

```python
# 采集频率配置
COLLECTION_INTERVAL = 3600  # 1小时
ANALYSIS_INTERVAL = 1800    # 30分钟

# 数据存储配置
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "database": "hotspot_data",
    "username": "root",
    "password": "password"
}
```

## 使用示例

### 数据采集

```python
from 国内热点数据 import HotspotCollector

# 创建采集器
collector = HotspotCollector()

# 采集新闻热点
news_hotspots = collector.collect_news_hotspots()

# 采集政策热点
policy_hotspots = collector.collect_policy_hotspots()

# 采集市场热点
market_hotspots = collector.collect_market_hotspots()
```

### 数据分析

```python
from 国内热点数据 import HotspotAnalyzer

# 创建分析器
analyzer = HotspotAnalyzer()

# 情感分析
sentiment_results = analyzer.analyze_sentiment(hotspots)

# 热度评估
heat_results = analyzer.evaluate_heat(hotspots)

# 关联分析
relation_results = analyzer.analyze_relations(hotspots)
```

### 数据管理

```python
from 国内热点数据 import HotspotManager

# 创建管理器
manager = HotspotManager()

# 保存热点数据
manager.save_hotspots(hotspots)

# 查询热点数据
hotspots = manager.get_hotspots_by_type("news")

# 更新热点状态
manager.update_hotspot_status(hotspot_id, "expired")
```

## 监控和维护

### 日志监控

```bash
# 查看采集日志
tail -f logs/hotspot_collector.log

# 查看分析日志
tail -f logs/hotspot_analyzer.log

# 查看API日志
tail -f logs/hotspot_api.log
```

### 数据监控

```bash
# 检查数据质量
python -m 国内热点数据.scripts.monitor --check data_quality

# 检查采集状态
python -m 国内热点数据.scripts.monitor --check collection_status

# 检查API状态
python -m 国内热点数据.scripts.monitor --check api_status
```

## 开发指南

### 添加新的数据源

1. 在 `core/hotspot_collector.py` 中添加新的采集方法
2. 实现数据解析和清洗逻辑
3. 添加相应的测试用例
4. 更新配置文件

### 扩展分析功能

1. 在 `core/hotspot_analyzer.py` 中添加新的分析方法
2. 实现分析算法
3. 添加相应的测试用例
4. 更新API接口

### 自定义配置

1. 修改 `config.py` 中的配置项
2. 添加环境变量支持
3. 更新文档说明

## 故障排除

### 常见问题

1. **数据采集失败**
   - 检查网络连接
   - 验证数据源配置
   - 查看错误日志

2. **分析结果异常**
   - 检查数据质量
   - 验证分析参数
   - 查看分析日志

3. **API服务异常**
   - 检查服务状态
   - 验证端口配置
   - 查看服务日志

### 性能优化

1. **采集性能**
   - 使用异步采集
   - 实现并发控制
   - 优化数据解析

2. **分析性能**
   - 使用缓存机制
   - 实现增量分析
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