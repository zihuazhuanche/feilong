#!/usr/bin/env python3
"""
测试 make_latex_model 技能的基本功能
"""

import os
import sys
import yaml

def test_skill_structure():
    """测试技能目录结构"""
    print("🔍 检查技能结构...")
    
    required_files = [
        'SKILL.md',
        'README.md', 
        'config.yaml',
        'scripts/',
        'templates/',
        'docs/'
    ]
    
    for file in required_files:
        path = os.path.join(os.path.dirname(__file__), file)
        if os.path.exists(path):
            status = "✅ 存在"
        else:
            status = "❌ 缺失"
        print(f"  {file:20} {status}")
    
    return True

def test_config():
    """测试配置文件"""
    print("\n📋 检查配置文件...")
    
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print(f"  ✅ 配置加载成功")
        print(f"    技能名称: {config.get('name', '未指定')}")
        print(f"    版本: {config.get('version', '未指定')}")
        print(f"    作者: {config.get('author', '未指定')}")
        
        return True
    except Exception as e:
        print(f"  ❌ 配置加载失败: {e}")
        return False

def test_scripts():
    """测试脚本文件"""
    print("\n📜 检查脚本文件...")
    
    scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
    if not os.path.exists(scripts_dir):
        print("  ❌ scripts目录不存在")
        return False
    
    script_files = os.listdir(scripts_dir)
    python_scripts = [f for f in script_files if f.endswith('.py')]
    
    print(f"  ✅ 找到 {len(python_scripts)} 个Python脚本")
    for script in python_scripts[:5]:  # 显示前5个
        print(f"    - {script}")
    
    if len(python_scripts) > 5:
        print(f"    ... 还有 {len(python_scripts)-5} 个脚本")
    
    return len(python_scripts) > 0

def main():
    print("🧪 make_latex_model 技能测试")
    print("=" * 50)
    
    tests = [
        ("技能结构", test_skill_structure),
        ("配置文件", test_config),
        ("脚本文件", test_scripts)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"  ❌ 测试异常: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {test_name:15} {status}")
    
    print(f"\n🎯 总成绩: {passed}/{total} 通过")
    
    if passed == total:
        print("✨ 技能安装成功，基本功能正常！")
        return 0
    else:
        print("⚠️  技能安装完成，但部分功能需要进一步配置")
        return 1

if __name__ == "__main__":
    sys.exit(main())