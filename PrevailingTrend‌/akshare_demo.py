import akshare as ak
import json
import time

"""
AKShare 接口数据获取示例
功能：从 AKShare 获取股票数据并保存原始数据结构
"""

def fetch_stock_data_from_akshare():
    """从 AKShare 获取股票数据示例"""
    try:
        # 获取所有股票代码列表
        print("尝试从 AKShare 获取股票数据...")
        stock_zh_a_spot_df = ak.stock_zh_a_spot_em()
        
        # 保存原始数据结构到文本文件
        with open('akshare_stock_structure.txt', 'w', encoding='utf-8') as f:
            # 写入数据结构信息
            f.write("=== AKShare 股票数据结构 ===\n")
            f.write(f"数据类型: {type(stock_zh_a_spot_df)}\n")
            f.write(f"数据形状: {stock_zh_a_spot_df.shape}\n")
            f.write(f"列名: {list(stock_zh_a_spot_df.columns)}\n\n")
            
            # 写入前5行数据作为示例
            f.write("=== 前5行数据示例 ===\n")
            f.write(stock_zh_a_spot_df.head(5).to_string())
            
            # 写入数据字典形式（JSON）作为结构化表示
            f.write("\n\n=== 数据JSON结构 ===\n")
            # 转换为JSON并写入，只保留前5条数据
            sample_data = stock_zh_a_spot_df.head(5).to_dict(orient='records')
            f.write(json.dumps(sample_data, ensure_ascii=False, indent=2))
        
        print("AKShare 数据获取成功！原始数据结构已保存到 akshare_stock_structure.txt")
        return stock_zh_a_spot_df
    
    except Exception as e:
        print(f"获取 AKShare 数据失败: {str(e)}")
        # 写入错误信息到文件
        with open('akshare_error.log', 'a', encoding='utf-8') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 错误: {str(e)}\n")
        return None

if __name__ == "__main__":
    fetch_stock_data_from_akshare()