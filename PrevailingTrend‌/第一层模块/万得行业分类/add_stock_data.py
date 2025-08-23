"""
添加股票数据到数据库
"""

import pymysql
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

def get_stock_data():
    """获取股票数据"""
    # A股股票数据 - 已映射
    a_stocks_mapped = [
        ('000001', '平安银行', '100100', '银行', 'confirmed', 1.0),
        ('000002', '万科A', '110100', '房地产开发', 'confirmed', 1.0),
        ('000858', '五粮液', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('600036', '招商银行', '100100', '银行', 'confirmed', 1.0),
        ('600519', '贵州茅台', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('000725', '京东方A', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('002594', '比亚迪', '036000', '汽车制造业', 'confirmed', 1.0),
        ('600030', '中信证券', '100300', '资本市场服务', 'confirmed', 1.0),
        ('002415', '海康威视', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('000063', '中兴通讯', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
    ]
    
    # A股股票数据 - 未映射
    a_stocks_unmapped = [
        ('600887', '伊利股份', None, None, 'pending', 0.0),
        ('300059', '东方财富', None, None, 'pending', 0.0),
        ('300750', '宁德时代', None, None, 'pending', 0.0),
        ('002352', '顺丰控股', None, None, 'pending', 0.0),
        ('000100', 'TCL科技', None, None, 'pending', 0.0),
    ]
    
    # 港股通股票数据 - 已映射
    hk_stocks_mapped = [
        ('00700', '腾讯控股', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('00941', '中国移动', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('02318', '中国平安', '100200', '保险业', 'confirmed', 1.0),
        ('01398', '工商银行', '100100', '银行', 'confirmed', 1.0),
        ('00388', '香港交易所', '100300', '资本市场服务', 'confirmed', 1.0),
        ('01024', '快手-W', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('03690', '美团-W', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('09988', '阿里巴巴-SW', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('02269', '药明生物', '027000', '医药制造业', 'confirmed', 1.0),
        ('01810', '小米集团-W', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
    ]
    
    # 港股通股票数据 - 未映射  
    hk_stocks_unmapped = [
        ('03988', '中国银行', None, None, 'pending', 0.0),
        ('02020', '安踏体育', None, None, 'pending', 0.0),
        ('01093', '石药集团', None, None, 'pending', 0.0),
        ('06618', '京东健康', None, None, 'pending', 0.0),
        ('02382', '舜宇光学科技', None, None, 'pending', 0.0),
    ]
    
    return a_stocks_mapped + a_stocks_unmapped + hk_stocks_mapped + hk_stocks_unmapped

def add_stocks_to_database():
    """添加股票数据到数据库"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 清空现有数据
        print("清空现有股票数据...")
        cursor.execute("DELETE FROM stock_industry_mapping")
        
        # 获取股票数据
        stocks = get_stock_data()
        
        print(f"准备插入 {len(stocks)} 条股票数据...")
        
        # 插入股票数据
        for stock in stocks:
            stock_code, stock_name, industry_code, industry_name, mapping_status, confidence = stock
            
            # 处理NULL值，改为空字符串
            if industry_code is None:
                industry_code = ''
            if industry_name is None:
                industry_name = ''
                
            sql = """
            INSERT INTO stock_industry_mapping 
            (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence))
        
        connection.commit()
        print(f"成功插入 {len(stocks)} 条股票数据")
        
        # 验证数据
        cursor.execute("SELECT COUNT(*) as total FROM stock_industry_mapping")
        total = cursor.fetchone()[0]
        print(f"数据库中现有股票总数: {total}")
        
        cursor.execute("SELECT COUNT(*) as mapped FROM stock_industry_mapping WHERE industry_code IS NOT NULL")
        mapped = cursor.fetchone()[0]
        print(f"已映射股票数: {mapped}")
        
        cursor.execute("SELECT COUNT(*) as unmapped FROM stock_industry_mapping WHERE industry_code IS NULL")
        unmapped = cursor.fetchone()[0]
        print(f"未映射股票数: {unmapped}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"添加股票数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始添加股票数据...")
    success = add_stocks_to_database()
    if success:
        print("股票数据添加完成！")
    else:
        print("股票数据添加失败！") 