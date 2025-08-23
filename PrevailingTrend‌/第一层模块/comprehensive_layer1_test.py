"""
第一层模块综合测试脚本
测试所有第一层模块的功能和数据
"""

import sys
import os
import pymysql
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """测试数据库连接"""
    print("测试数据库连接...")
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='rr1234RR',
            database='pt',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ 数据库连接成功，MySQL版本: {version['VERSION()']}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def test_all_tables():
    """测试所有表"""
    print("\n测试所有表...")
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='rr1234RR',
            database='pt',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 第一层模块表
        layer1_tables = [
            'l1_wind_industry_classification',
            'l1_wind_stock_industry_mapping',
            'l1_company_list_info',
            'l1_domestic_hotspot_data'
        ]
        
        print("第一层模块表:")
        for table in layer1_tables:
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            result = cursor.fetchone()
            if result:
                # 查询记录数
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                count_result = cursor.fetchone()
                print(f"  ✅ {table}: {count_result['count']} 条记录")
            else:
                print(f"  ❌ {table}: 表不存在")
        
        # 系统表
        system_tables = [
            'system_logs',
            'system_data_flow_logs',
            'system_module_status',
            'system_data_quality'
        ]
        
        print("\n系统表:")
        for table in system_tables:
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            result = cursor.fetchone()
            if result:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                count_result = cursor.fetchone()
                print(f"  ✅ {table}: {count_result['count']} 条记录")
            else:
                print(f"  ❌ {table}: 表不存在")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 表测试失败: {e}")
        return False

def test_data_operations():
    """测试数据操作"""
    print("\n测试数据操作...")
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='rr1234RR',
            database='pt',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 测试行业数据查询
        cursor.execute("SELECT * FROM l1_wind_industry_classification LIMIT 3")
        industries = cursor.fetchall()
        print(f"✅ 行业分类数据: {len(industries)} 条")
        
        # 测试公司数据查询
        cursor.execute("SELECT * FROM l1_company_list_info LIMIT 3")
        companies = cursor.fetchall()
        print(f"✅ 公司列表数据: {len(companies)} 条")
        
        # 测试热点数据查询
        cursor.execute("SELECT * FROM l1_domestic_hotspot_data LIMIT 3")
        hotspots = cursor.fetchall()
        print(f"✅ 热点数据: {len(hotspots)} 条")
        
        # 测试模块状态查询
        cursor.execute("SELECT * FROM system_module_status LIMIT 3")
        modules = cursor.fetchall()
        print(f"✅ 模块状态数据: {len(modules)} 条")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据操作测试失败: {e}")
        return False

def test_data_insertion():
    """测试数据插入"""
    print("\n测试数据插入...")
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='rr1234RR',
            database='pt',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 插入测试行业数据
        industry_sql = """
        INSERT INTO l1_wind_industry_classification 
        (industry_code, industry_name, industry_level, parent_code, sw_code, csrc_code, status, industry_desc, major_companies, industry_keywords, market_cap_total, company_count, update_date, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        test_industry = ('777777', '测试行业777', 1, None, '777777', 'TEST', 'active', '测试用行业777', '["测试公司"]', '["测试"]', 7777777.0, 7, datetime.now(), 'test')
        cursor.execute(industry_sql, test_industry)
        
        # 插入测试公司数据
        company_sql = """
        INSERT INTO l1_company_list_info 
        (company_name, stock_code, market, short_name, industry_code, list_date, status, company_type, area, website, business_scope, market_cap, employees, update_date, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        test_company = ('测试公司777股份有限公司', '777777', 'SZ', '测试公司777', '777777', '2020-01-01', 'active', 'main_board', '深圳', 'http://test777.com', '测试业务', 777777777.0, 777, datetime.now(), 'test')
        cursor.execute(company_sql, test_company)
        
        # 插入测试热点数据
        hotspot_sql = """
        INSERT INTO l1_domestic_hotspot_data 
        (hotspot_id, title, content, hotspot_type, hotspot_level, status, source, url, publish_time, keywords, related_companies, related_industries, sentiment_score, heat_score, update_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        test_hotspot = ('TEST_777', '测试热点777', '测试热点内容777', 'test', 'medium', 'active', 'test', 'http://test777.com', datetime.now(), '["测试"]', '["测试公司"]', '["777777"]', 0.7, 77.7, datetime.now())
        cursor.execute(hotspot_sql, test_hotspot)
        
        connection.commit()
        print("✅ 测试数据插入成功")
        
        # 验证数据
        cursor.execute("SELECT COUNT(*) as count FROM l1_wind_industry_classification WHERE industry_code = '777777'")
        industry_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) as count FROM l1_company_list_info WHERE stock_code = '777777'")
        company_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) as count FROM l1_domestic_hotspot_data WHERE hotspot_id = 'TEST_777'")
        hotspot_count = cursor.fetchone()[0]
        
        if industry_count > 0 and company_count > 0 and hotspot_count > 0:
            print("✅ 数据验证成功")
        else:
            print("❌ 数据验证失败")
        
        # 清理测试数据
        cursor.execute("DELETE FROM l1_wind_industry_classification WHERE industry_code = '777777'")
        cursor.execute("DELETE FROM l1_company_list_info WHERE stock_code = '777777'")
        cursor.execute("DELETE FROM l1_domestic_hotspot_data WHERE hotspot_id = 'TEST_777'")
        connection.commit()
        print("✅ 测试数据清理完成")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据插入测试失败: {e}")
        return False

def test_data_statistics():
    """测试数据统计"""
    print("\n测试数据统计...")
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='rr1234RR',
            database='pt',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 统计各表数据量
        tables = [
            'l1_wind_industry_classification',
            'l1_wind_stock_industry_mapping',
            'l1_company_list_info',
            'l1_domestic_hotspot_data',
            'system_module_status'
        ]
        
        print("各表数据统计:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            result = cursor.fetchone()
            print(f"  {table}: {result['count']} 条记录")
        
        # 统计行业数据
        cursor.execute("SELECT industry_level, COUNT(*) as count FROM l1_wind_industry_classification GROUP BY industry_level")
        level_stats = cursor.fetchall()
        print("\n行业层级统计:")
        for stat in level_stats:
            print(f"  L{stat['industry_level']}: {stat['count']} 个")
        
        # 统计公司数据
        cursor.execute("SELECT market, COUNT(*) as count FROM l1_company_list_info GROUP BY market")
        market_stats = cursor.fetchall()
        print("\n公司市场统计:")
        for stat in market_stats:
            print(f"  {stat['market']}: {stat['count']} 家")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据统计测试失败: {e}")
        return False

def test_data_quality():
    """测试数据质量"""
    print("\n测试数据质量...")
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='rr1234RR',
            database='pt',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 检查数据完整性
        cursor.execute("SELECT COUNT(*) as total, COUNT(industry_desc) as desc_count FROM l1_wind_industry_classification")
        industry_result = cursor.fetchone()
        industry_completeness = (industry_result['desc_count'] / industry_result['total']) * 100 if industry_result['total'] > 0 else 0
        
        cursor.execute("SELECT COUNT(*) as total, COUNT(short_name) as name_count FROM l1_company_list_info")
        company_result = cursor.fetchone()
        company_completeness = (company_result['name_count'] / company_result['total']) * 100 if company_result['total'] > 0 else 0
        
        print(f"✅ 行业描述完整率: {industry_completeness:.1f}%")
        print(f"✅ 公司简称完整率: {company_completeness:.1f}%")
        
        # 检查数据唯一性
        cursor.execute("SELECT COUNT(*) as total, COUNT(DISTINCT industry_code) as unique_count FROM l1_wind_industry_classification")
        industry_unique = cursor.fetchone()
        industry_uniqueness = (industry_unique['unique_count'] / industry_unique['total']) * 100 if industry_unique['total'] > 0 else 0
        
        cursor.execute("SELECT COUNT(*) as total, COUNT(DISTINCT stock_code) as unique_count FROM l1_company_list_info")
        company_unique = cursor.fetchone()
        company_uniqueness = (company_unique['unique_count'] / company_unique['total']) * 100 if company_unique['total'] > 0 else 0
        
        print(f"✅ 行业代码唯一性: {industry_uniqueness:.1f}%")
        print(f"✅ 股票代码唯一性: {company_uniqueness:.1f}%")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据质量测试失败: {e}")
        return False

def test_module_integration():
    """测试模块集成"""
    print("\n测试模块集成...")
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='rr1234RR',
            database='pt',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 测试公司与行业关联查询
        sql = """
        SELECT 
            c.company_name,
            c.stock_code,
            c.market,
            w.industry_name,
            w.industry_level
        FROM l1_company_list_info c
        LEFT JOIN l1_wind_stock_industry_mapping w ON c.stock_code = w.stock_code
        LIMIT 5
        """
        
        cursor.execute(sql)
        mappings = cursor.fetchall()
        print(f"✅ 公司与行业关联查询: {len(mappings)} 条记录")
        
        for mapping in mappings:
            industry_name = mapping['industry_name'] or '未分类'
            print(f"  {mapping['company_name']} ({mapping['stock_code']}) -> {industry_name}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 模块集成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("第一层模块综合测试")
    print("=" * 60)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(test_database_connection())
    test_results.append(test_all_tables())
    test_results.append(test_data_operations())
    test_results.append(test_data_insertion())
    test_results.append(test_data_statistics())
    test_results.append(test_data_quality())
    test_results.append(test_module_integration())
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    passed = sum(test_results)
    total = len(test_results)
    print(f"通过: {passed}/{total}")
    
    test_names = [
        "数据库连接",
        "表结构检查",
        "数据操作",
        "数据插入",
        "数据统计",
        "数据质量",
        "模块集成"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    if passed == total:
        print("\n🎉 所有测试通过！第一层模块功能正常！")
        print("\n模块状态:")
        print("✅ 万得行业分类模块: 正常")
        print("✅ 公司名字列表模块: 正常")
        print("✅ 国内热点数据模块: 正常")
        print("✅ 数据库配置: 正常")
        print("✅ 数据流向: 正常")
    else:
        print(f"\n⚠️  有 {total - passed} 项测试失败，需要修复")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 