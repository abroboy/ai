#!/usr/bin/env java3
"""
扩展股票数据生成脚本
快速生成200+只股票数据
"""

import pymysql
import random
from datetime import datetime

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def generate_more_stocks():
    """生成200+只股票数据"""
    print("开始生成200+只股票数据...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 清理现有数据
        cursor.execute("DELETE FROM l1_wind_stock_mapping")
        cursor.execute("ALTER TABLE l1_wind_stock_mapping AUTO_INCREMENT = 1")
        
        # 行业映射
        industries = [
            ('480100', '银行'),
            ('610300', '白酒'),
            ('360100', '半导体'),
            ('420000', '交通运输'),
            ('430100', '房地产开发'),
            ('610000', '食品饮料'),
            ('270200', '通用机械'),
            ('280100', '电机'),
            ('330100', '白色家电'),
            ('490000', '非银金融'),
            ('240000', '建筑材料'),
            ('230000', '基础化工'),
            ('210000', '有色金属'),
            ('410100', '电力'),
            ('620000', '纺织服装'),
            ('460000', '休闲服务'),
            ('720000', '传媒'),
            ('450000', '商业贸易')
        ]
        
        # 股票前缀
        prefixes = ['000', '002', '300', '600', '601', '603', '688', '301']
        market_types = ['A股', 'A股', 'A股', 'A股', '科创板']
        
        # 基础股票数据
        base_stocks = [
            ('000001', '平安银行', '480100', '银行'),
            ('000002', '万科A', '430100', '房地产开发'),
            ('000858', '五粮液', '610300', '白酒'),
            ('002415', '海康威视', '360100', '半导体'),
            ('300059', '东方财富', '490000', '非银金融'),
            ('600519', '贵州茅台', '610300', '白酒'),
            ('600036', '招商银行', '480100', '银行'),
            ('000725', '京东方A', '360100', '半导体'),
            ('002594', '比亚迪', '420000', '交通运输'),
            ('300750', '宁德时代', '280100', '电机'),
        ]
        
        stock_data = []
        
        # 添加基础股票
        for stock_code, stock_name, industry_code, industry_name in base_stocks:
            market_type = '科创板' if stock_code.startswith('688') else 'A股'
            total_market_value = random.randint(50000, 2000000)
            daily_net_inflow = random.uniform(-50000, 50000)
            net_inflow_ratio = random.uniform(-5.0, 6.0)
            recent_volatility = random.uniform(0.01, 0.08)
            latest_7d_inflow = daily_net_inflow * 7 + random.uniform(-100000, 100000)
            
            stock_data.append((
                stock_code, stock_name, market_type, industry_code, industry_name, '已映射',
                total_market_value, round(daily_net_inflow, 2), round(net_inflow_ratio, 2),
                round(recent_volatility, 4), round(latest_7d_inflow, 2), '正常'
            ))
        
        # 生成190只额外股票
        used_codes = set([stock[0] for stock in base_stocks])
        
        for i in range(190):
            # 生成唯一的股票代码
            while True:
                prefix = random.choice(prefixes)
                number = str(random.randint(100, 999))
                stock_code = prefix + number
                if stock_code not in used_codes:
                    used_codes.add(stock_code)
                    break
            
            # 随机选择行业
            industry_code, industry_name = random.choice(industries)
            
            # 生成股票名称
            company_suffixes = ['科技', '股份', '集团', '有限', '控股', '实业', '发展', '投资', '电子', '材料', '制造', '能源', '环保', '生物', '医药', '食品', '服装', '贸易', '地产', '银行']
            company_prefixes = ['华为', '中兴', '海尔', '美的', '格力', '万科', '招商', '平安', '工商', '建设', '中国', '北京', '上海', '深圳', '广州', '杭州', '苏州', '南京', '青岛', '大连']
            stock_name = random.choice(company_prefixes) + random.choice(company_suffixes)
            
            # 确定市场类型
            if stock_code.startswith('688') or stock_code.startswith('301'):
                market_type = '科创板'
            else:
                market_type = 'A股'
            
            # 生成随机财务数据
            total_market_value = random.randint(30000, 1500000)
            daily_net_inflow = random.uniform(-40000, 40000)
            net_inflow_ratio = random.uniform(-4.0, 5.0)
            recent_volatility = random.uniform(0.01, 0.08)
            latest_7d_inflow = daily_net_inflow * 7 + random.uniform(-80000, 80000)
            
            stock_data.append((
                stock_code, stock_name, market_type, industry_code, industry_name, '已映射',
                total_market_value, round(daily_net_inflow, 2), round(net_inflow_ratio, 2),
                round(recent_volatility, 4), round(latest_7d_inflow, 2), '正常'
            ))
        
        # 插入数据
        insert_sql = """
        INSERT INTO l1_wind_stock_mapping 
        (stock_code, stock_name, market_type, industry_code, industry_name, mapping_status, 
         total_market_value, daily_net_inflow, net_inflow_ratio, recent_volatility, 
         latest_7d_inflow, operation_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(insert_sql, stock_data)
        connection.commit()
        
        print(f"✅ 成功生成 {len(stock_data)} 只股票数据")
        
        # 显示统计信息
        cursor.execute("SELECT market_type, COUNT(*) FROM l1_wind_stock_mapping GROUP BY market_type")
        market_stats = cursor.fetchall()
        for market, count in market_stats:
            print(f"  {market}: {count} 只股票")
            
        cursor.execute("SELECT industry_name, COUNT(*) FROM l1_wind_stock_mapping GROUP BY industry_name ORDER BY COUNT(*) DESC LIMIT 10")
        industry_stats = cursor.fetchall()
        print("\n热门行业 (前10):")
        for industry, count in industry_stats:
            print(f"  {industry}: {count} 只股票")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"✗ 生成股票数据失败: {e}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("万得行业分类模块 - 扩展股票数据生成")
    print("="*60)
    
    success = generate_more_stocks()
    
    if success:
        print("\n✅ 股票数据扩展完成！")
        print("\n接下来可以:")
        print("1. 启动API服务器: java RealTimeDataService")
        print("2. 测试数据接口: http://localhost:5001/api/stock-mappings")
    else:
        print("✗ 股票数据扩展失败")

if __name__ == "__main__":
    main()