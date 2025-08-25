import pymysql
import re

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def get_industry_by_name(stock_name):
    """根据股票名称判断行业"""
    # 银行股
    if any(keyword in stock_name for keyword in ['银行', '农商', '农信']):
        return '801780', '银行'
    
    # 证券股
    if any(keyword in stock_name for keyword in ['证券', '券商']):
        return '801790', '非银金融'
    
    # 保险股
    if any(keyword in stock_name for keyword in ['保险', '人寿', '平安', '太保']):
        return '801790', '非银金融'
    
    # 白酒股
    if any(keyword in stock_name for keyword in ['茅台', '五粮液', '泸州', '洋河', '汾酒', '古井', '酒鬼', '伊力特']):
        return '801120', '食品饮料'
    
    # 医药股
    if any(keyword in stock_name for keyword in ['医药', '生物', '制药', '医疗', '健康', '眼科', '牙科', '器械']):
        return '801150', '医药生物'
    
    # 科技股
    if any(keyword in stock_name for keyword in ['科技', '软件', '信息', '数据', '网络', '通信', '电子', '芯片', '半导体']):
        return '801080', '电子'
    
    # 汽车股
    if any(keyword in stock_name for keyword in ['汽车', '比亚迪', '长安', '上汽', '一汽', '解放', '宇通', '金龙']):
        return '801880', '汽车'
    
    # 房地产股
    if any(keyword in stock_name for keyword in ['地产', '房地产', '置业', '开发', '万科', '保利', '招商蛇口']):
        return '801180', '房地产'
    
    # 能源股
    if any(keyword in stock_name for keyword in ['电力', '能源', '石油', '石化', '煤炭', '燃气', '华能', '国电']):
        return '801160', '公用事业'
    
    # 消费股
    if any(keyword in stock_name for keyword in ['伊利', '双汇', '顺丰', '分众', '海尔', '美的', '格力', 'TCL']):
        return '801110', '家用电器'
    
    # 制造业
    if any(keyword in stock_name for keyword in ['制造', '机械', '设备', '工业', '重工', '工程']):
        return '801890', '机械设备'
    
    # 化工股
    if any(keyword in stock_name for keyword in ['化工', '化学', '材料', '塑料', '橡胶']):
        return '801030', '化工'
    
    # 钢铁股
    if any(keyword in stock_name for keyword in ['钢铁', '钢', '铁', '金属']):
        return '801040', '钢铁'
    
    # 有色金属
    if any(keyword in stock_name for keyword in ['有色', '铜', '铝', '锌', '铅', '镍', '稀土']):
        return '801050', '有色金属'
    
    # 建筑材料
    if any(keyword in stock_name for keyword in ['水泥', '建材', '玻璃', '陶瓷']):
        return '801710', '建筑材料'
    
    # 建筑装饰
    if any(keyword in stock_name for keyword in ['建筑', '装饰', '装修', '园林']):
        return '801720', '建筑装饰'
    
    # 电气设备
    if any(keyword in stock_name for keyword in ['电气', '电器', '设备', '仪器', '仪表']):
        return '801730', '电气设备'
    
    # 国防军工
    if any(keyword in stock_name for keyword in ['军工', '国防', '航天', '航空', '船舶']):
        return '801740', '国防军工'
    
    # 计算机
    if any(keyword in stock_name for keyword in ['计算机', '软件', '系统', '技术', '智能']):
        return '801750', '计算机'
    
    # 传媒
    if any(keyword in stock_name for keyword in ['传媒', '文化', '影视', '出版', '广告']):
        return '801760', '传媒'
    
    # 通信
    if any(keyword in stock_name for keyword in ['通信', '联通', '移动', '电信', '网络']):
        return '801770', '通信'
    
    # 交通运输
    if any(keyword in stock_name for keyword in ['交通', '运输', '物流', '港口', '机场', '铁路']):
        return '801170', '交通运输'
    
    # 商业贸易
    if any(keyword in stock_name for keyword in ['商业', '贸易', '零售', '百货', '超市']):
        return '801200', '商业贸易'
    
    # 休闲服务
    if any(keyword in stock_name for keyword in ['旅游', '酒店', '餐饮', '娱乐', '休闲']):
        return '801210', '休闲服务'
    
    # 农林牧渔
    if any(keyword in stock_name for keyword in ['农业', '林业', '牧业', '渔业', '种植', '养殖']):
        return '801010', '农林牧渔'
    
    # 采掘
    if any(keyword in stock_name for keyword in ['矿业', '采掘', '开采', '资源']):
        return '801020', '采掘'
    
    # 纺织服装
    if any(keyword in stock_name for keyword in ['纺织', '服装', '服饰', '鞋帽']):
        return '801130', '纺织服装'
    
    # 轻工制造
    if any(keyword in stock_name for keyword in ['轻工', '造纸', '印刷', '包装']):
        return '801140', '轻工制造'
    
    return '', ''

def map_industries():
    """为股票映射行业"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 获取所有股票
        cursor.execute("SELECT id, stock_code, stock_name FROM stock_industry_mapping")
        stocks = cursor.fetchall()
        
        print(f"开始为 {len(stocks)} 只股票映射行业...")
        
        mapped_count = 0
        for stock_id, stock_code, stock_name in stocks:
            industry_code, industry_name = get_industry_by_name(stock_name)
            
            if industry_code and industry_name:
                # 更新行业信息
                sql = """
                UPDATE stock_industry_mapping 
                SET industry_code = %s, industry_name = %s, mapping_status = 'confirmed', confidence = 1.0
                WHERE id = %s
                """
                cursor.execute(sql, (industry_code, industry_name, stock_id))
                mapped_count += 1
        
        connection.commit()
        
        # 统计
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE industry_name != ''")
        total_mapped = cursor.fetchone()[0]
        
        cursor.execute("SELECT industry_name, COUNT(*) as count FROM stock_industry_mapping WHERE industry_name != '' GROUP BY industry_name ORDER BY count DESC")
        industries = cursor.fetchall()
        
        print(f"✅ 成功映射 {mapped_count} 只股票")
        print(f"📊 总映射数: {total_mapped}")
        print("\n行业分布:")
        for industry, count in industries:
            print(f"  {industry}: {count}只股票")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"映射失败: {e}")
        return False

if __name__ == "__main__":
    print("开始行业映射...")
    if map_industries():
        print("✅ 行业映射完成！")
    else:
        print("❌ 行业映射失败！") 