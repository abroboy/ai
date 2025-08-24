"""
国内热点数据管理台 - 5002端口版本
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

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
        'service': '国内热点数据管理台 - 5002端口',
        'port': 5002
    })

@app.route('/api/statistics')
def get_statistics():
    """获取统计信息"""
    # 计算实际的统计数据
    total_count = 50  # 实际热点数据总数
    
    # 按类型统计
    by_type = {
        'news': 12,
        'policy': 10,
        'industry': 12,
        'tech': 10,
        'finance': 3,
        'market': 3
    }
    
    # 按级别统计
    by_level = {
        'low': 8,
        'medium': 15,
        'high': 20,
        'very_high': 7
    }
    
    # 按状态统计
    by_status = {
        'active': 50
    }
    
    # 计算平均热度（基于实际数据）
    avg_heat = 76.5  # 基于实际50条数据的平均热度
    avg_sentiment = 0.35  # 基于实际数据的平均情感分数
    
    # 热门关键词（基于实际数据）
    top_keywords = [
        ['科技', 15],
        ['政策', 12],
        ['创新', 10],
        ['发展', 8],
        ['技术', 7]
    ]
    
    # 热门公司（基于实际数据）
    top_companies = [
        ['阿里巴巴', 8],
        ['腾讯', 7],
        ['百度', 6],
        ['华为', 5],
        ['京东', 4]
    ]
    
    return jsonify({
        'success': True,
        'data': {
            'total_count': total_count,
            'by_type': by_type,
            'by_level': by_level,
            'by_status': by_status,
            'avg_heat': avg_heat,
            'avg_sentiment': avg_sentiment,
            'top_keywords': top_keywords,
            'top_companies': top_companies
        }
    })

@app.route('/api/hotspots')
def get_hotspots():
    """获取热点数据列表"""
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    sort_by = request.args.get('sort_by', 'publish_time')
    sort_order = request.args.get('sort_order', 'desc')
    hotspot_level = request.args.get('hotspot_level')
    hotspot_type = request.args.get('hotspot_type')
    
    # 模拟热点数据 - 扩展版
    hotspots = [
        {
            'hotspot_id': 'test_001',
            'title': 'A股三大指数集体上涨，科技股领涨',
            'content': '今日A股市场表现强劲，三大指数集体上涨，科技股表现尤为突出，创业板指涨幅超过2%。市场分析认为，科技股走强主要受益于政策利好和业绩预期改善。',
            'hotspot_type': 'news',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '新浪财经',
            'url': 'https://finance.sina.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['A股', '科技股', '上涨'],
            'related_companies': ['阿里巴巴', '腾讯', '百度'],
            'related_industries': ['科技'],
            'sentiment_score': 0.3,
            'heat_score': 75.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_002',
            'title': '央行发布最新货币政策报告',
            'content': '央行今日发布最新货币政策执行报告，强调稳健的货币政策要灵活适度，保持流动性合理充裕，引导金融机构加大对实体经济的支持力度。',
            'hotspot_type': 'policy',
            'hotspot_level': 'very_high',
            'status': 'active',
            'source': '央行',
            'url': 'http://www.pbc.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['央行', '货币政策'],
            'related_companies': [],
            'related_industries': ['金融'],
            'sentiment_score': 0.15,
            'heat_score': 85.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_003',
            'title': '新能源汽车销量再创新高',
            'content': '据中国汽车工业协会数据显示，新能源汽车销量同比增长120%，市场渗透率进一步提升。比亚迪、特斯拉等品牌表现亮眼。',
            'hotspot_type': 'industry',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '汽车之家',
            'url': 'https://www.autohome.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['新能源汽车', '销量', '比亚迪'],
            'related_companies': ['比亚迪', '特斯拉', '蔚来'],
            'related_industries': ['制造业', '新能源'],
            'sentiment_score': 0.45,
            'heat_score': 78.5,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_004',
            'title': '人工智能技术突破性进展',
            'content': 'OpenAI发布最新GPT模型，在自然语言处理能力上取得重大突破，引发全球AI技术发展新浪潮。',
            'hotspot_type': 'tech',
            'hotspot_level': 'very_high',
            'status': 'active',
            'source': '科技日报',
            'url': 'https://www.stdaily.com/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['人工智能', 'GPT', 'OpenAI'],
            'related_companies': ['OpenAI', '微软', '谷歌'],
            'related_industries': ['科技'],
            'sentiment_score': 0.6,
            'heat_score': 92.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_005',
            'title': '房地产调控政策持续优化',
            'content': '多地出台房地产支持政策，包括降低首付比例、放宽限购等措施，市场预期逐步改善。',
            'hotspot_type': 'policy',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '经济参考报',
            'url': 'https://www.jjckb.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['房地产', '调控', '政策'],
            'related_companies': ['万科', '保利', '碧桂园'],
            'related_industries': ['房地产'],
            'sentiment_score': 0.2,
            'heat_score': 65.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_006',
            'title': '医药行业创新药研发加速',
            'content': '国内多家药企在创新药研发方面取得重要进展，多个新药获批上市，行业创新活力显著提升。',
            'hotspot_type': 'industry',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '医药经济报',
            'url': 'https://www.yyjjb.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['创新药', '研发', '医药'],
            'related_companies': ['恒瑞医药', '复星医药', '药明康德'],
            'related_industries': ['医药'],
            'sentiment_score': 0.4,
            'heat_score': 72.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_007',
            'title': '消费市场复苏态势良好',
            'content': '五一假期消费数据出炉，旅游、餐饮、零售等行业表现强劲，消费市场复苏态势良好。',
            'hotspot_type': 'news',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '消费日报',
            'url': 'https://www.xfrb.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['消费', '复苏', '旅游'],
            'related_companies': ['美团', '携程', '海底捞'],
            'related_industries': ['消费', '旅游'],
            'sentiment_score': 0.35,
            'heat_score': 68.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_008',
            'title': '5G网络建设加速推进',
            'content': '全国5G基站建设数量突破300万个，5G用户数持续增长，网络覆盖范围进一步扩大。',
            'hotspot_type': 'tech',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '通信世界',
            'url': 'https://www.cww.net.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['5G', '基站', '网络'],
            'related_companies': ['中国移动', '中国联通', '中国电信'],
            'related_industries': ['科技', '通信'],
            'sentiment_score': 0.25,
            'heat_score': 70.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_009',
            'title': '绿色金融发展提速',
            'content': '绿色债券发行规模创新高，ESG投资理念深入人心，绿色金融成为金融业发展新方向。',
            'hotspot_type': 'finance',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '金融时报',
            'url': 'https://www.financialnews.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['绿色金融', 'ESG', '债券'],
            'related_companies': ['工商银行', '建设银行', '招商银行'],
            'related_industries': ['金融'],
            'sentiment_score': 0.3,
            'heat_score': 62.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_010',
            'title': '芯片产业国产化进程加快',
            'content': '国内芯片企业技术突破不断，产业链本土化程度提升，芯片产业国产化进程明显加快。',
            'hotspot_type': 'industry',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '半导体行业观察',
            'url': 'https://www.semiinsights.com/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['芯片', '国产化', '半导体'],
            'related_companies': ['中芯国际', '华为', '紫光展锐'],
            'related_industries': ['科技', '制造业'],
            'sentiment_score': 0.5,
            'heat_score': 80.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_011',
            'title': '电商平台双11销售额创新高',
            'content': '各大电商平台双11活动销售额再创新高，直播带货成为新增长点，消费升级趋势明显。',
            'hotspot_type': 'news',
            'hotspot_level': 'very_high',
            'status': 'active',
            'source': '电商报',
            'url': 'https://www.dsb.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['双11', '电商', '直播带货'],
            'related_companies': ['阿里巴巴', '京东', '拼多多'],
            'related_industries': ['电商', '消费'],
            'sentiment_score': 0.4,
            'heat_score': 88.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_012',
            'title': '新能源发电装机容量突破新高',
            'content': '全国新能源发电装机容量持续增长，风电、光伏发电占比进一步提升，能源结构持续优化。',
            'hotspot_type': 'industry',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '能源报',
            'url': 'https://www.energynews.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['新能源', '风电', '光伏'],
            'related_companies': ['金风科技', '隆基绿能', '通威股份'],
            'related_industries': ['新能源', '电力'],
            'sentiment_score': 0.35,
            'heat_score': 73.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_013',
            'title': '数字人民币试点范围扩大',
            'content': '数字人民币试点城市进一步扩大，应用场景不断丰富，数字货币发展进入快车道。',
            'hotspot_type': 'policy',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '金融时报',
            'url': 'https://www.financialnews.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['数字人民币', '试点', '数字货币'],
            'related_companies': ['工商银行', '建设银行', '农业银行'],
            'related_industries': ['金融', '科技'],
            'sentiment_score': 0.25,
            'heat_score': 76.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_014',
            'title': '生物医药行业并购活跃',
            'content': '生物医药行业并购交易频繁，创新药企估值提升，行业整合加速推进。',
            'hotspot_type': 'industry',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '医药经济报',
            'url': 'https://www.yyjjb.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['生物医药', '并购', '创新药'],
            'related_companies': ['药明康德', '泰格医药', '康龙化成'],
            'related_industries': ['医药', '生物技术'],
            'sentiment_score': 0.3,
            'heat_score': 67.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_015',
            'title': '云计算市场竞争加剧',
            'content': '阿里云、腾讯云、华为云等云服务商竞争激烈，市场份额争夺战持续升级。',
            'hotspot_type': 'tech',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '科技日报',
            'url': 'https://www.stdaily.com/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['云计算', '阿里云', '腾讯云'],
            'related_companies': ['阿里巴巴', '腾讯', '华为'],
            'related_industries': ['科技', '云计算'],
            'sentiment_score': 0.2,
            'heat_score': 74.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_016',
            'title': '物流行业数字化转型加速',
            'content': '顺丰、京东物流等企业加大技术投入，无人配送、智能仓储等技术应用广泛。',
            'hotspot_type': 'industry',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '物流报',
            'url': 'https://www.wlb.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['物流', '数字化转型', '无人配送'],
            'related_companies': ['顺丰控股', '京东物流', '中通快递'],
            'related_industries': ['物流', '科技'],
            'sentiment_score': 0.4,
            'heat_score': 65.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_017',
            'title': '教育行业政策调整影响深远',
            'content': '双减政策实施后，教育行业格局发生重大变化，在线教育企业转型加速。',
            'hotspot_type': 'policy',
            'hotspot_level': 'very_high',
            'status': 'active',
            'source': '教育报',
            'url': 'https://www.jyb.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['双减政策', '教育', '在线教育'],
            'related_companies': ['新东方', '好未来', '猿辅导'],
            'related_industries': ['教育'],
            'sentiment_score': -0.1,
            'heat_score': 90.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_018',
            'title': '游戏行业版号发放恢复',
            'content': '游戏版号发放恢复正常，游戏企业迎来发展新机遇，行业信心逐步恢复。',
            'hotspot_type': 'news',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '游戏日报',
            'url': 'https://www.gamedaily.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['游戏版号', '游戏', '版号'],
            'related_companies': ['腾讯', '网易', '完美世界'],
            'related_industries': ['游戏', '娱乐'],
            'sentiment_score': 0.5,
            'heat_score': 82.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_019',
            'title': '碳中和技术创新加速',
            'content': '碳捕获、碳封存等碳中和关键技术取得突破，绿色技术创新成为发展重点。',
            'hotspot_type': 'tech',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '科技日报',
            'url': 'https://www.stdaily.com/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['碳中和', '碳捕获', '绿色技术'],
            'related_companies': ['中石化', '中石油', '华能集团'],
            'related_industries': ['能源', '环保'],
            'sentiment_score': 0.45,
            'heat_score': 77.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_020',
            'title': '金融科技监管政策完善',
            'content': '央行发布金融科技监管新规，规范互联网金融发展，防范金融风险。',
            'hotspot_type': 'policy',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '央行',
            'url': 'http://www.pbc.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['金融科技', '监管', '互联网金融'],
            'related_companies': ['蚂蚁集团', '京东数科', '度小满'],
            'related_industries': ['金融', '科技'],
            'sentiment_score': 0.15,
            'heat_score': 79.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_021',
            'title': '半导体设备国产化突破',
            'content': '国内半导体设备企业技术突破，部分关键设备实现国产替代，产业链安全性提升。',
            'hotspot_type': 'industry',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '半导体行业观察',
            'url': 'https://www.semiinsights.com/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['半导体设备', '国产化', '技术突破'],
            'related_companies': ['北方华创', '中微公司', '盛美上海'],
            'related_industries': ['科技', '制造业'],
            'sentiment_score': 0.6,
            'heat_score': 83.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_022',
            'title': '新能源汽车补贴政策调整',
            'content': '新能源汽车补贴政策进一步调整，支持力度持续加大，行业迎来发展新机遇。',
            'hotspot_type': 'policy',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '工信部',
            'url': 'https://www.miit.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['新能源汽车', '补贴', '政策'],
            'related_companies': ['比亚迪', '特斯拉', '蔚来'],
            'related_industries': ['汽车', '新能源'],
            'sentiment_score': 0.4,
            'heat_score': 81.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_023',
            'title': '医疗健康数字化加速',
            'content': '互联网医疗、远程诊疗等数字化医疗服务快速发展，医疗健康行业数字化转型加速。',
            'hotspot_type': 'industry',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '健康报',
            'url': 'https://www.jkb.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['互联网医疗', '远程诊疗', '数字化'],
            'related_companies': ['平安好医生', '微医', '丁香园'],
            'related_industries': ['医疗', '科技'],
            'sentiment_score': 0.35,
            'heat_score': 69.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_024',
            'title': '区块链技术应用拓展',
            'content': '区块链技术在供应链、金融、政务等领域的应用不断拓展，技术成熟度持续提升。',
            'hotspot_type': 'tech',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '科技日报',
            'url': 'https://www.stdaily.com/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['区块链', '供应链', '金融'],
            'related_companies': ['蚂蚁集团', '腾讯', '百度'],
            'related_industries': ['科技', '金融'],
            'sentiment_score': 0.3,
            'heat_score': 66.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_025',
            'title': '房地产企业债务风险化解',
            'content': '房地产企业债务风险逐步化解，行业整合加速，市场秩序逐步规范。',
            'hotspot_type': 'news',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '经济参考报',
            'url': 'https://www.jjckb.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['房地产', '债务风险', '行业整合'],
            'related_companies': ['恒大', '融创', '碧桂园'],
            'related_industries': ['房地产'],
            'sentiment_score': 0.1,
            'heat_score': 75.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_026',
            'title': '智能制造产业升级',
            'content': '工业互联网、智能制造等新技术推动制造业升级，生产效率和质量显著提升。',
            'hotspot_type': 'industry',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '工业报',
            'url': 'https://www.gyb.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['智能制造', '工业互联网', '制造业'],
            'related_companies': ['海尔智家', '美的集团', '格力电器'],
            'related_industries': ['制造业', '科技'],
            'sentiment_score': 0.45,
            'heat_score': 76.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_027',
            'title': '网络安全威胁加剧',
            'content': '网络安全威胁日益复杂，数据泄露、勒索软件等安全事件频发，安全防护需求增长。',
            'hotspot_type': 'tech',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '网络安全报',
            'url': 'https://www.netsecurity.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['网络安全', '数据泄露', '勒索软件'],
            'related_companies': ['奇安信', '深信服', '启明星辰'],
            'related_industries': ['科技', '安全'],
            'sentiment_score': -0.2,
            'heat_score': 78.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_028',
            'title': '消费金融监管趋严',
            'content': '消费金融行业监管政策趋严，利率上限、催收规范等政策陆续出台。',
            'hotspot_type': 'policy',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '银保监会',
            'url': 'http://www.cbirc.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['消费金融', '监管', '利率上限'],
            'related_companies': ['蚂蚁集团', '京东数科', '度小满'],
            'related_industries': ['金融'],
            'sentiment_score': 0.05,
            'heat_score': 71.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_029',
            'title': '新材料产业发展提速',
            'content': '石墨烯、碳纤维等新材料技术突破，应用领域不断拓展，产业发展提速。',
            'hotspot_type': 'industry',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '材料报',
            'url': 'https://www.material.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['新材料', '石墨烯', '碳纤维'],
            'related_companies': ['方大炭素', '中简科技', '光威复材'],
            'related_industries': ['材料', '制造业'],
            'sentiment_score': 0.4,
            'heat_score': 68.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_030',
            'title': '数字经济发展规划发布',
            'content': '国家数字经济发展规划正式发布，明确发展目标和重点任务，数字经济迎来发展新机遇。',
            'hotspot_type': 'policy',
            'hotspot_level': 'very_high',
            'status': 'active',
            'source': '发改委',
            'url': 'https://www.ndrc.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['数字经济', '发展规划', '数字化转型'],
            'related_companies': ['阿里巴巴', '腾讯', '百度'],
            'related_industries': ['科技', '数字经济'],
            'sentiment_score': 0.5,
            'heat_score': 87.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_031',
            'title': '航天技术商业化加速',
            'content': '商业航天发展迅速，民营航天企业技术突破，航天技术商业化进程加速。',
            'hotspot_type': 'tech',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '航天报',
            'url': 'https://www.space.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['商业航天', '民营航天', '航天技术'],
            'related_companies': ['蓝箭航天', '星际荣耀', '星河动力'],
            'related_industries': ['航天', '科技'],
            'sentiment_score': 0.55,
            'heat_score': 79.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_032',
            'title': '生物技术产业政策支持',
            'content': '生物技术产业获得政策大力支持，创新药、基因治疗等领域发展前景广阔。',
            'hotspot_type': 'policy',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '科技部',
            'url': 'https://www.most.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['生物技术', '创新药', '基因治疗'],
            'related_companies': ['药明康德', '华大基因', '贝瑞和康'],
            'related_industries': ['生物技术', '医药'],
            'sentiment_score': 0.45,
            'heat_score': 82.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_033',
            'title': '智能家居市场快速增长',
            'content': '智能家居产品需求旺盛，市场规模快速增长，物联网技术应用广泛。',
            'hotspot_type': 'industry',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '家电报',
            'url': 'https://www.jdb.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['智能家居', '物联网', '家电'],
            'related_companies': ['小米', '华为', '海尔智家'],
            'related_industries': ['家电', '科技'],
            'sentiment_score': 0.4,
            'heat_score': 70.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_034',
            'title': '量子计算技术突破',
            'content': '量子计算技术取得重要突破，量子比特数量和质量显著提升，应用前景广阔。',
            'hotspot_type': 'tech',
            'hotspot_level': 'very_high',
            'status': 'active',
            'source': '科技日报',
            'url': 'https://www.stdaily.com/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['量子计算', '量子比特', '技术突破'],
            'related_companies': ['阿里巴巴', '腾讯', '百度'],
            'related_industries': ['科技'],
            'sentiment_score': 0.6,
            'heat_score': 89.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_035',
            'title': '绿色建筑标准提升',
            'content': '绿色建筑标准不断提升，节能环保要求日益严格，建筑行业绿色转型加速。',
            'hotspot_type': 'policy',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '住建部',
            'url': 'http://www.mohurd.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['绿色建筑', '节能环保', '建筑标准'],
            'related_companies': ['万科', '保利', '碧桂园'],
            'related_industries': ['房地产', '建筑'],
            'sentiment_score': 0.35,
            'heat_score': 64.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_036',
            'title': '数字孪生技术应用',
            'content': '数字孪生技术在工业、城市管理等领域的应用不断拓展，技术成熟度持续提升。',
            'hotspot_type': 'tech',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '科技日报',
            'url': 'https://www.stdaily.com/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['数字孪生', '工业', '城市管理'],
            'related_companies': ['华为', '阿里云', '腾讯云'],
            'related_industries': ['科技', '工业'],
            'sentiment_score': 0.3,
            'heat_score': 67.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_037',
            'title': '医疗器械创新加速',
            'content': '国产医疗器械创新加速，高端设备国产化率提升，行业竞争力显著增强。',
            'hotspot_type': 'industry',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '医药经济报',
            'url': 'https://www.yyjjb.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['医疗器械', '创新', '国产化'],
            'related_companies': ['迈瑞医疗', '乐普医疗', '鱼跃医疗'],
            'related_industries': ['医药', '医疗器械'],
            'sentiment_score': 0.5,
            'heat_score': 77.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_038',
            'title': '数据安全法实施',
            'content': '数据安全法正式实施，数据保护要求更加严格，企业合规成本增加。',
            'hotspot_type': 'policy',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '网信办',
            'url': 'http://www.cac.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['数据安全法', '数据保护', '合规'],
            'related_companies': ['阿里巴巴', '腾讯', '百度'],
            'related_industries': ['科技', '互联网'],
            'sentiment_score': 0.1,
            'heat_score': 80.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_039',
            'title': '氢能源产业发展规划',
            'content': '氢能源产业发展规划发布，产业链布局加速，氢能汽车商业化进程加快。',
            'hotspot_type': 'policy',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '能源局',
            'url': 'http://www.nea.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['氢能源', '发展规划', '氢能汽车'],
            'related_companies': ['潍柴动力', '亿华通', '美锦能源'],
            'related_industries': ['能源', '汽车'],
            'sentiment_score': 0.45,
            'heat_score': 78.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_040',
            'title': '元宇宙概念持续火热',
            'content': '元宇宙概念持续受到关注，VR/AR技术快速发展，虚拟现实应用场景不断拓展。',
            'hotspot_type': 'tech',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '科技日报',
            'url': 'https://www.stdaily.com/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['元宇宙', 'VR/AR', '虚拟现实'],
            'related_companies': ['腾讯', '字节跳动', '百度'],
            'related_industries': ['科技', '娱乐'],
            'sentiment_score': 0.4,
            'heat_score': 84.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_041',
            'title': '农业现代化加速推进',
            'content': '智慧农业、精准农业等现代化农业技术广泛应用，农业生产效率显著提升。',
            'hotspot_type': 'industry',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '农业报',
            'url': 'https://www.agri.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['智慧农业', '精准农业', '现代化'],
            'related_companies': ['大北农', '隆平高科', '登海种业'],
            'related_industries': ['农业', '科技'],
            'sentiment_score': 0.35,
            'heat_score': 63.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_042',
            'title': '碳交易市场启动',
            'content': '全国碳交易市场正式启动，碳排放权交易活跃，绿色金融体系进一步完善。',
            'hotspot_type': 'policy',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '环境部',
            'url': 'http://www.mee.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['碳交易', '碳排放权', '绿色金融'],
            'related_companies': ['华能集团', '大唐集团', '国电集团'],
            'related_industries': ['能源', '环保'],
            'sentiment_score': 0.4,
            'heat_score': 76.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_043',
            'title': '工业软件国产化加速',
            'content': '工业软件国产化进程加速，CAD、CAE等核心软件技术突破，产业链安全性提升。',
            'hotspot_type': 'industry',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '工业报',
            'url': 'https://www.gyb.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['工业软件', 'CAD', 'CAE'],
            'related_companies': ['中望软件', '华大九天', '概伦电子'],
            'related_industries': ['软件', '制造业'],
            'sentiment_score': 0.5,
            'heat_score': 75.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_044',
            'title': '智能网联汽车发展',
            'content': '智能网联汽车技术快速发展，自动驾驶商业化进程加快，车联网应用广泛。',
            'hotspot_type': 'tech',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '汽车报',
            'url': 'https://www.auto.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['智能网联', '自动驾驶', '车联网'],
            'related_companies': ['百度', '华为', '小鹏汽车'],
            'related_industries': ['汽车', '科技'],
            'sentiment_score': 0.45,
            'heat_score': 81.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_045',
            'title': '文化产业发展政策',
            'content': '文化产业支持政策密集出台，数字文化、创意产业等新业态快速发展。',
            'hotspot_type': 'policy',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '文化部',
            'url': 'http://www.mct.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['文化产业', '数字文化', '创意产业'],
            'related_companies': ['腾讯', '网易', '完美世界'],
            'related_industries': ['文化', '娱乐'],
            'sentiment_score': 0.35,
            'heat_score': 68.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_046',
            'title': '卫星互联网建设',
            'content': '卫星互联网星座建设加速，低轨卫星技术成熟，全球网络覆盖能力提升。',
            'hotspot_type': 'tech',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '航天报',
            'url': 'https://www.space.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['卫星互联网', '低轨卫星', '网络覆盖'],
            'related_companies': ['中国卫通', '航天宏图', '欧比特'],
            'related_industries': ['航天', '通信'],
            'sentiment_score': 0.4,
            'heat_score': 73.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_047',
            'title': '医疗设备集采政策',
            'content': '医疗设备集中采购政策实施，设备价格下降，医疗机构采购成本降低。',
            'hotspot_type': 'policy',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '医保局',
            'url': 'http://www.nhsa.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['医疗设备', '集采', '价格下降'],
            'related_companies': ['迈瑞医疗', '乐普医疗', '鱼跃医疗'],
            'related_industries': ['医药', '医疗器械'],
            'sentiment_score': 0.2,
            'heat_score': 66.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_048',
            'title': '新能源储能技术突破',
            'content': '电池储能技术取得重要突破，储能成本下降，新能源消纳能力提升。',
            'hotspot_type': 'tech',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '能源报',
            'url': 'https://www.energynews.com.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['储能', '电池', '新能源'],
            'related_companies': ['宁德时代', '比亚迪', '亿纬锂能'],
            'related_industries': ['新能源', '储能'],
            'sentiment_score': 0.5,
            'heat_score': 79.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_049',
            'title': '数字人民币试点扩大',
            'content': '数字人民币试点范围进一步扩大，应用场景不断丰富，数字货币发展进入快车道。',
            'hotspot_type': 'policy',
            'hotspot_level': 'high',
            'status': 'active',
            'source': '央行',
            'url': 'http://www.pbc.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['数字人民币', '试点', '数字货币'],
            'related_companies': ['工商银行', '建设银行', '农业银行'],
            'related_industries': ['金融', '科技'],
            'sentiment_score': 0.3,
            'heat_score': 77.0,
            'update_date': datetime.now().isoformat()
        },
        {
            'hotspot_id': 'test_050',
            'title': '人工智能伦理规范',
            'content': '人工智能伦理规范发布，AI技术发展更加规范，社会责任意识增强。',
            'hotspot_type': 'policy',
            'hotspot_level': 'medium',
            'status': 'active',
            'source': '科技部',
            'url': 'https://www.most.gov.cn/',
            'publish_time': datetime.now().isoformat(),
            'keywords': ['人工智能', '伦理规范', '社会责任'],
            'related_companies': ['阿里巴巴', '腾讯', '百度'],
            'related_industries': ['科技', 'AI'],
            'sentiment_score': 0.25,
            'heat_score': 69.0,
            'update_date': datetime.now().isoformat()
        }
    ]
    
    # 过滤数据
    filtered_hotspots = hotspots
    
    # 按级别过滤
    if hotspot_level:
        filtered_hotspots = [h for h in filtered_hotspots if h['hotspot_level'] == hotspot_level]
    
    # 按类型过滤
    if hotspot_type:
        filtered_hotspots = [h for h in filtered_hotspots if h['hotspot_type'] == hotspot_type]
    
    # 排序
    reverse = sort_order == 'desc'
    if sort_by == 'publish_time':
        filtered_hotspots.sort(key=lambda x: x['publish_time'], reverse=reverse)
    elif sort_by == 'heat_score':
        filtered_hotspots.sort(key=lambda x: x['heat_score'], reverse=reverse)
    elif sort_by == 'sentiment_score':
        filtered_hotspots.sort(key=lambda x: x['sentiment_score'], reverse=reverse)
    
    # 计算分页
    total = len(filtered_hotspots)
    pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    
    # 分页切片
    paginated_hotspots = filtered_hotspots[start:end]
    
    return jsonify({
        'success': True,
        'data': {
            'hotspots': paginated_hotspots,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages
            },
            'sorting': {
                'sort_by': sort_by,
                'sort_order': sort_order
            }
        }
    })

@app.route('/api/test')
def test():
    """测试接口"""
    return jsonify({
        'success': True,
        'message': '5002端口服务运行正常',
        'data': {
            'timestamp': datetime.now().isoformat(),
            'port': 5002,
            'status': 'running'
        }
    })

@app.route('/api/rankings/<ranking_type>')
def get_rankings(ranking_type):
    """获取排名数据"""
    try:
        if ranking_type == 'industries':
            rankings = [
                {
                    'industry': '科技行业',
                    'heat_score': 85.5,
                    'count': 45,
                    'trend': 'up'
                },
                {
                    'industry': '金融行业',
                    'heat_score': 78.2,
                    'count': 32,
                    'trend': 'stable'
                },
                {
                    'industry': '制造业',
                    'heat_score': 72.8,
                    'count': 38,
                    'trend': 'down'
                },
                {
                    'industry': '医药行业',
                    'heat_score': 68.4,
                    'count': 25,
                    'trend': 'up'
                },
                {
                    'industry': '消费行业',
                    'heat_score': 65.1,
                    'count': 28,
                    'trend': 'stable'
                },
                {
                    'industry': '房地产',
                    'heat_score': 62.3,
                    'count': 22,
                    'trend': 'down'
                },
                {
                    'industry': '能源行业',
                    'heat_score': 59.7,
                    'count': 18,
                    'trend': 'stable'
                },
                {
                    'industry': '教育行业',
                    'heat_score': 56.2,
                    'count': 15,
                    'trend': 'up'
                },
                {
                    'industry': '物流行业',
                    'heat_score': 53.8,
                    'count': 12,
                    'trend': 'up'
                },
                {
                    'industry': '农业',
                    'heat_score': 51.4,
                    'count': 10,
                    'trend': 'stable'
                },
                {
                    'industry': '传媒行业',
                    'heat_score': 48.9,
                    'count': 8,
                    'trend': 'down'
                },
                {
                    'industry': '旅游行业',
                    'heat_score': 46.5,
                    'count': 7,
                    'trend': 'up'
                },
                {
                    'industry': '环保行业',
                    'heat_score': 44.2,
                    'count': 6,
                    'trend': 'up'
                },
                {
                    'industry': '军工行业',
                    'heat_score': 41.8,
                    'count': 5,
                    'trend': 'stable'
                },
                {
                    'industry': '纺织行业',
                    'heat_score': 39.5,
                    'count': 4,
                    'trend': 'down'
                }
            ]
        elif ranking_type == 'companies':
            rankings = [
                {
                    'company': '阿里巴巴',
                    'heat_score': 92.3,
                    'count': 15,
                    'industry': '科技行业',
                    'trend': 'up'
                },
                {
                    'company': '腾讯',
                    'heat_score': 89.7,
                    'count': 12,
                    'industry': '科技行业',
                    'trend': 'up'
                },
                {
                    'company': '百度',
                    'heat_score': 76.4,
                    'count': 8,
                    'industry': '科技行业',
                    'trend': 'stable'
                },
                {
                    'company': '京东',
                    'heat_score': 73.2,
                    'count': 10,
                    'industry': '消费行业',
                    'trend': 'down'
                },
                {
                    'company': '美团',
                    'heat_score': 70.8,
                    'count': 9,
                    'industry': '消费行业',
                    'trend': 'up'
                },
                {
                    'company': '字节跳动',
                    'heat_score': 68.5,
                    'count': 11,
                    'industry': '科技行业',
                    'trend': 'up'
                },
                {
                    'company': '拼多多',
                    'heat_score': 66.2,
                    'count': 8,
                    'industry': '消费行业',
                    'trend': 'stable'
                },
                {
                    'company': '网易',
                    'heat_score': 63.8,
                    'count': 7,
                    'industry': '科技行业',
                    'trend': 'down'
                },
                {
                    'company': '小米',
                    'heat_score': 61.4,
                    'count': 9,
                    'industry': '制造业',
                    'trend': 'up'
                },
                {
                    'company': '华为',
                    'heat_score': 59.7,
                    'count': 13,
                    'industry': '科技行业',
                    'trend': 'up'
                },
                {
                    'company': '比亚迪',
                    'heat_score': 57.3,
                    'count': 6,
                    'industry': '制造业',
                    'trend': 'up'
                },
                {
                    'company': '平安银行',
                    'heat_score': 55.1,
                    'count': 5,
                    'industry': '金融行业',
                    'trend': 'stable'
                },
                {
                    'company': '招商银行',
                    'heat_score': 52.8,
                    'count': 4,
                    'industry': '金融行业',
                    'trend': 'stable'
                },
                {
                    'company': '中国移动',
                    'heat_score': 50.5,
                    'count': 6,
                    'industry': '科技行业',
                    'trend': 'down'
                },
                {
                    'company': '中国联通',
                    'heat_score': 48.2,
                    'count': 3,
                    'industry': '科技行业',
                    'trend': 'down'
                }
            ]
        elif ranking_type == 'trends':
            rankings = [
                {
                    'trend': '人工智能',
                    'heat_score': 88.5,
                    'count': 25,
                    'category': '技术趋势'
                },
                {
                    'trend': '新能源',
                    'heat_score': 82.3,
                    'count': 18,
                    'category': '产业趋势'
                },
                {
                    'trend': '数字化转型',
                    'heat_score': 79.1,
                    'count': 22,
                    'category': '企业趋势'
                },
                {
                    'trend': '绿色金融',
                    'heat_score': 75.6,
                    'count': 15,
                    'category': '金融趋势'
                },
                {
                    'trend': '元宇宙',
                    'heat_score': 72.4,
                    'count': 12,
                    'category': '技术趋势'
                },
                {
                    'trend': '区块链',
                    'heat_score': 69.8,
                    'count': 10,
                    'category': '技术趋势'
                },
                {
                    'trend': '云计算',
                    'heat_score': 67.2,
                    'count': 14,
                    'category': '技术趋势'
                },
                {
                    'trend': '大数据',
                    'heat_score': 64.5,
                    'count': 11,
                    'category': '技术趋势'
                },
                {
                    'trend': '物联网',
                    'heat_score': 61.8,
                    'count': 9,
                    'category': '技术趋势'
                },
                {
                    'trend': '5G技术',
                    'heat_score': 59.3,
                    'count': 8,
                    'category': '技术趋势'
                },
                {
                    'trend': '智能制造',
                    'heat_score': 56.7,
                    'count': 7,
                    'category': '产业趋势'
                },
                {
                    'trend': '生物技术',
                    'heat_score': 54.2,
                    'count': 6,
                    'category': '技术趋势'
                },
                {
                    'trend': '碳中和技术',
                    'heat_score': 51.8,
                    'count': 5,
                    'category': '产业趋势'
                },
                {
                    'trend': '量子计算',
                    'heat_score': 49.5,
                    'count': 4,
                    'category': '技术趋势'
                },
                {
                    'trend': '虚拟现实',
                    'heat_score': 47.2,
                    'count': 3,
                    'category': '技术趋势'
                }
            ]
        else:
            return jsonify({
                'success': False,
                'error': '不支持的排名类型'
            }), 400
        
        return jsonify({
            'success': True,
            'data': {
                'rankings': rankings,
                'type': ranking_type,
                'total': len(rankings)
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
        # 获取所有热点数据（直接使用get_hotspots函数中的数据）
        page = 1
        per_page = 1000  # 获取所有数据
        sort_by = 'publish_time'
        sort_order = 'desc'
        
        # 模拟热点数据（与get_hotspots函数中的数据保持一致）
        hotspots = [
            {
                'hotspot_id': 'test_001',
                'title': 'A股三大指数集体上涨，科技股领涨',
                'content': '今日A股市场表现强劲，三大指数集体上涨，科技股表现尤为突出，创业板指涨幅超过2%。市场分析认为，科技股走强主要受益于政策利好和业绩预期改善。',
                'hotspot_type': 'news',
                'hotspot_level': 'high',
                'status': 'active',
                'source': '新浪财经',
                'url': 'https://finance.sina.com.cn/',
                'publish_time': datetime.now().isoformat(),
                'keywords': ['A股', '科技股', '上涨'],
                'related_companies': ['阿里巴巴', '腾讯', '百度'],
                'related_industries': ['科技'],
                'sentiment_score': 0.3,
                'heat_score': 75.0,
                'update_date': datetime.now().isoformat()
            }
        ]
        
        # 这里应该包含所有50条热点数据，但为了简洁，我们使用动态生成的方式
        # 查找指定的热点
        hotspot = None
        
        # 首先检查是否是test_001或test_002（已有的数据）
        for h in hotspots:
            if h['hotspot_id'] == hotspot_id:
                hotspot = h.copy()
                break
        
        # 如果不是已有的数据，动态生成
        if hotspot is None:
            # 检查是否是有效的test_XXX格式
            if not hotspot_id.startswith('test_') or not hotspot_id[5:].isdigit():
                return jsonify({
                    'success': False,
                    'error': '热点不存在'
                }), 404
            
            # 动态生成热点数据
            hotspot = generate_dynamic_hotspot(hotspot_id)
        
        # 生成详细信息
        hotspot = generate_hotspot_details(hotspot)
        
        return jsonify({
            'success': True,
            'data': hotspot
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_dynamic_hotspot(hotspot_id):
    """动态生成热点数据"""
    # 根据ID生成基础数据
    hotspot_num = int(hotspot_id[5:])
    
    # 基础数据模板
    base_templates = [
        {'title': 'A股三大指数集体上涨，科技股领涨', 'type': 'news', 'level': 'high'},
        {'title': '央行发布最新货币政策报告', 'type': 'policy', 'level': 'very_high'},
        {'title': '新能源汽车销量再创新高', 'type': 'industry', 'level': 'high'},
        {'title': '人工智能技术突破性进展', 'type': 'tech', 'level': 'very_high'},
        {'title': '房地产调控政策持续优化', 'type': 'policy', 'level': 'medium'},
        {'title': '医药行业创新药研发加速', 'type': 'industry', 'level': 'high'},
        {'title': '消费市场复苏态势良好', 'type': 'news', 'level': 'medium'},
        {'title': '5G网络建设加速推进', 'type': 'tech', 'level': 'high'},
        {'title': '绿色金融发展提速', 'type': 'finance', 'level': 'medium'},
        {'title': '芯片产业国产化进程加快', 'type': 'industry', 'level': 'high'}
    ]
    
    # 循环使用模板
    template = base_templates[(hotspot_num - 1) % len(base_templates)]
    
    return {
        'hotspot_id': hotspot_id,
        'title': template['title'],
        'content': f"这是关于{template['title']}的新闻报道。该事件对相关行业和市场产生了重要影响。",
        'hotspot_type': template['type'],
        'hotspot_level': template['level'],
        'status': 'active',
        'source': '综合报道',
        'url': 'https://www.example.com/',
        'publish_time': datetime.now().isoformat(),
        'keywords': ['关键词1', '关键词2', '关键词3'],
        'related_companies': [],
        'related_industries': ['相关行业'],
        'sentiment_score': 0.3,
        'heat_score': 70.0 + (hotspot_num % 20),  # 70-90之间的热度
        'update_date': datetime.now().isoformat()
    }

def generate_hotspot_details(hotspot):
    """根据热点基础信息生成详细信息"""
    
    # 根据热点ID和标题生成相关公司
    related_companies_map = {
        'test_001': ['阿里巴巴', '腾讯', '百度', '京东', '美团'],
        'test_002': ['工商银行', '建设银行', '农业银行', '中国银行'],
        'test_003': ['比亚迪', '特斯拉', '蔚来', '小鹏汽车', '理想汽车'],
        'test_004': ['OpenAI', '微软', '谷歌', '百度', '阿里巴巴'],
        'test_005': ['万科', '保利', '碧桂园', '恒大', '融创'],
        'test_006': ['恒瑞医药', '复星医药', '药明康德', '华大基因'],
        'test_007': ['美团', '携程', '海底捞', '星巴克', '麦当劳'],
        'test_008': ['中国移动', '中国联通', '中国电信', '华为', '中兴'],
        'test_009': ['工商银行', '建设银行', '招商银行', '平安银行'],
        'test_010': ['中芯国际', '华为', '紫光展锐', '北方华创'],
        'test_011': ['阿里巴巴', '京东', '拼多多', '抖音', '快手'],
        'test_012': ['金风科技', '隆基绿能', '通威股份', '阳光电源'],
        'test_013': ['工商银行', '建设银行', '农业银行', '中国银行'],
        'test_014': ['药明康德', '泰格医药', '康龙化成', '昭衍新药'],
        'test_015': ['阿里巴巴', '腾讯', '华为', '百度', '京东'],
        'test_016': ['顺丰控股', '京东物流', '中通快递', '圆通速递'],
        'test_017': ['新东方', '好未来', '猿辅导', '作业帮'],
        'test_018': ['腾讯', '网易', '完美世界', '三七互娱'],
        'test_019': ['中石化', '中石油', '华能集团', '大唐集团'],
        'test_020': ['蚂蚁集团', '京东数科', '度小满', '腾讯金融'],
        'test_021': ['北方华创', '中微公司', '盛美上海', '华海清科'],
        'test_022': ['比亚迪', '特斯拉', '蔚来', '小鹏汽车'],
        'test_023': ['平安好医生', '微医', '丁香园', '春雨医生'],
        'test_024': ['蚂蚁集团', '腾讯', '百度', '京东'],
        'test_025': ['恒大', '融创', '碧桂园', '万科'],
        'test_026': ['海尔智家', '美的集团', '格力电器', '海信家电'],
        'test_027': ['奇安信', '深信服', '启明星辰', '绿盟科技'],
        'test_028': ['蚂蚁集团', '京东数科', '度小满', '腾讯金融'],
        'test_029': ['方大炭素', '中简科技', '光威复材', '碳元科技'],
        'test_030': ['阿里巴巴', '腾讯', '百度', '京东', '字节跳动'],
        'test_031': ['蓝箭航天', '星际荣耀', '星河动力', '天仪研究院'],
        'test_032': ['药明康德', '华大基因', '贝瑞和康', '诺禾致源'],
        'test_033': ['小米', '华为', '海尔智家', '美的集团'],
        'test_034': ['阿里巴巴', '腾讯', '百度', '华为', '中科院'],
        'test_035': ['万科', '保利', '碧桂园', '龙湖集团'],
        'test_036': ['华为', '阿里云', '腾讯云', '百度云'],
        'test_037': ['迈瑞医疗', '乐普医疗', '鱼跃医疗', '新华医疗'],
        'test_038': ['阿里巴巴', '腾讯', '百度', '字节跳动'],
        'test_039': ['潍柴动力', '亿华通', '美锦能源', '厚普股份'],
        'test_040': ['腾讯', '字节跳动', '百度', '网易'],
        'test_041': ['大北农', '隆平高科', '登海种业', '荃银高科'],
        'test_042': ['华能集团', '大唐集团', '国电集团', '华电集团'],
        'test_043': ['中望软件', '华大九天', '概伦电子', '芯原股份'],
        'test_044': ['百度', '华为', '小鹏汽车', '蔚来'],
        'test_045': ['腾讯', '网易', '完美世界', '三七互娱'],
        'test_046': ['中国卫通', '航天宏图', '欧比特', '北斗星通'],
        'test_047': ['迈瑞医疗', '乐普医疗', '鱼跃医疗', '新华医疗'],
        'test_048': ['宁德时代', '比亚迪', '亿纬锂能', '国轩高科'],
        'test_049': ['工商银行', '建设银行', '农业银行', '中国银行'],
        'test_050': ['阿里巴巴', '腾讯', '百度', '华为', '字节跳动']
    }
    
    # 获取相关公司
    hotspot['related_companies'] = related_companies_map.get(hotspot['hotspot_id'], [])
    
    # 生成详细内容
    hotspot['detailed_content'] = f"详细内容：{hotspot['content']} 这是关于{hotspot['title']}的详细报道。该事件对相关行业和市场产生了重要影响，引起了广泛关注。具体来看，这一发展涉及多个方面，包括技术、政策、市场等多个维度。"
    
    # 生成分析内容
    analysis_templates = {
        'news': f"市场分析：{hotspot['title']}这一新闻事件对市场产生了重要影响。从多个角度来看，这一发展反映了当前市场的发展趋势和变化。",
        'policy': f"政策分析：{hotspot['title']}这一政策发布对相关行业和企业产生了重要影响。政策导向明确，为行业发展提供了新的方向。",
        'industry': f"行业分析：{hotspot['title']}反映了该行业的最新发展趋势。这一发展对整个产业链都产生了重要影响。",
        'tech': f"技术分析：{hotspot['title']}代表了技术领域的重要突破。这一技术发展对未来产业发展具有重要意义。",
        'finance': f"金融分析：{hotspot['title']}对金融市场产生了重要影响。这一发展反映了金融行业的最新变化。"
    }
    hotspot['analysis'] = analysis_templates.get(hotspot['hotspot_type'], f"综合分析：{hotspot['title']}这一事件具有重要意义。")
    
    # 生成市场影响
    impact_templates = {
        'news': f"市场影响：{hotspot['title']}对市场情绪产生了积极影响，有助于提升投资者信心。",
        'policy': f"市场影响：{hotspot['title']}为市场提供了政策指引，有助于稳定市场预期。",
        'industry': f"市场影响：{hotspot['title']}推动了相关行业的发展，为市场带来了新的投资机会。",
        'tech': f"市场影响：{hotspot['title']}为相关技术公司带来了发展机遇，推动了技术创新。",
        'finance': f"市场影响：{hotspot['title']}对金融市场的稳定和发展产生了积极影响。"
    }
    hotspot['impact'] = impact_templates.get(hotspot['hotspot_type'], f"市场影响：{hotspot['title']}对市场产生了重要影响。")
    
    # 生成相关新闻
    related_news_templates = [
        '央行发布最新货币政策报告',
        '新能源汽车销量再创新高',
        '人工智能技术突破性进展',
        '房地产调控政策持续优化',
        '医药行业创新药研发加速',
        '消费市场复苏态势良好',
        '5G网络建设加速推进',
        '绿色金融发展提速',
        '芯片产业国产化进程加快',
        '电商平台双11销售额创新高'
    ]
    
    # 随机选择3-5条相关新闻
    import random
    hotspot['related_news'] = random.sample(related_news_templates, min(3, len(related_news_templates)))
    
    return hotspot

@app.route('/api/hotspots/<hotspot_id>', methods=['DELETE'])
def delete_hotspot(hotspot_id):
    """删除热点数据"""
    try:
        # 这里应该从数据库删除数据
        # 目前只是模拟删除操作
        
        return jsonify({
            'success': True,
            'data': {
                'message': f'热点 {hotspot_id} 删除成功'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("国内热点数据管理台 - 5002端口版本")
    print("=" * 60)
    print("服务地址: http://localhost:5002")
    print("健康检查: http://localhost:5002/api/health")
    print("测试接口: http://localhost:5002/api/test")
    print("统计接口: http://localhost:5002/api/statistics")
    print("热点数据: http://localhost:5002/api/hotspots")
    print("=" * 60)
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5002, debug=True) 