# 📚 广联达行业 AI 平台 - 学习工具完整指南

**技能版本**: glodon-ai-help v1.2.0  
**最后更新**: 2026-03-20

---

## 🎯 学习目标

从语雀知识库（https://glodon-cv-help.yuque.com/cuv0se/ol9231）学习 59 篇文档到本地。

---

## 🛠️ 学习工具对比

| 工具 | Cookie | 内容完整度 | 速度 | 推荐场景 |
|------|--------|-----------|------|---------|
| `learn_simple.py` | ❌ | 元数据 | ⚡ 快 | 快速索引 |
| `learn_yuque.py` | ✅ | 完整 | 🐢 中 | **日常使用** |
| `learn_docs.py` | ✅ (Token) | 完整 + 下钻 | 🐢 慢 | 深度学习 |
| `demo_learn.py` | ❌ | 模拟 | ⚡ 快 | 演示/测试 |

---

## 🚀 快速开始

### 方案 A：无需 Cookie（5 分钟）

适合快速建立文档索引：

```bash
cd /home/admin/.openclaw/workspace/skills/glodon-ai-help

# 学习 5 篇核心文档
python3 scripts/learn_simple.py

# 查看生成的文档
ls -la knowledge/*.md
cat knowledge/yck25gn683z3wa2f.md
```

**优点**: 无需配置，立即可用  
**缺点**: 只有元数据，无完整内容

---

### 方案 B：完整学习（推荐）⭐

#### 步骤 1：获取 Cookie（5 分钟）

详见 [`COOKIE_SETUP.md`](./COOKIE_SETUP.md)

简要步骤：
1. 浏览器访问语雀知识库
2. F12 打开开发者工具
3. Network 标签找到 `api/docs` 请求
4. 复制 Cookie 和 x-csrf-token

#### 步骤 2：配置 Cookie（1 分钟）

```bash
cd /home/admin/.openclaw/workspace/skills/glodon-ai-help

# 复制配置模板
cp .yuque_config.example .yuque_config

# 编辑配置（填入 Cookie 和 CSRF）
vim .yuque_config
```

或使用环境变量：
```bash
export YUQUE_COOKIE='你的 Cookie'
export YUQUE_CSRF='你的 CSRF Token'
```

#### 步骤 3：测试配置（30 秒）

```bash
python3 scripts/learn_yuque.py --catalog
```

看到文档列表表示配置成功。

#### 步骤 4：开始学习（10-30 分钟）

```bash
python3 scripts/learn_yuque.py
```

等待完成，会显示学习进度。

---

## 📖 工具详细说明

### 1. learn_simple.py

**最简单**的学习脚本，兼容所有 Python 版本。

```bash
# 使用
python3 scripts/learn_simple.py

# 输出
knowledge/yck25gn683z3wa2f.md
knowledge/lpetkzefs5er4q5x.md
...
```

**特点**:
- ✅ 无需 Cookie
- ✅ 兼容老 Python
- ✅ 速度快
- ⚠️ 只有元数据

---

### 2. learn_yuque.py ⭐

**推荐使用**的完整学习工具。

```bash
# 学习全部文档
python3 scripts/learn_yuque.py

# 仅获取目录
python3 scripts/learn_yuque.py --catalog

# 查看配置帮助
python3 scripts/learn_yuque.py --config
```

**特点**:
- ✅ 获取完整内容
- ✅ 使用内部 API
- ✅ 自动保存状态
- ⚠️ 需要 Cookie

---

### 3. learn_docs.py

深度学习工具，支持递归下钻关联链接。

```bash
# 学习核心文档
python3 scripts/learn_docs.py

# 学习全部（含下钻）
python3 scripts/learn_docs.py --all --depth 2

# 学习指定文档
python3 scripts/learn_docs.py --slugs yck25gn683z3wa2f lpetkzefs5er4q5x

# 查看状态
python3 scripts/learn_docs.py --state
```

**特点**:
- ✅ 递归下钻学习
- ✅ 状态持久化
- ✅ 关联链接追踪
- ⚠️ 需要语雀 API Token

---

### 4. demo_learn.py

演示学习流程，无需网络。

```bash
# 运行演示
python3 scripts/demo_learn.py

# 查看演示状态
python3 scripts/demo_learn.py --state
```

**特点**:
- ✅ 无需网络
- ✅ 演示流程
- ✅ 创建目录结构
- ⚠️ 模拟内容

---

## 📁 文件目录管理

### 知识库结构

```
knowledge/
├── 01-platform-intro/        # 分类目录
├── 02-api-reference/
├── 03-knowledge-base/
├── 04-prompt-engineering/
├── 05-models/
├── 06-tutorials/
├── 07-faq/
├── *.md                      # 文档文件
├── .learn_state.json         # 学习状态
├── .demo_state.json          # 演示状态
├── LEARN_REPORT.md           # 学习报告
├── faq.json                  # FAQ 库
└── README.md                 # 索引
```

### 文档命名

- 使用语雀 Slug 作为文件名
- 格式：`{slug}.md`
- 示例：`yck25gn683z3wa2f.md`

### 状态追踪

`.learn_state.json` 记录：
```json
{
  "last_sync": "2026-03-20T10:27:00",
  "learned_docs": ["yck25gn683z3wa2f", ...],
  "total_learned": 5
}
```

---

## 🔧 配置管理

### Cookie 配置

**方式 1**: 环境变量
```bash
export YUQUE_COOKIE='...'
export YUQUE_CSRF='...'
```

**方式 2**: 配置文件
```
# .yuque_config
cookie=...
csrf=...
```

### Token 配置（用于 learn_docs.py）

```bash
export YUQUE_TOKEN='...'
```

获取 Token: https://www.yuque.com/settings/tokens

---

## 📊 学习进度

### 查看状态

```bash
# 查看学习状态
cat knowledge/.learn_state.json

# 查看文档数量
ls knowledge/*.md | wc -l

# 查看学习报告
cat knowledge/LEARN_REPORT.md
```

### 更新学习

```bash
# 重新学习全部
python3 scripts/learn_yuque.py

# 增量学习（只学新的）
# 脚本会自动跳过已学习的文档
```

---

## ⚠️ 常见问题

### Q: Cookie 过期了怎么办？
A: 重新获取 Cookie，替换 `.yuque_config` 中的值

### Q: 学习中断了怎么办？
A: 重新运行脚本，会从断点继续

### Q: 如何清空学习记录？
A: 删除状态文件
```bash
rm knowledge/.learn_state.json
```

### Q: 文档内容不完整？
A: 使用 `learn_yuque.py` 或 `learn_docs.py` 获取完整内容

### Q: 如何查看语雀原始链接？
A: 每个文档顶部都有在线查看链接

---

## 📈 学习统计

### 核心文档（5 篇）✅
- 平台介绍
- 平台使用常见问题汇总
- 平台认证 Token 说明文档
- Key Secret 认证获取 Token
- API 调用

### 待学习（54 篇）
- 模型服务（10+ 篇）
- OCR 服务（10+ 篇）
- 应用开发（10+ 篇）
- 工作流（5+ 篇）
- 其他（10+ 篇）

---

## 🎯 推荐学习路径

### 第 1 天：配置 + 核心文档
```bash
# 配置 Cookie
cp .yuque_config.example .yuque_config
vim .yuque_config

# 测试配置
python3 scripts/learn_yuque.py --catalog

# 学习核心 5 篇
python3 scripts/learn_simple.py
```

### 第 2 天：完整学习
```bash
# 学习全部 59 篇
python3 scripts/learn_yuque.py
```

### 第 3 天：深度学习
```bash
# 配置 Token
export YUQUE_TOKEN='...'

# 深度学习（含关联链接）
python3 scripts/learn_docs.py --all --depth 2
```

---

## 📞 支持文档

- [`COOKIE_SETUP.md`](./COOKIE_SETUP.md) - Cookie 配置详解
- [`LEARN_GUIDE.md`](./LEARN_GUIDE.md) - 自动学习功能指南
- [`LEARN_REPORT.md`](./knowledge/LEARN_REPORT.md) - 学习报告
- [`SKILL.md`](./SKILL.md) - 技能说明

---

**最后更新**: 2026-03-20 10:38  
**技能版本**: glodon-ai-help v1.2.0
