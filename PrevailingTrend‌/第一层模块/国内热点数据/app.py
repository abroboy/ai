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

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 初始化组件
data_collector = DataCollector()
data_processor = DataProcessor()

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
    """采集热点数据"""
    try:
        # 采集热点数据
        hotspots = data_collector.collect_all_hotspots()
        
        # 处理热点数据
        processed_hotspots = data_processor.process_hotspots(hotspots)
        
        return jsonify({
            'success': True,
            'data': {
                'collected_count': len(hotspots),
                'processed_count': len(processed_hotspots),
                'message': f'成功采集并处理 {len(processed_hotspots)} 条热点数据'
            }
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

def generate_sample_hotspots() -> List[HotspotModel]:
    """生成示例热点数据"""
    hotspots = []
    
    sample_data = [
        # 新闻热点
        {
            'title': 'A股三大指数集体上涨，科技股领涨',
            'content': '今日A股市场表现强劲，三大指数集体上涨，科技股表现突出。上证指数上涨1.2%，深证成指上涨1.8%，创业板指上涨2.1%。市场成交量明显放大，投资者情绪乐观。',
            'type': HotspotType.NEWS,
            'level': HotspotLevel.HIGH,
            'source': '新浪财经',
            'sentiment': 0.7,
            'heat': 85.0
        },
        {
            'title': '房地产市场调控政策持续优化',
            'content': '各地陆续出台房地产调控优化政策，支持刚需和改善性住房需求。政策包括降低首付比例、调整贷款利率、优化限购政策等，市场预期逐步改善。',
            'type': HotspotType.NEWS,
            'level': HotspotLevel.MEDIUM,
            'source': '财新网',
            'sentiment': 0.4,
            'heat': 70.0
        },
        {
            'title': '科技创新引领经济高质量发展',
            'content': '国家高度重视科技创新，加大研发投入，推动关键核心技术突破。人工智能、量子计算、生物技术等前沿领域取得重要进展，为经济高质量发展提供强劲动力。',
            'type': HotspotType.NEWS,
            'level': HotspotLevel.HIGH,
            'source': '第一财经',
            'sentiment': 0.8,
            'heat': 82.0
        },
        {
            'title': '绿色金融发展提速',
            'content': '绿色金融产品和服务不断创新，绿色债券、绿色信贷规模持续扩大。金融机构积极支持绿色产业发展，推动经济社会绿色转型。',
            'type': HotspotType.NEWS,
            'level': HotspotLevel.MEDIUM,
            'source': '21世纪经济报道',
            'sentiment': 0.6,
            'heat': 68.0
        },
        {
            'title': '数字经济成为经济增长新引擎',
            'content': '数字经济发展迅速，数字产业化、产业数字化进程加快。云计算、大数据、物联网等新技术广泛应用，推动传统产业转型升级。',
            'type': HotspotType.NEWS,
            'level': HotspotLevel.HIGH,
            'source': '经济观察报',
            'sentiment': 0.7,
            'heat': 78.0
        },
        
        # 政策热点
        {
            'title': '央行发布最新货币政策报告',
            'content': '央行发布2024年第一季度货币政策执行报告，强调稳健货币政策，保持流动性合理充裕。报告指出，将继续实施稳健的货币政策，保持货币供应量和社会融资规模增速同名义经济增速基本匹配。',
            'type': HotspotType.POLICY,
            'level': HotspotLevel.VERY_HIGH,
            'source': '央行',
            'sentiment': 0.5,
            'heat': 90.0
        },
        {
            'title': '国务院发布关于促进经济高质量发展的意见',
            'content': '国务院发布重要政策文件，强调经济高质量发展。文件提出要加快构建新发展格局，推动高质量发展，深化供给侧结构性改革，扩大内需，促进消费升级，推动产业升级和科技创新。',
            'type': HotspotType.POLICY,
            'level': HotspotLevel.VERY_HIGH,
            'source': '中国政府网',
            'sentiment': 0.6,
            'heat': 95.0
        },
        {
            'title': '证监会发布资本市场改革措施',
            'content': '证监会发布资本市场改革措施，深化注册制改革，完善多层次资本市场体系。措施包括优化发行上市制度、加强投资者保护、提升监管效能等。',
            'type': HotspotType.POLICY,
            'level': HotspotLevel.HIGH,
            'source': '证监会',
            'sentiment': 0.4,
            'heat': 88.0
        },
        {
            'title': '发改委发布新能源产业发展规划',
            'content': '国家发改委发布新能源产业发展规划，推动绿色转型。规划提出到2030年，非化石能源占一次能源消费比重达到25%左右，风电、太阳能发电总装机容量达到12亿千瓦以上。',
            'type': HotspotType.POLICY,
            'level': HotspotLevel.HIGH,
            'source': '发改委',
            'sentiment': 0.7,
            'heat': 85.0
        },
        
        # 行业热点
        {
            'title': '汽车行业电动化转型加速',
            'content': '汽车行业电动化转型加速，传统车企纷纷加大新能源汽车投入。比亚迪、吉利、长城等自主品牌在电动化领域取得重要突破，市场份额持续提升。',
            'type': HotspotType.INDUSTRY,
            'level': HotspotLevel.MEDIUM,
            'source': '中国汽车工业协会',
            'sentiment': 0.8,
            'heat': 75.0
        },
        {
            'title': '钢铁行业绿色低碳发展',
            'content': '钢铁行业积极推进绿色低碳发展，加大环保投入，推广清洁生产技术。行业集中度进一步提升，龙头企业竞争力增强。',
            'type': HotspotType.INDUSTRY,
            'level': HotspotLevel.MEDIUM,
            'source': '中国钢铁工业协会',
            'sentiment': 0.6,
            'heat': 65.0
        },
        {
            'title': '有色金属行业技术创新',
            'content': '有色金属行业技术创新取得重要进展，新材料研发应用加快。铝、铜、锂等金属在新能源、电子等领域的应用不断扩大。',
            'type': HotspotType.INDUSTRY,
            'level': HotspotLevel.MEDIUM,
            'source': '中国有色金属工业协会',
            'sentiment': 0.7,
            'heat': 70.0
        },
        
        # 市场热点
        {
            'title': '科创板注册制改革成效显著',
            'content': '科创板注册制改革成效显著，服务科技创新企业能力持续增强。科创板上市公司数量和质量不断提升，为科技创新企业提供重要融资平台。',
            'type': HotspotType.MARKET,
            'level': HotspotLevel.HIGH,
            'source': '上海证券交易所',
            'sentiment': 0.6,
            'heat': 80.0
        },
        {
            'title': '创业板改革深化',
            'content': '创业板改革深化，注册制试点稳步推进。创业板服务成长型创新创业企业功能进一步增强，市场活力持续释放。',
            'type': HotspotType.MARKET,
            'level': HotspotLevel.HIGH,
            'source': '深圳证券交易所',
            'sentiment': 0.5,
            'heat': 78.0
        },
        {
            'title': '北交所建设稳步推进',
            'content': '北交所建设稳步推进，服务中小企业能力不断提升。北交所为专精特新中小企业提供重要融资渠道，促进中小企业高质量发展。',
            'type': HotspotType.MARKET,
            'level': HotspotLevel.MEDIUM,
            'source': '北京证券交易所',
            'sentiment': 0.7,
            'heat': 72.0
        },
        
        # 公司热点
        {
            'title': '阿里巴巴发布最新财报',
            'content': '阿里巴巴发布2024年第一季度财报，营收和利润均超预期，股价大涨。公司云计算、数字媒体等业务表现亮眼，未来发展前景看好。',
            'type': HotspotType.COMPANY,
            'level': HotspotLevel.HIGH,
            'source': '新浪财经',
            'sentiment': 0.9,
            'heat': 80.0
        },
        {
            'title': '腾讯游戏业务增长强劲',
            'content': '腾讯游戏业务增长强劲，多款新游戏表现优异。公司持续加大游戏研发投入，海外市场拓展取得重要进展。',
            'type': HotspotType.COMPANY,
            'level': HotspotLevel.MEDIUM,
            'source': '东方财富',
            'sentiment': 0.8,
            'heat': 75.0
        },
        {
            'title': '比亚迪新能源汽车销量创新高',
            'content': '比亚迪新能源汽车销量创新高，市场份额持续提升。公司在电池技术、车型设计等方面取得重要突破，竞争优势明显。',
            'type': HotspotType.COMPANY,
            'level': HotspotLevel.HIGH,
            'source': '证券时报',
            'sentiment': 0.9,
            'heat': 85.0
        }
    ]
    
    for i, data in enumerate(sample_data):
        hotspot = HotspotModel(
            hotspot_id=f"sample_{i}_{int(datetime.now().timestamp())}",
            title=data['title'],
            content=data['content'],
            hotspot_type=data['type'],
            hotspot_level=data['level'],
            status=HotspotStatus.ACTIVE,
            source=data['source'],
            url=f"https://example.com/hotspot/{i}",
            publish_time=datetime.now() - timedelta(hours=i),
            keywords=['股票', '经济', '政策'] if i % 2 == 0 else ['科技', '创新', '发展'],
            related_companies=['阿里巴巴', '腾讯'] if i % 2 == 0 else ['比亚迪', '特斯拉'],
            related_industries=['801080', '801090'] if i % 2 == 0 else ['801770'],
            sentiment_score=data['sentiment'],
            heat_score=data['heat'],
            update_date=datetime.now()
        )
        hotspots.append(hotspot)
    
    return hotspots

if __name__ == '__main__':
    app.run(
        host=config.WEB['host'],
        port=config.WEB['port'],
        debug=config.WEB['debug']
    ) 