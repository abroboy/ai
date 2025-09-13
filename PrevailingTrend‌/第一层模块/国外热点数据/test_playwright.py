#!/usr/bin/env python3
"""
使用Playwright自动化测试国外热点数据页面
验证heat_score错误修复是否生效
"""

import asyncio
import time
from playwright.async_api import async_playwright
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class DashboardTester:
    def __init__(self, base_url="http://localhost:5004"):
        self.base_url = base_url
        self.browser = None
        self.page = None
        
    async def setup(self):
        """初始化浏览器"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False,  # 显示浏览器窗口
            slow_mo=1000     # 放慢操作速度，便于观察
        )
        self.page = await self.browser.new_page()
        
        # 设置视口大小
        await self.page.set_viewport_size({"width": 1280, "height": 720})
        
        # 监听控制台消息
        self.page.on("console", self.handle_console)
        
    async def handle_console(self, msg):
        """处理控制台消息"""
        print(f"[控制台] {msg.type}: {msg.text}")
        
    async def test_dashboard_page(self):
        """测试Dashboard页面"""
        print("🔍 开始测试Dashboard页面...")
        
        try:
            # 访问Dashboard页面
            print(f"📱 访问页面: {self.base_url}/dashboard")
            await self.page.goto(f"{self.base_url}/dashboard", wait_until="networkidle")
            
            # 强制刷新页面以确保获取最新版本
            await self.page.reload(wait_until="networkidle")
            
            # 等待页面加载
            await self.page.wait_for_load_state("networkidle")
            
            # 检查页面标题
            title = await self.page.title()
            print(f"📄 页面标题: {title}")
            
            # 检查页面版本
            if "v2.5" in title:
                print("✅ 页面版本正确 (v2.5)")
            elif "v2.4" in title:
                print("⚠️ 页面版本是v2.4，可能需要刷新")
            else:
                print(f"❌ 页面版本不正确: {title}")
                return False
            
            # 等待页面结构加载
            await self.page.wait_for_selector("#hotspotsTableBody", timeout=10000)
            print("✅ 页面结构加载完成")
            
            # 检查是否有JavaScript错误
            console_errors = []
            self.page.on("console", lambda msg: console_errors.append(msg) if msg.type == "error" else None)
            
            # 等待数据加载
            print("⏳ 等待数据加载...")
            await asyncio.sleep(3)
            
            # 检查是否有heat_score错误
            page_content = await self.page.content()
            if "heat_score.toFixed is not a function" in page_content:
                print("❌ 检测到heat_score错误")
                return False
            else:
                print("✅ 未检测到heat_score错误")
            
            # 测试按钮功能
            print("🔘 测试按钮功能...")
            
            # 测试"测试JS"按钮
            test_js_button = await self.page.query_selector('button:has-text("测试JS")')
            if test_js_button:
                await test_js_button.click()
                print("✅ 测试JS按钮点击成功")
                
                # 等待alert出现
                try:
                    dialog = await self.page.wait_for_event("dialog", timeout=3000)
                    await dialog.accept()
                    print("✅ 测试JS alert处理成功")
                except:
                    print("⚠️ 未检测到测试JS alert")
            else:
                print("❌ 未找到测试JS按钮")
            
            # 测试"刷新数据"按钮
            refresh_button = await self.page.query_selector('button:has-text("刷新数据")')
            if refresh_button:
                await refresh_button.click()
                print("✅ 刷新数据按钮点击成功")
                
                # 等待alert出现
                try:
                    dialog = await self.page.wait_for_event("dialog", timeout=3000)
                    await dialog.accept()
                    print("✅ 刷新数据 alert处理成功")
                except:
                    print("⚠️ 未检测到刷新数据 alert")
            else:
                print("❌ 未找到刷新数据按钮")
            
            # 测试"收集数据"按钮
            collect_button = await self.page.query_selector('button:has-text("收集数据")')
            if collect_button:
                await collect_button.click()
                print("✅ 收集数据按钮点击成功")
                
                # 等待alert出现
                try:
                    dialog = await self.page.wait_for_event("dialog", timeout=3000)
                    await dialog.accept()
                    print("✅ 收集数据 alert处理成功")
                except:
                    print("⚠️ 未检测到收集数据 alert")
            else:
                print("❌ 未找到收集数据按钮")
            
            # 检查数据表格
            print("📊 检查数据表格...")
            table_body = await self.page.query_selector("#hotspotsTableBody")
            if table_body:
                rows = await table_body.query_selector_all("tr")
                print(f"✅ 数据表格加载成功，共 {len(rows)} 行数据")
                
                # 检查第一行数据
                if len(rows) > 0:
                    first_row = rows[0]
                    cells = await first_row.query_selector_all("td")
                    if len(cells) >= 5:  # 至少有5列（包括heat_score列）
                        heat_score_cell = cells[4]  # 第5列是heat_score
                        heat_score_text = await heat_score_cell.text_content()
                        print(f"✅ 第一行heat_score值: {heat_score_text}")
                    else:
                        print("⚠️ 数据行列数不足")
                else:
                    print("⚠️ 数据表格为空")
            else:
                print("❌ 未找到数据表格")
            
            # 截图保存
            screenshot_path = "dashboard_test_result.png"
            await self.page.screenshot(path=screenshot_path)
            print(f"📸 截图已保存: {screenshot_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ 测试过程中发生错误: {e}")
            # 出错时也截图
            try:
                screenshot_path = "dashboard_test_error.png"
                await self.page.screenshot(path=screenshot_path)
                print(f"📸 错误截图已保存: {screenshot_path}")
            except:
                pass
            return False
    
    async def test_simple_test_page(self):
        """测试简单测试页面"""
        print("\n🔍 开始测试简单测试页面...")
        
        try:
            # 访问简单测试页面
            print(f"📱 访问页面: {self.base_url}/simple-test")
            await self.page.goto(f"{self.base_url}/simple-test")
            
            # 等待页面加载
            await self.page.wait_for_load_state("networkidle")
            
            # 检查页面标题
            title = await self.page.title()
            print(f"📄 页面标题: {title}")
            
            # 等待页面结构加载
            await self.page.wait_for_selector("#testResults", timeout=10000)
            print("✅ 测试页面结构加载完成")
            
            # 点击"运行所有测试"按钮
            run_tests_button = await self.page.query_selector('button:has-text("运行所有测试")')
            if run_tests_button:
                await run_tests_button.click()
                print("✅ 点击运行所有测试按钮")
                
                # 等待测试完成
                await asyncio.sleep(3)
                
                # 检查测试结果
                test_results = await self.page.query_selector("#testResults")
                if test_results:
                    results_text = await test_results.text_content()
                    print("📊 测试结果:")
                    print(results_text)
                    
                    # 检查是否包含成功信息
                    if "7/7 测试通过" in results_text and "API测试通过" in results_text:
                        print("✅ 所有测试通过")
                        return True
                    else:
                        print("❌ 部分测试失败")
                        return False
                else:
                    print("❌ 未找到测试结果")
                    return False
            else:
                print("❌ 未找到运行所有测试按钮")
                return False
                
        except Exception as e:
            print(f"❌ 简单测试页面测试过程中发生错误: {e}")
            return False
    
    async def cleanup(self):
        """清理资源"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()

async def main():
    """主函数"""
    print("🚀 开始自动化测试国外热点数据页面")
    print("=" * 50)
    
    tester = DashboardTester()
    
    try:
        await tester.setup()
        
        # 测试Dashboard页面
        dashboard_success = await tester.test_dashboard_page()
        
        # 测试简单测试页面
        simple_test_success = await tester.test_simple_test_page()
        
        # 总结结果
        print("\n" + "=" * 50)
        print("📋 测试总结:")
        print(f"Dashboard页面测试: {'✅ 通过' if dashboard_success else '❌ 失败'}")
        print(f"简单测试页面测试: {'✅ 通过' if simple_test_success else '❌ 失败'}")
        
        if dashboard_success and simple_test_success:
            print("\n🎉 所有测试通过！heat_score错误修复成功！")
            return 0
        else:
            print("\n⚠️ 部分测试失败，需要进一步检查")
            return 1
            
    except Exception as e:
        print(f"❌ 测试过程中发生严重错误: {e}")
        return 1
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    # 检查是否安装了playwright
    try:
        import playwright
    except ImportError:
        print("❌ 未安装playwright，请先安装:")
        print("pip install playwright")
        print("playwright install chromium")
        sys.exit(1)
    
    # 运行测试
    result = asyncio.run(main())
    sys.exit(result) 