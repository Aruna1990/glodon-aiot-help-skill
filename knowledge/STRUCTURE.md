# 知识库目录结构说明

> 最后整理时间：2026-03-20

---

## 📁 目录结构

```
knowledge/
├── INDEX.md                    # 主索引（所有文档链接汇总）
├── docs_index.json             # JSON 格式索引
├── README.md                   # 使用说明
│
├── 01-platform-intro/          # 平台介绍
│   ├── platform_intro.md       # 平台介绍
│   └── changelog.md            # 平台更新记录
│
├── 02-api-reference/           # API 参考（29 个接口）
│   ├── auth.md                 # 认证相关
│   ├── vision.md               # 视觉 API（OCR、检测等）
│   ├── nlp.md                  # NLP API（LLM、Embedding 等）
│   └── data.md                 # 数据 API（AecDataIO）
│
├── 03-coze-studio/             # Coze Studio
│   ├── introduction.md         # Coze Studio 介绍
│   ├── api.md                  # Coze API 调用
│   └── sdk/                    # SDK 文档
│       ├── chat_app_sdk.md     # 新版前端 SDK（推荐）
│       └── bot_client_ui.md    # 旧版 SDK（已废弃）
│
├── 04-knowledge-base/          # 知识库（RAG）
│   ├── rag.md                  # RAG 检索
│   ├── data-management.md      # 数据管理
│   └── knowledge-enhancement.md # 知识增强
│
├── 05-models/                  # 模型服务
│   ├── models.md               # 行业 AI 模型
│   └── fine-tuning.md          # 模型精调
│
├── 06-prompt-engineering/      # Prompt 工程
│   ├── templates.md            # Prompt 模板
│   └── examples.md             # 示例库
│
├── 07-evaluation/              # 评估中心
│   ├── statistics.md           # 调用统计
│   ├── llm-eval.md             # LLM 评估
│   └── rag-eval.md             # 知识检索评估
│
├── 08-integration/             # 应用集成
│   ├── app-integration.md      # 应用对接
│   └── plugins.md              # 插件管理
│
└── 09-faq/                     # 常见问题
    ├── faq.json                # FAQ 数据
    ├── platform-faq.md         # 平台使用常见问题
    └── complaints.md           # 投诉举报处理
```

---

## 📊 文档统计

| 分类 | 文档数 | 说明 |
|------|--------|------|
| 01-platform-intro | 2 | L0 概述文档 |
| 02-api-reference | 29 | L1-L2 接口文档 |
| 03-coze-studio | 5 | Coze Studio + 工作流 |
| 04-knowledge-base | 4 | RAG 相关 |
| 05-models | 3 | 模型训练/部署 |
| 06-prompt-engineering | 3 | 模板与示例 |
| 07-evaluation | 4 | 效果评估 |
| 08-integration | 7 | 插件与对接 + 解决方案 |
| 09-faq | 2 | FAQ |
| **总计** | **59** | - |

---

## 🔗 语雀知识库

- **主库**: https://glodon-cv-help.yuque.com/cuv0se/ol9231
- **同步方式**: `python3 create_index.py`（生成索引，无需 Token）
- **完整同步**: `python3 learn_yuque.py`（需要 Cookie）

---

## 📝 整理原则

1. **核心文档放根目录** - INDEX.md、README.md、docs_index.json
2. **按平台模块分类** - 对应 4 层 11 模块架构
3. **SDK 独立管理** - 新旧版本 SDK 放在 `03-coze-studio/sdk/`
4. **FAQ 集中管理** - 所有常见问题汇总到 `09-faq/`
5. **原始文档归档** - 语雀原始文档（ID 命名）可放在 `original/` 子目录

---

## 🔄 维护说明

- 新增文档后运行 `python3 create_index.py` 更新索引
- 定期清理临时文件（`.json`, `.swp`, `learn_state.json` 等）
- SDK 文档更新后同步到 `03-coze-studio/sdk/`
