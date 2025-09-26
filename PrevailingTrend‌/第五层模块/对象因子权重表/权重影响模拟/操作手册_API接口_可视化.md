# API接口说明 - 可视化

## 1. 可视化接口

### 1.1 可视化权重调整对特定行业或公司的影响

```
POST /api/visualization/impact
```

**请求参数**：
```json
{
  "simulation_ids": ["industry_20250926160000", "industry_20250926160100"],
  "entity_code": "BK0001",
  "is_industry": true
}
```

**响应**：
返回PNG格式的图表，包含得分和排名的比较

### 1.2 可视化权重分布

```
GET /api/visualization/weight_distribution
```

**响应**：
返回PNG格式的图表，展示当前权重的分布情况

## 2. 使用示例

### 2.1 模拟行业排名并获取图表

```python
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 模拟行业排名
response = requests.post(
    'http://localhost:5000/api/industry/simulate',
    json={
        'weight_adjustments': {
            'fundamental.revenue_growth': 0.20,
            'industry.industry_growth': 0.05
        }
    }
)

# 获取模拟结果
result = response.json()
simulation_id = result['simulation_id']

# 获取排名图表
chart_response = requests.get(f'http://localhost:5000/api/industry/chart/{simulation_id}?top_n=10')

# 保存图表
with open('industry_ranking.png', 'wb') as f:
    f.write(chart_response.content)

# 显示图表
img = mpimg.imread('industry_ranking.png')
plt.figure(figsize=(12, 8))
plt.imshow(img)
plt.axis('off')
plt.show()
```

### 2.2 比较多个模拟结果

```python
import requests
import json

# 创建第一个模拟
response1 = requests.post(
    'http://localhost:5000/api/industry/simulate',
    json={
        'weight_adjustments': {
            'fundamental.revenue_growth': 0.20,
            'industry.industry_growth': 0.05
        }
    }
)
simulation_id1 = response1.json()['simulation_id']

# 创建第二个模拟
response2 = requests.post(
    'http://localhost:5000/api/industry/simulate',
    json={
        'weight_adjustments': {
            'fundamental.profit_margin': 0.20,
            'fundamental.revenue_growth': 0.15
        }
    }
)
simulation_id2 = response2.json()['simulation_id']

# 比较模拟结果
compare_response = requests.post(
    'http://localhost:5000/api/industry/compare',
    json={
        'simulation_ids': [simulation_id1, simulation_id2]
    }
)

# 获取比较结果
compare_result = compare_response.json()

# 分析排名变化
changes = compare_result['data']['sim_1']['changes']
significant_changes = [c for c in changes if abs(c['rank_change']) >= 3]

print(f"发现 {len(significant_changes)} 个显著变化的行业:")
for change in significant_changes:
    print(f"行业代码: {change['industry_code']}, 排名变化: {change['rank_change']}")

# 可视化特定行业的影响
impact_response = requests.post(
    'http://localhost:5000/api/visualization/impact',
    json={
        'simulation_ids': [simulation_id1, simulation_id2],
        'entity_code': significant_changes[0]['industry_code'] if significant_changes else 'BK0001',
        'is_industry': True
    }
)

# 保存图表
with open('industry_impact.png', 'wb') as f:
    f.write(impact_response.content)