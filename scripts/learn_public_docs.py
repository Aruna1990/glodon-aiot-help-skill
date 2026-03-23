#!/usr/bin/env python3
"""
语雀公开文档学习脚本（行业 AI 平台）
支持两种方式获取文档内容：
1. 语雀 API（优先）- 获取完整 HTML 内容，转换为 Markdown
2. 网页抓取（降级）- 仅获取元数据

根据语雀文档实际目录结构自动创建本地目录
"""

import os
import sys
import subprocess
import json
import re
import time
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# 导入统一配置和工具
sys.path.insert(0, str(Path(__file__).parent))
from config import IndustryAIPlatform as Config, Common
from utils import html_to_markdown, ensure_dir

# 使用配置
BASE_URL = Config.BASE_URL
API_BASE = Config.API_BASE
BOOK_ID = Config.BOOK_ID
CORE_DOCS = Config.CORE_DOCS
KNOWLEDGE_DIR = Config.OUTPUT_DIR
LEARN_STATE_FILE = Common.STATE_FILE
USER_AGENT = Common.USER_AGENT
REQUEST_TIMEOUT = Common.REQUEST_TIMEOUT


def html_to_markdown(html_content: str) -> str:
    """
    将语雀 Lake HTML 转换为 Markdown
    
    使用 markdownify 库进行转换，并做特殊处理：
    - 移除 meta 标签
    - 处理表格
    - 处理代码块
    - 处理图片
    """
    try:
        from markdownify import markdownify as md
        
        # 移除 doctype 和 meta 标签
        clean_html = re.sub(r'<!doctype[^>]*>', '', html_content)
        clean_html = re.sub(r'<meta[^>]*>', '', clean_html)
        
        # 移除 card 标签（语雀的特殊组件，如图片、代码块等）
        # 保留 card 中的文本内容
        card_pattern = r'<card[^>]*value="data:([^"]*)"[^>]*></card>'
        def replace_card(match):
            import base64
            import urllib.parse
            try:
                data_str = match.group(1)
                decoded = urllib.parse.unquote(data_str)
                # 尝试解析 JSON
                card_data = json.loads(decoded[5:] if decoded.startswith('data:') else decoded)
                
                # 处理代码块
                if card_data.get('name') == 'codeblock':
                    code = card_data.get('code', '')
                    lang = card_data.get('mode', '')
                    return f"\n```{lang}\n{code}\n```\n"
                
                # 处理图片
                elif card_data.get('name') == 'image':
                    src = card_data.get('src', '')
                    return f"\n![image]({src})\n"
                
                # 处理书签
                elif card_data.get('name') == 'bookmarkInline':
                    detail = card_data.get('detail', {})
                    title = detail.get('title', '')
                    url = detail.get('url', '')
                    return f"\n[{title}]({url})\n"
                
                # 处理内联链接
                elif card_data.get('name') == 'yuqueinline':
                    detail = card_data.get('detail', {})
                    title = detail.get('title', '')
                    url = detail.get('url', '')
                    return f"\n[{title}]({url})\n"
                
                else:
                    return ""
            except:
                return ""
        
        clean_html = re.sub(card_pattern, replace_card, clean_html)
        
        # 转换 HTML 到 Markdown
        markdown = md(
            clean_html,
            heading_style='ATX',
            strip=['script', 'style'],
            bullets='-'
        )
        
        # 清理多余的空白行
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        return markdown
    
    except ImportError:
        # 如果 markdownify 不可用，返回简化版
        return html_content


def fetch_doc_via_api(slug: str) -> Optional[Dict]:
    """
    通过语雀 API 获取文档内容（优先方式）
    
    API: https://glodon-cv-help.yuque.com/api/docs/${slug}?include_contributors=true&include_like=true&include_hits=true&merge_dynamic_data=false&book_id=41611578
    
    返回 data.content 字段包含文档的 HTML 内容
    """
    api_url = f"{API_BASE}/docs/{slug}?include_contributors=true&include_like=true&include_hits=true&merge_dynamic_data=false&book_id={BOOK_ID}"
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', api_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            
            # 检查是否有 data.content 字段
            if 'data' in data and 'content' in data['data']:
                html_content = data['data']['content']
                title = data['data'].get('title', slug)
                description = data['data'].get('description', '')
                
                # 转换 HTML 到 Markdown
                markdown_content = html_to_markdown(html_content)
                
                # 构建完整文档
                content = f"# {title}\n\n"
                if description:
                    # 清理描述中的 HTML 标签
                    desc_clean = re.sub(r'<[^>]+>', '', description)
                    content += f"{desc_clean}\n\n"
                
                content += f"---\n\n{markdown_content}\n\n"
                content += f"---\n\n"
                content += f"## 文档信息\n\n"
                content += f"- **Slug**: `{slug}`\n"
                content += f"- **URL**: {BASE_URL}/{slug}\n"
                content += f"- **获取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                content += f"- **来源**: 语雀 API（HTML 转 Markdown）\n"
                
                return {
                    "title": title,
                    "content": content,
                    "category": None,
                    "url": f"{BASE_URL}/{slug}",
                    "source": "api"
                }
            
            return None
        
        return None
        
    except Exception as e:
        print(f"    API 获取失败：{e}")
        return None


def fetch_doc_via_web(slug: str) -> Optional[Dict]:
    """
    通过网页抓取获取文档内容（降级方式）
    仅获取元数据摘要
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
            
            if "·" in page_title:
                page_title = page_title.split("·")[0].strip()
            
            # 提取描述
            desc_match = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
            description = desc_match.group(1) if desc_match else ""
            
            # 构建元数据文档
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
- **来源**: 网页抓取（元数据）

---

*本文档由 learn_public_docs.py 自动生成*
"""
            
            return {
                "title": page_title,
                "content": content,
                "category": None,
                "url": url,
                "source": "web"
            }
        
        return None
        
    except Exception as e:
        print(f"    网页抓取失败：{e}")
        return None


def save_doc(slug: str, title: str, content: str, category: str = None):
    """保存文档到本地"""
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    filepath = os.path.join(KNOWLEDGE_DIR, f"{slug}.md")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


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
    api_count = 0
    web_count = 0
    
    for i, doc in enumerate(CORE_DOCS, 1):
        slug = doc["slug"]
        title = doc["title"]
        
        print(f"[{i}/{len(CORE_DOCS)}] 📥 {title}")
        print(f"    {BASE_URL}/{slug}")
        
        # 优先尝试 API 方式
        doc_data = fetch_doc_via_api(slug)
        
        # API 失败则降级到网页抓取
        if not doc_data:
            print(f"    ⚠️ API 不可用，降级到网页抓取...")
            doc_data = fetch_doc_via_web(slug)
        
        if doc_data:
            source = doc_data.get("source", "unknown")
            if source == "api":
                api_count += 1
                print(f"    ✓ API 获取成功 (HTML 转 Markdown)")
            else:
                web_count += 1
                print(f"    ✓ 网页抓取成功 (元数据)")
            
            filepath = save_doc(slug, doc_data["title"], doc_data["content"])
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
    print(f"API 获取：{api_count} 篇")
    print(f"网页抓取：{web_count} 篇")
    print("=" * 60)
    
    # 保存状态
    state = {
        "last_sync": datetime.now().isoformat(),
        "learned_docs": [doc["slug"] for doc in CORE_DOCS],
        "total_learned": learned,
        "api_count": api_count,
        "web_count": web_count
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
