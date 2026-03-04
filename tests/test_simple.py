#!/usr/bin/env python3
"""
简化测试 - 不依赖外部API
"""

import sys
import os
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 模拟 google.generativeai 模块
class MockGenAI:
    class GenerativeModel:
        def generate_content(self, prompt):
            return type('obj', (object,), {'text': f"[Mock Gemini] 响应: {prompt[:100]}..."})()

def mock_import(name, *args, **kwargs):
    if name == 'google.generativeai':
        sys.modules['google'] = type('module', (object,), {})()
        sys.modules['google.generativeai'] = MockGenAI()
        return sys.modules['google.generativeai']
    raise ImportError(f"No module named '{name}'")

# 替换导入
import builtins
original_import = builtins.__import__
builtins.__import__ = mock_import

try:
    from scripts.ai_assistant import AIAssistant
    from scripts.openclaw_integration import OpenClawAIAssistant
    
    print("✅ 导入成功")
    
    # 测试初始化
    print("\n1. 测试初始化...")
    assistant = AIAssistant()
    print("   AI Assistant 初始化成功")
    
    # 测试统计
    print("\n2. 测试统计信息...")
    stats = assistant.get_stats()
    print(f"   可用大脑: {stats.get('available_brains', [])}")
    
    # 测试本地问答
    print("\n3. 测试本地问答...")
    answer = assistant.ask("测试问题", brain="local_llm")
    print(f"   回答: {answer[:200]}...")
    
    # 测试代码生成
    print("\n4. 测试代码生成...")
    code = assistant.generate_code("python", "打印Hello World")
    print(f"   生成的代码: {code[:200]}...")
    
    # 测试OpenClaw集成
    print("\n5. 测试OpenClaw集成...")
    integration = OpenClawAIAssistant()
    caps = integration.get_capabilities()
    print(f"   技能名称: {caps.get('name')}")
    
    print("\n🎉 简化测试通过！")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
finally:
    # 恢复原始导入
    builtins.__import__ = original_import
