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
    
    # 数据源配置
    DATA_SOURCES = {
        'news_sources': [
            {
                'name': '新浪财经',
                'url': 'https://finance.sina.com.cn/',
                'type': 'news',
                'enabled': True
            },
            {
                'name': '东方财富',
                'url': 'https://www.eastmoney.com/',
                'type': 'news',
                'enabled': True
            },
            {
                'name': '证券时报',
                'url': 'http://www.stcn.com/',
                'type': 'news',
                'enabled': True
            },
            {
                'name': '财新网',
                'url': 'http://www.caixin.com/',
                'type': 'news',
                'enabled': True
            },
            {
                'name': '第一财经',
                'url': 'https://www.yicai.com/',
                'type': 'news',
                'enabled': True
            },
            {
                'name': '21世纪经济报道',
                'url': 'http://www.21jingji.com/',
                'type': 'news',
                'enabled': True
            },
            {
                'name': '经济观察报',
                'url': 'http://www.eeo.com.cn/',
                'type': 'news',
                'enabled': True
            },
            {
                'name': '中国证券报',
                'url': 'http://www.cs.com.cn/',
                'type': 'news',
                'enabled': True
            },
            {
                'name': '上海证券报',
                'url': 'http://www.cnstock.com/',
                'type': 'news',
                'enabled': True
            },
            {
                'name': '证券日报',
                'url': 'http://www.zqrb.cn/',
                'type': 'news',
                'enabled': True
            }
        ],
        'policy_sources': [
            {
                'name': '中国政府网',
                'url': 'http://www.gov.cn/',
                'type': 'policy',
                'enabled': True
            },
            {
                'name': '发改委',
                'url': 'https://www.ndrc.gov.cn/',
                'type': 'policy',
                'enabled': True
            },
            {
                'name': '央行',
                'url': 'http://www.pbc.gov.cn/',
                'type': 'policy',
                'enabled': True
            },
            {
                'name': '证监会',
                'url': 'http://www.csrc.gov.cn/',
                'type': 'policy',
                'enabled': True
            },
            {
                'name': '银保监会',
                'url': 'http://www.cbirc.gov.cn/',
                'type': 'policy',
                'enabled': True
            },
            {
                'name': '财政部',
                'url': 'http://www.mof.gov.cn/',
                'type': 'policy',
                'enabled': True
            },
            {
                'name': '工信部',
                'url': 'http://www.miit.gov.cn/',
                'type': 'policy',
                'enabled': True
            },
            {
                'name': '商务部',
                'url': 'http://www.mofcom.gov.cn/',
                'type': 'policy',
                'enabled': True
            }
        ],
        'industry_sources': [
            {
                'name': '中国汽车工业协会',
                'url': 'http://www.caam.org.cn/',
                'type': 'industry',
                'enabled': True
            },
            {
                'name': '中国钢铁工业协会',
                'url': 'http://www.chinaisa.org.cn/',
                'type': 'industry',
                'enabled': True
            },
            {
                'name': '中国有色金属工业协会',
                'url': 'http://www.china-nia.org.cn/',
                'type': 'industry',
                'enabled': True
            },
            {
                'name': '中国石油和化学工业联合会',
                'url': 'http://www.cpcif.org.cn/',
                'type': 'industry',
                'enabled': True
            }
        ],
        'market_sources': [
            {
                'name': '上海证券交易所',
                'url': 'http://www.sse.com.cn/',
                'type': 'market',
                'enabled': True
            },
            {
                'name': '深圳证券交易所',
                'url': 'http://www.szse.cn/',
                'type': 'market',
                'enabled': True
            },
            {
                'name': '北京证券交易所',
                'url': 'http://www.bse.cn/',
                'type': 'market',
                'enabled': True
            },
            {
                'name': '中国期货业协会',
                'url': 'http://www.cfachina.org/',
                'type': 'market',
                'enabled': True
            }
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
        'max_concurrent': 5
    }

# 创建配置实例
config = Config() 