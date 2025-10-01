#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国内热点数据获取服务
从多个数据源获取国内热点新闻和数据
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random

class DomesticHotspotFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def fetch_sina_finance_news(self) -> List[Dict[str, Any]]:
        """获取新浪财经热点新闻"""
        try:
            # 模拟新浪财经API调用
            # 实际应用中需要替换为真实的API
            mock_data = [
                {
                    "id": f"sina_{i}",
                    "title": f"新浪财经热点 {i}: 央行降准预期升温，银行股集体上涨",
                    "content": "市场预期央行可能在近期实施降准措施，银行板块受益明显，多只银行股涨停。",
                    "source": "新浪财经",
                    "publish_time": (datetime.now() - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S"),
                    "category": "金融政策",
                    "heat_score": random.randint(70, 95),
                    "sentiment": random.choice(["积极", "中性", "消极"]),
                    "keywords": ["央行", "降准", "银行股", "金融政策"],
                    "url": f"https://finance.sina.com.cn/news/{i}"
                }
                for i in range(1, 6)
            ]
            return mock_data
        except Exception as e:
            print(f"获取新浪财经数据失败: {e}")
            return []
    
    def fetch_eastmoney_news(self) -> List[Dict[str, Any]]:
        """获取东方财富热点新闻"""
        try:
            # 模拟东方财富API调用
            mock_data = [
                {
                    "id": f"eastmoney_{i}",
                    "title": f"东财热点 {i}: 新能源汽车销量创新高，产业链公司受益",
                    "content": "最新数据显示新能源汽车销量同比增长超30%，带动电池、电机等产业链公司业绩提升。",
                    "source": "东方财富",
                    "publish_time": (datetime.now() - timedelta(hours=i+2)).strftime("%Y-%m-%d %H:%M:%S"),
                    "category": "行业动态",
                    "heat_score": random.randint(75, 90),
                    "sentiment": random.choice(["积极", "中性"]),
                    "keywords": ["新能源汽车", "销量", "产业链", "电池"],
                    "url": f"https://finance.eastmoney.com/news/{i}"
                }
                for i in range(1, 6)
            ]
            return mock_data
        except Exception as e:
            print(f"获取东方财富数据失败: {e}")
            return []
    
    def fetch_cnstock_news(self) -> List[Dict[str, Any]]:
        """获取中国证券网热点新闻"""
        try:
            # 模拟中国证券网API调用
            mock_data = [
                {
                    "id": f"cnstock_{i}",
                    "title": f"中证网热点 {i}: 科创板改革持续深化，注册制全面推行",
                    "content": "科创板注册制改革取得显著成效，为资本市场发展注入新活力。",
                    "source": "中国证券网",
                    "publish_time": (datetime.now() - timedelta(hours=i+4)).strftime("%Y-%m-%d %H:%M:%S"),
                    "category": "资本市场",
                    "heat_score": random.randint(80, 95),
                    "sentiment": "积极",
                    "keywords": ["科创板", "注册制", "资本市场", "改革"],
                    "url": f"https://www.cnstock.com/news/{i}"
                }
                for i in range(1, 4)
            ]
            return mock_data
        except Exception as e:
            print(f"获取中国证券网数据失败: {e}")
            return []
    
    def fetch_weibo_hotspots(self) -> List[Dict[str, Any]]:
        """获取微博财经热搜"""
        try:
            # 模拟微博热搜API调用
            mock_data = [
                {
                    "id": f"weibo_{i}",
                    "title": f"微博热搜 {i}: #{topic}#",
                    "content": f"微博热搜话题: {topic}，讨论热度持续上升。",
                    "source": "微博",
                    "publish_time": (datetime.now() - timedelta(minutes=i*30)).strftime("%Y-%m-%d %H:%M:%S"),
                    "category": "社交媒体",
                    "heat_score": random.randint(60, 85),
                    "sentiment": random.choice(["积极", "中性", "消极"]),
                    "keywords": [topic, "热搜", "讨论"],
                    "url": f"https://weibo.com/hot/{i}"
                }
                for i, topic in enumerate(["央行降准", "新能源汽车", "芯片股", "房地产政策", "人工智能"], 1)
            ]
            return mock_data
        except Exception as e:
            print(f"获取微博热搜数据失败: {e}")
            return []
    
    def fetch_baidu_index(self) -> List[Dict[str, Any]]:
        """获取百度指数热点"""
        try:
            # 模拟百度指数API调用
            keywords = ["股票", "基金", "理财", "投资", "房价", "黄金", "比特币", "保险"]
            mock_data = [
                {
                    "id": f"baidu_{i}",
                    "title": f"百度指数热词: {keyword}",
                    "content": f"关键词 '{keyword}' 搜索热度上升，用户关注度较高。",
                    "source": "百度指数",
                    "publish_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "category": "搜索热度",
                    "heat_score": random.randint(50, 80),
                    "sentiment": "中性",
                    "keywords": [keyword, "搜索", "热度"],
                    "url": f"https://index.baidu.com/v2/main/index.html#{keyword}"
                }
                for i, keyword in enumerate(keywords, 1)
            ]
            return mock_data
        except Exception as e:
            print(f"获取百度指数数据失败: {e}")
            return []
    
    def fetch_all_hotspots(self) -> Dict[str, Any]:
        """获取所有来源的热点数据"""
        try:
            print("开始获取国内热点数据...")
            
            # 并发获取各个数据源
            sina_data = self.fetch_sina_finance_news()
            eastmoney_data = self.fetch_eastmoney_news()
            cnstock_data = self.fetch_cnstock_news()
            weibo_data = self.fetch_weibo_hotspots()
            baidu_data = self.fetch_baidu_index()
            
            # 合并所有数据
            all_hotspots = []
            all_hotspots.extend(sina_data)
            all_hotspots.extend(eastmoney_data)
            all_hotspots.extend(cnstock_data)
            all_hotspots.extend(weibo_data)
            all_hotspots.extend(baidu_data)
            
            # 按热度排序
            all_hotspots.sort(key=lambda x: x['heat_score'], reverse=True)
            
            # 计算统计信息
            stats = self.calculate_statistics(all_hotspots)
            
            print(f"成功获取 {len(all_hotspots)} 条热点数据")
            
            return {
                "success": True,
                "data": all_hotspots,
                "statistics": stats,
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_count": len(all_hotspots)
            }
            
        except Exception as e:
            print(f"获取热点数据失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": [],
                "statistics": {},
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_count": 0
            }
    
    def calculate_statistics(self, hotspots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算热点数据统计信息"""
        if not hotspots:
            return {}
        
        # 按来源统计
        source_stats = {}
        for hotspot in hotspots:
            source = hotspot.get('source', '未知')
            source_stats[source] = source_stats.get(source, 0) + 1
        
        # 按分类统计
        category_stats = {}
        for hotspot in hotspots:
            category = hotspot.get('category', '其他')
            category_stats[category] = category_stats.get(category, 0) + 1
        
        # 按情感统计
        sentiment_stats = {"积极": 0, "中性": 0, "消极": 0}
        for hotspot in hotspots:
            sentiment = hotspot.get('sentiment', '中性')
            if sentiment in sentiment_stats:
                sentiment_stats[sentiment] += 1
        
        # 热度分布
        high_heat = len([h for h in hotspots if h.get('heat_score', 0) >= 80])
        medium_heat = len([h for h in hotspots if 60 <= h.get('heat_score', 0) < 80])
        low_heat = len([h for h in hotspots if h.get('heat_score', 0) < 60])
        
        return {
            "total_count": len(hotspots),
            "source_distribution": source_stats,
            "category_distribution": category_stats,
            "sentiment_distribution": sentiment_stats,
            "heat_distribution": {
                "high": high_heat,
                "medium": medium_heat,
                "low": low_heat
            },
            "avg_heat_score": sum(h.get('heat_score', 0) for h in hotspots) / len(hotspots),
            "top_keywords": self.extract_top_keywords(hotspots)
        }
    
    def extract_top_keywords(self, hotspots: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
        """提取热门关键词"""
        keyword_count = {}
        
        for hotspot in hotspots:
            keywords = hotspot.get('keywords', [])
            for keyword in keywords:
                keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
        
        # 排序并返回前N个
        sorted_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {"keyword": keyword, "count": count}
            for keyword, count in sorted_keywords[:top_n]
        ]

# 创建全局实例
domestic_fetcher = DomesticHotspotFetcher()

def get_domestic_hotspots() -> Dict[str, Any]:
    """获取国内热点数据的主函数"""
    return domestic_fetcher.fetch_all_hotspots()

if __name__ == "__main__":
    # 测试数据获取
    result = get_domestic_hotspots()
    print(json.dumps(result, ensure_ascii=False, indent=2))