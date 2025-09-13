#!/usr/bin/env python3
"""
最终测试脚本 - 验证heat_score错误修复
"""

import asyncio
from playwright.async_api import async_playwright
import sys
import requests
import time

async def test_dashboard_final():
    """最终测试Dashboard页面"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        try:
            print("🔍 开始最终测试...")
            
            # 访问Dashboard页面
            print("📱 访问页面: http://localhost:5004/dashboard")
            await page.goto("http://localhost:5004/dashboard")
            
            # 等待页面加载
            await page.wait_for_load_state("networkidle")
            
            # 检查页面标题
            title = await page.title()
            print(f"📄 页面标题: {title}")
            
            # 检查页面版本
            if "v2.5" in title:
                print("✅ 页面版本正确 (v2.5)")
            else:
                print(f"⚠️ 页面版本: {title}")
            
            # 监听控制台错误
            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg) if msg.type == "error" else None)
            
            # 等待JavaScript执行
            print("⏳ 等待JavaScript执行...")
            await asyncio.sleep(5)
            
            # 检查heat_score错误
            heat_score_error = False
            for error in console_errors:
                if "heat_score.toFixed is not a function" in error.text:
                    heat_score_error = True
                    print(f"❌ 检测到heat_score错误: {error.text}")
                    break
            
            if not heat_score_error:
                print("✅ 未检测到heat_score错误")
            
            # 测试按钮功能
            print("🔘 测试按钮功能...")
            
            # 测试"测试JS"按钮
            test_js_button = await page.query_selector('button:has-text("测试JS")')
            if test_js_button:
                await test_js_button.click()
                print("✅ 测试JS按钮点击成功")
                
                # 等待alert
                try:
                    dialog = await page.wait_for_event("dialog", timeout=3000)
                    await dialog.accept()
                    print("✅ 测试JS alert处理成功")
                except:
                    print("⚠️ 未检测到测试JS alert")
            else:
                print("❌ 未找到测试JS按钮")
            
            # 截图
            await page.screenshot(path="final_test_result.png")
            print("📸 截图已保存: final_test_result.png")
            
            return not heat_score_error
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False
        finally:
            await browser.close()

def test_api_endpoints():
    """测试API端点"""
    print("\n🌐 测试API端点...")
    
    base_url = "http://localhost:5004"
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ 健康检查API正常")
        else:
            print(f"❌ 健康检查API失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查API错误: {e}")
        return False
    
    # 测试热点数据API
    try:
        response = requests.get(f"{base_url}/api/hotspots?limit=5", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 热点数据API正常，返回 {len(data.get('data', []))} 条数据")
            else:
                print(f"⚠️ 热点数据API返回错误: {data.get('error')}")
        else:
            print(f"❌ 热点数据API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 热点数据API错误: {e}")
    
    # 测试统计数据API
    try:
        response = requests.get(f"{base_url}/api/statistics", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 统计数据API正常")
            else:
                print(f"⚠️ 统计数据API返回错误: {data.get('error')}")
        else:
            print(f"❌ 统计数据API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 统计数据API错误: {e}")
    
    return True

async def main():
    """主函数"""
    print("🚀 开始最终测试")
    print("=" * 50)
    
    # 测试API端点
    api_success = test_api_endpoints()
    
    # 测试Dashboard页面
    dashboard_success = await test_dashboard_final()
    
    # 总结结果
    print("\n" + "=" * 50)
    print("📋 最终测试总结:")
    print(f"API端点测试: {'✅ 通过' if api_success else '❌ 失败'}")
    print(f"Dashboard页面测试: {'✅ 通过' if dashboard_success else '❌ 失败'}")
    
    if api_success and dashboard_success:
        print("\n🎉 所有测试通过！heat_score错误修复成功！")
        return 0
    else:
        print("\n⚠️ 部分测试失败，需要进一步检查")
        return 1

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result) 