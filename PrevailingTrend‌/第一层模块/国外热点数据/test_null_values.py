#!/usr/bin/env python3
"""
测试null值处理的脚本
"""

import asyncio
from playwright.async_api import async_playwright
import sys
import json

async def test_null_values():
    """测试null值处理"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        try:
            print("🔍 测试null值处理...")
            
            # 创建一个测试页面
            test_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Null值测试</title>
            </head>
            <body>
                <div id="result"></div>
                <script>
                    // 模拟热点数据
                    const testData = [
                        {
                            title: "测试1",
                            heat_score: null,
                            sentiment_score: null
                        },
                        {
                            title: "测试2", 
                            heat_score: "9.2",
                            sentiment_score: 0.5
                        },
                        {
                            title: "测试3",
                            heat_score: undefined,
                            sentiment_score: undefined
                        }
                    ];
                    
                    // 测试处理函数
                    function processHeatScore(score) {
                        if (score === null || score === undefined) {
                            return '-';
                        }
                        
                        let numericScore;
                        if (typeof score === 'string') {
                            numericScore = parseFloat(score);
                        } else if (typeof score === 'number') {
                            numericScore = score;
                        } else if (score && typeof score.toString === 'function') {
                            numericScore = parseFloat(score.toString());
                        } else {
                            numericScore = parseFloat(score);
                        }
                        
                        if (!isNaN(numericScore)) {
                            return numericScore.toFixed(1);
                        }
                        return '-';
                    }
                    
                    function processSentimentScore(score) {
                        if (score === null || score === undefined) {
                            return '中性';
                        }
                        
                        let numericScore;
                        if (typeof score === 'string') {
                            numericScore = parseFloat(score);
                        } else if (typeof score === 'number') {
                            numericScore = score;
                        } else if (score && typeof score.toString === 'function') {
                            numericScore = parseFloat(score.toString());
                        } else {
                            numericScore = parseFloat(score);
                        }
                        
                        if (isNaN(numericScore)) {
                            return '中性';
                        }
                        
                        if (numericScore > 0.3) return '正面';
                        if (numericScore < -0.3) return '负面';
                        return '中性';
                    }
                    
                    // 处理测试数据
                    const results = testData.map((item, index) => {
                        const heatScore = processHeatScore(item.heat_score);
                        const sentiment = processSentimentScore(item.sentiment_score);
                        return `测试${index + 1}: heat_score=${item.heat_score} -> ${heatScore}, sentiment=${item.sentiment_score} -> ${sentiment}`;
                    });
                    
                    document.getElementById('result').innerHTML = results.join('<br>');
                    console.log('测试结果:', results);
                </script>
            </body>
            </html>
            """
            
            # 设置页面内容
            await page.set_content(test_html)
            
            # 等待JavaScript执行
            await asyncio.sleep(3)
            
            # 获取结果
            result_text = await page.text_content('#result')
            print("📋 测试结果:")
            print(result_text)
            
            # 检查控制台消息
            console_messages = []
            page.on("console", lambda msg: console_messages.append(msg))
            
            await asyncio.sleep(2)
            
            print("\n📋 控制台消息:")
            for msg in console_messages:
                print(f"[{msg.type}] {msg.text}")
            
            # 截图
            await page.screenshot(path="null_test_result.png")
            print("\n📸 截图已保存: null_test_result.png")
            
            return True
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False
        finally:
            await browser.close()

async def main():
    """主函数"""
    print("🚀 开始null值处理测试")
    success = await test_null_values()
    
    if success:
        print("\n✅ 测试完成")
    else:
        print("\n❌ 测试失败")
    
    return 0 if success else 1

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result) 