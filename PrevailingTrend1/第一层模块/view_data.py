"""
简单数据查看器
"""

import pymysql

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def view_all_data():
    """查看所有数据"""
    print("第一层模块数据查看")
    print("="*60)
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 查看行业数据
        print("\n1. 行业分类数据:")
        cursor.execute("SELECT * FROM l1_wind_industry_classification")
        industries = cursor.fetchall()
        print(f"   总数: {len(industries)} 条")
        for industry in industries:
            print(f"   {industry['industry_code']} - {industry['industry_name']} (L{industry['industry_level']})")
        
        # 查看公司数据
        print("\n2. 公司列表数据:")
        cursor.execute("SELECT * FROM l1_company_list_info")
        companies = cursor.fetchall()
        print(f"   总数: {len(companies)} 条")
        for company in companies:
            print(f"   {company['company_name']} ({company['stock_code']}) - {company['market']}")
        
        # 查看热点数据
        print("\n3. 热点数据:")
        cursor.execute("SELECT * FROM l1_domestic_hotspot_data")
        hotspots = cursor.fetchall()
        print(f"   总数: {len(hotspots)} 条")
        if hotspots:
            for hotspot in hotspots:
                print(f"   {hotspot['title'][:50]}... (热度: {hotspot.get('heat_score', 'N/A')})")
        else:
            print("   暂无热点数据")
        
        # 查看模块状态
        print("\n4. 模块状态:")
        cursor.execute("SELECT * FROM system_module_status")
        modules = cursor.fetchall()
        print(f"   总数: {len(modules)} 条")
        for module in modules:
            print(f"   {module['module_name']} - {module['status']}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"查看数据失败: {e}")

if __name__ == "__main__":
    view_all_data() 