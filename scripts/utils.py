#!/usr/bin/env python3
"""
通用工具函数

提供所有学习脚本共用的工具函数
"""

import json
import re
from typing import Optional


def html_to_markdown(html_content: str) -> str:
    """
    将语雀 Lake HTML 转换为 Markdown
    
    使用 markdownify 库进行转换，并做特殊处理：
    - 移除 meta 标签
    - 处理表格
    - 处理代码块
    - 处理图片
    - 处理书签和内联链接
    """
    try:
        from markdownify import markdownify as md
        
        # 移除 doctype 和 meta 标签
        clean_html = re.sub(r'<!doctype[^>]*>', '', html_content)
        clean_html = re.sub(r'<meta[^>]*>', '', clean_html)
        
        # 移除 card 标签（语雀的特殊组件）
        card_pattern = r'<card[^>]*value="data:([^"]*)"[^>]*></card>'
        
        def replace_card(match):
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
        print("⚠️  markdownify 未安装，返回原始 HTML")
        return html_content


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符
    
    Args:
        filename: 原始文件名
    
    Returns:
        清理后的文件名
    """
    # 移除非法字符
    illegal_chars = r'[<>:"/\\|？*]'
    sanitized = re.sub(illegal_chars, '', filename)
    # 替换空格为下划线
    sanitized = sanitized.replace(' ', '_')
    return sanitized


def extract_slug_from_url(url: str) -> Optional[str]:
    """
    从语雀 URL 提取文档 slug
    
    Args:
        url: 语雀文档 URL
    
    Returns:
        文档 slug，如果提取失败返回 None
    """
    pattern = r'/[a-z0-9]+/[a-z0-9]+/([a-z0-9]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None


def ensure_dir(dir_path):
    """
    确保目录存在，不存在则创建
    
    Args:
        dir_path: 目录路径（Path 对象或字符串）
    """
    from pathlib import Path
    if isinstance(dir_path, str):
        dir_path = Path(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)
