# 国外热点数据模块
另外数据拉取和展示要分离，这样页面响应速度会快很多。

## 📋 模块概述

国外热点数据模块是一个专门用于收集、分析和展示国际热点信息的系统。该模块参考万得行业分类模块的架构，将数据拉取和展示分离，提供完整的Web界面和API接口。

## 🏗️ 架构设计

### 数据拉取与展示分离

- **数据收集服务** (`collect_data.py`) - 专门负责从国际数据源收集热点信息
- **展示服务** (`start.py`) - 专门负责数据展示和Web界面
- **API模块** (`api/`) - 提供RESTful API接口

### 目录结构

```
国外热点数据模块/
├── start.py                    # 展示服务启动脚本 (端口5004)
├── collect_data.py             # 数据收集脚本
├── config.py                   # 配置文件
├── api/                        # API模块
│   ├── __init__.py
│   └── hotspot_api.py          # 热点数据API
├── core/                       # 核心功能模块
│   ├── international_hotspot_collector.py    # 数据收集器
│   ├── international_hotspot_analyzer.py     # 数据分析器
│   └── international_hotspot_manager.py      # 数据管理器
├── models/                     # 数据模型
│   └── international_hotspot_model.py        # 热点数据模型
├── utils/                      # 工具模块
│   ├── database.py             # 数据库工具
│   └── logger.py               # 日志工具
├── templates/                  # 前端模板
│   ├── index.html              # 首页
│   └── dashboard.html          # 仪表盘
└── requirements.txt            # 依赖包列表
```

## 🚀 快速启动

### 1. 启动展示服务

```bash
cd 第一层模块/国外热点数据
java start.py
```

服务将在 http://localhost:5004 启动

### 2. 收集数据

```bash
java collect_data.py
```

### 3. 访问界面

- **首页**: http://localhost:5004
- **仪表盘**: http://localhost:5004/dashboard

## 📊 功能特性

### 数据收集
- 支持多个国际数据源：Reuters、Bloomberg、Financial Times、Wall Street Journal、CNBC等
- 自动数据解析和清洗
- 智能关键词提取和情感分析
- 热度计算和评分

### 数据展示
- 实时统计信息
- 热点数据列表
- 按类型和地区筛选
- 响应式Web界面

### API接口
- `/api/health` - 健康检查
- `/api/statistics` - 统计数据
- `/api/hotspots` - 热点数据列表

## 📈 数据统计

当前模块已成功收集：
- **总数据量**: 28条
- **新闻热点**: 7条
- **政策热点**: 21条
- **全球数据**: 8条
- **美国数据**: 17条

## 🔧 配置说明

### 数据库配置
```java
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}
```

### 数据源配置
支持以下类型的数据源：
- **新闻媒体**: Reuters、Bloomberg、Financial Times等
- **政策机构**: IMF、World Bank、Federal Reserve等
- **地区覆盖**: 全球、美国、欧洲、英国、亚洲

## 📝 使用示例

### 获取统计数据
```bash
curl http://localhost:5004/api/statistics
```

### 获取热点数据
```bash
curl http://localhost:5004/api/hotspots?limit=10
```

### 健康检查
```bash
curl http://localhost:5004/api/health
```

## 🎯 服务端口

国外热点数据模块使用 **端口5004**，与其他模块保持一致：
- 万得行业分类: 5001
- 国内热点数据: 5002  
- 全球资金流向: 5003
- **国外热点数据: 5004** ✅

## 📚 技术栈

- **后端**: java + Flask
- **数据库**: MySQL
- **前端**: Bootstrap + JavaScript
- **数据收集**: Requests + BeautifulSoup
- **日志**: Loguru

## 🔄 数据流程

1. **数据收集** → 从国际数据源抓取热点信息
2. **数据分析** → 关键词提取、情感分析、热度计算
3. **数据存储** → 存储到MySQL数据库
4. **数据展示** → 通过Web界面和API展示

## 📞 支持

如有问题或需要技术支持，请查看日志文件或联系开发团队。