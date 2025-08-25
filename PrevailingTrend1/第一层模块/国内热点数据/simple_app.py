"""
国内热点数据管理台 - 简化版
Flask Web应用（不包含后台数据更新任务）
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
from typing import Dict, Any, List
import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus
from core.data_collector import DataCollector
from core.data_processor import DataProcessor
from core.data_storage import DataStorage
from loguru import logger

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 初始化组件
data_collector = DataCollector()
data_processor = DataProcessor()
data_storage = DataStorage()

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """仪表盘"""
    return render_template('dashboard.html')

@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': '国内热点数据管理台'
    })

@app.route('/api/statistics')
def get_statistics():
    """获取统计信息"""
    try:
        # 从数据库获取统计数据
        stats = data_storage.get_statistics()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hotspots')
def get_hotspots():
    """获取热点数据列表"""
    try:
        # 获取查询参数
        hotspot_type = request.args.get('hotspot_type')
        hotspot_level = request.args.get('hotspot_level')
        status = request.args.get('status')
        source = request.args.get('source')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        sort_by = request.args.get('sort_by', 'publish_time')
        sort_order = request.args.get('sort_order', 'desc')
        
        # 从数据库获取数据
        result = data_storage.get_hotspots_from_db(
            page=page,
            per_page=per_page,
            hotspot_type=hotspot_type,
            source=source,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # 转换为字典
        hotspot_list = []
        for hotspot in result['hotspots']:
            hotspot_list.append({
                'hotspot_id': hotspot.hotspot_id,
                'title': hotspot.title,
                'content': hotspot.content[:100] + '...' if len(hotspot.content) > 100 else hotspot.content,
                'hotspot_type': hotspot.hotspot_type.value,
                'hotspot_level': hotspot.hotspot_level.value,
                'status': hotspot.status.value,
                'source': hotspot.source,
                'url': hotspot.url,
                'publish_time': hotspot.publish_time.isoformat() if hotspot.publish_time else None,
                'keywords': hotspot.keywords,
                'related_companies': hotspot.related_companies,
                'related_industries': hotspot.related_industries,
                'sentiment_score': hotspot.sentiment_score,
                'heat_score': hotspot.heat_score,
                'update_date': hotspot.update_date.isoformat() if hotspot.update_date else None
            })
        
        return jsonify({
            'success': True,
            'data': {
                'hotspots': hotspot_list,
                'pagination': {
                    'page': result['page'],
                    'per_page': result['per_page'],
                    'total': result['total'],
                    'pages': result['total_pages']
                },
                'sorting': {
                    'sort_by': result['sort_by'],
                    'sort_order': result['sort_order']
                }
            }
        })
        
    except Exception as e:
        logger.error(f"获取热点数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hotspots/<hotspot_id>')
def get_hotspot_detail(hotspot_id):
    """获取热点详情"""
    try:
        hotspot = data_storage.get_hotspot_by_id(hotspot_id)
        if hotspot:
            return jsonify({
                'success': True,
                'data': {
                    'hotspot_id': hotspot.hotspot_id,
                    'title': hotspot.title,
                    'content': hotspot.content,
                    'hotspot_type': hotspot.hotspot_type.value,
                    'hotspot_level': hotspot.hotspot_level.value,
                    'status': hotspot.status.value,
                    'source': hotspot.source,
                    'url': hotspot.url,
                    'publish_time': hotspot.publish_time.isoformat() if hotspot.publish_time else None,
                    'keywords': hotspot.keywords,
                    'related_companies': hotspot.related_companies,
                    'related_industries': hotspot.related_industries,
                    'sentiment_score': hotspot.sentiment_score,
                    'heat_score': hotspot.heat_score,
                    'update_date': hotspot.update_date.isoformat() if hotspot.update_date else None
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': '热点不存在'
            }), 404
            
    except Exception as e:
        logger.error(f"获取热点详情失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/collect', methods=['POST'])
def collect_data():
    """手动触发数据采集"""
    try:
        # 采集数据
        hotspots = data_collector.collect_all_hotspots()
        logger.info(f"采集到 {len(hotspots)} 条热点数据")
        
        # 处理数据
        processed_hotspots = data_processor.process_hotspots(hotspots)
        logger.info(f"处理完成 {len(processed_hotspots)} 条热点数据")
        
        # 保存到数据库
        success_count = data_storage.batch_insert_hotspots(processed_hotspots)
        logger.info(f"保存到数据库 {success_count} 条热点数据")
        
        return jsonify({
            'success': True,
            'message': f'数据采集完成，共处理 {success_count} 条热点数据',
            'data': {
                'collected': len(hotspots),
                'processed': len(processed_hotspots),
                'saved': success_count
            }
        })
        
    except Exception as e:
        logger.error(f"数据采集失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("国内热点数据管理台 - 简化版")
    print("=" * 60)
    print(f"服务地址: http://{config.WEB['host']}:{config.WEB['port']}")
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    
    app.run(
        host=config.WEB['host'],
        port=config.WEB['port'],
        debug=config.WEB['debug']
    ) 