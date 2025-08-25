"""
国内热点数据模块配置文件
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类"""
    
    # 数据库配置
    DATABASE = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'rr1234RR'),
        'database': os.getenv('DB_NAME', 'pt'),
        'charset': 'utf8mb4'
    }
    
    # Web服务配置
    WEB = {
        'host': os.getenv('WEB_HOST', '0.0.0.0'),
        'port': int(os.getenv('WEB_PORT', 5002)),
        'debug': os.getenv('DEBUG', 'False').lower() == 'true'
    }
    
    # 数据源配置 - 扩展到50+个数据源
    DATA_SOURCES = {
        'news_sources': [
            # 主流财经媒体
            {'name': '新浪财经', 'url': 'https://finance.sina.com.cn/', 'type': 'news', 'enabled': True},
            {'name': '东方财富', 'url': 'https://www.eastmoney.com/', 'type': 'news', 'enabled': True},
            {'name': '证券时报', 'url': 'http://www.stcn.com/', 'type': 'news', 'enabled': True},
            {'name': '财新网', 'url': 'http://www.caixin.com/', 'type': 'news', 'enabled': True},
            {'name': '第一财经', 'url': 'https://www.yicai.com/', 'type': 'news', 'enabled': True},
            {'name': '21世纪经济报道', 'url': 'http://www.21jingji.com/', 'type': 'news', 'enabled': True},
            {'name': '经济观察报', 'url': 'http://www.eeo.com.cn/', 'type': 'news', 'enabled': True},
            {'name': '中国证券报', 'url': 'http://www.cs.com.cn/', 'type': 'news', 'enabled': True},
            {'name': '上海证券报', 'url': 'http://www.cnstock.com/', 'type': 'news', 'enabled': True},
            {'name': '证券日报', 'url': 'http://www.zqrb.cn/', 'type': 'news', 'enabled': True},
            {'name': '金融时报', 'url': 'http://www.financialnews.com.cn/', 'type': 'news', 'enabled': True},
            {'name': '经济参考报', 'url': 'http://www.jjckb.cn/', 'type': 'news', 'enabled': True},
            {'name': '中国经营报', 'url': 'http://www.cb.com.cn/', 'type': 'news', 'enabled': True},
            {'name': '华夏时报', 'url': 'http://www.chinatimes.net.cn/', 'type': 'news', 'enabled': True},
            {'name': '每日经济新闻', 'url': 'http://www.nbd.com.cn/', 'type': 'news', 'enabled': True},
            {'name': '界面新闻', 'url': 'https://www.jiemian.com/', 'type': 'news', 'enabled': True},
            {'name': '澎湃新闻', 'url': 'https://www.thepaper.cn/', 'type': 'news', 'enabled': True},
            {'name': '凤凰网财经', 'url': 'https://finance.ifeng.com/', 'type': 'news', 'enabled': True},
            {'name': '腾讯财经', 'url': 'https://finance.qq.com/', 'type': 'news', 'enabled': True},
            {'name': '网易财经', 'url': 'https://money.163.com/', 'type': 'news', 'enabled': True},
            {'name': '搜狐财经', 'url': 'https://business.sohu.com/', 'type': 'news', 'enabled': True},
            {'name': '和讯网', 'url': 'http://www.hexun.com/', 'type': 'news', 'enabled': True},
            {'name': '金融界', 'url': 'http://www.jrj.com.cn/', 'type': 'news', 'enabled': True},
            {'name': '中金在线', 'url': 'http://www.cnfol.com/', 'type': 'news', 'enabled': True},
            {'name': '全景网', 'url': 'http://www.p5w.net/', 'type': 'news', 'enabled': True},
            {'name': '证券之星', 'url': 'http://www.stockstar.com/', 'type': 'news', 'enabled': True},
            {'name': '同花顺', 'url': 'http://www.10jqka.com.cn/', 'type': 'news', 'enabled': True},
            {'name': '大智慧', 'url': 'http://www.gw.com.cn/', 'type': 'news', 'enabled': True},
            {'name': '万得资讯', 'url': 'http://www.wind.com.cn/', 'type': 'news', 'enabled': True},
            {'name': '彭博社中文', 'url': 'https://www.bloomberg.cn/', 'type': 'news', 'enabled': True},
            {'name': '路透社中文', 'url': 'https://cn.reuters.com/', 'type': 'news', 'enabled': True},
            {'name': '华尔街日报中文', 'url': 'https://cn.wsj.com/', 'type': 'news', 'enabled': True},
        ],
        'policy_sources': [
            # 政府部门
            {'name': '中国政府网', 'url': 'http://www.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '发改委', 'url': 'https://www.ndrc.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '央行', 'url': 'http://www.pbc.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '证监会', 'url': 'http://www.csrc.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '银保监会', 'url': 'http://www.cbirc.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '财政部', 'url': 'http://www.mof.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '工信部', 'url': 'http://www.miit.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '商务部', 'url': 'http://www.mofcom.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '科技部', 'url': 'http://www.most.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '人社部', 'url': 'http://www.mohrss.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '自然资源部', 'url': 'http://www.mnr.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '生态环境部', 'url': 'http://www.mee.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '住建部', 'url': 'http://www.mohurd.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '交通运输部', 'url': 'http://www.mot.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '农业农村部', 'url': 'http://www.moa.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '文化和旅游部', 'url': 'https://www.mct.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '国家卫健委', 'url': 'http://www.nhc.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '应急管理部', 'url': 'http://www.mem.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '人民银行', 'url': 'http://www.pbc.gov.cn/', 'type': 'policy', 'enabled': True},
            {'name': '外汇管理局', 'url': 'http://www.safe.gov.cn/', 'type': 'policy', 'enabled': True},
        ],
        'industry_sources': [
            # 行业协会
            {'name': '中国汽车工业协会', 'url': 'http://www.caam.org.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国钢铁工业协会', 'url': 'http://www.chinaisa.org.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国有色金属工业协会', 'url': 'http://www.china-nia.org.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国石油和化学工业联合会', 'url': 'http://www.cpcif.org.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国机械工业联合会', 'url': 'http://www.mei.net.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国轻工业联合会', 'url': 'http://www.clii.com.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国纺织工业联合会', 'url': 'http://www.ctei.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国建筑材料联合会', 'url': 'http://www.cbmf.org/', 'type': 'industry', 'enabled': True},
            {'name': '中国电力企业联合会', 'url': 'http://www.cec.org.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国煤炭工业协会', 'url': 'http://www.coalchina.org.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国电子企业协会', 'url': 'http://www.ceea.org.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国软件行业协会', 'url': 'http://www.csia.org.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国互联网协会', 'url': 'http://www.isc.org.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国通信企业协会', 'url': 'http://www.cace.org.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国房地产业协会', 'url': 'http://www.fangchan.com/', 'type': 'industry', 'enabled': True},
            {'name': '中国银行业协会', 'url': 'http://www.china-cba.net/', 'type': 'industry', 'enabled': True},
            {'name': '中国证券业协会', 'url': 'http://www.sac.net.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国保险行业协会', 'url': 'http://www.iachina.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国基金业协会', 'url': 'http://www.amac.org.cn/', 'type': 'industry', 'enabled': True},
            {'name': '中国期货业协会', 'url': 'http://www.cfachina.org/', 'type': 'industry', 'enabled': True},
        ],
        'market_sources': [
            # 交易所和监管机构
            {'name': '上海证券交易所', 'url': 'http://www.sse.com.cn/', 'type': 'market', 'enabled': True},
            {'name': '深圳证券交易所', 'url': 'http://www.szse.cn/', 'type': 'market', 'enabled': True},
            {'name': '北京证券交易所', 'url': 'http://www.bse.cn/', 'type': 'market', 'enabled': True},
            {'name': '中国金融期货交易所', 'url': 'http://www.cffex.com.cn/', 'type': 'market', 'enabled': True},
            {'name': '上海期货交易所', 'url': 'http://www.shfe.com.cn/', 'type': 'market', 'enabled': True},
            {'name': '郑州商品交易所', 'url': 'http://www.czce.com.cn/', 'type': 'market', 'enabled': True},
            {'name': '大连商品交易所', 'url': 'http://www.dce.com.cn/', 'type': 'market', 'enabled': True},
            {'name': '上海黄金交易所', 'url': 'http://www.sge.com.cn/', 'type': 'market', 'enabled': True},
            {'name': '全国中小企业股份转让系统', 'url': 'http://www.neeq.com.cn/', 'type': 'market', 'enabled': True},
            {'name': '中国证券登记结算公司', 'url': 'http://www.chinaclear.cn/', 'type': 'market', 'enabled': True},
        ]
    }
    
    # 热点分析配置
    ANALYSIS = {
        'sentiment_analysis': {
            'enabled': True,
            'model': 'snownlp',
            'threshold': 0.3
        },
        'heat_calculation': {
            'enabled': True,
            'factors': ['read_count', 'comment_count', 'share_count', 'time_decay'],
            'weights': [0.3, 0.2, 0.2, 0.3]
        },
        'keyword_extraction': {
            'enabled': True,
            'max_keywords': 10,
            'min_frequency': 2
        }
    }
    
    # 缓存配置
    CACHE = {
        'redis_host': os.getenv('REDIS_HOST', 'localhost'),
        'redis_port': int(os.getenv('REDIS_PORT', 6379)),
        'redis_db': int(os.getenv('REDIS_DB', 0)),
        'cache_ttl': 3600  # 1小时
    }
    
    # 日志配置
    LOGGING = {
        'level': os.getenv('LOG_LEVEL', 'INFO'),
        'format': '{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}',
        'file': 'logs/hotspot.log',
        'max_size': '10 MB',
        'retention': '7 days'
    }
    
    # API配置
    API = {
        'rate_limit': 100,  # 每分钟请求限制
        'timeout': 30,      # 请求超时时间
        'max_retries': 3    # 最大重试次数
    }
    
    # 数据更新配置
    UPDATE = {
        'auto_update': True,
        'update_interval': 300,  # 5分钟
        'batch_size': 100,
        'max_concurrent': 5,
        'daily_target': 150  # 每日目标热点数量
    }
    
    # API密钥配置
    API_KEYS = {
        'news_api': os.getenv('NEWS_API_KEY', ''),  # NewsAPI密钥
        'tushare': os.getenv('TUSHARE_TOKEN', ''),   # Tushare密钥
        'akshare': os.getenv('AKSHARE_TOKEN', ''),   # AKShare密钥
        'tianapi': os.getenv('TIANAPI_KEY', ''),     # 天行API密钥
        'jisuapi': os.getenv('JISUAPI_KEY', ''),     # 极速API密钥
    }

# 创建配置实例
config = Config() 