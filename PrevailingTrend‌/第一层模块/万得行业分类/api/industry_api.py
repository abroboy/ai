"""
行业相关API接口
提供行业分类的RESTful API
"""

from flask import Flask, request, jsonify
from typing import Dict, Any, List
import json

from ..core.simple_classifier import SimpleIndustryClassifier
from ..utils.logger import logger


class IndustryAPI:
    """行业API类"""
    
    def __init__(self):
        self.classifier = SimpleIndustryClassifier()
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        """设置路由"""
        
        @self.app.route('/api/industries', methods=['GET'])
        def get_industries():
            """获取行业列表"""
            try:
                level = request.args.get('level', type=int)
                if level:
                    industries = self.classifier.get_industries_by_level(level)
                else:
                    industries = self.classifier.get_industries_by_level(1)
                
                result = {
                    'success': True,
                    'data': [industry.to_dict() for industry in industries],
                    'count': len(industries)
                }
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"获取行业列表失败: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/industries/<industry_code>', methods=['GET'])
        def get_industry(industry_code):
            """获取行业详情"""
            try:
                industry = self.classifier.get_industry_by_code(industry_code)
                if industry:
                    result = {
                        'success': True,
                        'data': industry.to_dict()
                    }
                    return jsonify(result)
                else:
                    return jsonify({
                        'success': False,
                        'error': f'行业代码 {industry_code} 不存在'
                    }), 404
                    
            except Exception as e:
                logger.error(f"获取行业详情失败: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/industries/search', methods=['GET'])
        def search_industries():
            """搜索行业"""
            try:
                keyword = request.args.get('keyword', '')
                if not keyword:
                    return jsonify({
                        'success': False,
                        'error': '搜索关键词不能为空'
                    }), 400
                
                industries = self.classifier.search_industries(keyword)
                result = {
                    'success': True,
                    'data': [industry.to_dict() for industry in industries],
                    'count': len(industries),
                    'keyword': keyword
                }
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"搜索行业失败: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/industries/statistics', methods=['GET'])
        def get_statistics():
            """获取统计信息"""
            try:
                stats = self.classifier.get_industry_statistics()
                result = {
                    'success': True,
                    'data': stats
                }
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"获取统计信息失败: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/industries/update', methods=['POST'])
        def update_industries():
            """更新行业数据"""
            try:
                result = self.classifier.run_full_update()
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"更新行业数据失败: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """运行API服务"""
        logger.info(f"启动行业API服务: {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


# 创建API实例
industry_api = IndustryAPI() 