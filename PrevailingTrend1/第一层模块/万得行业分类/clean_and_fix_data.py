import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def clean_and_fix_data():
    """清理重复数据并重新添加正确的股票数据"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 清空现有数据
        print("清空现有股票数据...")
        cursor.execute("DELETE FROM stock_industry_mapping")
        
        # 正确的股票数据（无重复）
        stocks = [
            # A股股票 - 已映射
            ('000001', '平安银行', '100100', '银行', 'confirmed', 1.0),
            ('000002', '万科A', '110100', '房地产开发', 'confirmed', 1.0),
            ('00858', '五粮液', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
            ('600036', '招商银行', '100100', '银行', 'confirmed', 1.0),
            ('600519', '贵州茅台', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
            ('000725', '京东方A', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
            ('002594', '比亚迪', '036000', '汽车制造业', 'confirmed', 1.0),
            ('600030', '中信证券', '100300', '资本市场服务', 'confirmed', 1.0),
            ('002415', '海康威视', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
            ('000063', '中兴通讯', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
            ('000651', '格力电器', '038000', '电气机械和器材制造业', 'confirmed', 1.0),
            ('002304', '洋河股份', '031200', '酒、饮料和精制茶制造业', 'confirmed', 1.0),
            ('600900', '长江电力', '044000', '电力、热力生产和供应业', 'confirmed', 1.0),
            ('000776', '广发证券', '100300', '资本市场服务', 'confirmed', 1.0),
            ('000100', 'TCL科技', '039000', '计算机、通信和其他电子设备制造业', 'confirmed', 1.0),
            
            # A股股票 - 未映射
            ('600887', '伊利股份', '', '', 'pending', 0.0),
            ('300059', '东方财富', '', '', 'pending', 0.0),
            ('300750', '宁德时代', '', '', 'pending', 0.0),
            ('002352', '顺丰控股', '', '', 'pending', 0.0),
            ('000625', '长安汽车', '', '', 'pending', 0.0),
            ('600104', '上汽集团', '', '', 'pending', 0.0),
            ('002736', '国信证券', '', '', 'pending', 0.0),
            ('601318', '中国平安', '', '', 'pending', 0.0),
            ('601601', '中国太保', '', '', 'pending', 0.0),
            ('601336', '新华保险', '', '', 'pending', 0.0),
            ('600276', '恒瑞医药', '', '', 'pending', 0.0),
            ('300015', '爱尔眼科', '', '', 'pending', 0.0),
            ('002007', '华兰生物', '', '', 'pending', 0.0),
            ('000895', '双汇发展', '', '', 'pending', 0.0),
            ('600011', '华能国际', '', '', 'pending', 0.0),
            ('000333', '美的集团', '', '', 'pending', 0.0),
            ('002475', '立讯精密', '', '', 'pending', 0.0),
            
            # 港股通股票 - 已映射
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
            ('00762', '中国联通', '090100', '信息传输服务业', 'confirmed', 1.0),
            ('00823', '领展房产基金', '110100', '房地产开发', 'confirmed', 1.0),
            ('01093', '石药集团', '027000', '医药制造业', 'confirmed', 1.0),
            ('02020', '安踏体育', '032900', '其他制造业', 'confirmed', 1.0),
            ('02331', '李宁', '032900', '其他制造业', 'confirmed', 1.0),
            ('01068', '雨润食品', '031400', '食品制造业', 'confirmed', 1.0),
            ('00857', '中国石油股份', '020000', '采矿业', 'confirmed', 1.0),
            ('00386', '中国石油化工股份', '020000', '采矿业', 'confirmed', 1.0),
            ('00883', '中国海洋石油', '020000', '采矿业', 'confirmed', 1.0),
            
            # 港股通股票 - 未映射
            ('03988', '中国银行', '', '', 'pending', 0.0),
            ('06618', '京东健康', '', '', 'pending', 0.0),
            ('02382', '舜宇光学科技', '', '', 'pending', 0.0),
            ('00939', '建设银行', '', '', 'pending', 0.0),
        ]
        
        print(f"准备插入 {len(stocks)} 条股票数据...")
        
        # 插入股票数据
        for stock in stocks:
            stock_code, stock_name, industry_code, industry_name, mapping_status, confidence = stock
            
            sql = """
            INSERT INTO stock_industry_mapping 
            (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence))
        
        conn.commit()
        print(f"成功插入 {len(stocks)} 条股票数据")
        
        # 验证数据
        cursor.execute("SELECT COUNT(*) as total FROM stock_industry_mapping")
        total = cursor.fetchone()[0]
        print(f"数据库中现有股票总数: {total}")
        
        cursor.execute("SELECT COUNT(*) as mapped FROM stock_industry_mapping WHERE industry_code IS NOT NULL AND industry_code != ''")
        mapped = cursor.fetchone()[0]
        print(f"已映射股票数: {mapped}")
        
        cursor.execute("SELECT COUNT(*) as unmapped FROM stock_industry_mapping WHERE industry_code IS NULL OR industry_code = ''")
        unmapped = cursor.fetchone()[0]
        print(f"未映射股票数: {unmapped}")
        
        # 检查唯一性
        cursor.execute("SELECT COUNT(DISTINCT stock_code) as unique_stocks FROM stock_industry_mapping")
        unique_count = cursor.fetchone()[0]
        print(f"唯一股票数量: {unique_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"清理和修复数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始清理和修复股票数据...")
    success = clean_and_fix_data()
    if success:
        print("股票数据清理和修复完成！")
    else:
        print("股票数据清理和修复失败！") 