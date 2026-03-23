#!/usr/bin/env python3
"""
学习 @glodon-aiot/chat-app-sdk 文档

从以下来源获取 SDK 文档：
1. NPM 包页面：https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk
2. GitHub Repo（如果有）
3. 广联达官方文档

用法：
    python3 learn_chat_app_sdk.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加技能根目录到路径（scripts/ 的父目录）
SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

# 知识库目录
KNOWLEDGE_DIR = SKILL_DIR / "knowledge"
KNOWLEDGE_DIR.mkdir(exist_ok=True)

# 知识库 SDK 文档路径（需与 03-coze-studio/sdk/ 目录结构一致）
OUTPUT_DIR = KNOWLEDGE_DIR / "03-coze-studio" / "sdk"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "chat_app_sdk.md"


def fetch_npm_package_info():
    """从 NPM Registry 获取包元信息（版本、描述等）"""
    import urllib.request

    url = "https://registry.npmjs.org/@glodon-aiot/chat-app-sdk"

    try:
        req = urllib.request.Request(url, headers={
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (compatible; GlodonAIHelp/1.0)'
        })

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))

            latest = data.get('dist-tags', {}).get('latest', 'unknown')
            description = data.get('description', '广联达 Coze Studio 前端聊天应用 SDK')
            homepage = data.get('homepage', 'https://copilot.glodon.com/')
            repository = data.get('repository', {})

            return {
                'version': latest,
                'description': description,
                'homepage': homepage,
                'repository': repository,
                'keywords': data.get('keywords', []),
                'author': data.get('author', {}),
                'license': data.get('license', 'MIT')
            }
    except Exception as e:
        print(f"⚠️  无法从 NPM 获取信息：{e}")
        return {
            'version': 'latest',
            'description': '广联达 Coze Studio 前端聊天应用 SDK',
            'homepage': 'https://copilot.glodon.com/',
            'repository': {},
            'keywords': ['glodon', 'coze', 'chat', 'ai', 'sdk'],
            'author': {},
            'license': 'Proprietary'
        }


def fetch_npm_readme_content():
    """从 NPM 网站获取 README 完整内容（含实际 API 用法）"""
    import urllib.request

    # 使用 unpkg 获取包的 README（npm 官网页面内容来自包内 README）
    readme_urls = [
        "https://unpkg.com/@glodon-aiot/chat-app-sdk@latest/README.md",
        "https://raw.githubusercontent.com/glodon-aiot/chat-app-sdk/main/README.md",
    ]

    for url in readme_urls:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; GlodonAIHelp/1.0)'
            })
            with urllib.request.urlopen(req, timeout=15) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"⚠️  尝试 {url} 失败：{e}")
            continue

    return None


def generate_sdk_doc():
    """生成 SDK 文档：优先使用 NPM README 内容，保证与 npm 官网一致"""
    npm_info = fetch_npm_package_info()
    readme_content = fetch_npm_readme_content()

    # 若成功获取 README，以其为主；否则回退到精简版（仅含正确 API 的说明）
    if readme_content:
        # 使用 README 主体内容，仅补充技能相关说明
        doc = f"""# @glodon-aiot/chat-app-sdk 文档

> **版本**: {npm_info['version']} | **最后更新**: {datetime.now().strftime('%Y-%m-%d')} | **来源**: NPM 包 README（与 npm 官网完全一致）

---

## 📦 包信息

| 属性 | 值 |
|------|-----|
| **包名** | @glodon-aiot/chat-app-sdk |
| **版本** | {npm_info['version']} |
| **描述** | {npm_info['description']} |
| **许可证** | {npm_info['license']} |
| **首页** | {npm_info['homepage']} |
| **NPM 地址** | https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk |

---

{readme_content}

---

_本文档由 glodon-ai-help 技能自动生成，内容来自 NPM 包 README，最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}_
"""
    else:
        # 回退：使用与 npm README 一致的 API（WebChatClient 而非 ChatApp）
        doc = f"""# @glodon-aiot/chat-app-sdk 文档

> **版本**: {npm_info['version']} | **最后更新**: {datetime.now().strftime('%Y-%m-%d')} | **来源**: NPM Registry（建议直接查阅 [NPM 官网](https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk) 获取完整 README）

---

## 📦 包信息

| 属性 | 值 |
|------|-----|
| **包名** | @glodon-aiot/chat-app-sdk |
| **版本** | {npm_info['version']} |
| **描述** | {npm_info['description']} |
| **NPM 地址** | https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk |

---

## 🚀 快速开始（与 NPM README 一致）

### 基础用法

```typescript
import {{ WebChatClient }} from '@glodon-aiot/chat-app-sdk';

const client = new WebChatClient({{
  mode: 'float', // 'float' 浮窗 | 'embed' 嵌入

  config: {{
    type: 'app',
    appInfo: {{
      appId: 'your-app-id',
      workflowId: 'your-workflow-id',
      draft_mode: false,
    }},
  }},

  auth: {{
    type: 'token',
    token: 'your-token',
    onRefreshToken: async () => {{
      const res = await fetch('/api/refresh-token');
      const {{ token }} = await res.json();
      return token;
    }},
  }},

  ui: {{
    base: {{ layout: 'pc', lang: 'zh-CN' }},
    chatBot: {{ title: '智能助手', uploadable: true }},
  }},
}});

client.showChatBot();
client.hideChatBot();
client.destroy();
```

### 嵌入模式

```typescript
const client = new WebChatClient({{
  mode: 'embed',
  getContainer: () => document.getElementById('chat-container'),
  config: {{ type: 'app', appInfo: {{ appId: '...', workflowId: '...' }} }},
  auth: {{ type: 'token', token: 'your-token' }},
}});
```

**重要**：回答 @glodon-aiot 包时必须使用 NPM 官网 README 内容，请访问：
https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk

---

_本文档由 glodon-ai-help 技能自动生成，最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}_
"""

    return doc


def main():
    print("📚 开始学习 @glodon-aiot/chat-app-sdk 文档...")
    
    # 生成文档
    doc = generate_sdk_doc()
    
    # 写入文件
    OUTPUT_FILE.write_text(doc, encoding='utf-8')
    
    print(f"✅ 文档已保存到：{OUTPUT_FILE}")
    print(f"📄 文件大小：{OUTPUT_FILE.stat().st_size} 字节")
    
    # 更新学习状态
    state_file = SKILL_DIR / ".learn_state.json"
    state = {}
    if state_file.exists():
        state = json.loads(state_file.read_text())
    
    state['chat_app_sdk'] = {
        'last_learned': datetime.now().isoformat(),
        'version': 'auto',
        'source': 'npm_registry'
    }
    
    state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    print(f"💾 学习状态已更新")
    
    print("\n🎉 完成！现在可以回答关于 Coze Studio 前端 SDK 集成的问题了。")


if __name__ == '__main__':
    main()
