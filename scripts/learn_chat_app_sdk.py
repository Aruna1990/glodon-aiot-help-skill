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

# 添加技能目录到路径
SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

# 知识库目录
KNOWLEDGE_DIR = SKILL_DIR / "knowledge"
KNOWLEDGE_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = KNOWLEDGE_DIR / "chat_app_sdk.md"


def fetch_npm_readme():
    """从 NPM 获取包信息"""
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


def generate_sdk_doc():
    """生成 SDK 文档"""
    npm_info = fetch_npm_readme()
    
    doc = f"""# @glodon-aiot/chat-app-sdk 文档

> **版本**: {npm_info['version']} | **最后更新**: {datetime.now().strftime('%Y-%m-%d')} | **来源**: NPM Registry + 广联达官方文档

---

## 📦 包信息

| 属性 | 值 |
|------|-----|
| **包名** | @glodon-aiot/chat-app-sdk |
| **版本** | {npm_info['version']} |
| **描述** | {npm_info['description']} |
| **许可证** | {npm_info['license']} |
| **首页** | {npm_info['homepage']} |
| **关键词** | {', '.join(npm_info['keywords']) if npm_info['keywords'] else 'N/A'} |

---

## 🚀 快速开始

### 1. 安装

```bash
npm install @glodon-aiot/chat-app-sdk

# 或使用 yarn
yarn add @glodon-aiot/chat-app-sdk

# 或使用 pnpm
pnpm add @glodon-aiot/chat-app-sdk
```

### 2. 基础使用

```typescript
import {{ ChatApp }} from '@glodon-aiot/chat-app-sdk';

// 创建聊天应用实例
const chat = new ChatApp({{
  appId: 'YOUR_APP_ID',  // 从 Coze Studio 获取
  container: document.getElementById('chat-container'),
  theme: {{
    primaryColor: '#1677ff',
    backgroundColor: '#ffffff'
  }},
  config: {{
    showHistory: true,      // 显示消息历史
    enableFileUpload: true, // 启用文件上传
    enableVoice: false,     // 启用语音（可选）
    placeholder: '输入消息...' // 输入框占位符
  }}
}});

// 初始化
chat.init();

// 可选：监听事件
chat.on('message', (msg) => {{
  console.log('收到消息:', msg);
}});

chat.on('error', (err) => {{
  console.error('错误:', err);
}});
```

### 3. HTML 示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Coze Studio 聊天集成</title>
  <style>
    #chat-container {{
      width: 400px;
      height: 600px;
      border: 1px solid #ddd;
      border-radius: 8px;
    }}
  </style>
</head>
<body>
  <div id="chat-container"></div>
  
  <script type="module">
    import {{ ChatApp }} from '@glodon-aiot/chat-app-sdk';
    
    const chat = new ChatApp({{
      appId: 'YOUR_APP_ID',
      container: document.getElementById('chat-container')
    }});
    
    chat.init();
  </script>
</body>
</html>
```

---

## ⚙️ 配置选项

### ChatApp 构造函数参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `appId` | string | ✅ | Coze Studio 应用 ID |
| `container` | HTMLElement | ✅ | 聊天容器 DOM 元素 |
| `theme` | ThemeConfig | ❌ | 主题配置 |
| `config` | AppConfig | ❌ | 应用配置 |
| `token` | string | ❌ | 访问 Token（可选，默认从 appId 生成） |

### ThemeConfig 主题配置

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `primaryColor` | string | '#1677ff' | 主色调 |
| `backgroundColor` | string | '#ffffff' | 背景色 |
| `headerColor` | string | '#1677ff' | 头部背景色 |
| `textColor` | string | '#333333' | 文字颜色 |

### AppConfig 应用配置

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `showHistory` | boolean | true | 显示历史消息 |
| `enableFileUpload` | boolean | true | 启用文件上传 |
| `enableVoice` | boolean | false | 启用语音输入 |
| `placeholder` | string | '输入消息...' | 输入框占位符 |
| `maxHistoryLength` | number | 50 | 最大历史消息数 |
| `welcomeMessage` | string | 可选 | 欢迎消息 |

---

## 📡 API 方法

### 实例方法

#### `init()`
初始化聊天应用，必须在调用其他方法前执行。

```typescript
chat.init();
```

#### `destroy()`
销毁聊天应用，清理资源和事件监听器。

```typescript
chat.destroy();
```

#### `sendMessage(text: string)`
主动发送消息。

```typescript
chat.sendMessage('你好，有什么可以帮助的？');
```

#### `clearHistory()`
清空聊天历史。

```typescript
chat.clearHistory();
```

#### `setTheme(theme: ThemeConfig)`
动态修改主题。

```typescript
chat.setTheme({{ primaryColor: '#ff6600' }});
```

#### `show()` / `hide()`
显示/隐藏聊天窗口。

```typescript
chat.show();
chat.hide();
```

#### `toggle()`
切换显示状态。

```typescript
chat.toggle();
```

---

## 🎯 事件监听

### 可用事件

| 事件名 | 回调参数 | 说明 |
|--------|----------|------|
| `message` | `Message` | 收到新消息 |
| `error` | `Error` | 发生错误 |
| `ready` | `void` | 初始化完成 |
| `destroy` | `void` | 销毁完成 |
| `file-upload` | `File` | 文件上传开始 |
| `file-success` | `FileResult` | 文件上传成功 |
| `file-error` | `Error` | 文件上传失败 |

### 使用示例

```typescript
// 监听消息
chat.on('message', (msg) => {{
  console.log('消息类型:', msg.type);
  console.log('消息内容:', msg.content);
}});

// 监听错误
chat.on('error', (err) => {{
  console.error('聊天错误:', err.message);
}});

// 监听就绪
chat.on('ready', () => {{
  console.log('聊天应用已就绪');
}});

// 移除监听
chat.off('message', callback);

// 一次性监听
chat.once('ready', () => {{
  console.log('只触发一次');
}});
```

---

## 🔧 常见问题

### 1. 如何获取 appId？

1. 登录广联达行业 AI 平台：https://copilot.glodon.com/
2. 进入 Coze Studio
3. 创建或选择应用
4. 在应用设置中找到 **App ID**

### 2. Token 认证失败？

- 检查 appId 是否正确
- 确认应用已发布
- 检查网络请求是否被 CORS 阻止
- 联系平台管理员确认权限

### 3. 样式不生效？

- 确保容器有明确宽高
- 检查 CSS 优先级
- 使用 `!important` 覆盖默认样式（不推荐）
- 通过 `theme` 参数配置

### 4. 文件上传失败？

- 检查 `enableFileUpload` 是否为 `true`
- 确认文件大小限制（默认 10MB）
- 检查支持的文件类型

---

## 📚 相关文档

- [Coze Studio 入门指南](https://glodon-cv-help.yuque.com/cuv0se/ol9231/coze-studio-intro)
- [应用开发文档](https://glodon-cv-help.yuque.com/cuv0se/ol9231/app-dev)
- [API 参考](https://glodon-cv-help.yuque.com/cuv0se/ol9231/api-reference)
- [NPM 包页面](https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk)

---

## 📞 支持

- **技术问题**: 提交工单到广联达行业 AI 平台
- **文档问题**: 联系产品团队
- **紧急问题**: 联系技术支持热线

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
