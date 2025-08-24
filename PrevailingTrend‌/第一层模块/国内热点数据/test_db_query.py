"""
测试数据库查询
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import db_manager
from loguru import logger

def test_database_queries():
    """测试数据库查询"""
    print("🧪 测试数据库查询")
    print("=" * 50)
    
    try:
        connection = db_manager.get_connection()
        cursor = connection.cursor()
        
        # 测试平均热度查询
        print("1. 测试平均热度查询:")
        cursor.execute("SELECT AVG(heat_score) as avg_heat FROM l1_domestic_hotspot_data WHERE heat_score IS NOT NULL")
        result = cursor.fetchone()
        print(f"   结果: {result}")
        if result:
            print(f"   平均热度: {result['avg_heat']}")
        
        # 测试平均情感查询
        print("\n2. 测试平均情感查询:")
        cursor.execute("SELECT AVG(sentiment_score) as avg_sentiment FROM l1_domestic_hotspot_data WHERE sentiment_score IS NOT NULL")
        result = cursor.fetchone()
        print(f"   结果: {result}")
        if result:
            print(f"   平均情感: {result['avg_sentiment']}")
        
        # 测试状态统计查询
        print("\n3. 测试状态统计查询:")
        cursor.execute("SELECT status, COUNT(*) as count FROM l1_domestic_hotspot_data GROUP BY status")
        results = cursor.fetchall()
        print(f"   结果: {results}")
        for row in results:
            print(f"   状态 {row['status']}: {row['count']} 条")
        
        # 测试统计函数
        print("\n4. 测试统计函数:")
        stats = db_manager.get_hotspots_statistics()
        print(f"   统计结果: {stats}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        logger.error(f"数据库查询测试失败: {e}")

def main():
    """主函数"""
    test_database_queries()

if __name__ == "__main__":
    main() 