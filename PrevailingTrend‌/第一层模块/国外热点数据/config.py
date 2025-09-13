"""
国外热点数据模块配置文件
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
        'port': int(os.getenv('WEB_PORT', 5004)),
        'debug': os.getenv('DEBUG', 'False').lower() == 'true'
    }
    
    # 国外数据源配置
    DATA_SOURCES = {
        'news_sources': [
            {'name': 'Reuters', 'url': 'https://www.reuters.com/', 'type': 'news', 'enabled': True, 'region': 'global'},
            {'name': 'Bloomberg', 'url': 'https://www.bloomberg.com/', 'type': 'news', 'enabled': True, 'region': 'global'},
            {'name': 'Financial Times', 'url': 'https://www.ft.com/', 'type': 'news', 'enabled': True, 'region': 'uk'},
            {'name': 'Wall Street Journal', 'url': 'https://www.wsj.com/', 'type': 'news', 'enabled': True, 'region': 'us'},
            {'name': 'CNBC', 'url': 'https://www.cnbc.com/', 'type': 'news', 'enabled': True, 'region': 'us'},
        ],
        'policy_sources': [
            {'name': 'IMF', 'url': 'https://www.imf.org/', 'type': 'policy', 'enabled': True, 'region': 'global'},
            {'name': 'World Bank', 'url': 'https://www.worldbank.org/', 'type': 'policy', 'enabled': True, 'region': 'global'},
            {'name': 'Federal Reserve', 'url': 'https://www.federalreserve.gov/', 'type': 'policy', 'enabled': True, 'region': 'us'},
            {'name': 'ECB', 'url': 'https://www.ecb.europa.eu/', 'type': 'policy', 'enabled': True, 'region': 'eu'},
        ]
    }
    
    # 数据收集配置
    COLLECTOR = {
        'max_workers': int(os.getenv('MAX_WORKERS', 10)),
        'request_timeout': int(os.getenv('REQUEST_TIMEOUT', 30)),
        'retry_times': int(os.getenv('RETRY_TIMES', 3)),
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    
    # 日志配置
    LOGGING = {
        'level': os.getenv('LOG_LEVEL', 'INFO'),
        'file': os.getenv('LOG_FILE', 'logs/international_hotspot.log'),
    } 