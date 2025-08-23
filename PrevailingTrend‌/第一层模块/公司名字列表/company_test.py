"""
公司名字列表模块测试脚本
测试公司数据功能
"""

import sys
import os
import pymysql
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database():
    """测试数据库功能"""
    print("测试数据库功能...")
    try:
        # 直接连接数据库
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='rr1234RR',
            database='pt',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 测试查询公司数据
        cursor.execute("SELECT * FROM l1_company_list_info LIMIT 5")
        companies = cursor.fetchall()
        print(f"✅ 查询到 {len(companies)} 条公司数据")
        
        for company in companies:
            print(f"  {company['company_name']} ({company['stock_code']}) - {company['market']}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
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
        
        # 插入测试公司数据
        test_company = {
            'company_name': '测试公司股份有限公司',
            'stock_code': '999999',
            'market': 'SZ',
            'short_name': '测试公司',
            'industry_code': '801010',
            'list_date': '2020-01-01',
            'status': 'active',
            'company_type': 'main_board',
            'area': '深圳',
            'website': 'http://www.test.com',
            'business_scope': '测试业务范围',
            'market_cap': 999999999.0,
            'employees': 999,
            'update_date': datetime.now(),
            'source': 'test'
        }
        
        sql = """
        INSERT INTO l1_company_list_info 
        (company_name, stock_code, market, short_name, industry_code, list_date, status, company_type, area, website, business_scope, market_cap, employees, update_date, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (
            test_company['company_name'],
            test_company['stock_code'],
            test_company['market'],
            test_company['short_name'],
            test_company['industry_code'],
            test_company['list_date'],
            test_company['status'],
            test_company['company_type'],
            test_company['area'],
            test_company['website'],
            test_company['business_scope'],
            test_company['market_cap'],
            test_company['employees'],
            test_company['update_date'],
            test_company['source']
        ))
        
        connection.commit()
        print("✅ 测试公司数据插入成功")
        
        # 验证插入的数据
        cursor.execute("SELECT * FROM l1_company_list_info WHERE stock_code = '999999'")
        result = cursor.fetchone()
        if result:
            print("✅ 公司数据验证成功")
        else:
            print("❌ 公司数据验证失败")
        
        # 清理测试数据
        cursor.execute("DELETE FROM l1_company_list_info WHERE stock_code = '999999'")
        connection.commit()
        print("✅ 测试公司数据清理完成")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 公司数据插入测试失败: {e}")
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
        
        # 统计公司数据
        cursor.execute("SELECT COUNT(*) as total FROM l1_company_list_info")
        company_count = cursor.fetchone()['total']
        print(f"✅ 公司列表总数: {company_count}")
        
        # 按市场统计公司
        cursor.execute("SELECT market, COUNT(*) as count FROM l1_company_list_info GROUP BY market")
        market_stats = cursor.fetchall()
        print("✅ 按市场统计公司:")
        for stat in market_stats:
            print(f"  {stat['market']}: {stat['count']} 家")
        
        # 按地区统计公司
        cursor.execute("SELECT area, COUNT(*) as count FROM l1_company_list_info GROUP BY area")
        area_stats = cursor.fetchall()
        print("✅ 按地区统计公司:")
        for stat in area_stats:
            print(f"  {stat['area']}: {stat['count']} 家")
        
        # 按公司类型统计
        cursor.execute("SELECT company_type, COUNT(*) as count FROM l1_company_list_info GROUP BY company_type")
        type_stats = cursor.fetchall()
        print("✅ 按公司类型统计:")
        for stat in type_stats:
            print(f"  {stat['company_type']}: {stat['count']} 家")
        
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
        cursor.execute("SELECT COUNT(*) as total, COUNT(short_name) as short_name_count FROM l1_company_list_info")
        result = cursor.fetchone()
        completeness = (result['short_name_count'] / result['total']) * 100 if result['total'] > 0 else 0
        print(f"✅ 公司简称完整率: {completeness:.1f}%")
        
        # 检查数据唯一性
        cursor.execute("SELECT COUNT(*) as total FROM l1_company_list_info")
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(DISTINCT stock_code) as unique_count FROM l1_company_list_info")
        unique = cursor.fetchone()['unique_count']
        uniqueness = (unique / total) * 100 if total > 0 else 0
        print(f"✅ 股票代码唯一性: {uniqueness:.1f}%")
        
        # 检查数据时效性
        cursor.execute("SELECT COUNT(*) as recent_count FROM l1_company_list_info WHERE update_date >= DATE_SUB(NOW(), INTERVAL 1 DAY)")
        recent = cursor.fetchone()['recent_count']
        timeliness = (recent / total) * 100 if total > 0 else 0
        print(f"✅ 数据时效性: {timeliness:.1f}%")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据质量测试失败: {e}")
        return False

def test_company_industry_mapping():
    """测试公司与行业映射"""
    print("\n测试公司与行业映射...")
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
        
        # 查询公司与行业映射
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
        print(f"✅ 查询到 {len(mappings)} 条公司与行业映射")
        
        for mapping in mappings:
            industry_name = mapping['industry_name'] or '未分类'
            industry_level = mapping['industry_level'] or '未知'
            print(f"  {mapping['company_name']} ({mapping['stock_code']}) -> {industry_name} (L{industry_level})")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 公司与行业映射测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("公司名字列表模块测试")
    print("=" * 60)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(test_database())
    test_results.append(test_data_insertion())
    test_results.append(test_data_statistics())
    test_results.append(test_data_quality())
    test_results.append(test_company_industry_mapping())
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    passed = sum(test_results)
    total = len(test_results)
    print(f"通过: {passed}/{total}")
    
    test_names = [
        "数据库功能",
        "数据插入",
        "数据统计",
        "数据质量",
        "行业映射"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    if passed == total:
        print("\n🎉 所有测试通过！公司名字列表模块功能正常！")
    else:
        print(f"\n⚠️  有 {total - passed} 项测试失败，需要修复")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 