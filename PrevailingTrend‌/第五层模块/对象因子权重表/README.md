# 对象因子权重表模块

## 模块概述

对象因子权重表模块是第五层的核心组件，负责管理和配置各种因子的权重，为行业和公司评分提供基础。本模块包含权重配置、权重影响模拟等功能，支持动态调整权重并观察对排名的影响。

## 子模块

### 1. 权重影响模拟

权重影响模拟子模块提供了一套完整的工具，用于模拟不同权重配置对行业和公司排名的影响。通过调整各因子权重，可以观察排名变化，帮助用户找到最优的权重配置。

详细功能包括：
- 权重调整模拟
- 行业排名模拟
- 公司排名模拟
- 模拟结果比较
- 可视化分析
- REST API接口

详细使用方法请参考 [权重影响模拟操作手册](./权重影响模拟/操作手册.md)。

## 数据结构

对象因子权重表模块使用以下数据结构：

### 1. 权重配置

权重配置采用JSON格式，支持嵌套结构：

```json
{
  "fundamental": {
    "revenue_growth": 0.15,
    "profit_margin": 0.15,
    "debt_ratio": 0.10,
    "cash_flow": 0.10
  },
  "market": {
    "price_momentum": 0.10,
    "volatility": 0.05,
    "liquidity": 0.05
  },
  "sentiment": {
    "analyst_rating": 0.10,
    "social_media": 0.05,
    "news_sentiment": 0.05
  },
  "industry": {
    "industry_growth": 0.10,
    "industry_concentration": 0.05
  }
}
```

### 2. 行业数据

行业数据包含以下字段：
- `industry_code`：行业代码
- `industry_name`：行业名称
- 各因子得分字段：如 `revenue_growth`、`profit_margin` 等
- `total_score`：总分
- `rank`：排名

### 3. 公司数据

公司数据包含以下字段：
- `company_code`：公司代码
- `company_name`：公司名称
- `industry_code`：所属行业代码
- `industry_name`：所属行业名称
- 各因子得分字段：如 `revenue_growth`、`profit_margin` 等
- `total_score`：总分
- `rank`：排名

## 与其他模块的集成

对象因子权重表模块与其他模块的集成关系如下：

1. **与第四层模块的集成**：
   - 接收第四层模块提供的行业分值表、公司分值表和行业+公司分值表数据
   - 根据配置的权重计算总分并生成排名

2. **与第六层模块的集成**：
   - 向第六层模块提供权重配置和排名数据
   - 接收第六层模块的预测结果，用于优化权重配置

## API接口

对象因子权重表模块提供以下API接口：

1. **权重配置接口**：
   - `GET /api/weights`：获取当前权重配置
   - `POST /api/weights`：更新权重配置

2. **行业排名接口**：
   - `POST /api/industry/simulate`：模拟权重调整对行业排名的影响
   - `POST /api/industry/compare`：比较多个行业模拟结果
   - `GET /api/industry/chart/{simulation_id}`：获取行业排名图表

3. **公司排名接口**：
   - `POST /api/company/simulate`：模拟权重调整对公司排名的影响
   - `POST /api/company/compare`：比较多个公司模拟结果
   - `GET /api/company/chart/{simulation_id}`：获取公司排名图表

4. **可视化接口**：
   - `POST /api/visualization/impact`：可视化权重调整对特定行业或公司的影响
   - `GET /api/visualization/weight_distribution`：可视化权重分布

详细API文档请参考 [API接口文档](./权重影响模拟/操作手册_API接口_权重配置.md)。