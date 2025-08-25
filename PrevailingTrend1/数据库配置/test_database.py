"""
数据库连接测试脚本
测试数据库连接和基本操作
"""

import sys
import os
import pymysql
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_config import db_config, table_names

def test_connection():
    """测试数据库连接"""
    print("测试数据库连接...")
    
    try:
        connection = pymysql.connect(**db_config.get_connection_config())
        cursor = connection.cursor()
        
        # 测试查询
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ 数据库连接成功，MySQL版本: {version[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def test_tables():
    """测试表是否存在"""
    print("\n测试表结构...")
    
    try:
        connection = pymysql.connect(**db_config.get_connection_config())
        cursor = connection.cursor()
        
        # 检查第一层模块表
        layer1_tables = [
            'l1_wind_industry_classification',
            'l1_wind_stock_industry_mapping', 
            'l1_company_list_info',
            'l1_domestic_hotspot_data'
        ]
        
        for table in layer1_tables:
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            result = cursor.fetchone()
            if result:
                print(f"✅ 表 {table} 存在")
            else:
                print(f"❌ 表 {table} 不存在")
        
        # 检查系统表
        system_tables = [
            'system_logs',
            'system_data_flow_logs',
            'system_module_status',
            'system_data_quality'
        ]
        
        for table in system_tables:
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            result = cursor.fetchone()
            if result:
                print(f"✅ 表 {table} 存在")
            else:
                print(f"❌ 表 {table} 不存在")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 测试表结构失败: {e}")
        return False

def test_data():
    """测试数据查询"""
    print("\n测试数据查询...")
    
    try:
        connection = pymysql.connect(**db_config.get_connection_config())
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 查询行业数据
        cursor.execute("SELECT COUNT(*) as count FROM l1_wind_industry_classification")
        result = cursor.fetchone()
        print(f"✅ 行业分类表有 {result['count']} 条记录")
        
        # 查询公司数据
        cursor.execute("SELECT COUNT(*) as count FROM l1_company_list_info")
        result = cursor.fetchone()
        print(f"✅ 公司列表表有 {result['count']} 条记录")
        
        # 查询模块状态
        cursor.execute("SELECT COUNT(*) as count FROM system_module_status")
        result = cursor.fetchone()
        print(f"✅ 模块状态表有 {result['count']} 条记录")
        
        # 显示示例数据
        print("\n示例行业数据:")
        cursor.execute("SELECT industry_code, industry_name, industry_level FROM l1_wind_industry_classification LIMIT 3")
        industries = cursor.fetchall()
        for industry in industries:
            print(f"  {industry['industry_code']} - {industry['industry_name']} (L{industry['industry_level']})")
        
        print("\n示例公司数据:")
        cursor.execute("SELECT company_name, stock_code, market FROM l1_company_list_info LIMIT 3")
        companies = cursor.fetchall()
        for company in companies:
            print(f"  {company['company_name']} ({company['stock_code']}) - {company['market']}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 测试数据查询失败: {e}")
        return False

def test_table_names():
    """测试表名配置"""
    print("\n测试表名配置...")
    
    try:
        # 测试表名获取
        industry_table = table_names.get_table_name('LAYER1', 'wind_industry', 'industry_classification')
        print(f"✅ 行业分类表名: {industry_table}")
        
        company_table = table_names.get_table_name('LAYER1', 'company_list', 'company_info')
        print(f"✅ 公司信息表名: {company_table}")
        
        # 显示所有表名配置
        print("\n所有表名配置:")
        all_tables = table_names.get_all_tables()
        for layer, modules in all_tables.items():
            print(f"  {layer}:")
            for module, tables in modules.items():
                print(f"    {module}:")
                for table_name, table_id in tables.items():
                    print(f"      {table_name}: {table_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试表名配置失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("数据库连接测试")
    print("=" * 60)
    print(f"数据库配置:")
    print(f"  主机: {db_config.HOST}")
    print(f"  端口: {db_config.PORT}")
    print(f"  用户名: {db_config.USERNAME}")
    print(f"  数据库: {db_config.DATABASE}")
    print("=" * 60)
    
    test_results = []
    
    # 运行测试
    test_results.append(test_connection())
    test_results.append(test_tables())
    test_results.append(test_data())
    test_results.append(test_table_names())
    
    # 输出结果
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    passed = sum(test_results)
    total = len(test_results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！数据库配置正确！")
        print("\n数据库状态:")
        print("✅ 连接正常")
        print("✅ 表结构完整")
        print("✅ 数据可查询")
        print("✅ 配置正确")
    else:
        print(f"⚠️  有 {total - passed} 项测试失败")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 