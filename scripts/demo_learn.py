#!/usr/bin/env python3
"""
演示学习脚本 - 展示 glodon-ai-help 的学习流程
无需 Token 也可演示完整流程
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List

# 配置
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge")
DEMO_STATE_FILE = os.path.join(KNOWLEDGE_DIR, ".demo_state.json")

# 核心文档（按学习优先级排序）
CORE_DOCS = [
    {"slug": "yck25gn683z3wa2f", "title": "平台介绍", "priority": 1},
    {"slug": "lpetkzefs5er4q5x", "title": "平台使用常见问题汇总", "priority": 1},
    {"slug": "ku9i5oea97ynfzt4", "title": "平台认证 Token 说明文档", "priority": 2},
    {"slug": "tl0hylbi1hm61mu3", "title": "Key Secret 认证获取 Token", "priority": 2},
    {"slug": "etgvtorzglntmv39", "title": "API 调用", "priority": 2},
    {"slug": "thkdpzvfc9lffg7g", "title": "执行对话接口说明文档", "priority": 3},
    {"slug": "ku8iulvfl3e9sghk", "title": "服务 API 调用", "priority": 3},
    {"slug": "xcrcis1brhczo6ei", "title": "Prompt 工程", "priority": 3},
    {"slug": "cw6wurwnygkv1nne", "title": "知识库", "priority": 3},
    {"slug": "hhgfdznfypkcz0t1", "title": "数据管理", "priority": 3},
]

# 关联链接映射（模拟下钻学习）
RELATED_LINKS = {
    "yck25gn683z3wa2f": ["ouwzx8mgo63oboqg", "bgmy2qkoqqk7whtq"],  # 平台介绍 → 模型、解决方案
    "ku9i5oea97ynfzt4": ["tl0hylbi1hm61mu3"],  # Token 说明 → Key Secret 认证
    "etgvtorzglntmv39": ["thkdpzvfc9lffg7g", "ku8iulvfl3e9sghk"],  # API 调用 → 具体接口
    "xcrcis1brhczo6ei": ["drznpftt901w3v5x", "empb7s1d9xaqyiko"],  # Prompt → 模板、样例
    "cw6wurwnygkv1nne": ["mwhq7ogvirgkxp0l", "caz83r4dkqw6vf5n"],  # 知识库 → API、示例
}


def print_step(step: int, total: int, message: str, icon: str = "📖"):
    """打印步骤信息"""
    print(f"[{step}/{total}] {icon} {message}")


def simulate_fetch_content(slug: str, title: str) -> str:
    """模拟获取文档内容"""
    yuque_token = os.environ.get("YUQUE_TOKEN", "")
    
    if not yuque_token:
        return f"""# {title}

> ⚠️ **演示模式** - 未配置 YUQUE_TOKEN，以下为模拟内容
> 
> 真实内容需要从语雀获取：https://glodon-cv-help.yuque.com/cuv0se/ol9231/{slug}

---

## 文档概述

本文档是广联达行业 AI 平台的核心文档之一。

### 主要内容

1. **功能介绍** - 详细说明平台的核心功能
2. **使用指南** - 逐步操作指导
3. **最佳实践** - 推荐使用方式
4. **常见问题** - FAQ 解答

---

## 关联文档

本文档引用了以下相关文档：
- 查看完整内容需要配置 YUQUE_TOKEN

---

*演示模式生成 · 完整内容请访问语雀*
"""
    else:
        # 实际调用语雀 API 的逻辑（略）
        return "真实文档内容..."


def organize_directory():
    """组织知识库目录结构"""
    print("\n" + "=" * 60)
    print("📁 组织知识库目录结构")
    print("=" * 60)
    
    # 创建分类子目录
    categories = {
        "01-platform-intro": "平台介绍",
        "02-api-reference": "API 参考",
        "03-knowledge-base": "知识库",
        "04-prompt-engineering": "Prompt 工程",
        "05-models": "模型服务",
        "06-tutorials": "使用教程",
        "07-faq": "常见问题",
    }
    
    for dir_name, description in categories.items():
        dir_path = os.path.join(KNOWLEDGE_DIR, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"  ✓ 创建目录：{dir_name}/ ({description})")
        else:
            print(f"  ⏭️  已存在：{dir_name}/")
    
    return categories


def learn_document(doc: Dict, depth: int = 0, max_depth: int = 2) -> Dict:
    """学习单个文档"""
    indent = "  " * depth
    slug = doc["slug"]
    title = doc["title"]
    
    print(f"{indent}📖 学习：{title}")
    print(f"{indent}   链接：https://glodon-cv-help.yuque.com/cuv0se/ol9231/{slug}")
    
    # 模拟获取内容
    content = simulate_fetch_content(slug, title)
    
    # 检查关联链接
    related = RELATED_LINKS.get(slug, [])
    
    doc_info = {
        "slug": slug,
        "title": title,
        "learned_at": datetime.now().isoformat(),
        "content_length": len(content),
        "related_docs": related,
        "depth": depth
    }
    
    print(f"{indent}   ✓ 内容长度：{len(content)} 字符")
    if related:
        print(f"{indent}   🔗 关联文档：{len(related)} 个")
    
    return doc_info


def demo_learning():
    """演示学习流程"""
    print("=" * 60)
    print("🚀 glodon-ai-help 学习功能演示")
    print("=" * 60)
    print(f"知识库：https://glodon-cv-help.yuque.com/cuv0se/ol9231")
    print(f"输出目录：{KNOWLEDGE_DIR}")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 检查 Token
    yuque_token = os.environ.get("YUQUE_TOKEN", "")
    if not yuque_token:
        print("\n⚠️  未配置 YUQUE_TOKEN")
        print("   演示模式：使用模拟内容")
        print("   配置方法：export YUQUE_TOKEN='your_token'")
    else:
        print("\n✅ YUQUE_TOKEN 已配置")
        print("   将从语雀 API 获取真实内容")
    
    # 步骤 1：组织目录
    categories = organize_directory()
    
    # 步骤 2：学习核心文档
    print("\n" + "=" * 60)
    print("📚 开始学习核心文档")
    print("=" * 60)
    
    learned_docs = []
    total_docs = len(CORE_DOCS)
    
    for i, doc in enumerate(CORE_DOCS, 1):
        print_step(i, total_docs, f"优先级 P{doc['priority']} - {doc['title']}")
        
        doc_info = learn_document(doc, depth=0)
        learned_docs.append(doc_info)
        
        # 模拟下钻学习关联文档
        if doc["slug"] in RELATED_LINKS:
            print(f"    🔍 下钻学习关联文档...")
            for related_slug in RELATED_LINKS[doc["slug"]]:
                # 查找关联文档信息
                related_doc = next((d for d in CORE_DOCS if d["slug"] == related_slug), None)
                if related_doc:
                    learn_document(related_doc, depth=1)
                else:
                    print(f"      📄 {related_slug} (在完整文档列表中)")
        
        print()
        time.sleep(0.3)  # 模拟请求延迟
    
    # 步骤 3：保存学习状态
    print("=" * 60)
    print("💾 保存学习状态")
    print("=" * 60)
    
    state = {
        "demo_mode": not yuque_token,
        "learned_at": datetime.now().isoformat(),
        "total_docs": len(learned_docs),
        "documents": learned_docs,
        "categories": list(categories.keys())
    }
    
    with open(DEMO_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ 状态文件：{DEMO_STATE_FILE}")
    
    # 步骤 4：生成学习报告
    print("\n" + "=" * 60)
    print("📊 学习报告")
    print("=" * 60)
    
    print(f"""
✅ 学习完成！

📈 统计信息:
   • 学习文档：{len(learned_docs)} 篇核心文档
   • 关联下钻：{sum(len(RELATED_LINKS.get(d['slug'], [])) for d in learned_docs)} 篇
   • 目录分类：{len(categories)} 个
   • 学习模式：{"真实内容" if yuque_token else "演示模式"}

📁 目录结构:
"""
    )
    
    for dir_name, description in categories.items():
        print(f"   knowledge/{dir_name}/ - {description}")
    
    print(f"""
🔗 语雀知识库:
   https://glodon-cv-help.yuque.com/cuv0se/ol9231

💡 下一步:
   1. 配置 YUQUE_TOKEN 获取真实内容
   2. 运行完整学习：python3 learn_docs.py --all
   3. 查看学习状态：python3 learn_docs.py --state
""")
    
    print("=" * 60)
    
    return state


def show_current_state():
    """显示当前学习状态"""
    print("=" * 60)
    print("📊 当前学习状态")
    print("=" * 60)
    
    # 检查已有文档
    md_files = [f for f in os.listdir(KNOWLEDGE_DIR) if f.endswith('.md')]
    
    print(f"""
📁 知识库目录：{KNOWLEDGE_DIR}
📄 文档数量：{len(md_files)} 篇

📋 文档列表:
""")
    
    for f in sorted(md_files)[:10]:
        filepath = os.path.join(KNOWLEDGE_DIR, f)
        size = os.path.getsize(filepath)
        print(f"   • {f} ({size} 字节)")
    
    if len(md_files) > 10:
        print(f"   ... 还有 {len(md_files) - 10} 篇")
    
    # 检查状态文件
    if os.path.exists(DEMO_STATE_FILE):
        with open(DEMO_STATE_FILE, 'r') as f:
            state = json.load(f)
        print(f"\n💾 学习状态：已记录 ({state.get('learned_at', '未知')})")
    else:
        print("\n💾 学习状态：无记录")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="学习功能演示")
    parser.add_argument("--state", action="store_true", help="显示当前状态")
    parser.add_argument("--demo", action="store_true", help="运行演示流程")
    
    args = parser.parse_args()
    
    if args.state:
        show_current_state()
    elif args.demo:
        demo_learning()
    else:
        # 默认运行演示
        demo_learning()


if __name__ == "__main__":
    main()
