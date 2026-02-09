---
title: Git Worktree 应该这样用
date: 2026-02-09
description: 'Git Worktree 是一个强大但常被忽视的功能。本文介绍如何使用 git worktree 来同时处理多个分支，提高开发效率。'
tags: [Git, 工具, 教程]
categories:
---

## 为什么需要 Git Worktree？

在日常开发中，我们经常遇到这样的场景：

1. 正在开发一个新功能，突然需要修复线上紧急 bug
2. 同时需要维护多个版本分支（如 v1.0、v2.0）
3. 需要对比两个分支的代码差异

传统做法是：
- 使用 `git stash` 暂存当前工作
- 或者创建多个工作目录副本

但这些方法都有问题：
- `git stash` 容易混乱，且只能暂存一套
- 多个副本占用空间，且不同步

**Git Worktree 完美解决了这些问题！**

## 什么是 Git Worktree？

Git Worktree 允许你在同一个仓库中，同时检出多个分支到不同的工作目录。

```
my-project/
├── .git/
├── main-branch/          # 主分支工作目录
├── feature-branch/       # 功能分支工作目录
└── hotfix-branch/        # 热修复分支工作目录
```

## 基本用法

### 创建新的 Worktree

```bash
# 基于现有分支创建 worktree
git worktree add ../feature-branch feature-branch

# 基于新分支创建 worktree
git worktree add ../bugfix -b hotfix/bug-123

# 指定提交创建 worktree
git worktree add ../temp-commit abc1234
```

### 查看 Worktree 列表

```bash
git worktree list
```

输出示例：
```
/Users/dev/project                            abc1234 [main]
/Users/dev/feature-branch          def5678 [feature-branch]
/Users/dev/hotfix-branch            3456789 [hotfix/bug-123]
```

### 删除 Worktree

```bash
# 删除指定 worktree
git worktree remove ../feature-branch

# 删除后清理
git worktree prune
```

## 实战场景

### 场景一：紧急 Bug 修复

```bash
# 1. 当前正在开发功能
cd ~/dev/project
git status
# On branch feature/new-ui
# Changes not staged...

# 2. 突然需要修复紧急 bug
git worktree add ../hotfix main
cd ../hotfix

# 3. 修复 bug 并提交
# ... 修复代码 ...
git add .
git commit -m "Fix: critical bug"
git push origin main

# 4. 删除 worktree
cd ..
git worktree remove hotfix
```

### 场景二：同时维护多个版本

```bash
# 主目录：开发版本
cd ~/dev/project-main

# 创建稳定版本 worktree
git worktree add ../project-v1.0 release/v1.0

# 创建下一个版本 worktree
git worktree add ../project-v2.0 develop

# 现在可以同时在不同目录工作
# ~/dev/project-main    - 开发新功能
# ~/dev/project-v1.0    - 修复 v1.0 bug
# ~/dev/project-v2.0    - 准备 v2.0 发布
```

### 场景三：代码审查

```bash
# 审查同事的 PR
git worktree add ../review-pr-123 origin/pr/123

# 在独立目录中测试、修改
cd ../review-pr-123
npm install
npm test

# 如果发现问题，直接提交
git commit -m "Fix review comments"
git push origin pr/123

# 完成后删除
git worktree remove review-pr-123
```

## 高级技巧

### 1. 自动清理

```bash
# 添加自动清理配置
git config worktree.cleanup true

# 或者在 .gitconfig 中添加
[worktree]
    cleanup = true
```

### 2. Worktree 与 Git Hook

在每个 worktree 中，Git hooks 都会独立工作：

```bash
# 在主仓库设置 hooks
cd ~/dev/project
cp pre-commit .git/hooks/

# 所有 worktree 都会使用相同的 hooks
```

### 3. 不同 Worktree 使用不同配置

```bash
# 在每个 worktree 中使用不同的 .git/config
cd ~/dev/project-v1.0
git config user.email "v1.0-maintainer@example.com"

cd ~/dev/project-v2.0
git config user.email "v2.0-maintainer@example.com"
```

## 常见问题

### Q1: Worktree 可以推送吗？

A: 可以！每个 worktree 都可以独立推送：

```bash
cd ../feature-branch
git push origin feature-branch
```

### Q2: 如何在不同 worktree 之间共享配置？

A: 使用全局 Git 配置或符号链接：

```bash
# 共享 .gitignore
ln -s ~/dev/project/.gitignore ~/dev/feature-branch/.gitignore
```

### Q3: Worktree 会占用更多空间吗？

A: 不会！Worktree 共享同一个 `.git` 目录，只包含工作文件，不会复制 Git 对象。

## 最佳实践

1. **命名规范**
   ```bash
   # 使用描述性的目录名
   git worktree add ../feature-user-auth feature/user-auth
   git worktree add ../hotfix-login-bug hotfix/login-bug
   ```

2. **定期清理**
   ```bash
   # 每周清理未使用的 worktree
   git worktree prune
   ```

3. **使用完及时删除**
   ```bash
   # 任务完成后删除 worktree
   git worktree remove ../temporary-branch
   ```

4. **配合 IDE 使用**
   - VS Code：每个 worktree 作为独立项目打开
   - IntelliJ：使用 "Open as Project"

## 总结

Git Worktree 是一个强大的工具，可以：

- ✅ 同时处理多个分支
- ✅ 避免频繁切换分支
- ✅ 隔离不同任务的工作环境
- ✅ 不占用额外存储空间

如果你的工作涉及多分支并行开发，Git Worktree 绝对值得一试！

## 参考资源

- [Git Worktree 官方文档](https://git-scm.com/docs/git-worktree)
- [Git Worktree 实战技巧](https://github.blog/git-worktree/)

[](#进一步学习)进一步学习

尝试在你的下一个项目中使用 Git Worktree，你会发现开发效率大大提升！

如果你有更多 Git Worktree 使用技巧，欢迎分享！
