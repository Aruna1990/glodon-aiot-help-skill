#!/usr/bin/env python3
"""
语雀公开文档学习脚本
使用 curl 直接获取公开文档内容（无需 Token）

根据语雀文档实际目录结构自动创建本地目录
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
SKILL_DIR = os.path.join(os.path.dirname(__file__), "..")
KNOWLEDGE_DIR = os.path.join(SKILL_DIR, "knowledge")
LEARN_STATE_FILE = os.path.join(KNOWLEDGE_DIR, ".learn_state.json")

# 核心文档（不再预设分类，由脚本自动提取）
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


def fetch_yuque_toc() -> List[Dict]:
    """
    获取语雀知识库目录结构
    
    语雀知识库目录页通常包含所有文档的层级结构
    通过解析目录页可以获取文档的分类信息
    """
    toc_url = BASE_URL
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', toc_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=30
        )
        
        if result.returncode == 0:
            html = result.stdout
            # 提取目录结构（语雀的目录通常在特定的 div 中）
            # 这里简单提取所有文档链接和标题
            pattern = r'href="/cuv0se/ol9231/([a-z0-9]+)"[^>]*>([^<]+)<'
            matches = re.findall(pattern, html)
            
            toc = []
            for slug, title in matches:
                # 去重
                if not any(doc['slug'] == slug for doc in toc):
                    toc.append({"slug": slug, "title": title.strip()})
            
            return toc
        
        return []
        
    except Exception as e:
        print(f"获取目录失败：{e}")
        return []


def fetch_doc_content(slug: str) -> Optional[Dict]:
    """
    使用 curl 获取文档内容
    返回包含内容、标题、分类信息的字典
    """
    url = f"{BASE_URL}/{slug}"
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=30
        )
        
        if result.returncode == 0:
            html = result.stdout
            
            # 提取标题
            title_match = re.search(r'<title>([^<]+)</title>', html)
            page_title = title_match.group(1).strip() if title_match else slug
            
            # 清理标题（移除"· 行业 AI 平台文档中心"等后缀）
            if "·" in page_title:
                page_title = page_title.split("·")[0].strip()
            
            # 提取描述/摘要
            desc_match = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
            description = desc_match.group(1) if desc_match else ""
            
            # 尝试提取面包屑导航（确定分类）
            # 语雀的面包屑通常形如：知识库 > 分类名 > 文档名
            breadcrumb_match = re.search(r'breadcrumb[^>]*>(.*?)</', html, re.IGNORECASE)
            category = None
            if breadcrumb_match:
                breadcrumb = breadcrumb_match.group(1)
                # 提取分类（中间的部分）
                parts = re.split(r'[>\/]', breadcrumb)
                if len(parts) >= 2:
                    category = parts[-2].strip()
                    # 清理分类名
                    category = re.sub(r'[^\w\u4e00-\u9fff-]', '', category)
            
            # 提取正文内容（简化版：提取第一个主要段落）
            content = f"# {page_title}\n\n"
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
"""
            
            if category:
                content += f"- **分类**: {category}\n"
            
            content += "\n---\n\n*本文档由 learn_public_docs.py 自动生成*\n"
            
            return {
                "title": page_title,
                "content": content,
                "category": category,
                "url": url
            }
        
        return None
        
    except Exception as e:
        print(f"错误：{e}")
        return None


def save_doc(slug: str, title: str, content: str, category: str = None):
    """保存文档到本地，根据分类自动创建目录"""
    # 确定保存目录
    if category:
        # 创建分类目录（使用 slug 作为目录名，避免中文路径问题）
        save_dir = os.path.join(KNOWLEDGE_DIR, slug)
    else:
        save_dir = KNOWLEDGE_DIR
    
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, f"{slug}.md")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
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
    categories = set()
    
    for i, doc in enumerate(CORE_DOCS, 1):
        slug = doc["slug"]
        title = doc["title"]
        
        print(f"[{i}/{len(CORE_DOCS)}] 📥 {title}")
        print(f"    {BASE_URL}/{slug}")
        
        # 获取内容（包含分类信息）
        doc_data = fetch_doc_content(slug)
        
        if doc_data:
            # 保存文档（自动根据分类创建目录）
            category = doc_data.get("category")
            if category:
                categories.add(category)
                print(f"    分类：{category}")
            
            filepath = save_doc(slug, doc_data["title"], doc_data["content"], category)
            
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
    if categories:
        print(f"分类：{', '.join(categories)}")
    print("=" * 60)
    
    # 保存状态
    state = {
        "last_sync": datetime.now().isoformat(),
        "learned_docs": [doc["slug"] for doc in CORE_DOCS],
        "total_learned": learned,
        "categories": list(categories)
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
    parser.add_argument("--toc", action="store_true", help="获取目录结构")
    parser.add_argument("--state", action="store_true", help="查看状态")
    
    args = parser.parse_args()
    
    if args.state:
        show_state()
    elif args.toc:
        print("📑 获取语雀知识库目录...")
        toc = fetch_yuque_toc()
        print(f"找到 {len(toc)} 篇文档:")
        for doc in toc[:20]:  # 只显示前 20 篇
            print(f"  - {doc['title']} ({doc['slug']})")
        if len(toc) > 20:
            print(f"  ... 还有 {len(toc) - 20} 篇")
    elif args.core:
        learn_core_docs()
    else:
        learn_core_docs()


if __name__ == "__main__":
    main()
