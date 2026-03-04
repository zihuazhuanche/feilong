#!/usr/bin/env python3
"""
测试Discord token有效性
"""

import requests
import base64
import sys

def test_discord_token(token):
    """测试Discord token"""
    print("🔍 测试Discord token有效性")
    print("=" * 60)
    
    # 分析token
    parts = token.split('.')
    print(f"Token格式: {len(parts)}部分")
    
    if len(parts) >= 1:
        try:
            # 解码第一部分
            part1 = parts[0]
            padding = '=' * (4 - len(part1) % 4)
            decoded = base64.b64decode(part1 + padding).decode('utf-8')
            print(f"应用程序ID: {decoded}")
        except Exception as e:
            print(f"无法解码第一部分: {e}")
    
    # 测试API连接
    headers = {
        "Authorization": f"Bot {token}"
    }
    
    endpoints = [
        ("应用程序信息", "https://discord.com/api/v10/applications/@me"),
        ("网关信息", "https://discord.com/api/v10/gateway/bot"),
    ]
    
    for name, url in endpoints:
        print(f"\n📡 测试: {name}")
        print(f"  URL: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                print("  ✅ 连接成功!")
                try:
                    data = response.json()
                    print(f"  响应: {data}")
                except:
                    print(f"  响应: {response.text[:100]}...")
            elif response.status_code == 401:
                print("  ❌ 未授权 - token可能无效或已过期")
            elif response.status_code == 403:
                print("  ❌ 禁止访问 - 权限不足")
            elif response.status_code == 429:
                print("  ⚠️ 速率限制 - 请稍后重试")
            else:
                print(f"  ⚠️ 其他错误: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("  ⏱️ 请求超时 - 网络连接问题")
        except requests.exceptions.ConnectionError:
            print("  🔌 连接错误 - 无法连接到Discord API")
        except Exception as e:
            print(f"  ❌ 错误: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")

if __name__ == "__main__":
    # 从配置文件读取token
    import json
    import os
    
    config_path = "/home/node/.openclaw/openclaw.json"
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        token = config.get("channels", {}).get("discord", {}).get("token")
        
        if token:
            test_discord_token(token)
        else:
            print("❌ 配置文件中未找到Discord token")
    else:
        print(f"❌ 配置文件不存在: {config_path}")