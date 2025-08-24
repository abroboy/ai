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
- **Web管理台**: 提供可视化的数据管理界面

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

编辑 `config.py` 文件中的数据库配置，或创建 `.env` 文件：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=pt
WEB_PORT=5002
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

- `news`: 新闻热点
- `policy`: 政策热点
- `industry`: 行业热点
- `company`: 公司热点
- `market`: 市场热点
- `economy`: 经济热点

## 测试

### 运行模块测试

```bash
python test_module.py
```

### 运行数据库测试

```bash
python hotspot_test.py
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

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持基础数据采集和处理
- 提供Web管理台
- 完整的API接口
