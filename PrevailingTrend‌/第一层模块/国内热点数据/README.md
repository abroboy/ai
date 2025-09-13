# 国内热点数据模块
数据都需要动态，最新的数据。 按照日期分布。
## 模块概述

国内热点数据模块负责收集、分析和处理国内市场的热点信息，包括新闻热点、政策热点、市场热点等。该模块为整个大势所趋风险框架提供国内市场的热点信息基础。

## 功能特性

- **真实数据采集**: 通过API接口实时获取真实热点数据，支持多种数据源
- **智能数据转换**: 自动将原始数据转换为标准格式，支持数据清洗和转换
- **多源数据采集**: 支持50+个数据源，涵盖新闻媒体、政府部门、行业协会、交易所等
- **热点识别**: 自动识别和分类热点信息（新闻、政策、行业、市场、公司）
- **情感分析**: 对热点信息进行情感倾向分析
- **热度评估**: 评估热点信息的热度级别
- **关联分析**: 分析热点与公司、行业的关联关系
- **实时更新**: 支持实时数据更新和监控
- **Web管理台**: 提供可视化的数据管理界面
- **详情查看**: 支持点击查看热点详细内容
- **排序功能**: 支持按标题、热度、情感、来源、发布时间等字段排序
- **备用机制**: 当真实数据不可用时，自动使用模拟数据作为备用

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

复制环境变量示例文件并配置：

```bash
cp env.example .env
```

编辑 `.env` 文件，配置数据库和API密钥：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=pt

# Web服务配置
WEB_PORT=5002
WEB_DEBUG=false

# API密钥配置 - 请填入真实的API密钥
NEWS_API_KEY=your_news_api_key_here
TUSHARE_TOKEN=your_tushare_token_here
AKSHARE_TOKEN=your_akshare_token_here
TIANAPI_KEY=your_tianapi_key_here
JISUAPI_KEY=your_jisuapi_key_here
```

### 3. 启动服务

```bash
# 启动完整服务（包括数据采集和Web管理台）
python start.py

# 或仅启动Web服务
python app.py
```

### 4. 访问管理台

打开浏览器访问：`http://localhost:5002`

## 系统架构

```
国内热点数据模块/
├── config.py              # 配置文件
├── app.py                 # Web应用
├── start.py               # 启动脚本
├── test_module.py         # 模块测试
├── requirements.txt       # 依赖包
├── README.md             # 说明文档
├── 操作手册.md           # 操作手册
├── core/                 # 核心模块
│   ├── __init__.py
│   ├── data_collector.py # 数据采集器
│   └── data_processor.py # 数据处理器
├── models/               # 数据模型
│   ├── __init__.py
│   └── hotspot_model.py  # 热点数据模型
├── utils/                # 工具模块
│   ├── __init__.py
│   └── database.py       # 数据库工具
├── templates/            # Web模板
│   ├── index.html        # 主页面
│   └── dashboard.html    # 仪表盘
├── static/               # 静态资源
│   └── js/
│       └── dashboard.js  # 前端脚本
└── logs/                 # 日志目录
```

## 核心组件

### 1. 数据采集器 (DataCollector)

负责从各种数据源采集热点信息：

- 新闻网站：新浪财经、东方财富、证券时报等
- 政策平台：中国政府网、发改委等
- 支持自定义数据源配置

### 2. 数据处理器 (DataProcessor)

负责热点数据的分析和处理：

- 关键词提取
- 情感分析
- 热度计算
- 关联分析
- 数据过滤和统计

### 3. 数据模型 (HotspotModel)

定义热点信息的数据结构：

- 热点基本信息（标题、内容、类型等）
- 分析结果（热度、情感、关键词等）
- 关联信息（公司、行业等）
- 元数据（时间、状态等）

### 4. Web管理台

提供可视化的数据管理界面：

- 仪表盘：数据概览和统计图表
- 热点列表：数据查看和筛选
- 统计分析：趋势分析和报告
- 数据采集：手动采集和监控
- 系统设置：配置管理

## API接口

### 热点数据接口

- `GET /api/hotspots` - 获取热点列表
- `GET /api/hotspots/{id}` - 获取热点详情
- `PUT /api/hotspots/{id}` - 更新热点数据
- `DELETE /api/hotspots/{id}` - 删除热点数据

### 统计接口

- `GET /api/statistics` - 获取统计信息

### 采集接口

- `POST /api/collect` - 手动触发数据采集

## 数据模型

### 热点数据表 (l1_domestic_hotspot_data)

| 字段 | 类型 | 说明 |
|------|------|------|
| hotspot_id | VARCHAR(100) | 热点ID |
| title | VARCHAR(500) | 热点标题 |
| content | TEXT | 热点内容 |
| hotspot_type | VARCHAR(20) | 热点类型 |
| hotspot_level | VARCHAR(20) | 热度级别 |
| status | VARCHAR(20) | 状态 |
| source | VARCHAR(100) | 数据来源 |
| sentiment_score | DECIMAL(3,2) | 情感得分 |
| heat_score | DECIMAL(5,2) | 热度得分 |

### 热点类型

- `news`: 新闻热点 (40%)
- `policy`: 政策热点 (25%)
- `industry`: 行业热点 (15%)
- `market`: 市场热点 (10%)
- `company`: 公司热点 (10%)

### 数据源分类

#### 新闻媒体 (30个)
- 主流财经媒体：新浪财经、东方财富、证券时报、财新网、第一财经等
- 专业财经媒体：21世纪经济报道、经济观察报、中国证券报、上海证券报等
- 综合财经平台：凤凰网财经、腾讯财经、网易财经、搜狐财经等
- 国际媒体：彭博社中文、路透社中文、华尔街日报中文等

#### 政府部门 (20个)
- 国务院及各部委：中国政府网、发改委、央行、证监会、银保监会等
- 专业监管机构：财政部、工信部、商务部、科技部等

#### 行业协会 (20个)
- 工业协会：中国汽车工业协会、中国钢铁工业协会、中国有色金属工业协会等
- 金融协会：中国银行业协会、中国证券业协会、中国保险行业协会等

#### 交易所 (10个)
- 证券交易所：上海证券交易所、深圳证券交易所、北京证券交易所等
- 期货交易所：中国金融期货交易所、上海期货交易所、郑州商品交易所等

## 测试

### 运行模块测试

```bash
python test_module.py
```

### 运行数据库测试

```bash
python hotspot_test.py
```

### 运行真实数据采集测试

```bash
python test_real_data.py
```

### 运行排序功能测试

```bash
python test_sorting.py
```

### 运行大规模数据生成测试

```bash
python test_large_data.py
```

### 测试结果示例

```
开始测试大规模数据生成...
成功生成 149 条热点数据

=== 数据统计 ===
按类型分布:
  news: 60 条
  policy: 37 条
  industry: 22 条
  market: 15 条
  company: 15 条

按级别分布:
  high: 57 条
  medium: 55 条
  very_high: 37 条

数据源数量: 31 个
主要数据源:
  上海证券报: 10 条
  21世纪经济报道: 9 条
  东方财富: 9 条
  第一财经: 9 条
  央行: 8 条

=== 数据质量检查 ===
平均标题长度: 18.8 字符
平均内容长度: 62.5 字符
平均情感得分: 0.24
平均热度得分: 60.8

关键词总数: 464
热门关键词:
  市场: 115 次
  发展: 73 次
  增长: 65 次
  政策: 37 次
  经济: 34 次
```

## 配置说明

### 数据源配置

在 `config.py` 中配置数据源：

```python
DATA_SOURCES = {
    'news_sources': [
        {
            'name': '新浪财经',
            'url': 'https://finance.sina.com.cn/',
            'type': 'news',
            'enabled': True
        }
    ]
}
```

### 分析配置

配置分析参数：

```python
ANALYSIS = {
    'sentiment_analysis': {
        'enabled': True,
        'threshold': 0.3
    },
    'heat_calculation': {
        'enabled': True,
        'factors': ['read_count', 'comment_count', 'share_count', 'time_decay']
    }
}
```

## 监控和维护

### 日志监控

日志文件：`logs/hotspot.log`

### 数据库监控

```sql
-- 查看数据统计
SELECT COUNT(*) FROM l1_domestic_hotspot_data;
SELECT hotspot_type, COUNT(*) FROM l1_domestic_hotspot_data GROUP BY hotspot_type;
```

### 性能监控

- 数据采集频率和成功率
- 数据库连接状态
- Web服务响应时间

## 扩展开发

### 添加新数据源

1. 在 `config.py` 中添加数据源配置
2. 在 `data_collector.py` 中实现采集逻辑
3. 测试采集功能

### 优化分析算法

1. 修改 `data_processor.py` 中的分析逻辑
2. 调整配置参数
3. 验证分析结果

### 扩展Web功能

1. 在 `app.py` 中添加新的API接口
2. 创建对应的前端页面
3. 更新路由配置

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否启动
   - 验证连接参数是否正确

2. **数据采集失败**
   - 检查网络连接
   - 验证目标网站是否可访问

3. **Web服务无法访问**
   - 检查端口是否被占用
   - 验证防火墙设置

## 联系支持

如有问题或建议，请联系开发团队。

## 更新日志

### v1.1.0 (2024-08-24)
- 大幅扩展数据源至50+个
- 实现大规模数据生成，每日150+条热点
- 修复热点详情查看功能
- 优化数据分类和分布
- 增加数据质量检查功能
- 完善筛选器和统计功能

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持基础数据采集和处理
- 提供Web管理台
- 完整的API接口
