## API接口说明

### 1. 预测接口

```
POST /api/predict
```

**请求参数**：
```json
{
  "data": [...],  // 时间序列数据，JSON数组或CSV字符串
  "date_column": "date",  // 日期列名
  "value_column": "value",  // 值列名
  "model_type": "arima",  // 模型类型，可选值为'arima', 'lstm', 'ensemble'
  "steps": 30  // 预测步数
}
```

**响应**：
```json
{
  "success": true,
  "data": [
    {
      "date": "2025-10-01",
      "prediction": 123.45,
      "lower_bound": 110.23,  // 仅ARIMA模型返回
      "upper_bound": 136.67   // 仅ARIMA模型返回
    },
    ...
  ],
  "chart_url": "/api/charts/prediction_20250926160000.png"
}
```

### 2. 模型管理接口

#### 2.1 创建模型

```
POST /api/models
```

**请求参数**：
```json
{
  "name": "股价预测模型",
  "type": "arima",
  "description": "用于预测股票价格的ARIMA模型",
  "data": [...],  // 训练数据
  "date_column": "date",
  "value_column": "price"
}
```

#### 2.2 获取模型列表

```
GET /api/models
```

#### 2.3 获取模型详情

```
GET /api/models/{model_id}
```

#### 2.4 删除模型

```
DELETE /api/models/{model_id}
```

#### 2.5 使用指定模型预测

```
POST /api/models/{model_id}/predict
```

**请求参数**：
```json
{
  "data": [...],  // 可选，如果不提供则使用训练数据
  "steps": 30
}
```

### 3. 图表接口

```
GET /api/charts/{filename}