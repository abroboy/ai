"""
管理台API测试脚本
测试管理台的API接口和数据连接
"""

import requests
import json
import time

def test_api_endpoints():
    """测试API接口"""
    base_url = "http://localhost:8080"
    
    print("测试管理台API接口...")
    print("=" * 50)
    
    # 测试首页
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ 首页访问: {response.status_code}")
    except Exception as e:
        print(f"❌ 首页访问失败: {e}")
    
    # 测试仪表板API
    try:
        response = requests.get(f"{base_url}/api/dashboard")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 仪表板API: {response.status_code}")
            if data.get('success'):
                dashboard_data = data.get('data', {})
                modules = dashboard_data.get('modules', {})
                data_stats = dashboard_data.get('data', {})
                print(f"  模块统计: 总数={modules.get('total', 0)}, 运行中={modules.get('running', 0)}")
                print(f"  数据统计: 行业={data_stats.get('industries', 0)}, 公司={data_stats.get('companies', 0)}, 热点={data_stats.get('hotspots', 0)}")
            else:
                print(f"  ❌ API返回错误: {data.get('message', '未知错误')}")
        else:
            print(f"❌ 仪表板API: {response.status_code}")
    except Exception as e:
        print(f"❌ 仪表板API失败: {e}")
    
    # 测试模块API
    try:
        response = requests.get(f"{base_url}/api/modules")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 模块API: {response.status_code}")
            if data.get('success'):
                modules = data.get('data', {})
                print(f"  模块数量: {len(modules)}")
                for module_id, module_info in modules.items():
                    print(f"    {module_info['name']}: {module_info['status']}")
            else:
                print(f"  ❌ API返回错误: {data.get('message', '未知错误')}")
        else:
            print(f"❌ 模块API: {response.status_code}")
    except Exception as e:
        print(f"❌ 模块API失败: {e}")
    
    # 测试数据API
    data_types = ['industries', 'companies', 'hotspots', 'module_status']
    for data_type in data_types:
        try:
            response = requests.get(f"{base_url}/api/data/{data_type}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {data_type}数据API: {response.status_code}")
                if data.get('success'):
                    count = data.get('count', 0)
                    print(f"  数据条数: {count}")
                else:
                    print(f"  ❌ API返回错误: {data.get('message', '未知错误')}")
            else:
                print(f"❌ {data_type}数据API: {response.status_code}")
        except Exception as e:
            print(f"❌ {data_type}数据API失败: {e}")
    
    # 测试统计API
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 统计API: {response.status_code}")
            if data.get('success'):
                stats_data = data.get('data', {})
                print(f"  统计数据类型: {list(stats_data.keys())}")
            else:
                print(f"  ❌ API返回错误: {data.get('message', '未知错误')}")
        else:
            print(f"❌ 统计API: {response.status_code}")
    except Exception as e:
        print(f"❌ 统计API失败: {e}")

def test_database_connection():
    """测试数据库连接"""
    print("\n测试数据库连接...")
    print("=" * 50)
    
    try:
        import pymysql
        
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='rr1234RR',
            database='pt',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 测试各表数据
        tables = [
            'l1_wind_industry_classification',
            'l1_company_list_info',
            'l1_domestic_hotspot_data',
            'system_module_status'
        ]
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                result = cursor.fetchone()
                print(f"✅ {table}: {result['count']} 条记录")
            except Exception as e:
                print(f"❌ {table}: {e}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")

def main():
    """主函数"""
    print("管理台API测试")
    print("=" * 60)
    
    # 等待管理台启动
    print("等待管理台启动...")
    time.sleep(2)
    
    # 测试数据库连接
    test_database_connection()
    
    # 测试API接口
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("如果看到数据，说明管理台工作正常")
    print("如果看不到数据，请检查:")
    print("1. 管理台是否正常启动")
    print("2. 数据库连接是否正常")
    print("3. 数据表是否有数据")

if __name__ == "__main__":
    main() 