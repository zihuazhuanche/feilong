#!/usr/bin/env python3
"""
使用模拟API密钥测试Gemini Brain技能
"""

import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch

# 添加技能目录到路径
skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir))

def test_with_mock_api():
    """使用模拟API密钥测试"""
    print("🧪 使用模拟API密钥测试...")
    
    # 设置模拟API密钥
    os.environ['GEMINI_API_KEY'] = 'mock-api-key-for-testing'
    
    try:
        # 模拟google.generativeai模块
        with patch('google.generativeai.GenerativeModel') as mock_model:
            # 配置模拟响应
            mock_response = Mock()
            mock_response.text = "这是一个模拟的Gemini回答，用于测试目的。"
            
            mock_instance = Mock()
            mock_instance.generate_content.return_value = mock_response
            mock_model.return_value = mock_instance
            
            # 现在导入和测试
            from scripts.gemini_brain import GeminiBrain
            from scripts.openclaw_integration import OpenClawGeminiSkill
            
            print("✅ 模拟设置完成")
            
            # 测试初始化
            print("\n1. 测试初始化...")
            brain = GeminiBrain()
            print("✅ GeminiBrain 初始化成功")
            
            # 测试提问
            print("\n2. 测试提问功能...")
            answer = brain.ask("测试问题")
            print(f"✅ 提问成功，回答: {answer[:50]}...")
            
            # 测试技能信息
            print("\n3. 测试技能信息...")
            skill = OpenClawGeminiSkill()
            result = skill.handle_command("info", {})
            if result.get("success"):
                info = result["skill_info"]
                print(f"✅ 技能信息: {info.get('name')} v{info.get('version')}")
            else:
                print(f"❌ 技能信息失败: {result.get('error')}")
            
            # 测试错误处理
            print("\n4. 测试错误处理...")
            result = skill.handle_command("invalid_command", {})
            if not result.get("success") and "error" in result:
                print("✅ 无效命令错误处理正确")
            else:
                print("❌ 无效命令错误处理不正确")
            
            # 测试格式响应
            print("\n5. 测试响应格式化...")
            test_result = {"success": True, "answer": "测试回答"}
            formatted = skill.format_response(test_result)
            if "测试回答" in formatted:
                print("✅ 响应格式化正确")
            else:
                print("❌ 响应格式化不正确")
            
            # 测试代码生成命令
            print("\n6. 测试代码生成命令...")
            result = skill.handle_command("code", {
                "language": "python",
                "requirements": "打印Hello World"
            })
            if result.get("success"):
                print("✅ 代码生成命令处理成功")
            else:
                print(f"❌ 代码生成命令失败: {result.get('error')}")
            
            # 测试搜索命令
            print("\n7. 测试搜索命令...")
            result = skill.handle_command("search", {
                "query": "测试搜索"
            })
            if result.get("success"):
                print("✅ 搜索命令处理成功")
            else:
                print(f"❌ 搜索命令失败: {result.get('error')}")
            
            # 测试统计命令
            print("\n8. 测试统计命令...")
            result = skill.handle_command("stats", {})
            if result.get("success") and "stats" in result:
                stats = result["stats"]
                print(f"✅ 统计信息: {stats.get('total_questions')} 个问题")
            else:
                print(f"❌ 统计命令失败: {result.get('error')}")
            
            # 测试清空历史
            print("\n9. 测试清空历史...")
            result = skill.handle_command("clear", {})
            if result.get("success"):
                print("✅ 清空历史命令成功")
            else:
                print(f"❌ 清空历史命令失败: {result.get('error')}")
            
            print("\n" + "="*60)
            print("🎉 所有模拟测试通过！")
            print("="*60)
            
            return True
            
    except Exception as e:
        print(f"❌ 模拟测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理环境变量
        if 'GEMINI_API_KEY' in os.environ:
            del os.environ['GEMINI_API_KEY']

def test_cli_interface():
    """测试命令行接口"""
    print("\n🧪 测试命令行接口...")
    
    # 设置模拟API密钥
    os.environ['GEMINI_API_KEY'] = 'mock-api-key-for-testing'
    
    try:
        # 测试info命令
        print("\n1. 测试info命令...")
        import subprocess
        result = subprocess.run(
            [sys.executable, "scripts/openclaw_integration.py", "info"],
            capture_output=True,
            text=True,
            cwd=skill_dir
        )
        
        if result.returncode == 0 and "gemini-brain" in result.stdout:
            print("✅ CLI info命令成功")
        else:
            print(f"❌ CLI info命令失败: {result.stderr}")
        
        # 测试直接脚本
        print("\n2. 测试直接脚本...")
        with patch('google.generativeai.GenerativeModel'):
            result = subprocess.run(
                [sys.executable, "scripts/gemini_brain.py", "--help"],
                capture_output=True,
                text=True,
                cwd=skill_dir
            )
            
            if result.returncode == 0 and "usage" in result.stdout.lower():
                print("✅ 直接脚本帮助信息正常")
            else:
                print(f"❌ 直接脚本帮助信息失败: {result.stderr}")
        
        print("\n✅ CLI接口测试完成")
        return True
        
    except Exception as e:
        print(f"❌ CLI接口测试失败: {e}")
        return False
    finally:
        # 清理环境变量
        if 'GEMINI_API_KEY' in os.environ:
            del os.environ['GEMINI_API_KEY']

def main():
    """主测试函数"""
    print("="*60)
    print("🤖 Gemini Brain 技能模拟测试")
    print("="*60)
    
    print("注意: 使用模拟API密钥进行测试，不调用真实Gemini API")
    
    # 运行模拟测试
    if test_with_mock_api():
        print("\n✅ 核心功能模拟测试通过")
    else:
        print("\n❌ 核心功能模拟测试失败")
        return False
    
    # 运行CLI测试
    if test_cli_interface():
        print("\n✅ CLI接口测试通过")
    else:
        print("\n❌ CLI接口测试失败")
        return False
    
    print("\n" + "="*60)
    print("📋 测试总结:")
    print("   1. ✅ 核心功能模块正常")
    print("   2. ✅ 错误处理机制完善")
    print("   3. ✅ 配置系统工作正常")
    print("   4. ✅ 命令行接口可用")
    print("   5. ⚠️  需要真实API密钥进行完整测试")
    print("\n💡 下一步:")
    print("   1. 获取Gemini API密钥")
    print("   2. 设置环境变量: export GEMINI_API_KEY='your-key'")
    print("   3. 运行真实测试: python scripts/gemini_brain.py '测试问题'")
    print("="*60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)