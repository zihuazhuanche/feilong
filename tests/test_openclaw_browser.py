
import asyncio
import aiohttp
import json

async def test_browser_connection():
    """测试浏览器连接"""
    print("测试OpenClaw浏览器连接...")
    
    # 尝试连接不同的CDP端口
    ports = [
        (18792, "Chrome扩展"),
        (18800, "OpenClaw浏览器"),
        (9222, "Chrome远程调试"),
    ]
    
    for port, description in ports:
        try:
            print(f"\n尝试连接 {description} (端口 {port})...")
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://127.0.0.1:{port}/json/version", timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"  ✅ 连接成功!")
                        print(f"     浏览器: {data.get('Browser', 'N/A')}")
                        print(f"     协议: {data.get('Protocol-Version', 'N/A')}")
                        print(f"     WebSocket: {data.get('webSocketDebuggerUrl', 'N/A')}")
                        return port, description, data
                    else:
                        print(f"  ❌ HTTP {response.status}: {await response.text()[:100]}")
        except Exception as e:
            print(f"  ❌ 连接错误: {e}")
    
    print("\n❌ 所有连接尝试都失败")
    return None

async def test_obsidian_access():
    """测试访问Obsidian"""
    print("\n测试访问Obsidian网站...")
    
    # 使用aiohttp直接测试
    url = "https://obsidian.lazycat1012.heiyu.space/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10, ssl=False) as response:
                print(f"  状态码: {response.status}")
                print(f"  最终URL: {response.url}")
                print(f"  内容类型: {response.headers.get('Content-Type', 'N/A')}")
                
                # 读取部分内容
                content = await response.text()
                print(f"  内容长度: {len(content)} 字符")
                
                # 检查标题
                import re
                title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE)
                if title_match:
                    print(f"  页面标题: {title_match.group(1)}")
                else:
                    print("  未找到页面标题")
                
                return response.status, str(response.url)
    except Exception as e:
        print(f"  ❌ 访问错误: {e}")
        return None

async def main():
    print("开始OpenClaw浏览器测试...")
    print("=" * 70)
    
    # 测试连接
    connection = await test_browser_connection()
    
    # 测试网站访问
    access_result = await test_obsidian_access()
    
    print("\n" + "=" * 70)
    print("测试完成!")
    
    # 生成报告
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "browser_connection": "成功" if connection else "失败",
        "obsidian_access": "成功" if access_result else "失败",
        "connection_details": connection,
        "access_details": access_result,
    }
    
    # 保存报告
    import json
    with open('/home/node/clawd/browser_test_report.json', 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"测试报告已保存: /home/node/clawd/browser_test_report.json")
    
    return report

if __name__ == "__main__":
    import time
    report = asyncio.run(main())
    
    # 打印总结
    print("\n📊 测试总结:")
    print(f"  浏览器连接: {'✅ 成功' if report['browser_connection'] == '成功' else '❌ 失败'}")
    print(f"  Obsidian访问: {'✅ 成功' if report['obsidian_access'] == '成功' else '❌ 失败'}")
    
    if report['connection_details']:
        port, desc, info = report['connection_details']
        print(f"  连接类型: {desc} (端口 {port})")
