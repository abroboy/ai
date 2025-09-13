#!/usr/bin/env python3
"""
简化的Playwright测试脚本
"""

import asyncio
from playwright.async_api import async_playwright
import sys

async def test_dashboard():
    """测试Dashboard页面"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        try:
            print("🔍 访问Dashboard页面...")
            await page.goto("http://localhost:5004/dashboard")
            
            # 等待页面加载
            await page.wait_for_load_state("networkidle")
            
            # 检查页面标题
            title = await page.title()
            print(f"📄 页面标题: {title}")
            
            # 检查是否有heat_score错误
            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg) if msg.type == "error" else None)
            
            # 等待一段时间让JavaScript执行
            await asyncio.sleep(5)
            
            # 检查控制台错误
            heat_score_error = False
            for error in console_errors:
                if "heat_score.toFixed is not a function" in error.text:
                    heat_score_error = True
                    print(f"❌ 检测到heat_score错误: {error.text}")
                    break
            
            if not heat_score_error:
                print("✅ 未检测到heat_score错误")
            
            # 截图
            await page.screenshot(path="dashboard_test.png")
            print("📸 截图已保存: dashboard_test.png")
            
            return not heat_score_error
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False
        finally:
            await browser.close()

async def main():
    """主函数"""
    print("🚀 开始简化测试")
    success = await test_dashboard()
    
    if success:
        print("✅ 测试通过！")
    else:
        print("❌ 测试失败！")
    
    return 0 if success else 1

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result) 