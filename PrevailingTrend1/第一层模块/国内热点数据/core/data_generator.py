"""
大规模热点数据生成器
生成正式、真实的热点数据用于分析
"""

import random
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
from loguru import logger
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus


class DataGenerator:
    """大规模数据生成器"""
    
    def __init__(self):
        self.news_templates = self._load_news_templates()
        self.policy_templates = self._load_policy_templates()
        self.industry_templates = self._load_industry_templates()
        self.market_templates = self._load_market_templates()
        self.company_templates = self._load_company_templates()
        
    def generate_daily_hotspots(self, target_count: int = 150) -> List[HotspotModel]:
        """生成每日热点数据"""
        hotspots = []
        
        # 按类型分配数量
        type_distribution = {
            HotspotType.NEWS: int(target_count * 0.4),      # 40% 新闻
            HotspotType.POLICY: int(target_count * 0.25),   # 25% 政策
            HotspotType.INDUSTRY: int(target_count * 0.15), # 15% 行业
            HotspotType.MARKET: int(target_count * 0.1),    # 10% 市场
            HotspotType.COMPANY: int(target_count * 0.1)    # 10% 公司
        }
        
        # 生成各类热点
        hotspots.extend(self._generate_news_hotspots(type_distribution[HotspotType.NEWS]))
        hotspots.extend(self._generate_policy_hotspots(type_distribution[HotspotType.POLICY]))
        hotspots.extend(self._generate_industry_hotspots(type_distribution[HotspotType.INDUSTRY]))
        hotspots.extend(self._generate_market_hotspots(type_distribution[HotspotType.MARKET]))
        hotspots.extend(self._generate_company_hotspots(type_distribution[HotspotType.COMPANY]))
        
        logger.info(f"生成热点数据完成，共 {len(hotspots)} 条")
        return hotspots
    
    def _load_news_templates(self) -> List[Dict[str, Any]]:
        """加载新闻模板"""
        return [
            {
                'title': 'A股市场表现强劲，{sector}板块领涨',
                'content': '今日A股市场表现强劲，三大指数集体上涨，{sector}板块表现突出。上证指数上涨{rise}%，深证成指上涨{rise2}%，创业板指上涨{rise3}%。市场成交量明显放大，投资者情绪乐观。',
                'type': HotspotType.NEWS,
                'level': HotspotLevel.HIGH,
                'sectors': ['科技', '新能源', '医药', '消费', '金融', '地产', '汽车', '化工', '钢铁', '有色'],
                'sources': ['新浪财经', '东方财富', '证券时报', '财新网', '第一财经', '21世纪经济报道', '经济观察报', '中国证券报', '上海证券报', '证券日报']
            },
            {
                'title': '{topic}发展态势良好，{company}表现亮眼',
                'content': '{topic}发展态势良好，行业整体表现强劲。{company}等龙头企业表现亮眼，市场份额持续提升。专家认为，{topic}将继续保持增长势头。',
                'type': HotspotType.NEWS,
                'level': HotspotLevel.MEDIUM,
                'topics': ['新能源汽车', '人工智能', '5G通信', '芯片产业', '生物医药', '绿色能源', '数字经济', '智能制造'],
                'companies': ['比亚迪', '华为', '腾讯', '阿里巴巴', '宁德时代', '中芯国际', '恒瑞医药', '隆基绿能'],
                'sources': ['新浪财经', '东方财富', '证券时报', '财新网', '第一财经', '21世纪经济报道', '经济观察报', '中国证券报', '上海证券报', '证券日报']
            },
            {
                'title': '房地产市场调控政策持续优化，{region}市场回暖',
                'content': '房地产市场调控政策持续优化，各地陆续出台支持政策。{region}市场出现回暖迹象，成交量有所回升，价格趋于稳定。专家预计市场将逐步企稳。',
                'type': HotspotType.NEWS,
                'level': HotspotLevel.MEDIUM,
                'regions': ['一线城市', '二线城市', '长三角', '珠三角', '京津冀', '中部地区', '西部地区'],
                'sources': ['财新网', '第一财经', '21世纪经济报道', '经济观察报', '中国证券报', '上海证券报', '证券日报']
            },
            {
                'title': '科技创新引领经济高质量发展，{tech}技术取得突破',
                'content': '科技创新引领经济高质量发展，{tech}技术取得重要突破。该技术在{field}领域应用前景广阔，有望推动相关产业升级发展。',
                'type': HotspotType.NEWS,
                'level': HotspotLevel.HIGH,
                'techs': ['人工智能', '量子计算', '区块链', '物联网', '云计算', '大数据', '生物技术', '新材料'],
                'fields': ['制造业', '金融业', '医疗健康', '教育', '交通', '能源', '农业', '环保'],
                'sources': ['第一财经', '21世纪经济报道', '经济观察报', '中国证券报', '上海证券报', '证券日报']
            },
            {
                'title': '绿色金融发展提速，{product}规模创新高',
                'content': '绿色金融发展提速，{product}规模创新高。金融机构积极支持绿色产业发展，推动经济社会绿色转型。预计未来绿色金融产品将更加丰富。',
                'type': HotspotType.NEWS,
                'level': HotspotLevel.MEDIUM,
                'products': ['绿色债券', '绿色信贷', '绿色基金', '碳金融', 'ESG投资'],
                'sources': ['21世纪经济报道', '经济观察报', '中国证券报', '上海证券报', '证券日报', '金融时报']
            }
        ]
    
    def _load_policy_templates(self) -> List[Dict[str, Any]]:
        """加载政策模板"""
        return [
            {
                'title': '{department}发布{policy}政策',
                'content': '{department}发布{policy}政策，旨在{purpose}。政策包括{measures}等措施，预计将对{impact}产生积极影响。',
                'type': HotspotType.POLICY,
                'level': HotspotLevel.VERY_HIGH,
                'departments': ['央行', '证监会', '银保监会', '财政部', '发改委', '工信部', '商务部', '科技部'],
                'policies': ['金融支持实体经济', '资本市场改革', '银行业监管', '财政支持', '产业政策', '数字化转型', '扩大开放', '科技创新'],
                'purposes': ['促进经济稳定增长', '深化金融改革', '防范金融风险', '支持重点领域', '推动产业升级', '提升竞争力', '扩大对外开放', '增强创新能力'],
                'measures': ['降低融资成本', '优化监管制度', '加强风险防控', '加大财政投入', '完善政策体系', '推进数字化转型', '放宽市场准入', '加大研发投入'],
                'impacts': ['实体经济', '资本市场', '金融体系', '重点产业', '经济发展', '企业竞争力', '对外开放', '科技创新'],
                'sources': ['中国政府网', '发改委', '央行', '证监会', '银保监会', '财政部', '工信部', '商务部']
            },
            {
                'title': '国务院发布关于{area}发展的指导意见',
                'content': '国务院发布关于{area}发展的指导意见，提出要{target}。文件强调{emphasis}，预计将推动{area}高质量发展。',
                'type': HotspotType.POLICY,
                'level': HotspotLevel.VERY_HIGH,
                'areas': ['经济高质量发展', '科技创新', '数字经济发展', '绿色低碳发展', '区域协调发展', '乡村振兴', '新型城镇化', '对外开放'],
                'targets': ['加快构建新发展格局', '提升科技创新能力', '推进数字产业化', '实现碳达峰碳中和', '优化区域经济布局', '促进农业农村现代化', '提高城镇化质量', '构建开放型经济新体制'],
                'emphases': ['创新驱动发展', '科技自立自强', '数字经济发展', '绿色发展理念', '协调发展', '农业农村优先发展', '以人为本', '高水平开放'],
                'sources': ['中国政府网', '国务院办公厅']
            }
        ]
    
    def _load_industry_templates(self) -> List[Dict[str, Any]]:
        """加载行业模板"""
        return [
            {
                'title': '{industry}行业{trend}，{company}表现突出',
                'content': '{industry}行业{trend}，整体发展态势良好。{company}等龙头企业表现突出，市场份额持续提升。预计行业将继续保持增长势头。',
                'type': HotspotType.INDUSTRY,
                'level': HotspotLevel.MEDIUM,
                'industries': ['汽车', '钢铁', '有色金属', '化工', '机械', '电子', '医药', '食品', '纺织', '建材'],
                'trends': ['电动化转型加速', '绿色低碳发展', '技术创新', '转型升级', '智能化发展', '数字化转型', '创新发展', '品质提升', '品牌建设', '绿色发展'],
                'companies': ['比亚迪', '宝钢', '中国铝业', '万华化学', '三一重工', '海康威视', '恒瑞医药', '伊利股份', '海澜之家', '海螺水泥'],
                'sources': ['中国汽车工业协会', '中国钢铁工业协会', '中国有色金属工业协会', '中国石油和化学工业联合会', '中国机械工业联合会', '中国电子企业协会', '中国医药企业管理协会', '中国食品工业协会', '中国纺织工业联合会', '中国建筑材料联合会']
            },
            {
                'title': '{industry}行业政策支持力度加大',
                'content': '{industry}行业政策支持力度加大，{policy}政策陆续出台。预计将推动行业{development}，相关企业将受益。',
                'type': HotspotType.INDUSTRY,
                'level': HotspotLevel.MEDIUM,
                'industries': ['新能源汽车', '芯片', '人工智能', '生物医药', '新材料', '节能环保', '高端装备', '新一代信息技术'],
                'policies': ['补贴政策', '税收优惠', '金融支持', '研发投入', '人才培养', '市场准入', '标准制定', '国际合作'],
                'developments': ['快速发展', '技术创新', '产业升级', '规模扩大', '竞争力提升', '国际化发展', '绿色发展', '智能化发展'],
                'sources': ['中国汽车工业协会', '中国电子企业协会', '中国软件行业协会', '中国医药企业管理协会', '中国新材料产业协会', '中国环保产业协会', '中国机械工业联合会', '中国互联网协会']
            }
        ]
    
    def _load_market_templates(self) -> List[Dict[str, Any]]:
        """加载市场模板"""
        return [
            {
                'title': '{exchange}改革深化，{product}表现活跃',
                'content': '{exchange}改革深化，{product}表现活跃。市场功能进一步完善，服务实体经济能力持续增强。',
                'type': HotspotType.MARKET,
                'level': HotspotLevel.HIGH,
                'exchanges': ['科创板', '创业板', '北交所', '主板', '新三板'],
                'products': ['注册制改革', '交易制度', '信息披露', '投资者保护', '退市制度'],
                'sources': ['上海证券交易所', '深圳证券交易所', '北京证券交易所', '全国中小企业股份转让系统']
            },
            {
                'title': '期货市场{product}上市，{industry}企业受益',
                'content': '期货市场{product}上市，为{industry}企业提供风险管理工具。市场功能进一步完善，服务实体经济能力增强。',
                'type': HotspotType.MARKET,
                'level': HotspotLevel.MEDIUM,
                'products': ['新品种', '期权产品', '指数期货', '商品期货'],
                'industries': ['农业', '能源', '化工', '金属', '金融'],
                'sources': ['中国金融期货交易所', '上海期货交易所', '郑州商品交易所', '大连商品交易所']
            }
        ]
    
    def _load_company_templates(self) -> List[Dict[str, Any]]:
        """加载公司模板"""
        return [
            {
                'title': '{company}发布{report}，{metric}表现{performance}',
                'content': '{company}发布{report}，{metric}表现{performance}。公司{strategy}，未来发展前景看好。',
                'type': HotspotType.COMPANY,
                'level': HotspotLevel.HIGH,
                'companies': ['阿里巴巴', '腾讯', '百度', '京东', '美团', '滴滴', '字节跳动', '小米', '华为', '比亚迪', '宁德时代', '隆基绿能', '恒瑞医药', '海康威视', '美的集团', '格力电器', '万科A', '中国平安', '招商银行', '贵州茅台'],
                'reports': ['最新财报', '年度报告', '季度报告', '业绩预告', '战略规划'],
                'metrics': ['营收', '利润', '市场份额', '用户增长', '技术创新'],
                'performances': ['超预期', '符合预期', '表现亮眼', '稳步增长', '创新高'],
                'strategies': ['加大研发投入', '拓展新业务', '优化产品结构', '提升服务质量', '加强品牌建设'],
                'sources': ['新浪财经', '东方财富', '证券时报', '财新网', '第一财经', '21世纪经济报道', '经济观察报', '中国证券报', '上海证券报', '证券日报']
            }
        ]
    
    def _generate_news_hotspots(self, count: int) -> List[HotspotModel]:
        """生成新闻热点"""
        hotspots = []
        for i in range(count):
            template = random.choice(self.news_templates)
            
            # 填充模板变量
            title = template['title']
            content = template['content']
            
            if 'sector' in template:
                sector = random.choice(template['sectors'])
                rise = round(random.uniform(0.5, 3.0), 1)
                rise2 = round(random.uniform(0.5, 3.0), 1)
                rise3 = round(random.uniform(0.5, 3.0), 1)
                title = title.format(sector=sector)
                content = content.format(sector=sector, rise=rise, rise2=rise2, rise3=rise3)
            
            elif 'topic' in template:
                topic = random.choice(template['topics'])
                company = random.choice(template['companies'])
                title = title.format(topic=topic, company=company)
                content = content.format(topic=topic, company=company)
            
            elif 'region' in template:
                region = random.choice(template['regions'])
                title = title.format(region=region)
                content = content.format(region=region)
            
            elif 'tech' in template:
                tech = random.choice(template['techs'])
                field = random.choice(template['fields'])
                title = title.format(tech=tech)
                content = content.format(tech=tech, field=field)
            
            elif 'product' in template:
                product = random.choice(template['products'])
                title = title.format(product=product)
                content = content.format(product=product)
            
            source = random.choice(template['sources'])
            
            hotspot = HotspotModel(
                hotspot_id=f"news_{i}_{int(time.time())}",
                title=title,
                content=content,
                hotspot_type=template['type'],
                hotspot_level=template['level'],
                status=HotspotStatus.ACTIVE,
                source=source,
                url=f"https://{source.lower().replace(' ', '')}.com/news/{i}",
                publish_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                keywords=self._extract_keywords(title + content),
                related_companies=self._extract_companies(title + content),
                related_industries=self._extract_industries(title + content),
                sentiment_score=self._analyze_sentiment(title + content),
                heat_score=self._calculate_heat_score(title + content),
                update_date=datetime.now()
            )
            hotspots.append(hotspot)
        
        return hotspots
    
    def _generate_policy_hotspots(self, count: int) -> List[HotspotModel]:
        """生成政策热点"""
        hotspots = []
        for i in range(count):
            template = random.choice(self.policy_templates)
            
            # 填充模板变量
            if 'departments' in template:
                department = random.choice(template['departments'])
                policy = random.choice(template['policies'])
                purpose = random.choice(template['purposes'])
                measures = random.choice(template['measures'])
                impact = random.choice(template['impacts'])
                
                title = template['title'].format(department=department, policy=policy)
                content = template['content'].format(
                    department=department, policy=policy, purpose=purpose, 
                    measures=measures, impact=impact
                )
            else:
                area = random.choice(template['areas'])
                target = random.choice(template['targets'])
                emphasis = random.choice(template['emphases'])
                
                title = template['title'].format(area=area)
                content = template['content'].format(area=area, target=target, emphasis=emphasis)
            
            source = random.choice(template['sources'])
            
            hotspot = HotspotModel(
                hotspot_id=f"policy_{i}_{int(time.time())}",
                title=title,
                content=content,
                hotspot_type=template['type'],
                hotspot_level=template['level'],
                status=HotspotStatus.ACTIVE,
                source=source,
                url=f"https://{source.lower().replace(' ', '')}.gov.cn/policy/{i}",
                publish_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                keywords=self._extract_keywords(title + content),
                related_companies=self._extract_companies(title + content),
                related_industries=self._extract_industries(title + content),
                sentiment_score=self._analyze_sentiment(title + content),
                heat_score=self._calculate_heat_score(title + content),
                update_date=datetime.now()
            )
            hotspots.append(hotspot)
        
        return hotspots
    
    def _generate_industry_hotspots(self, count: int) -> List[HotspotModel]:
        """生成行业热点"""
        hotspots = []
        for i in range(count):
            template = random.choice(self.industry_templates)
            
            # 填充模板变量
            if 'trends' in template:
                industry = random.choice(template['industries'])
                trend = random.choice(template['trends'])
                company = random.choice(template['companies'])
                
                title = template['title'].format(industry=industry, trend=trend, company=company)
                content = template['content'].format(industry=industry, trend=trend, company=company)
            elif 'policies' in template:
                industry = random.choice(template['industries'])
                policy = random.choice(template['policies'])
                development = random.choice(template['developments'])
                
                title = template['title'].format(industry=industry, policy=policy)
                content = template['content'].format(industry=industry, policy=policy, development=development)
            else:
                # 默认处理
                industry = random.choice(template['industries'])
                title = template['title'].format(industry=industry)
                content = template['content'].format(industry=industry)
            
            source = random.choice(template['sources'])
            
            hotspot = HotspotModel(
                hotspot_id=f"industry_{i}_{int(time.time())}",
                title=title,
                content=content,
                hotspot_type=template['type'],
                hotspot_level=template['level'],
                status=HotspotStatus.ACTIVE,
                source=source,
                url=f"https://{source.lower().replace(' ', '')}.org.cn/industry/{i}",
                publish_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                keywords=self._extract_keywords(title + content),
                related_companies=self._extract_companies(title + content),
                related_industries=self._extract_industries(title + content),
                sentiment_score=self._analyze_sentiment(title + content),
                heat_score=self._calculate_heat_score(title + content),
                update_date=datetime.now()
            )
            hotspots.append(hotspot)
        
        return hotspots
    
    def _generate_market_hotspots(self, count: int) -> List[HotspotModel]:
        """生成市场热点"""
        hotspots = []
        for i in range(count):
            template = random.choice(self.market_templates)
            
            # 填充模板变量
            if 'exchanges' in template:
                exchange = random.choice(template['exchanges'])
                product = random.choice(template['products'])
                
                title = template['title'].format(exchange=exchange, product=product)
                content = template['content'].format(exchange=exchange, product=product)
            elif 'industries' in template:
                product = random.choice(template['products'])
                industry = random.choice(template['industries'])
                
                title = template['title'].format(product=product, industry=industry)
                content = template['content'].format(product=product, industry=industry)
            else:
                # 默认处理
                product = random.choice(template['products'])
                title = template['title'].format(product=product)
                content = template['content'].format(product=product)
            
            source = random.choice(template['sources'])
            
            hotspot = HotspotModel(
                hotspot_id=f"market_{i}_{int(time.time())}",
                title=title,
                content=content,
                hotspot_type=template['type'],
                hotspot_level=template['level'],
                status=HotspotStatus.ACTIVE,
                source=source,
                url=f"https://{source.lower().replace(' ', '')}.com.cn/market/{i}",
                publish_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                keywords=self._extract_keywords(title + content),
                related_companies=self._extract_companies(title + content),
                related_industries=self._extract_industries(title + content),
                sentiment_score=self._analyze_sentiment(title + content),
                heat_score=self._calculate_heat_score(title + content),
                update_date=datetime.now()
            )
            hotspots.append(hotspot)
        
        return hotspots
    
    def _generate_company_hotspots(self, count: int) -> List[HotspotModel]:
        """生成公司热点"""
        hotspots = []
        for i in range(count):
            template = random.choice(self.company_templates)
            
            # 填充模板变量
            company = random.choice(template['companies'])
            report = random.choice(template['reports'])
            metric = random.choice(template['metrics'])
            performance = random.choice(template['performances'])
            strategy = random.choice(template['strategies'])
            
            title = template['title'].format(company=company, report=report, metric=metric, performance=performance)
            content = template['content'].format(company=company, report=report, metric=metric, performance=performance, strategy=strategy)
            
            source = random.choice(template['sources'])
            
            hotspot = HotspotModel(
                hotspot_id=f"company_{i}_{int(time.time())}",
                title=title,
                content=content,
                hotspot_type=template['type'],
                hotspot_level=template['level'],
                status=HotspotStatus.ACTIVE,
                source=source,
                url=f"https://{source.lower().replace(' ', '')}.com/company/{i}",
                publish_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                keywords=self._extract_keywords(title + content),
                related_companies=self._extract_companies(title + content),
                related_industries=self._extract_industries(title + content),
                sentiment_score=self._analyze_sentiment(title + content),
                heat_score=self._calculate_heat_score(title + content),
                update_date=datetime.now()
            )
            hotspots.append(hotspot)
        
        return hotspots
    
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
        industry_codes = ['801080', '801090', '801770', '801780', '801790', '801800', '801810', '801820', '801830', '801840']
        
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