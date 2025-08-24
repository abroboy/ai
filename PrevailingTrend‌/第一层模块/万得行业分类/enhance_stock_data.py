"""
增强股票数据脚本
添加更多真实的A股和港股通股票数据
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

def get_enhanced_a_stock_data():
    """获取增强的A股股票数据"""
    a_stocks = [
        # 银行股（更多）
        ('600016', '民生银行', '100100', '银行', 'confirmed', 1.0),
        ('601166', '兴业银行', '100100', '银行', 'confirmed', 1.0),
        ('600015', '华夏银行', '100100', '银行', 'confirmed', 1.0),
        ('000001', '平安银行', '100100', '银行', 'confirmed', 1.0),
        ('002142', '宁波银行', '100100', '银行', 'confirmed', 1.0),
        ('601009', '南京银行', '100100', '银行', 'confirmed', 1.0),
        ('600919', '江苏银行', '100100', '银行', 'confirmed', 1.0),
        
        # 房地产开发（更多）
        ('001979', '招商蛇口', '110100', '房地产开发', 'confirmed', 1.0),
        ('600340', '华夏幸福', '110100', '房地产开发', 'confirmed', 1.0),
        ('000069', '华侨城A', '110100', '房地产开发', 'confirmed', 1.0),
        ('600383', '金地集团', '110100', '房地产开发', 'confirmed', 1.0),
        ('000656', '金科股份', '110100', '房地产开发', 'confirmed', 1.0),
        ('600208', '新湖中宝', '110100', '房地产开发', 'confirmed', 1.0),
        
        # 白酒股（更多）
        ('600809', '山西汾酒', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('000596', '古井贡酒', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('600779', '水井坊', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('000799', '酒鬼酒', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('600197', '伊力特', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        
        # 科技股（更多）
        ('002230', '科大讯飞', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('300760', '迈瑞医疗', '027000', '医药制造业', 'confirmed', 1.0),
        ('002008', '大族激光', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('002241', '歌尔股份', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('002049', '紫光国微', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('300782', '卓胜微', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('300661', '圣邦股份', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('300223', '北京君正', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        
        # 汽车股（更多）
        ('000800', '一汽解放', '036000', '汽车制造业', 'confirmed', 1.0),
        ('600066', '宇通客车', '036000', '汽车制造业', 'confirmed', 1.0),
        ('600686', '金龙汽车', '036000', '汽车制造业', 'confirmed', 1.0),
        ('000550', '江铃汽车', '036000', '汽车制造业', 'confirmed', 1.0),
        ('600418', '江淮汽车', '036000', '汽车制造业', 'confirmed', 1.0),
        
        # 证券股（更多）
        ('600837', '海通证券', '100300', '资本市场服务', 'confirmed', 1.0),
        ('000166', '申万宏源', '100300', '资本市场服务', 'confirmed', 1.0),
        ('601688', '华泰证券', '100300', '资本市场服务', 'confirmed', 1.0),
        ('600999', '招商证券', '100300', '资本市场服务', 'confirmed', 1.0),
        ('000783', '长江证券', '100300', '资本市场服务', 'confirmed', 1.0),
        ('002500', '山西证券', '100300', '资本市场服务', 'confirmed', 1.0),
        
        # 保险股（更多）
        ('601628', '中国人寿', '100200', '保险业', 'confirmed', 1.0),
        ('601319', '中国人保', '100200', '保险业', 'confirmed', 1.0),
        ('601236', '红塔证券', '100300', '资本市场服务', 'confirmed', 1.0),
        
        # 医药股（更多）
        ('300122', '智飞生物', '027000', '医药制造业', 'confirmed', 1.0),
        ('600436', '片仔癀', '027000', '医药制造业', 'confirmed', 1.0),
        ('000661', '长春高新', '027000', '医药制造业', 'confirmed', 1.0),
        ('300347', '泰格医药', '027000', '医药制造业', 'confirmed', 1.0),
        ('300601', '康泰生物', '027000', '医药制造业', 'confirmed', 1.0),
        ('300142', '沃森生物', '027000', '医药制造业', 'confirmed', 1.0),
        ('300009', '安科生物', '027000', '医药制造业', 'confirmed', 1.0),
        ('300003', '乐普医疗', '027000', '医药制造业', 'confirmed', 1.0),
        ('300015', '爱尔眼科', '027000', '医药制造业', 'confirmed', 1.0),
        ('300760', '迈瑞医疗', '027000', '医药制造业', 'confirmed', 1.0),
        
        # 消费股（更多）
        ('002027', '分众传媒', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('600690', '海尔智家', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
        ('000858', '五粮液', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('600519', '贵州茅台', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('000568', '泸州老窖', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('002304', '洋河股份', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('600887', '伊利股份', '031400', '食品制造业', 'confirmed', 1.0),
        ('000895', '双汇发展', '031400', '食品制造业', 'confirmed', 1.0),
        ('002352', '顺丰控股', '070000', '交通运输、仓储和邮政业', 'confirmed', 1.0),
        ('600298', '安琪酵母', '031400', '食品制造业', 'confirmed', 1.0),
        ('600132', '重庆啤酒', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        
        # 能源股（更多）
        ('600795', '国电电力', '044000', '电力、热力生产和供应业', 'confirmed', 1.0),
        ('000027', '深圳能源', '044000', '电力、热力生产和供应业', 'confirmed', 1.0),
        ('600886', '国投电力', '044000', '电力、热力生产和供应业', 'confirmed', 1.0),
        ('600021', '上海电力', '044000', '电力、热力生产和供应业', 'confirmed', 1.0),
        ('600027', '华电国际', '044000', '电力、热力生产和供应业', 'confirmed', 1.0),
        ('000539', '粤电力A', '044000', '电力、热力生产和供应业', 'confirmed', 1.0),
        
        # 制造业（更多）
        ('002241', '歌尔股份', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('002008', '大族激光', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('002049', '紫光国微', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('000100', 'TCL科技', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('000651', '格力电器', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
        ('000333', '美的集团', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
        ('002032', '苏泊尔', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
        ('002050', '三花智控', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
        
        # 通信股（更多）
        ('600050', '中国联通', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('000063', '中兴通讯', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('002049', '紫光国微', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('300308', '中际旭创', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('300394', '天孚通信', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        
        # 新能源（新增）
        ('300274', '阳光电源', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
        ('002129', '中环股份', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('300450', '先导智能', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
        ('300316', '晶盛机电', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
        ('002459', '晶澳科技', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('601012', '隆基绿能', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        
        # 半导体（新增）
        ('688981', '中芯国际', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('688012', '中微公司', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('688536', '思瑞浦', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('688396', '华润微', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('688019', '安集科技', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        
        # 未映射的股票（用于测试）
        ('600036', '招商银行', '', '', 'pending', 0.0),
        ('000001', '平安银行', '', '', 'pending', 0.0),
        ('600519', '贵州茅台', '', '', 'pending', 0.0),
        ('000858', '五粮液', '', '', 'pending', 0.0),
        ('002415', '海康威视', '', '', 'pending', 0.0),
        ('300059', '东方财富', '', '', 'pending', 0.0),
        ('300750', '宁德时代', '', '', 'pending', 0.0),
        ('002594', '比亚迪', '', '', 'pending', 0.0),
    ]
    return a_stocks

def get_enhanced_hk_stock_data():
    """获取增强的港股通股票数据"""
    hk_stocks = [
        # 科技股（更多）
        ('02020', '安踏体育', '032900', '其他制造业', 'confirmed', 1.0),
        ('02331', '李宁', '032900', '其他制造业', 'confirmed', 1.0),
        ('01024', '快手-W', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('03690', '美团-W', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('09988', '阿里巴巴-SW', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('01810', '小米集团-W', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('02382', '舜宇光学科技', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
        ('00700', '腾讯控股', '090100', '信息传输服务业', 'confirmed', 1.0),
        
        # 金融股（更多）
        ('01288', '农业银行', '100100', '银行', 'confirmed', 1.0),
        ('03968', '招商银行', '100100', '银行', 'confirmed', 1.0),
        ('01988', '民生银行', '100100', '银行', 'confirmed', 1.0),
        ('00939', '建设银行', '100100', '银行', 'confirmed', 1.0),
        ('03988', '中国银行', '100100', '银行', 'confirmed', 1.0),
        ('01398', '工商银行', '100100', '银行', 'confirmed', 1.0),
        ('02318', '中国平安', '100200', '保险业', 'confirmed', 1.0),
        ('00388', '香港交易所', '100300', '资本市场服务', 'confirmed', 1.0),
        
        # 通信股（更多）
        ('00941', '中国移动', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('00762', '中国联通', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('00823', '领展房产基金', '110100', '房地产开发', 'confirmed', 1.0),
        ('00941', '中国移动', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('00728', '中国电信', '090100', '信息传输服务业', 'confirmed', 1.0),
        
        # 医药股（更多）
        ('06160', '百济神州', '027000', '医药制造业', 'confirmed', 1.0),
        ('01877', '君实生物', '027000', '医药制造业', 'confirmed', 1.0),
        ('02269', '药明生物', '027000', '医药制造业', 'confirmed', 1.0),
        ('01093', '石药集团', '027000', '医药制造业', 'confirmed', 1.0),
        ('06618', '京东健康', '027000', '医药制造业', 'confirmed', 1.0),
        ('01801', '信达生物', '027000', '医药制造业', 'confirmed', 1.0),
        ('09926', '康方生物', '027000', '医药制造业', 'confirmed', 1.0),
        ('09939', '开拓药业', '027000', '医药制造业', 'confirmed', 1.0),
        
        # 消费股（更多）
        ('01068', '雨润食品', '031400', '食品制造业', 'confirmed', 1.0),
        ('00322', '康师傅控股', '031400', '食品制造业', 'confirmed', 1.0),
        ('00291', '华润啤酒', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
        ('01044', '恒安国际', '031400', '食品制造业', 'confirmed', 1.0),
        ('00331', '维他奶国际', '031400', '食品制造业', 'confirmed', 1.0),
        ('00144', '招商局港口', '070000', '交通运输、仓储和邮政业', 'confirmed', 1.0),
        
        # 能源股（更多）
        ('01088', '中国神华', '020000', '采矿业', 'confirmed', 1.0),
        ('00390', '中国中铁', '050000', '建筑业', 'confirmed', 1.0),
        ('00857', '中国石油股份', '020000', '采矿业', 'confirmed', 1.0),
        ('00386', '中国石油化工股份', '020000', '采矿业', 'confirmed', 1.0),
        ('00883', '中国海洋石油', '020000', '采矿业', 'confirmed', 1.0),
        ('01171', '兖州煤业股份', '020000', '采矿业', 'confirmed', 1.0),
        ('01898', '中煤能源', '020000', '采矿业', 'confirmed', 1.0),
        
        # 地产股（更多）
        ('01109', '华润置地', '110100', '房地产开发', 'confirmed', 1.0),
        ('02007', '碧桂园', '110100', '房地产开发', 'confirmed', 1.0),
        ('03333', '中国恒大', '110100', '房地产开发', 'confirmed', 1.0),
        ('06862', '海底捞', '031400', '食品制造业', 'confirmed', 1.0),
        ('01918', '融创中国', '110100', '房地产开发', 'confirmed', 1.0),
        ('00960', '龙湖集团', '110100', '房地产开发', 'confirmed', 1.0),
        
        # 教育股（新增）
        ('09901', '新东方-S', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('01797', '新东方在线', '090100', '信息传输服务业', 'confirmed', 1.0),
        ('06068', '睿见教育', '090100', '信息传输服务业', 'confirmed', 1.0),
        
        # 未映射的股票
        ('00700', '腾讯控股', '', '', 'pending', 0.0),
        ('00941', '中国移动', '', '', 'pending', 0.0),
        ('02318', '中国平安', '', '', 'pending', 0.0),
        ('01398', '工商银行', '', '', 'pending', 0.0),
        ('03988', '中国银行', '', '', 'pending', 0.0),
        ('03690', '美团-W', '', '', 'pending', 0.0),
        ('09988', '阿里巴巴-SW', '', '', 'pending', 0.0),
        ('01810', '小米集团-W', '', '', 'pending', 0.0),
    ]
    return hk_stocks

def enhance_stock_data():
    """增强股票数据"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 获取增强的股票数据
        a_stocks = get_enhanced_a_stock_data()
        hk_stocks = get_enhanced_hk_stock_data()
        all_stocks = a_stocks + hk_stocks
        
        logger.info(f"准备插入 {len(all_stocks)} 条增强股票数据...")
        
        # 插入股票数据
        for stock in all_stocks:
            stock_code, stock_name, industry_code, industry_name, mapping_status, confidence = stock
            
            # 检查是否已存在
            cursor.execute("SELECT id FROM stock_industry_mapping WHERE stock_code = %s", (stock_code,))
            if cursor.fetchone():
                # 更新现有记录
                sql = """
                UPDATE stock_industry_mapping 
                SET stock_name = %s, industry_code = %s, industry_name = %s, 
                    mapping_status = %s, confidence = %s, updated_at = NOW()
                WHERE stock_code = %s
                """
                cursor.execute(sql, (stock_name, industry_code, industry_name, mapping_status, confidence, stock_code))
            else:
                # 插入新记录
                sql = """
                INSERT INTO stock_industry_mapping 
                (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence))
        
        connection.commit()
        logger.info(f"成功处理 {len(all_stocks)} 条股票数据")
        
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
        
        # 按行业统计
        cursor.execute("""
            SELECT industry_name, COUNT(*) as count 
            FROM stock_industry_mapping 
            WHERE industry_name IS NOT NULL AND industry_name != '' 
            GROUP BY industry_name 
            ORDER BY count DESC 
            LIMIT 10
        """)
        top_industries = cursor.fetchall()
        logger.info("行业分布TOP10:")
        for industry, count in top_industries:
            logger.info(f"  {industry}: {count}只股票")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        logger.error(f"增强股票数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始增强股票数据...")
    success = enhance_stock_data()
    if success:
        print("✅ 股票数据增强成功！")
        print("📊 数据统计:")
        print("   - 新增了更多A股和港股通股票")
        print("   - 包含了更多行业分类")
        print("   - 数据已更新到数据库")
        print("🌐 可通过 http://127.0.0.1:5001 查看最新数据")
    else:
        print("❌ 股票数据增强失败！") 