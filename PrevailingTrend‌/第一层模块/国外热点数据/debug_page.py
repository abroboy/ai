#!/usr/bin/env python3
"""
调试脚本 - 直接打开页面检查错误
"""

import asyncio
from playwright.async_api import async_playwright
import sys

async def debug_page():
    """调试页面"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        try:
            print("🔍 正在打开页面...")
            await page.goto("http://localhost:5004/dashboard")
            
            # 等待页面加载
            await page.wait_for_load_state("networkidle")
            
            # 监听所有控制台消息
            console_messages = []
            page.on("console", lambda msg: console_messages.append(msg))
            
            # 等待JavaScript执行
            print("⏳ 等待JavaScript执行...")
            await asyncio.sleep(10)
            
            # 打印所有控制台消息
            print("\n📋 控制台消息:")
            for msg in console_messages:
                print(f"[{msg.type}] {msg.text}")
            
            # 检查是否有heat_score错误
            heat_score_errors = [msg for msg in console_messages if "heat_score.toFixed" in msg.text]
            if heat_score_errors:
                print(f"\n❌ 发现 {len(heat_score_errors)} 个heat_score错误:")
                for error in heat_score_errors:
                    print(f"  - {error.text}")
            else:
                print("\n✅ 未发现heat_score错误")
            
            # 截图
            await page.screenshot(path="debug_page.png")
            print("\n📸 截图已保存: debug_page.png")
            
            # 获取页面源码
            content = await page.content()
            with open("debug_page_source.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("📄 页面源码已保存: debug_page_source.html")
            
            return len(heat_score_errors) == 0
            
        except Exception as e:
            print(f"❌ 调试失败: {e}")
            return False
        finally:
            await browser.close()

async def main():
    """主函数"""
    print("🚀 开始调试页面")
    success = await debug_page()
    
    if success:
        print("\n✅ 调试完成，未发现heat_score错误")
    else:
        print("\n❌ 调试完成，发现heat_score错误")
    
    return 0 if success else 1

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result) 