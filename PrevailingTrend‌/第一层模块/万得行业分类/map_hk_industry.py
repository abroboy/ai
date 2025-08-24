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

def get_industry_mapping():
    """基于股票名称的行业映射规则"""
    return {
        # 银行金融
        '银行': 'BK0475',
        '保险': 'BK0474', 
        '证券': 'BK0473',
        '金融': 'BK0738',
        
        # 科技
        '科技': 'BK0737',
        '软件': 'BK0737',
        '半导体': 'BK1036',
        '通讯': 'BK0448',
        '电子': 'BK0459',
        '数码': 'BK1037',
        '网络': 'BK0447',
        '互联网': 'BK0447',
        
        # 汽车
        '汽车': 'BK1029',
        '车': 'BK1029',
        
        # 地产
        '地产': 'BK0451',
        '物业': 'BK1045',
        '建设': 'BK0425',
        '建筑': 'BK0720',
        
        # 医药
        '医药': 'BK0465',
        '医疗': 'BK0727',
        '药业': 'BK0465',
        '生物': 'BK1044',
        '健康': 'BK0727',
        
        # 消费
        '食品': 'BK0438',
        '饮料': 'BK0438',
        '服装': 'BK0436',
        '零售': 'BK0482',
        '商贸': 'BK0484',
        '百货': 'BK0482',
        
        # 能源
        '石油': 'BK0464',
        '煤炭': 'BK0437',
        '电力': 'BK0428',
        '能源': 'BK1015',
        '燃气': 'BK1028',
        
        # 制造业
        '制造': 'BK0910',
        '机械': 'BK0739',
        '设备': 'BK0545',
        '工程': 'BK0425',
        '材料': 'BK1020',
        '化工': 'BK0538',
        '钢铁': 'BK0479',
        '有色': 'BK0478',
        
        # 交通运输
        '航空': 'BK0420',
        '港口': 'BK0450',
        '物流': 'BK0422',
        '运输': 'BK0450',
        '船舶': 'BK0729',
        
        # 公用事业
        '电信': 'BK0736',
        '公用': 'BK0427',
        '水务': 'BK0427',
        
        # 传媒娱乐
        '传媒': 'BK0486',
        '文化': 'BK0486',
        '游戏': 'BK1046',
        '娱乐': 'BK0485',
        '旅游': 'BK0485',
        
        # 农业
        '农业': 'BK0433',
        '农牧': 'BK0433',
        '渔业': 'BK0433',
    }

def get_industry_names():
    """行业代码对应的中文名称"""
    return {
        'BK0475': '银行',
        'BK0474': '保险',
        'BK0473': '证券',
        'BK0738': '多元金融',
        'BK0737': '软件开发',
        'BK1036': '半导体',
        'BK0448': '通信设备',
        'BK0459': '电子元件',
        'BK1037': '消费电子',
        'BK0447': '互联网服务',
        'BK1029': '汽车整车',
        'BK0451': '房地产开发',
        'BK1045': '房地产服务',
        'BK0425': '工程建设',
        'BK0720': '建筑装饰',
        'BK0465': '化学制药',
        'BK0727': '医疗服务',
        'BK1044': '生物制品',
        'BK0438': '食品饮料',
        'BK0436': '纺织服装',
        'BK0482': '商业百货',
        'BK0484': '贸易行业',
        'BK0464': '石油行业',
        'BK0437': '煤炭行业',
        'BK0428': '电力行业',
        'BK1015': '能源金属',
        'BK1028': '燃气',
        'BK0910': '专用设备',
        'BK0739': '工程机械',
        'BK0545': '通用设备',
        'BK1020': '非金属材料',
        'BK0538': '化学制品',
        'BK0479': '钢铁行业',
        'BK0478': '有色金属',
        'BK0420': '航空机场',
        'BK0450': '航运港口',
        'BK0422': '物流行业',
        'BK0729': '船舶制造',
        'BK0736': '通信服务',
        'BK0427': '公用事业',
        'BK0486': '文化传媒',
        'BK1046': '游戏',
        'BK0485': '旅游酒店',
        'BK0433': '农牧饲渔',
    }

def map_hk_industries():
    """为港股映射行业"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 获取港股列表（长度为5的股票代码）
        cursor.execute("SELECT stock_code, stock_name FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5")
        hk_stocks = cursor.fetchall()
        
        print(f"找到 {len(hk_stocks)} 只港股需要映射行业")
        
        industry_mapping = get_industry_mapping()
        industry_names = get_industry_names()
        
        mapped_count = 0
        
        for stock_code, stock_name in hk_stocks:
            matched_industry = None
            matched_keyword = None
            
            # 遍历所有关键词，寻找匹配
            for keyword, industry_code in industry_mapping.items():
                if keyword in stock_name:
                    matched_industry = industry_code
                    matched_keyword = keyword
                    break
            
            if matched_industry:
                industry_name = industry_names.get(matched_industry, '未知行业')
                
                # 更新数据库
                sql = """
                UPDATE stock_industry_mapping 
                SET industry_code = %s, industry_name = %s, mapping_status = 'auto_mapped', confidence = 0.8
                WHERE stock_code = %s
                """
                cursor.execute(sql, (matched_industry, industry_name, stock_code))
                mapped_count += 1
                
                print(f"✅ {stock_code} {stock_name} -> {industry_name} (关键词: {matched_keyword})")
        
        connection.commit()
        
        # 统计结果
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5 AND industry_name != ''")
        hk_mapped = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5")
        hk_total = cursor.fetchone()[0]
        
        print(f"\n📊 港股行业映射结果:")
        print(f"   - 总港股数: {hk_total}")
        print(f"   - 已映射: {hk_mapped}")
        print(f"   - 本次映射: {mapped_count}")
        print(f"   - 映射率: {hk_mapped/hk_total*100:.1f}%")
        
        # 显示港股行业分布
        cursor.execute("""
            SELECT industry_name, COUNT(*) as count 
            FROM stock_industry_mapping 
            WHERE LENGTH(stock_code) = 5 AND industry_name != '' 
            GROUP BY industry_name 
            ORDER BY count DESC 
            LIMIT 10
        """)
        industries = cursor.fetchall()
        
        if industries:
            print(f"\n🏭 港股行业分布TOP10:")
            for industry, count in industries:
                print(f"   {industry}: {count}只股票")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 映射失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🇭🇰 开始为港股映射行业")
    print("=" * 60)
    
    if map_hk_industries():
        print("\n" + "=" * 60)
        print("✅ 港股行业映射完成！")
        print("🌐 访问 http://127.0.0.1:5001 查看数据")
        print("=" * 60)
    else:
        print("❌ 港股行业映射失败！")

if __name__ == "__main__":
    main() 