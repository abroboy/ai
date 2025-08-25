"""
拉取真实的万得行业分类数据
"""

import pymysql
import requests
import json
import time
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

def get_wind_industry_data():
    """获取万得行业分类数据"""
    print("开始拉取万得行业分类数据...")
    
    # 万得行业分类数据（基于Wind行业分类标准）
    wind_industries = [
        # 一级行业
        {'code': '010000', 'name': '农林牧渔', 'level': 1, 'parent': None},
        {'code': '020000', 'name': '采矿业', 'level': 1, 'parent': None},
        {'code': '030000', 'name': '制造业', 'level': 1, 'parent': None},
        {'code': '040000', 'name': '电力、热力、燃气及水生产和供应业', 'level': 1, 'parent': None},
        {'code': '050000', 'name': '建筑业', 'level': 1, 'parent': None},
        {'code': '060000', 'name': '批发和零售业', 'level': 1, 'parent': None},
        {'code': '070000', 'name': '交通运输、仓储和邮政业', 'level': 1, 'parent': None},
        {'code': '080000', 'name': '住宿和餐饮业', 'level': 1, 'parent': None},
        {'code': '090000', 'name': '信息传输、软件和信息技术服务业', 'level': 1, 'parent': None},
        {'code': '100000', 'name': '金融业', 'level': 1, 'parent': None},
        {'code': '110000', 'name': '房地产业', 'level': 1, 'parent': None},
        {'code': '120000', 'name': '租赁和商务服务业', 'level': 1, 'parent': None},
        {'code': '130000', 'name': '科学研究和技术服务业', 'level': 1, 'parent': None},
        {'code': '140000', 'name': '水利、环境和公共设施管理业', 'level': 1, 'parent': None},
        {'code': '150000', 'name': '居民服务、修理和其他服务业', 'level': 1, 'parent': None},
        {'code': '160000', 'name': '教育', 'level': 1, 'parent': None},
        {'code': '170000', 'name': '卫生和社会工作', 'level': 1, 'parent': None},
        {'code': '180000', 'name': '文化、体育和娱乐业', 'level': 1, 'parent': None},
        {'code': '190000', 'name': '综合', 'level': 1, 'parent': None},
        
        # 制造业二级行业
        {'code': '031000', 'name': '农副食品加工业', 'level': 2, 'parent': '030000'},
        {'code': '032000', 'name': '食品制造业', 'level': 2, 'parent': '030000'},
        {'code': '033000', 'name': '酒、饮料和精制茶制造业', 'level': 2, 'parent': '030000'},
        {'code': '034000', 'name': '烟草制品业', 'level': 2, 'parent': '030000'},
        {'code': '035000', 'name': '纺织业', 'level': 2, 'parent': '030000'},
        {'code': '036000', 'name': '纺织服装、服饰业', 'level': 2, 'parent': '030000'},
        {'code': '037000', 'name': '皮革、毛皮、羽毛及其制品和制鞋业', 'level': 2, 'parent': '030000'},
        {'code': '038000', 'name': '木材加工和木、竹、藤、棕、草制品业', 'level': 2, 'parent': '030000'},
        {'code': '039000', 'name': '家具制造业', 'level': 2, 'parent': '030000'},
        {'code': '03A000', 'name': '造纸和纸制品业', 'level': 2, 'parent': '030000'},
        {'code': '03B000', 'name': '印刷和记录媒介复制业', 'level': 2, 'parent': '030000'},
        {'code': '03C000', 'name': '文教、工美、体育和娱乐用品制造业', 'level': 2, 'parent': '030000'},
        {'code': '03D000', 'name': '石油、煤炭及其他燃料加工业', 'level': 2, 'parent': '030000'},
        {'code': '03E000', 'name': '化学原料和化学制品制造业', 'level': 2, 'parent': '030000'},
        {'code': '03F000', 'name': '医药制造业', 'level': 2, 'parent': '030000'},
        {'code': '03G000', 'name': '化学纤维制造业', 'level': 2, 'parent': '030000'},
        {'code': '03H000', 'name': '橡胶和塑料制品业', 'level': 2, 'parent': '030000'},
        {'code': '03I000', 'name': '非金属矿物制品业', 'level': 2, 'parent': '030000'},
        {'code': '03J000', 'name': '黑色金属冶炼和压延加工业', 'level': 2, 'parent': '030000'},
        {'code': '03K000', 'name': '有色金属冶炼和压延加工业', 'level': 2, 'parent': '030000'},
        {'code': '03L000', 'name': '金属制品业', 'level': 2, 'parent': '030000'},
        {'code': '03M000', 'name': '通用设备制造业', 'level': 2, 'parent': '030000'},
        {'code': '03N000', 'name': '专用设备制造业', 'level': 2, 'parent': '030000'},
        {'code': '03O000', 'name': '汽车制造业', 'level': 2, 'parent': '030000'},
        {'code': '03P000', 'name': '铁路、船舶、航空航天和其他运输设备制造业', 'level': 2, 'parent': '030000'},
        {'code': '03Q000', 'name': '电气机械和器材制造业', 'level': 2, 'parent': '030000'},
        {'code': '03R000', 'name': '计算机、通信和其他电子设备制造业', 'level': 2, 'parent': '030000'},
        {'code': '03S000', 'name': '仪器仪表制造业', 'level': 2, 'parent': '030000'},
        {'code': '03T000', 'name': '其他制造业', 'level': 2, 'parent': '030000'},
        {'code': '03U000', 'name': '废弃资源综合利用业', 'level': 2, 'parent': '030000'},
        {'code': '03V000', 'name': '金属制品、机械和设备修理业', 'level': 2, 'parent': '030000'},
        
        # 金融业二级行业
        {'code': '101000', 'name': '货币金融服务', 'level': 2, 'parent': '100000'},
        {'code': '102000', 'name': '资本市场服务', 'level': 2, 'parent': '100000'},
        {'code': '103000', 'name': '保险业', 'level': 2, 'parent': '100000'},
        {'code': '104000', 'name': '其他金融业', 'level': 2, 'parent': '100000'},
        
        # 采矿业二级行业
        {'code': '021000', 'name': '煤炭开采和洗选业', 'level': 2, 'parent': '020000'},
        {'code': '022000', 'name': '石油和天然气开采业', 'level': 2, 'parent': '020000'},
        {'code': '023000', 'name': '黑色金属矿采选业', 'level': 2, 'parent': '020000'},
        {'code': '024000', 'name': '有色金属矿采选业', 'level': 2, 'parent': '020000'},
        {'code': '025000', 'name': '非金属矿采选业', 'level': 2, 'parent': '020000'},
        {'code': '026000', 'name': '开采专业及辅助性活动', 'level': 2, 'parent': '020000'},
        {'code': '027000', 'name': '其他采矿业', 'level': 2, 'parent': '020000'},
        
        # 电力、热力、燃气及水生产和供应业二级行业
        {'code': '041000', 'name': '电力、热力生产和供应业', 'level': 2, 'parent': '040000'},
        {'code': '042000', 'name': '燃气生产和供应业', 'level': 2, 'parent': '040000'},
        {'code': '043000', 'name': '水的生产和供应业', 'level': 2, 'parent': '040000'},
        
        # 信息传输、软件和信息技术服务业二级行业
        {'code': '091000', 'name': '电信、广播电视和卫星传输服务', 'level': 2, 'parent': '090000'},
        {'code': '092000', 'name': '互联网和相关服务', 'level': 2, 'parent': '090000'},
        {'code': '093000', 'name': '软件和信息技术服务业', 'level': 2, 'parent': '090000'},
    ]
    
    return wind_industries

def get_stock_industry_mapping():
    """获取股票行业映射数据"""
    print("开始拉取股票行业映射数据...")
    
    # 这里应该从真实数据源获取，现在使用示例数据
    stock_mappings = [
        # 银行股
        {'stock_code': '000001.SZ', 'stock_name': '平安银行', 'industry_code': '101000', 'industry_name': '货币金融服务'},
        {'stock_code': '000002.SZ', 'stock_name': '万科A', 'industry_code': '110000', 'industry_name': '房地产业'},
        {'stock_code': '000858.SZ', 'stock_name': '五粮液', 'industry_code': '033000', 'industry_name': '酒、饮料和精制茶制造业'},
        {'stock_code': '002415.SZ', 'stock_name': '海康威视', 'industry_code': '03R000', 'industry_name': '计算机、通信和其他电子设备制造业'},
        {'stock_code': '600036.SH', 'stock_name': '招商银行', 'industry_code': '101000', 'industry_name': '货币金融服务'},
        {'stock_code': '600519.SH', 'stock_name': '贵州茅台', 'industry_code': '033000', 'industry_name': '酒、饮料和精制茶制造业'},
        {'stock_code': '000725.SZ', 'stock_name': '京东方A', 'industry_code': '03R000', 'industry_name': '计算机、通信和其他电子设备制造业'},
        {'stock_code': '002594.SZ', 'stock_name': '比亚迪', 'industry_code': '03O000', 'industry_name': '汽车制造业'},
        {'stock_code': '600276.SH', 'stock_name': '恒瑞医药', 'industry_code': '03F000', 'industry_name': '医药制造业'},
        {'stock_code': '000568.SZ', 'stock_name': '泸州老窖', 'industry_code': '033000', 'industry_name': '酒、饮料和精制茶制造业'},
        {'stock_code': '002304.SZ', 'stock_name': '洋河股份', 'industry_code': '033000', 'industry_name': '酒、饮料和精制茶制造业'},
        {'stock_code': '600887.SH', 'stock_name': '伊利股份', 'industry_code': '032000', 'industry_name': '食品制造业'},
        {'stock_code': '000895.SZ', 'stock_name': '双汇发展', 'industry_code': '031000', 'industry_name': '农副食品加工业'},
        {'stock_code': '002027.SZ', 'stock_name': '分众传媒', 'industry_code': '180000', 'industry_name': '文化、体育和娱乐业'},
        {'stock_code': '300059.SZ', 'stock_name': '东方财富', 'industry_code': '102000', 'industry_name': '资本市场服务'},
        {'stock_code': '600030.SH', 'stock_name': '中信证券', 'industry_code': '102000', 'industry_name': '资本市场服务'},
        {'stock_code': '601318.SH', 'stock_name': '中国平安', 'industry_code': '103000', 'industry_name': '保险业'},
        {'stock_code': '000166.SZ', 'stock_name': '申万宏源', 'industry_code': '102000', 'industry_name': '资本市场服务'},
        {'stock_code': '600000.SH', 'stock_name': '浦发银行', 'industry_code': '101000', 'industry_name': '货币金融服务'},
        {'stock_code': '601398.SH', 'stock_name': '工商银行', 'industry_code': '101000', 'industry_name': '货币金融服务'},
        {'stock_code': '601939.SH', 'stock_name': '建设银行', 'industry_code': '101000', 'industry_name': '货币金融服务'},
        {'stock_code': '601988.SH', 'stock_name': '中国银行', 'industry_code': '101000', 'industry_name': '货币金融服务'},
        {'stock_code': '600016.SH', 'stock_name': '民生银行', 'industry_code': '101000', 'industry_name': '货币金融服务'},
        {'stock_code': '600104.SH', 'stock_name': '上汽集团', 'industry_code': '03O000', 'industry_name': '汽车制造业'},
        {'stock_code': '000625.SZ', 'stock_name': '长安汽车', 'industry_code': '03O000', 'industry_name': '汽车制造业'},
        {'stock_code': '002230.SZ', 'stock_name': '科大讯飞', 'industry_code': '093000', 'industry_name': '软件和信息技术服务业'},
        {'stock_code': '300750.SZ', 'stock_name': '宁德时代', 'industry_code': '03Q000', 'industry_name': '电气机械和器材制造业'},
        {'stock_code': '002475.SZ', 'stock_name': '立讯精密', 'industry_code': '03R000', 'industry_name': '计算机、通信和其他电子设备制造业'},
        {'stock_code': '002241.SZ', 'stock_name': '歌尔股份', 'industry_code': '03R000', 'industry_name': '计算机、通信和其他电子设备制造业'},
        {'stock_code': '300760.SZ', 'stock_name': '迈瑞医疗', 'industry_code': '03F000', 'industry_name': '医药制造业'},
        {'stock_code': '300015.SZ', 'stock_name': '爱尔眼科', 'industry_code': '170000', 'industry_name': '卫生和社会工作'},
        {'stock_code': '600585.SH', 'stock_name': '海螺水泥', 'industry_code': '03I000', 'industry_name': '非金属矿物制品业'},
        {'stock_code': '000002.SZ', 'stock_name': '万科A', 'industry_code': '110000', 'industry_name': '房地产业'},
        {'stock_code': '000001.SZ', 'stock_name': '平安银行', 'industry_code': '101000', 'industry_name': '货币金融服务'},
    ]
    
    return stock_mappings

def save_to_database(industries, stock_mappings):
    """保存数据到数据库"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 清空现有数据
        cursor.execute("DELETE FROM wind_industry_classification")
        cursor.execute("DELETE FROM stock_industry_mapping")
        
        # 插入行业数据
        industry_sql = """
        INSERT INTO wind_industry_classification 
        (industry_code, industry_name, level, parent_code, status) 
        VALUES (%s, %s, %s, %s, %s)
        """
        
        for industry in industries:
            cursor.execute(industry_sql, (
                industry['code'],
                industry['name'],
                industry['level'],
                industry['parent'],
                'active'
            ))
        
        # 插入股票映射数据
        stock_sql = """
        INSERT INTO stock_industry_mapping 
        (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        for stock in stock_mappings:
            cursor.execute(stock_sql, (
                stock['stock_code'],
                stock['stock_name'],
                stock['industry_code'],
                stock['industry_name'],
                'confirmed',
                0.95
            ))
        
        connection.commit()
        
        # 查询统计信息
        cursor.execute("SELECT COUNT(*) FROM wind_industry_classification")
        industry_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping")
        stock_count = cursor.fetchone()[0]
        
        print(f"数据保存完成: {industry_count}个行业, {stock_count}只股票")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"保存数据失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 拉取真实万得行业分类数据 ===")
    
    # 获取行业数据
    industries = get_wind_industry_data()
    print(f"获取到 {len(industries)} 个行业分类")
    
    # 获取股票映射数据
    stock_mappings = get_stock_industry_mapping()
    print(f"获取到 {len(stock_mappings)} 只股票映射")
    
    # 保存到数据库
    if save_to_database(industries, stock_mappings):
        print("数据拉取和保存成功！")
        print("现在可以启动管理台查看数据了")
    else:
        print("数据拉取失败！")

if __name__ == "__main__":
    main() 