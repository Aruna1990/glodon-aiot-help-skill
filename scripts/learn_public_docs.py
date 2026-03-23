#!/usr/bin/env python3
"""
语雀公开文档学习脚本
使用 curl 直接获取公开文档内容（无需 Token）
"""

import os
import subprocess
import json
import re
import time
from datetime import datetime
from typing import List, Dict, Optional

# 配置
BASE_URL = "https://glodon-cv-help.yuque.com/cuv0se/ol9231"
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge")
LEARN_STATE_FILE = os.path.join(KNOWLEDGE_DIR, ".learn_state.json")

# 核心文档
CORE_DOCS = [
    {"slug": "yck25gn683z3wa2f", "title": "平台介绍"},
    {"slug": "lpetkzefs5er4q5x", "title": "平台使用常见问题汇总"},
    {"slug": "ku9i5oea97ynfzt4", "title": "平台认证 Token 说明文档"},
    {"slug": "tl0hylbi1hm61mu3", "title": "Key Secret 认证获取 Token"},
    {"slug": "etgvtorzglntmv39", "title": "API 调用"},
    {"slug": "thkdpzvfc9lffg7g", "title": "执行对话接口说明文档"},
    {"slug": "ku8iulvfl3e9sghk", "title": "服务 API 调用"},
    {"slug": "xcrcis1brhczo6ei", "title": "Prompt 工程"},
    {"slug": "cw6wurwnygkv1nne", "title": "知识库"},
    {"slug": "hhgfdznfypkcz0t1", "title": "数据管理"},
]


def fetch_doc_content(slug: str) -> Optional[str]:
    """使用 curl 获取文档内容"""
    url = f"{BASE_URL}/{slug}"
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            html = result.stdout
            
            # 简单提取标题和内容
            # 语雀页面的内容通常在 <meta name="description"> 或特定的 div 中
            # 这里提取页面标题作为占位
            title_match = re.search(r'<title>([^<]+)</title>', html)
            title = title_match.group(1) if title_match else slug
            
            # 提取描述
            desc_match = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
            description = desc_match.group(1) if desc_match else ""
            
            content = f"# {title}\n\n"
            if description:
                content += f"{description}\n\n"
            
            content += f"""> 📖 完整文档：{url}

---

**注意**: 这是文档的元数据摘要。

由于语雀页面的反爬保护，完整内容需要：
1. 使用浏览器访问上方链接
2. 或使用语雀 API（需要 Token）
3. 或手动复制粘贴内容到本地

---

## 文档信息

- **Slug**: `{slug}`
- **URL**: {url}
- **获取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

*本文档由 learn_public_docs.py 自动生成*
"""
            return content
        
        return None
        
    except Exception as e:
        print(f"错误：{e}")
        return None


def save_doc(slug: str, title: str, content: str, links: List[str] = None):
    """保存文档到本地"""
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    filepath = os.path.join(KNOWLEDGE_DIR, f"{slug}.md")
    
    doc_content = f"""# {title}

> 来源：广联达行业 AI 平台文档中心  
> 链接：{BASE_URL}/{slug}  
> 学习时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{content}

---

## 关联文档

"""
    if links:
        for link in links:
            doc_content += f"- [{link}]({BASE_URL}/{link})\n"
    else:
        doc_content += "*暂无关联文档*\n"
    
    doc_content += f"\n---\n\n*本文档由 learn_public_docs.py 自动获取 · 公开文档*\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(doc_content)
    
    return filepath


def extract_links(content: str) -> List[str]:
    """提取文档中的语雀链接"""
    pattern = r'/cuv0se/ol9231/([a-z0-9]+)'
    matches = re.findall(pattern, content)
    return list(set(matches))


def learn_core_docs():
    """学习核心文档"""
    print("=" * 60)
    print("📚 广联达行业 AI 平台 - 核心文档学习")
    print("=" * 60)
    print(f"知识库：{BASE_URL}")
    print(f"输出目录：{KNOWLEDGE_DIR}")
    print(f"文档数量：{len(CORE_DOCS)} 篇")
    print("=" * 60)
    print()
    
    learned = 0
    failed = 0
    
    for i, doc in enumerate(CORE_DOCS, 1):
        slug = doc["slug"]
        title = doc["title"]
        
        print(f"[{i}/{len(CORE_DOCS)}] 📥 {title}")
        print(f"    {BASE_URL}/{slug}")
        
        # 获取内容
        content = fetch_doc_content(slug)
        
        if content:
            # 提取链接
            links = extract_links(content)
            
            # 保存文档
            filepath = save_doc(slug, title, content, links)
            
            print(f"    ✓ 已保存：{filepath}")
            learned += 1
        else:
            print(f"    ❌ 获取失败")
            failed += 1
        
        time.sleep(0.5)
    
    print()
    print("=" * 60)
    print("📊 学习完成")
    print("=" * 60)
    print(f"成功：{learned} 篇")
    print(f"失败：{failed} 篇")
    print("=" * 60)
    
    # 保存状态
    state = {
        "last_sync": datetime.now().isoformat(),
        "learned_docs": [doc["slug"] for doc in CORE_DOCS],
        "total_learned": learned
    }
    
    with open(LEARN_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 状态已保存：{LEARN_STATE_FILE}")


def show_state():
    """显示学习状态"""
    if os.path.exists(LEARN_STATE_FILE):
        with open(LEARN_STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        print("📊 学习状态:")
        print(json.dumps(state, indent=2, ensure_ascii=False))
    else:
        print("📊 无学习状态记录")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="语雀公开文档学习工具")
    parser.add_argument("--core", action="store_true", help="学习核心文档")
    parser.add_argument("--state", action="store_true", help="查看状态")
    
    args = parser.parse_args()
    
    if args.state:
        show_state()
    elif args.core:
        learn_core_docs()
    else:
        learn_core_docs()


if __name__ == "__main__":
    main()
