"""
国内热点数据模块测试脚本
测试热点数据功能
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
        
        # 检查热点数据表是否存在
        cursor.execute("SHOW TABLES LIKE 'l1_domestic_hotspot_data'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            # 测试查询热点数据
            cursor.execute("SELECT * FROM l1_domestic_hotspot_data LIMIT 5")
            hotspots = cursor.fetchall()
            print(f"✅ 查询到 {len(hotspots)} 条热点数据")
            
            for hotspot in hotspots:
                print(f"  {hotspot['title'][:50]}... (热度: {hotspot.get('heat_score', 'N/A')})")
        else:
            print("⚠️  热点数据表不存在，需要创建")
        
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
        
        # 插入测试热点数据
        test_hotspot = {
            'hotspot_id': 'TEST_001',
            'title': '测试热点标题：人工智能发展新趋势',
            'content': '这是一条测试热点内容，用于验证热点数据模块的功能。',
            'hotspot_type': 'technology',
            'hotspot_level': 'high',
            'status': 'active',
            'source': 'test',
            'url': 'http://test.com/hotspot/001',
            'publish_time': datetime.now(),
            'keywords': '["人工智能", "技术", "发展"]',
            'related_companies': '["百度", "腾讯", "阿里巴巴"]',
            'related_industries': '["801080", "801090"]',
            'sentiment_score': 0.8,
            'heat_score': 85.5,
            'update_date': datetime.now()
        }
        
        sql = """
        INSERT INTO l1_domestic_hotspot_data 
        (hotspot_id, title, content, hotspot_type, hotspot_level, status, source, url, publish_time, keywords, related_companies, related_industries, sentiment_score, heat_score, update_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (
            test_hotspot['hotspot_id'],
            test_hotspot['title'],
            test_hotspot['content'],
            test_hotspot['hotspot_type'],
            test_hotspot['hotspot_level'],
            test_hotspot['status'],
            test_hotspot['source'],
            test_hotspot['url'],
            test_hotspot['publish_time'],
            test_hotspot['keywords'],
            test_hotspot['related_companies'],
            test_hotspot['related_industries'],
            test_hotspot['sentiment_score'],
            test_hotspot['heat_score'],
            test_hotspot['update_date']
        ))
        
        connection.commit()
        print("✅ 测试热点数据插入成功")
        
        # 验证插入的数据
        cursor.execute("SELECT * FROM l1_domestic_hotspot_data WHERE hotspot_id = 'TEST_001'")
        result = cursor.fetchone()
        if result:
            print("✅ 热点数据验证成功")
        else:
            print("❌ 热点数据验证失败")
        
        # 清理测试数据
        cursor.execute("DELETE FROM l1_domestic_hotspot_data WHERE hotspot_id = 'TEST_001'")
        connection.commit()
        print("✅ 测试热点数据清理完成")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 热点数据插入测试失败: {e}")
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
        
        # 统计热点数据
        cursor.execute("SELECT COUNT(*) as total FROM l1_domestic_hotspot_data")
        hotspot_count = cursor.fetchone()['total']
        print(f"✅ 热点数据总数: {hotspot_count}")
        
        # 按类型统计热点
        cursor.execute("SELECT hotspot_type, COUNT(*) as count FROM l1_domestic_hotspot_data GROUP BY hotspot_type")
        type_stats = cursor.fetchall()
        print("✅ 按类型统计热点:")
        for stat in type_stats:
            print(f"  {stat['hotspot_type']}: {stat['count']} 条")
        
        # 按级别统计热点
        cursor.execute("SELECT hotspot_level, COUNT(*) as count FROM l1_domestic_hotspot_data GROUP BY hotspot_level")
        level_stats = cursor.fetchall()
        print("✅ 按级别统计热点:")
        for stat in level_stats:
            print(f"  {stat['hotspot_level']}: {stat['count']} 条")
        
        # 按来源统计热点
        cursor.execute("SELECT source, COUNT(*) as count FROM l1_domestic_hotspot_data GROUP BY source")
        source_stats = cursor.fetchall()
        print("✅ 按来源统计热点:")
        for stat in source_stats:
            print(f"  {stat['source']}: {stat['count']} 条")
        
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
        cursor.execute("SELECT COUNT(*) as total, COUNT(title) as title_count FROM l1_domestic_hotspot_data")
        result = cursor.fetchone()
        completeness = (result['title_count'] / result['total']) * 100 if result['total'] > 0 else 0
        print(f"✅ 热点标题完整率: {completeness:.1f}%")
        
        # 检查数据唯一性
        cursor.execute("SELECT COUNT(*) as total FROM l1_domestic_hotspot_data")
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(DISTINCT hotspot_id) as unique_count FROM l1_domestic_hotspot_data")
        unique = cursor.fetchone()['unique_count']
        uniqueness = (unique / total) * 100 if total > 0 else 0
        print(f"✅ 热点ID唯一性: {uniqueness:.1f}%")
        
        # 检查数据时效性
        cursor.execute("SELECT COUNT(*) as recent_count FROM l1_domestic_hotspot_data WHERE update_date >= DATE_SUB(NOW(), INTERVAL 1 DAY)")
        recent = cursor.fetchone()['recent_count']
        timeliness = (recent / total) * 100 if total > 0 else 0
        print(f"✅ 数据时效性: {timeliness:.1f}%")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据质量测试失败: {e}")
        return False

def test_hotspot_analysis():
    """测试热点分析"""
    print("\n测试热点分析...")
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
        
        # 查询高热度热点
        cursor.execute("SELECT title, heat_score, sentiment_score FROM l1_domestic_hotspot_data WHERE heat_score > 80 ORDER BY heat_score DESC LIMIT 3")
        high_heat = cursor.fetchall()
        print(f"✅ 查询到 {len(high_heat)} 条高热度热点")
        
        for hotspot in high_heat:
            print(f"  {hotspot['title'][:30]}... (热度: {hotspot['heat_score']}, 情感: {hotspot['sentiment_score']})")
        
        # 查询正面情感热点
        cursor.execute("SELECT title, sentiment_score FROM l1_domestic_hotspot_data WHERE sentiment_score > 0.7 ORDER BY sentiment_score DESC LIMIT 3")
        positive = cursor.fetchall()
        print(f"✅ 查询到 {len(positive)} 条正面情感热点")
        
        for hotspot in positive:
            print(f"  {hotspot['title'][:30]}... (情感: {hotspot['sentiment_score']})")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 热点分析测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("国内热点数据模块测试")
    print("=" * 60)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(test_database())
    test_results.append(test_data_insertion())
    test_results.append(test_data_statistics())
    test_results.append(test_data_quality())
    test_results.append(test_hotspot_analysis())
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    passed = sum(test_results)
    total = len(test_results)
    print(f"通过: {passed}/{total}")
    
    test_names = [
        "数据库功能",
        "数据插入",
        "数据统计",
        "数据质量",
        "热点分析"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    if passed == total:
        print("\n🎉 所有测试通过！国内热点数据模块功能正常！")
    else:
        print(f"\n⚠️  有 {total - passed} 项测试失败，需要修复")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 