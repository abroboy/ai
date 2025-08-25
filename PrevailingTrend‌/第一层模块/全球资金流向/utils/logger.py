# -*- coding: utf-8 -*-
"""
日志管理工具
"""

import os
import logging
import logging.handlers
from datetime import datetime
from config import LOGGING_CONFIG

def setup_logger(name='global_flow_analysis', level=None, log_file=None):
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径
    
    Returns:
        logger: 配置好的日志记录器
    """
    
    # 创建日志目录
    log_dir = os.path.dirname(LOGGING_CONFIG['file'])
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    
    # 设置日志级别
    log_level = level or getattr(logging, LOGGING_CONFIG['level'].upper())
    logger.setLevel(log_level)
    
    # 清除现有的处理器
    logger.handlers.clear()
    
    # 创建格式化器
    formatter = logging.Formatter(LOGGING_CONFIG['format'])
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file or LOGGING_CONFIG['file']:
        file_path = log_file or LOGGING_CONFIG['file']
        
        # 使用RotatingFileHandler进行日志轮转
        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name='global_flow_analysis'):
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
    
    Returns:
        logger: 日志记录器
    """
    return logging.getLogger(name)

class LoggerMixin:
    """日志记录器混入类"""
    
    def __init__(self, logger_name=None):
        """初始化日志记录器"""
        self.logger = get_logger(logger_name or self.__class__.__name__)
    
    def log_info(self, message):
        """记录信息日志"""
        self.logger.info(message)
    
    def log_warning(self, message):
        """记录警告日志"""
        self.logger.warning(message)
    
    def log_error(self, message):
        """记录错误日志"""
        self.logger.error(message)
    
    def log_debug(self, message):
        """记录调试日志"""
        self.logger.debug(message)
    
    def log_exception(self, message):
        """记录异常日志"""
        self.logger.exception(message)

def log_function_call(func):
    """函数调用日志装饰器"""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.info(f"调用函数: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"函数 {func.__name__} 执行成功")
            return result
        except Exception as e:
            logger.error(f"函数 {func.__name__} 执行失败: {e}")
            raise
    return wrapper

def log_performance(func):
    """性能日志装饰器"""
    import time
    
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"函数 {func.__name__} 执行时间: {execution_time:.4f} 秒")
            return result
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.error(f"函数 {func.__name__} 执行失败，耗时: {execution_time:.4f} 秒，错误: {e}")
            raise
    
    return wrapper

class PerformanceLogger:
    """性能日志记录器"""
    
    def __init__(self, name):
        self.name = name
        self.logger = get_logger(name)
        self.start_time = None
    
    def start(self):
        """开始计时"""
        self.start_time = datetime.now()
        self.logger.info(f"开始执行: {self.name}")
    
    def end(self, success=True):
        """结束计时"""
        if self.start_time:
            end_time = datetime.now()
            duration = (end_time - self.start_time).total_seconds()
            
            if success:
                self.logger.info(f"执行完成: {self.name}，耗时: {duration:.4f} 秒")
            else:
                self.logger.error(f"执行失败: {self.name}，耗时: {duration:.4f} 秒")
            
            self.start_time = None
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end(success=exc_type is None) 