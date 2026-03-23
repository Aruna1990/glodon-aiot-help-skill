# @glodon-aiot/bot-client-ui 文档（旧版）

> **⚠️ 已废弃** - 此 SDK 已被 **Coze Studio** 取代，新项目请使用 `@glodon-aiot/chat-app-sdk`  
> **版本**: 3.17.0 | **最后更新**: 2026-03-20 18:03 | **来源**: NPM Registry + 广联达官方文档

---

## 📦 包信息

| 属性 | 值 |
|------|-----|
| **包名** | @glodon-aiot/bot-client-ui |
| **版本** | 3.17.0 |
| **描述** | aiot libembeds |
| **许可证** | MIT |
| **状态** | ⚠️ **已废弃 / Deprecated** |
| **首页** | https://copilot.glodon.com/ |
| **替代方案** | `@glodon-aiot/chat-app-sdk` (Coze Studio) |

---

## ⚠️ 重要说明

### 为什么被废弃？

`bot-client-ui` 是广联达行业 AI 平台**早期版本**的前端集成方案，存在以下限制：

1. **功能有限** - 仅支持基础对话，缺少文件上传、语音、富媒体等
2. **配置复杂** - 需要手动管理 Token 和会话状态
3. **样式固化** - 主题定制能力弱
4. **维护停止** - 官方已停止更新，转向 Coze Studio

### 迁移建议

| 项目状态 | 建议 |
|----------|------|
| **新项目** | ✅ 使用 **Coze Studio** (`@glodon-aiot/chat-app-sdk`) |
| **旧项目维护** | ⚠️ 可继续使用，但建议规划迁移 |
| **遇到问题** | 🔧 优先升级到 Coze Studio |

---

## 🚀 历史用法（供参考）

### 1. 安装

```bash
npm install @glodon-aiot/bot-client-ui
```

### 2. 基础使用（旧版 API）

```javascript
import BotClientUI from '@glodon-aiot/bot-client-ui';

const bot = new BotClientUI({
  container: document.getElementById('bot-container'),
  botId: 'YOUR_BOT_ID',
  token: 'YOUR_TOKEN'
});

bot.init();
```

### 3. HTML 示例

```html
<div id="bot-container"></div>
<script>
  const bot = new BotClientUI({
    container: document.getElementById('bot-container'),
    botId: 'YOUR_BOT_ID',
    token: 'YOUR_TOKEN'
  });
  bot.init();
</script>
```

---

## 📡 旧版 API 方法

| 方法 | 说明 |
|------|------|
| `init()` | 初始化 |
| `destroy()` | 销毁 |
| `sendMessage(text)` | 发送消息 |
| `clearHistory()` | 清空历史 |
| `show()` / `hide()` | 显示/隐藏 |

### 事件监听

```javascript
bot.on('message', (msg) => {
  console.log('收到消息:', msg);
});

bot.on('error', (err) => {
  console.error('错误:', err);
});
```

---

## 🔄 迁移到 Coze Studio

### 对比表

| 特性 | bot-client-ui (旧) | chat-app-sdk (新) |
|------|-------------------|------------------|
| **包名** | `@glodon-aiot/bot-client-ui` | `@glodon-aiot/chat-app-sdk` |
| **认证方式** | botId + Token | appId (自动管理 Token) |
| **配置方式** | 手动配置 | 声明式配置 |
| **主题定制** | 有限 | 完整 ThemeConfig |
| **文件上传** | ❌ | ✅ |
| **语音输入** | ❌ | ✅ |
| **消息历史** | 基础 | 可配置长度 |
| **事件系统** | 基础 | 完整事件类型 |
| **维护状态** | ⚠️ 已停止 | ✅ 活跃更新 |

### 迁移步骤

**1. 更换 NPM 包**
```bash
npm uninstall @glodon-aiot/bot-client-ui
npm install @glodon-aiot/chat-app-sdk
```

**2. 修改代码**

旧代码:
```javascript
import BotClientUI from '@glodon-aiot/bot-client-ui';
const bot = new BotClientUI({ container: el, botId: 'xxx', token: 'xxx' });
```

新代码:
```javascript
import { ChatApp } from '@glodon-aiot/chat-app-sdk';
const chat = new ChatApp({ appId: 'xxx', container: el });
```

**3. 更新配置**
- 在 Coze Studio 创建/迁移应用
- 获取新的 `appId`

**4. 测试验证**

---

## 🔧 常见问题

**Q: 旧项目必须迁移吗？**  
A: 不是必须，但建议：运行稳定可继续用，需新功能必须迁移。

**Q: 迁移成本高吗？**  
A: 较低，API 设计相似，1-2 小时可完成基础迁移。

**Q: botId 和 appId 有什么区别？**  
A: botId 指向单个 Bot 实例，appId 指向 Coze Studio 应用（可包含多个 Bot/工作流）。

---

## 📚 相关文档

- [Coze Studio 新版 SDK](chat_app_sdk.md) - **推荐使用**
- [应用对接历史文档](https://glodon-cv-help.yuque.com/cuv0se/ol9231/app-integration-legacy)
- [NPM 包页面](https://www.npmjs.com/package/@glodon-aiot/bot-client-ui)

---

_本文档由 glodon-ai-help 技能自动生成，最后更新：2026-03-20 18:03_

**⚠️ 提醒**: 新项目请使用 **Coze Studio** (`@glodon-aiot/chat-app-sdk`)
