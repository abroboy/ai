#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球资金流向分析系统启动脚本
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from utils.logger import setup_logger
from utils.database import DatabaseManager
from core.data_collector import DataCollector
from core.flow_analyzer import FlowAnalyzer
from app import app

def initialize_system():
    """初始化系统"""
    logger = setup_logger('system_init')
    logger.info("开始初始化全球资金流向分析系统")
    
    try:
        # 创建必要的目录
        directories = [
            'logs',
            'static/charts',
            'static/reports',
            'data'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"创建目录: {directory}")
        
        # 初始化数据库
        db_manager = DatabaseManager()
        if db_manager.connect():
            db_manager.create_tables()
            logger.info("数据库初始化成功")
        else:
            logger.error("数据库连接失败")
            return False
        
        # 初始化数据收集器
        data_collector = DataCollector(db_manager)
        logger.info("数据收集器初始化成功")
        
        # 初始化分析器
        flow_analyzer = FlowAnalyzer(db_manager)
        logger.info("资金流向分析器初始化成功")
        
        logger.info("系统初始化完成")
        return True
        
    except Exception as e:
        logger.error(f"系统初始化失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("全球资金流向分析系统")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 初始化系统
    if not initialize_system():
        print("系统初始化失败，请检查配置和数据库连接")
        sys.exit(1)
    
    print("系统初始化成功！")
    print("正在启动Web服务...")
    print()
    
    # 启动Flask应用
    try:
        app.run(
            host='0.0.0.0',
            port=5003,
            debug=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n系统已停止")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == '__main__':
    main() 