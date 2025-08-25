"""
检查数据库结构
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import db_manager
from loguru import logger

def check_database_structure():
    """检查数据库表结构"""
    print("🔍 检查数据库表结构")
    print("=" * 50)
    
    try:
        connection = db_manager.get_connection()
        cursor = connection.cursor()
        
        # 检查表是否存在
        cursor.execute("SHOW TABLES LIKE 'l1_domestic_hotspot_data'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ 表 l1_domestic_hotspot_data 不存在")
            return
        
        print("✅ 表 l1_domestic_hotspot_data 存在")
        
        # 检查表结构
        cursor.execute("DESCRIBE l1_domestic_hotspot_data")
        columns = cursor.fetchall()
        
        print("\n📋 表结构:")
        print("-" * 80)
        print(f"{'字段名':<20} {'类型':<20} {'是否为空':<10} {'键':<10} {'默认值':<10}")
        print("-" * 80)
        
        for column in columns:
            field = column['Field']
            field_type = column['Type']
            null = column['Null']
            key = column['Key']
            default = column['Default'] or 'NULL'
            print(f"{field:<20} {field_type:<20} {null:<10} {key:<10} {default:<10}")
        
        # 检查数据量
        cursor.execute("SELECT COUNT(*) as total FROM l1_domestic_hotspot_data")
        total = cursor.fetchone()['total']
        print(f"\n📊 数据量: {total} 条")
        
        # 检查热度字段的样本数据
        cursor.execute("SELECT heat_score, sentiment_score FROM l1_domestic_hotspot_data LIMIT 5")
        samples = cursor.fetchall()
        
        print(f"\n🔥 热度字段样本数据:")
        for i, sample in enumerate(samples, 1):
            heat_score = sample['heat_score']
            sentiment_score = sample['sentiment_score']
            print(f"  {i}. heat_score: {heat_score}, sentiment_score: {sentiment_score}")
        
        # 检查热度字段的统计
        cursor.execute("SELECT MIN(heat_score) as min_heat, MAX(heat_score) as max_heat, AVG(heat_score) as avg_heat FROM l1_domestic_hotspot_data WHERE heat_score IS NOT NULL")
        heat_stats = cursor.fetchone()
        
        print(f"\n📈 热度字段统计:")
        print(f"  最小值: {heat_stats['min_heat']}")
        print(f"  最大值: {heat_stats['max_heat']}")
        print(f"  平均值: {heat_stats['avg_heat']}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        logger.error(f"数据库结构检查失败: {e}")

def main():
    """主函数"""
    check_database_structure()

if __name__ == "__main__":
    main() 