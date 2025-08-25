"""
万得行业分类模块演示测试
"""

import requests
import time
import sys

def test_api_server():
    """测试API服务器"""
    print("测试API服务器...")
    
    base_url = "http://localhost:5000"
    
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    try:
        # 测试首页
        print("测试首页...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 首页测试成功: {data}")
        else:
            print(f"❌ 首页测试失败: {response.status_code}")
            return False
        
        # 测试健康检查
        print("测试健康检查...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查成功: {data}")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
        
        # 测试行业列表
        print("测试行业列表...")
        response = requests.get(f"{base_url}/api/industries", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 行业列表成功: {data}")
        else:
            print(f"❌ 行业列表失败: {response.status_code}")
            return False
        
        # 测试股票列表
        print("测试股票列表...")
        response = requests.get(f"{base_url}/api/stocks/801010", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 股票列表成功: {data}")
        else:
            print(f"❌ 股票列表失败: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器正在运行")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_models():
    """测试数据模型"""
    print("\n测试数据模型...")
    try:
        from models.industry_model import IndustryModel, IndustryStatus
        from models.stock_industry_model import StockIndustryModel, MappingStatus
        from datetime import datetime
        
        # 创建行业模型
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
        
        # 创建股票行业映射模型
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

def main():
    """主测试函数"""
    print("万得行业分类模块演示测试")
    print("=" * 50)
    
    results = []
    
    # 测试数据模型
    results.append(test_models())
    
    # 测试API服务器
    results.append(test_api_server())
    
    # 输出结果
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！模块运行正常！")
    else:
        print("⚠️  部分测试失败")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 