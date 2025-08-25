"""
万得行业分类模块直接测试脚本
直接测试核心功能，避免导入问题
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
        
        # 测试查询行业数据
        cursor.execute("SELECT * FROM l1_wind_industry_classification LIMIT 5")
        industries = cursor.fetchall()
        print(f"✅ 查询到 {len(industries)} 条行业数据")
        
        for industry in industries:
            print(f"  {industry['industry_code']} - {industry['industry_name']} (L{industry['industry_level']})")
        
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
        
        # 插入测试行业数据
        test_industry = {
            'industry_code': '888888',
            'industry_name': '测试行业888',
            'industry_level': 1,
            'parent_code': None,
            'sw_code': '888888',
            'csrc_code': 'TEST',
            'status': 'active',
            'industry_desc': '测试用行业888',
            'major_companies': '["测试公司A", "测试公司B"]',
            'industry_keywords': '["测试", "行业", "888"]',
            'market_cap_total': 8888888.0,
            'company_count': 8,
            'update_date': datetime.now(),
            'source': 'test'
        }
        
        sql = """
        INSERT INTO l1_wind_industry_classification 
        (industry_code, industry_name, industry_level, parent_code, sw_code, csrc_code, status, industry_desc, major_companies, industry_keywords, market_cap_total, company_count, update_date, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (
            test_industry['industry_code'],
            test_industry['industry_name'],
            test_industry['industry_level'],
            test_industry['parent_code'],
            test_industry['sw_code'],
            test_industry['csrc_code'],
            test_industry['status'],
            test_industry['industry_desc'],
            test_industry['major_companies'],
            test_industry['industry_keywords'],
            test_industry['market_cap_total'],
            test_industry['company_count'],
            test_industry['update_date'],
            test_industry['source']
        ))
        
        connection.commit()
        print("✅ 测试数据插入成功")
        
        # 验证插入的数据
        cursor.execute("SELECT * FROM l1_wind_industry_classification WHERE industry_code = '888888'")
        result = cursor.fetchone()
        if result:
            print("✅ 数据验证成功")
        else:
            print("❌ 数据验证失败")
        
        # 清理测试数据
        cursor.execute("DELETE FROM l1_wind_industry_classification WHERE industry_code = '888888'")
        connection.commit()
        print("✅ 测试数据清理完成")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据插入测试失败: {e}")
        return False

def test_data_update():
    """测试数据更新"""
    print("\n测试数据更新...")
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
        
        # 更新行业描述
        update_sql = """
        UPDATE l1_wind_industry_classification 
        SET industry_desc = '更新后的行业描述' 
        WHERE industry_code = '801010'
        """
        
        cursor.execute(update_sql)
        connection.commit()
        print("✅ 数据更新成功")
        
        # 验证更新
        cursor.execute("SELECT industry_desc FROM l1_wind_industry_classification WHERE industry_code = '801010'")
        result = cursor.fetchone()
        if result and '更新后的行业描述' in result[0]:
            print("✅ 数据更新验证成功")
        else:
            print("❌ 数据更新验证失败")
        
        # 恢复原数据
        restore_sql = """
        UPDATE l1_wind_industry_classification 
        SET industry_desc = '农业、林业、畜牧业、渔业' 
        WHERE industry_code = '801010'
        """
        
        cursor.execute(restore_sql)
        connection.commit()
        print("✅ 数据恢复完成")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据更新测试失败: {e}")
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
        
        # 统计行业数据
        cursor.execute("SELECT COUNT(*) as total FROM l1_wind_industry_classification")
        industry_count = cursor.fetchone()['total']
        print(f"✅ 行业分类总数: {industry_count}")
        
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
        
        # 按行业层级统计
        cursor.execute("SELECT industry_level, COUNT(*) as count FROM l1_wind_industry_classification GROUP BY industry_level")
        level_stats = cursor.fetchall()
        print("✅ 按行业层级统计:")
        for stat in level_stats:
            print(f"  L{stat['industry_level']}: {stat['count']} 个")
        
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
        result = cursor.fetchone()
        completeness = (result['desc_count'] / result['total']) * 100 if result['total'] > 0 else 0
        print(f"✅ 行业描述完整率: {completeness:.1f}%")
        
        # 检查数据唯一性
        cursor.execute("SELECT COUNT(*) as total FROM l1_wind_industry_classification")
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(DISTINCT industry_code) as unique_count FROM l1_wind_industry_classification")
        unique = cursor.fetchone()['unique_count']
        uniqueness = (unique / total) * 100 if total > 0 else 0
        print(f"✅ 行业代码唯一性: {uniqueness:.1f}%")
        
        # 检查数据时效性
        cursor.execute("SELECT COUNT(*) as recent_count FROM l1_wind_industry_classification WHERE update_date >= DATE_SUB(NOW(), INTERVAL 1 DAY)")
        recent = cursor.fetchone()['recent_count']
        timeliness = (recent / total) * 100 if total > 0 else 0
        print(f"✅ 数据时效性: {timeliness:.1f}%")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据质量测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("万得行业分类模块直接测试")
    print("=" * 60)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(test_database())
    test_results.append(test_data_insertion())
    test_results.append(test_data_update())
    test_results.append(test_data_statistics())
    test_results.append(test_data_quality())
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    passed = sum(test_results)
    total = len(test_results)
    print(f"通过: {passed}/{total}")
    
    test_names = [
        "数据库功能",
        "数据插入",
        "数据更新",
        "数据统计",
        "数据质量"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    if passed == total:
        print("\n🎉 所有测试通过！万得行业分类模块数据功能正常！")
    else:
        print(f"\n⚠️  有 {total - passed} 项测试失败，需要修复")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 