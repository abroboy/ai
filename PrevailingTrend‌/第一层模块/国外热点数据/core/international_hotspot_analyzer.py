"""
国外热点数据分析器
"""

import re
from typing import List, Dict, Any
from loguru import logger


class InternationalHotspotAnalyzer:
    """国外热点数据分析器"""
    
    def __init__(self):
        # 关键词词典
        self.keywords_dict = {
            'finance': ['finance', 'financial', 'banking', 'investment', 'trading', 'market'],
            'technology': ['tech', 'technology', 'digital', 'software', 'ai', 'artificial intelligence'],
            'economy': ['economy', 'economic', 'gdp', 'inflation', 'recession', 'growth'],
            'policy': ['policy', 'regulation', 'law', 'government', 'federal', 'central bank'],
            'trade': ['trade', 'tariff', 'import', 'export', 'commerce', 'business'],
            'energy': ['energy', 'oil', 'gas', 'renewable', 'solar', 'wind'],
            'healthcare': ['health', 'medical', 'pharmaceutical', 'biotech', 'vaccine'],
            'automotive': ['auto', 'automotive', 'car', 'vehicle', 'tesla', 'electric'],
        }
        
        # 情感词典
        self.positive_words = [
            'positive', 'growth', 'increase', 'rise', 'gain', 'profit', 'success',
            'strong', 'improve', 'better', 'up', 'higher', 'bullish', 'optimistic'
        ]
        
        self.negative_words = [
            'negative', 'decline', 'decrease', 'fall', 'loss', 'failure', 'weak',
            'worse', 'down', 'lower', 'bearish', 'pessimistic', 'crisis', 'risk'
        ]
    
    def analyze_hotspot(self, hotspot: Dict[str, Any]) -> Dict[str, Any]:
        """分析单个热点数据"""
        try:
            # 提取关键词
            keywords = self._extract_keywords(hotspot['title'] + ' ' + hotspot['content'])
            hotspot['keywords'] = keywords
            
            # 分析情感
            sentiment_score = self._analyze_sentiment(hotspot['title'] + ' ' + hotspot['content'])
            hotspot['sentiment_score'] = sentiment_score
            
            # 计算热度得分
            heat_score = self._calculate_heat_score(hotspot)
            hotspot['heat_score'] = heat_score
            
            # 提取相关公司和行业
            companies, industries = self._extract_entities(hotspot['title'] + ' ' + hotspot['content'])
            hotspot['related_companies'] = companies
            hotspot['related_industries'] = industries
            
            logger.info(f"热点分析完成: {hotspot['hotspot_id']}")
            return hotspot
            
        except Exception as e:
            logger.error(f"分析热点数据失败: {e}")
            return hotspot
    
    def analyze_hotspots(self, hotspots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量分析热点数据"""
        analyzed_hotspots = []
        
        for hotspot in hotspots:
            analyzed_hotspot = self.analyze_hotspot(hotspot)
            analyzed_hotspots.append(analyzed_hotspot)
        
        logger.info(f"批量分析完成，共分析 {len(analyzed_hotspots)} 条数据")
        return analyzed_hotspots
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        text_lower = text.lower()
        
        for category, words in self.keywords_dict.items():
            for word in words:
                if word in text_lower:
                    keywords.append(word)
        
        # 去重并限制数量
        keywords = list(set(keywords))[:10]
        return keywords
    
    def _analyze_sentiment(self, text: str) -> float:
        """分析情感得分"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        
        total_words = len(text.split())
        if total_words == 0:
            return 0.0
        
        # 计算情感得分 (-1 到 1 之间)
        sentiment_score = (positive_count - negative_count) / total_words
        
        # 限制在 -1 到 1 之间
        sentiment_score = max(-1.0, min(1.0, sentiment_score))
        
        return round(sentiment_score, 3)
    
    def _calculate_heat_score(self, hotspot: Dict[str, Any]) -> float:
        """计算热度得分"""
        score = 50.0  # 基础分数
        
        # 根据关键词数量调整
        score += len(hotspot.get('keywords', [])) * 5
        
        # 根据情感强度调整
        sentiment_score = abs(hotspot.get('sentiment_score', 0))
        score += sentiment_score * 20
        
        # 根据标题长度调整
        title_length = len(hotspot.get('title', ''))
        if title_length > 50:
            score += 10
        
        # 限制在 0 到 100 之间
        score = max(0.0, min(100.0, score))
        
        return round(score, 2)
    
    def _extract_entities(self, text: str) -> tuple:
        """提取相关公司和行业"""
        companies = []
        industries = []
        
        # 简单的实体提取（实际项目中可以使用更复杂的NLP技术）
        # 这里只是示例，实际应该使用命名实体识别
        
        # 提取可能的公司名（大写字母开头的词组）
        company_pattern = r'\b[A-Z][a-zA-Z\s&]+(?:Inc|Corp|Ltd|LLC|Company|Corporation)\b'
        companies = re.findall(company_pattern, text)
        
        # 提取可能的行业名
        industry_keywords = ['technology', 'finance', 'healthcare', 'energy', 'automotive', 'retail']
        for keyword in industry_keywords:
            if keyword.lower() in text.lower():
                industries.append(keyword)
        
        return companies[:5], industries[:5]  # 限制数量 