"""
万得行业分类模块管理台
提供Web界面来管理和查看行业分类数据
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
import sys
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.industry_classifier import IndustryClassifier
from utils.logger import logger
from utils.database import db_manager

app = Flask(__name__)
CORS(app)

# 配置
app.config['SECRET_KEY'] = 'wind_industry_dashboard_2025'
app.config['DEBUG'] = True

# 初始化分类器
classifier = IndustryClassifier()

@app.route('/')
def index():
    """管理台首页"""
    return render_template('dashboard.html')

@app.route('/api/dashboard/stats')
def get_dashboard_stats():
    """获取仪表板统计信息"""
    try:
        stats = classifier.get_industry_statistics()
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/industries')
def get_industries():
    """获取行业列表"""
    try:
        level = request.args.get('level', type=int)
        keyword = request.args.get('keyword', '')
        
        if level:
            industries = classifier.get_industries_by_level(level)
        elif keyword:
            industries = classifier.search_industries(keyword)
        else:
            industries = classifier.get_all_industries()
        
        return jsonify({'success': True, 'data': industries})
    except Exception as e:
        logger.error(f"获取行业列表失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/industries/<industry_code>')
def get_industry_detail(industry_code):
    """获取行业详情"""
    try:
        industry = classifier.get_industry_by_code(industry_code)
        if not industry:
            return jsonify({'success': False, 'message': '行业不存在'})
        
        stocks = classifier.get_stocks_by_industry(industry_code)
        
        return jsonify({
            'success': True,
            'data': {
                'industry': industry,
                'stocks': stocks
            }
        })
    except Exception as e:
        logger.error(f"获取行业详情失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/data/update', methods=['POST'])
def update_data():
    """更新数据"""
    try:
        result = classifier.run_full_update()
        return jsonify({
            'success': result['success'],
            'message': result.get('message', ''),
            'data': result
        })
    except Exception as e:
        logger.error(f"数据更新失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    logger.info("启动万得行业分类管理台...")
    app.run(host='0.0.0.0', port=5001, debug=True) 