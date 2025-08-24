"""
数据采集器
负责从各种数据源采集热点信息
"""

import requests
from datetime import datetime
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import re
import time
import random
from loguru import logger
from config import config
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus


class DataCollector:
    """数据采集器"""
    
    def __init__(self):
        self.config = config.DATA_SOURCES
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def collect_news_hotspots(self) -> List[HotspotModel]:
        """采集新闻热点"""
        hotspots = []
        
        # 模拟采集新闻热点
        sample_news = [
            {
                'title': 'A股三大指数集体上涨，科技股领涨',
                'content': '今日A股市场表现强劲，三大指数集体上涨，科技股表现突出。上证指数上涨1.2%，深证成指上涨1.8%，创业板指上涨2.1%。市场成交量明显放大，投资者情绪乐观。',
                'source': '新浪财经',
                'url': 'https://finance.sina.com.cn/stock/'
            },
            {
                'title': '央行发布最新货币政策报告',
                'content': '央行发布2024年第一季度货币政策执行报告，强调稳健货币政策，保持流动性合理充裕。报告指出，将继续实施稳健的货币政策，保持货币供应量和社会融资规模增速同名义经济增速基本匹配。',
                'source': '东方财富',
                'url': 'https://www.eastmoney.com/'
            },
            {
                'title': '新能源汽车销量创新高',
                'content': '2024年新能源汽车销量持续增长，多家车企表现亮眼。比亚迪、特斯拉等品牌销量大幅增长，市场渗透率进一步提升。政策支持和消费者认可度提高是主要推动因素。',
                'source': '证券时报',
                'url': 'http://www.stcn.com/'
            },
            {
                'title': '房地产市场调控政策持续优化',
                'content': '各地陆续出台房地产调控优化政策，支持刚需和改善性住房需求。政策包括降低首付比例、调整贷款利率、优化限购政策等，市场预期逐步改善。',
                'source': '财新网',
                'url': 'http://www.caixin.com/'
            },
            {
                'title': '科技创新引领经济高质量发展',
                'content': '国家高度重视科技创新，加大研发投入，推动关键核心技术突破。人工智能、量子计算、生物技术等前沿领域取得重要进展，为经济高质量发展提供强劲动力。',
                'source': '第一财经',
                'url': 'https://www.yicai.com/'
            },
            {
                'title': '绿色金融发展提速',
                'content': '绿色金融产品和服务不断创新，绿色债券、绿色信贷规模持续扩大。金融机构积极支持绿色产业发展，推动经济社会绿色转型。',
                'source': '21世纪经济报道',
                'url': 'http://www.21jingji.com/'
            },
            {
                'title': '数字经济成为经济增长新引擎',
                'content': '数字经济发展迅速，数字产业化、产业数字化进程加快。云计算、大数据、物联网等新技术广泛应用，推动传统产业转型升级。',
                'source': '经济观察报',
                'url': 'http://www.eeo.com.cn/'
            },
            {
                'title': '资本市场改革深化',
                'content': '注册制改革全面推进，多层次资本市场体系不断完善。科创板、创业板改革成效显著，北交所建设稳步推进，服务实体经济能力持续增强。',
                'source': '中国证券报',
                'url': 'http://www.cs.com.cn/'
            },
            {
                'title': '金融风险防控加强',
                'content': '金融监管部门持续加强风险防控，完善监管制度，防范化解重大金融风险。银行业、保险业、证券业风险总体可控，金融体系稳健运行。',
                'source': '上海证券报',
                'url': 'http://www.cnstock.com/'
            },
            {
                'title': '对外开放水平不断提升',
                'content': '金融业对外开放步伐加快，外资机构准入条件放宽，跨境投融资便利化程度提高。人民币国际化进程稳步推进，国际影响力不断增强。',
                'source': '证券日报',
                'url': 'http://www.zqrb.cn/'
            }
        ]
        
        for i, news in enumerate(sample_news):
            try:
                hotspot = HotspotModel(
                    hotspot_id=f"news_{i}_{int(time.time())}",
                    title=news['title'],
                    content=news['content'],
                    hotspot_type=HotspotType.NEWS,
                    hotspot_level=HotspotLevel.MEDIUM,
                    status=HotspotStatus.ACTIVE,
                    source=news['source'],
                    url=news['url'],
                    publish_time=datetime.now(),
                    keywords=self._extract_keywords(news['title']),
                    related_companies=self._extract_companies(news['title']),
                    related_industries=[],
                    sentiment_score=self._analyze_sentiment(news['title']),
                    heat_score=self._calculate_heat_score(news['title']),
                    update_date=datetime.now()
                )
                hotspots.append(hotspot)
                
            except Exception as e:
                logger.error(f"创建新闻热点失败: {e}")
        
        return hotspots
    
    def collect_policy_hotspots(self) -> List[HotspotModel]:
        """采集政策热点"""
        hotspots = []
        
        # 模拟采集政策热点
        sample_policies = [
            {
                'title': '国务院发布关于促进经济高质量发展的意见',
                'content': '国务院发布重要政策文件，强调经济高质量发展。文件提出要加快构建新发展格局，推动高质量发展，深化供给侧结构性改革，扩大内需，促进消费升级，推动产业升级和科技创新。',
                'source': '中国政府网',
                'url': 'http://www.gov.cn/'
            },
            {
                'title': '发改委发布新能源产业发展规划',
                'content': '国家发改委发布新能源产业发展规划，推动绿色转型。规划提出到2030年，非化石能源占一次能源消费比重达到25%左右，风电、太阳能发电总装机容量达到12亿千瓦以上。',
                'source': '发改委',
                'url': 'https://www.ndrc.gov.cn/'
            },
            {
                'title': '央行发布金融支持实体经济政策',
                'content': '央行发布金融支持实体经济政策，加大对重点领域和薄弱环节的金融支持。政策包括降低企业融资成本、扩大信贷投放、优化信贷结构等措施。',
                'source': '央行',
                'url': 'http://www.pbc.gov.cn/'
            },
            {
                'title': '证监会发布资本市场改革措施',
                'content': '证监会发布资本市场改革措施，深化注册制改革，完善多层次资本市场体系。措施包括优化发行上市制度、加强投资者保护、提升监管效能等。',
                'source': '证监会',
                'url': 'http://www.csrc.gov.cn/'
            },
            {
                'title': '银保监会发布银行业保险业监管政策',
                'content': '银保监会发布银行业保险业监管政策，防范化解金融风险，服务实体经济。政策强调要守住不发生系统性金融风险的底线，提升金融服务质效。',
                'source': '银保监会',
                'url': 'http://www.cbirc.gov.cn/'
            },
            {
                'title': '财政部发布财政支持政策',
                'content': '财政部发布财政支持政策，加大财政支持力度，促进经济稳定增长。政策包括减税降费、扩大政府投资、优化支出结构等措施。',
                'source': '财政部',
                'url': 'http://www.mof.gov.cn/'
            },
            {
                'title': '工信部发布制造业数字化转型政策',
                'content': '工信部发布制造业数字化转型政策，推动制造业高质量发展。政策提出要加快数字化、网络化、智能化发展，提升制造业核心竞争力。',
                'source': '工信部',
                'url': 'http://www.miit.gov.cn/'
            },
            {
                'title': '商务部发布扩大开放政策',
                'content': '商务部发布扩大开放政策，推动高水平对外开放。政策包括放宽市场准入、优化营商环境、扩大进口等措施，促进国内国际双循环。',
                'source': '商务部',
                'url': 'http://www.mofcom.gov.cn/'
            }
        ]
        
        for i, policy in enumerate(sample_policies):
            try:
                hotspot = HotspotModel(
                    hotspot_id=f"policy_{i}_{int(time.time())}",
                    title=policy['title'],
                    content=policy['content'],
                    hotspot_type=HotspotType.POLICY,
                    hotspot_level=HotspotLevel.HIGH,
                    status=HotspotStatus.ACTIVE,
                    source=policy['source'],
                    url=policy['url'],
                    publish_time=datetime.now(),
                    keywords=self._extract_keywords(policy['title']),
                    related_companies=self._extract_companies(policy['title']),
                    related_industries=[],
                    sentiment_score=self._analyze_sentiment(policy['title']),
                    heat_score=self._calculate_heat_score(policy['title']),
                    update_date=datetime.now()
                )
                hotspots.append(hotspot)
                
            except Exception as e:
                logger.error(f"创建政策热点失败: {e}")
        
        return hotspots
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        finance_keywords = ['股票', '基金', '债券', 'A股', '央行', '政策', '经济', '发展']
        
        for keyword in finance_keywords:
            if keyword in text:
                keywords.append(keyword)
        
        return keywords[:5]
    
    def _extract_companies(self, text: str) -> List[str]:
        """提取相关公司"""
        companies = []
        company_names = ['阿里巴巴', '腾讯', '百度', '华为', '比亚迪', '宁德时代']
        
        for company in company_names:
            if company in text:
                companies.append(company)
        
        return companies
    
    def _analyze_sentiment(self, text: str) -> float:
        """分析情感倾向"""
        positive_words = ['利好', '上涨', '增长', '发展', '机遇']
        negative_words = ['利空', '下跌', '下降', '风险', '问题']
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            return 0.6
        elif negative_count > positive_count:
            return -0.4
        else:
            return 0.0
    
    def _calculate_heat_score(self, text: str) -> float:
        """计算热度得分"""
        base_score = 50.0
        hot_keywords = ['重大', '紧急', '突发', '创新', '突破']
        
        for keyword in hot_keywords:
            if keyword in text:
                base_score += 15.0
        
        return min(100.0, base_score)
    
    def collect_industry_hotspots(self) -> List[HotspotModel]:
        """采集行业热点"""
        hotspots = []
        
        # 模拟采集行业热点
        sample_industries = [
            {
                'title': '汽车行业电动化转型加速',
                'content': '汽车行业电动化转型加速，传统车企纷纷加大新能源汽车投入。比亚迪、吉利、长城等自主品牌在电动化领域取得重要突破，市场份额持续提升。',
                'source': '中国汽车工业协会',
                'url': 'http://www.caam.org.cn/'
            },
            {
                'title': '钢铁行业绿色低碳发展',
                'content': '钢铁行业积极推进绿色低碳发展，加大环保投入，推广清洁生产技术。行业集中度进一步提升，龙头企业竞争力增强。',
                'source': '中国钢铁工业协会',
                'url': 'http://www.chinaisa.org.cn/'
            },
            {
                'title': '有色金属行业技术创新',
                'content': '有色金属行业技术创新取得重要进展，新材料研发应用加快。铝、铜、锂等金属在新能源、电子等领域的应用不断扩大。',
                'source': '中国有色金属工业协会',
                'url': 'http://www.china-nia.org.cn/'
            },
            {
                'title': '化工行业转型升级',
                'content': '化工行业转型升级步伐加快，新材料、精细化工等高附加值产品占比提升。行业向绿色化、高端化、智能化方向发展。',
                'source': '中国石油和化学工业联合会',
                'url': 'http://www.cpcif.org.cn/'
            }
        ]
        
        for i, industry in enumerate(sample_industries):
            try:
                hotspot = HotspotModel(
                    hotspot_id=f"industry_{i}_{int(time.time())}",
                    title=industry['title'],
                    content=industry['content'],
                    hotspot_type=HotspotType.INDUSTRY,
                    hotspot_level=HotspotLevel.MEDIUM,
                    status=HotspotStatus.ACTIVE,
                    source=industry['source'],
                    url=industry['url'],
                    publish_time=datetime.now(),
                    keywords=self._extract_keywords(industry['title']),
                    related_companies=self._extract_companies(industry['title']),
                    related_industries=[],
                    sentiment_score=self._analyze_sentiment(industry['title']),
                    heat_score=self._calculate_heat_score(industry['title']),
                    update_date=datetime.now()
                )
                hotspots.append(hotspot)
                
            except Exception as e:
                logger.error(f"创建行业热点失败: {e}")
        
        return hotspots
    
    def collect_market_hotspots(self) -> List[HotspotModel]:
        """采集市场热点"""
        hotspots = []
        
        # 模拟采集市场热点
        sample_markets = [
            {
                'title': '科创板注册制改革成效显著',
                'content': '科创板注册制改革成效显著，服务科技创新企业能力持续增强。科创板上市公司数量和质量不断提升，为科技创新企业提供重要融资平台。',
                'source': '上海证券交易所',
                'url': 'http://www.sse.com.cn/'
            },
            {
                'title': '创业板改革深化',
                'content': '创业板改革深化，注册制试点稳步推进。创业板服务成长型创新创业企业功能进一步增强，市场活力持续释放。',
                'source': '深圳证券交易所',
                'url': 'http://www.szse.cn/'
            },
            {
                'title': '北交所建设稳步推进',
                'content': '北交所建设稳步推进，服务中小企业能力不断提升。北交所为专精特新中小企业提供重要融资渠道，促进中小企业高质量发展。',
                'source': '北京证券交易所',
                'url': 'http://www.bse.cn/'
            },
            {
                'title': '期货市场创新发展',
                'content': '期货市场创新发展，新品种上市步伐加快。期货市场服务实体经济功能进一步增强，风险管理工具日益丰富。',
                'source': '中国期货业协会',
                'url': 'http://www.cfachina.org/'
            }
        ]
        
        for i, market in enumerate(sample_markets):
            try:
                hotspot = HotspotModel(
                    hotspot_id=f"market_{i}_{int(time.time())}",
                    title=market['title'],
                    content=market['content'],
                    hotspot_type=HotspotType.MARKET,
                    hotspot_level=HotspotLevel.HIGH,
                    status=HotspotStatus.ACTIVE,
                    source=market['source'],
                    url=market['url'],
                    publish_time=datetime.now(),
                    keywords=self._extract_keywords(market['title']),
                    related_companies=self._extract_companies(market['title']),
                    related_industries=[],
                    sentiment_score=self._analyze_sentiment(market['title']),
                    heat_score=self._calculate_heat_score(market['title']),
                    update_date=datetime.now()
                )
                hotspots.append(hotspot)
                
            except Exception as e:
                logger.error(f"创建市场热点失败: {e}")
        
        return hotspots

    def collect_all_hotspots(self) -> List[HotspotModel]:
        """采集所有类型的热点"""
        all_hotspots = []
        
        # 采集新闻热点
        news_hotspots = self.collect_news_hotspots()
        all_hotspots.extend(news_hotspots)
        
        # 采集政策热点
        policy_hotspots = self.collect_policy_hotspots()
        all_hotspots.extend(policy_hotspots)
        
        # 采集行业热点
        industry_hotspots = self.collect_industry_hotspots()
        all_hotspots.extend(industry_hotspots)
        
        # 采集市场热点
        market_hotspots = self.collect_market_hotspots()
        all_hotspots.extend(market_hotspots)
        
        logger.info(f"采集完成，共获得 {len(all_hotspots)} 条热点数据")
        return all_hotspots 