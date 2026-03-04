#!/usr/bin/env python3
import requests
import sys

# 禁用SSL警告（仅用于测试）
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_login():
    login_url = "https://lazycat1012.heiyu.space/sys/login"
    obsidian_url = "https://obsidian.lazycat1012.heiyu.space/"
    
    # 凭据
    username = "shiery"
    password = "Znli1349."
    
    print(f"尝试登录: {login_url}")
    print(f"目标URL: {obsidian_url}")
    print(f"用户名: {username}")
    
    # 创建会话
    session = requests.Session()
    
    try:
        # 首先获取登录页面，获取可能的CSRF token等
        print("\n1. 获取登录页面...")
        response = session.get(login_url, verify=False, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应长度: {len(response.text)} 字符")
        
        # 尝试登录（需要查看实际的登录表单结构）
        # 这里需要根据实际的登录表单来调整
        login_data = {
            'username': username,
            'password': password,
            # 可能需要其他字段如csrf token等
        }
        
        print("\n2. 尝试登录...")
        response = session.post(login_url, data=login_data, verify=False, timeout=10)
        print(f"登录状态码: {response.status_code}")
        print(f"重定向: {response.history}")
        
        if response.history:
            for resp in response.history:
                print(f"  重定向: {resp.status_code} -> {resp.headers.get('location', 'N/A')}")
        
        print(f"最终URL: {response.url}")
        print(f"响应长度: {len(response.text)} 字符")
        
        # 尝试访问Obsidian页面
        print("\n3. 尝试访问Obsidian...")
        response = session.get(obsidian_url, verify=False, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"标题前100字符: {response.text[:100] if response.text else '空响应'}")
        
        # 保存响应内容供查看
        with open('/home/node/clawd/obsidian_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\n响应已保存到: /home/node/clawd/obsidian_response.html")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_login()