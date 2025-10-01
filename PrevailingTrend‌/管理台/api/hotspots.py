# -*- coding: utf-8 -*-
"""
热点相关 API 业务模块
- generate_hotspots: 优先从数据库读取，失败或为空返回默认数据
- calc_stats: 根据热点数据计算统计
- 其他热点类模拟接口：国外热点、论坛热点、全球资金流向、腾讯济安指数
"""
from __future__ import annotations
from typing import Dict, Any, List
import os
import json
import time
from datetime import datetime
from database import get_stocks

def generate_hotspots(ROOT_DIR: str) -> Dict[str, Any]:
    try:
        stocks = get_stocks(100)
        if stocks:
            return {
                "success": True,
                "data": [{
                    'id': stock['code'],
                    'title': f"{stock['name']} ({stock['code']})",
                    'category': stock['industry'],
                    'content': f"价格: {stock['price']} 涨跌幅: {stock['change_percent']}%",
                    'publishTime': stock['last_update'],
                    'source': "数据库",
                    'heatScore': stock['heat_score'],
                    'sentiment': stock['sentiment'],
                    'keywords': [stock['industry'], "A股"]
                } for stock in stocks]
            }
    except Exception as e:
        print(f"从数据库获取热点数据失败: {str(e)}")

    # 无外部请求，直接返回默认数据
    return {
        "success": True,
        "data": [
            {
                'id': "000001",
                'title': "上证指数 (000001)",
                'category': "指数",
                'content': "默认数据，请配置有效数据源",
                'publishTime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'source': "系统",
                'heatScore': 50,
                'sentiment': "中性",
                'keywords': ["指数", "A股"]
            }
        ]
    }

def calc_stats(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    stats = {
        "total_hotspots": len(data),
        "finance_hotspots": 0,
        "policy_hotspots": 0,
        "market_hotspots": 0,
        "industry_hotspots": 0,
        "company_hotspots": 0,
        "macro_hotspots": 0,
        "investment_hotspots": 0,
        "positive_count": 0,
        "neutral_count": 0,
        "negative_count": 0,
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    cat_map = {
        "财经热点": "finance_hotspots",
        "政策动态": "policy_hotspots",
        "市场新闻": "market_hotspots",
        "行业资讯": "industry_hotspots",
        "公司热点": "company_hotspots",
        "宏观经济": "macro_hotspots",
        "投资热点": "investment_hotspots",
    }
    for item in data:
        key = cat_map.get(item.get("category"))
        if key:
            stats[key] += 1
        sentiment = item.get("sentiment")
        if sentiment == "积极":
            stats["positive_count"] += 1
        elif sentiment == "中性":
            stats["neutral_count"] += 1
        elif sentiment == "消极":
            stats["negative_count"] += 1
    p, n, z = stats["positive_count"], stats["negative_count"], stats["neutral_count"]
    stats["market_sentiment"] = "积极" if p >= n and p >= z else ("消极" if n >= p and n >= z else "中性")
    return {"success": True, "data": stats}

def generate_foreign_hotspots() -> Dict[str, Any]:
    try:
        foreign_hotspots = [
            {"id": 1, "title": "美联储加息预期升温", "source": "Bloomberg", "date": "2025-09-20", "impact": 92, "region": "北美", "category": "货币政策"},
            {"id": 2, "title": "欧盟碳关税机制正式实施", "source": "Reuters", "date": "2025-09-19", "impact": 85, "region": "欧洲", "category": "环保政策"},
            {"id": 3, "title": "日本央行调整收益率曲线控制政策", "source": "Nikkei", "date": "2025-09-18", "impact": 78, "region": "亚太", "category": "货币政策"},
            {"id": 4, "title": "英国推出新一轮科技创新战略", "source": "Financial Times", "date": "2025-09-17", "impact": 72, "region": "欧洲", "category": "产业政策"},
            {"id": 5, "title": "印度修订外商投资政策", "source": "Economic Times", "date": "2025-09-16", "impact": 76, "region": "亚太", "category": "投资政策"},
            {"id": 6, "title": "巴西启动大规模基础设施建设计划", "source": "Globo", "date": "2025-09-15", "impact": 68, "region": "拉美", "category": "基建政策"},
            {"id": 7, "title": "德国汽车产业转型加速", "source": "Der Spiegel", "date": "2025-09-14", "impact": 83, "region": "欧洲", "category": "产业政策"},
            {"id": 8, "title": "沙特阿拉伯宣布新能源投资计划", "source": "Al Jazeera", "date": "2025-09-13", "impact": 79, "region": "中东", "category": "能源政策"},
            {"id": 9, "title": "澳大利亚矿产资源税改革", "source": "Australian Financial Review", "date": "2025-09-12", "impact": 74, "region": "亚太", "category": "税收政策"},
            {"id": 10, "title": "加拿大推出新的移民政策", "source": "CBC News", "date": "2025-09-11", "impact": 65, "region": "北美", "category": "人口政策"}
        ]
        return {"success": True, "data": foreign_hotspots}
    except Exception as e:
        return {"success": False, "message": f"获取国外热点数据失败: {str(e)}", "data": []}

def generate_forum_hotspots() -> Dict[str, Any]:
    try:
        forum_hotspots = [
            {"id": 1, "title": "新能源汽车行业未来发展前景如何？", "platform": "雪球", "author": "价值投资者", "date": "2025-09-22", "views": 12580, "comments": 356, "sentiment": 0.78},
            {"id": 2, "title": "半导体国产化进程加速，哪些公司将受益？", "platform": "雪球", "author": "科技研究员", "date": "2025-09-21", "views": 9876, "comments": 245, "sentiment": 0.85},
            {"id": 3, "title": "美联储加息对A股影响分析", "platform": "东方财富网", "author": "宏观经济学家", "date": "2025-09-20", "views": 15670, "comments": 423, "sentiment": -0.32},
            {"id": 4, "title": "医药板块估值修复，关注这些细分领域", "platform": "雪球", "author": "医药行业分析师", "date": "2025-09-19", "views": 7890, "comments": 198, "sentiment": 0.56},
            {"id": 5, "title": "ChatGPT-6发布，AI概念股再度爆发", "platform": "集思录", "author": "人工智能研究", "date": "2025-09-18", "views": 18920, "comments": 567, "sentiment": 0.92},
            {"id": 6, "title": "地产政策松绑，房地产股会否迎来转机？", "platform": "东方财富网", "author": "地产观察家", "date": "2025-09-17", "views": 11230, "comments": 321, "sentiment": 0.12},
            {"id": 7, "title": "新一轮稀土价格上涨，产业链全景梳理", "platform": "雪球", "author": "资源研究员", "date": "2025-09-16", "views": 6540, "comments": 187, "sentiment": 0.65},
            {"id": 8, "title": "光伏行业产能过剩担忧加剧", "platform": "集思录", "author": "能源分析师", "date": "2025-09-15", "views": 8760, "comments": 234, "sentiment": -0.45},
            {"id": 9, "title": "军工板块持续走强，关注这些细分龙头", "platform": "雪球", "author": "军工研究员", "date": "2025-09-14", "views": 9870, "comments": 276, "sentiment": 0.82},
            {"id": 10, "title": "消费电子行业复苏迹象明显", "platform": "东方财富网", "author": "科技消费分析", "date": "2025-09-13", "views": 7650, "comments": 198, "sentiment": 0.43}
        ]
        return {"success": True, "data": forum_hotspots}
    except Exception as e:
        return {"success": False, "message": f"获取论坛热点数据失败: {str(e)}", "data": []}

def generate_global_capital_flow() -> Dict[str, Any]:
    try:
        data = [
            {"id": 1, "region": "北美", "inflow": 2856.7, "outflow": 2345.8, "netFlow": 510.9, "change": 3.2, "date": "2025-09-22"},
            {"id": 2, "region": "欧洲", "inflow": 1987.3, "outflow": 2156.4, "netFlow": -169.1, "change": -1.8, "date": "2025-09-22"},
            {"id": 3, "region": "亚太", "inflow": 3245.6, "outflow": 2876.9, "netFlow": 368.7, "change": 2.5, "date": "2025-09-22"},
            {"id": 4, "region": "中国", "inflow": 1567.8, "outflow": 1234.5, "netFlow": 333.3, "change": 4.7, "date": "2025-09-22"},
            {"id": 5, "region": "日本", "inflow": 876.5, "outflow": 923.7, "netFlow": -47.2, "change": -0.8, "date": "2025-09-22"},
        ]
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "message": f"获取全球资金流向数据失败: {str(e)}", "data": []}

def generate_tencent_jian_index() -> Dict[str, Any]:
    try:
        data = {
            "currentIndex": 78.5,
            "previousIndex": 76.2,
            "change": 2.3,
            "updateTime": "2025-09-23 09:30",
            "historicalData": [
                {"date": "2025-09-16", "value": 75.8},
                {"date": "2025-09-17", "value": 74.6},
                {"date": "2025-09-18", "value": 75.2},
                {"date": "2025-09-19", "value": 76.5},
                {"date": "2025-09-20", "value": 76.8},
                {"date": "2025-09-21", "value": 76.2},
                {"date": "2025-09-22", "value": 77.4},
                {"date": "2025-09-23", "value": 78.5}
            ]
        }
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "message": f"获取腾讯济安指数数据失败: {str(e)}", "data": {}}