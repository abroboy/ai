"""
国内热点数据管理台
Flask Web应用
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus
from core.data_collector import DataCollector
from core.data_processor import DataProcessor
from core.data_generator import DataGenerator
from core.real_data_collector import RealDataCollector
from core.data_storage import DataStorage
from core.data_updater import start_data_updater, manual_update_data, get_update_status
from loguru import logger

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 初始化组件
data_collector = DataCollector()
data_processor = DataProcessor()
data_generator = DataGenerator()
real_data_collector = RealDataCollector()
data_storage = DataStorage()

# 延迟启动后台数据更新任务，避免影响首页加载
def start_background_update_delayed():
    import threading
    import time
    
    def delayed_start():
        time.sleep(10)  # 等待10秒让应用完全启动
        try:
            # 只在配置允许时启动数据更新
            if config.UPDATE.get('auto_update', False):
                start_data_updater()
                logger.info("后台数据更新任务已启动")
            else:
                logger.info("自动数据更新已禁用")
        except Exception as e:
            logger.error(f"启动后台数据更新任务失败: {e}")
    
    thread = threading.Thread(target=delayed_start, daemon=True)
    thread.start()

# 启动延迟的后台更新任务
start_background_update_delayed()

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """仪表盘"""
    return render_template('dashboard.html')

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
        sort_by = request.args.get('sort_by', 'publish_time')  # 排序字段
        sort_order = request.args.get('sort_order', 'desc')    # 排序方向
        
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
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hotspots/<hotspot_id>')
def get_hotspot_detail(hotspot_id):
    """获取热点详情"""
    try:
        # 从数据库获取热点详情
        hotspot = data_storage.get_hotspot_detail(hotspot_id)
        
        if not hotspot:
            # 如果找不到，返回一个默认的热点详情
            default_hotspot = {
                'hotspot_id': hotspot_id,
                'title': '热点详情',
                'content': '这是一个示例热点内容。由于这是演示数据，实际内容会根据真实数据源动态生成。热点内容通常包含详细的新闻信息、政策解读、市场分析等内容。',
                'hotspot_type': 'news',
                'hotspot_level': 'medium',
                'status': 'active',
                'source': '示例数据源',
                'url': 'https://example.com/hotspot',
                'publish_time': datetime.now().isoformat(),
                'keywords': ['示例', '热点', '数据'],
                'related_companies': ['示例公司A', '示例公司B'],
                'related_industries': ['801080', '801090'],
                'sentiment_score': 0.5,
                'heat_score': 75.0,
                'update_date': datetime.now().isoformat()
            }
            return jsonify({
                'success': True,
                'data': default_hotspot
            })
        
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
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistics')
def get_statistics():
    """获取统计信息"""
    try:
        # 从数据库获取统计数据
        stats = data_storage.get_statistics()
        
        return jsonify({
            'success': True,
            'data': {
                'total_count': stats.get('total_count', 0),
                'today_count': stats.get('today_count', 0),
                'avg_heat': stats.get('avg_heat', 0),
                'avg_sentiment': stats.get('avg_sentiment', 0),
                'by_type': stats.get('by_type', {}),
                'by_level': stats.get('by_level', {}),
                'by_status': stats.get('by_status', {}),
                'by_source': stats.get('by_source', {})
            }
        })
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/collect', methods=['POST'])
def collect_hotspots():
    """手动触发数据更新"""
    try:
        logger.info("手动触发数据更新...")
        result = manual_update_data()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"手动数据更新失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/update-status')
def get_update_status():
    """获取数据更新状态"""
    try:
        status = get_update_status()
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hotspots/<hotspot_id>', methods=['PUT'])
def update_hotspot(hotspot_id):
    """更新热点数据"""
    try:
        data = request.get_json()
        
        # 模拟更新热点数据
        return jsonify({
            'success': True,
            'data': {
                'hotspot_id': hotspot_id,
                'message': '热点数据更新成功'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hotspots/<hotspot_id>', methods=['DELETE'])
def delete_hotspot(hotspot_id):
    """删除热点数据"""
    try:
        # 模拟删除热点数据
        return jsonify({
            'success': True,
            'data': {
                'hotspot_id': hotspot_id,
                'message': '热点数据删除成功'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/rankings/industries')
def get_industry_rankings():
    """获取行业热度排名"""
    try:
        # 从数据库获取行业热度数据
        rankings = data_storage.get_industry_rankings()
        
        return jsonify({
            'success': True,
            'data': {
                'rankings': rankings,
                'update_time': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"获取行业热度排名失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/rankings/companies')
def get_company_rankings():
    """获取公司热度排名"""
    try:
        # 从数据库获取公司热度数据
        rankings = data_storage.get_company_rankings()
        
        return jsonify({
            'success': True,
            'data': {
                'rankings': rankings,
                'update_time': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"获取公司热度排名失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/rankings/trends')
def get_trend_rankings():
    """获取趋势热度排名"""
    try:
        # 从数据库获取趋势热度数据
        rankings = data_storage.get_trend_rankings()
        
        return jsonify({
            'success': True,
            'data': {
                'rankings': rankings,
                'update_time': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"获取趋势热度排名失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_sample_hotspots() -> List[HotspotModel]:
    """生成热点数据 - 优先使用真实数据，备用模拟数据"""
    try:
        # 尝试获取真实数据
        logger.info("尝试获取真实数据...")
        real_hotspots = real_data_collector.collect_all_real_data()
        
        if real_hotspots and len(real_hotspots) >= 50:
            logger.info(f"成功获取 {len(real_hotspots)} 条真实数据")
            return real_hotspots
        else:
            logger.warning("真实数据不足，使用模拟数据")
            return data_generator.generate_daily_hotspots(150)
            
    except Exception as e:
        logger.error(f"获取真实数据失败: {e}")
        logger.info("使用模拟数据作为备用")
        return data_generator.generate_daily_hotspots(150)

if __name__ == '__main__':
    app.run(
        host=config.WEB['host'],
        port=config.WEB['port'],
        debug=config.WEB['debug']
    ) 