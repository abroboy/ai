"""
万得行业分类模块配置文件
定义数据源、数据库连接、API配置等核心参数
"""

import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """数据库配置"""
    host: str = "localhost"
    port: int = 3306
    database: str = "prevailing_trend"
    username: str = "root"
    password: str = ""
    charset: str = "utf8mb4"
    
    @property
    def connection_string(self) -> str:
        """获取数据库连接字符串"""
        return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?charset={self.charset}"


@dataclass
class WindConfig:
    """万得Wind配置"""
    # 万得Wind API配置
    wind_username: str = ""
    wind_password: str = ""
    wind_server: str = "10.0.0.1"
    wind_port: int = 17011
    
    # 行业分类相关配置
    industry_table: str = "wind_industry_classification"
    stock_industry_table: str = "stock_industry_mapping"
    
    # 数据更新频率配置
    update_frequency_hours: int = 24  # 数据更新频率（小时）
    max_retry_times: int = 3  # 最大重试次数


@dataclass
class TushareConfig:
    """Tushare配置"""
    token: str = ""
    base_url: str = "http://api.tushare.pro"
    
    # API接口配置
    timeout: int = 30
    max_requests_per_minute: int = 500


@dataclass
class AKShareConfig:
    """AKShare配置"""
    base_url: str = "http://push2.eastmoney.com"
    timeout: int = 30
    max_requests_per_minute: int = 100


@dataclass
class LogConfig:
    """日志配置"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "logs/industry_classification.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


class Config:
    """主配置类"""
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.wind = WindConfig()
        self.tushare = TushareConfig()
        self.akshare = AKShareConfig()
        self.log = LogConfig()
        
        # 从环境变量加载配置
        self._load_from_env()
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        # 数据库配置
        self.database.host = os.getenv("DB_HOST", self.database.host)
        self.database.port = int(os.getenv("DB_PORT", str(self.database.port)))
        self.database.database = os.getenv("DB_NAME", self.database.database)
        self.database.username = os.getenv("DB_USER", self.database.username)
        self.database.password = os.getenv("DB_PASSWORD", self.database.password)
        
        # 万得配置
        self.wind.wind_username = os.getenv("WIND_USERNAME", self.wind.wind_username)
        self.wind.wind_password = os.getenv("WIND_PASSWORD", self.wind.wind_password)
        self.wind.wind_server = os.getenv("WIND_SERVER", self.wind.wind_server)
        self.wind.wind_port = int(os.getenv("WIND_PORT", str(self.wind.wind_port)))
        
        # Tushare配置
        self.tushare.token = os.getenv("TUSHARE_TOKEN", self.tushare.token)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "database": {
                "host": self.database.host,
                "port": self.database.port,
                "database": self.database.database,
                "username": self.database.username,
                "charset": self.database.charset
            },
            "wind": {
                "server": self.wind.wind_server,
                "port": self.wind.wind_port,
                "industry_table": self.wind.industry_table,
                "stock_industry_table": self.wind.stock_industry_table,
                "update_frequency_hours": self.wind.update_frequency_hours
            },
            "tushare": {
                "base_url": self.tushare.base_url,
                "timeout": self.tushare.timeout
            },
            "akshare": {
                "base_url": self.akshare.base_url,
                "timeout": self.akshare.timeout
            },
            "log": {
                "level": self.log.level,
                "file_path": self.log.file_path
            }
        }


# 全局配置实例
config = Config() 