"""
股票相关API接口
提供股票行业映射的RESTful API
"""

from flask import Flask, request, jsonify
from typing import Dict, Any, List
import json

from ..core.simple_classifier import SimpleIndustryClassifier
from ..utils.logger import logger


class StockAPI:
    """股票API类"""
    
    def __init__(self):
        self.classifier = SimpleIndustryClassifier()
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        """设置路由"""
        
        @self.app.route('/api/stocks/industry/<industry_code>', methods=['GET'])
        def get_stocks_by_industry(industry_code):
            """获取行业下的股票列表"""
            try:
                from ..utils.database import db_manager
                
                sql = """
                SELECT * FROM stock_industry_mapping 
                WHERE industry_code = %s AND status = 'active'
                ORDER BY confidence DESC
                """
                results = db_manager.execute_query(sql, (industry_code,))
                
                result = {
                    'success': True,
                    'data': results,
                    'count': len(results),
                    'industry_code': industry_code
                }
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"获取行业股票列表失败: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/stocks/<stock_code>', methods=['GET'])
        def get_stock_industry(stock_code):
            """获取股票的行业信息"""
            try:
                from ..utils.database import db_manager
                
                sql = """
                SELECT * FROM stock_industry_mapping 
                WHERE stock_code = %s AND status = 'active'
                ORDER BY confidence DESC
                LIMIT 1
                """
                results = db_manager.execute_query(sql, (stock_code,))
                
                if results:
                    result = {
                        'success': True,
                        'data': results[0]
                    }
                    return jsonify(result)
                else:
                    return jsonify({
                        'success': False,
                        'error': f'股票代码 {stock_code} 未找到行业映射'
                    }), 404
                    
            except Exception as e:
                logger.error(f"获取股票行业信息失败: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/stocks/search', methods=['GET'])
        def search_stocks():
            """搜索股票"""
            try:
                keyword = request.args.get('keyword', '')
                if not keyword:
                    return jsonify({
                        'success': False,
                        'error': '搜索关键词不能为空'
                    }), 400
                
                from ..utils.database import db_manager
                
                sql = """
                SELECT * FROM stock_industry_mapping 
                WHERE (stock_code LIKE %s OR stock_name LIKE %s) 
                AND status = 'active'
                ORDER BY confidence DESC
                LIMIT 100
                """
                search_pattern = f"%{keyword}%"
                results = db_manager.execute_query(sql, (search_pattern, search_pattern))
                
                result = {
                    'success': True,
                    'data': results,
                    'count': len(results),
                    'keyword': keyword
                }
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"搜索股票失败: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/stocks/statistics', methods=['GET'])
        def get_stock_statistics():
            """获取股票映射统计信息"""
            try:
                from ..utils.database import db_manager
                
                # 总股票数量
                sql = "SELECT COUNT(*) as count FROM stock_industry_mapping WHERE status = 'active'"
                result = db_manager.execute_query(sql)
                total_stocks = result[0]['count']
                
                # 高置信度股票数量
                sql = "SELECT COUNT(*) as count FROM stock_industry_mapping WHERE confidence >= 0.8 AND status = 'active'"
                result = db_manager.execute_query(sql)
                high_confidence_stocks = result[0]['count']
                
                # 按行业统计
                sql = """
                SELECT industry_code, industry_name, COUNT(*) as count 
                FROM stock_industry_mapping 
                WHERE status = 'active' 
                GROUP BY industry_code, industry_name 
                ORDER BY count DESC 
                LIMIT 10
                """
                industry_stats = db_manager.execute_query(sql)
                
                stats = {
                    'total_stocks': total_stocks,
                    'high_confidence_stocks': high_confidence_stocks,
                    'confidence_ratio': high_confidence_stocks / total_stocks if total_stocks > 0 else 0,
                    'top_industries': industry_stats
                }
                
                result = {
                    'success': True,
                    'data': stats
                }
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"获取股票统计信息失败: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    
    def run(self, host='0.0.0.0', port=5001, debug=False):
        """运行API服务"""
        logger.info(f"启动股票API服务: {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


# 创建API实例
stock_api = StockAPI() 