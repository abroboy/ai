"""
日志工具类
"""

import os
from loguru import logger
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config


class Logger:
    """日志管理类"""
    
    @staticmethod
    def setup():
        """设置日志配置"""
        # 创建日志目录
        log_dir = os.path.dirname(Config.LOGGING['file'])
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 移除默认处理器
        logger.remove()
        
        # 添加控制台处理器
        logger.add(
            sink=lambda msg: print(msg, end=""),
            level=Config.LOGGING['level'],
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
        
        # 添加文件处理器
        logger.add(
            sink=Config.LOGGING['file'],
            level=Config.LOGGING['level'],
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="100 MB",
            retention="30 days",
            encoding="utf-8"
        )
        
        logger.info("日志系统初始化完成")
    
    @staticmethod
    def get_logger(name: str = None):
        """获取日志记录器"""
        return logger.bind(name=name) if name else logger 