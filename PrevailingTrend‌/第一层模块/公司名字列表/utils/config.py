"""
配置管理模块
提供统一的配置管理功能
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """配置管理类"""
    
    # 数据库配置
    DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DATABASE_PORT = int(os.getenv('DATABASE_PORT', 3306))
    DATABASE_USER = os.getenv('DATABASE_USER', 'root')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'prevailing_trend')
    
    # 数据源配置
    SSE_BASE_URL = os.getenv('SSE_BASE_URL', 'http://www.sse.com.cn/')
    SZSE_BASE_URL = os.getenv('SZSE_BASE_URL', 'http://www.szse.cn/')
    HKEX_BASE_URL = os.getenv('HKEX_BASE_URL', 'https://www.hkex.com.hk/')
    
    # API配置
    API_HOST = os.getenv('API_HOST', 'localhost')
    API_PORT = int(os.getenv('API_PORT', 5000))
    API_DEBUG = os.getenv('API_DEBUG', 'False').lower() == 'true'
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/company_list.log')
    
    # 采集配置
    COLLECTION_INTERVAL = int(os.getenv('COLLECTION_INTERVAL', 3600))  # 1小时
    RETRY_TIMES = int(os.getenv('RETRY_TIMES', 3))
    TIMEOUT = int(os.getenv('TIMEOUT', 30))
    
    # 缓存配置
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1小时
    
    # 监控配置
    MONITOR_ENABLED = os.getenv('MONITOR_ENABLED', 'True').lower() == 'true'
    MONITOR_INTERVAL = int(os.getenv('MONITOR_INTERVAL', 300))  # 5分钟
    
    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        """获取数据库配置"""
        return {
            'host': cls.DATABASE_HOST,
            'port': cls.DATABASE_PORT,
            'user': cls.DATABASE_USER,
            'password': cls.DATABASE_PASSWORD,
            'database': cls.DATABASE_NAME
        }
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """获取API配置"""
        return {
            'host': cls.API_HOST,
            'port': cls.API_PORT,
            'debug': cls.API_DEBUG
        }
    
    @classmethod
    def get_log_config(cls) -> Dict[str, Any]:
        """获取日志配置"""
        return {
            'level': cls.LOG_LEVEL,
            'file': cls.LOG_FILE
        }
    
    @classmethod
    def get_collection_config(cls) -> Dict[str, Any]:
        """获取采集配置"""
        return {
            'interval': cls.COLLECTION_INTERVAL,
            'retry_times': cls.RETRY_TIMES,
            'timeout': cls.TIMEOUT
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """验证配置"""
        try:
            # 验证数据库配置
            if not cls.DATABASE_HOST or not cls.DATABASE_NAME:
                print("❌ 数据库配置不完整")
                return False
            
            # 验证API配置
            if cls.API_PORT < 1 or cls.API_PORT > 65535:
                print("❌ API端口配置无效")
                return False
            
            # 验证采集配置
            if cls.COLLECTION_INTERVAL < 60:
                print("❌ 采集间隔配置过短")
                return False
            
            print("✅ 配置验证通过")
            return True
            
        except Exception as e:
            print(f"❌ 配置验证失败: {e}")
            return False
    
    @classmethod
    def print_config(cls):
        """打印配置信息"""
        print("当前配置:")
        print(f"  数据库: {cls.DATABASE_HOST}:{cls.DATABASE_PORT}/{cls.DATABASE_NAME}")
        print(f"  API服务: {cls.API_HOST}:{cls.API_PORT}")
        print(f"  日志级别: {cls.LOG_LEVEL}")
        print(f"  采集间隔: {cls.COLLECTION_INTERVAL}秒")
        print(f"  缓存启用: {cls.CACHE_ENABLED}")
        print(f"  监控启用: {cls.MONITOR_ENABLED}")


# 创建全局配置实例
config = Config() 