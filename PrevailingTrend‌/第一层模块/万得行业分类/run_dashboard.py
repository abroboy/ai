"""
万得行业分类管理台启动脚本
按照最新规范：127.0.0.1:5001只做万得行业分类的数据，不涉及模块
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
import time

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='万得行业分类管理台')
    parser.add_argument('--host', default='127.0.0.1', help='服务主机地址')
    parser.add_argument('--port', type=int, default=5001, help='服务端口')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    parser.add_argument('--init-db', action='store_true', help='初始化数据库')
    
    args = parser.parse_args()
    
    try:
        # 检查templates目录
        templates_dir = Path(__file__).parent / 'templates'
        if not templates_dir.exists():
            print(f"创建templates目录: {templates_dir}")
            templates_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查dashboard.html是否存在
        dashboard_file = templates_dir / 'dashboard.html'
        if not dashboard_file.exists():
            print("错误: dashboard.html模板文件不存在")
            print("请确保templates/dashboard.html文件存在")
            return
        
        # 启动管理台
        print(f"启动万得行业分类管理台...")
        print(f"访问地址: http://{args.host}:{args.port}")
        print("按 Ctrl+C 停止服务")
        
        # 直接启动Flask应用
        from flask import Flask, render_template, jsonify, request
        from flask_cors import CORS
        import pymysql
        
        app = Flask(__name__, static_folder='static')
        CORS(app)
        
        # 数据库配置
        DB_CONFIG = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'rr1234RR',
            'database': 'pt',
            'charset': 'utf8mb4'
        }
        
        # 缓存机制
        cache = {
            'stats': None,
            'stats_time': 0,
            'industries': None,
            'industries_time': 0
        }
        CACHE_DURATION = 30  # 缓存30秒
        
        def get_db_connection():
            """获取数据库连接"""
            try:
                return pymysql.connect(**DB_CONFIG)
            except Exception as e:
                print(f"数据库连接失败: {e}")
                return None
        
        def get_cached_stats():
            """获取缓存的统计信息"""
            current_time = time.time()
            if (cache['stats'] is None or 
                current_time - cache['stats_time'] > CACHE_DURATION):
                
                try:
                    connection = get_db_connection()
                    if not connection:
                        return None
                    
                    cursor = connection.cursor(pymysql.cursors.DictCursor)
                    
                    # 一次性查询所有统计信息
                    cursor.execute("""
                        SELECT 
                            (SELECT COUNT(*) FROM wind_industry_classification) as total_industries,
                            (SELECT COUNT(*) FROM stock_industry_mapping) as total_stocks,
                            (SELECT COUNT(*) FROM wind_industry_classification WHERE level = 1) as level_1_count,
                            (SELECT COUNT(*) FROM wind_industry_classification WHERE level = 2) as level_2_count
                    """)
                    
                    stats = cursor.fetchone()
                    cursor.close()
                    connection.close()
                    
                    cache['stats'] = stats
                    cache['stats_time'] = current_time
                    
                except Exception as e:
                    print(f"获取统计信息失败: {e}")
                    return None
            
            return cache['stats']
        
        @app.route('/')
        def index():
            """主页 - 万得行业分类数据展示"""
            return render_template('dashboard.html')
        
        @app.route('/api/stats')
        def get_stats():
            """获取统计数据"""
            try:
                stats = get_cached_stats()
                
                if stats:
                    return jsonify({
                        'success': True,
                        'data': {
                            'total_industries': stats['total_industries'],
                            'total_stocks': stats['total_stocks'],
                            'level_1_count': stats['level_1_count'],
                            'level_2_count': stats['level_2_count']
                        }
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': '数据库连接失败',
                        'data': {
                            'total_industries': 0,
                            'total_stocks': 0,
                            'level_1_count': 0,
                            'level_2_count': 0
                        }
                    })
                
            except Exception as e:
                print(f"获取统计信息失败: {e}")
                return jsonify({
                    'success': False,
                    'message': str(e),
                    'data': {
                        'total_industries': 0,
                        'total_stocks': 0,
                        'level_1_count': 0,
                        'level_2_count': 0
                    }
                })
        
        @app.route('/api/industries')
        def get_industries():
            """获取行业列表 - 支持分页、搜索、筛选"""
            try:
                page = request.args.get('page', 1, type=int)
                page_size = request.args.get('page_size', 10, type=int)
                level = request.args.get('level', type=int)
                keyword = request.args.get('keyword', '')
                
                connection = get_db_connection()
                if not connection:
                    return jsonify({
                        'success': False,
                        'message': '数据库连接失败',
                        'data': {'industries': [], 'total': 0, 'page': page, 'page_size': page_size}
                    })
                
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                
                # 构建查询条件
                where_conditions = []
                params = []
                
                if level and level > 0:
                    where_conditions.append("level = %s")
                    params.append(level)
                
                if keyword:
                    where_conditions.append("industry_name LIKE %s")
                    params.append(f'%{keyword}%')
                
                where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
                
                # 获取总数
                count_sql = f"SELECT COUNT(*) as count FROM wind_industry_classification{where_clause}"
                cursor.execute(count_sql, params)
                total = cursor.fetchone()['count']
                
                # 获取分页数据
                offset = (page - 1) * page_size
                sql = f"""
                    SELECT * FROM wind_industry_classification{where_clause}
                    ORDER BY level, industry_code
                    LIMIT %s OFFSET %s
                """
                cursor.execute(sql, params + [page_size, offset])
                industries = cursor.fetchall()
                
                cursor.close()
                connection.close()
                
                return jsonify({
                    'success': True,
                    'data': {
                        'industries': industries,
                        'total': total,
                        'page': page,
                        'page_size': page_size,
                        'total_pages': (total + page_size - 1) // page_size
                    }
                })
                
            except Exception as e:
                print(f"获取行业列表失败: {e}")
                return jsonify({
                    'success': False,
                    'message': str(e),
                    'data': {'industries': [], 'total': 0, 'page': page, 'page_size': page_size}
                })
        
        @app.route('/api/industries/<industry_code>')
        def get_industry_detail(industry_code):
            """获取行业详情"""
            try:
                connection = get_db_connection()
                if not connection:
                    return jsonify({
                        'success': False,
                        'message': '数据库连接失败'
                    })
                
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                
                # 获取行业信息
                cursor.execute("SELECT * FROM wind_industry_classification WHERE industry_code = %s", (industry_code,))
                industry = cursor.fetchone()
                
                if not industry:
                    cursor.close()
                    connection.close()
                    return jsonify({'success': False, 'message': '行业不存在'})
                
                # 获取该行业下的股票
                cursor.execute("SELECT * FROM stock_industry_mapping WHERE industry_code = %s", (industry_code,))
                stocks = cursor.fetchall()
                
                cursor.close()
                connection.close()
                
                return jsonify({
                    'success': True,
                    'data': {
                        'industry': industry,
                        'stocks': stocks
                    }
                })
                
            except Exception as e:
                print(f"获取行业详情失败: {e}")
                return jsonify({'success': False, 'message': str(e)})
        
        @app.route('/api/stocks/stats')
        def get_stocks_stats():
            """获取股票统计数据"""
            try:
                connection = get_db_connection()
                if not connection:
                    return jsonify({
                        'success': False,
                        'message': '数据库连接失败',
                        'data': {
                            'total_mapped': 0,
                            'unmapped': 0,
                            'sync_status': '未连接',
                            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    })
                
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                
                # 获取股票统计信息
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_stocks,
                        COUNT(CASE WHEN industry_code IS NOT NULL AND industry_code != '' THEN 1 END) as mapped_stocks,
                        COUNT(CASE WHEN industry_code IS NULL OR industry_code = '' THEN 1 END) as unmapped_stocks
                    FROM stock_industry_mapping
                """)
                
                stats = cursor.fetchone()
                cursor.close()
                connection.close()
                
                return jsonify({
                    'success': True,
                    'data': {
                        'total_mapped': stats['mapped_stocks'] or 0,
                        'unmapped': stats['unmapped_stocks'] or 0,
                        'sync_status': '已同步',
                        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                })
                
            except Exception as e:
                print(f"获取股票统计数据失败: {e}")
                return jsonify({
                    'success': False,
                    'message': str(e),
                    'data': {
                        'total_mapped': 0,
                        'unmapped': 0,
                        'sync_status': '错误',
                        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                })
        
        @app.route('/api/stocks')
        def get_stocks_list():
            """获取股票列表"""
            try:
                page = int(request.args.get('page', 1))
                page_size = int(request.args.get('page_size', 20))
                filter_type = request.args.get('filter', 'all')
                keyword = request.args.get('keyword', '')
                
                connection = get_db_connection()
                if not connection:
                    return jsonify({
                        'success': False,
                        'message': '数据库连接失败',
                        'data': {'stocks': [], 'total': 0, 'page': page, 'page_size': page_size}
                    })
                
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                
                # 构建查询条件
                where_conditions = []
                params = []
                
                # 根据股票代码判断市场类型
                if filter_type == 'a':
                    where_conditions.append("(stock_code LIKE '0%' OR stock_code LIKE '3%' OR stock_code LIKE '6%')")
                elif filter_type == 'hk':
                    where_conditions.append("stock_code LIKE '%HK%' OR LENGTH(stock_code) = 5")
                elif filter_type == 'mapped':
                    where_conditions.append("industry_code IS NOT NULL AND industry_code != ''")
                elif filter_type == 'unmapped':
                    where_conditions.append("(industry_code IS NULL OR industry_code = '')")
                
                if keyword:
                    where_conditions.append("(stock_code LIKE %s OR stock_name LIKE %s)")
                    params.extend([f'%{keyword}%', f'%{keyword}%'])
                
                where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
                
                # 获取总数
                count_sql = f"SELECT COUNT(*) as total FROM stock_industry_mapping{where_clause}"
                cursor.execute(count_sql, params)
                total = cursor.fetchone()['total']
                
                # 获取分页数据
                offset = (page - 1) * page_size
                sql = f"""
                    SELECT 
                        stock_code,
                        stock_name,
                        industry_code,
                        industry_name,
                        mapping_status,
                        confidence,
                        created_at,
                        updated_at
                    FROM stock_industry_mapping{where_clause}
                    ORDER BY stock_code
                    LIMIT %s OFFSET %s
                """
                cursor.execute(sql, params + [page_size, offset])
                stocks = cursor.fetchall()
                
                # 处理返回数据，添加市场类型判断
                for stock in stocks:
                    stock_code = stock['stock_code']
                    # 根据股票代码判断市场类型
                    if stock_code.startswith(('0', '3', '6')) and len(stock_code) == 6:
                        stock['market'] = 'A股'
                    elif 'HK' in stock_code or len(stock_code) == 5:
                        stock['market'] = '港股通'
                    else:
                        stock['market'] = 'A股'  # 默认为A股
                    
                    # 判断映射状态
                    stock['mapped'] = bool(stock.get('industry_code'))
                
                cursor.close()
                connection.close()
                
                return jsonify({
                    'success': True,
                    'data': {
                        'stocks': stocks,
                        'total': total,
                        'page': page,
                        'page_size': page_size,
                        'total_pages': (total + page_size - 1) // page_size
                    }
                })
                
            except Exception as e:
                print(f"获取股票列表失败: {e}")
                return jsonify({
                    'success': False,
                    'message': str(e),
                    'data': {'stocks': [], 'total': 0, 'page': page, 'page_size': page_size}
                })
        
        @app.route('/api/health')
        def health_check():
            """健康检查接口"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'service': '万得行业分类管理台',
                'cache_info': {
                    'stats_cached': cache['stats'] is not None,
                    'industries_cached': cache['industries'] is not None
                }
            })
        
        # 启动应用
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n管理台已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 