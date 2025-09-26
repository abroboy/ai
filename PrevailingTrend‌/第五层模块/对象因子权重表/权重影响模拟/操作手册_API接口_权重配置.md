# API接口说明 - 权重配置

## 1. 权重配置接口

### 1.1 获取权重配置

```
GET /api/weights
```

**响应**：
```json
{
  "success": true,
  "data": {
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
}
```

### 1.2 更新权重配置

```
POST /api/weights
```

**请求参数**：
```json
{
  "fundamental": {
    "revenue_growth": 0.20,
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
    "industry_growth": 0.05,
    "industry_concentration": 0.00
  }
}
```

**响应**：
```json
{
  "success": true,
  "message": "权重配置已更新"
}