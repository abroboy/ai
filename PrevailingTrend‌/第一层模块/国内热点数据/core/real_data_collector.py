"""
真实数据采集器
通过API接口实时获取热点数据
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from loguru import logger
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus
import config


class RealDataCollector:
    """真实数据采集器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def collect_from_news_api(self) -> List[HotspotModel]:
        """从新闻API获取数据"""
        hotspots = []
        
        # 使用新闻API获取数据
        api_urls = [
            "https://api.newsapi.org/v2/top-headlines",  # 示例API
            "https://api.tianapi.com/finance/index",     # 天行API
            "https://api.jisuapi.com/news/get",          # 极速API
        ]
        
        for api_url in api_urls:
            try:
                params = {
                    'country': 'cn',
                    'category': 'business',
                    'apiKey': config.API_KEYS.get('news_api', ''),
                    'pageSize': 20
                }
                
                response = self.session.get(api_url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    hotspots.extend(self._parse_news_api_data(data))
                    
            except Exception as e:
                logger.warning(f"新闻API {api_url} 获取失败: {e}")
        
        return hotspots
    
    def collect_from_stock_api(self) -> List[HotspotModel]:
        """从股票API获取数据"""
        hotspots = []
        
        # 使用股票相关API
        stock_apis = [
            "https://api.tushare.pro/query",  # Tushare API
            "https://api.akshare.xyz/api",    # AKShare API
        ]
        
        for api_url in stock_apis:
            try:
                params = {
                    'token': config.API_KEYS.get('tushare', ''),
                    'api_name': 'news',
                    'fields': 'title,content,publish_time,source'
                }
                
                response = self.session.post(api_url, json=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    hotspots.extend(self._parse_stock_api_data(data))
                    
            except Exception as e:
                logger.warning(f"股票API {api_url} 获取失败: {e}")
        
        return hotspots
    
    def collect_from_policy_api(self) -> List[HotspotModel]:
        """从政策API获取数据"""
        hotspots = []
        
        # 政府政策API
        policy_apis = [
            "http://www.gov.cn/api/policy",  # 中国政府网API
            "https://api.ndrc.gov.cn/policy", # 发改委API
        ]
        
        for api_url in policy_apis:
            try:
                params = {
                    'page': 1,
                    'size': 20,
                    'type': 'policy'
                }
                
                response = self.session.get(api_url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    hotspots.extend(self._parse_policy_api_data(data))
                    
            except Exception as e:
                logger.warning(f"政策API {api_url} 获取失败: {e}")
        
        return hotspots
    
    def collect_from_industry_api(self) -> List[HotspotModel]:
        """从行业API获取数据"""
        hotspots = []
        
        # 行业协会API
        industry_apis = [
            "https://api.caam.org.cn/news",  # 汽车工业协会
            "https://api.cisa.com.cn/news",  # 钢铁工业协会
        ]
        
        for api_url in industry_apis:
            try:
                params = {
                    'page': 1,
                    'limit': 20
                }
                
                response = self.session.get(api_url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    hotspots.extend(self._parse_industry_api_data(data))
                    
            except Exception as e:
                logger.warning(f"行业API {api_url} 获取失败: {e}")
        
        return hotspots
    
    def collect_from_market_api(self) -> List[HotspotModel]:
        """从市场API获取数据"""
        hotspots = []
        
        # 交易所API
        market_apis = [
            "https://query.sse.com.cn/commonQuery.do",  # 上交所
            "http://www.szse.cn/api/report/ShowReport", # 深交所
        ]
        
        for api_url in market_apis:
            try:
                params = {
                    'jsonCallBack': 'jsonpCallback',
                    'sqlId': 'COMMON_SSE_XXPL_CXJL_SSGSGZTZ_S',
                    'pageHelp.pageSize': 20
                }
                
                response = self.session.get(api_url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    hotspots.extend(self._parse_market_api_data(data))
                    
            except Exception as e:
                logger.warning(f"市场API {api_url} 获取失败: {e}")
        
        return hotspots
    
    def collect_all_real_data(self) -> List[HotspotModel]:
        """收集所有真实数据"""
        logger.info("开始收集真实数据...")
        
        all_hotspots = []
        
        # 并行收集各类数据
        collectors = [
            self.collect_from_news_api,
            self.collect_from_stock_api,
            self.collect_from_policy_api,
            self.collect_from_industry_api,
            self.collect_from_market_api,
        ]
        
        for collector in collectors:
            try:
                hotspots = collector()
                all_hotspots.extend(hotspots)
                logger.info(f"从 {collector.__name__} 获取到 {len(hotspots)} 条数据")
            except Exception as e:
                logger.error(f"数据收集失败 {collector.__name__}: {e}")
        
        logger.info(f"总共收集到 {len(all_hotspots)} 条真实数据")
        return all_hotspots
    
    def _parse_news_api_data(self, data: Dict) -> List[HotspotModel]:
        """解析新闻API数据"""
        hotspots = []
        
        try:
            articles = data.get('articles', [])
            for article in articles:
                hotspot = HotspotModel(
                    hotspot_id=f"news_{int(time.time())}_{len(hotspots)}",
                    title=article.get('title', ''),
                    content=article.get('description', ''),
                    hotspot_type=HotspotType.NEWS,
                    hotspot_level=self._determine_level(article.get('title', '')),
                    status=HotspotStatus.ACTIVE,
                    source=article.get('source', {}).get('name', '未知来源'),
                    url=article.get('url', ''),
                    publish_time=datetime.fromisoformat(article.get('publishedAt', '').replace('Z', '+00:00')),
                    keywords=self._extract_keywords(article.get('title', '') + article.get('description', '')),
                    related_companies=self._extract_companies(article.get('title', '') + article.get('description', '')),
                    related_industries=self._extract_industries(article.get('title', '') + article.get('description', '')),
                    sentiment_score=self._analyze_sentiment(article.get('title', '') + article.get('description', '')),
                    heat_score=self._calculate_heat_score(article.get('title', '') + article.get('description', '')),
                    update_date=datetime.now()
                )
                hotspots.append(hotspot)
        except Exception as e:
            logger.error(f"解析新闻API数据失败: {e}")
        
        return hotspots
    
    def _parse_stock_api_data(self, data: Dict) -> List[HotspotModel]:
        """解析股票API数据"""
        hotspots = []
        
        try:
            items = data.get('data', {}).get('items', [])
            for item in items:
                hotspot = HotspotModel(
                    hotspot_id=f"stock_{int(time.time())}_{len(hotspots)}",
                    title=item.get('title', ''),
                    content=item.get('content', ''),
                    hotspot_type=HotspotType.MARKET,
                    hotspot_level=self._determine_level(item.get('title', '')),
                    status=HotspotStatus.ACTIVE,
                    source=item.get('source', '股票数据'),
                    url=item.get('url', ''),
                    publish_time=datetime.fromtimestamp(item.get('publish_time', time.time())),
                    keywords=self._extract_keywords(item.get('title', '') + item.get('content', '')),
                    related_companies=self._extract_companies(item.get('title', '') + item.get('content', '')),
                    related_industries=self._extract_industries(item.get('title', '') + item.get('content', '')),
                    sentiment_score=self._analyze_sentiment(item.get('title', '') + item.get('content', '')),
                    heat_score=self._calculate_heat_score(item.get('title', '') + item.get('content', '')),
                    update_date=datetime.now()
                )
                hotspots.append(hotspot)
        except Exception as e:
            logger.error(f"解析股票API数据失败: {e}")
        
        return hotspots
    
    def _parse_policy_api_data(self, data: Dict) -> List[HotspotModel]:
        """解析政策API数据"""
        hotspots = []
        
        try:
            policies = data.get('data', [])
            for policy in policies:
                hotspot = HotspotModel(
                    hotspot_id=f"policy_{int(time.time())}_{len(hotspots)}",
                    title=policy.get('title', ''),
                    content=policy.get('content', ''),
                    hotspot_type=HotspotType.POLICY,
                    hotspot_level=HotspotLevel.VERY_HIGH,
                    status=HotspotStatus.ACTIVE,
                    source=policy.get('source', '政府政策'),
                    url=policy.get('url', ''),
                    publish_time=datetime.fromisoformat(policy.get('publish_time', datetime.now().isoformat())),
                    keywords=self._extract_keywords(policy.get('title', '') + policy.get('content', '')),
                    related_companies=self._extract_companies(policy.get('title', '') + policy.get('content', '')),
                    related_industries=self._extract_industries(policy.get('title', '') + policy.get('content', '')),
                    sentiment_score=self._analyze_sentiment(policy.get('title', '') + policy.get('content', '')),
                    heat_score=self._calculate_heat_score(policy.get('title', '') + policy.get('content', '')),
                    update_date=datetime.now()
                )
                hotspots.append(hotspot)
        except Exception as e:
            logger.error(f"解析政策API数据失败: {e}")
        
        return hotspots
    
    def _parse_industry_api_data(self, data: Dict) -> List[HotspotModel]:
        """解析行业API数据"""
        hotspots = []
        
        try:
            news = data.get('data', [])
            for item in news:
                hotspot = HotspotModel(
                    hotspot_id=f"industry_{int(time.time())}_{len(hotspots)}",
                    title=item.get('title', ''),
                    content=item.get('content', ''),
                    hotspot_type=HotspotType.INDUSTRY,
                    hotspot_level=self._determine_level(item.get('title', '')),
                    status=HotspotStatus.ACTIVE,
                    source=item.get('source', '行业协会'),
                    url=item.get('url', ''),
                    publish_time=datetime.fromisoformat(item.get('publish_time', datetime.now().isoformat())),
                    keywords=self._extract_keywords(item.get('title', '') + item.get('content', '')),
                    related_companies=self._extract_companies(item.get('title', '') + item.get('content', '')),
                    related_industries=self._extract_industries(item.get('title', '') + item.get('content', '')),
                    sentiment_score=self._analyze_sentiment(item.get('title', '') + item.get('content', '')),
                    heat_score=self._calculate_heat_score(item.get('title', '') + item.get('content', '')),
                    update_date=datetime.now()
                )
                hotspots.append(hotspot)
        except Exception as e:
            logger.error(f"解析行业API数据失败: {e}")
        
        return hotspots
    
    def _parse_market_api_data(self, data: Dict) -> List[HotspotModel]:
        """解析市场API数据"""
        hotspots = []
        
        try:
            announcements = data.get('data', [])
            for announcement in announcements:
                hotspot = HotspotModel(
                    hotspot_id=f"market_{int(time.time())}_{len(hotspots)}",
                    title=announcement.get('title', ''),
                    content=announcement.get('content', ''),
                    hotspot_type=HotspotType.MARKET,
                    hotspot_level=self._determine_level(announcement.get('title', '')),
                    status=HotspotStatus.ACTIVE,
                    source=announcement.get('source', '交易所'),
                    url=announcement.get('url', ''),
                    publish_time=datetime.fromisoformat(announcement.get('publish_time', datetime.now().isoformat())),
                    keywords=self._extract_keywords(announcement.get('title', '') + announcement.get('content', '')),
                    related_companies=self._extract_companies(announcement.get('title', '') + announcement.get('content', '')),
                    related_industries=self._extract_industries(announcement.get('title', '') + announcement.get('content', '')),
                    sentiment_score=self._analyze_sentiment(announcement.get('title', '') + announcement.get('content', '')),
                    heat_score=self._calculate_heat_score(announcement.get('title', '') + announcement.get('content', '')),
                    update_date=datetime.now()
                )
                hotspots.append(hotspot)
        except Exception as e:
            logger.error(f"解析市场API数据失败: {e}")
        
        return hotspots
    
    def _determine_level(self, text: str) -> HotspotLevel:
        """根据文本内容确定热度级别"""
        high_keywords = ['重大', '紧急', '突发', '重要', '关键', '核心', '首次', '最大', '最高']
        medium_keywords = ['发展', '增长', '提升', '改善', '优化', '加强', '扩大', '推进']
        
        if any(keyword in text for keyword in high_keywords):
            return HotspotLevel.HIGH
        elif any(keyword in text for keyword in medium_keywords):
            return HotspotLevel.MEDIUM
        else:
            return HotspotLevel.LOW
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        finance_keywords = ['股票', '基金', '债券', 'A股', '央行', '政策', '经济', '发展', '创新', '科技', '金融', '市场', '投资', '改革', '增长', '企业', '行业', '技术', '产品', '服务']
        
        for keyword in finance_keywords:
            if keyword in text and len(keywords) < 5:
                keywords.append(keyword)
        
        return keywords
    
    def _extract_companies(self, text: str) -> List[str]:
        """提取相关公司"""
        companies = []
        company_names = ['阿里巴巴', '腾讯', '百度', '京东', '美团', '滴滴', '字节跳动', '小米', '华为', '比亚迪', '宁德时代', '隆基绿能', '恒瑞医药', '海康威视', '美的集团', '格力电器', '万科A', '中国平安', '招商银行', '贵州茅台']
        
        for company in company_names:
            if company in text:
                companies.append(company)
        
        return companies
    
    def _extract_industries(self, text: str) -> List[str]:
        """提取相关行业"""
        industries = []
        
        # 根据文本内容匹配行业
        if any(word in text for word in ['汽车', '新能源']):
            industries.append('801080')
        elif any(word in text for word in ['钢铁', '有色']):
            industries.append('801090')
        elif any(word in text for word in ['科技', '芯片']):
            industries.append('801770')
        elif any(word in text for word in ['医药', '生物']):
            industries.append('801780')
        elif any(word in text for word in ['金融', '银行']):
            industries.append('801790')
        elif any(word in text for word in ['地产', '房地产']):
            industries.append('801800')
        elif any(word in text for word in ['消费', '食品']):
            industries.append('801810')
        elif any(word in text for word in ['化工', '材料']):
            industries.append('801820')
        elif any(word in text for word in ['机械', '装备']):
            industries.append('801830')
        elif any(word in text for word in ['电子', '通信']):
            industries.append('801840')
        
        return industries
    
    def _analyze_sentiment(self, text: str) -> float:
        """分析情感倾向"""
        positive_words = ['利好', '上涨', '增长', '发展', '机遇', '突破', '创新', '成功', '优秀', '提升', '改善', '优化', '加强', '扩大', '推进']
        negative_words = ['利空', '下跌', '下降', '风险', '问题', '困难', '挑战', '危机', '亏损', '下滑', '减少', '收缩', '放缓', '担忧', '压力']
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count == 0 and negative_count == 0:
            return 0.0
        elif positive_count > negative_count:
            return min(0.8, positive_count * 0.2)
        else:
            return max(-0.8, -negative_count * 0.2)
    
    def _calculate_heat_score(self, text: str) -> float:
        """计算热度得分"""
        base_score = 50.0
        hot_keywords = ['重大', '紧急', '突发', '创新', '突破', '政策', '改革', '发展', '重要', '关键', '核心', '领先', '首次', '最大', '最高']
        
        for keyword in hot_keywords:
            if keyword in text:
                base_score += 10.0
        
        return min(100.0, base_score) 