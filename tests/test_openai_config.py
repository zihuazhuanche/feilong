#!/usr/bin/env python3
"""
测试OpenAI配置
"""

import json
import os

def test_openai_config():
    """测试OpenAI配置"""
    print("🔍 测试OpenAI配置")
    print("=" * 60)
    
    # 读取配置文件
    config_path = "/home/node/.openclaw/openclaw.json"
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # 检查OpenAI配置
        openai_config = config.get("models", {}).get("providers", {}).get("openai", {})
        
        if openai_config:
            print("✅ OpenAI配置找到")
            print(f"   基础URL: {openai_config.get('baseUrl')}")
            print(f"   认证方式: {openai_config.get('auth')}")
            print(f"   API类型: {openai_config.get('api')}")
            
            # 检查API密钥
            api_key = openai_config.get('apiKey', '')
            if api_key and api_key != "需要你的OpenAI API密钥":
                print(f"   API密钥: {api_key[:10]}... (已设置)")
            else:
                print("   ⚠️ API密钥: 需要设置有效的OpenAI API密钥")
            
            # 检查模型
            models = openai_config.get('models', [])
            print(f"   配置的模型数量: {len(models)}")
            
            for i, model in enumerate(models, 1):
                print(f"   {i}. {model.get('id')} - {model.get('name')}")
                print(f"      输入类型: {model.get('input')}")
                print(f"      推理能力: {model.get('reasoning')}")
                print(f"      上下文窗口: {model.get('contextWindow')}")
                print(f"      最大token: {model.get('maxTokens')}")
        else:
            print("❌ OpenAI配置未找到")
        
        # 检查默认代理配置
        agents_config = config.get("agents", {}).get("defaults", {}).get("model", {})
        print(f"\n🎯 默认代理模型配置:")
        print(f"   主要模型: {agents_config.get('primary')}")
        print(f"   备选模型: {agents_config.get('fallbacks', [])}")
        
    else:
        print(f"❌ 配置文件不存在: {config_path}")
    
    print("\n" + "=" * 60)
    print("📋 使用说明:")
    print("1. 确保已设置有效的OpenAI API密钥")
    print("2. 重启Gateway应用配置")
    print("3. 可以使用以下模型:")
    print("   - openai/gpt-4o")
    print("   - openai/gpt-4o-mini")
    print("4. 系统会自动在DeepSeek不可用时使用OpenAI模型")

if __name__ == "__main__":
    test_openai_config()