# 广联达行业 AI 平台 - 使用说明

## 🎯 功能说明

该问答机器人基于语雀知识库（59 篇文档）和 FAQ 库（10+ 问题），可以：

1. **回答用户问题** - 基于 FAQ 库提供详细答案
2. **提供文档链接** - 自动匹配相关文档
3. **智能搜索** - 关键词匹配 + 语义理解

---

## 🚀 快速开始

### 方式 1: 命令行交互

```bash
cd /home/admin/.openclaw/workspace/skills/glodon-ai-help
python3 scripts/bot.py
```

然后输入问题即可：
```
🤔 你的问题：如何获取 API Key
```

### 方式 2: 代码调用

```python
from bot import AIBotAssistant

bot = AIBotAssistant()

# 提问
response = bot.answer("如何获取 API Token？")

# 获取格式化回答
formatted = bot.format_response(response)
print(formatted)

# 获取原始数据
print(response['answer'])           # 答案文本
print(response['faq_answer'])       # FAQ 答案
print(response['related_docs'])     # 相关文档链接
```

### 方式 3: Webhook 集成

```python
# 在 OpenClaw 技能中调用
from glodon_ai_help.bot import AIBotAssistant

def handle_user_message(message):
    bot = AIBotAssistant()
    response = bot.answer(message)
    return bot.format_response(response)
```

---

## 📋 回答格式

机器人回答包含三部分：

### 1. FAQ 答案（如果有匹配）
```
📋 **如何获取 API Key？**

获取 API Key 步骤：
1. 登录平台...
2. 进入控制台...
...
```

### 2. 相关文档链接
```
📚 **相关文档**:

1. [知识库 API 对接文档](https://...)
2. [API 调用](https://...)
3. [平台认证 Token 说明文档](https://...)
```

### 3. 知识库首页
```
📖 **知识库首页**: https://glodon-cv-help.yuque.com/cuv0se/ol9231
```

---

## 🎯 示例问答

### 认证相关
```
Q: 如何获取 API Token？
A: 有两种方式...
   📚 相关文档：平台认证 Token 说明文档、Key Secret 认证获取 Token
```

### API 调用
```
Q: API 返回 401 怎么办？
A: 401 错误表示认证失败...
   📚 相关文档：API 调用、服务 API 调用
```

### OCR 相关
```
Q: 怎么调用 OCR 接口？
A: 平台支持多种 OCR 能力...
   📚 相关文档：OCR 检测、OCR 文本识别、表格识别...
```

### 知识库
```
Q: 知识库怎么用？
A: 知识库使用步骤...
   📚 相关文档：知识库、知识库 API 对接文档、RAG 检索
```

### Prompt 工程
```
Q: 有 Prompt 模板吗？
A: 平台提供多种 Prompt 模板...
   📚 相关文档：Prompt 工程、Prompt 模板、prompt 样例库
```

---

## 🔧 配置说明

### 环境变量（可选）
```bash
# 语雀 Token（用于获取完整文档内容）
export YUQUE_TOKEN='your_token'

# 知识库路径
export KNOWLEDGE_DIR='/path/to/knowledge'
```

### 文件结构
```
glodon-ai-help/
├── bot.py                      # 问答机器人主程序
├── knowledge/
│   ├── faq.json                # FAQ 库
│   ├── README.md               # 文档索引
│   └── *.md                    # 59 篇文档
└── USAGE.md                    # 使用说明（本文件）
```

---

## 📊 匹配逻辑

### FAQ 匹配
1. **问题匹配** - 逐词匹配用户问题和 FAQ 问题
2. **标签匹配** - 匹配 FAQ 标签（权重×3）
3. **分类匹配** - 匹配 FAQ 分类（权重×2）
4. **答案匹配** - 用户问题出现在答案中（权重×5）

### 文档匹配
1. **标题完全匹配** - 用户问题在文档标题中（权重×10）
2. **关键词匹配** - 逐词匹配标题（权重×2）
3. **主题匹配** - OCR、Token、API 等特殊主题（权重×5）

---

## 🔌 集成到 OpenClaw

### 在技能中调用

```python
# skills/glodon-ai-help/SKILL.md 中定义的处理逻辑
from bot import AIBotAssistant

def handle_message(user_message):
    bot = AIBotAssistant()
    response = bot.answer(user_message)
    return bot.format_response(response)
```

### Webhook 配置

```yaml
# config.yaml
webhook:
  endpoint: /api/webchat
  handler: bot.handle_message
```

---

## 📈 性能优化

### 缓存机制
```python
# 添加缓存
from functools import lru_cache

@lru_cache(maxsize=100)
def answer_cached(query):
    return bot.answer(query)
```

### 批量搜索
```python
# 一次性搜索多个相关问题
questions = ["如何获取 Token", "Token 有效期", "Token 刷新"]
responses = [bot.answer(q) for q in questions]
```

---

## 🐛 故障排查

### 问题：找不到 FAQ 答案
**原因**: FAQ 库中没有匹配的问题
**解决**: 在 `knowledge/faq.json` 中添加新 FAQ

### 问题：文档链接不相关
**原因**: 关键词匹配度低
**解决**: 优化文档标题或添加更多关键词

### 问题：回答速度慢
**原因**: 文档数量多
**解决**: 添加缓存或优化搜索算法

---

## 📝 更新 FAQ 库

编辑 `knowledge/faq.json`:

```json
{
  "faqs": [
    {
      "id": "faq_011",
      "question": "你的新问题",
      "answer": "详细答案...",
      "category": "分类",
      "tags": ["标签 1", "标签 2"]
    }
  ]
}
```

---

## 🎓 最佳实践

1. **问题标准化** - 使用用户常用的提问方式
2. **答案结构化** - 使用列表、代码块等格式
3. **标签丰富** - 添加多个相关标签提高匹配率
4. **文档更新** - 定期同步语雀最新文档
5. **收集反馈** - 记录未匹配的问题，补充 FAQ

---

## 📞 支持

- **知识库**: https://glodon-cv-help.yuque.com/cuv0se/ol9231
- **技术支持**: 平台使用常见问题汇总
- **投诉建议**: 用户投诉举报处理系统

---

**最后更新**: 2026-03-19
**版本**: v1.1.0
