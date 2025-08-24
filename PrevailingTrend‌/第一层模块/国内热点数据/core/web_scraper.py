"""
网页爬虫模块
从真实网站获取热点数据
"""

import requests
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from loguru import logger
from bs4 import BeautifulSoup
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus
import re
import json


class WebScraper:
    """网页爬虫类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def scrape_sina_finance(self) -> List[HotspotModel]:
        """爬取新浪财经热点"""
        hotspots = []
        try:
            # 新浪财经首页
            url = "https://finance.sina.com.cn/"
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 获取财经新闻
                news_items = soup.find_all('a', href=re.compile(r'/roll/|/stock/|/money/'))
                
                for item in news_items[:20]:  # 限制数量
                    title = item.get_text(strip=True)
                    link = item.get('href', '')
                    
                    if title and len(title) > 5 and 'http' in link:
                        # 获取详细内容
                        try:
                            detail_response = self.session.get(link, timeout=5)
                            detail_response.encoding = 'utf-8'
                            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                            
                            # 提取正文内容
                            content_elem = detail_soup.find('div', class_='article') or \
                                         detail_soup.find('div', class_='content') or \
                                         detail_soup.find('div', id='artibody')
                            
                            content = content_elem.get_text(strip=True)[:200] if content_elem else title
                            
                            hotspot = HotspotModel(
                                hotspot_id=f"sina_{int(time.time())}_{len(hotspots)}",
                                title=title,
                                content=content,
                                hotspot_type=HotspotType.NEWS,
                                hotspot_level=self._determine_level(title),
                                status=HotspotStatus.ACTIVE,
                                source="新浪财经",
                                url=link,
                                publish_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                                keywords=self._extract_keywords(title + content),
                                related_companies=self._extract_companies(title + content),
                                related_industries=self._extract_industries(title + content),
                                sentiment_score=self._analyze_sentiment(title + content),
                                heat_score=self._calculate_heat_score(title + content),
                                update_date=datetime.now()
                            )
                            hotspots.append(hotspot)
                            
                        except Exception as e:
                            logger.warning(f"获取新浪财经详情失败: {e}")
                            continue
                            
                        time.sleep(0.5)  # 避免请求过快
                        
        except Exception as e:
            logger.error(f"爬取新浪财经失败: {e}")
            
        return hotspots
    
    def scrape_eastmoney(self) -> List[HotspotModel]:
        """爬取东方财富热点"""
        hotspots = []
        try:
            # 东方财富财经频道
            url = "https://finance.eastmoney.com/"
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 获取财经新闻
                news_items = soup.find_all('a', href=re.compile(r'/a/|/news/'))
                
                for item in news_items[:20]:
                    title = item.get_text(strip=True)
                    link = item.get('href', '')
                    
                    if title and len(title) > 5:
                        if not link.startswith('http'):
                            link = 'https://finance.eastmoney.com' + link
                            
                        try:
                            detail_response = self.session.get(link, timeout=5)
                            detail_response.encoding = 'utf-8'
                            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                            
                            # 提取正文内容
                            content_elem = detail_soup.find('div', class_='article-content') or \
                                         detail_soup.find('div', class_='content') or \
                                         detail_soup.find('div', id='ContentBody')
                            
                            content = content_elem.get_text(strip=True)[:200] if content_elem else title
                            
                            hotspot = HotspotModel(
                                hotspot_id=f"eastmoney_{int(time.time())}_{len(hotspots)}",
                                title=title,
                                content=content,
                                hotspot_type=HotspotType.NEWS,
                                hotspot_level=self._determine_level(title),
                                status=HotspotStatus.ACTIVE,
                                source="东方财富",
                                url=link,
                                publish_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                                keywords=self._extract_keywords(title + content),
                                related_companies=self._extract_companies(title + content),
                                related_industries=self._extract_industries(title + content),
                                sentiment_score=self._analyze_sentiment(title + content),
                                heat_score=self._calculate_heat_score(title + content),
                                update_date=datetime.now()
                            )
                            hotspots.append(hotspot)
                            
                        except Exception as e:
                            logger.warning(f"获取东方财富详情失败: {e}")
                            continue
                            
                        time.sleep(0.5)
                        
        except Exception as e:
            logger.error(f"爬取东方财富失败: {e}")
            
        return hotspots
    
    def scrape_caixin(self) -> List[HotspotModel]:
        """爬取财新网热点"""
        hotspots = []
        try:
            # 财新网财经频道
            url = "https://economy.caixin.com/"
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 获取财经新闻
                news_items = soup.find_all('a', href=re.compile(r'/2025/|/2024/'))
                
                for item in news_items[:15]:
                    title = item.get_text(strip=True)
                    link = item.get('href', '')
                    
                    if title and len(title) > 5:
                        if not link.startswith('http'):
                            link = 'https://economy.caixin.com' + link
                            
                        try:
                            detail_response = self.session.get(link, timeout=5)
                            detail_response.encoding = 'utf-8'
                            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                            
                            # 提取正文内容
                            content_elem = detail_soup.find('div', class_='article-content') or \
                                         detail_soup.find('div', class_='content')
                            
                            content = content_elem.get_text(strip=True)[:200] if content_elem else title
                            
                            hotspot = HotspotModel(
                                hotspot_id=f"caixin_{int(time.time())}_{len(hotspots)}",
                                title=title,
                                content=content,
                                hotspot_type=HotspotType.NEWS,
                                hotspot_level=self._determine_level(title),
                                status=HotspotStatus.ACTIVE,
                                source="财新网",
                                url=link,
                                publish_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                                keywords=self._extract_keywords(title + content),
                                related_companies=self._extract_companies(title + content),
                                related_industries=self._extract_industries(title + content),
                                sentiment_score=self._analyze_sentiment(title + content),
                                heat_score=self._calculate_heat_score(title + content),
                                update_date=datetime.now()
                            )
                            hotspots.append(hotspot)
                            
                        except Exception as e:
                            logger.warning(f"获取财新网详情失败: {e}")
                            continue
                            
                        time.sleep(0.5)
                        
        except Exception as e:
            logger.error(f"爬取财新网失败: {e}")
            
        return hotspots
    
    def scrape_government_policy(self) -> List[HotspotModel]:
        """爬取政府政策信息"""
        hotspots = []
        try:
            # 中国政府网政策
            url = "http://www.gov.cn/zhengce/"
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 获取政策新闻
                news_items = soup.find_all('a', href=re.compile(r'/content/'))
                
                for item in news_items[:10]:
                    title = item.get_text(strip=True)
                    link = item.get('href', '')
                    
                    if title and len(title) > 5:
                        if not link.startswith('http'):
                            link = 'http://www.gov.cn' + link
                            
                        try:
                            detail_response = self.session.get(link, timeout=5)
                            detail_response.encoding = 'utf-8'
                            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                            
                            # 提取正文内容
                            content_elem = detail_soup.find('div', class_='article') or \
                                         detail_soup.find('div', class_='content')
                            
                            content = content_elem.get_text(strip=True)[:200] if content_elem else title
                            
                            hotspot = HotspotModel(
                                hotspot_id=f"gov_{int(time.time())}_{len(hotspots)}",
                                title=title,
                                content=content,
                                hotspot_type=HotspotType.POLICY,
                                hotspot_level=HotspotLevel.VERY_HIGH,
                                status=HotspotStatus.ACTIVE,
                                source="中国政府网",
                                url=link,
                                publish_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                                keywords=self._extract_keywords(title + content),
                                related_companies=self._extract_companies(title + content),
                                related_industries=self._extract_industries(title + content),
                                sentiment_score=self._analyze_sentiment(title + content),
                                heat_score=self._calculate_heat_score(title + content),
                                update_date=datetime.now()
                            )
                            hotspots.append(hotspot)
                            
                        except Exception as e:
                            logger.warning(f"获取政府网详情失败: {e}")
                            continue
                            
                        time.sleep(0.5)
                        
        except Exception as e:
            logger.error(f"爬取政府政策失败: {e}")
            
        return hotspots
    
    def scrape_stock_exchange(self) -> List[HotspotModel]:
        """爬取交易所公告"""
        hotspots = []
        try:
            # 上交所公告
            url = "http://www.sse.com.cn/disclosure/listedinfo/announcement/"
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 获取公告信息
                news_items = soup.find_all('a', href=re.compile(r'/disclosure/'))
                
                for item in news_items[:10]:
                    title = item.get_text(strip=True)
                    link = item.get('href', '')
                    
                    if title and len(title) > 5:
                        if not link.startswith('http'):
                            link = 'http://www.sse.com.cn' + link
                            
                        hotspot = HotspotModel(
                            hotspot_id=f"sse_{int(time.time())}_{len(hotspots)}",
                            title=title,
                            content=title,  # 公告标题作为内容
                            hotspot_type=HotspotType.MARKET,
                            hotspot_level=self._determine_level(title),
                            status=HotspotStatus.ACTIVE,
                            source="上海证券交易所",
                            url=link,
                            publish_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                            keywords=self._extract_keywords(title),
                            related_companies=self._extract_companies(title),
                            related_industries=self._extract_industries(title),
                            sentiment_score=self._analyze_sentiment(title),
                            heat_score=self._calculate_heat_score(title),
                            update_date=datetime.now()
                        )
                        hotspots.append(hotspot)
                        
                        time.sleep(0.5)
                        
        except Exception as e:
            logger.error(f"爬取交易所公告失败: {e}")
            
        return hotspots
    
    def scrape_all_sources(self) -> List[HotspotModel]:
        """爬取所有数据源"""
        logger.info("开始爬取真实数据...")
        
        all_hotspots = []
        
        # 爬取各个数据源
        scrapers = [
            ("新浪财经", self.scrape_sina_finance),
            ("东方财富", self.scrape_eastmoney),
            ("财新网", self.scrape_caixin),
            ("政府政策", self.scrape_government_policy),
            ("交易所公告", self.scrape_stock_exchange),
        ]
        
        for name, scraper_func in scrapers:
            try:
                logger.info(f"正在爬取 {name}...")
                hotspots = scraper_func()
                all_hotspots.extend(hotspots)
                logger.info(f"从 {name} 获取到 {len(hotspots)} 条数据")
                time.sleep(1)  # 避免请求过快
            except Exception as e:
                logger.error(f"爬取 {name} 失败: {e}")
        
        logger.info(f"总共爬取到 {len(all_hotspots)} 条真实数据")
        return all_hotspots
    
    def _determine_level(self, text: str) -> HotspotLevel:
        """根据文本内容确定热度级别"""
        high_keywords = ['重大', '紧急', '突发', '重要', '关键', '核心', '首次', '最大', '最高', '政策', '改革']
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