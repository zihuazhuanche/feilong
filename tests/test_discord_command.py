#!/usr/bin/env python3
"""
测试 Discord 命令是否正常工作
"""

import subprocess
import time
import sys

def test_discord_connection():
    print("测试 Discord 连接...")
    
    # 检查 Gateway 状态
    print("1. 检查 Gateway 状态:")
    result = subprocess.run(["openclaw", "status"], capture_output=True, text=True)
    print(result.stdout[:500])
    
    # 检查 Discord 状态
    print("\n2. 检查 Discord 状态:")
    result = subprocess.run(["openclaw", "channels", "status"], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'discord' in line.lower():
            print(f"   {line}")
    
    # 检查日志中是否有错误
    print("\n3. 检查最近日志:")
    result = subprocess.run(["openclaw", "logs", "--limit", "20"], capture_output=True, text=True)
    error_lines = []
    for line in result.stdout.split('\n'):
        if 'error' in line.lower() or 'failed' in line.lower() or 'unknown' in line.lower():
            error_lines.append(line)
    
    if error_lines:
        print("  发现错误:")
        for err in error_lines[:5]:
            print(f"    {err}")
    else:
        print("  未发现错误")
    
    # 检查配置
    print("\n4. 检查当前配置:")
    result = subprocess.run(["openclaw", "config", "get", "models.providers"], capture_output=True, text=True)
    print(f"  模型提供商: {list(eval(result.stdout).keys())}")
    
    # 测试建议
    print("\n5. 测试建议:")
    print("  - 在 Discord 中发送消息测试")
    print("  - 检查是否还有 'Unknown model' 错误")
    print("  - 如果仍有错误，可能需要检查 Discord 插件代码")
    
    return 0

if __name__ == "__main__":
    sys.exit(test_discord_connection())