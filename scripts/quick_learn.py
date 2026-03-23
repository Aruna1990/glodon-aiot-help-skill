#!/usr/bin/env python3
"""
快速学习脚本 - 使用 web_fetch 批量获取公开文档
"""

import os
import json
from datetime import datetime

# 核心文档
CORE_DOCS = [
    {"slug": "yck25gn683z3wa2f", "title": "平台介绍"},
    {"slug": "lpetkzefs5er4q5x", "title": "平台使用常见问题汇总"},
    {"slug": "ku9i5oea97ynfzt4", "title": "平台认证 Token 说明文档"},
    {"slug": "etgvtorzglntmv39", "title": "API 调用"},
    {"slug": "xcrcis1brhczo6ei", "title": "Prompt 工程"},
]

BASE_URL = "https://glodon-cv-help.yuque.com/cuv0se/ol9231"
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge")

print("=" * 60)
print("📚 快速学习 - 核心文档")
print("=" * 60)

for i, doc in enumerate(CORE_DOCS, 1):
    url = f"{BASE_URL}/{doc['slug']}"
    print(f"\n[{i}/{len(CORE_DOCS)}] {doc['title']}")
    print(f"URL: {url}")
    print(f"命令：openclaw web-fetch {url}")
    
    # 生成 web_fetch 调用命令
    print(f"执行：curl -X POST http://localhost:8888/api/web_fetch -d '{{\"url\":\"{url}\",\"extractMode\":\"markdown\"}}'")

print("\n" + "=" * 60)
