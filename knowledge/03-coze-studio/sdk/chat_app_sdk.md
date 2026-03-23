# @glodon-aiot/chat-app-sdk 文档

> **版本**: 0.0.30 | **最后更新**: 2026-03-23 | **来源**: NPM 包 README（与 npm 官网完全一致）

---

## 📦 包信息

| 属性 | 值 |
|------|-----|
| **包名** | @glodon-aiot/chat-app-sdk |
| **版本** | 0.0.30 |
| **描述** | Glodon AIoT Chat App SDK |
| **许可证** | MIT |
| **首页** | https://copilot.glodon.com/ |
| **NPM 地址** | https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk |

---

# @glodon-aiot/chat-app-sdk

Glodon AIoT Chat App SDK - 基于广联达行业AI平台的智能聊天 SDK，支持浮窗和嵌入两种模式，提供完整的 TypeScript 类型定义和 Web Components 支持。

[![npm version](https://img.shields.io/npm/v/@glodon-aiot/chat-app-sdk.svg)](https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk)
[![npm downloads](https://img.shields.io/npm/dm/@glodon-aiot/chat-app-sdk.svg)](https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk)
[![License](https://img.shields.io/npm/l/@glodon-aiot/chat-app-sdk.svg)](https://github.com/glodon-aiot/chat-app-sdk/blob/main/LICENSE)

## 📚 在线示例

**🎯 [查看完整示例和演示](https://glodon-aiot.github.io/chat-app-sdk-demo/live/#/demo)**

示例项目展示了以下功能：
- ✅ Web Components 集成
- ✅ 自定义 JsonItem 组件
- ✅ 自定义 ContentBox 组件
- ✅ 搜索结果展示
- ✅ 知识库引用展示
- ✅ 联网搜索开关
- ✅ Bot 和 App 两种模式

## ✨ 特性

- 🎯 **多模式支持**：浮窗模式和嵌入模式自由切换
- 📦 **多种引入方式**：支持 npm 安装和 CDN 引入
- 🔷 **Web Components**：支持自定义 Web Components 扩展
- 📘 **类型安全**：完整的 TypeScript 类型定义
- ⚛️ **React 友好**：完美支持 React 项目集成
- 📱 **移动端适配**：自动检测设备类型并适配布局
- 🎨 **高度可定制**：丰富的 UI 配置选项
- 🔄 **Token 自动刷新**：支持 Token 过期自动刷新

## 📦 安装

### NPM 安装

```bash
# 使用 npm
npm install @glodon-aiot/chat-app-sdk

# 使用 pnpm
pnpm add @glodon-aiot/chat-app-sdk

# 使用 yarn
yarn add @glodon-aiot/chat-app-sdk
```

### CDN 引入

```html
<!-- 最新版本 -->
<script src="https://unpkg.com/@glodon-aiot/chat-app-sdk@latest/libs/cn/index.js"></script>

<!-- 指定版本 -->
<script src="https://unpkg.com/@glodon-aiot/chat-app-sdk@0.0.1-alpha.19/libs/cn/index.js"></script>

<!-- 或使用 jsDelivr -->
<script src="https://cdn.jsdelivr.net/npm/@glodon-aiot/chat-app-sdk@latest/libs/cn/index.js"></script>
```

## 🚀 快速开始

### 基础用法（NPM）

```typescript
import { WebChatClient } from '@glodon-aiot/chat-app-sdk';

// 创建聊天客户端实例
const client = new WebChatClient({
  mode: 'float', // 'float' 浮窗模式 | 'embed' 嵌入模式

  config: {
    type: 'app',
    appInfo: {
      appId: 'your-app-id',
      workflowId: 'your-workflow-id',
      draft_mode: false, // 是否使用草稿模式
    },
    apiUrl: 'https://your-api-domain.com/api', // 可选：自定义 API 地址
  },

  auth: {
    type: 'token',
    token: 'your-token',
    onRefreshToken: async () => {
      // Token 刷新逻辑
      const response = await fetch('/api/refresh-token');
      const { token } = await response.json();
      return token;
    },
  },

  ui: {
    base: {
      layout: 'pc', // 'pc' | 'mobile'
      lang: 'zh-CN', // 'zh-CN' | 'en-US'
    },
    chatBot: {
      title: '智能助手',
      uploadable: true,
      width: 400,
    },
  },
});

// 显示聊天窗口
client.showChatBot();

// 隐藏聊天窗口
client.hideChatBot();

// 销毁实例
client.destroy();
```

### React 集成

```tsx
import React, { useEffect, useRef } from 'react';
import { WebChatClient } from '@glodon-aiot/chat-app-sdk';

function ChatComponent() {
  const containerRef = useRef<HTMLDivElement>(null);
  const clientRef = useRef<WebChatClient | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    clientRef.current = new WebChatClient({
      mode: 'embed',
      getContainer: () => containerRef.current!,
      config: {
        type: 'app',
        appInfo: {
          appId: 'your-app-id',
          workflowId: 'your-workflow-id',
        },
      },
      auth: {
        type: 'token',
        token: 'your-token',
        onRefreshToken: async () => {
          // 刷新 token 逻辑
          return 'new-token';
        },
      },
    });

    return () => {
      clientRef.current?.destroy();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      style={{ width: '100%', height: '100vh' }}
    />
  );
}
```

### CDN 使用

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Glodon AIoT Chat SDK</title>
</head>
<body>
  <div id="chat-container" style="width: 100%; height: 100vh;"></div>

  <!-- 引入 SDK -->
  <script src="https://unpkg.com/@glodon-aiot/chat-app-sdk@latest/libs/cn/index.js"></script>

  <script>
    // 使用全局变量 GlodonAIoT
    const client = new window.GlodonAIoT.WebChatClient({
      mode: 'embed',
      getContainer: () => document.getElementById('chat-container'),
      config: {
        type: 'app',
        appInfo: {
          appId: 'your-app-id',
          workflowId: 'your-workflow-id',
        },
      },
      auth: {
        type: 'token',
        token: 'your-token',
        onRefreshToken: function() {
          return 'your-new-token';
        },
      },
    });
  </script>
</body>
</html>
```

## 🎯 两种模式

### 浮窗模式（Float）

显示悬浮按钮，点击后弹出聊天窗口。适合作为页面辅助功能。

```typescript
const client = new WebChatClient({
  mode: 'float', // 浮窗模式
  config: {
    type: 'app',
    appInfo: {
      appId: 'your-app-id',
      workflowId: 'your-workflow-id',
    },
  },
  auth: {
    type: 'token',
    token: 'your-token',
  },
});
```

### 嵌入模式（Embed）

全屏展示聊天页面，自动打开。适合专门的聊天页面。

```typescript
const client = new WebChatClient({
  mode: 'embed',
  getContainer: () => document.getElementById('chat-container'),
  config: {
    type: 'app',
    appInfo: {
      appId: 'your-app-id',
      workflowId: 'your-workflow-id',
    },
  },
  auth: {
    type: 'token',
    token: 'your-token',
  },
});
```

## 🔷 Web Components 支持

SDK 支持通过 Web Components 自定义组件，实现更灵活的 UI 扩展。

### 注册自定义组件

```typescript
import { WebChatClient } from '@glodon-aiot/chat-app-sdk';

// 注册自定义 Web Components
customElements.define('custom-json-item', CustomJsonItem);
customElements.define('custom-content-box', CustomContentBox);

const client = new WebChatClient({
  // ... 配置
  ui: {
    uiKitCustomWebComponents: {
      JsonItem: 'custom-json-item', // 使用自定义 JsonItem
    },
    contentBoxWebComponent: 'custom-content-box', // 使用自定义 ContentBox
  },
});
```

### 示例组件

查看 [在线示例](https://glodon-aiot.github.io/chat-app-sdk-demo/live/#/demo) 了解以下组件的实现：

- `knowledge-reference-list` - 知识库引用列表组件
- `search-result-list` - 搜索结果列表组件
- `demo-json-item` - 自定义 JsonItem 组件
- `demo-content-box` - 自定义 ContentBox 组件

## 📖 API 文档

### WebChatClient 构造函数

```typescript
new WebChatClient(options: WebChatOptions)
```

### WebChatOptions

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `mode` | `'float' \| 'embed'` | 是 | 渲染模式 |
| `config` | `BotConfig` | 是 | Bot 配置信息 |
| `auth` | `AuthConfig` | 是 | 认证配置 |
| `ui` | `UIConfig` | 否 | UI 配置 |
| `getContainer` | `() => HTMLElement` | 否 | 容器元素（embed 模式必需） |
| `env` | `'test' \| 'prod'` | 否 | 环境配置 |
| `apiUrl` | `string` | 否 | 自定义 API 地址 |

### BotConfig

```typescript
{
  type: 'app',
  appInfo: {                  // 必填
    appId: string,             // 应用 ID
    workflowId: string,        // 工作流 ID
    draft_mode?: boolean,      // 是否使用草稿模式
    parameters?: Record<string, unknown>, // 工作流参数
  },
  apiUrl?: string,             // 可选：自定义 API 地址
}
```

### AuthConfig

```typescript
{
  type: 'token',                              // 认证类型
  token: string,                              // 访问令牌
  onRefreshToken?: () => string | Promise<string>, // Token 刷新回调
}
```

### UIConfig

```typescript
{
  base?: {
    layout?: 'pc' | 'mobile',   // 布局模式
    lang?: string,               // 语言设置
    zIndex?: number,             // z-index 层级
    icon?: string,               // 自定义图标
  },
  chatBot?: {
    title?: string,              // 聊天窗口标题
    uploadable?: boolean,        // 是否支持上传
    width?: number,              // 窗口宽度
    isNeedClearContext?: boolean, // 是否需要清除上下文
    isNeedClearMessage?: boolean, // 是否需要清除消息
    isNeedAddNewConversation?: boolean, // 是否需要新建会话
    isNeedFunctionCallMessage?: boolean, // 是否需要函数调用消息
  },
  header?: {
    isShow?: boolean,            // 是否显示头部
    isNeedClose?: boolean,       // 是否显示关闭按钮
  },
  asstBtn?: {
    isNeed?: boolean,            // 是否显示浮动按钮
  },
  conversations?: {
    isNeed?: boolean,            // 是否需要会话列表
  },
  input?: {
    placeholder?: string,        // 输入框占位符
    isShow?: boolean,           // 是否显示输入框
    defaultText?: string,       // 默认文本
    renderChatInputRightActions?: () => ReactNode, // 自定义右侧操作按钮
  },
  uiKitCustomWebComponents?: {
    JsonItem?: string,          // 自定义 JsonItem 组件名称
  },
  contentBoxWebComponent?: string, // 自定义 ContentBox 组件名称
  getMessageRenderIndex?: (message: unknown) => number, // 自定义消息渲染索引
}
```

### WebChatClient 实例方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `showChatBot()` | 显示聊天窗口 | `void` |
| `hideChatBot()` | 隐藏聊天窗口 | `void` |
| `destroy()` | 销毁实例，清理资源 | `void` |

### WebChatClient 实例属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `chatClientId` | `string` | 客户端唯一 ID |
| `options` | `WebChatOptions` | 配置选项 |
| `senderName` | `string` | 发送者名称 |
| `apiUrl` | `string` | API 地址 |

## 🔧 常见问题

### Q1: 如何获取 appId 和 workflowId？

需要从广联达行业AI平台获取：
1. 登录 [广联达行业AI平台](https://copilot.glodon.com/)
2. 从“产品中心”选择“行业AI平台”
3. 左侧menu中点击“Coze Studio -> 项目开发”
2. 创建或选择你的应用
3. 在应用"发布状态"中找到相应的 ID

### Q2: CDN 引入后如何使用？

SDK 会在 `window.GlodonAIoT` 上暴露 API：

```javascript
const client = new window.GlodonAIoT.WebChatClient({
  // 配置...
});
```

### Q3: 支持哪些浏览器？

支持所有现代浏览器：
- Chrome >= 88
- Firefox >= 85
- Safari >= 14
- Edge >= 88

### Q4: 如何处理 Token 过期？

通过 `onRefreshToken` 回调处理：

```typescript
auth: {
  type: 'token',
  token: 'current-token',
  onRefreshToken: async () => {
    // 调用你的 API 获取新 token
    const response = await fetch('/api/refresh-token');
    const { token } = await response.json();
    return token;
  },
}
```

### Q5: 如何在嵌入模式下设置容器高度？

容器会自动填满 100% 高度，确保父元素有明确的高度：

```html
<div id="chat-container" style="height: 100vh;"></div>
```

### Q6: 如何自定义 Web Components？

参考 [在线示例](https://glodon-aiot.github.io/chat-app-sdk-demo/live/#/demo) 中的实现，注册自定义组件并在配置中指定：

```typescript
// 注册组件
customElements.define('my-json-item', MyJsonItem);

// 在配置中使用
ui: {
  uiKitCustomWebComponents: {
    JsonItem: 'my-json-item',
  },
}
```

### Q7: 如何切换 Bot 和 App 模式？

通过 `config.type` 字段切换：

```typescript
// Bot 模式
config: {
  type: 'bot',
  botId: 'your-bot-id',
}

// App 模式
config: {
  type: 'app',
  appInfo: {
    appId: 'your-app-id',
    workflowId: 'your-workflow-id',
  },
}
```

## 🌐 环境要求

- **Node.js**: >= 18
- **React**: >= 18.2.0 (如果使用 React)
- **ReactDOM**: >= 18.2.0 (如果使用 React)
- **浏览器**: 支持 ES6+ 的现代浏览器

## 📄 许可证

Apache-2.0

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系我们

如有问题或建议，请联系 Glodon AIoT 团队。

## 🔗 相关链接

- 📚 [在线示例和演示](https://glodon-aiot.github.io/chat-app-sdk-demo/live/#/demo)
- 📦 [npm 包地址](https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk)
- 📖 [广联达行业AI平台官方文档](https://glodon-cv-help.yuque.com/cuv0se/ol9231)

---

**Made with ❤️ by Glodon AIoT Team**


---

_本文档由 glodon-ai-help 技能自动生成，内容来自 NPM 包 README，最后更新：2026-03-23 11:32_
