"""
万得行业分类模块修复版测试脚本
解决相对导入问题
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
        cursor.execute("SELECT COUNT(*) as count FROM l1_wind_industry_classification")
        result = cursor.fetchone()
        print(f"✅ 数据库连接成功，行业分类表有 {result['count']} 条记录")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def test_models():
    """测试数据模型"""
    print("\n测试数据模型...")
    try:
        # 直接导入模型文件
        import models.industry_model
        import models.stock_industry_model
        
        from models.industry_model import IndustryModel, IndustryStatus
        from models.stock_industry_model import StockIndustryModel, MappingStatus
        
        # 测试行业模型
        industry = IndustryModel(
            industry_code="801010",
            industry_name="农林牧渔",
            industry_level=1,
            parent_code=None,
            sw_code="801010",
            csrc_code="A01",
            status=IndustryStatus.ACTIVE,
            industry_desc="农业、林业、畜牧业、渔业",
            major_companies=["牧原股份", "温氏股份"],
            industry_keywords=["农业", "养殖", "种植"],
            market_cap_total=1000000000.0,
            company_count=50,
            update_date=datetime.now(),
            source="wind"
        )
        
        print(f"✅ 行业模型创建成功: {industry}")
        
        # 测试股票行业映射模型
        mapping = StockIndustryModel(
            stock_code="000001",
            stock_name="平安银行",
            industry_code="801010",
            industry_name="农林牧渔",
            industry_level=1,
            mapping_date=datetime.now(),
            status=MappingStatus.ACTIVE,
            confidence=0.95,
            source="wind"
        )
        
        print(f"✅ 股票行业映射模型创建成功: {mapping}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据模型测试失败: {e}")
        return False

def test_config():
    """测试配置"""
    print("\n测试配置...")
    try:
        # 直接导入配置文件
        import utils.config
        from utils.config import config
        
        print("✅ 配置模块导入成功")
        print(f"  数据库: {config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}")
        print(f"  API服务: {config.API_HOST}:{config.API_PORT}")
        print(f"  日志级别: {config.LOG_LEVEL}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_logger():
    """测试日志器"""
    print("\n测试日志器...")
    try:
        import utils.logger
        from utils.logger import logger
        
        logger.info("测试信息日志")
        logger.warning("测试警告日志")
        logger.error("测试错误日志")
        print("✅ 日志器工作正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 日志器测试失败: {e}")
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
        
        # 查询行业数据
        cursor.execute("SELECT * FROM l1_wind_industry_classification LIMIT 3")
        industries = cursor.fetchall()
        print(f"✅ 查询到 {len(industries)} 条行业数据")
        
        for industry in industries:
            print(f"  {industry['industry_code']} - {industry['industry_name']}")
        
        # 查询公司数据
        cursor.execute("SELECT * FROM l1_company_list_info LIMIT 3")
        companies = cursor.fetchall()
        print(f"✅ 查询到 {len(companies)} 条公司数据")
        
        for company in companies:
            print(f"  {company['company_name']} ({company['stock_code']})")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据操作测试失败: {e}")
        return False

def test_core_modules():
    """测试核心模块"""
    print("\n测试核心模块...")
    try:
        # 测试简单验证器
        import core.simple_validator
        from core.simple_validator import SimpleValidator
        
        validator = SimpleValidator()
        print("✅ 验证器创建成功")
        
        # 测试简单分类器
        import core.simple_classifier
        from core.simple_classifier import SimpleClassifier
        
        classifier = SimpleClassifier()
        print("✅ 分类器创建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 核心模块测试失败: {e}")
        return False

def test_api_modules():
    """测试API模块"""
    print("\n测试API模块...")
    try:
        # 测试API模块导入
        import api.industry_api
        import api.stock_api
        
        print("✅ API模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ API模块测试失败: {e}")
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
            'industry_code': '999999',
            'industry_name': '测试行业',
            'industry_level': 1,
            'parent_code': None,
            'sw_code': '999999',
            'csrc_code': 'TEST',
            'status': 'active',
            'industry_desc': '测试用行业',
            'major_companies': '["测试公司1", "测试公司2"]',
            'industry_keywords': '["测试", "行业"]',
            'market_cap_total': 1000000.0,
            'company_count': 5,
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
        cursor.execute("SELECT * FROM l1_wind_industry_classification WHERE industry_code = '999999'")
        result = cursor.fetchone()
        if result:
            print("✅ 数据验证成功")
        else:
            print("❌ 数据验证失败")
        
        # 清理测试数据
        cursor.execute("DELETE FROM l1_wind_industry_classification WHERE industry_code = '999999'")
        connection.commit()
        print("✅ 测试数据清理完成")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据插入测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("万得行业分类模块修复版测试")
    print("=" * 60)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(test_database_connection())
    test_results.append(test_models())
    test_results.append(test_config())
    test_results.append(test_logger())
    test_results.append(test_data_operations())
    test_results.append(test_core_modules())
    test_results.append(test_api_modules())
    test_results.append(test_data_insertion())
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    passed = sum(test_results)
    total = len(test_results)
    print(f"通过: {passed}/{total}")
    
    test_names = [
        "数据库连接",
        "数据模型",
        "配置管理",
        "日志系统",
        "数据操作",
        "核心模块",
        "API模块",
        "数据插入"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    if passed == total:
        print("\n🎉 所有测试通过！万得行业分类模块功能正常！")
    else:
        print(f"\n⚠️  有 {total - passed} 项测试失败，需要修复")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 