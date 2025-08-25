"""
API服务器启动文件
提供RESTful API服务
"""

import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.industry_api import industry_api
from api.stock_api import stock_api
from utils.logger import logger


def start_industry_api():
    """启动行业API服务"""
    logger.info("启动行业API服务...")
    industry_api.run(host='0.0.0.0', port=5000, debug=False)


def start_stock_api():
    """启动股票API服务"""
    logger.info("启动股票API服务...")
    stock_api.run(host='0.0.0.0', port=5001, debug=False)


def start_combined_api():
    """启动组合API服务"""
    from flask import Flask, Blueprint
    
    app = Flask(__name__)
    
    # 注册行业API蓝图
    industry_blueprint = Blueprint('industry', __name__, url_prefix='/industry')
    industry_blueprint.add_url_rule('/api/industries', 'get_industries', 
                                   industry_api.app.view_functions['get_industries'])
    industry_blueprint.add_url_rule('/api/industries/<industry_code>', 'get_industry',
                                   industry_api.app.view_functions['get_industry'])
    industry_blueprint.add_url_rule('/api/industries/search', 'search_industries',
                                   industry_api.app.view_functions['search_industries'])
    industry_blueprint.add_url_rule('/api/industries/statistics', 'get_statistics',
                                   industry_api.app.view_functions['get_statistics'])
    industry_blueprint.add_url_rule('/api/industries/update', 'update_industries',
                                   industry_api.app.view_functions['update_industries'])
    
    # 注册股票API蓝图
    stock_blueprint = Blueprint('stock', __name__, url_prefix='/stock')
    stock_blueprint.add_url_rule('/api/stocks/industry/<industry_code>', 'get_stocks_by_industry',
                                stock_api.app.view_functions['get_stocks_by_industry'])
    stock_blueprint.add_url_rule('/api/stocks/<stock_code>', 'get_stock_industry',
                                stock_api.app.view_functions['get_stock_industry'])
    stock_blueprint.add_url_rule('/api/stocks/search', 'search_stocks',
                                stock_api.app.view_functions['search_stocks'])
    stock_blueprint.add_url_rule('/api/stocks/statistics', 'get_stock_statistics',
                                stock_api.app.view_functions['get_stock_statistics'])
    
    app.register_blueprint(industry_blueprint)
    app.register_blueprint(stock_blueprint)
    
    @app.route('/')
    def index():
        """API首页"""
        return {
            'message': '万得行业分类API服务',
            'version': '1.0.0',
            'endpoints': {
                'industry': '/industry/api/industries',
                'stock': '/stock/api/stocks'
            }
        }
    
    @app.route('/health')
    def health():
        """健康检查"""
        return {'status': 'healthy'}
    
    logger.info("启动组合API服务...")
    app.run(host='0.0.0.0', port=5000, debug=False)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='万得行业分类API服务器')
    parser.add_argument('--service', choices=['industry', 'stock', 'combined'], 
                       default='combined', help='启动的服务类型')
    parser.add_argument('--host', default='0.0.0.0', help='服务主机地址')
    parser.add_argument('--port', type=int, default=5000, help='服务端口')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    try:
        if args.service == 'industry':
            start_industry_api()
        elif args.service == 'stock':
            start_stock_api()
        elif args.service == 'combined':
            start_combined_api()
        
    except KeyboardInterrupt:
        logger.info("API服务已停止")
    except Exception as e:
        logger.error(f"API服务启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 