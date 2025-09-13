#!/usr/bin/env python3
"""
修复数据格式问题并添加测试数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import Database
from datetime import datetime
import json

def add_test_data():
    """添加测试数据"""
    db = Database()
    
    try:
        with db as database:
            # 创建表
            database.create_table()
            
            # 测试数据
            test_hotspots = [
                {
                    'hotspot_id': 'test_001',
                    'title': '美联储宣布加息25个基点',
                    'content': '美联储在最新会议上宣布加息25个基点，这是今年以来的第三次加息。',
                    'hotspot_type': '政策',
                    'region': '美国',
                    'hotspot_level': 'high',
                    'status': 'active',
                    'source': 'Reuters',
                    'url': 'https://www.reuters.com/fed-rate-hike',
                    'publish_time': datetime.now(),
                    'keywords': ['美联储', '加息', '货币政策'],
                    'related_companies': ['Federal Reserve'],
                    'related_industries': ['金融'],
                    'sentiment_score': -0.3,
                    'heat_score': 9.2
                },
                {
                    'hotspot_id': 'test_002',
                    'title': '欧洲央行维持利率不变',
                    'content': '欧洲央行在最新会议上决定维持当前利率水平不变。',
                    'hotspot_type': '政策',
                    'region': '欧洲',
                    'hotspot_level': 'medium',
                    'status': 'active',
                    'source': 'Bloomberg',
                    'url': 'https://www.bloomberg.com/ecb-rate',
                    'publish_time': datetime.now(),
                    'keywords': ['欧洲央行', '利率', '货币政策'],
                    'related_companies': ['European Central Bank'],
                    'related_industries': ['金融'],
                    'sentiment_score': 0.1,
                    'heat_score': 8.5
                },
                {
                    'hotspot_id': 'test_003',
                    'title': '日本经济数据超预期',
                    'content': '日本最新经济数据显示GDP增长超出市场预期。',
                    'hotspot_type': '经济',
                    'region': '日本',
                    'hotspot_level': 'medium',
                    'status': 'active',
                    'source': 'Nikkei',
                    'url': 'https://www.nikkei.com/japan-economy',
                    'publish_time': datetime.now(),
                    'keywords': ['日本', 'GDP', '经济增长'],
                    'related_companies': ['Bank of Japan'],
                    'related_industries': ['经济'],
                    'sentiment_score': 0.6,
                    'heat_score': 7.8
                },
                {
                    'hotspot_id': 'test_004',
                    'title': '英国脱欧后续影响持续',
                    'content': '英国脱欧后的经济影响仍在持续，多个行业受到影响。',
                    'hotspot_type': '社会',
                    'region': '英国',
                    'hotspot_level': 'medium',
                    'status': 'active',
                    'source': 'BBC',
                    'url': 'https://www.bbc.com/brexit-impact',
                    'publish_time': datetime.now(),
                    'keywords': ['英国', '脱欧', '经济影响'],
                    'related_companies': ['UK Government'],
                    'related_industries': ['政治'],
                    'sentiment_score': -0.2,
                    'heat_score': 6.9
                },
                {
                    'hotspot_id': 'test_005',
                    'title': '澳大利亚矿业出口增长',
                    'content': '澳大利亚矿业出口数据显示强劲增长，主要受益于亚洲市场需求。',
                    'hotspot_type': '经济',
                    'region': '澳大利亚',
                    'hotspot_level': 'medium',
                    'status': 'active',
                    'source': 'Sydney Morning Herald',
                    'url': 'https://www.smh.com.au/mining-exports',
                    'publish_time': datetime.now(),
                    'keywords': ['澳大利亚', '矿业', '出口'],
                    'related_companies': ['BHP', 'Rio Tinto'],
                    'related_industries': ['矿业'],
                    'sentiment_score': 0.4,
                    'heat_score': 6.2
                }
            ]
            
            # 插入测试数据
            success_count = 0
            for hotspot in test_hotspots:
                if database.insert_hotspot(hotspot):
                    success_count += 1
                    print(f"✓ 插入成功: {hotspot['title']}")
                else:
                    print(f"✗ 插入失败: {hotspot['title']}")
            
            print(f"\n测试数据插入完成: {success_count}/{len(test_hotspots)}")
            
            # 验证数据
            print("\n验证数据格式:")
            hotspots = database.get_hotspots(5)
            for i, hotspot in enumerate(hotspots, 1):
                print(f"数据 {i}:")
                print(f"  heat_score: {hotspot.get('heat_score')} (类型: {type(hotspot.get('heat_score'))})")
                print(f"  sentiment_score: {hotspot.get('sentiment_score')} (类型: {type(hotspot.get('sentiment_score'))})")
                print()
            
    except Exception as e:
        print(f"添加测试数据失败: {e}")

def fix_data_format():
    """修复数据格式问题"""
    db = Database()
    
    try:
        with db as database:
            # 获取所有数据
            hotspots = database.get_hotspots(1000)
            
            print(f"找到 {len(hotspots)} 条数据")
            
            # 修复数据格式
            fixed_count = 0
            for hotspot in hotspots:
                needs_update = False
                
                # 检查并修复heat_score
                heat_score = hotspot.get('heat_score')
                if heat_score is not None:
                    try:
                        # 如果是字符串，转换为数字
                        if isinstance(heat_score, str):
                            heat_score = float(heat_score)
                            needs_update = True
                        elif isinstance(heat_score, (int, float)):
                            # 确保是数字类型
                            pass
                        else:
                            heat_score = None
                            needs_update = True
                    except (ValueError, TypeError):
                        heat_score = None
                        needs_update = True
                
                # 检查并修复sentiment_score
                sentiment_score = hotspot.get('sentiment_score')
                if sentiment_score is not None:
                    try:
                        # 如果是字符串，转换为数字
                        if isinstance(sentiment_score, str):
                            sentiment_score = float(sentiment_score)
                            needs_update = True
                        elif isinstance(sentiment_score, (int, float)):
                            # 确保是数字类型
                            pass
                        else:
                            sentiment_score = None
                            needs_update = True
                    except (ValueError, TypeError):
                        sentiment_score = None
                        needs_update = True
                
                # 更新数据
                if needs_update:
                    with database.connection.cursor() as cursor:
                        sql = """
                        UPDATE international_hotspot_data 
                        SET heat_score = %s, sentiment_score = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE hotspot_id = %s
                        """
                        cursor.execute(sql, (heat_score, sentiment_score, hotspot['hotspot_id']))
                        fixed_count += 1
            
            print(f"修复了 {fixed_count} 条数据的格式问题")
            
    except Exception as e:
        print(f"修复数据格式失败: {e}")

if __name__ == "__main__":
    print("=== 修复数据格式问题 ===")
    fix_data_format()
    
    print("\n=== 添加测试数据 ===")
    add_test_data()
    
    print("\n完成！") 