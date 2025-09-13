"""
国外热点数据Web应用
"""

from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
from datetime import datetime
from loguru import logger
from config import Config
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.logger import Logger
from core.international_hotspot_manager import InternationalHotspotManager

# 初始化日志
Logger.setup()

app = Flask(__name__)
CORS(app)

# 初始化管理器
manager = InternationalHotspotManager()

@app.route('/')
def index():
    """首页 - 直接重定向到dashboard"""
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    """仪表盘页面"""
    return render_template('dashboard_v2.5.html')

@app.route('/test-fix')
def test_fix():
    """测试修复页面"""
    return render_template('test_fix.html')

@app.route('/simple-test')
def simple_test():
    """简单测试页面"""
    return render_template('simple_test.html')

@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'International Hotspot Data Service'
    })

@app.route('/api/hotspots')
def get_hotspots():
    """获取热点数据列表"""
    try:
        limit = request.args.get('limit', 100, type=int)
        hotspots = manager.get_hotspots(limit)
        
        return jsonify({
            'success': True,
            'data': hotspots,
            'count': len(hotspots)
        })
    except Exception as e:
        logger.error(f"获取热点数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistics')
def get_statistics():
    """获取统计数据"""
    try:
        stats = manager.get_statistics()
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"获取统计数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/collect', methods=['POST'])
def collect_data():
    """手动触发数据收集"""
    try:
        success = manager.run_collection()
        
        return jsonify({
            'success': success,
            'message': '数据收集完成' if success else '数据收集失败'
        })
    except Exception as e:
        logger.error(f"数据收集失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    logger.info(f"启动国外热点数据服务，端口: {Config.WEB['port']}")
    app.run(
        host=Config.WEB['host'],
        port=Config.WEB['port'],
        debug=Config.WEB['debug']
    ) 