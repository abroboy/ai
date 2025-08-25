#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球资金流向数据收集服务 - 简化版
"""

import os
import json
import logging
import random
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 创建必要的目录
os.makedirs('logs', exist_ok=True)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleDataCollector:
    def __init__(self):
        self.is_running = False
        self.last_collection_time = None
        self.collected_data = []
        
    def start_collection(self):
        if self.is_running:
            return {"success": False, "message": "数据收集服务已在运行"}
        
        self.is_running = True
        logger.info("数据收集服务已启动")
        
        try:
            # 生成模拟数据
            mock_data = self._generate_mock_data()
            self.collected_data.extend(mock_data)
            
            self.last_collection_time = datetime.now()
            logger.info(f"数据收集完成，共收集 {len(mock_data)} 条记录")
            
            return {
                "success": True,
                "message": "数据收集完成",
                "data": {
                    "total_records": len(mock_data),
                    "collection_time": self.last_collection_time.isoformat(),
                    "total_stored": len(self.collected_data)
                }
            }
            
        except Exception as e:
            logger.error(f"数据收集失败: {e}")
            self.is_running = False
            return {"success": False, "message": f"数据收集失败: {str(e)}"}
    
    def stop_collection(self):
        self.is_running = False
        logger.info("数据收集服务已停止")
        return {"success": True, "message": "数据收集服务已停止"}
    
    def get_status(self):
        return {
            "success": True,
            "data": {
                "is_running": self.is_running,
                "last_collection_time": self.last_collection_time.isoformat() if self.last_collection_time else None,
                "total_stored_records": len(self.collected_data),
                "database_connected": True
            }
        }
    
    def _generate_mock_data(self):
        data = []
        current_time = datetime.now()
        
        asset_types = ['forex', 'stock', 'bond', 'commodity']
        regions = ['US', 'Europe', 'Asia', 'Global']
        
        for i in range(50):
            record = {
                'id': len(self.collected_data) + i + 1,
                'timestamp': (current_time - timedelta(minutes=i)).isoformat(),
                'asset_type': random.choice(asset_types),
                'region': random.choice(regions),
                'net_flow': round(random.uniform(-100, 100), 2),
                'volume': round(random.uniform(1000, 10000), 2),
                'price_change': round(random.uniform(-5, 5), 2),
                'sentiment': random.choice(['bullish', 'bearish', 'neutral'])
            }
            data.append(record)
        
        return data

# 创建服务实例
collector_service = SimpleDataCollector()

@app.route('/api/status')
def status():
    return jsonify(collector_service.get_status())

@app.route('/api/start_collection', methods=['POST'])
def start_collection():
    return jsonify(collector_service.start_collection())

@app.route('/api/stop_collection', methods=['POST'])
def stop_collection():
    return jsonify(collector_service.stop_collection())

@app.route('/api/collect_once', methods=['POST'])
def collect_once():
    return jsonify(collector_service.start_collection())

@app.route('/api/health')
def health_check():
    return jsonify({
        "success": True,
        "message": "数据收集服务运行正常",
        "timestamp": datetime.now().isoformat(),
        "service": "simple_data_collector"
    })

@app.route('/api/data')
def get_data():
    return jsonify({
        "success": True,
        "data": {
            "records": collector_service.collected_data[-100:],
            "total_count": len(collector_service.collected_data)
        }
    })

if __name__ == '__main__':
    print("=" * 60)
    print("全球资金流向数据收集服务 - 简化版")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("服务正在启动...")
    print()
    print("API端点:")
    print("- 服务状态: http://localhost:5004/api/status")
    print("- 启动收集: http://localhost:5004/api/start_collection")
    print("- 停止收集: http://localhost:5004/api/stop_collection")
    print("- 执行收集: http://localhost:5004/api/collect_once")
    print("- 健康检查: http://localhost:5004/api/health")
    print("- 获取数据: http://localhost:5004/api/data")
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