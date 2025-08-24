import akshare as ak
import pymysql
import time

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def get_industry_list():
    """获取行业列表"""
    print("获取行业列表...")
    
    try:
        # 获取东方财富行业分类
        industries = ak.stock_board_industry_name_em()
        print(f"✅ 获取到 {len(industries)} 个行业")
        return industries
    except Exception as e:
        print(f"❌ 获取行业列表失败: {e}")
        return None

def get_stocks_by_industry(industry_code):
    """根据行业代码获取股票列表"""
    try:
        stocks = ak.stock_board_industry_cons_em(symbol=industry_code)
        return stocks
    except Exception as e:
        print(f"❌ 获取行业 {industry_code} 股票失败: {e}")
        return None

def update_stock_industry_mapping():
    """更新股票行业映射"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 获取行业列表
        industries = get_industry_list()
        if industries is None or industries.empty:
            return False
        
        print(f"开始更新 {len(industries)} 个行业的股票映射...")
        
        total_updated = 0
        
        for _, industry in industries.iterrows():
            industry_code = industry['板块代码']
            industry_name = industry['板块名称']
            
            print(f"处理行业: {industry_name} ({industry_code})")
            
            # 获取该行业的股票
            stocks = get_stocks_by_industry(industry_code)
            if stocks is not None and not stocks.empty:
                print(f"  获取到 {len(stocks)} 只股票")
                
                for _, stock in stocks.iterrows():
                    stock_code = str(stock.get('代码', ''))
                    stock_name = stock.get('名称', '')
                    
                    if stock_code and stock_name and len(stock_code) == 6:
                        # 更新股票行业信息
                        sql = """
                        UPDATE stock_industry_mapping 
                        SET industry_code = %s, industry_name = %s, mapping_status = 'confirmed', confidence = 1.0
                        WHERE stock_code = %s
                        """
                        cursor.execute(sql, (industry_code, industry_name, stock_code))
                        total_updated += 1
            else:
                print(f"  未获取到股票数据")
            
            time.sleep(0.5)  # 避免请求过快
        
        connection.commit()
        print(f"✅ 成功更新 {total_updated} 只股票的行业映射")
        
        # 统计更新后的数据
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE industry_name != ''")
        mapped_count = cursor.fetchone()[0]
        print(f"📊 已映射股票数: {mapped_count}")
        
        cursor.execute("SELECT industry_name, COUNT(*) as count FROM stock_industry_mapping WHERE industry_name != '' GROUP BY industry_name ORDER BY count DESC LIMIT 10")
        industries = cursor.fetchall()
        print("\n行业分布TOP10:")
        for industry, count in industries:
            print(f"  {industry}: {count}只股票")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🏭 开始获取行业股票映射")
    print("=" * 60)
    
    if update_stock_industry_mapping():
        print("\n" + "=" * 60)
        print("✅ 行业映射完成！")
        print("🌐 访问 http://127.0.0.1:5001 查看数据")
        print("=" * 60)
    else:
        print("❌ 行业映射失败！")

if __name__ == "__main__":
    main() 