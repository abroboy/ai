import requests
import json
import time

"""
东方财富接口数据获取示例
功能：从东方财富获取股票数据并保存原始数据结构
"""

# 设置请求头，模拟浏览器访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://quote.eastmoney.com/',
}

def fetch_stock_data_from_eastmoney(max_retries=3):
    """从东方财富获取股票数据示例"""
    url = 'http://push2.eastmoney.com/api/qt/clist/get'
    
    # 请求参数
    params = {
        'pn': '1',       # 页码
        'pz': '100',     # 每页数量
        'po': '1',       # 排序方式
        'np': '1',       # 不知道什么参数，固定1
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',     # 不知道什么参数，固定2
        'invt': '2',     # 不知道什么参数，固定2
        'fid': 'f3',     # 排序字段，f3=涨跌幅
        'fs': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048', # 股票范围
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152', # 返回字段
    }
    
    retry_count = 0
    while retry_count < max_retries:
        try:
            print(f"尝试第{retry_count+1}次获取东方财富数据...")
            response = requests.get(url, params=params, headers=HEADERS, timeout=10)
            response.raise_for_status()  # 如果状态码不是200，抛出异常
            
            # 解析JSON数据
            data = response.json()
            
            # 保存原始数据结构到文本文件
            with open('eastmoney_stock_structure.txt', 'w', encoding='utf-8') as f:
                # 写入数据结构信息
                f.write("=== 东方财富股票数据结构 ===\n")
                f.write(f"数据类型: {type(data)}\n\n")
                
                # 写入完整的JSON数据结构
                f.write("=== 完整JSON数据结构 ===\n")
                f.write(json.dumps(data, ensure_ascii=False, indent=2))
                
                # 写入返回数据字段说明
                f.write("\n\n=== 东方财富数据字段说明 ===\n")
                f.write("f1: 未知\n")
                f.write("f2: 最新价\n")
                f.write("f3: 涨跌幅\n")
                f.write("f4: 涨跌额\n")
                f.write("f5: 总市值\n")
                f.write("f6: 流通市值\n")
                f.write("f7: 成交量（手）\n")
                f.write("f8: 成交额（万）\n")
                f.write("f9: 换手率\n")
                f.write("f10: 量比\n")
                f.write("f12: 股票代码\n")
                f.write("f13: 市场类型\n")
                f.write("f14: 股票名称\n")
                f.write("f15: 最高\n")
                f.write("f16: 最低\n")
                f.write("f17: 今开\n")
                f.write("f18: 昨收\n")
                f.write("f20: 市盈率(TTM)\n")
                f.write("f21: 市净率\n")
                f.write("f23: 涨停价\n")
                f.write("f24: 跌停价\n")
                f.write("f25: 委比\n")
                f.write("f22: 振幅\n")
                f.write("f11: 未知\n")
                f.write("f62: 未知\n")
                f.write("f128: 未知\n")
                f.write("f136: 未知\n")
                f.write("f115: 未知\n")
                f.write("f152: 未知\n")
            
            print("东方财富数据获取成功！原始数据结构已保存到 eastmoney_stock_structure.txt")
            return data
            
        except requests.exceptions.RequestException as e:
            retry_count += 1
            print(f"获取东方财富数据失败 (尝试 {retry_count}/{max_retries}): {str(e)}")
            if retry_count < max_retries:
                print("等待2秒后重试...")
                time.sleep(2)
        except json.JSONDecodeError as e:
            print(f"解析东方财富数据失败: {str(e)}")
            break
        except Exception as e:
            print(f"处理东方财富数据时发生未知错误: {str(e)}")
            break
    
    # 写入错误信息到文件
    with open('eastmoney_error.log', 'a', encoding='utf-8') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 错误: 获取东方财富数据失败\n")
    
    return None

if __name__ == "__main__":
    fetch_stock_data_from_eastmoney()