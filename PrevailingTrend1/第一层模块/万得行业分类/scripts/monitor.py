"""
监控脚本
用于监控系统运行状态和数据质量
"""

import sys
import os
import time
import json
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import logger
from utils.database import db_manager
from config import config


class SystemMonitor:
    """系统监控器"""
    
    def __init__(self):
        self.monitoring_data = {}
    
    def check_database_connection(self):
        """检查数据库连接"""
        try:
            db_manager.connect()
            db_manager.disconnect()
            return True, "数据库连接正常"
        except Exception as e:
            return False, f"数据库连接失败: {e}"
    
    def check_api_health(self):
        """检查API健康状态"""
        try:
            import requests
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                return True, "API服务正常"
            else:
                return False, f"API服务异常，状态码: {response.status_code}"
        except Exception as e:
            return False, f"API服务不可用: {e}"
    
    def check_data_freshness(self):
        """检查数据新鲜度"""
        try:
            db_manager.connect()
            
            # 检查行业数据更新时间
            sql = """
            SELECT MAX(update_date) as last_update 
            FROM wind_industry_classification 
            WHERE update_date IS NOT NULL
            """
            result = db_manager.execute_query(sql)
            
            if result and result[0]['last_update']:
                last_update = result[0]['last_update']
                if isinstance(last_update, str):
                    last_update = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
                
                days_since_update = (datetime.now() - last_update).days
                
                if days_since_update <= 1:
                    return True, f"数据新鲜度正常，最后更新: {last_update.strftime('%Y-%m-%d %H:%M:%S')}"
                elif days_since_update <= 3:
                    return False, f"数据较旧，最后更新: {last_update.strftime('%Y-%m-%d %H:%M:%S')}，已过 {days_since_update} 天"
                else:
                    return False, f"数据过旧，最后更新: {last_update.strftime('%Y-%m-%d %H:%M:%S')}，已过 {days_since_update} 天"
            else:
                return False, "未找到数据更新时间"
                
        except Exception as e:
            return False, f"检查数据新鲜度失败: {e}"
        finally:
            db_manager.disconnect()
    
    def check_data_quality(self):
        """检查数据质量"""
        try:
            db_manager.connect()
            
            # 检查行业数据质量
            industry_sql = """
            SELECT 
                COUNT(*) as total_count,
                COUNT(CASE WHEN industry_code IS NULL OR industry_code = '' THEN 1 END) as null_codes,
                COUNT(CASE WHEN industry_name IS NULL OR industry_name = '' THEN 1 END) as null_names,
                COUNT(CASE WHEN industry_level NOT IN (1,2,3) THEN 1 END) as invalid_levels
            FROM wind_industry_classification
            """
            industry_result = db_manager.execute_query(industry_sql)
            
            # 检查股票映射数据质量
            mapping_sql = """
            SELECT 
                COUNT(*) as total_count,
                COUNT(CASE WHEN stock_code IS NULL OR stock_code = '' THEN 1 END) as null_stock_codes,
                COUNT(CASE WHEN industry_code IS NULL OR industry_code = '' THEN 1 END) as null_industry_codes,
                COUNT(CASE WHEN confidence < 0 OR confidence > 1 THEN 1 END) as invalid_confidence,
                AVG(confidence) as avg_confidence
            FROM stock_industry_mapping
            """
            mapping_result = db_manager.execute_query(mapping_sql)
            
            # 分析结果
            industry_data = industry_result[0]
            mapping_data = mapping_result[0]
            
            issues = []
            
            # 行业数据质量检查
            if industry_data['null_codes'] > 0:
                issues.append(f"行业数据中有 {industry_data['null_codes']} 条空行业代码")
            
            if industry_data['null_names'] > 0:
                issues.append(f"行业数据中有 {industry_data['null_names']} 条空行业名称")
            
            if industry_data['invalid_levels'] > 0:
                issues.append(f"行业数据中有 {industry_data['invalid_levels']} 条无效层级")
            
            # 股票映射数据质量检查
            if mapping_data['null_stock_codes'] > 0:
                issues.append(f"股票映射中有 {mapping_data['null_stock_codes']} 条空股票代码")
            
            if mapping_data['null_industry_codes'] > 0:
                issues.append(f"股票映射中有 {mapping_data['null_industry_codes']} 条空行业代码")
            
            if mapping_data['invalid_confidence'] > 0:
                issues.append(f"股票映射中有 {mapping_data['invalid_confidence']} 条无效置信度")
            
            avg_confidence = mapping_data['avg_confidence'] or 0
            if avg_confidence < 0.7:
                issues.append(f"平均置信度过低: {avg_confidence:.2f}")
            
            if issues:
                return False, f"数据质量问题: {'; '.join(issues)}"
            else:
                return True, f"数据质量良好，行业数据: {industry_data['total_count']}条，股票映射: {mapping_data['total_count']}条"
                
        except Exception as e:
            return False, f"检查数据质量失败: {e}"
        finally:
            db_manager.disconnect()
    
    def check_system_performance(self):
        """检查系统性能"""
        try:
            # 检查数据库查询性能
            start_time = time.time()
            db_manager.connect()
            
            # 执行简单查询
            sql = "SELECT COUNT(*) as count FROM wind_industry_classification"
            result = db_manager.execute_query(sql)
            
            query_time = time.time() - start_time
            db_manager.disconnect()
            
            if query_time < 1.0:
                return True, f"系统性能正常，查询耗时: {query_time:.3f}秒"
            elif query_time < 5.0:
                return False, f"系统性能较慢，查询耗时: {query_time:.3f}秒"
            else:
                return False, f"系统性能异常，查询耗时: {query_time:.3f}秒"
                
        except Exception as e:
            return False, f"检查系统性能失败: {e}"
    
    def run_full_monitoring(self):
        """运行完整监控"""
        logger.info("开始系统监控...")
        
        checks = [
            ("数据库连接", self.check_database_connection),
            ("API健康状态", self.check_api_health),
            ("数据新鲜度", self.check_data_freshness),
            ("数据质量", self.check_data_quality),
            ("系统性能", self.check_system_performance),
        ]
        
        results = {}
        all_passed = True
        
        for check_name, check_func in checks:
            try:
                passed, message = check_func()
                results[check_name] = {
                    'status': 'PASS' if passed else 'FAIL',
                    'message': message,
                    'timestamp': datetime.now().isoformat()
                }
                
                if not passed:
                    all_passed = False
                    logger.warning(f"{check_name}: {message}")
                else:
                    logger.info(f"{check_name}: {message}")
                    
            except Exception as e:
                results[check_name] = {
                    'status': 'ERROR',
                    'message': f"监控检查失败: {e}",
                    'timestamp': datetime.now().isoformat()
                }
                all_passed = False
                logger.error(f"{check_name}: 监控检查失败: {e}")
        
        # 保存监控结果
        self.monitoring_data = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'HEALTHY' if all_passed else 'UNHEALTHY',
            'checks': results
        }
        
        # 输出监控报告
        self.print_monitoring_report()
        
        return all_passed
    
    def print_monitoring_report(self):
        """打印监控报告"""
        print("\n" + "="*60)
        print("系统监控报告")
        print("="*60)
        print(f"监控时间: {self.monitoring_data['timestamp']}")
        print(f"整体状态: {self.monitoring_data['overall_status']}")
        print("-"*60)
        
        for check_name, result in self.monitoring_data['checks'].items():
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            print(f"{status_icon} {check_name}: {result['status']}")
            print(f"   消息: {result['message']}")
            print()
        
        print("="*60)
    
    def save_monitoring_report(self, filename=None):
        """保存监控报告"""
        if filename is None:
            filename = f"monitoring_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.monitoring_data, f, ensure_ascii=False, indent=2)
            logger.info(f"监控报告已保存到: {filename}")
        except Exception as e:
            logger.error(f"保存监控报告失败: {e}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='系统监控脚本')
    parser.add_argument('--check', choices=['db', 'api', 'data', 'performance', 'all'], 
                       default='all', help='检查项目')
    parser.add_argument('--save-report', action='store_true', help='保存监控报告')
    parser.add_argument('--continuous', action='store_true', help='持续监控模式')
    parser.add_argument('--interval', type=int, default=300, help='监控间隔（秒）')
    
    args = parser.parse_args()
    
    monitor = SystemMonitor()
    
    try:
        if args.continuous:
            logger.info(f"启动持续监控模式，间隔: {args.interval}秒")
            while True:
                monitor.run_full_monitoring()
                if args.save_report:
                    monitor.save_monitoring_report()
                time.sleep(args.interval)
        else:
            # 单次监控
            if args.check == 'all':
                monitor.run_full_monitoring()
            elif args.check == 'db':
                passed, message = monitor.check_database_connection()
                print(f"数据库连接: {'✅' if passed else '❌'} {message}")
            elif args.check == 'api':
                passed, message = monitor.check_api_health()
                print(f"API健康状态: {'✅' if passed else '❌'} {message}")
            elif args.check == 'data':
                passed, message = monitor.check_data_freshness()
                print(f"数据新鲜度: {'✅' if passed else '❌'} {message}")
                passed, message = monitor.check_data_quality()
                print(f"数据质量: {'✅' if passed else '❌'} {message}")
            elif args.check == 'performance':
                passed, message = monitor.check_system_performance()
                print(f"系统性能: {'✅' if passed else '❌'} {message}")
            
            if args.save_report:
                monitor.save_monitoring_report()
        
    except KeyboardInterrupt:
        logger.info("监控已停止")
    except Exception as e:
        logger.error(f"监控失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 