#!/usr/bin/env python3
"""
探索OpenClaw的OAuth认证配置
"""

import json
import os

def explore_oauth_config():
    """探索OAuth配置选项"""
    print("🔍 探索OpenClaw OAuth认证配置")
    print("=" * 60)
    
    # 读取配置文件
    config_path = "/home/node/.openclaw/openclaw.json"
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # 检查OpenAI配置
        openai_config = config.get("models", {}).get("providers", {}).get("openai", {})
        
        print("当前OpenAI配置:")
        for key, value in openai_config.items():
            if key != "models":  # 跳过模型列表
                print(f"  {key}: {value}")
        
        print("\n📋 可能的OAuth配置方式:")
        print("1. auth: 'oauth' + apiKey: 'oauth-token'")
        print("2. auth: 'bearer' + apiKey: 'bearer-token'")
        print("3. auth: 'oauth2' + 其他OAuth参数")
        print("4. 使用accessToken字段（如果支持）")
        
        print("\n🔧 建议尝试的配置:")
        print("方案A: 使用Bearer token")
        print("  openclaw config set models.providers.openai.auth 'bearer'")
        print("  openclaw config set models.providers.openai.apiKey 'your-oauth-bearer-token'")
        
        print("\n方案B: 使用OAuth token")
        print("  openclaw config set models.providers.openai.auth 'oauth'")
        print("  openclaw config set models.providers.openai.apiKey 'your-oauth-token'")
        
        print("\n方案C: 检查OpenClaw文档")
        print("  查看 /app/npm-global/lib/node_modules/openclaw/docs/ 中的认证文档")
        
    else:
        print(f"❌ 配置文件不存在: {config_path}")
    
    print("\n" + "=" * 60)
    print("💡 OpenAI OAuth认证说明:")
    print("OpenAI支持多种认证方式:")
    print("1. API密钥 (sk-...开头)")
    print("2. OAuth 2.0 (需要client_id, client_secret)")
    print("3. Bearer token (oauth2访问令牌)")
    print("")
    print("你需要哪种OAuth认证？")
    print("A. OAuth客户端凭证 (client_id + client_secret)")
    print("B. OAuth访问令牌 (access_token)")
    print("C. Bearer令牌")

if __name__ == "__main__":
    explore_oauth_config()