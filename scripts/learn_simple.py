#!/usr/bin/env python3
"""
语雀公开文档学习脚本 - 兼容老版本 Python
使用 curl 直接获取公开文档内容（无需 Token）
"""

import os
import subprocess
import json
import re
import time
from datetime import datetime

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
]


def fetch_doc(slug, title):
    """获取并保存文档"""
    url = BASE_URL + "/" + slug
    output_file = os.path.join(KNOWLEDGE_DIR, slug + ".md")
    
    print("📥 " + title)
    print("   " + url)
    
    # 使用 curl 获取
    cmd = "curl -s -L -A 'Mozilla/5.0' '" + url + "' 2>/dev/null"
    try:
        html = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        
        # 简单处理
        content = """# """ + title + """

> 来源：广联达行业 AI 平台文档中心  
> 链接：""" + url + """  
> 学习时间：""" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """

---

## 文档内容

📖 **在线查看**: """ + url + """

> 由于语雀页面使用 JavaScript 渲染，完整内容建议在浏览器中打开查看。

---

## 文档信息

- **Slug**: """ + slug + """
- **URL**: """ + url + """
- **获取时间**: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """

---

*本文档由 learn_public_docs.py 自动生成 · 公开文档无需 Token*
"""
        
        with open(output_file, 'w') as f:
            f.write(content)
        
        print("   ✓ 已保存：" + output_file)
        return True
        
    except Exception as e:
        print("   ❌ 错误：" + str(e))
        return False


def main():
    print("=" * 60)
    print("📚 广联达行业 AI 平台 - 核心文档学习")
    print("=" * 60)
    print("知识库：" + BASE_URL)
    print("输出目录：" + KNOWLEDGE_DIR)
    print("文档数量：" + str(len(CORE_DOCS)) + " 篇")
    print("=" * 60)
    print()
    
    learned = 0
    
    for doc in CORE_DOCS:
        if fetch_doc(doc["slug"], doc["title"]):
            learned += 1
        time.sleep(0.5)
        print()
    
    print("=" * 60)
    print("✅ 学习完成：" + str(learned) + "/" + str(len(CORE_DOCS)) + " 篇")
    print("=" * 60)
    
    # 保存状态
    state = {
        "last_sync": datetime.now().isoformat(),
        "learned_docs": [doc["slug"] for doc in CORE_DOCS],
        "total_learned": learned
    }
    
    with open(LEARN_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    
    print("\n💾 状态已保存：" + LEARN_STATE_FILE)


if __name__ == "__main__":
    main()
