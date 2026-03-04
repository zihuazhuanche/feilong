#!/usr/bin/env python3
"""
测试 NotebookLM 登录的简单脚本
"""

import asyncio
from playwright.async_api import async_playwright
import os

async def test_notebooklm_access():
    """测试是否能访问 NotebookLM"""
    print("🚀 启动浏览器测试...")
    
    async with async_playwright() as p:
        # 使用系统 Chromium
        browser = await p.chromium.launch(
            executable_path="/usr/bin/chromium",
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 1024},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        
        try:
            print("🌐 导航到 NotebookLM...")
            await page.goto('https://notebooklm.google.com', wait_until='domcontentloaded', timeout=30000)
            
            # 检查当前 URL
            current_url = page.url
            print(f"📋 当前 URL: {current_url}")
            
            # 检查页面标题
            title = await page.title()
            print(f"📄 页面标题: {title}")
            
            # 检查是否有登录表单
            login_form = await page.query_selector('input[type="email"], input[type="password"]')
            if login_form:
                print("🔐 检测到登录表单")
                
                # 截图保存
                await page.screenshot(path='/tmp/notebooklm_login.png')
                print("📸 截图已保存: /tmp/notebooklm_login.png")
                
                # 检查页面内容
                content = await page.content()
                if 'Sign in' in content or '登录' in content or 'signin' in current_url:
                    print("⚠️  需要登录 Google 账号")
                    
                    # 尝试自动填写（需要账号密码）
                    # 注意：这通常会被 Google 安全机制阻止
                    email_input = await page.query_selector('input[type="email"]')
                    if email_input:
                        print("📧 找到邮箱输入框")
                        # 这里需要你的 Google 邮箱
                        # await email_input.fill('your-email@gmail.com')
                    
                    return False
                else:
                    print("✅ 可能已经登录或不需要登录")
                    return True
            else:
                print("✅ 没有检测到登录表单，可能已登录")
                return True
                
        except Exception as e:
            print(f"❌ 错误: {e}")
            return False
        finally:
            await browser.close()

async def test_google_login():
    """测试 Google 登录流程"""
    print("\n🔐 测试 Google 登录流程...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/usr/bin/chromium",
            headless=False,  # 非无头模式，可以看到浏览器
            args=['--no-sandbox', '--disable-dev-shm-usage', '--window-size=1280,1024']
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 1024}
        )
        
        page = await context.new_page()
        
        try:
            # 直接导航到 Google 登录页面
            print("🌐 导航到 Google 登录...")
            await page.goto('https://accounts.google.com', wait_until='domcontentloaded')
            
            # 截图
            await page.screenshot(path='/tmp/google_login.png')
            print("📸 Google 登录页面截图: /tmp/google_login.png")
            
            # 检查页面元素
            email_field = await page.query_selector('input[type="email"]')
            if email_field:
                print("📧 找到 Google 邮箱输入框")
                print("⚠️  需要手动输入邮箱和密码")
                print("💡 提示: 在浏览器窗口中手动登录")
                
                # 等待一段时间让用户手动登录
                print("⏳ 等待 60 秒供手动登录...")
                await asyncio.sleep(60)
                
                # 检查是否登录成功
                current_url = page.url
                if 'myaccount.google.com' in current_url or 'notebooklm.google.com' in current_url:
                    print("✅ 登录成功!")
                    
                    # 保存 cookies
                    cookies = await context.cookies()
                    print(f"🍪 获取到 {len(cookies)} 个 cookies")
                    
                    # 保存浏览器状态
                    await context.storage_state(path='/tmp/browser_state.json')
                    print("💾 浏览器状态已保存: /tmp/browser_state.json")
                    
                    return True
                else:
                    print("❌ 登录未完成")
                    return False
            else:
                print("❌ 未找到邮箱输入框")
                return False
                
        except Exception as e:
            print(f"❌ 错误: {e}")
            return False
        finally:
            await browser.close()

async def main():
    """主函数"""
    print("=" * 50)
    print("NotebookLM 登录测试")
    print("=" * 50)
    
    # 测试 1: 直接访问 NotebookLM
    print("\n1. 测试直接访问 NotebookLM:")
    result1 = await test_notebooklm_access()
    
    if not result1:
        print("\n2. 尝试 Google 登录流程:")
        # 注意：在 Docker 中，headless=False 可能无法显示浏览器
        # 需要 X11 转发或虚拟显示
        result2 = await test_google_login()
    else:
        print("\n🎉 可以直接访问 NotebookLM!")
        
    print("\n" + "=" * 50)
    print("测试完成")

if __name__ == "__main__":
    # 在虚拟显示中运行
    asyncio.run(main())