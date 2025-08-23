"""
日志管理器
提供统一的日志记录功能
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class Logger:
    """日志管理器 - 单例模式"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """设置日志配置"""
        # 创建日志目录
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 创建日志文件名
        log_file = os.path.join(log_dir, f"company_list_{datetime.now().strftime('%Y%m%d')}.log")
        
        # 创建日志记录器
        self._logger = logging.getLogger('company_list')
        self._logger.setLevel(logging.DEBUG)
        
        # 清除现有的处理器
        self._logger.handlers.clear()
        
        # 文件处理器
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def info(self, message):
        """记录信息日志"""
        self._logger.info(message)
    
    def warning(self, message):
        """记录警告日志"""
        self._logger.warning(message)
    
    def error(self, message):
        """记录错误日志"""
        self._logger.error(message)
    
    def debug(self, message):
        """记录调试日志"""
        self._logger.debug(message)
    
    def critical(self, message):
        """记录严重错误日志"""
        self._logger.critical(message)
    
    def exception(self, message):
        """记录异常日志"""
        self._logger.exception(message)


# 创建全局日志实例
logger = Logger() 