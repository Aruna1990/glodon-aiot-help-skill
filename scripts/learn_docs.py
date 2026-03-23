#!/usr/bin/env python3
"""
语雀文档深度学习脚本 - 广联达行业 AI 平台
自动阅读文档内容，下钻关联链接，构建完整知识库
"""

import os
import re
import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
from urllib.parse import urlparse, parse_qs

# 配置
SPACE_ID = "cuv0se"
BOOK_ID = "ol9231"
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge")
LEARN_STATE_FILE = os.path.join(KNOWLEDGE_DIR, ".learn_state.json")
YUQUE_API_BASE = "https://www.yuque.com/api/v2"

# 语雀 Token（从环境变量获取）
YUQUE_TOKEN = os.environ.get("YUQUE_TOKEN", "")


class YuqueDoc:
    """语雀文档信息"""
    def __init__(self, slug: str, title: str, url: str, content: str = ""):
        self.slug = slug
        self.title = title
        self.url = url
        self.content = content
        self.links: List[str] = []  # 文档内的参考链接
        self.learned_at: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "slug": self.slug,
            "title": self.title,
            "url": self.url,
            "content": self.content,
            "links": self.links,
            "learned_at": self.learned_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "YuqueDoc":
        doc = cls(
            slug=data["slug"],
            title=data["title"],
            url=data["url"],
            content=data.get("content", "")
        )
        doc.links = data.get("links", [])
        doc.learned_at = data.get("learned_at")
        return doc


class DocLearner:
    """文档学习器 - 自动阅读和下钻"""
    
    def __init__(self, knowledge_dir: str = KNOWLEDGE_DIR):
        self.knowledge_dir = knowledge_dir
        self.state = self._load_state()
        self.session = requests.Session()
        if YUQUE_TOKEN:
            self.session.headers["X-Auth-Token"] = YUQUE_TOKEN
        
        # 已学习的文档
        self.learned_docs: Dict[str, YuqueDoc] = {}
        # 待学习的文档队列
        self.pending_queue: List[str] = []
        # 已处理的链接
        self.processed_links: Set[str] = set()
    
    def _load_state(self) -> Dict:
        """加载学习状态"""
        if os.path.exists(LEARN_STATE_FILE):
            with open(LEARN_STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "last_sync": None,
            "learned_docs": {},
            "pending_links": [],
            "total_learned": 0
        }
    
    def _save_state(self):
        """保存学习状态"""
        os.makedirs(self.knowledge_dir, exist_ok=True)
        state = {
            "last_sync": datetime.now().isoformat(),
            "learned_docs": {slug: doc.to_dict() for slug, doc in self.learned_docs.items()},
            "pending_links": list(self.pending_queue),
            "total_learned": self.state.get("total_learned", 0) + len(self.learned_docs)
        }
        with open(LEARN_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def _extract_yuque_slug(self, url: str) -> Optional[str]:
        """从语雀 URL 中提取 slug"""
        # 格式：https://glodon-cv-help.yuque.com/cuv0se/ol9231/<slug>
        pattern = r"glodon-cv-help\.yuque\.com/cuv0se/ol9231/([a-z0-9]+)"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return None
    
    def _parse_markdown_links(self, content: str) -> List[str]:
        """从 Markdown 内容中提取所有链接"""
        # 匹配 [text](url) 格式
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = []
        for match in re.finditer(link_pattern, content):
            url = match.group(2)
            if url.startswith('http'):
                links.append(url)
        return links
    
    def _fetch_doc_content(self, slug: str) -> Optional[str]:
        """从语雀 API 获取文档内容"""
        if not YUQUE_TOKEN:
            print(f"⚠️  未设置 YUQUE_TOKEN，无法获取文档内容")
            return None
        
        url = f"{YUQUE_API_BASE}/spaces/{SPACE_ID}/docs/{slug}"
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get("data", {}).get("body", "")
            else:
                print(f"❌ 获取文档失败：{slug} - HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ 请求错误：{slug} - {e}")
        return None
    
    def _fetch_catalog(self) -> List[Dict]:
        """获取知识库目录"""
        if not YUQUE_TOKEN:
            print(f"⚠️  未设置 YUQUE_TOKEN，使用内置文档列表")
            return []
        
        url = f"{YUQUE_API_BASE}/spaces/{SPACE_ID}/books/{BOOK_ID}/toc"
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
        except Exception as e:
            print(f"❌ 获取目录失败：{e}")
        return []
    
    def _save_doc(self, doc: YuqueDoc):
        """保存文档到本地"""
        os.makedirs(self.knowledge_dir, exist_ok=True)
        filepath = os.path.join(self.knowledge_dir, f"{doc.slug}.md")
        
        content = f"""# {doc.title}

> 来源：广联达行业 AI 平台文档中心  
> 链接：{doc.url}  
> 学习时间：{doc.learned_at}  
> 关联链接：{len(doc.links)} 个

---

## 文档内容

{doc.content}

---

## 关联文档

"""
        if doc.links:
            for i, link in enumerate(doc.links, 1):
                content += f"{i}. {link}\n"
        else:
            content += "*无关联链接*\n"
        
        content += f"""
---

*本文档由 learn_docs.py 自动学习生成*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"    ✓ 已保存：{filepath}")
    
    def learn_doc(self, slug: str, depth: int = 0, max_depth: int = 3) -> Optional[YuqueDoc]:
        """
        学习单个文档，并递归学习关联链接
        
        Args:
            slug: 文档 slug
            depth: 当前递归深度
            max_depth: 最大递归深度
        """
        if depth > max_depth:
            print(f"    ⏹️  达到最大深度 {max_depth}，停止下钻")
            return None
        
        url = f"https://glodon-cv-help.yuque.com/{SPACE_ID}/{BOOK_ID}/{slug}"
        
        # 检查是否已学习
        if slug in self.learned_docs:
            print(f"    ⏭️  已学习过，跳过")
            return self.learned_docs[slug]
        
        print(f"{'  ' * depth}📖 学习：{slug} (深度 {depth})")
        
        # 获取文档内容
        content = self._fetch_doc_content(slug)
        if not content:
            # 如果没有 Token，创建占位文档
            content = f"*文档内容需要从语雀获取，请在语雀中打开：{url}*"
        
        doc = YuqueDoc(
            slug=slug,
            title=f"文档 {slug}",  # 标题会在获取内容后更新
            url=url,
            content=content
        )
        doc.learned_at = datetime.now().isoformat()
        
        # 提取文档内的链接
        links = self._parse_markdown_links(content)
        yuque_links = []
        for link in links:
            if "glodon-cv-help.yuque.com/cuv0se/ol9231" in link:
                linked_slug = self._extract_yuque_slug(link)
                if linked_slug and linked_slug != slug:
                    yuque_links.append(linked_slug)
                    if linked_slug not in self.processed_links:
                        self.pending_queue.append(linked_slug)
                        self.processed_links.add(linked_slug)
        
        doc.links = yuque_links
        self.learned_docs[slug] = doc
        
        # 保存到本地
        self._save_doc(doc)
        
        return doc
    
    def learn_all(self, doc_slugs: List[str], max_depth: int = 2):
        """
        学习所有文档，包括下钻关联链接
        
        Args:
            doc_slugs: 初始文档 slug 列表
            max_depth: 最大下钻深度
        """
        print("=" * 60)
        print("📚 广联达行业 AI 平台 - 文档深度学习")
        print("=" * 60)
        print(f"知识库：{SPACE_ID}/{BOOK_ID}")
        print(f"初始文档：{len(doc_slugs)} 篇")
        print(f"最大下钻深度：{max_depth}")
        print(f"输出目录：{self.knowledge_dir}")
        print("=" * 60)
        print()
        
        # 初始化待学习队列
        self.pending_queue = list(doc_slugs)
        self.processed_links = set(doc_slugs)
        
        total = 0
        learned_count = 0
        
        while self.pending_queue:
            slug = self.pending_queue.pop(0)
            total += 1
            
            try:
                doc = self.learn_doc(slug, depth=0, max_depth=max_depth)
                if doc:
                    learned_count += 1
            except Exception as e:
                print(f"❌ 学习失败：{slug} - {e}")
            
            # 避免请求过快
            time.sleep(0.5)
        
        print()
        print("=" * 60)
        print(f"✅ 学习完成！")
        print(f"总处理：{total} 篇")
        print(f"成功学习：{learned_count} 篇")
        print(f"发现关联链接：{len(self.processed_links) - len(doc_slugs)} 个")
        print("=" * 60)
        
        # 保存状态
        self._save_state()
        
        return learned_count
    
    def learn_from_catalog(self, max_depth: int = 2):
        """从知识库目录开始学习所有文档"""
        print("📑 获取知识库目录...")
        catalog = self._fetch_catalog()
        
        if not catalog:
            print("❌ 无法获取目录，请检查 YUQUE_TOKEN 配置")
            return 0
        
        # 提取所有文档 slug
        doc_slugs = []
        def extract_docs(items):
            for item in items:
                if item.get("type") == "doc":
                    doc_slugs.append(item.get("url", "").split("/")[-1])
                elif item.get("type") == "group" and item.get("children"):
                    extract_docs(item["children"])
        
        extract_docs(catalog)
        
        print(f"📋 目录中共有 {len(doc_slugs)} 篇文档")
        return self.learn_all(doc_slugs, max_depth=max_depth)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="语雀文档深度学习工具")
    parser.add_argument("--slugs", nargs="+", help="指定要学习的文档 slug 列表")
    parser.add_argument("--all", action="store_true", help="学习知识库所有文档")
    parser.add_argument("--depth", type=int, default=2, help="最大下钻深度（默认 2）")
    parser.add_argument("--state", action="store_true", help="显示学习状态")
    
    args = parser.parse_args()
    
    learner = DocLearner()
    
    if args.state:
        print("📊 当前学习状态:")
        print(json.dumps(learner.state, indent=2, ensure_ascii=False))
        return
    
    if args.all:
        learner.learn_from_catalog(max_depth=args.depth)
    elif args.slugs:
        learner.learn_all(args.slugs, max_depth=args.depth)
    else:
        # 默认学习核心文档
        core_docs = [
            "yck25gn683z3wa2f",  # 平台介绍
            "lpetkzefs5er4q5x",  # 常见问题
            "etgvtorzglntmv39",  # API 调用
            "ku9i5oea97ynfzt4",  # Token 说明
        ]
        print("🎯 学习核心文档...")
        learner.learn_all(core_docs, max_depth=args.depth)


# 需要 requests 库
try:
    import requests
except ImportError:
    print("❌ 需要安装 requests 库：pip install requests")
    exit(1)


if __name__ == "__main__":
    main()
