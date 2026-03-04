#!/usr/bin/env python3
"""
AI Assistant 基础测试脚本
测试核心功能是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from scripts.ai_assistant import AIAssistant
from scripts.openclaw_integration import OpenClawAIAssistant, openclaw_handler

def test_ai_assistant():
    """测试 AI Assistant 核心功能"""
    print("=" * 60)
    print("测试 AI Assistant 核心功能")
    print("=" * 60)
    
    try:
        # 创建助手实例
        print("\n1. 初始化 AI Assistant...")
        assistant = AIAssistant()
        
        # 测试统计信息
        print("\n2. 测试统计信息...")
        stats = assistant.get_stats()
        print(f"  可用大脑: {stats.get('available_brains', [])}")
        print(f"  配置状态: {stats.get('config', {})}")
        
        # 测试简单问答（使用本地 LLM）
        print("\n3. 测试简单问答（本地 LLM）...")
        question = "请用一句话介绍 AI Assistant"
        answer = assistant.ask(question, brain="local_llm")
        print(f"  问题: {question}")
        print(f"  回答: {answer[:200]}...")
        
        # 测试代码生成
        print("\n4. 测试代码生成...")
        code = assistant.generate_code("python", "打印Hello World")
        print(f"  生成的代码: {code[:200]}...")
        
        # 测试搜索增强
        print("\n5. 测试搜索增强...")
        search_result = assistant.search_enhanced("人工智能")
        print(f"  搜索结果: {search_result[:200]}...")
        
        # 测试缓存
        print("\n6. 测试缓存功能...")
        # 第一次询问
        answer1 = assistant.ask("测试缓存的问题")
        # 第二次询问同样的问题（应该从缓存获取）
        answer2 = assistant.ask("测试缓存的问题")
        print(f"  第一次回答长度: {len(answer1)}")
        print(f"  第二次回答长度: {len(answer2)}")
        print(f"  缓存是否生效: {'是' if answer1 == answer2 else '否'}")
        
        # 测试清空历史
        print("\n7. 测试清空对话历史...")
        assistant.clear_history()
        print("  对话历史已清空")
        
        print("\n✅ AI Assistant 核心功能测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ AI Assistant 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_openclaw_integration():
    """测试 OpenClaw 集成"""
    print("\n" + "=" * 60)
    print("测试 OpenClaw 集成")
    print("=" * 60)
    
    try:
        # 创建集成实例
        print("\n1. 初始化 OpenClaw 集成...")
        integration = OpenClawAIAssistant()
        
        # 测试能力查询
        print("\n2. 测试能力查询...")
        caps = integration.get_capabilities()
        print(f"  技能名称: {caps.get('name')}")
        print(f"  版本: {caps.get('version')}")
        print(f"  可用能力: {list(caps.get('capabilities', {}).keys())}")
        
        # 测试请求处理
        print("\n3. 测试请求处理...")
        
        # 测试问答请求
        result = integration.handle_request({
            "type": "ask",
            "text": "AI Assistant 是什么？"
        })
        print(f"  问答请求结果: {result.get('success', False)}")
        if result.get("answer"):
            print(f"  回答预览: {result['answer'][:150]}...")
        
        # 测试代码生成请求
        result = integration.handle_request({
            "type": "code",
            "language": "python",
            "requirements": "一个简单的函数"
        })
        print(f"  代码生成结果: {result.get('success', False)}")
        
        # 测试统计请求
        result = integration.handle_request({"type": "stats"})
        print(f"  统计请求结果: {result.get('success', False)}")
        
        # 测试清空请求
        result = integration.handle_request({"type": "clear"})
        print(f"  清空请求结果: {result.get('success', False)}")
        print(f"  消息: {result.get('message')}")
        
        # 测试 openclaw_handler 函数
        print("\n4. 测试 openclaw_handler 函数...")
        response = openclaw_handler("测试 handler 函数")
        print(f"  handler 响应: {response[:150]}...")
        
        print("\n✅ OpenClaw 集成测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ OpenClaw 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """测试配置功能"""
    print("\n" + "=" * 60)
    print("测试配置功能")
    print("=" * 60)
    
    try:
        # 测试默认配置
        print("\n1. 测试默认配置...")
        assistant = AIAssistant()
        default_stats = assistant.get_stats()
        print(f"  默认配置大脑: {default_stats.get('available_brains', [])}")
        
        # 测试自定义配置文件
        print("\n2. 测试自定义配置...")
        # 创建一个测试配置文件
        test_config = """
brains:
  gemini:
    enabled: false
  local_llm:
    enabled: true
  web_search:
    enabled: false
caching:
  enabled: false
conversation:
  memory_enabled: true
"""
        config_path = Path(__file__).parent / "test_config.yaml"
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(test_config)
        
        assistant2 = AIAssistant(str(config_path))
        custom_stats = assistant2.get_stats()
        print(f"  自定义配置大脑: {custom_stats.get('available_brains', [])}")
        
        # 清理测试文件
        config_path.unlink()
        
        print("\n✅ 配置功能测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 配置功能测试失败: {e}")
        # 清理可能创建的测试文件
        test_config = Path(__file__).parent / "test_config.yaml"
        if test_config.exists():
            test_config.unlink()
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n" + "=" * 60)
    print("测试错误处理")
    print("=" * 60)
    
    try:
        assistant = AIAssistant()
        
        # 测试无效大脑选择
        print("\n1. 测试无效大脑选择...")
        try:
            answer = assistant.ask("测试问题", brain="invalid_brain")
            print(f"  降级处理结果: {answer[:100]}...")
        except Exception as e:
            print(f"  错误处理: {e}")
        
        # 测试空问题
        print("\n2. 测试空问题处理...")
        integration = OpenClawAIAssistant()
        result = integration.handle_request({"type": "ask", "text": ""})
        print(f"  空问题结果: {result.get('success', False)}")
        print(f"  错误信息: {result.get('error')}")
        
        # 测试无效请求类型
        print("\n3. 测试无效请求类型...")
        result = integration.handle_request({"type": "invalid_type"})
        print(f"  无效类型结果: {result.get('success', False)}")
        print(f"  错误信息: {result.get('error')}")
        
        print("\n✅ 错误处理测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 错误处理测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("开始 AI Assistant 全面测试")
    print("=" * 60)
    
    results = []
    
    # 运行各个测试
    results.append(("AI Assistant 核心", test_ai_assistant()))
    results.append(("OpenClaw 集成", test_openclaw_integration()))
    results.append(("配置功能", test_configuration()))
    results.append(("错误处理", test_error_handling()))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name:20} {status}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n总计: {len(results)} 个测试")
    print(f"通过: {passed} 个")
    print(f"失败: {failed} 个")
    
    if failed == 0:
        print("\n🎉 所有测试通过！AI Assistant 可以正常使用。")
        return True
    else:
        print(f"\n⚠️  有 {failed} 个测试失败，请检查相关问题。")
        return False

if __name__ == "__main__":
    # 运行测试
    success = run_all_tests()
    
    # 退出码
    sys.exit(0 if success else 1)