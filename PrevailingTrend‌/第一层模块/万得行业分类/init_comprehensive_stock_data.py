"""
全面的股票数据初始化脚本
包含真实的A股和港股通股票数据
"""

import pymysql
import logging
from datetime import datetime

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

def get_real_a_stock_data():
    """获取真实的A股股票数据"""
    a_stocks = [
        # 银行股
        ('000001', '平安银行', '100100', '银行', 'confirmed', 1.0),
        ('600036', '招商银行', '100100', '银行', 'confirmed', 1.0),
        ('601398', '工商银行', '100100', '银行', 'confirmed', 1.0),
        ('601939', '建设银行', '100100', '银行', 'confirmed', 1.0),
        ('600000', '浦发银行', '100100', '银行', 'confirmed', 1.0),
        ('601988', '中国银行', '100100', '银行', 'confirmed', 1.0),
        
        # 白酒股
        ('000858', '五粮液', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('600519', '贵州茅台', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('000568', '泸州老窖', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('002304', '洋河股份', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        
        # 科技股
        ('000725', '京东方A', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('002415', '海康威视', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('000063', '中兴通讯', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('002475', '立讯精密', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('300059', '东方财富', '100300', '资本市场服务', 'confirmed', 1.0),
        ('300750', '宁德时代', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
        
        # 汽车股
        ('002594', '比亚迪', '036000', '汽车制造业', 'confirmed', 1.0),
        ('000625', '长安汽车', '036000', '汽车制造业', 'confirmed', 1.0),
        ('600104', '上汽集团', '036000', '汽车制造业', 'confirmed', 1.0),
        
        # 证券股
        ('600030', '中信证券', '100300', '资本市场服务', 'confirmed', 1.0),
        ('000776', '广发证券', '100300', '资本市场服务', 'confirmed', 1.0),
        ('002736', '国信证券', '100300', '资本市场服务', 'confirmed', 1.0),
        
        # 保险股
        ('601318', '中国平安', '100200', '保险业', 'confirmed', 1.0),
        ('601601', '中国太保', '100200', '保险业', 'confirmed', 1.0),
        ('601336', '新华保险', '100200', '保险业', 'confirmed', 1.0),
        
        # 医药股
        ('600276', '恒瑞医药', '027000', '医药制造业', 'confirmed', 1.0),
        ('300015', '爱尔眼科', '027000', '医药制造业', 'confirmed', 1.0),
        ('002007', '华兰生物', '027000', '医药制造业', 'confirmed', 1.0),
        
        # 消费股
        ('600887', '伊利股份', '031400', '食品制造业', 'confirmed', 1.0),
        ('000895', '双汇发展', '031400', '食品制造业', 'confirmed', 1.0),
        ('002352', '顺丰控股', '070000', '交通运输、仓储和邮政业', 'confirmed', 1.0),
        
        # 能源股
        ('600900', '长江电力', '044000', '电力、热力生产和供应业', 'confirmed', 1.0),
        ('600011', '华能国际', '044000', '电力、热力生产和供应业', 'confirmed', 1.0),
        
        # 制造业
        ('000651', '格力电器', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
        ('000333', '美的集团', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
        ('000100', 'TCL科技', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
    ]
    return a_stocks

def get_real_hk_stock_data():
    """获取真实的港股通股票数据"""
    hk_stocks = [
        # 科技股
        ('00700', '腾讯控股', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('01024', '快手-W', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('03690', '美团-W', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('09988', '阿里巴巴-SW', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('01810', '小米集团-W', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('02382', '舜宇光学科技', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        
        # 金融股
        ('02318', '中国平安', '100200', '保险业', 'confirmed', 1.0),
        ('01398', '工商银行', '100100', '银行', 'confirmed', 1.0),
        ('03988', '中国银行', '100100', '银行', 'confirmed', 1.0),
        ('00939', '建设银行', '100100', '银行', 'confirmed', 1.0),
        ('00388', '香港交易所', '100300', '资本市场服务', 'confirmed', 1.0),
        
        # 通信股
        ('00941', '中国移动', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('00762', '中国联通', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('00823', '领展房产基金', '110100', '房地产开发', 'confirmed', 1.0),
        
        # 医药股
        ('02269', '药明生物', '027000', '医药制造业', 'confirmed', 1.0),
        ('01093', '石药集团', '027000', '医药制造业', 'confirmed', 1.0),
        ('06618', '京东健康', '027000', '医药制造业', 'confirmed', 1.0),
        
        # 消费股
        ('02020', '安踏体育', '032900', '其他制造业', 'confirmed', 1.0),
        ('02331', '李宁', '032900', '其他制造业', 'confirmed', 1.0),
        ('01068', '雨润食品', '031400', '食品制造业', 'confirmed', 1.0),
        
        # 能源股
        ('00857', '中国石油股份', '020000', '采矿业', 'confirmed', 1.0),
        ('00386', '中国石油化工股份', '020000', '采矿业', 'confirmed', 1.0),
        ('00883', '中国海洋石油', '020000', '采矿业', 'confirmed', 1.0),
    ]
    return hk_stocks

def initialize_stock_data():
    """初始化股票数据"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 清空现有数据
        logger.info("清空现有股票数据...")
        cursor.execute("DELETE FROM stock_industry_mapping")
        
        # 获取股票数据
        a_stocks = get_real_a_stock_data()
        hk_stocks = get_real_hk_stock_data()
        all_stocks = a_stocks + hk_stocks
        
        logger.info(f"准备插入 {len(all_stocks)} 条股票数据...")
        
        # 插入股票数据
        for stock in all_stocks:
            stock_code, stock_name, industry_code, industry_name, mapping_status, confidence = stock
            
            sql = """
            INSERT INTO stock_industry_mapping 
            (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence))
        
        connection.commit()
        logger.info(f"成功插入 {len(all_stocks)} 条股票数据")
        
        # 验证数据
        cursor.execute("SELECT COUNT(*) as total FROM stock_industry_mapping")
        total = cursor.fetchone()[0]
        logger.info(f"数据库中现有股票总数: {total}")
        
        cursor.execute("SELECT COUNT(*) as mapped FROM stock_industry_mapping WHERE industry_code IS NOT NULL AND industry_code != ''")
        mapped = cursor.fetchone()[0]
        logger.info(f"已映射股票数: {mapped}")
        
        cursor.execute("SELECT COUNT(*) as a_stocks FROM stock_industry_mapping WHERE LENGTH(stock_code) = 6")
        a_stocks_count = cursor.fetchone()[0]
        logger.info(f"A股数量: {a_stocks_count}")
        
        cursor.execute("SELECT COUNT(*) as hk_stocks FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5")
        hk_stocks_count = cursor.fetchone()[0]
        logger.info(f"港股通数量: {hk_stocks_count}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        logger.error(f"初始化股票数据失败: {e}")
        return False

if __name__ == "__main__":
    print("开始初始化股票数据...")
    success = initialize_stock_data()
    if success:
        print("✅ 股票数据初始化成功！")
    else:
        print("❌ 股票数据初始化失败！") 