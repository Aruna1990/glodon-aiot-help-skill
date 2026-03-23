# 自动学习功能使用指南

## 📚 功能概述

`learn_docs.py` 是广联达行业 AI 平台的**深度学习脚本**，能够：

1. **自动下载文档内容** - 从语雀 API 获取完整文档
2. **下钻关联链接** - 递归阅读文档中引用的其他文档
3. **本地知识库更新** - 将学习内容保存到 `knowledge/` 目录
4. **状态持久化** - 记录学习历史，避免重复学习

---

## 🚀 快速开始

### 1. 配置语雀 Token

```bash
# 获取 Token: https://www.yuque.com/settings/tokens
export YUQUE_TOKEN='your_yuque_token'
```

### 2. 基础使用

```bash
# 学习核心文档（推荐首次使用）
python3 scripts/learn_docs.py

# 学习指定文档
python3 scripts/learn_docs.py --slugs yck25gn683z3wa2f lpetkzefs5er4q5x

# 学习知识库所有文档
python3 scripts/learn_docs.py --all

# 查看学习状态
python3 scripts/learn_docs.py --state
```

### 3. 高级选项

```bash
# 指定下钻深度（默认 2，最大 5）
python3 scripts/learn_docs.py --all --depth 3

# 组合使用
python3 scripts/learn_docs.py --slugs yck25gn683z3wa2f --depth 1
```

---

## 📖 工作原理

### 学习流程

```
1. 从初始文档列表开始
   ↓
2. 调用语雀 API 获取文档内容
   ↓
3. 解析文档中的 Markdown 链接
   ↓
4. 提取语雀知识库内的关联链接
   ↓
5. 将关联文档加入学习队列
   ↓
6. 递归学习（达到最大深度停止）
   ↓
7. 保存到本地 knowledge/ 目录
   ↓
8. 更新学习状态文件
```

### 下钻示例

假设学习"平台介绍"文档：

```
平台介绍 (深度 0)
├── 行业 AI 模型 (深度 1) ← 文档内链接
│   └── 模型精调 (深度 2) ← 关联链接
└── API 调用 (深度 1) ← 文档内链接
    └── Token 说明 (深度 2) ← 关联链接
```

---

## 📁 输出文件

### 学习状态文件
`knowledge/.learn_state.json`
```json
{
  "last_sync": "2026-03-20T10:30:00",
  "learned_docs": {
    "yck25gn683z3wa2f": {
      "slug": "yck25gn683z3wa2f",
      "title": "平台介绍",
      "url": "...",
      "content": "...",
      "links": ["ouwzx8mgo63oboqg", "etgvtorzglntmv39"],
      "learned_at": "2026-03-20T10:30:00"
    }
  },
  "pending_links": [],
  "total_learned": 15
}
```

### 文档文件
`knowledge/<slug>.md`
```markdown
# 平台介绍

> 来源：广联达行业 AI 平台文档中心  
> 链接：https://glodon-cv-help.yuque.com/cuv0se/ol9231/yck25gn683z3wa2f  
> 学习时间：2026-03-20T10:30:00  
> 关联链接：2 个

---

## 文档内容

[完整的文档内容...]

---

## 关联文档

1. https://glodon-cv-help.yuque.com/cuv0se/ol9231/ouwzx8mgo63oboqg
2. https://glodon-cv-help.yuque.com/cuv0se/ol9231/etgvtorzglntmv39

---

*本文档由 learn_docs.py 自动学习生成*
```

---

## 🔄 与 bot.py 集成

### 自动触发学习

当用户提问时，`bot.py` 会检测是否需要学习：

```python
# bot.py 中的检测逻辑
def _should_trigger_learning(self, query: str):
    if "不知道" in query or "没有" in query:
        return True, ["lpetkzefs5er4q5x"]  # 常见问题
    return False, []
```

### 手动触发学习

在对话中：
```
用户：去学习 API 调用的文档
助手：好的，正在学习相关文档...
[后台执行 learn_docs.py --slugs etgvtorzglntmv39]
```

---

## ⚙️ 配置选项

在 `config.yaml` 中配置：

```yaml
learning:
  enabled: true           # 是否启用自动学习
  auto_trigger: true      # 检测知识盲区时自动触发
  max_depth: 2            # 最大下钻深度
  rate_limit: 0.5         # 请求间隔（秒），避免限流
  state_file: .learn_state.json
  core_docs:              # 核心文档列表
    - yck25gn683z3wa2f
    - lpetkzefs5er4q5x
```

---

## 📊 监控与维护

### 查看学习状态
```bash
python3 scripts/learn_docs.py --state
```

### 清空学习状态（重新学习）
```bash
rm knowledge/.learn_state.json
```

### 查看已学习文档
```bash
ls -la knowledge/*.md | wc -l
```

---

## ⚠️ 注意事项

1. **语雀 Token** - 没有 Token 只能创建占位文档，无法获取内容
2. **请求频率** - 默认 0.5 秒间隔，避免触发语雀限流
3. **下钻深度** - 建议不超过 3，避免学习过多无关文档
4. **存储空间** - 每篇文档约 5-50KB，59 篇约 1-3MB

---

## 🐛 故障排查

### 问题：无法获取文档内容
```
⚠️  未设置 YUQUE_TOKEN，无法获取文档内容
```
**解决**: 设置环境变量 `export YUQUE_TOKEN='your_token'`

### 问题：请求失败
```
❌ 获取文档失败：xxx - HTTP 401
```
**解决**: 检查 Token 是否有效，是否过期

### 问题：学习卡住
**解决**: 按 Ctrl+C 中断，检查网络连接

---

## 📞 支持

如有问题，查看 `SKILL.md` 或联系技术支持。
