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

def get_enhanced_industry_mapping():
    """增强的行业映射规则"""
    return {
        # 银行金融
        '银行': 'BK0475',
        '保险': 'BK0474', 
        '证券': 'BK0473',
        '金融': 'BK0738',
        '信托': 'BK0738',
        '投资': 'BK0738',
        '基金': 'BK0738',
        
        # 科技
        '科技': 'BK0737',
        '软件': 'BK0737',
        '半导体': 'BK1036',
        '芯片': 'BK1036',
        '通讯': 'BK0448',
        '通信': 'BK0448',
        '电子': 'BK0459',
        '数码': 'BK1037',
        '网络': 'BK0447',
        '互联网': 'BK0447',
        '智能': 'BK0737',
        '数据': 'BK0737',
        '信息': 'BK0737',
        '系统': 'BK0737',
        '平台': 'BK0447',
        '在线': 'BK0447',
        '数字': 'BK0737',
        '云': 'BK0737',
        'AI': 'BK0737',
        '人工智能': 'BK0737',
        '区块链': 'BK0737',
        '元宇宙': 'BK0737',
        
        # 汽车
        '汽车': 'BK1029',
        '车': 'BK1029',
        '新能源': 'BK1033',
        '电池': 'BK1033',
        '充电': 'BK1033',
        '电动': 'BK1033',
        
        # 地产
        '地产': 'BK0451',
        '物业': 'BK1045',
        '建设': 'BK0425',
        '建筑': 'BK0720',
        '房地产': 'BK0451',
        '置业': 'BK0451',
        '开发': 'BK0451',
        '投资': 'BK0738',
        
        # 医药
        '医药': 'BK0465',
        '医疗': 'BK0727',
        '药业': 'BK0465',
        '生物': 'BK1044',
        '健康': 'BK0727',
        '制药': 'BK0465',
        '器械': 'BK1041',
        '诊断': 'BK0727',
        '基因': 'BK1044',
        '疫苗': 'BK1044',
        '抗体': 'BK1044',
        '细胞': 'BK1044',
        '肿瘤': 'BK0465',
        '癌症': 'BK0465',
        '康复': 'BK0727',
        '护理': 'BK0727',
        '诊所': 'BK0727',
        '医院': 'BK0727',
        
        # 消费
        '食品': 'BK0438',
        '饮料': 'BK0438',
        '服装': 'BK0436',
        '零售': 'BK0482',
        '商贸': 'BK0484',
        '百货': 'BK0482',
        '超市': 'BK0482',
        '购物': 'BK0482',
        '连锁': 'BK0482',
        '品牌': 'BK0436',
        '时尚': 'BK0436',
        '美妆': 'BK1035',
        '美容': 'BK1035',
        '护肤': 'BK1035',
        '化妆品': 'BK1035',
        '奢侈品': 'BK0436',
        '珠宝': 'BK0734',
        '黄金': 'BK0732',
        '钻石': 'BK0734',
        '手表': 'BK0436',
        '酒': 'BK0438',
        '啤酒': 'BK0438',
        '白酒': 'BK0438',
        '红酒': 'BK0438',
        '烟草': 'BK0438',
        
        # 能源
        '石油': 'BK0464',
        '煤炭': 'BK0437',
        '电力': 'BK0428',
        '能源': 'BK1015',
        '燃气': 'BK1028',
        '新能源': 'BK1033',
        '太阳能': 'BK1031',
        '光伏': 'BK1031',
        '风电': 'BK1032',
        '核电': 'BK0428',
        '水电': 'BK0428',
        '火电': 'BK0428',
        '天然气': 'BK1028',
        '液化气': 'BK1028',
        '油气': 'BK0464',
        '勘探': 'BK1017',
        '开采': 'BK1017',
        '矿业': 'BK1017',
        '金属': 'BK0478',
        '有色金属': 'BK0478',
        '钢铁': 'BK0479',
        '铝': 'BK0478',
        '铜': 'BK0478',
        '锌': 'BK0478',
        '镍': 'BK0478',
        '锂': 'BK1015',
        '稀土': 'BK1015',
        '小金属': 'BK1027',
        
        # 制造业
        '制造': 'BK0910',
        '机械': 'BK0739',
        '设备': 'BK0545',
        '工程': 'BK0425',
        '材料': 'BK1020',
        '化工': 'BK0538',
        '化学': 'BK0538',
        '塑料': 'BK0454',
        '橡胶': 'BK1018',
        '玻璃': 'BK0546',
        '水泥': 'BK0424',
        '建材': 'BK0476',
        '装饰': 'BK0725',
        '装修': 'BK0725',
        '家具': 'BK0440',
        '家电': 'BK0456',
        '电器': 'BK0456',
        '空调': 'BK0456',
        '冰箱': 'BK0456',
        '洗衣机': 'BK0456',
        '电视': 'BK0456',
        '手机': 'BK1037',
        '电脑': 'BK0735',
        '笔记本': 'BK0735',
        '服务器': 'BK0735',
        '芯片': 'BK1036',
        '电路': 'BK0459',
        '元件': 'BK0459',
        '器件': 'BK0459',
        '传感器': 'BK0458',
        '仪器': 'BK0458',
        '仪表': 'BK0458',
        '自动化': 'BK0545',
        '机器人': 'BK0545',
        '工业': 'BK0545',
        '机床': 'BK0545',
        '泵': 'BK0545',
        '阀门': 'BK0545',
        '轴承': 'BK0545',
        '齿轮': 'BK0545',
        '电机': 'BK1030',
        '变压器': 'BK0457',
        '电缆': 'BK0457',
        '电线': 'BK0457',
        '开关': 'BK0457',
        '配电': 'BK0457',
        '电网': 'BK0457',
        '电源': 'BK1034',
        '充电器': 'BK1034',
        '逆变器': 'BK1034',
        
        # 交通运输
        '航空': 'BK0420',
        '机场': 'BK0420',
        '港口': 'BK0450',
        '物流': 'BK0422',
        '运输': 'BK0450',
        '船舶': 'BK0729',
        '航运': 'BK0450',
        '海运': 'BK0450',
        '铁路': 'BK0421',
        '公路': 'BK0421',
        '高速': 'BK0421',
        '地铁': 'BK0421',
        '公交': 'BK0421',
        '出租车': 'BK0421',
        '快递': 'BK0422',
        '仓储': 'BK0422',
        '配送': 'BK0422',
        '供应链': 'BK0422',
        
        # 公用事业
        '电信': 'BK0736',
        '公用': 'BK0427',
        '水务': 'BK0427',
        '供水': 'BK0427',
        '排水': 'BK0427',
        '污水处理': 'BK0728',
        '环保': 'BK0728',
        '垃圾': 'BK0728',
        '废物': 'BK0728',
        '回收': 'BK0728',
        '节能': 'BK0728',
        '减排': 'BK0728',
        '清洁': 'BK0728',
        
        # 传媒娱乐
        '传媒': 'BK0486',
        '文化': 'BK0486',
        '游戏': 'BK1046',
        '娱乐': 'BK0485',
        '旅游': 'BK0485',
        '酒店': 'BK0485',
        '度假': 'BK0485',
        '景区': 'BK0485',
        '主题公园': 'BK0485',
        '电影': 'BK0486',
        '电视': 'BK0486',
        '广播': 'BK0486',
        '出版': 'BK0486',
        '报纸': 'BK0486',
        '杂志': 'BK0486',
        '广告': 'BK0486',
        '营销': 'BK0486',
        '公关': 'BK0486',
        '会展': 'BK0486',
        '演出': 'BK0486',
        '演唱会': 'BK0486',
        '音乐会': 'BK0486',
        '剧院': 'BK0486',
        '博物馆': 'BK0486',
        '图书馆': 'BK0486',
        '教育': 'BK0740',
        '培训': 'BK0740',
        '学校': 'BK0740',
        '大学': 'BK0740',
        '学院': 'BK0740',
        '在线教育': 'BK0740',
        '职业教育': 'BK0740',
        '语言': 'BK0740',
        '考试': 'BK0740',
        
        # 农业
        '农业': 'BK0433',
        '农牧': 'BK0433',
        '渔业': 'BK0433',
        '养殖': 'BK0433',
        '种植': 'BK0433',
        '畜牧': 'BK0433',
        '饲料': 'BK0730',
        '农药': 'BK0730',
        '兽药': 'BK0730',
        '化肥': 'BK0731',
        '种子': 'BK0433',
        '农产品': 'BK0433',
        '粮食': 'BK0433',
        '蔬菜': 'BK0433',
        '水果': 'BK0433',
        '肉类': 'BK0433',
        '乳制品': 'BK0438',
        '水产': 'BK0433',
        
        # 其他
        '综合': 'BK0539',
        '集团': 'BK0539',
        '控股': 'BK0539',
        '股份': 'BK0539',
        '有限': 'BK0539',
        '国际': 'BK0539',
        '中国': 'BK0539',
        '香港': 'BK0539',
        '亚洲': 'BK0539',
        '全球': 'BK0539',
        '世界': 'BK0539',
        '企业': 'BK0539',
        '公司': 'BK0539',
        '实业': 'BK0539',
        '工业': 'BK0545',
        '商业': 'BK0482',
        '贸易': 'BK0484',
        '进出口': 'BK0484',
        '代理': 'BK0484',
        '经销': 'BK0484',
        '批发': 'BK0484',
        '零售': 'BK0482',
        '服务': 'BK1043',
        '咨询': 'BK1043',
        '法律': 'BK1043',
        '会计': 'BK1043',
        '审计': 'BK1043',
        '评估': 'BK1043',
        '认证': 'BK1043',
        '检测': 'BK1043',
        '检验': 'BK1043',
        '认证': 'BK1043',
        '标准': 'BK1043',
        '质量': 'BK1043',
        '安全': 'BK1043',
        '保险': 'BK0474',
        '再保险': 'BK0474',
        '寿险': 'BK0474',
        '财险': 'BK0474',
        '健康险': 'BK0474',
        '意外险': 'BK0474',
        '车险': 'BK0474',
        '房屋险': 'BK0474',
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
        'BK1033': '电池',
        'BK0451': '房地产开发',
        'BK1045': '房地产服务',
        'BK0425': '工程建设',
        'BK0720': '建筑装饰',
        'BK0465': '化学制药',
        'BK0727': '医疗服务',
        'BK1044': '生物制品',
        'BK1041': '医疗器械',
        'BK0438': '食品饮料',
        'BK0436': '纺织服装',
        'BK0482': '商业百货',
        'BK0484': '贸易行业',
        'BK1035': '美容护理',
        'BK0734': '珠宝首饰',
        'BK0732': '贵金属',
        'BK0464': '石油行业',
        'BK0437': '煤炭行业',
        'BK0428': '电力行业',
        'BK1015': '能源金属',
        'BK1028': '燃气',
        'BK1031': '光伏设备',
        'BK1032': '风电设备',
        'BK1017': '采掘行业',
        'BK0478': '有色金属',
        'BK0479': '钢铁行业',
        'BK1027': '小金属',
        'BK0910': '专用设备',
        'BK0739': '工程机械',
        'BK0545': '通用设备',
        'BK1020': '非金属材料',
        'BK0538': '化学制品',
        'BK0454': '塑料制品',
        'BK1018': '橡胶制品',
        'BK0546': '玻璃玻纤',
        'BK0424': '水泥建材',
        'BK0476': '装修建材',
        'BK0725': '装修装饰',
        'BK0440': '家用轻工',
        'BK0456': '家电行业',
        'BK0735': '计算机设备',
        'BK0458': '仪器仪表',
        'BK1030': '电机',
        'BK0457': '电网设备',
        'BK1034': '电源设备',
        'BK0420': '航空机场',
        'BK0450': '航运港口',
        'BK0422': '物流行业',
        'BK0729': '船舶制造',
        'BK0421': '铁路公路',
        'BK0736': '通信服务',
        'BK0427': '公用事业',
        'BK0728': '环保行业',
        'BK0486': '文化传媒',
        'BK1046': '游戏',
        'BK0485': '旅游酒店',
        'BK0740': '教育',
        'BK0433': '农牧饲渔',
        'BK0730': '农药兽药',
        'BK0731': '化肥行业',
        'BK0539': '综合行业',
        'BK1043': '专业服务',
    }

def map_hk_industries_enhanced():
    """为港股映射行业 - 增强版"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 获取未映射的港股列表
        cursor.execute("SELECT stock_code, stock_name FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5 AND (industry_name = '' OR industry_name IS NULL)")
        unmapped_hk_stocks = cursor.fetchall()
        
        print(f"找到 {len(unmapped_hk_stocks)} 只未映射的港股")
        
        industry_mapping = get_enhanced_industry_mapping()
        industry_names = get_industry_names()
        
        mapped_count = 0
        
        for stock_code, stock_name in unmapped_hk_stocks:
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
        print(f"   - 本次新增映射: {mapped_count}")
        print(f"   - 映射率: {hk_mapped/hk_total*100:.1f}%")
        
        # 显示港股行业分布
        cursor.execute("""
            SELECT industry_name, COUNT(*) as count 
            FROM stock_industry_mapping 
            WHERE LENGTH(stock_code) = 5 AND industry_name != '' 
            GROUP BY industry_name 
            ORDER BY count DESC 
            LIMIT 15
        """)
        industries = cursor.fetchall()
        
        if industries:
            print(f"\n🏭 港股行业分布TOP15:")
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
    print("🇭🇰 开始为港股补充行业分类 - 增强版")
    print("=" * 60)
    
    if map_hk_industries_enhanced():
        print("\n" + "=" * 60)
        print("✅ 港股行业分类补充完成！")
        print("🌐 访问 http://127.0.0.1:5001 查看数据")
        print("=" * 60)
    else:
        print("❌ 港股行业分类补充失败！")

if __name__ == "__main__":
    main() 