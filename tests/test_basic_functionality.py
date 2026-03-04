#!/usr/bin/env python3
"""
测试Gemini Brain技能的基本功能
"""

import sys
import os
from pathlib import Path

# 添加技能目录到路径
skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir))

def test_imports():
    """测试模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        # 测试核心模块导入
        from scripts.gemini_brain import GeminiBrain
        print("✅ GeminiBrain 类导入成功")
        
        # 测试集成模块导入
        from scripts.openclaw_integration import OpenClawGeminiSkill
        print("✅ OpenClawGeminiSkill 类导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_config_loading():
    """测试配置加载"""
    print("\n🧪 测试配置加载...")
    
    try:
        # 检查配置文件
        config_path = skill_dir / "config.yaml"
        if config_path.exists():
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print(f"✅ 配置文件加载成功")
            print(f"   模型: {config.get('gemini', {}).get('model', '未设置')}")
            print(f"   温度: {config.get('gemini', {}).get('temperature', '未设置')}")
            return True
        else:
            print("❌ 配置文件不存在")
            return False
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

def test_class_initialization():
    """测试类初始化"""
    print("\n🧪 测试类初始化...")
    
    try:
        # 测试在没有API密钥的情况下初始化（应该会失败）
        from scripts.gemini_brain import GeminiBrain
        
        # 临时移除API密钥环境变量
        original_key = os.environ.get('GEMINI_API_KEY')
        if original_key:
            del os.environ['GEMINI_API_KEY']
        
        try:
            brain = GeminiBrain()
            print("❌ 预期初始化失败但成功了（可能配置中有默认密钥）")
            return False
        except ValueError as e:
            if "API密钥" in str(e) or "api_key" in str(e).lower():
                print("✅ 正确的错误处理: 缺少API密钥时抛出异常")
                return True
            else:
                print(f"❌ 错误的异常类型: {e}")
                return False
        finally:
            # 恢复环境变量
            if original_key:
                os.environ['GEMINI_API_KEY'] = original_key
                
    except Exception as e:
        print(f"❌ 初始化测试失败: {e}")
        return False

def test_skill_info():
    """测试技能信息"""
    print("\n🧪 测试技能信息...")
    
    try:
        from scripts.openclaw_integration import OpenClawGeminiSkill
        
        skill = OpenClawGeminiSkill()
        result = skill.handle_command("info", {})
        
        if result.get("success") and "skill_info" in result:
            info = result["skill_info"]
            print(f"✅ 技能信息获取成功")
            print(f"   名称: {info.get('name')}")
            print(f"   版本: {info.get('version')}")
            print(f"   描述: {info.get('description')[:50]}...")
            
            # 检查命令列表
            commands = info.get('commands', {})
            if commands:
                print(f"   可用命令: {', '.join(commands.keys())}")
                return True
            else:
                print("❌ 命令列表为空")
                return False
        else:
            print(f"❌ 技能信息获取失败: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ 技能信息测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n🧪 测试错误处理...")
    
    try:
        from scripts.openclaw_integration import OpenClawGeminiSkill
        
        skill = OpenClawGeminiSkill()
        
        # 测试无效命令
        result = skill.handle_command("invalid_command", {})
        if not result.get("success") and "error" in result:
            print("✅ 无效命令正确处理")
        else:
            print("❌ 无效命令未正确处理")
            return False
        
        # 测试缺少参数
        result = skill.handle_command("ask", {})
        if not result.get("success") and "error" in result:
            print("✅ 缺少参数正确处理")
        else:
            print("❌ 缺少参数未正确处理")
            return False
        
        # 测试格式响应
        error_result = {"success": False, "error": "测试错误"}
        formatted = skill.format_response(error_result)
        if "错误" in formatted or "error" in formatted.lower():
            print("✅ 错误响应格式化正确")
        else:
            print("❌ 错误响应格式化不正确")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False

def test_config_file():
    """测试配置文件"""
    print("\n🧪 测试配置文件...")
    
    config_path = skill_dir / "config.yaml"
    if not config_path.exists():
        print("❌ 配置文件不存在")
        return False
    
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 检查必要配置项
        required_sections = ['gemini', 'search', 'code_generation', 'conversation']
        missing = [section for section in required_sections if section not in config]
        
        if missing:
            print(f"❌ 缺少配置节: {missing}")
            return False
        
        # 检查gemini配置
        gemini_config = config.get('gemini', {})
        if 'model' not in gemini_config:
            print("❌ gemini配置缺少model")
            return False
        
        print(f"✅ 配置文件结构正确")
        print(f"   模型: {gemini_config.get('model')}")
        print(f"   温度: {gemini_config.get('temperature')}")
        print(f"   搜索功能: {'启用' if config.get('search', {}).get('enabled') else '禁用'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置文件测试失败: {e}")
        return False

def test_example_files():
    """测试示例文件"""
    print("\n🧪 测试示例文件...")
    
    examples_dir = skill_dir / "examples"
    if not examples_dir.exists():
        print("❌ 示例目录不存在")
        return False
    
    # 检查示例文件
    example_files = list(examples_dir.glob("*.md"))
    if not example_files:
        print("❌ 没有示例文件")
        return False
    
    print(f"✅ 找到 {len(example_files)} 个示例文件")
    for file in example_files:
        print(f"   - {file.name}")
    
    # 检查主要示例文件
    main_example = examples_dir / "usage_examples.md"
    if main_example.exists():
        file_size = main_example.stat().st_size
        print(f"✅ 主示例文件大小: {file_size} 字节")
        return True
    else:
        print("❌ 主示例文件不存在")
        return False

def main():
    """主测试函数"""
    print("="*60)
    print("🔧 Gemini Brain 技能功能测试")
    print("="*60)
    
    tests = [
        ("模块导入", test_imports),
        ("配置加载", test_config_loading),
        ("类初始化", test_class_initialization),
        ("技能信息", test_skill_info),
        ("错误处理", test_error_handling),
        ("配置文件", test_config_file),
        ("示例文件", test_example_files),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: 通过")
            else:
                print(f"❌ {test_name}: 失败")
        except Exception as e:
            print(f"❌ {test_name}: 异常 - {e}")
    
    print("\n" + "="*60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！技能功能正常。")
        print("\n💡 下一步:")
        print("   1. 设置GEMINI_API_KEY环境变量")
        print("   2. 运行: python scripts/gemini_brain.py \"测试问题\"")
        print("   3. 或运行: python scripts/openclaw_integration.py info")
    else:
        print("⚠️  部分测试失败，需要检查问题。")
    
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)