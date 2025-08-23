"""
数据查看器
直接查看数据库中的数据，不依赖管理台
"""

import pymysql
import json
from datetime import datetime

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def view_industry_data():
    """查看行业数据"""
    print("\n" + "="*60)
    print("行业分类数据")
    print("="*60)
    
    try:
        connection = get_db_connection()
        if not connection:
            return
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT * FROM l1_wind_industry_classification ORDER BY industry_code")
        industries = cursor.fetchall()
        
        print(f"总共有 {len(industries)} 条行业数据:")
        print("-" * 60)
        
        for industry in industries:
            print(f"代码: {industry['industry_code']}")
            print(f"名称: {industry['industry_name']}")
            print(f"层级: L{industry['industry_level']}")
            print(f"状态: {industry['status']}")
            print(f"描述: {industry['industry_desc']}")
            print(f"主要公司: {industry['major_companies']}")
            print(f"关键词: {industry['industry_keywords']}")
            print(f"市值: {industry['market_cap_total']}")
            print(f"公司数: {industry['company_count']}")
            print(f"更新时间: {industry['update_date']}")
            print(f"数据源: {industry['source']}")
            print("-" * 60)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"查看行业数据失败: {e}")

def view_company_data():
    """查看公司数据"""
    print("\n" + "="*60)
    print("公司列表数据")
    print("="*60)
    
    try:
        connection = get_db_connection()
        if not connection:
            return
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT * FROM l1_company_list_info ORDER BY stock_code")
        companies = cursor.fetchall()
        
        print(f"总共有 {len(companies)} 条公司数据:")
        print("-" * 60)
        
        for company in companies:
            print(f"公司名称: {company['company_name']}")
            print(f"股票代码: {company['stock_code']}")
            print(f"市场: {company['market']}")
            print(f"简称: {company['short_name']}")
            print(f"行业代码: {company['industry_code']}")
            print(f"上市日期: {company['list_date']}")
            print(f"状态: {company['status']}")
            print(f"公司类型: {company['company_type']}")
            print(f"地区: {company['area']}")
            print(f"网站: {company['website']}")
            print(f"经营范围: {company['business_scope']}")
            print(f"市值: {company['market_cap']}")
            print(f"员工数: {company['employees']}")
            print(f"更新时间: {company['update_date']}")
            print(f"数据源: {company['source']}")
            print("-" * 60)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"查看公司数据失败: {e}")

def view_hotspot_data():
    """查看热点数据"""
    print("\n" + "="*60)
    print("热点数据")
    print("="*60)
    
    try:
        connection = get_db_connection()
        if not connection:
            return
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT * FROM l1_domestic_hotspot_data ORDER BY update_date DESC")
        hotspots = cursor.fetchall()
        
        print(f"总共有 {len(hotspots)} 条热点数据:")
        
        if len(hotspots) == 0:
            print("暂无热点数据")
        else:
            print("-" * 60)
            for hotspot in hotspots:
                print(f"热点ID: {hotspot['hotspot_id']}")
                print(f"标题: {hotspot['title']}")
                print(f"类型: {hotspot['hotspot_type']}")
                print(f"级别: {hotspot['hotspot_level']}")
                print(f"状态: {hotspot['status']}")
                print(f"热度得分: {hotspot['heat_score']}")
                print(f"情感得分: {hotspot['sentiment_score']}")
                print(f"关键词: {hotspot['keywords']}")
                print(f"相关公司: {hotspot['related_companies']}")
                print(f"相关行业: {hotspot['related_industries']}")
                print(f"发布时间: {hotspot['publish_time']}")
                print(f"更新时间: {hotspot['update_date']}")
                print(f"数据源: {hotspot['source']}")
                print("-" * 60)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"查看热点数据失败: {e}")

def view_module_status():
    """查看模块状态"""
    print("\n" + "="*60)
    print("模块状态数据")
    print("="*60)
    
    try:
        connection = get_db_connection()
        if not connection:
            return
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT * FROM system_module_status ORDER BY updated_at DESC")
        modules = cursor.fetchall()
        
        print(f"总共有 {len(modules)} 条模块状态数据:")
        print("-" * 60)
        
        for module in modules:
            print(f"模块名称: {module['module_name']}")
            print(f"所属层级: {module['layer']}")
            print(f"状态: {module['status']}")
            print(f"最后运行时间: {module['last_run_time']}")
            print(f"下次运行时间: {module['next_run_time']}")
            print(f"运行次数: {module['run_count']}")
            print(f"错误次数: {module['error_count']}")
            print(f"最后错误信息: {module['last_error_message']}")
            print(f"配置信息: {module['config']}")
            print(f"创建时间: {module['created_at']}")
            print(f"更新时间: {module['updated_at']}")
            print("-" * 60)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"查看模块状态失败: {e}")

def view_data_statistics():
    """查看数据统计"""
    print("\n" + "="*60)
    print("数据统计")
    print("="*60)
    
    try:
        connection = get_db_connection()
        if not connection:
            return
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 各表数据量统计
        tables = [
            'l1_wind_industry_classification',
            'l1_company_list_info',
            'l1_domestic_hotspot_data',
            'system_module_status'
        ]
        
        print("各表数据量:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            result = cursor.fetchone()
            print(f"  {table}: {result['count']} 条记录")
        
        print("\n行业层级统计:")
        cursor.execute("SELECT industry_level, COUNT(*) as count FROM l1_wind_industry_classification GROUP BY industry_level")
        level_stats = cursor.fetchall()
        for stat in level_stats:
            print(f"  L{stat['industry_level']}: {stat['count']} 个")
        
        print("\n公司市场统计:")
        cursor.execute("SELECT market, COUNT(*) as count FROM l1_company_list_info GROUP BY market")
        market_stats = cursor.fetchall()
        for stat in market_stats:
            print(f"  {stat['market']}: {stat['count']} 家")
        
        print("\n热点类型统计:")
        cursor.execute("SELECT hotspot_type, COUNT(*) as count FROM l1_domestic_hotspot_data GROUP BY hotspot_type")
        type_stats = cursor.fetchall()
        if type_stats:
            for stat in type_stats:
                print(f"  {stat['hotspot_type']}: {stat['count']} 条")
        else:
            print("  暂无热点数据")
        
        print("\n模块状态统计:")
        cursor.execute("SELECT status, COUNT(*) as count FROM system_module_status GROUP BY status")
        status_stats = cursor.fetchall()
        for stat in status_stats:
            print(f"  {stat['status']}: {stat['count']} 个")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"查看数据统计失败: {e}")

def view_data_quality():
    """查看数据质量"""
    print("\n" + "="*60)
    print("数据质量报告")
    print("="*60)
    
    try:
        connection = get_db_connection()
        if not connection:
            return
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 行业数据质量
        cursor.execute("SELECT COUNT(*) as total, COUNT(industry_desc) as desc_count FROM l1_wind_industry_classification")
        industry_result = cursor.fetchone()
        industry_completeness = (industry_result['desc_count'] / industry_result['total']) * 100 if industry_result['total'] > 0 else 0
        
        cursor.execute("SELECT COUNT(*) as total, COUNT(DISTINCT industry_code) as unique_count FROM l1_wind_industry_classification")
        industry_unique = cursor.fetchone()
        industry_uniqueness = (industry_unique['unique_count'] / industry_unique['total']) * 100 if industry_unique['total'] > 0 else 0
        
        # 公司数据质量
        cursor.execute("SELECT COUNT(*) as total, COUNT(short_name) as name_count FROM l1_company_list_info")
        company_result = cursor.fetchone()
        company_completeness = (company_result['name_count'] / company_result['total']) * 100 if company_result['total'] > 0 else 0
        
        cursor.execute("SELECT COUNT(*) as total, COUNT(DISTINCT stock_code) as unique_count FROM l1_company_list_info")
        company_unique = cursor.fetchone()
        company_uniqueness = (company_unique['unique_count'] / company_unique['total']) * 100 if company_unique['total'] > 0 else 0
        
        print("数据完整性:")
        print(f"  行业描述完整率: {industry_completeness:.1f}%")
        print(f"  公司简称完整率: {company_completeness:.1f}%")
        
        print("\n数据唯一性:")
        print(f"  行业代码唯一性: {industry_uniqueness:.1f}%")
        print(f"  股票代码唯一性: {company_uniqueness:.1f}%")
        
        print("\n数据时效性:")
        cursor.execute("SELECT COUNT(*) as recent_count FROM l1_wind_industry_classification WHERE update_date >= DATE_SUB(NOW(), INTERVAL 1 DAY)")
        industry_recent = cursor.fetchone()['recent_count']
        industry_timeliness = (industry_recent / industry_result['total']) * 100 if industry_result['total'] > 0 else 0
        print(f"  行业数据时效性: {industry_timeliness:.1f}%")
        
        cursor.execute("SELECT COUNT(*) as recent_count FROM l1_company_list_info WHERE update_date >= DATE_SUB(NOW(), INTERVAL 1 DAY)")
        company_recent = cursor.fetchone()['recent_count']
        company_timeliness = (company_recent / company_result['total']) * 100 if company_result['total'] > 0 else 0
        print(f"  公司数据时效性: {company_timeliness:.1f}%")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"查看数据质量失败: {e}")

def main():
    """主函数"""
    print("第一层模块数据查看器")
    print("="*60)
    print("直接查看数据库中的数据")
    print("="*60)
    
    while True:
        print("\n请选择要查看的数据:")
        print("1. 行业分类数据")
        print("2. 公司列表数据")
        print("3. 热点数据")
        print("4. 模块状态数据")
        print("5. 数据统计")
        print("6. 数据质量报告")
        print("7. 查看所有数据")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-7): ").strip()
        
        if choice == '0':
            print("退出数据查看器")
            break
        elif choice == '1':
            view_industry_data()
        elif choice == '2':
            view_company_data()
        elif choice == '3':
            view_hotspot_data()
        elif choice == '4':
            view_module_status()
        elif choice == '5':
            view_data_statistics()
        elif choice == '6':
            view_data_quality()
        elif choice == '7':
            view_industry_data()
            view_company_data()
            view_hotspot_data()
            view_module_status()
            view_data_statistics()
            view_data_quality()
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main() 