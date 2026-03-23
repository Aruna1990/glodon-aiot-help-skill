# 🔧 语雀 Cookie 配置指南

## 为什么需要 Cookie？

语雀知识库虽然是公开的，但**完整内容需要通过 API 获取**，API 需要 Cookie 认证。

---

## 📋 获取 Cookie 步骤

### 步骤 1：打开语雀知识库

在浏览器中访问：
```
https://glodon-cv-help.yuque.com/cuv0se/ol9231
```

### 步骤 2：打开开发者工具

- **Chrome/Edge**: 按 `F12` 或 `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows)
- **Safari**: 按 `Cmd+Option+I`
- **Firefox**: 按 `F12`

### 步骤 3：切换到 Network 标签

在开发者工具中点击 **Network**（网络）标签

### 步骤 4：刷新页面

按 `F5` 或 `Cmd+R` / `Ctrl+R` 刷新页面

### 步骤 5：找到 API 请求

在请求列表中找到：
```
api/docs?book_id=41611578
```

如果没有看到，在过滤框中输入 `api/docs`

### 步骤 6：复制 Cookie

1. 点击 `api/docs` 请求
2. 在右侧找到 **Headers**（请求头）标签
3. 找到 **Cookie** 字段
4. 复制整个 Cookie 值（很长的一串）

### 步骤 7：复制 CSRF Token

在同一个请求的 Headers 中，找到：
```
x-csrf-token: 9XQmovVTHAxtZXPna0_Hd3Pl
```
复制 Token 值

---

## 🔐 配置方式

### 方式 1：环境变量（推荐）

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export YUQUE_COOKIE='你的 Cookie 值'
export YUQUE_CSRF='你的 CSRF Token'

# 重新加载配置
source ~/.bashrc  # 或 source ~/.zshrc
```

### 方式 2：配置文件

```bash
cd /home/admin/.openclaw/workspace/skills/glodon-ai-help

# 复制示例文件
cp .yuque_config.example .yuque_config

# 编辑配置文件
vim .yuque_config
```

填入内容：
```
cookie=你的 Cookie 值
csrf=你的 CSRF Token
```

---

## ⚠️ 注意事项

### Cookie 有效期

- Cookie 会**过期**（通常 7-30 天）
- 过期后需要重新获取
- 学习脚本会提示 Cookie 无效

### 安全提示

- ⚠️ **不要分享 Cookie** - 包含登录凭证
- ⚠️ **不要提交到 Git** - `.yuque_config` 已在 `.gitignore` 中
- ✅ 使用环境变量更安全

### 多设备使用

每个设备/浏览器需要单独获取 Cookie

---

## 🧪 测试配置

```bash
cd /home/admin/.openclaw/workspace/skills/glodon-ai-help

# 测试获取目录
python3 scripts/learn_yuque.py --catalog

# 如果成功，会显示文档列表
# 如果失败，会提示配置 Cookie
```

---

## 🚀 开始学习

配置完成后：

```bash
# 学习全部文档
python3 scripts/learn_yuque.py

# 查看学习状态
cat knowledge/.learn_state.json
```

---

## 📞 常见问题

### Q: Cookie 在哪里？
A: 浏览器开发者工具 → Network → api/docs 请求 → Headers → Cookie

### Q: CSRF Token 是什么？
A: 防止跨站请求伪造的令牌，在同一个请求的 Headers 中

### Q: Cookie 过期了怎么办？
A: 重新按上述步骤获取新的 Cookie

### Q: 可以不用 Cookie 吗？
A: 可以，使用 `learn_simple.py` 但只能获取元数据，无法获取完整内容

---

**最后更新**: 2026-03-20
