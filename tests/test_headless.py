
import asyncio
from pyppeteer import launch
import os

async def test_browser():
    print("测试无头浏览器...")
    try:
        # 尝试启动浏览器
        browser = await launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        print("✅ 浏览器启动成功")
        
        # 创建页面
        page = await browser.newPage()
        
        # 访问测试页面
        await page.goto('https://httpbin.org/ip', {'waitUntil': 'networkidle2'})
        
        # 获取页面内容
        content = await page.content()
        
        # 截图
        await page.screenshot({'path': '/home/node/clawd/browser_test_screenshot.png'})
        print("✅ 截图已保存: /home/node/clawd/browser_test_screenshot.png")
        
        # 获取标题
        title = await page.title()
        print(f"✅ 页面标题: {title}")
        
        await browser.close()
        print("✅ 浏览器已关闭")
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

# 运行测试
if __name__ == "__main__":
    success = asyncio.get_event_loop().run_until_complete(test_browser())
    if success:
        print("\n🎉 无头浏览器测试成功！")
    else:
        print("\n😞 无头浏览器测试失败")
