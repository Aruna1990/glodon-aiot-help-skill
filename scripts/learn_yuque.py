#!/usr/bin/env python3
"""
语雀知识库学习脚本
使用内部 API 获取目录和文档内容（需要 Cookie）
"""

import os
import subprocess
import json
import re
import time
from datetime import datetime

# 配置
BOOK_ID = "41611578"  # 从用户提供的请求中获取
SPACE = "cuv0se"
BASE_URL = "https://glodon-cv-help.yuque.com"
API_URL = BASE_URL + "/api/docs?book_id=" + BOOK_ID
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge")
LEARN_STATE_FILE = os.path.join(KNOWLEDGE_DIR, ".learn_state.json")

# Cookie（从浏览器获取）
# 注意：Cookie 会过期，需要定期更新
COOKIE = os.environ.get("YUQUE_COOKIE", "")

# CSRF Token
CSRF_TOKEN = os.environ.get("YUQUE_CSRF", "")


def get_cookie_from_env():
    """从环境变量获取 Cookie"""
    if COOKIE:
        return COOKIE
    
    # 尝试从配置文件读取
    config_file = os.path.join(os.path.dirname(__file__), ".yuque_config")
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            for line in f:
                if line.startswith("cookie="):
                    return line.strip().split("=", 1)[1]
    return ""


def get_csrf_from_env():
    """从环境变量获取 CSRF Token"""
    if CSRF_TOKEN:
        return CSRF_TOKEN
    
    config_file = os.path.join(os.path.dirname(__file__), ".yuque_config")
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            for line in f:
                if line.startswith("csrf="):
                    return line.strip().split("=", 1)[1]
    return ""


def fetch_catalog():
    """获取知识库目录"""
    print("📑 获取知识库目录...")
    print("   API: " + API_URL)
    
    cookie = get_cookie_from_env()
    csrf = get_csrf_from_env()
    
    if not cookie:
        print("   ⚠️  未配置 Cookie")
        print("   请设置环境变量：export YUQUE_COOKIE='your_cookie'")
        print("   或创建配置文件：.yuque_config")
        return None
    
    # 构建 curl 命令
    cmd = "curl -s '" + API_URL + "'"
    cmd += " -X 'GET'"
    cmd += " -H 'Content-Type: application/json'"
    cmd += " -H 'Accept: application/json'"
    cmd += " -H 'User-Agent: Mozilla/5.0'"
    cmd += " -H 'Cookie: " + cookie + "'"
    cmd += " -H 'x-csrf-token: " + csrf + "'"
    cmd += " -H 'X-Requested-With: XMLHttpRequest'"
    
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        data = json.loads(output)
        
        if "data" in data:
            print("   ✓ 成功获取目录")
            print("   文档数量：" + str(len(data["data"])))
            return data["data"]
        else:
            print("   ❌ 响应格式异常")
            print("   " + str(data)[:200])
            return None
            
    except Exception as e:
        print("   ❌ 错误：" + str(e))
        return None


def fetch_doc_content(slug):
    """获取单个文档内容"""
    url = BASE_URL + "/" + SPACE + "/ol9231/" + slug
    print("   📥 " + slug)
    
    cookie = get_cookie_from_env()
    csrf = get_csrf_from_env()
    
    # 尝试从 HTML 页面提取内容
    cmd = "curl -s -L '" + url + "'"
    cmd += " -H 'Cookie: " + cookie + "'"
    cmd += " -H 'User-Agent: Mozilla/5.0'"
    
    try:
        html = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return html
    except Exception as e:
        print("      ❌ " + str(e))
        return None


def save_doc(slug, title, content):
    """保存文档"""
    output_file = os.path.join(KNOWLEDGE_DIR, slug + ".md")
    
    # 简单提取内容
    doc_content = "# " + title + "\n\n"
    doc_content += "> 来源：广联达行业 AI 平台文档中心\n"
    doc_content += "> 链接：" + BASE_URL + "/" + SPACE + "/ol9231/" + slug + "\n"
    doc_content += "> 学习时间：" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n"
    doc_content += "---\n\n"
    doc_content += "📖 **在线查看**: " + BASE_URL + "/" + SPACE + "/ol9231/" + slug + "\n\n"
    doc_content += "---\n\n"
    doc_content += "*本文档由 learn_yuque.py 自动生成*\n"
    
    with open(output_file, 'w') as f:
        f.write(doc_content)
    
    return output_file


def learn_from_catalog():
    """从目录学习所有文档"""
    print("=" * 60)
    print("📚 语雀知识库学习")
    print("=" * 60)
    print("知识库：" + BASE_URL + "/" + SPACE + "/ol9231")
    print("BOOK_ID: " + BOOK_ID)
    print("输出目录：" + KNOWLEDGE_DIR)
    print("=" * 60)
    print()
    
    # 获取目录
    catalog = fetch_catalog()
    
    if not catalog:
        print("\n❌ 无法获取目录，退出")
        return
    
    # 学习文档
    learned = 0
    failed = 0
    
    print("\n📖 开始学习文档...")
    print()
    
    for i, doc in enumerate(catalog, 1):
        slug = doc.get("slug", "")
        title = doc.get("title", "Untitled")
        
        print("[" + str(i) + "/" + str(len(catalog)) + "] " + title)
        
        if slug:
            # 获取内容
            content = fetch_doc_content(slug)
            
            if content:
                # 保存
                filepath = save_doc(slug, title, content)
                print("    ✓ " + filepath)
                learned += 1
            else:
                print("    ❌ 获取内容失败")
                failed += 1
        else:
            print("    ⏭️  无 slug，跳过")
        
        time.sleep(0.5)
    
    print()
    print("=" * 60)
    print("✅ 学习完成")
    print("=" * 60)
    print("成功：" + str(learned) + " 篇")
    print("失败：" + str(failed) + " 篇")
    print("=" * 60)
    
    # 保存状态
    state = {
        "last_sync": datetime.now().isoformat(),
        "book_id": BOOK_ID,
        "total_docs": len(catalog),
        "learned": learned,
        "failed": failed
    }
    
    with open(LEARN_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    
    print("\n💾 状态已保存：" + LEARN_STATE_FILE)


def show_config_help():
    """显示配置帮助"""
    print("=" * 60)
    print("🔧 配置帮助")
    print("=" * 60)
    print()
    print("方法 1：环境变量（推荐）")
    print()
    print("  export YUQUE_COOKIE='your_cookie_here'")
    print("  export YUQUE_CSRF='your_csrf_token'")
    print()
    print("方法 2：配置文件")
    print()
    print("  创建文件：.yuque_config")
    print("  内容格式：")
    print("    cookie=your_cookie_here")
    print("    csrf=your_csrf_token")
    print()
    print("获取 Cookie 方法：")
    print("  1. 打开浏览器访问：https://glodon-cv-help.yuque.com/cuv0se/ol9231")
    print("  2. 按 F12 打开开发者工具")
    print("  3. 切换到 Network 标签")
    print("  4. 刷新页面")
    print("  5. 找到 api/docs 请求")
    print("  6. 复制 Cookie 和 x-csrf-token")
    print()
    print("=" * 60)


def main():
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--config":
            show_config_help()
            return
        elif sys.argv[1] == "--catalog":
            fetch_catalog()
            return
    
    learn_from_catalog()


if __name__ == "__main__":
    main()
