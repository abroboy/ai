#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API接口测试脚本
大势所趋风险框架管理台
"""

import requests
import json
import time
from datetime import datetime

def test_api_endpoint(url, description):
    """测试API端点"""
    print(f"\n{'='*50}")
    print(f"测试: {description}")
    print(f"URL: {url}")
    print(f"{'='*50}")
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {end_time - start_time:.2f}秒")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"响应数据类型: {type(data)}")
                if isinstance(data, dict):
                    print(f"响应字段: {list(data.keys())}")
                elif isinstance(data, list):
                    print(f"响应数组长度: {len(data)}")
                    if len(data) > 0:
                        print(f"第一个元素字段: {list(data[0].keys()) if isinstance(data[0], dict) else '非字典类型'}")
                print("✅ 测试通过")
                return True
            except json.JSONDecodeError:
                print(f"响应内容: {response.text[:200]}...")
                print("✅ 测试通过 (非JSON响应)")
                return True
        else:
            print(f"❌ 测试失败: HTTP {response.status_code}")
            print(f"错误信息: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 服务器可能未启动")
        return False
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("大势所趋风险框架管理台 - API接口测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    base_url = "http://localhost:8090"
    
    # 测试用例列表
    test_cases = [
        # 静态文件测试
        (f"{base_url}/", "首页访问测试"),
        (f"{base_url}/index.html", "原始首页测试"),
        (f"{base_url}/updated_index.html", "更新首页测试"),
        
        # API接口测试
        (f"{base_url}/api/listed-companies", "上市公司数据接口"),
        (f"{base_url}/api/domestic-hotspot", "国内热点数据接口"),
        (f"{base_url}/api/wind-industries", "Wind行业数据接口"),
        (f"{base_url}/api/global-capital-flow", "全球资本流动接口"),
        
        # 数据库查询接口测试
        (f"{base_url}/api/db/query?table=companies&limit=5", "数据库查询接口"),
        
        # 静态资源测试
        (f"{base_url}/static/js/domestic_hotspot_enhanced.js", "增强版国内热点JS"),
        (f"{base_url}/static/js/xueqiu_hotspot_enhanced.js", "增强版雪球热点JS"),
        (f"{base_url}/static/js/financial_statements.js", "财务三表JS"),
        (f"{base_url}/static/js/missing_modules.js", "缺失模块JS"),
    ]
    
    # 执行测试
    passed = 0
    total = len(test_cases)
    
    for url, description in test_cases:
        if test_api_endpoint(url, description):
            passed += 1
        time.sleep(0.5)  # 避免请求过于频繁
    
    # 测试总结
    print(f"\n{'='*60}")
    print("测试总结")
    print(f"{'='*60}")
    print(f"总测试数: {total}")
    print(f"通过测试: {passed}")
    print(f"失败测试: {total - passed}")
    print(f"通过率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常。")
    elif passed > total * 0.8:
        print("⚠️  大部分测试通过，系统基本正常。")
    else:
        print("❌ 多个测试失败，请检查系统配置。")
    
    print(f"\n测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()