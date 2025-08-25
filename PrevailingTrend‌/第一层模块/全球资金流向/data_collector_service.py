#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球资金流向数据收集服务
独立的数据拉取和入库模块
"""

import os
import sys
import time
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.data_collector import GlobalFlowDataCollector
from core.flow_analyzer import FlowAnalyzer
from utils.database import DatabaseManager
from utils.logger import setup_logger

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 设置日志
logger = setup_logger('data_collector', 'logs/data_collector.log')

# 初始化数据库管理器
db_manager = DatabaseManager()

# 初始化数据收集器
data_collector = GlobalFlowDataCollector()
flow_analyzer = FlowAnalyzer()

class DataCollectorService:
    """数据收集服务类"""
    
    def __init__(self):
        self.is_running = False
        self.last_collection_time = None
        self.collection_interval = 3600  # 1小时收集一次
        
    def start_collection(self):
        """开始数据收集"""
        if self.is_running:
            return {"success": False, "message": "数据收集服务已在运行"}
        
        self.is_running = True
        logger.info("数据收集服务已启动")
        
        try:
            # 收集全球资金流向数据
            flow_data = data_collector.collect_global_flow_data()
            
            # 分析数据
            analysis_result = flow_analyzer.analyze_flow_data(flow_data)
            
            # 存储到数据库
            self._store_data(flow_data, analysis_result)
            
            self.last_collection_time = datetime.now()
            logger.info(f"数据收集完成，共收集 {len(flow_data)} 条记录")
            
            return {
                "success": True,
                "message": "数据收集完成",
                "data": {
                    "total_records": len(flow_data),
                    "collection_time": self.last_collection_time.isoformat(),
                    "analysis_summary": analysis_result.get('summary', {})
                }
            }
            
        except Exception as e:
            logger.error(f"数据收集失败: {e}")
            self.is_running = False
            return {"success": False, "message": f"数据收集失败: {str(e)}"}
    
    def stop_collection(self):
        """停止数据收集"""
        self.is_running = False
        logger.info("数据收集服务已停止")
        return {"success": True, "message": "数据收集服务已停止"}
    
    def get_status(self):
        """获取服务状态"""
        return {
            "success": True,
            "data": {
                "is_running": self.is_running,
                "last_collection_time": self.last_collection_time.isoformat() if self.last_collection_time else None,
                "collection_interval": self.collection_interval,
                "database_connected": db_manager.is_connected()
            }
        }
    
    def _store_data(self, flow_data, analysis_result):
        """存储数据到数据库"""
        try:
            # 存储原始数据
            for data in flow_data:
                db_manager.insert_flow_data(data)
            
            # 存储分析结果
            db_manager.insert_analysis_result(analysis_result)
            
            logger.info("数据存储完成")
            
        except Exception as e:
            logger.error(f"数据存储失败: {e}")
            raise

# 创建服务实例
collector_service = DataCollectorService()

@app.route('/api/status')
def status():
    """服务状态API"""
    return jsonify(collector_service.get_status())

@app.route('/api/start_collection', methods=['POST'])
def start_collection():
    """启动数据收集API"""
    return jsonify(collector_service.start_collection())

@app.route('/api/stop_collection', methods=['POST'])
def stop_collection():
    """停止数据收集API"""
    return jsonify(collector_service.stop_collection())

@app.route('/api/collect_once', methods=['POST'])
def collect_once():
    """执行一次数据收集API"""
    return jsonify(collector_service.start_collection())

@app.route('/api/database_info')
def database_info():
    """数据库信息API"""
    try:
        info = db_manager.get_database_info()
        return jsonify({
            "success": True,
            "data": info
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取数据库信息失败: {str(e)}"
        })

@app.route('/api/health')
def health_check():
    """健康检查API"""
    return jsonify({
        "success": True,
        "message": "数据收集服务运行正常",
        "timestamp": datetime.now().isoformat(),
        "service": "data_collector"
    })

if __name__ == '__main__':
    print("=" * 60)
    print("全球资金流向数据收集服务")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("服务正在启动...")
    print()
    print("API端点:")
    print("- 服务状态: http://localhost:5004/api/status")
    print("- 启动收集: http://localhost:5004/api/start_collection")
    print("- 停止收集: http://localhost:5004/api/stop_collection")
    print("- 执行收集: http://localhost:5004/api/collect_once")
    print("- 数据库信息: http://localhost:5004/api/database_info")
    print("- 健康检查: http://localhost:5004/api/health")
    print("=" * 60)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5004,
            debug=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n数据收集服务已停止")
    except Exception as e:
        print(f"启动失败: {e}") 