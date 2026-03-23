#!/usr/bin/env python3
"""
测试 glodon-ai-help 新功能
"""

import sys
import os

# 添加技能目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from bot import AIBotAssistant

def test_platform_access():
    """测试平台入门问题"""
    print("=" * 60)
    print("🧪 测试：平台入门问题")
    print("=" * 60)
    
    bot = AIBotAssistant()
    
    test_queries = [
        "怎么进入行业 AI 平台？",
        "如何访问平台？",
        "平台地址是什么？",
        "第一次使用怎么登录？",
        "新手入门指南",
    ]
    
    for query in test_queries:
        print(f"\n🤔 问题：{query}")
        response = bot.answer(query)
        
        if response.get("is_guide"):
            print("✅ 正确识别为入门指南问题")
        else:
            print("❌ 未识别为入门指南问题")
        
        # 检查是否有相关文档
        docs = response.get("related_docs", [])
        if docs:
            print(f"📚 推荐文档：{len(docs)} 篇")
        else:
            print("⚠️  无推荐文档")

def test_learning_trigger():
    """测试学习触发"""
    print("\n" + "=" * 60)
    print("🧪 测试：自动学习触发")
    print("=" * 60)
    
    bot = AIBotAssistant()
    
    test_queries = [
        "我不知道这个功能",
        "没有找到相关文档",
        "有最新的更新吗？",
    ]
    
    for query in test_queries:
        print(f"\n🤔 问题：{query}")
        response = bot.answer(query)
        
        if response.get("should_learn"):
            print(f"✅ 触发学习建议")
            print(f"   建议文档：{response.get('learn_slugs', [])}")
        else:
            print("⚠️  未触发学习")

def test_normal_qa():
    """测试普通问答"""
    print("\n" + "=" * 60)
    print("🧪 测试：普通问答")
    print("=" * 60)
    
    bot = AIBotAssistant()
    
    test_queries = [
        "平台介绍",
        "API 调用",
        "Token 怎么获取？",
    ]
    
    for query in test_queries:
        print(f"\n🤔 问题：{query}")
        response = bot.answer(query)
        formatted = bot.format_response(response)
        
        print(f"📝 回答长度：{len(formatted)} 字符")
        
        if response.get("related_docs"):
            print(f"📚 推荐文档：{len(response['related_docs'])} 篇")

def main():
    """运行所有测试"""
    print("🚀 glodon-ai-help 新功能测试\n")
    
    test_platform_access()
    test_learning_trigger()
    test_normal_qa()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
