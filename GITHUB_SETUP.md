# 发布到 GitHub 操作指南

## 当前状态

✅ Git 仓库已初始化  
✅ 首次提交已完成（154 个文件）  
✅ .gitignore 已配置（已排除 .yuque_config、.learn_state.json 等敏感/生成文件）

---

## 下一步：在 GitHub 创建仓库并推送

### 方式一：网页操作（推荐）

1. **创建新仓库**
   - 访问 https://github.com/new
   - Repository name 建议：`glodon-ai-help`（或自定义）
   - 选择 Public
   - ⚠️ **不要**勾选 "Add a README"（本地已有）
   - 点击 Create repository

2. **在本地添加远程并推送**

   ```bash
   cd /Users/aruna/Downloads/glodon-ai-help

   # 将下面的 YOUR_USERNAME 替换为你的 GitHub 用户名
   git remote add origin https://github.com/YOUR_USERNAME/glodon-ai-help.git

   git push -u origin main
   ```

### 方式二：使用 SSH（如果已配置 SSH key）

```bash
cd /Users/aruna/Downloads/glodon-ai-help
git remote add origin git@github.com:YOUR_USERNAME/glodon-ai-help.git
git push -u origin main
```

---

## 注意事项

- **不要提交** `.yuque_config`（内含 Cookie/Token），已在 .gitignore 中排除
- 首次 push 可能需要输入 GitHub 用户名和密码（建议使用 Personal Access Token 代替密码）
- 如需安装 GitHub CLI 实现一键创建：`brew install gh` → `gh auth login` → `gh repo create glodon-ai-help --source=. --push`
