# API接口说明 - 公司排名

## 1. 公司排名接口

### 1.1 模拟公司排名

```
POST /api/company/simulate
```

**请求参数**：
```json
{
  "industry_code": "BK0001",  // 可选，如果不提供则模拟所有公司
  "weight_adjustments": {
    "fundamental.revenue_growth": 0.20,
    "industry.industry_growth": 0.05
  }
}
```

**响应**：
```json
{
  "success": true,
  "simulation_id": "company_BK0001_20250926160000",
  "data": [
    {
      "company_code": "000001",
      "company_name": "平安银行",
      "industry_code": "BK0001",
      "industry_name": "农林牧渔",
      "revenue_growth": 0.85,
      "profit_margin": 0.72,
      "debt_ratio": 0.65,
      "cash_flow": 0.78,
      "price_momentum": 0.62,
      "volatility": 0.45,
      "liquidity": 0.55,
      "analyst_rating": 0.68,
      "social_media": 0.72,
      "news_sentiment": 0.65,
      "industry_growth": 0.82,
      "industry_concentration": 0.45,
      "total_score": 0.6925,
      "rank": 1
    },
    ...
  ]
}
```

### 1.2 比较公司模拟结果

```
POST /api/company/compare
```

**请求参数**：
```json
{
  "simulation_ids": ["company_BK0001_20250926160000", "company_BK0001_20250926160100"]
}
```

**响应**：
```json
{
  "success": true,
  "data": {
    "base": {
      "id": "company_BK0001_20250926160000",
      "weights": {
        "revenue_growth": 0.20,
        "profit_margin": 0.15,
        "debt_ratio": 0.10,
        "cash_flow": 0.10,
        "price_momentum": 0.10,
        "volatility": 0.05,
        "liquidity": 0.05,
        "analyst_rating": 0.10,
        "social_media": 0.05,
        "news_sentiment": 0.05,
        "industry_growth": 0.05,
        "industry_concentration": 0.00
      },
      "adjustments": {
        "fundamental.revenue_growth": 0.20,
        "industry.industry_growth": 0.05
      },
      "result": [...]
    },
    "sim_1": {
      "id": "company_BK0001_20250926160100",
      "weights": {
        "revenue_growth": 0.15,
        "profit_margin": 0.20,
        "debt_ratio": 0.10,
        "cash_flow": 0.10,
        "price_momentum": 0.10,
        "volatility": 0.05,
        "liquidity": 0.05,
        "analyst_rating": 0.10,
        "social_media": 0.05,
        "news_sentiment": 0.05,
        "industry_growth": 0.05,
        "industry_concentration": 0.00
      },
      "adjustments": {
        "fundamental.profit_margin": 0.20,
        "fundamental.revenue_growth": 0.15
      },
      "result": [...],
      "changes": [
        {
          "company_code": "000001",
          "rank_base": 1,
          "rank_1": 2,
          "rank_change": 1
        },
        ...
      ]
    }
  }
}
```

### 1.3 获取公司排名图表

```
GET /api/company/chart/{simulation_id}?industry_code=BK0001&top_n=20
```

**参数**：
- `simulation_id`：模拟ID
- `industry_code`：行业代码，可选
- `top_n`：显示前N个公司，默认为20

**响应**：
返回PNG格式的图表