#!/usr/bin/env python3
"""
AIoT 平台对接文档学习脚本
文档地址：https://glodon-cv-help.yuque.com/lzh2bp/gwam63

注意：部分文档需要登录才能访问
"""

import os
import subprocess
import json
import re
import time
from datetime import datetime
from typing import List, Dict, Optional

# 配置
AIOT_BASE_URL = "https://glodon-cv-help.yuque.com/lzh2bp/gwam63"
API_BASE = "https://glodon-cv-help.yuque.com/api"
AIOT_BOOK_ID = "29345082"  # AIoT 平台对接知识库 ID
SKILL_DIR = os.path.join(os.path.dirname(__file__), "..")
KNOWLEDGE_DIR = os.path.join(SKILL_DIR, "knowledge", "02-aiot-platform")
LEARN_STATE_FILE = os.path.join(KNOWLEDGE_DIR, ".learn_state.json")

# AIoT 平台对接核心文档（身份认证、Token 相关）
# 注意：部分文档需要登录才能访问
AIOT_DOCS = [
    {"slug": "tt25tc", "title": "Glodon AIoT 产品系统 API 接入文档", "public": True},
    {"slug": "kqg83f", "title": "身份认证", "public": False},
    {"slug": "pzx9r2", "title": "获取 Access Token", "public": False},
    {"slug": "m7h4n1", "title": "API 调用规范", "public": False},
]


def html_to_markdown(html_content: str) -> str:
    """将语雀 Lake HTML 转换为 Markdown"""
    try:
        from markdownify import markdownify as md
        
        clean_html = re.sub(r'<!doctype[^>]*>', '', html_content)
        clean_html = re.sub(r'<meta[^>]*>', '', clean_html)
        
        card_pattern = r'<card[^>]*value="data:([^"]*)"[^>]*></card>'
        def replace_card(match):
            import urllib.parse
            try:
                data_str = match.group(1)
                decoded = urllib.parse.unquote(data_str)
                card_data = json.loads(decoded[5:] if decoded.startswith('data:') else decoded)
                
                if card_data.get('name') == 'codeblock':
                    code = card_data.get('code', '')
                    lang = card_data.get('mode', '')
                    return f"\n```{lang}\n{code}\n```\n"
                elif card_data.get('name') == 'image':
                    src = card_data.get('src', '')
                    return f"\n![image]({src})\n"
                elif card_data.get('name') in ['bookmarkInline', 'yuqueinline']:
                    detail = card_data.get('detail', {})
                    title = detail.get('title', '')
                    url = detail.get('url', '')
                    return f"\n[{title}]({url})\n"
                else:
                    return ""
            except:
                return ""
        
        clean_html = re.sub(card_pattern, replace_card, clean_html)
        markdown = md(clean_html, heading_style='ATX', strip=['script', 'style'], bullets='-')
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        return markdown
    
    except ImportError:
        return html_content


def fetch_doc_via_api(slug: str) -> Optional[Dict]:
    """通过语雀 API 获取文档内容（使用 AIoT 平台 book_id）"""
    api_url = f"{API_BASE}/docs/{slug}?include_contributors=true&include_like=true&include_hits=true&merge_dynamic_data=false&book_id={AIOT_BOOK_ID}"
    
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
            
            if 'data' in data and 'content' in data['data']:
                html_content = data['data']['content']
                title = data['data'].get('title', slug)
                description = data['data'].get('description', '')
                
                markdown_content = html_to_markdown(html_content)
                
                content = f"# {title}\n\n"
                if description:
                    desc_clean = re.sub(r'<[^>]+>', '', description)
                    content += f"{desc_clean}\n\n"
                
                content += f"---\n\n{markdown_content}\n\n"
                content += f"---\n\n"
                content += f"## 文档信息\n\n"
                content += f"- **Slug**: `{slug}`\n"
                content += f"- **URL**: {AIOT_BASE_URL}/{slug}\n"
                content += f"- **获取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                content += f"- **来源**: 语雀 API（AIoT 平台对接文档）\n"
                content += f"- **Book ID**: {AIOT_BOOK_ID}\n"
                
                return {
                    "title": title,
                    "content": content,
                    "url": f"{AIOT_BASE_URL}/{slug}",
                    "source": "api"
                }
        
        return None
        
    except Exception as e:
        print(f"    API 获取失败：{e}")
        return None


def save_doc(slug: str, content: str):
    """保存文档到本地"""
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    filepath = os.path.join(KNOWLEDGE_DIR, f"{slug}.md")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


def learn_aiot_docs():
    """学习 AIoT 平台对接文档"""
    print("=" * 60)
    print("📚 AIoT 平台对接文档学习")
    print("=" * 60)
    print(f"知识库：{AIOT_BASE_URL}")
    print(f"Book ID: {AIOT_BOOK_ID}")
    print(f"输出目录：{KNOWLEDGE_DIR}")
    print(f"文档数量：{len(AIOT_DOCS)} 篇")
    print("=" * 60)
    print()
    
    learned = 0
    failed = 0
    public_count = 0
    login_required = 0
    
    for i, doc in enumerate(AIOT_DOCS, 1):
        slug = doc["slug"]
        title = doc["title"]
        is_public = doc.get("public", False)
        
        print(f"[{i}/{len(AIOT_DOCS)}] 📥 {title}")
        print(f"    {AIOT_BASE_URL}/{slug}")
        print(f"    {'✅ 公开' if is_public else '🔒 需登录'}")
        
        doc_data = fetch_doc_via_api(slug)
        
        if doc_data:
            print(f"    ✓ API 获取成功")
            filepath = save_doc(slug, doc_data["content"])
            print(f"    ✓ 已保存：{filepath}")
            learned += 1
            if is_public:
                public_count += 1
        else:
            print(f"    ⚠️ 获取失败（需要登录权限）")
            failed += 1
            if not is_public:
                login_required += 1
        
        time.sleep(0.5)
    
    print()
    print("=" * 60)
    print("📊 学习完成")
    print("=" * 60)
    print(f"成功：{learned} 篇")
    print(f"失败：{failed} 篇")
    print(f"公开文档：{public_count} 篇")
    print(f"需登录：{login_required} 篇")
    print("=" * 60)
    
    state = {
        "last_sync": datetime.now().isoformat(),
        "learned_docs": [doc["slug"] for doc in AIOT_DOCS],
        "total_learned": learned,
        "source": "AIoT 平台对接文档",
        "source_url": AIOT_BASE_URL
    }
    
    with open(LEARN_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 状态已保存：{LEARN_STATE_FILE}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AIoT 平台对接文档学习工具")
    parser.add_argument("--learn", action="store_true", help="学习 AIoT 文档")
    parser.add_argument("--state", action="store_true", help="查看状态")
    
    args = parser.parse_args()
    
    if args.state:
        if os.path.exists(LEARN_STATE_FILE):
            with open(LEARN_STATE_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)
            print("📊 学习状态:")
            print(json.dumps(state, indent=2, ensure_ascii=False))
        else:
            print("📊 无学习状态记录")
    elif args.learn:
        learn_aiot_docs()
    else:
        learn_aiot_docs()


if __name__ == "__main__":
    main()
