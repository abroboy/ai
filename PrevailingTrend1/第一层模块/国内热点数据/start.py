#!/usr/bin/env python3
"""
国内热点数据模块启动脚本
"""

import os
import sys
import time
import threading
from datetime import datetime
from loguru import logger

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from utils.database import db_manager
from core.data_collector import DataCollector
from core.data_processor import DataProcessor
from app import app


def setup_logging():
    """设置日志"""
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    
    # 配置日志
    logger.add(
        config.LOGGING['file'],
        level=config.LOGGING['level'],
        format=config.LOGGING['format'],
        rotation=config.LOGGING['max_size'],
        retention=config.LOGGING['retention']
    )


def init_database():
    """初始化数据库"""
    try:
        logger.info("初始化数据库...")
        db_manager.create_tables()
        logger.info("数据库初始化完成")
        return True
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        return False


def start_data_collection():
    """启动数据采集"""
    def collect_loop():
        collector = DataCollector()
        processor = DataProcessor()
        
        while True:
            try:
                logger.info("开始采集热点数据...")
                
                # 采集数据
                hotspots = collector.collect_all_hotspots()
                logger.info(f"采集到 {len(hotspots)} 条热点数据")
                
                # 处理数据
                processed_hotspots = processor.process_hotspots(hotspots)
                logger.info(f"处理完成 {len(processed_hotspots)} 条热点数据")
                
                # 保存到数据库
                success_count = db_manager.batch_insert_hotspots(processed_hotspots)
                logger.info(f"保存到数据库 {success_count} 条热点数据")
                
                # 等待下次采集
                time.sleep(config.UPDATE['update_interval'])
                
            except Exception as e:
                logger.error(f"数据采集失败: {e}")
                time.sleep(60)  # 出错后等待1分钟再重试
    
    # 启动采集线程
    collection_thread = threading.Thread(target=collect_loop, daemon=True)
    collection_thread.start()
    logger.info("数据采集线程已启动")


def start_web_server():
    """启动Web服务器"""
    try:
        logger.info(f"启动Web服务器: http://{config.WEB['host']}:{config.WEB['port']}")
        app.run(
            host=config.WEB['host'],
            port=config.WEB['port'],
            debug=config.WEB['debug']
        )
    except Exception as e:
        logger.error(f"Web服务器启动失败: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("国内热点数据模块")
    print("=" * 60)
    
    # 设置日志
    setup_logging()
    logger.info("国内热点数据模块启动")
    
    # 初始化数据库
    if not init_database():
        logger.error("数据库初始化失败，程序退出")
        sys.exit(1)
    
    # 启动数据采集
    if config.UPDATE['auto_update']:
        start_data_collection()
    
    # 启动Web服务器
    start_web_server()


if __name__ == "__main__":
    main() 