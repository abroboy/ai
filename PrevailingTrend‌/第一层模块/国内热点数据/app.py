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

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 初始化组件
data_collector = DataCollector()
data_processor = DataProcessor()
data_generator = DataGenerator()
real_data_collector = RealDataCollector()

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
        
        # 模拟热点数据
        hotspots = generate_sample_hotspots()
        
        # 过滤数据
        if hotspot_type:
            hotspots = [h for h in hotspots if h.hotspot_type.value == hotspot_type]
        if hotspot_level:
            hotspots = [h for h in hotspots if h.hotspot_level.value == hotspot_level]
        if status:
            hotspots = [h for h in hotspots if h.status.value == status]
        if source:
            hotspots = [h for h in hotspots if h.source == source]
        
        # 分页
        total = len(hotspots)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_hotspots = hotspots[start:end]
        
        # 转换为字典
        hotspot_list = []
        for hotspot in paginated_hotspots:
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
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
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
        # 模拟获取热点详情
        hotspots = generate_sample_hotspots()
        hotspot = next((h for h in hotspots if h.hotspot_id == hotspot_id), None)
        
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
        hotspots = generate_sample_hotspots()
        
        # 按类型统计
        by_type = {}
        for hotspot in hotspots:
            type_name = hotspot.hotspot_type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
        
        # 按级别统计
        by_level = {}
        for hotspot in hotspots:
            level_name = hotspot.hotspot_level.value
            by_level[level_name] = by_level.get(level_name, 0) + 1
        
        # 按状态统计
        by_status = {}
        for hotspot in hotspots:
            status_name = hotspot.status.value
            by_status[status_name] = by_status.get(status_name, 0) + 1
        
        # 按来源统计
        by_source = {}
        for hotspot in hotspots:
            source_name = hotspot.source
            by_source[source_name] = by_source.get(source_name, 0) + 1
        
        # 平均情感得分
        sentiment_scores = [h.sentiment_score for h in hotspots if h.sentiment_score is not None]
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        # 平均热度得分
        heat_scores = [h.heat_score for h in hotspots if h.heat_score is not None]
        avg_heat = sum(heat_scores) / len(heat_scores) if heat_scores else 0
        
        # 关键词统计
        keyword_count = {}
        for hotspot in hotspots:
            for keyword in hotspot.keywords:
                keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
        
        top_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 公司统计
        company_count = {}
        for hotspot in hotspots:
            for company in hotspot.related_companies:
                company_count[company] = company_count.get(company, 0) + 1
        
        top_companies = sorted(company_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return jsonify({
            'success': True,
            'data': {
                'total_count': len(hotspots),
                'by_type': by_type,
                'by_level': by_level,
                'by_status': by_status,
                'by_source': by_source,
                'avg_sentiment': round(avg_sentiment, 2),
                'avg_heat': round(avg_heat, 2),
                'top_keywords': top_keywords,
                'top_companies': top_companies
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/collect', methods=['POST'])
def collect_hotspots():
    """采集真实热点数据"""
    try:
        logger.info("手动触发真实数据采集...")
        real_hotspots = real_data_collector.collect_all_real_data()
        
        if real_hotspots:
            # 处理热点数据
            processed_hotspots = data_processor.process_hotspots(real_hotspots)
            
            return jsonify({
                'success': True,
                'data': {
                    'collected_count': len(real_hotspots),
                    'processed_count': len(processed_hotspots),
                    'message': f'成功采集并处理 {len(processed_hotspots)} 条真实热点数据'
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': '未获取到真实数据'
            }), 500
        
    except Exception as e:
        logger.error(f"数据采集失败: {e}")
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