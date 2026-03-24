---
name: glodon-ai-help
description: 广联达行业 AI 平台使用问题解答。平台问题必须完全依照语雀文档；@glodon-aiot npm 包必须使用 npm 网站 README 内容。禁止添加文档外的任何内容。
metadata:
  {
    "openclaw":
      {
        "emoji": "🏗️",
        "homepage": "https://glodon-cv-help.yuque.com/cuv0se/ol9231",
        "requires": { "bins": ["python3"] },
      },
  }
allowed-tools: read exec web_fetch
---

# 广联达行业 AI 平台帮助技能

> **版本**: 1.7.0 | **知识策略**: 按需学习 | **三源回答**: 行业 AI 平台 + AIoT 平台 + NPM

---

## ⭐ 核心原则（必须遵守）

### 回答规则

| 问题类型 | 数据来源 | 查阅方式 |
|----------|----------|----------|
| **平台功能/架构/API/Token** | 行业 AI 平台语雀知识库 | 读取 `knowledge/` 下对应文档 |
| **身份认证/Token 获取（通用）** | AIoT 平台对接文档 | 读取 `knowledge/02-aiot-platform/` 下文档 |
| **@glodon-aiot npm 包** | NPM 网站 README | 访问 https://www.npmjs.com/package/@glodon-aiot/包名 |

**严格约束**：
- ❌ 不得添加语雀文档中没有的平台功能说明
- ❌ 不得添加 NPM README 中没有的包 API/用法
- ❌ 不得凭记忆回答技术细节（URL、参数名、Token 流程等）
- ✅ **身份认证、Token 获取等问题优先参考 AIoT 平台对接文档**

### 知识策略：按需学习 🧠

```
┌─────────────────────────────────────────────────────────┐
│  用户提问 → 检查 knowledge/ 是否有相关文档？              │
│       ↓                                                  │
│   有 → 直接读取文档回答                                   │
│       ↓                                                  │
│   无 → 启动学习脚本 → 保存到 knowledge/ → 回答            │
└─────────────────────────────────────────────────────────┘
```

**何时学习**：
1. **首次使用**：knowledge/ 目录为空时
2. **知识缺失**：用户问题涉及的主题没有对应文档
3. **主动更新**：用户说"去学习"或"更新知识库"

**学习什么**：
- 语雀公开文档 → 根据语雀实际目录结构自动创建
- NPM SDK 文档 → `knowledge/03-coze-studio/sdk/`

---

## 📁 文件结构

```
glodon-ai-help/
├── SKILL.md                    # 技能说明（本文件）
├── config.yaml                 # 技能配置
│
├── knowledge/                  # 知识库（技能自己的数据，已 git ignore）⭐
│   ├── README.md               # 知识库说明
│   ├── .learn_state.json       # 学习状态
│   ├── 02-aiot-platform/       # AIoT 平台对接文档
│   │   ├── README.md           # 文档索引
│   │   └── <slug>.md
│   ├── <slug>.md               # 行业 AI 平台文档（按实际结构创建）
│   └── 03-coze-studio/sdk/     # SDK 文档（固定结构）
│
├── scripts/                    # 学习脚本
│   ├── check_and_learn.py      # 统一入口：检查 + 按需学习 ⭐
│   ├── config.py               # 统一配置管理
│   ├── utils.py                # 通用工具函数
│   ├── learn_public_docs.py    # 行业 AI 平台公开文档
│   ├── learn_aiot_docs.py      # AIoT 平台对接文档
│   ├── learn_chat_app_sdk.py   # NPM SDK 文档
│   └── learn_bot_client_ui.py  # 旧版 SDK 文档
│
├── .gitignore                  # Git 忽略配置（忽略 knowledge/）
└── intents.json                # 意图识别
```

**注意**：
- `knowledge/` 是技能自己的数据，位于技能目录内
- `.gitignore` 已配置忽略 `knowledge/`，不会提交到 Git 仓库
- 运行 `check_and_learn.py` 后自动生成文档
- 语雀文档目录**根据实际文档结构自动创建**，不预设固定分类

---

## 🚀 快速开始

### 方式 1：自动触发（推荐）

当用户提问时，技能会自动检查知识库：

```
用户：怎么调用 Token 接口？
→ 检查 knowledge/ 是否有认证相关文档
→ 无 → 自动运行 learn_public_docs.py
→ 有 → 读取文档回答
```

### 方式 2：手动学习

```bash
# 检查并学习（统一入口）
python3 scripts/check_and_learn.py

# 学习语雀核心文档
python3 scripts/learn_public_docs.py

# 学习 SDK 文档（NPM）
python3 scripts/learn_chat_app_sdk.py
```

### 方式 3：查看状态

```bash
python3 scripts/check_and_learn.py --state
```

---

## 📌 文档来源

### 行业 AI 平台（语雀）

- **URL**: https://glodon-cv-help.yuque.com/cuv0se/ol9231
- **认证**: 公开文档，无需 Token
- **学习脚本**: `learn_public_docs.py`
- **目录结构**: 根据语雀实际文档结构自动创建

### AIoT 平台对接（语雀）⭐

- **URL**: https://glodon-cv-help.yuque.com/lzh2bp/gwam63
- **Book ID**: `29345082`
- **认证**: **部分公开，部分需要登录**
- **学习脚本**: `learn_aiot_docs.py`
- **核心文档**:
  - ✅ [Glodon AIoT 产品系统 API 接入文档](https://glodon-cv-help.yuque.com/lzh2bp/gwam63/tt25tc) - 已缓存
  - 🔒 [身份认证](https://glodon-cv-help.yuque.com/lzh2bp/gwam63/kqg83f) - 需登录
  - 🔒 [获取 Access Token](https://glodon-cv-help.yuque.com/lzh2bp/gwam63/pzx9r2) - 需登录
  - 🔒 [API 调用规范](https://glodon-cv-help.yuque.com/lzh2bp/gwam63/m7h4n1) - 需登录
- **索引文件**: `knowledge/02-aiot-platform/README.md`
- **本地缓存**: `knowledge/02-aiot-platform/tt25tc.md`

**使用场景**：身份认证、Token 获取、API 调用规范等通用问题优先参考 AIoT 平台对接文档。

**关键信息**（来自 `tt25tc`）:
- **API Access Token 接口**: `POST https://copilot.glodon.com/api/auth/v1/access-token`
- **有效期**: 7 天（剩余 12 小时内刷新可获取新 Token）
- **鉴权方式**: API Key + API Secret + MD5 签名

### NPM 包

| 包名 | 用途 | NPM 地址 |
|------|------|----------|
| `@glodon-aiot/chat-app-sdk` | Coze Studio 前端 SDK（新版） | https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk |
| `@glodon-aiot/bot-client-ui` | 旧版 SDK（已废弃） | https://www.npmjs.com/package/@glodon-aiot/bot-client-ui |

- **认证**: 公开包，无需 Token
- **学习脚本**: `learn_chat_app_sdk.py`

---

## 💬 对话示例

### 平台入门

```
用户：怎么进入行业 AI 平台？
客服：🚀 **进入广联达行业 AI 平台指南**

      **步骤 1**: 访问 https://copilot.glodon.com/
      **步骤 2**: 使用广联达账号登录
      **步骤 3**: 选择租户
      **步骤 4**: 进入产品中心
      **步骤 5**: 点击"行业 AI 平台"卡片

      📚 来源：knowledge/<slug>/平台介绍.md
```

### API 调用

```
用户：Token 接口 URL 是什么？
客服：Token 接口信息：

      **URL**: `https://copilot.glodon.com/api/cvforce/auth/v1/token`
      **方法**: POST
      **参数**: 
      ```json
      {
        "apiKey": "your-api-key",
        "apiSecret": "your-api-secret"
      }
      ```

      📚 来源：knowledge/<slug>/平台认证 Token 说明文档.md
```

### SDK 使用

```
用户：@glodon-aiot/chat-app-sdk 怎么用？
客服：📦 **Coze Studio 前端 SDK 使用指南**

      **安装**:
      ```bash
      npm install @glodon-aiot/chat-app-sdk
      ```

      **基础用法**:
      ```typescript
      import { WebChatClient } from '@glodon-aiot/chat-app-sdk';
      
      const client = new WebChatClient({
        mode: 'float',
        config: { type: 'app', appInfo: { appId: '...', workflowId: '...' } },
        auth: { type: 'token', token: 'your-token' },
      });
      
      client.showChatBot();
      ```

      📚 来源：https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk
```

### 自动学习

```
用户：这个功能我没有找到相关文档
客服：抱歉，我暂时没有找到相关信息。

      📚 **正在学习相关文档...**
      [系统自动运行学习脚本]
      
      ✅ 已学习 3 篇文档，现在可以回答相关问题了。
```

---

## 🔧 配置说明

### 自动学习配置（config.yaml）

```yaml
learning:
  enabled: true
  auto_trigger: true          # 检测知识缺失时自动学习
  check_on_startup: true      # 启动时检查知识库
  state_file: knowledge/.learn_state.json
  scripts:
    check_and_learn: scripts/check_and_learn.py   # 统一入口
    public_docs: scripts/learn_public_docs.py     # 语雀文档
    chat_app_sdk: scripts/learn_chat_app_sdk.py   # 新版 SDK
    bot_client_ui: scripts/learn_bot_client_ui.py # 旧版 SDK
```

### 知识库状态文件

`knowledge/.learn_state.json` 记录学习状态：

```json
{
  "last_sync": "2026-03-23T15:00:00",
  "learned_docs": ["yck25gn683z3wa2f", "lpetkzefs5er4q5x"],
  "sdk_versions": {
    "chat-app-sdk": "1.2.3"
  },
  "categories": ["平台介绍", "API 参考"]
}
```

---

## ⚠️ 常见错误与教训

### 错误 1：Token 接口 URL 错误

**问题**：回答了 `https://api.glodon.com/ai-platform/v1/token`（错误）

**正确**：`https://copilot.glodon.com/api/cvforce/auth/v1/token`

**解决**：必须先查 `knowledge/` 下的认证文档

### 错误 2：参数名大小写错误

**问题**：使用 `api_key`（错误）

**正确**：`apiKey`（驼峰命名）

### 错误 3：凭记忆回答技术细节

**原则**：涉及 URL、参数、Token 流程等，必须先查文档！

---

## 🔄 更新日志

- **v1.6.1** (2026-03-23): 移除预设目录结构 🧹
  - 删除 knowledge/ 下预设的 11 个分类目录
  - 修改 `learn_public_docs.py` 根据语雀实际文档结构自动创建目录
  - 简化知识库结构说明

- **v1.6.0** (2026-03-23): 按需学习机制 🧠
  - 新增 `check_and_learn.py` 统一入口
  - 实现知识缺失自动检测 + 学习

- **v1.5.1** (2026-03-23): 清空知识库 🧹

- **v1.5.0** (2026-03-23): 简化认证 🎯
  - 仅使用公开文档（无需 Token）

- **v1.4.2** (2026-03-23): 严格约束 ⭐
  - 禁止添加文档外内容

---

## 📞 支持

- 文档问题：行业 AI 平台产品团队
- 技术问题：技术支持工单系统
