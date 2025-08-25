"""
日志管理工具
提供统一的日志记录功能，支持文件和控制台输出
"""

import logging
import os
from datetime import datetime
from typing import Optional
from pathlib import Path


class Logger:
    """日志管理类"""
    
    _instance = None
    _logger = None
    
    def __new__(cls, name: str = "industry_classification"):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, name: str = "industry_classification"):
        """初始化日志器"""
        if self._logger is None:
            self._logger = self._setup_logger(name)
    
    def _setup_logger(self, name: str) -> logging.Logger:
        """设置日志器"""
        logger = logging.getLogger(name)
        
        # 避免重复添加处理器
        if logger.handlers:
            return logger
        
        logger.setLevel(logging.INFO)
        
        # 创建日志目录
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 文件处理器
        log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
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
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def info(self, message: str):
        """记录信息日志"""
        self._logger.info(message)
    
    def warning(self, message: str):
        """记录警告日志"""
        self._logger.warning(message)
    
    def error(self, message: str):
        """记录错误日志"""
        self._logger.error(message)
    
    def debug(self, message: str):
        """记录调试日志"""
        self._logger.debug(message)
    
    def critical(self, message: str):
        """记录严重错误日志"""
        self._logger.critical(message)
    
    def exception(self, message: str):
        """记录异常日志"""
        self._logger.exception(message)


# 全局日志实例
logger = Logger() 