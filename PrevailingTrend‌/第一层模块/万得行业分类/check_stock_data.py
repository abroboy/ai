"""
检查股票数据统计信息
"""

import pymysql
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def check_stock_data():
    """检查股票数据统计信息"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=" * 60)
        print("📊 股票数据统计报告")
        print("=" * 60)
        
        # 1. 总体统计
        cursor.execute("SELECT COUNT(*) as total FROM stock_industry_mapping")
        total = cursor.fetchone()[0]
        print(f"📈 总股票数量: {total}")
        
        # 2. 映射状态统计
        cursor.execute("SELECT COUNT(*) as mapped FROM stock_industry_mapping WHERE industry_code IS NOT NULL AND industry_code != ''")
        mapped = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) as unmapped FROM stock_industry_mapping WHERE industry_code IS NULL OR industry_code = ''")
        unmapped = cursor.fetchone()[0]
        
        print(f"✅ 已映射股票: {mapped}")
        print(f"⏳ 未映射股票: {unmapped}")
        print(f"📊 映射率: {mapped/total*100:.1f}%")
        
        # 3. 市场类型统计
        cursor.execute("SELECT COUNT(*) as a_stocks FROM stock_industry_mapping WHERE LENGTH(stock_code) = 6")
        a_stocks_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) as hk_stocks FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5")
        hk_stocks_count = cursor.fetchone()[0]
        
        print(f"\n🏦 A股数量: {a_stocks_count}")
        print(f"🇭🇰 港股通数量: {hk_stocks_count}")
        
        # 4. 行业分布TOP10
        print(f"\n🏭 行业分布TOP10:")
        cursor.execute("""
            SELECT industry_name, COUNT(*) as count 
            FROM stock_industry_mapping 
            WHERE industry_name IS NOT NULL AND industry_name != '' 
            GROUP BY industry_name 
            ORDER BY count DESC 
            LIMIT 10
        """)
        top_industries = cursor.fetchall()
        for i, (industry, count) in enumerate(top_industries, 1):
            print(f"  {i:2d}. {industry}: {count}只股票")
        
        # 5. 映射状态统计
        print(f"\n📋 映射状态统计:")
        cursor.execute("""
            SELECT mapping_status, COUNT(*) as count 
            FROM stock_industry_mapping 
            GROUP BY mapping_status
        """)
        statuses = cursor.fetchall()
        for status, count in statuses:
            print(f"  {status}: {count}只股票")
        
        # 6. 置信度分布
        print(f"\n🎯 置信度分布:")
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN confidence >= 0.8 THEN '高置信度(≥0.8)'
                    WHEN confidence >= 0.5 THEN '中置信度(0.5-0.8)'
                    ELSE '低置信度(<0.5)'
                END as confidence_level,
                COUNT(*) as count
            FROM stock_industry_mapping 
            GROUP BY confidence_level
            ORDER BY count DESC
        """)
        confidence_levels = cursor.fetchall()
        for level, count in confidence_levels:
            print(f"  {level}: {count}只股票")
        
        # 7. 最新数据
        print(f"\n🕒 最新数据:")
        cursor.execute("""
            SELECT stock_code, stock_name, industry_name, created_at 
            FROM stock_industry_mapping 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        latest_data = cursor.fetchall()
        for stock_code, stock_name, industry_name, created_at in latest_data:
            print(f"  {stock_code} {stock_name} -> {industry_name} ({created_at})")
        
        print("\n" + "=" * 60)
        print("✅ 数据检查完成！")
        print("🌐 访问 http://127.0.0.1:5001 查看详细数据")
        print("=" * 60)
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        logger.error(f"检查股票数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_stock_data() 