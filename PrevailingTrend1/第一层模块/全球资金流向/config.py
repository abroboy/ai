# -*- coding: utf-8 -*-
"""
全球资金流向模块配置文件
"""

import os
from datetime import datetime, timedelta

# 数据库配置
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'prevailing_trend'),
    'charset': 'utf8mb4'
}

# 数据源配置
DATA_SOURCES = {
    # 外汇数据源
    'forex': {
        'api_key': os.getenv('FOREX_API_KEY', ''),
        'base_url': 'https://api.exchangerate-api.com/v4/latest/',
        'currencies': ['USD', 'EUR', 'CNY', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF']
    },
    
    # 股票市场数据源
    'stock_markets': {
        'us_markets': ['^GSPC', '^DJI', '^IXIC'],  # 标普500、道琼斯、纳斯达克
        'asia_markets': ['^N225', '^HSI', '^KS11'],  # 日经、恒生、韩国综合
        'europe_markets': ['^GDAXI', '^FCHI', '^FTSE']  # 德国DAX、法国CAC、英国富时
    },
    
    # 债券市场数据源
    'bonds': {
        'us_treasury': ['^TNX', '^TYX', '^IRX'],  # 美国国债收益率
        'china_bonds': ['CGB10Y', 'CGB5Y', 'CGB2Y']  # 中国国债收益率
    },
    
    # 大宗商品数据源
    'commodities': {
        'metals': ['GC=F', 'SI=F', 'PL=F'],  # 黄金、白银、铂金
        'energy': ['CL=F', 'NG=F', 'BZ=F'],  # 原油、天然气、布伦特原油
        'agriculture': ['ZC=F', 'ZS=F', 'KC=F']  # 玉米、大豆、咖啡
    }
}

# 资金流向分析配置
FLOW_ANALYSIS_CONFIG = {
    # 时间窗口配置
    'time_windows': {
        'short_term': 7,      # 短期：7天
        'medium_term': 30,    # 中期：30天
        'long_term': 90       # 长期：90天
    },
    
    # 资金流向指标
    'flow_indicators': {
        'net_flow': True,           # 净流入
        'relative_strength': True,  # 相对强度
        'momentum': True,           # 动量指标
        'volatility': True          # 波动率
    },
    
    # 阈值配置
    'thresholds': {
        'significant_flow': 0.05,   # 显著资金流向阈值（5%）
        'extreme_flow': 0.10,       # 极端资金流向阈值（10%）
        'trend_change': 0.03        # 趋势变化阈值（3%）
    }
}

# 可视化配置
VISUALIZATION_CONFIG = {
    'chart_colors': {
        'positive_flow': '#00ff00',    # 资金流入：绿色
        'negative_flow': '#ff0000',    # 资金流出：红色
        'neutral_flow': '#808080',     # 中性：灰色
        'trend_line': '#0000ff',       # 趋势线：蓝色
        'background': '#f8f9fa'        # 背景色
    },
    
    'chart_styles': {
        'width': 1200,
        'height': 800,
        'font_size': 12,
        'title_size': 16
    }
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/global_flow_analysis.log'
}

# API配置
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5003,
    'debug': True,
    'threaded': True
}

# 缓存配置
CACHE_CONFIG = {
    'enabled': True,
    'ttl': 3600,  # 1小时缓存
    'max_size': 1000
}

# 数据更新频率（分钟）
UPDATE_FREQUENCY = {
    'real_time': 1,      # 实时数据：1分钟
    'intraday': 5,       # 日内数据：5分钟
    'daily': 1440,       # 日线数据：24小时
    'weekly': 10080      # 周线数据：7天
} 