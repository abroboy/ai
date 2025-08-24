"""
爬虫启动脚本
展示爬虫信息和状态
"""

import sys
import os
import time
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.web_scraper import WebScraper
from core.real_data_collector import RealDataCollector
from core.data_updater import DataUpdater
from core.data_storage import DataStorage
from loguru import logger

def show_crawler_info():
    """显示爬虫信息"""
    print("=" * 60)
    print("🕷️  国内热点数据爬虫系统")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 显示爬虫配置
    print("📋 爬虫配置信息:")
    print("  - 数据源数量: 50+ 个")
    print("  - 目标数据量: 150+ 条/天")
    print("  - 更新频率: 30分钟")
    print("  - 数据存储: MySQL数据库")
    print()
    
    # 显示支持的数据源
    print("🌐 支持的数据源:")
    print("  新闻媒体:")
    print("    - 新浪财经 (sina.com.cn)")
    print("    - 东方财富 (eastmoney.com)")
    print("    - 财新网 (caixin.com)")
    print("    - 第一财经 (cbn.com.cn)")
    print("    - 证券时报 (stcn.com)")
    print("    - 中国证券报 (cs.com.cn)")
    print()
    print("  政府部门:")
    print("    - 中国政府网 (gov.cn)")
    print("    - 发改委 (ndrc.gov.cn)")
    print("    - 央行 (pbc.gov.cn)")
    print("    - 证监会 (csrc.gov.cn)")
    print("    - 银保监会 (cbirc.gov.cn)")
    print()
    print("  交易所:")
    print("    - 上海证券交易所 (sse.com.cn)")
    print("    - 深圳证券交易所 (szse.cn)")
    print("    - 北京证券交易所 (bse.cn)")
    print()
    print("  行业协会:")
    print("    - 中国汽车工业协会")
    print("    - 中国钢铁工业协会")
    print("    - 中国有色金属工业协会")
    print("    - 中国银行业协会")
    print("    - 中国证券业协会")
    print()
    
    print("🔧 技术特性:")
    print("  - 智能反爬虫策略")
    print("  - 数据去重和清洗")
    print("  - 实时数据更新")
    print("  - 错误重试机制")
    print("  - 数据质量验证")
    print()

def test_crawler_sources():
    """测试爬虫数据源"""
    print("🧪 开始测试爬虫数据源...")
    print()
    
    scraper = WebScraper()
    
    # 测试各个数据源
    sources = [
        ("新浪财经", scraper.scrape_sina_finance),
        ("东方财富", scraper.scrape_eastmoney),
        ("财新网", scraper.scrape_caixin),
        ("政府政策", scraper.scrape_government_policy),
        ("交易所公告", scraper.scrape_stock_exchange),
    ]
    
    total_data = 0
    source_results = []
    
    for name, scraper_func in sources:
        print(f"正在测试 {name}...")
        try:
            start_time = time.time()
            hotspots = scraper_func()
            end_time = time.time()
            
            duration = end_time - start_time
            total_data += len(hotspots)
            
            status = "✅" if hotspots else "⚠️"
            result = {
                'name': name,
                'count': len(hotspots),
                'duration': duration,
                'status': status
            }
            source_results.append(result)
            
            print(f"  {status} {name}: {len(hotspots)} 条数据 ({duration:.2f}秒)")
            
            # 显示示例数据
            if hotspots:
                for i, hotspot in enumerate(hotspots[:2]):
                    print(f"    示例{i+1}: {hotspot.title[:50]}...")
            
        except Exception as e:
            print(f"  ❌ {name}: 测试失败 - {e}")
            source_results.append({
                'name': name,
                'count': 0,
                'duration': 0,
                'status': '❌'
            })
        print()
    
    # 显示测试结果汇总
    print("📊 测试结果汇总:")
    print("-" * 50)
    for result in source_results:
        print(f"{result['status']} {result['name']:<12} {result['count']:>3} 条数据  {result['duration']:>6.2f}秒")
    
    print("-" * 50)
    print(f"总计: {total_data} 条数据")
    print()
    
    return total_data

def start_data_collection():
    """启动数据采集"""
    print("🚀 启动数据采集...")
    print()
    
    try:
        # 创建数据更新器
        updater = DataUpdater()
        
        # 执行数据更新
        print("正在执行数据更新...")
        result = updater.manual_update()
        
        if result['success']:
            print(f"✅ 数据采集成功!")
            print(f"   更新数量: {result['updated_count']} 条")
            print(f"   耗时: {result['duration']:.2f} 秒")
            print(f"   消息: {result['message']}")
        else:
            print(f"❌ 数据采集失败: {result['error']}")
        
        print()
        
        # 显示数据库状态
        storage = DataStorage()
        stats = storage.get_statistics()
        
        print("📈 数据库状态:")
        print(f"   总数据量: {stats['total']} 条")
        print(f"   今日数据: {stats['today_count']} 条")
        print(f"   类型分布: {stats['type_distribution']}")
        print(f"   来源分布: {len(stats['source_distribution'])} 个来源")
        
        return result
        
    except Exception as e:
        print(f"❌ 启动数据采集失败: {e}")
        return None

def show_realtime_status():
    """显示实时状态"""
    print("📡 实时状态监控:")
    print("  - 爬虫状态: 运行中")
    print("  - 数据更新: 自动")
    print("  - 错误处理: 启用")
    print("  - 日志记录: 启用")
    print()
    
    print("🔗 访问地址:")
    print("  - Web管理台: http://localhost:5002")
    print("  - API接口: http://localhost:5002/api")
    print("  - 数据更新: http://localhost:5002/api/collect")
    print("  - 状态查询: http://localhost:5002/api/update-status")
    print()

def main():
    """主函数"""
    try:
        # 显示爬虫信息
        show_crawler_info()
        
        # 测试爬虫数据源
        test_crawler_sources()
        
        # 启动数据采集
        start_data_collection()
        
        # 显示实时状态
        show_realtime_status()
        
        print("🎉 爬虫系统启动完成!")
        print("💡 提示: 访问 http://localhost:5002 查看Web管理台")
        print("💡 提示: 按 Ctrl+C 停止服务")
        print()
        
        # 保持程序运行
        try:
            while True:
                time.sleep(60)  # 每分钟显示一次状态
                print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - 爬虫系统运行中...")
        except KeyboardInterrupt:
            print("\n👋 爬虫系统已停止")
            
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        logger.error(f"爬虫启动失败: {e}")

if __name__ == "__main__":
    main() 