#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

class MockAPIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/wind-industries':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # 完整的上市公司或行业分类数据（基于二级市场标准）
            mock_data = {
                "success": True,
                "data": [
                    # 一级行业分类 (25个)
                    {"industryCode": "110000", "industryName": "石油石化", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 石油石化"},
                    {"industryCode": "210000", "industryName": "有色金属", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 有色金属"},
                    {"industryCode": "220000", "industryName": "钢铁", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 钢铁"},
                    {"industryCode": "230000", "industryName": "基础化工", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 基础化工"},
                    {"industryCode": "240000", "industryName": "建筑材料", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 建筑材料"},
                    {"industryCode": "270000", "industryName": "机械设备", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 机械设备"},
                    {"industryCode": "280000", "industryName": "电力设备", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 电力设备"},
                    {"industryCode": "330000", "industryName": "家用电器", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 家用电器"},
                    {"industryCode": "350000", "industryName": "计算机", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 计算机"},
                    {"industryCode": "360000", "industryName": "电子", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 电子"},
                    {"industryCode": "370000", "industryName": "通信", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 通信"},
                    {"industryCode": "410000", "industryName": "电力及公用事业", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 电力及公用事业"},
                    {"industryCode": "420000", "industryName": "交通运输", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 交通运输"},
                    {"industryCode": "430000", "industryName": "房地产", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 房地产"},
                    {"industryCode": "450000", "industryName": "商业贸易", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 商业贸易"},
                    {"industryCode": "460000", "industryName": "休闲服务", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 休闲服务"},
                    {"industryCode": "480000", "industryName": "银行", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 银行"},
                    {"industryCode": "490000", "industryName": "非银金融", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 非银金融"},
                    {"industryCode": "510000", "industryName": "综合", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 综合"},
                    {"industryCode": "610000", "industryName": "食品饮料", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 食品饮料"},
                    {"industryCode": "620000", "industryName": "纺织服装", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 纺织服装"},
                    {"industryCode": "630000", "industryName": "轻工制造", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 轻工制造"},
                    {"industryCode": "640000", "industryName": "金融服务", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 金融服务"},
                    {"industryCode": "710000", "industryName": "社服", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 社服"},
                    {"industryCode": "720000", "industryName": "传媒", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "一级行业: 传媒"},
                    
                    # 二级行业分类 (50个)
                    {"industryCode": "110100", "industryName": "石油开采", "industryLevel": 2, "parentIndustryCode": "110000", "industryDescription": "二级行业: 石油开采"},
                    {"industryCode": "110200", "industryName": "石油加工", "industryLevel": 2, "parentIndustryCode": "110000", "industryDescription": "二级行业: 石油加工"},
                    {"industryCode": "110300", "industryName": "石化产品", "industryLevel": 2, "parentIndustryCode": "110000", "industryDescription": "二级行业: 石化产品"},
                    {"industryCode": "210100", "industryName": "贵金属", "industryLevel": 2, "parentIndustryCode": "210000", "industryDescription": "二级行业: 贵金属"},
                    {"industryCode": "210200", "industryName": "基本金属", "industryLevel": 2, "parentIndustryCode": "210000", "industryDescription": "二级行业: 基本金属"},
                    {"industryCode": "210300", "industryName": "稀有金属", "industryLevel": 2, "parentIndustryCode": "210000", "industryDescription": "二级行业: 稀有金属"},
                    {"industryCode": "220100", "industryName": "钢铁冶炼", "industryLevel": 2, "parentIndustryCode": "220000", "industryDescription": "二级行业: 钢铁冶炼"},
                    {"industryCode": "220200", "industryName": "钢铁加工", "industryLevel": 2, "parentIndustryCode": "220000", "industryDescription": "二级行业: 钢铁加工"},
                    {"industryCode": "230100", "industryName": "基础化工原料", "industryLevel": 2, "parentIndustryCode": "230000", "industryDescription": "二级行业: 基础化工原料"},
                    {"industryCode": "230200", "industryName": "精细化工", "industryLevel": 2, "parentIndustryCode": "230000", "industryDescription": "二级行业: 精细化工"},
                    {"industryCode": "240100", "industryName": "水泥", "industryLevel": 2, "parentIndustryCode": "240000", "industryDescription": "二级行业: 水泥"},
                    {"industryCode": "240200", "industryName": "玻璃", "industryLevel": 2, "parentIndustryCode": "240000", "industryDescription": "二级行业: 玻璃"},
                    {"industryCode": "240300", "industryName": "陶瓷", "industryLevel": 2, "parentIndustryCode": "240000", "industryDescription": "二级行业: 陶瓷"},
                    {"industryCode": "270100", "industryName": "通用机械", "industryLevel": 2, "parentIndustryCode": "270000", "industryDescription": "二级行业: 通用机械"},
                    {"industryCode": "270200", "industryName": "专用设备", "industryLevel": 2, "parentIndustryCode": "270000", "industryDescription": "二级行业: 专用设备"},
                    {"industryCode": "270300", "industryName": "运输设备", "industryLevel": 2, "parentIndustryCode": "270000", "industryDescription": "二级行业: 运输设备"},
                    {"industryCode": "280100", "industryName": "电机", "industryLevel": 2, "parentIndustryCode": "280000", "industryDescription": "二级行业: 电机"},
                    {"industryCode": "280200", "industryName": "新能源设备", "industryLevel": 2, "parentIndustryCode": "280000", "industryDescription": "二级行业: 新能源设备"},
                    {"industryCode": "280300", "industryName": "输变电设备", "industryLevel": 2, "parentIndustryCode": "280000", "industryDescription": "二级行业: 输变电设备"},
                    {"industryCode": "330100", "industryName": "白色家电", "industryLevel": 2, "parentIndustryCode": "330000", "industryDescription": "二级行业: 白色家电"},
                    {"industryCode": "330200", "industryName": "黑色家电", "industryLevel": 2, "parentIndustryCode": "330000", "industryDescription": "二级行业: 黑色家电"},
                    {"industryCode": "350100", "industryName": "软件开发", "industryLevel": 2, "parentIndustryCode": "350000", "industryDescription": "二级行业: 软件开发"},
                    {"industryCode": "350200", "industryName": "系统集成", "industryLevel": 2, "parentIndustryCode": "350000", "industryDescription": "二级行业: 系统集成"},
                    {"industryCode": "350300", "industryName": "IT服务", "industryLevel": 2, "parentIndustryCode": "350000", "industryDescription": "二级行业: IT服务"},
                    {"industryCode": "360100", "industryName": "半导体", "industryLevel": 2, "parentIndustryCode": "360000", "industryDescription": "二级行业: 半导体"},
                    {"industryCode": "360200", "industryName": "消费电子", "industryLevel": 2, "parentIndustryCode": "360000", "industryDescription": "二级行业: 消费电子"},
                    {"industryCode": "360300", "industryName": "电子元器件", "industryLevel": 2, "parentIndustryCode": "360000", "industryDescription": "二级行业: 电子元器件"},
                    {"industryCode": "370100", "industryName": "通信设备", "industryLevel": 2, "parentIndustryCode": "370000", "industryDescription": "二级行业: 通信设备"},
                    {"industryCode": "370200", "industryName": "通信服务", "industryLevel": 2, "parentIndustryCode": "370000", "industryDescription": "二级行业: 通信服务"},
                    {"industryCode": "410100", "industryName": "电力", "industryLevel": 2, "parentIndustryCode": "410000", "industryDescription": "二级行业: 电力"},
                    {"industryCode": "410200", "industryName": "公用事业", "industryLevel": 2, "parentIndustryCode": "410000", "industryDescription": "二级行业: 公用事业"},
                    {"industryCode": "420100", "industryName": "航空运输", "industryLevel": 2, "parentIndustryCode": "420000", "industryDescription": "二级行业: 航空运输"},
                    {"industryCode": "420200", "industryName": "铁路运输", "industryLevel": 2, "parentIndustryCode": "420000", "industryDescription": "二级行业: 铁路运输"},
                    {"industryCode": "420300", "industryName": "公路运输", "industryLevel": 2, "parentIndustryCode": "420000", "industryDescription": "二级行业: 公路运输"},
                    {"industryCode": "420400", "industryName": "港口航运", "industryLevel": 2, "parentIndustryCode": "420000", "industryDescription": "二级行业: 港口航运"},
                    {"industryCode": "430100", "industryName": "房地产开发", "industryLevel": 2, "parentIndustryCode": "430000", "industryDescription": "二级行业: 房地产开发"},
                    {"industryCode": "430200", "industryName": "物业管理", "industryLevel": 2, "parentIndustryCode": "430000", "industryDescription": "二级行业: 物业管理"},
                    {"industryCode": "450100", "industryName": "零售", "industryLevel": 2, "parentIndustryCode": "450000", "industryDescription": "二级行业: 零售"},
                    {"industryCode": "450200", "industryName": "批发", "industryLevel": 2, "parentIndustryCode": "450000", "industryDescription": "二级行业: 批发"},
                    {"industryCode": "460100", "industryName": "旅游", "industryLevel": 2, "parentIndustryCode": "460000", "industryDescription": "二级行业: 旅游"},
                    {"industryCode": "460200", "industryName": "酒店", "industryLevel": 2, "parentIndustryCode": "460000", "industryDescription": "二级行业: 酒店"},
                    {"industryCode": "480100", "industryName": "银行", "industryLevel": 2, "parentIndustryCode": "480000", "industryDescription": "二级行业: 银行"},
                    {"industryCode": "480200", "industryName": "保险", "industryLevel": 2, "parentIndustryCode": "480000", "industryDescription": "二级行业: 保险"},
                    {"industryCode": "490100", "industryName": "证券", "industryLevel": 2, "parentIndustryCode": "490000", "industryDescription": "二级行业: 证券"},
                    {"industryCode": "490200", "industryName": "信托", "industryLevel": 2, "parentIndustryCode": "490000", "industryDescription": "二级行业: 信托"},
                    {"industryCode": "490300", "industryName": "租赁", "industryLevel": 2, "parentIndustryCode": "490000", "industryDescription": "二级行业: 租赁"},
                    {"industryCode": "610100", "industryName": "白酒", "industryLevel": 2, "parentIndustryCode": "610000", "industryDescription": "二级行业: 白酒"},
                    {"industryCode": "610200", "industryName": "啤酒", "industryLevel": 2, "parentIndustryCode": "610000", "industryDescription": "二级行业: 啤酒"},
                    {"industryCode": "610300", "industryName": "软饮料", "industryLevel": 2, "parentIndustryCode": "610000", "industryDescription": "二级行业: 软饮料"},
                    {"industryCode": "610400", "industryName": "食品加工", "industryLevel": 2, "parentIndustryCode": "610000", "industryDescription": "二级行业: 食品加工"},
                    {"industryCode": "620100", "industryName": "纺织", "industryLevel": 2, "parentIndustryCode": "620000", "industryDescription": "二级行业: 纺织"},
                    {"industryCode": "620200", "industryName": "服装", "industryLevel": 2, "parentIndustryCode": "620000", "industryDescription": "二级行业: 服装"},
                    {"industryCode": "630100", "industryName": "造纸", "industryLevel": 2, "parentIndustryCode": "630000", "industryDescription": "二级行业: 造纸"},
                    {"industryCode": "630200", "industryName": "包装", "industryLevel": 2, "parentIndustryCode": "630000", "industryDescription": "二级行业: 包装"},
                    {"industryCode": "710100", "industryName": "教育", "industryLevel": 2, "parentIndustryCode": "710000", "industryDescription": "二级行业: 教育"},
                    {"industryCode": "710200", "industryName": "医疗", "industryLevel": 2, "parentIndustryCode": "710000", "industryDescription": "二级行业: 医疗"},
                    {"industryCode": "720100", "industryName": "出版", "industryLevel": 2, "parentIndustryCode": "720000", "industryDescription": "二级行业: 出版"},
                    {"industryCode": "720200", "industryName": "广告", "industryLevel": 2, "parentIndustryCode": "720000", "industryDescription": "二级行业: 广告"},
                    
                    # 三级行业分类 (30个)
                    {"industryCode": "110101", "industryName": "原油开采", "industryLevel": 3, "parentIndustryCode": "110100", "industryDescription": "三级行业: 原油开采"},
                    {"industryCode": "110102", "industryName": "天然气开采", "industryLevel": 3, "parentIndustryCode": "110100", "industryDescription": "三级行业: 天然气开采"},
                    {"industryCode": "110201", "industryName": "炼油", "industryLevel": 3, "parentIndustryCode": "110200", "industryDescription": "三级行业: 炼油"},
                    {"industryCode": "110202", "industryName": "石化", "industryLevel": 3, "parentIndustryCode": "110200", "industryDescription": "三级行业: 石化"},
                    {"industryCode": "210101", "industryName": "黄金", "industryLevel": 3, "parentIndustryCode": "210100", "industryDescription": "三级行业: 黄金"},
                    {"industryCode": "210102", "industryName": "白银", "industryLevel": 3, "parentIndustryCode": "210100", "industryDescription": "三级行业: 白银"},
                    {"industryCode": "210201", "industryName": "铜", "industryLevel": 3, "parentIndustryCode": "210200", "industryDescription": "三级行业: 铜"},
                    {"industryCode": "210202", "industryName": "铝", "industryLevel": 3, "parentIndustryCode": "210200", "industryDescription": "三级行业: 铝"},
                    {"industryCode": "210203", "industryName": "锌", "industryLevel": 3, "parentIndustryCode": "210200", "industryDescription": "三级行业: 锌"},
                    {"industryCode": "210301", "industryName": "锂", "industryLevel": 3, "parentIndustryCode": "210300", "industryDescription": "三级行业: 锂"},
                    {"industryCode": "210302", "industryName": "稀土", "industryLevel": 3, "parentIndustryCode": "210300", "industryDescription": "三级行业: 稀土"},
                    {"industryCode": "220101", "industryName": "粗钢", "industryLevel": 3, "parentIndustryCode": "220100", "industryDescription": "三级行业: 粗钢"},
                    {"industryCode": "220102", "industryName": "钢材", "industryLevel": 3, "parentIndustryCode": "220100", "industryDescription": "三级行业: 钢材"},
                    {"industryCode": "230101", "industryName": "基础化工原料", "industryLevel": 3, "parentIndustryCode": "230100", "industryDescription": "三级行业: 基础化工原料"},
                    {"industryCode": "230102", "industryName": "化肥", "industryLevel": 3, "parentIndustryCode": "230100", "industryDescription": "三级行业: 化肥"},
                    {"industryCode": "240101", "industryName": "水泥制造", "industryLevel": 3, "parentIndustryCode": "240100", "industryDescription": "三级行业: 水泥制造"},
                    {"industryCode": "240102", "industryName": "水泥销售", "industryLevel": 3, "parentIndustryCode": "240100", "industryDescription": "三级行业: 水泥销售"},
                    {"industryCode": "270101", "industryName": "机床", "industryLevel": 3, "parentIndustryCode": "270100", "industryDescription": "三级行业: 机床"},
                    {"industryCode": "270102", "industryName": "工程机械", "industryLevel": 3, "parentIndustryCode": "270100", "industryDescription": "三级行业: 工程机械"},
                    {"industryCode": "280101", "industryName": "电机设备", "industryLevel": 3, "parentIndustryCode": "280100", "industryDescription": "三级行业: 电机设备"},
                    {"industryCode": "280201", "industryName": "光伏设备", "industryLevel": 3, "parentIndustryCode": "280200", "industryDescription": "三级行业: 光伏设备"},
                    {"industryCode": "280202", "industryName": "风电设备", "industryLevel": 3, "parentIndustryCode": "280200", "industryDescription": "三级行业: 风电设备"},
                    {"industryCode": "330101", "industryName": "空调", "industryLevel": 3, "parentIndustryCode": "330100", "industryDescription": "三级行业: 空调"},
                    {"industryCode": "330102", "industryName": "冰箱", "industryLevel": 3, "parentIndustryCode": "330100", "industryDescription": "三级行业: 冰箱"},
                    {"industryCode": "350101", "industryName": "应用软件", "industryLevel": 3, "parentIndustryCode": "350100", "industryDescription": "三级行业: 应用软件"},
                    {"industryCode": "350102", "industryName": "系统软件", "industryLevel": 3, "parentIndustryCode": "350100", "industryDescription": "三级行业: 系统软件"},
                    {"industryCode": "360101", "industryName": "芯片设计", "industryLevel": 3, "parentIndustryCode": "360100", "industryDescription": "三级行业: 芯片设计"},
                    {"industryCode": "360102", "industryName": "芯片制造", "industryLevel": 3, "parentIndustryCode": "360100", "industryDescription": "三级行业: 芯片制造"},
                    {"industryCode": "480101", "industryName": "国有银行", "industryLevel": 3, "parentIndustryCode": "480100", "industryDescription": "三级行业: 国有银行"},
                    {"industryCode": "480102", "industryName": "股份制银行", "industryLevel": 3, "parentIndustryCode": "480100", "industryDescription": "三级行业: 股份制银行"}
                ],
                "total": 105
            }
            
            response = json.dumps(mock_data, ensure_ascii=False, indent=2)
            self.wfile.write(response.encode('utf-8'))
            
        elif parsed_path.path == '/api/wind-industries/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            stats_data = {
                "success": True,
                "data": {
                    "total_industries": 105,
                    "level_1_count": 25,
                    "level_2_count": 50,
                    "level_3_count": 30
                }
            }
            
            response = json.dumps(stats_data, ensure_ascii=False, indent=2)
            self.wfile.write(response.encode('utf-8'))
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = json.dumps({"success": False, "error": "API endpoint not found"})
            self.wfile.write(error_response.encode('utf-8'))
    
    def log_message(self, format, *args):
        print(f"[{self.date_time_string()}] {format % args}")

if __name__ == "__main__":
    PORT = 5001
    
    with socketserver.TCPServer(("", PORT), MockAPIHandler) as httpd:
        print(f"========================================")
        print(f"上市公司或行业分类API模拟服务器启动中...")
        print(f"端口: {PORT}")
        print(f"API地址: http://localhost:{PORT}/api/wind-industries")
        print(f"统计数据: http://localhost:{PORT}/api/wind-industries/stats")
        print(f"========================================")
        print(f"数据统计:")
        print(f"- 一级行业: 25个")
        print(f"- 二级行业: 50个") 
        print(f"- 三级行业: 30个")
        print(f"- 总计: 105个行业分类")
        print(f"========================================")
        print(f"按 Ctrl+C 停止服务器")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n服务器已停止")
