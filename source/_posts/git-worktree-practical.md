---
title: Git Worktree 实战指南
date: 2026-02-09
description: 'Git Worktree 实战！本文通过真实项目场景，演示如何使用 git worktree 提升开发效率。包含完整的操作步骤和注意事项。'
tags: [Git, 工具, 实战, 教程]
categories:
---

## 前言

上一篇我们介绍了 Git Worktree 的基本用法。今天来点实战的！

假设你在一家快速发展的公司工作，同时负责：

1. 主线功能开发（`feature` 分支）
2. v2.0 版本维护（`release/v2.0` 分支）
3. v1.0 紧急修复（`hotfix/v1.0` 分支）

传统方式需要在三个分支间频繁切换，代码冲突、环境混乱...

让我们用 Git Worktree 来解决这些问题！

[](#场景一：主线开发时紧急修复)## 场景一：主线开发时紧急修复

### 问题描述

你正在 `feature/new-dashboard` 分支开发新功能，代码改到一半：

```bash
cd ~/project
git status
# On branch feature/new-dashboard
# Changes not staged for commit:
#   modified:   src/components/Dashboard.vue
#   modified:   src/views/Home.vue
#
# Untracked files:
#   src/components/widgets/
```

突然产品经理找你："线上登录功能挂了，马上修复！"

### 传统方式

```bash
# 1. 暂存当前工作
git stash save "WIP: new dashboard"

# 2. 切换到主分支
git checkout main

# 3. 创建修复分支
git checkout -b hotfix/login-bug

# ... 修复代码 ...

# 4. 提交并推送
git add .
git commit -m "Fix: login bug"
git push origin hotfix/login-bug

# 5. 切回开发分支
git checkout feature/new-dashboard

# 6. 恢复工作
git stash pop

# 7. 哎呀！stash pop 有冲突...
```

### 使用 Worktree 方式

```bash
# 1. 创建紧急修复的 worktree
git worktree add ../hotfix-login -b hotfix/login-bug

# 2. 进入修复目录
cd ../hotfix-login

# 3. 修复代码
vim src/auth/login.js

# 4. 测试、提交
npm test
git add .
git commit -m "Fix: login timeout bug"
git push origin hotfix/login-bug

# 5. 删除 worktree
cd ..
git worktree remove hotfix-login

# 你的主工作目录完全不受影响！
cd ~/project
git status
# 还是原来的 feature/new-dashboard 分支
# 所有修改都在
```

### 关键优势

- ✅ 不需要 stash，避免冲突风险
- ✅ 主分支工作完全不受影响
- ✅ 修复完成后一键清理
- ✅ 可以同时维护多个修复分支

[](#场景二：多版本并行开发)## 场景二：多版本并行开发

### 项目背景

你们的软件有两个版本同时维护：

- **v1.0**：稳定版，老客户使用
- **v2.0**：新版，正在推广中

现在需要给两个版本都添加一个新功能。

### 传统方式的问题

```bash
# 开发 v1.0 版本
git checkout release/v1.0
# 开发功能...
git commit -m "Add user profile"

# 切换到 v2.0
git checkout release/v2.0
# 同样的功能，但代码有差异
# cherry-pick? 手动合并？太麻烦了...
```

### Worktree 多版本方案

```bash
# 项目结构
~/myapp/
├── .git/
├── v1.0/          # v1.0 版本工作目录
├── v2.0/          # v2.0 版本工作目录
└── main/          # 主开发目录

# 1. 创建版本 worktree
cd ~/myapp
git worktree add ../myapp-v1.0 release/v1.0
git worktree add ../myapp-v2.0 release/v2.0

# 2. 在不同目录中开发
cd ~/myapp-v1.0
# 添加 v1.0 版本的用户资料功能
vim src/features/user-profile.js
# v1.0 使用老式 API
const api = 'https://api-v1.example.com/user';

git add .
git commit -m "Add user profile (v1.0)"

cd ~/myapp-v2.0
# 添加 v2.0 版本的用户资料功能
vim src/features/user-profile.js
# v2.0 使用新 API
const api = 'https://api-v2.example.com/user';

git add .
git commit -m "Add user profile (v2.0)"

# 3. 分别部署
cd ~/myapp-v1.0
git push origin release/v1.0
npm run deploy:v1.0

cd ~/myapp-v2.0
git push origin release/v2.0
npm run deploy:v2.0
```

### 实用技巧

**为每个版本设置不同环境**

```bash
# v1.0 使用 Node 14
cd ~/myapp-v1.0
echo "14" > .nvmrc
nvm use

# v2.0 使用 Node 18
cd ~/myapp-v2.0
echo "18" > .nvmrc
nvm use

# 每个目录可以独立运行
cd ~/myapp-v1.0 && npm run dev  # 端口 3000
cd ~/myapp-v2.0 && npm run dev  # 端口 3001
```

**版本对比**

```bash
# 查看同一功能在不同版本中的差异
diff ~/myapp-v1.0/src/auth/login.js ~/myapp-v2.0/src/auth/login.js

# 或使用 git diff
cd ~/myapp-v1.0
git diff ../myapp-v2.0/src/auth/login.js
```

[](#场景三：代码审查与协作)## 场景三：代码审查与协作

### 问题场景

同事提交了一个 PR，你需要：

1. 运行项目测试功能
2. 尝试修改代码验证想法
3. 审查通过后合并

### 审查流程

```bash
# 1. 创建审查 worktree
cd ~/project
git worktree add ../review-pr-456 origin/pr/456

# 2. 进入审查目录
cd ../review-pr-456

# 3. 安装依赖并启动
npm install
npm run dev

# 4. 测试功能
# 打开浏览器测试...
# 发现一个问题，想验证修复方案

# 5. 直接修改并测试
vim src/components/Button.js
npm run dev
# 验证修复方案可行

# 6. 如果只是建议，不需要提交
# 只需删除 worktree
cd ..
git worktree remove review-pr-456

# 7. 如果需要提交修改
cd ../review-pr-456
git commit -am "Fix: review comments"
git push origin pr/456
git worktree remove review-pr-456
```

### 批量审查多个 PR

```bash
# 同时审查多个 PR
git worktree add ../pr-123 origin/pr/123
git worktree add ../pr-456 origin/pr/456
git worktree add ../pr-789 origin/pr/789

# 在不同终端分别测试
# Terminal 1: cd ~/pr-123 && npm run dev
# Terminal 2: cd ~/pr-456 && npm run dev
# Terminal 3: cd ~/pr-789 && npm run dev

# 审查完成后批量删除
git worktree list
git worktree remove pr-123
git worktree remove pr-456
git worktree remove pr-789
```

[](#场景四：重构实验)## 场景四：重构实验

### 实验性重构

你想尝试一个大的重构方案，但不确定是否可行：

```bash
# 1. 创建实验 worktree
git worktree add ../experiment-refactor -b experiment/new-arch

# 2. 在实验环境中大胆重构
cd ../experiment-refact

# 重构整个项目结构
mv src/components/* src/views/
mv src/utils/* src/helpers/

# 更新所有 import
# ...

# 3. 如果失败了
cd ..
git worktree remove experiment-refactor
# 主项目完全不受影响！

# 4. 如果成功了
cd ../experiment-refactor
# 测试通过后合并回主分支
git checkout main
git merge experiment/new-arch
git worktree remove experiment-refactor
```

### A/B 测试

```bash
# 创建两个实验版本
git worktree add ../experiment-a -b experiment/variant-a
git worktree add ../experiment-b -b experiment/variant-b

# 实现不同的方案
cd ../experiment-a
# 实现方案 A...
vim src/algo/search.js

cd ../experiment-b
# 实现方案 B...
vim src/algo/search.js

# 分别测试性能
cd ../experiment-a
npm run benchmark
# A: 150ms

cd ../experiment-b
npm run benchmark
# B: 120ms

# 选择更好的方案
cd ~/project
git merge experiment/variant-b
git branch -d experiment/variant-a

# 清理 worktree
git worktree remove experiment-a
git worktree remove experiment-b
```

[](#高级技巧)## 高级技巧

### 1. Worktree 管理

```bash
# 列出所有 worktree
git worktree list

# 查看工作目录状态
git worktree list --porcelain

# 清理无效的 worktree
git worktree prune

# 移动 worktree
git worktree move ../old-path ../new-path

# 锁定 worktree（防止误删）
git worktree lock ../important-branch
git worktree unlock ../important-branch
```

### 2. 与 CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Test All Worktrees

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      # 测试主分支
      - name: Test Main
        run: npm test

      # 并行测试其他分支
      - name: Setup Worktrees
        run: |
          git worktree add ../feature-A
          git worktree add ../feature-B

      - name: Test Feature A
        working-directory: ../feature-A
        run: npm test

      - name: Test Feature B
        working-directory: ../feature-B
        run: npm test
```

### 3. 自动化脚本

```bash
#!/bin/bash
# ~/bin/git-worktree-helper.sh

# 快速创建并切换到 worktree
if [ -z "$1" ]; then
  echo "Usage: git-worktree-helper <branch-name>"
  exit 1
fi

BRANCH=$1
WORKTREE_PATH=~/worktrees/$BRANCH

# 创建 worktree
git worktree add $WORKTREE_PATH -b $BRANCH

# 自动进入目录
cd $WORKTREE_PATH

# 安装依赖（如果有 package.json）
if [ -f "package.json" ]; then
  npm install
fi

# 启动开发服务器
if [ -f "package.json" ]; then
  npm run dev &
fi

echo "Worktree created: $WORKTREE_PATH"
echo "Branch: $BRANCH"
```

使用方式：

```bash
git-worktree-helper feature/new-ui
# 自动创建 worktree、安装依赖、启动服务
```

### 4. IDE 集成

**VS Code**

```bash
# 在不同 worktree 中打开 VS Code
cd ~/project-v1.0
code .

cd ~/project-v2.0
code .
```

** IntelliJ IDEA**

每个 worktree 作为独立项目打开，可以：
- 独立的代码索引
- 独立的运行配置
- 同时调试多个版本

### 5. 配置共享

```bash
# 使用符号链接共享配置文件
cd ~/project-v1.0
ln -s ~/project/.vscode .vscode
ln -s ~/project/.eslintrc.js .eslintrc.js

# 或使用 Git 仓库级别的配置
git config --global include.path ~/.gitconfig-shared
```

[](#注意事项)## 注意事项

### 1. 磁盘空间

虽然 worktree 共享 `.git` 目录，但工作文件会占用空间：

```bash
# 定期清理不需要的 worktree
git worktree list
git worktree remove ../unused-branch

# 查看各 worktree 大小
du -sh ~/project*
```

### 2. 环境变量

不同 worktree 可能需要不同的环境：

```bash
# .env.local 文件
cd ~/project-v1.0
echo "API_URL=https://api-v1.example.com" > .env.local

cd ~/project-v2.0
echo "API_URL=https://api-v2.example.com" > .env.local
```

### 3. Git Hooks

确保 hooks 在所有 worktree 中正常工作：

```bash
# 在主仓库设置 hooks
cd ~/project
cp pre-commit .git/hooks/

# 所有 worktree 会共享这些 hooks
```

### 4. 提交前检查

切换 worktree 前记得检查状态：

```bash
# 在主仓库中检查所有 worktree 状态
git worktree list --porcelain | grep "worktree" | while read line; do
  path=$(echo $line | cut -d' ' -f2)
  echo "Checking $path..."
  cd $path
  git status
done
```

[](#常见问题解决)## 常见问题解决

### Q: Worktree 中 git fetch 没有更新？

```bash
# 在主仓库执行 fetch
cd ~/project
git fetch --all

# 然后在 worktree 中
cd ~/feature-branch
git merge origin/feature-branch
```

### Q: 删除 worktree 时提示有未提交的更改？

```bash
# 强制删除（会丢失更改！）
git worktree remove ../branch --force

# 或先提交更改
cd ../branch
git add .
git commit -m "WIP"
cd ..
git worktree remove ../branch
```

### Q: Worktree 和 submodule 一起使用？

```bash
# 创建 worktree 时会自动初始化 submodule
git worktree add ../feature-branch feature/branch

# 需要手动更新 submodule
cd ../feature-branch
git submodule update --init --recursive
```

[](#实战项目)## 实战项目

让我们用一个完整的项目来练习：

```bash
# 1. 初始化项目
mkdir ~/demo-project
cd ~/demo-project
git init
echo "# Demo Project" > README.md
git add . && git commit -m "Initial commit"

# 2. 创建主开发 worktree
git worktree add ../main-branch main

# 3. 创建功能开发 worktree
git worktree add ../feature-auth -b feature/auth

# 4. 创建 bug 修复 worktree
git worktree add ../hotfix-login -b hotfix/login

# 5. 列出所有 worktree
git worktree list

# 6. 在不同 worktree 中工作
cd ~/main-branch
echo "Main code" > main.js
git add . && git commit -m "Add main code"

cd ~/feature-auth
echo "Auth code" > auth.js
git add . && git commit -m "Add auth feature"

cd ~/hotfix-login
echo "Fix login" > login.js
git add . && git commit -m "Fix login bug"

# 7. 合并工作
cd ~/demo-project
git merge feature/auth
git merge hotfix/login

# 8. 清理 worktree
git worktree remove main-branch
git worktree remove feature-auth
git worktree remove hotfix-login
```

[](#总结)## 总结

Git Worktree 实战要点：

| 场景 | 传统方式 | Worktree 方式 |
|------|----------|---------------|
| 紧急修复 | stash/切换分支 | 创建临时 worktree |
| 多版本维护 | 频繁切换冲突 | 独立版本目录 |
| 代码审查 | 本地切换分支 | 独立审查环境 |
| 重构实验 | 担心破坏代码 | 安全实验空间 |

**记住**：

1. **及时清理** - 用完的 worktree 及时删除
2. **命名规范** - 使用描述性的目录名
3. **定期检查** - `git worktree list` 查看状态
4. **善用 prune** - `git worktree prune` 清理无效记录

Git Worktree 是提升 Git 使用效率的利器，希望这些实战场景能帮助你更好地使用它！

Happy Coding!
