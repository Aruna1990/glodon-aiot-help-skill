---
name: glodon-ai-help
description: 广联达行业 AI 平台使用问题解答。平台问题必须完全依照语雀文档；@glodon-aiot npm 包必须使用 npm 网站 README 内容。禁止添加文档外的任何内容。
---

# 广联达行业 AI 平台帮助技能

> **版本**: 1.4.2 | **平台**: 完全依语雀 | **npm**: 仅用 README 内容 | **禁止**: 添加文档外内容

---

## 🏗️ 平台模块架构

### 4 层 11 模块架构

```
用户接入层 → 应用开发层 → 核心能力层 → 基础支撑层
```

| 层级           | 模块                                                 | 说明           |
| -------------- | ---------------------------------------------------- | -------------- |
| **用户接入层** | 网页控制台、移动端 APP、API/SDK                      | 用户访问入口   |
| **应用开发层** | Coze Studio、工作流、应用集成、Prompt 工程、解决方案 | 应用开发与编排 |
| **核心能力层** | 模型服务、知识库、评估中心                           | AI 核心能力    |
| **基础支撑层** | API 参考 (29 个接口)、认证授权                       | 基础接口与安全 |

### 模块关系

- **Coze Studio** → 依赖 Prompt 工程、知识库、模型服务 → 快速搭建 AI 助手
- **工作流** → 依赖 API 参考、模型服务 → 流程自动化
- **知识库 (RAG)** → 依赖 Embedding API、数据管理 → 文档智能问答
- **评估中心** → 监控知识库、模型服务效果 → 持续优化

📚 详见：[PLATFORM_ARCHITECTURE.md](knowledge/PLATFORM_ARCHITECTURE.md)

---

## 📌 前端 SDK 版本说明

### 新旧版本对比

| SDK      | 包名                         | 状态      | 说明                                     |
| -------- | ---------------------------- | --------- | ---------------------------------------- |
| **新版** | `@glodon-aiot/chat-app-sdk`  | ✅ 推荐   | Coze Studio 前端 SDK，功能完整，活跃维护 |
| **旧版** | `@glodon-aiot/bot-client-ui` | ⚠️ 已废弃 | 应用对接模块旧 SDK，已停止更新           |

### 如何选择

- **新项目** → 使用 **Coze Studio** (`@glodon-aiot/chat-app-sdk`)
- **旧项目维护** → 可继续使用 `bot-client-ui`，但建议规划迁移
- **需要新功能**（文件上传、语音、主题定制）→ 必须迁移到 Coze Studio

📚 详细文档:

- [Coze Studio SDK 文档](knowledge/chat_app_sdk.md)
- [旧版 SDK 迁移指南](knowledge/bot_client_ui.md)

---

## 🎯 功能特性

### 0. 回答规则 ⭐⭐⭐（最重要！）

**涉及技术细节时必须先查文档，禁止凭记忆回答！**

#### 严格约束（必须遵守）

| 问题类型 | 回答依据 | 禁止行为 |
|----------|----------|----------|
| **广联达行业 AI 平台使用问题** | **完全依照语雀文档**回答 | ❌ 不得添加文档中没有的内容 |
| **@glodon-aiot npm 包** | **仅使用 NPM 网站上的 README / 文档内容**回答 | ❌ 不得添加文档中没有的内容 |

**核心原则**：只回答文档中已有的内容，不得推测或补充文档外信息。

#### 文档来源对照表

| 问题类型                                           | 数据来源   | 查阅方式                                                   |
| -------------------------------------------------- | ---------- | ---------------------------------------------------------- |
| **平台功能介绍**、架构、模块、API 接口、Token 认证 | 语雀知识库 | 读取 `knowledge/` 下对应的说明文件                         |
| **@glodon-aiot npm 包**（安装、配置、API、用法）   | NPM 网站   | **必须读取** https://www.npmjs.com/package/包名 的 README/文档内容 |

#### 查阅文档对照

| 场景                                                      | 必须查阅的文档                                                                |
| --------------------------------------------------------- | ----------------------------------------------------------------------------- |
| API 接口 URL、参数                                        | `knowledge/QUICK_REFERENCE.md`（首选）或 `AI_APP_INTEGRATION_GUIDE.md`        |
| Token 认证流程                                            | `knowledge/QUICK_REFERENCE.md` → 认证接口章节                                 |
| 平台功能介绍、架构、模块                                  | 语雀文档 → `knowledge/` 对应目录                                              |
| **@glodon-aiot npm 包**（如 chat-app-sdk、bot-client-ui） | **读取 NPM 网站** → `https://www.npmjs.com/package/@glodon-aiot/包名`         |
| 前端 SDK（代码/配置/API 细节）                            | 访问并读取 NPM 包页上的 README/MD 内容                                        |
| 平台架构/模块                                             | `knowledge/PLATFORM_ARCHITECTURE.md`                                          |
| 常见问题                                                  | `knowledge/faq.json` 或 `lpetkzefs5er4q5x.md`                                 |

**@glodon-aiot 包 NPM 地址：**

- 新版 SDK：https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk
- 旧版 SDK：https://www.npmjs.com/package/@glodon-aiot/bot-client-ui

**禁止行为：**

- ❌ 凭记忆回答 API URL、参数名、Token 流程等技术细节
- ❌ 猜测、推测或添加文档/README 中没有的信息
- ❌ 使用过时的文档（如旧版 SDK）
- ❌ **回答 @glodon-aiot npm 包问题时未读取 NPM 网站文档**
- ❌ **平台问题添加语雀文档以外内容** | **npm 问题添加 NPM 文档以外内容**

**文档路径更新（2026-03-20）：**

- `knowledge/QUICK_REFERENCE.md` → `knowledge/02-api-reference/` 或根目录
- `knowledge/chat_app_sdk.md` → `knowledge/03-coze-studio/sdk/chat_app_sdk.md`
- `knowledge/bot_client_ui.md` → `knowledge/03-coze-studio/sdk/bot_client_ui.md`
- `knowledge/PLATFORM_ARCHITECTURE.md` → 根目录或 `knowledge/core/`
- `knowledge/faq.json` → `knowledge/09-faq/faq.json`

### 1. 智能问答 ⭐

- 基于 FAQ 库提供详细答案
- 自动匹配相关文档链接
- 支持关键词和语义匹配
- 格式化输出（Markdown）

### 2. 平台入门指导 🚀

- **进入平台的方法**（网页/移动端/API）
- 首次使用准备（账号/API Key/白名单）
- 新手常见问题解答
- 快速上手指南

### 3. 自动学习 📚

- 检测知识盲区自动触发学习
- 从语雀知识库下载文档内容
- **下钻阅读关联链接**（递归学习）
- 本地知识库自动更新
- 学习状态持久化

### 4. 技术问题解答

- API 调用问题
- 模型部署问题
- 数据接入问题
- 性能优化建议

### 5. 故障排查

- 常见问题诊断
- 错误码解释
- 解决方案提供
- 升级工单指引

### 6. 文档检索

- 快速查找文档
- 相关文档推荐
- 版本差异说明

---

## 📁 文件结构

```
glodon-ai-help/
├── SKILL.md                    # 技能说明（本文件）
├── config.yaml                 # 技能配置
├── knowledge/                  # 知识库（目录结构，文档按需生成）
│   ├── 01-platform-intro/      # 平台介绍
│   ├── 02-api-reference/       # API 参考
│   ├── 03-coze-studio/         # Coze Studio
│   │   └── sdk/                # SDK 文档（由 learn_chat_app_sdk.py 生成）
│   ├── 04-knowledge-base/      # 知识库 RAG
│   ├── 05-models/              # 模型服务
│   ├── 06-prompt-engineering/  # Prompt 工程
│   ├── 07-evaluation/          # 评估中心
│   ├── 08-integration/         # 应用集成
│   └── 09-faq/                 # 常见问题
│
├── scripts/                    # 学习脚本
│   ├── create_index.py         # 生成索引（无需 Token）⭐
│   ├── learn_public_docs.py    # 学习公开文档（无需认证）
│   ├── learn_simple.py         # 简单学习（curl 获取）
│   ├── learn_chat_app_sdk.py   # SDK 文档同步（NPM）
│   ├── learn_bot_client_ui.py  # 旧版 SDK 同步（NPM）
│   ├── demo_learn.py           # 演示学习（离线）
│   ├── batch_learn.sh          # 批量学习
│   ├── quick_learn.py          # 快速学习
│   └── test_new_features.py    # 测试脚本
│
├── intents.json                # 意图识别配置
└── embeddings/                 # 文档向量索引（待生成）
```

**注意**: `knowledge/` 目录初始为空，运行脚本后自动生成文档：
- `create_index.py` → 生成 `INDEX.md`, `docs_index.json`, `README.md`
- `learn_public_docs.py` / `batch_learn.sh` → 下载语雀公开文档
- `learn_chat_app_sdk.py` → 生成 SDK 集成文档

📚 **文档索引**: 运行 `python3 scripts/create_index.py` 生成索引
📋 **结构说明**: 目录结构对应平台 4 层 11 模块架构

---

## 💬 对话示例

### 🚀 平台入门（新增）

```
用户：怎么进入行业 AI 平台？
客服：🚀 **进入广联达行业 AI 平台指南**

      **步骤 1**: 访问 https://copilot.glodon.com/
      **步骤 2**: 使用广联达账号登录
      **步骤 3**: 选择租户
      **步骤 4**: 进入产品中心
      **步骤 5**: 点击"行业 AI 平台"卡片

      ## 首次使用准备
      1. 账号准备（广联达账号 + 实名认证）
      2. 获取 API Key（开发者）
      3. 配置 IP 白名单（可选）

      📚 相关文档:
      1. [平台介绍](https://glodon-cv-help.yuque.com/cuv0se/ol9231/yck25gn683z3wa2f)
      2. [平台使用常见问题汇总](...)
```

### 智能问答

```
用户：广联达行业 AI 平台是什么？
客服：广联达行业 AI 平台是面向建筑行业的 AI 能力开放平台，提供：
      • 视觉识别能力（安全帽检测、烟火识别等）
      • NLP 处理能力
      • 模型训练和部署服务
      • API 调用和集成支持

      您想了解哪个方面的功能？
```

### API 调用

```
用户：怎么调用 API？
客服：调用 API 步骤：
      1. 登录平台获取 API Key
      2. 查看 API 文档了解接口参数
      3. 使用 HTTP POST 请求调用
      4. 处理返回结果

      需要我提供具体接口的调用示例吗？
```

### 自动学习（新增）

```
用户：这个功能我没有找到相关文档
客服：抱歉，我暂时没有找到相关信息。

      📚 **建议操作**：
      1. 我可以帮您从语雀知识库学习相关文档
      2. 查看 [平台使用常见问题汇总](...)
      3. 联系技术支持

      💡 **提示**: 说"去学习"可以让我更新知识库

[系统自动触发学习，下载相关文档并下钻关联链接]
```

### 故障排查

```
用户：API 返回 401 错误
客服：401 错误表示认证失败，可能原因：
      1. API Key 无效或已过期
      2. 请求头格式不正确
      3. IP 白名单未配置

      请检查：
      • API Key 是否正确复制
      • Authorization 头格式：Bearer <your_key>
      • 是否在控制台配置了 IP 白名单
```

---

## 🔧 配置说明

### 知识库来源（双源）

| 用途                    | 来源       | 说明                                                                      |
| ----------------------- | ---------- | ------------------------------------------------------------------------- |
| **平台功能介绍**        | 语雀知识库 | URL: https://glodon-cv-help.yuque.com/cuv0se/ol9231 → 公开文档，无需认证 |
| **@glodon-aiot npm 包** | NPM 网站   | 回答时**动态读取** https://www.npmjs.com/package/@glodon-aiot/包名        |

语雀文档更新：使用 `learn_public_docs.py` 或 `batch_learn.sh` 同步公开文档
NPM 包文档：实时获取，保证版本、API 等信息最新

### 文档同步

#### 方式 1：生成索引（推荐）⭐

```bash
python3 scripts/create_index.py
```

**无需 Cookie，无需 Token**，5 秒钟生成 59 篇文档的完整索引，点击链接直接查看。

#### 方式 2：学习公开文档

```bash
# 学习核心文档
python3 scripts/learn_public_docs.py

# 或快速学习
python3 scripts/learn_simple.py

# 批量学习
bash scripts/batch_learn.sh
```

使用 `curl` 直接获取语雀公开文档内容，**无需认证**。

#### 方式 3：同步 SDK 文档（NPM）

```bash
# 新版 SDK
python3 scripts/learn_chat_app_sdk.py

# 旧版 SDK
python3 scripts/learn_bot_client_ui.py
```

从 NPM Registry 实时获取 SDK 文档，**无需语雀认证**。

#### 方式 4：演示学习（离线）

```bash
python3 scripts/demo_learn.py
```

模拟学习流程，无需网络。

### 自动学习配置

在 `config.yaml` 中配置：

```yaml
learning:
  enabled: true
  auto_trigger: true # 检测知识盲区时自动学习
  max_depth: 2 # 关联链接下钻深度
  rate_limit: 0.5 # 请求间隔（秒）
```

### 向量检索

使用嵌入模型将文档向量化，支持语义检索：

```yaml
embedding:
  model: text-embedding-ada-002
  chunk_size: 500
  chunk_overlap: 50
```

---

## 🎨 意图识别

| 意图           | 触发词             | 处理逻辑      |
| -------------- | ------------------ | ------------- |
| platform_intro | 是什么、介绍、概述 | 返回平台介绍  |
| how_to         | 怎么、如何、步骤   | 返回操作指南  |
| api_help       | API、接口、调用    | 返回 API 文档 |
| error_help     | 错误、报错、失败   | 返回故障排查  |
| doc_search     | 文档、哪里看、资料 | 检索相关文档  |

---

## 🔌 集成方式

### Webhook

```yaml
webhook:
  endpoint: /api/webchat
  allowed_origins:
    - https://copilot.glodon.com
    - https://glodon-cv-help.yuque.com
```

### API 调用

```python
from skills.glodon_ai_help import AIBot

bot = AIBot()
response = bot.answer("怎么调用 API？")
print(response)
```

---

## 📊 知识库结构

### 平台介绍 (L0)

- 平台概述
- 核心能力
- 应用场景
- 计费说明
- 平台更新记录

### 快速入门 (L0-L1)

- 注册登录
- 获取 API Key
- Token 认证 (API Access Token / Resource Token)
- 首次使用准备

### 应用开发 (L1-L2)

- **Coze Studio**: 低代码 AI 应用开发
  - 前端 SDK: `@glodon-aiot/chat-app-sdk` (NPM)
  - 一键嵌入聊天界面到你的产品
  - 支持自定义主题、消息历史、文件上传、流式响应
- **工作流**: 流程编排引擎
- **应用集成**: 插件管理、API 对接
- **Prompt 工程**: 模板库、样例库
- **解决方案**: AI 助手构建、AI 评标

### 核心能力 (L1)

- **模型服务**: 预训练模型、自定义训练、模型部署
- **知识库**: RAG 检索、数据管理、知识增强
- **评估中心**: 调用统计、LLM 评估、知识检索评估

### API 参考 (L1-L2, 29 个接口)

- **认证**: Token 获取、Key Secret 认证
- **视觉**: OCR(10+)、物体检测、图像分类、CAD 转换
- **NLP**: 大模型 (LLM)、Embedding、Rerank
- **文档处理**: 表格识别、公式识别、水印/印章去除
- **数据**: AecDataIO 系列

### 故障排查 (L0)

- 平台使用常见问题汇总
- 错误码详解
- 解决方案
- 联系支持

### 文档索引

- **总文档数**: 59 篇（语雀公开文档）+ 外部文档（NPM SDK）
- **分类目录**: 11 个
- **文档生成**: 运行脚本后自动生成到 `knowledge/` 目录
  - `python3 scripts/create_index.py` → 生成索引文件
  - `bash scripts/batch_learn.sh` → 下载核心文档
  - `python3 scripts/learn_chat_app_sdk.py` → 生成 SDK 文档
- **外部学习源**:
  - 语雀知识库：https://glodon-cv-help.yuque.com/cuv0se/ol9231
  - NPM SDK：https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk

---

## ⚙️ 环境变量

```bash
# 平台配置（可选）
AI_PLATFORM_URL=https://copilot.glodon.com
```

**注意**：本技能仅访问语雀公开文档和 NPM 公开包，**无需任何 Token 或认证**。

---

## 🔄 更新日志

- **v1.5.1** (2026-03-23): 清空知识库 - 按需生成 🧹
  - **删除** `knowledge/` 目录下所有脚本生成的文件（124 个）
  - **保留** 11 个分类目录结构
  - 更新 SKILL.md 文件结构说明
  - 文档现在按需运行脚本生成

- **v1.5.0** (2026-03-23): 简化认证 - 仅使用公开文档 🎯
  - **删除** `learn_yuque.py`（需要 Cookie）
  - **删除** `learn_docs.py`（需要 Token）
  - **删除** `sync_yuque.py`（需要 Token）
  - **删除** `sync_all_docs.py`（需要 Token）
  - **保留** `learn_public_docs.py`、`learn_simple.py`、`batch_learn.sh`（无需认证）
  - 更新 SKILL.md 文档同步说明
  - 移除环境变量中的 Token 配置
  - 技能现在仅访问语雀公开文档和 NPM 公开包

- **v1.4.2** (2026-03-23): 严格约束 - 禁止添加文档外内容 ⭐
  - **平台使用问题** → 必须完全依照语雀文档，不得添加文档中没有的内容
  - **@glodon-aiot npm 包** → 必须使用 NPM 网站 README/MD 内容，不得添加文档中没有的内容
  - 新增「严格约束」表与核心原则

- **v1.4.1** (2026-03-23): 明确双源回答规则
  - **平台功能介绍** → 依据语雀文档（`knowledge/` 对应说明文件）
  - **@glodon-aiot npm 包** → 必须读取 NPM 网站介绍文档回答

- **v1.4.0** (2026-03-20): 新增新旧版 SDK 对比说明 🚀
  - 新增 **learn_bot_client_ui.py** 学习脚本（旧版 SDK）
  - 生成 `knowledge/bot_client_ui.md` 旧版 SDK 文档
  - 添加前端 SDK 版本对比表（新旧版本选择指南）
  - 配置自动触发：识别旧版 SDK 关键词自动学习
  - 提供迁移指南（bot-client-ui → chat-app-sdk）

- **v1.3.2** (2026-03-20): 新增 Coze Studio SDK 自动学习 🚀
  - 新增 **learn_chat_app_sdk.py** 学习脚本
  - 支持自动从 NPM Registry 获取 SDK 信息
  - 生成完整的 SDK 集成文档（安装/配置/API/事件）
  - 配置自动触发：当用户询问前端集成时自动学习
  - 生成文档路径：`knowledge/chat_app_sdk.md`

- **v1.3.1** (2026-03-20): 补充 Coze Studio 前端 SDK 信息
  - 新增 **@glodon-aiot/chat-app-sdk** NPM 包说明
  - 添加前端嵌入集成方式

- **v1.3.0** (2026-03-20): 平台模块架构总结 ⭐
  - 新增 **PLATFORM_ARCHITECTURE.md** 模块架构与关系图
  - 总结 **4 层 11 模块** 架构（用户接入/应用开发/核心能力/基础支撑）
  - 绘制模块依赖关系图和使用流程
  - 更新知识库结构说明（59 篇文档，11 个分类）
  - 添加模块选择建议表

- **v1.2.0** (2026-03-20): 自动学习 + 平台入门指南 ⭐
  - 新增 `learn_docs.py` 深度学习脚本
  - 支持**下钻阅读关联链接**（递归学习）
  - 新增平台入门指南（进入方法/首次使用准备）
  - 检测知识盲区自动触发学习
  - 学习状态持久化

- **v1.1.0** (2026-03-19): 智能问答机器人上线 ⭐
  - 支持 FAQ 自动匹配
  - 自动提供文档链接
  - 格式化输出回答

- **v1.0.0** (2026-03-19): 同步语雀文档 59 篇 ✅

---

## 📞 支持

文档问题联系：行业 AI 平台产品团队
技术问题联系：技术支持工单系统

---

## ⚠️ 常见错误与教训

### 错误案例 1：Token 接口 URL 错误（2026-03-20）

**问题**：用户问 Token 接口 URL，AI 回答了 `https://api.glodon.com/ai-platform/v1/token`，但正确的是 `https://copilot.glodon.com/api/cvforce/auth/v1/token`

**原因**：

- AI 没有先查 `AI_APP_INTEGRATION_GUIDE.md` 或 `QUICK_REFERENCE.md`
- 凭记忆/猜测回答了 URL
- 环境变量示例 `AI_PLATFORM_URL=https://ai.glodon.com` 是示例配置，不是 API 基准 URL

**正确做法**：

1. 识别关键词：`token`、`API`、`认证`、`URL`、`接口`
2. 立即读取 `knowledge/QUICK_REFERENCE.md` → 认证接口章节
3. 复制准确的 URL 和参数

**已修复**：

- ✅ 创建 `QUICK_REFERENCE.md` 汇总所有核心 API 和 URL
- ✅ 在 SKILL.md 中添加"回答规则"章节
- ✅ 明确禁止凭记忆回答技术细节

---

### 错误案例 2：参数名大小写错误

**问题**：使用 `api_key` 而不是 `apiKey`

**正确**：

```json
{
  "apiKey": "xxx",
  "apiSecret": "xxx"
}
```

**记忆技巧**：JavaScript/JSON 使用驼峰命名（camelCase）
