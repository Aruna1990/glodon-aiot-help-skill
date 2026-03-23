#!/usr/bin/env python3
"""
统一学习入口：检查 + 按需学习

功能：
1. 检查 knowledge/ 目录状态
2. 检测知识缺失时自动触发学习
3. 支持查看学习状态

用法：
    python3 check_and_learn.py              # 检查并学习
    python3 check_and_learn.py --state      # 查看状态
    python3 check_and_learn.py --force      # 强制重新学习
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 技能根目录（scripts/ 的父目录）
SKILL_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = SKILL_DIR / "knowledge"
STATE_FILE = KNOWLEDGE_DIR / ".learn_state.json"


def check_knowledge_state() -> Dict:
    """检查知识库状态"""
    state = {
        "knowledge_dir_exists": KNOWLEDGE_DIR.exists(),
        "state_file_exists": STATE_FILE.exists(),
        "directories": [],
        "files_count": 0,
        "last_sync": None,
        "needs_learning": False,
    }
    
    if not KNOWLEDGE_DIR.exists():
        state["needs_learning"] = True
        return state
    
    # 检查目录结构（排除隐藏文件和 README）
    for dir_path in KNOWLEDGE_DIR.iterdir():
        if dir_path.is_dir() and not dir_path.name.startswith("."):
            state["directories"].append(dir_path.name)
            # 统计文件数
            files = list(dir_path.rglob("*.md"))
            state["files_count"] += len(files)
    
    # 也统计根目录的 md 文件
    root_files = [f for f in KNOWLEDGE_DIR.glob("*.md") if f.name != "README.md"]
    state["files_count"] += len(root_files)
    
    # 检查状态文件
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            learn_state = json.load(f)
            state["last_sync"] = learn_state.get("last_sync")
    
    # 如果没有任何文档，需要学习
    if state["files_count"] == 0:
        state["needs_learning"] = True
    
    return state


def run_learn_script(script_name: str, args: List[str] = None) -> bool:
    """运行学习脚本"""
    script_path = SKILL_DIR / "scripts" / script_name
    
    if not script_path.exists():
        print(f"❌ 脚本不存在：{script_path}")
        return False
    
    try:
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        
        import subprocess
        # Python 3.6 兼容：使用 stdout=None 而不是 capture_output=False
        result = subprocess.run(cmd, cwd=str(SKILL_DIR), stdout=None, stderr=None)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行失败：{e}")
        return False


def learn_core_docs() -> bool:
    """学习核心文档（语雀）"""
    print("\n📚 正在学习语雀公开文档...")
    return run_learn_script("learn_public_docs.py", ["--core"])


def learn_sdk_docs() -> bool:
    """学习 SDK 文档（NPM）"""
    print("\n📦 正在学习 SDK 文档...")
    success1 = run_learn_script("learn_chat_app_sdk.py")
    success2 = run_learn_script("learn_bot_client_ui.py")
    return success1 and success2


def learn_all() -> bool:
    """学习所有文档"""
    print("=" * 60)
    print("🎯 开始学习广联达行业 AI 平台文档")
    print("=" * 60)
    
    # 学习语雀文档
    success1 = learn_core_docs()
    
    # 学习 SDK 文档
    success2 = learn_sdk_docs()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("✅ 学习完成！")
    else:
        print("⚠️  部分学习失败")
    print("=" * 60)
    
    return success1 and success2


def show_state():
    """显示详细状态"""
    state = check_knowledge_state()
    
    print("=" * 60)
    print("📊 知识库状态")
    print("=" * 60)
    print(f"知识库目录：{KNOWLEDGE_DIR}")
    print(f"目录存在：{'✅' if state['knowledge_dir_exists'] else '❌'}")
    print(f"状态文件：{'✅' if state['state_file_exists'] else '❌'}")
    print(f"文档目录：{len(state['directories'])} 个")
    print(f"文档数量：{state['files_count']} 篇")
    print(f"最后同步：{state['last_sync'] or '从未同步'}")
    print(f"需要学习：{'✅ 是' if state['needs_learning'] else '❌ 否'}")
    print("=" * 60)
    
    if state['directories']:
        print("\n文档目录 (按语雀结构自动创建):")
        for dir_name in sorted(state['directories']):
            dir_path = KNOWLEDGE_DIR / dir_name
            files = list(dir_path.rglob("*.md"))
            print(f"  {dir_name}: {len(files)} 篇")
    
    # 显示根目录文件
    root_files = [f.name for f in KNOWLEDGE_DIR.glob("*.md") if f.name != "README.md"]
    if root_files:
        print(f"\n根目录文件：{len(root_files)} 篇")


def main():
    parser = argparse.ArgumentParser(description="广联达 AI 帮助 - 统一学习入口")
    parser.add_argument("--state", action="store_true", help="查看状态")
    parser.add_argument("--force", action="store_true", help="强制重新学习")
    parser.add_argument("--topic", type=str, help="学习特定主题 (platform|api|sdk|all)")
    
    args = parser.parse_args()
    
    # 查看状态
    if args.state:
        show_state()
        return
    
    # 检查知识库状态
    state = check_knowledge_state()
    
    if state["needs_learning"] or args.force:
        print("📚 检测到知识库为空或需要更新")
        
        if args.topic == "api":
            learn_core_docs()
        elif args.topic == "sdk":
            learn_sdk_docs()
        else:
            learn_all()
    else:
        print("✅ 知识库已就绪")
        print(f"   文档数量：{state['files_count']} 篇")
        print(f"   最后同步：{state['last_sync']}")
        print("\n💡 提示:")
        print("   --force  强制重新学习")
        print("   --topic  学习特定主题 (platform|api|sdk|all)")
        print("   --state  查看详细状态")


if __name__ == "__main__":
    main()
