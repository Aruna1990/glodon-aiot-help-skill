#!/usr/bin/env python3
"""
语雀文档同步脚本
从广联达行业 AI 平台语雀知识库同步文档
"""

import requests
import json
import os
from datetime import datetime

# 配置
YUQUE_TOKEN = os.getenv("YUQUE_TOKEN", "")
YUQUE_BASE_URL = "https://www.yuque.com/api/v2"
SPACE_ID = "cuv0se"
BOOK_ID = "ol9231"
OUTPUT_DIR = "knowledge"

class YuqueSync:
    def __init__(self):
        self.session = requests.Session()
        if YUQUE_TOKEN:
            self.session.headers.update({
                "X-Auth-Token": YUQUE_TOKEN
            })
    
    def get_book_info(self):
        """获取知识库信息"""
        url = f"{YUQUE_BASE_URL}/spaces/{SPACE_ID}/books/{BOOK_ID}"
        response = self.session.get(url)
        return response.json()
    
    def get_docs(self):
        """获取文档列表"""
        url = f"{YUQUE_BASE_URL}/spaces/{SPACE_ID}/books/{BOOK_ID}/docs"
        response = self.session.get(url)
        return response.json()
    
    def get_doc_content(self, doc_id):
        """获取文档内容"""
        url = f"{YUQUE_BASE_URL}/spaces/{SPACE_ID}/books/{BOOK_ID}/docs/{doc_id}"
        response = self.session.get(url)
        return response.json()
    
    def sync_all(self, output_dir=OUTPUT_DIR):
        """同步所有文档"""
        print(f"开始同步语雀文档...")
        print(f"知识库：{SPACE_ID}/{BOOK_ID}")
        
        # 获取文档列表
        docs_response = self.get_docs()
        if 'data' not in docs_response:
            print(f"获取文档列表失败：{docs_response}")
            return
        
        docs = docs_response['data']
        print(f"找到 {len(docs)} 篇文档")
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 同步每篇文档
        for doc in docs:
            doc_id = doc['id']
            slug = doc['slug']
            title = doc['title']
            
            print(f"同步：{title}")
            
            # 获取文档内容
            content_response = self.get_doc_content(doc_id)
            if 'data' not in content_response:
                print(f"  获取内容失败")
                continue
            
            content = content_response['data']
            body = content.get('body', '')
            
            # 保存为 Markdown
            filename = f"{slug}.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"> 来源：语雀知识库\n")
                f.write(f"> 最后更新：{content.get('updated_at', '')}\n\n")
                f.write(f"---\n\n")
                f.write(body)
            
            print(f"  保存到：{filepath}")
        
        print(f"\n同步完成！共同步 {len(docs)} 篇文档")


if __name__ == "__main__":
    import sys
    
    if not YUQUE_TOKEN:
        print("⚠️  警告：未设置 YUQUE_TOKEN 环境变量")
        print("   部分公开文档可访问，但可能无法获取完整内容")
        print("")
    
    syncer = YuqueSync()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "list":
            # 列出文档
            docs = syncer.get_docs()
            if 'data' in docs:
                print(f"知识库文档列表:")
                for doc in docs['data']:
                    print(f"  - {doc['title']} ({doc['slug']})")
        
        elif cmd == "sync":
            # 同步所有文档
            syncer.sync_all()
        
        else:
            print(f"未知命令：{cmd}")
            print("用法：python3 sync_yuque.py [list|sync]")
    else:
        # 默认同步
        syncer.sync_all()
