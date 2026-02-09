# Git Worktree 使用指南

> 在同一个 git 仓库中同时维护多个独立的工作目录，实现真正的并行开发

## 为什么需要 Git Worktree？

### 传统工作流的痛点

```bash
# 场景：你正在开发一个复杂功能，突然需要修复紧急 bug

传统方式：
1. 暂存当前开发进度：git stash
2. 切换到修复分支：git checkout -b hotfix/bug
3. 修复 bug，提交，推送
4. 切回原分支：git checkout feature/new-feature
5. 恢复开发进度：git stash pop
6. 如果 stash 冲突，还需要手动解决...

问题：
- 频繁切换分支浪费时间
- 未完成的工作需要反复 stash/pop
- 如果当前有大量修改，stash 可能失败
- 无法同时运行不同版本的代码进行测试对比
```

### Git Worktree 的优势

```bash
# 场景：同样的情况，使用 git worktree

使用 git worktree：
1. 保持当前开发环境不变
2. 创建新的 worktree：git worktree add ../stadium-hotfix hotfix/bug
3. 进入新目录，修复 bug，提交，推送
4. 回到原目录继续开发，完全不受影响

优势：
- 无需切换分支，零干扰
- 未完成的工作可以保留在原目录
- 可以同时运行多个版本的代码
- 每个任务独立的工作环境，互不冲突
```

## 目录结构说明

### 实际目录布局

```
/Users/c/Apps/                    # 父目录
├── stadium-booking/             # 主工作目录（原目录）
│   ├── .git/                    # Git 仓库（唯一的）
│   ├── backend/
│   ├── frontend/
│   └── ...
│
├── stadium-feature-auth/        # Worktree 1（功能开发）
│   ├── backend/                 # 指向同一个 .git 仓库
│   ├── frontend/
│   └── ...
│
├── stadium-feature-payment/     # Worktree 2（支付功能）
│   ├── backend/
│   ├── frontend/
│   └── ...
│
└── stadium-hotfix/              # Worktree 3（紧急修复）
    ├── backend/
    ├── frontend/
    └── ...
```

**关键点：**
- 每个 worktree 都是一个完整的代码副本
- 所有 worktree 共享同一个 `.git` 仓库（在主目录）
- 每个 worktree 处于不同的分支
- 在任何 worktree 的提交都会出现在所有 worktree 中（共享历史）
- 删除 worktree 不会丢失代码（因为提交已经保存在 `.git` 中）

### 可视化理解

```
┌─────────────────────────────────────────────────────────┐
│                   唯一的 .git 仓库                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │  所有分支、所有提交历史、所有配置都在这里         │   │
│  │  worktree 只是 .git 的多个"视图"                 │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
           │                      │                      │
           ▼                      ▼                      ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │ main 分支 │           │ auth 分支 │           │ fix 分支  │
    │ 工作目录  │           │ 工作目录  │           │ 工作目录  │
    └──────────┘           └──────────┘           └──────────┘
```

## 基础命令详解

### 1. 创建 Worktree

```bash
# 基本语法
git worktree add <新目录路径> [分支名]

# 示例 1：基于当前分支创建新 worktree
git worktree add ../stadium-feature-auth feature/auth
# 说明：
# - ../stadium-feature-auth: 新 worktree 的目录位置（在父目录）
# - feature/auth: 新创建的分支名（如果已存在，则使用现有分支）

# 示例 2：基于现有分支创建 worktree
git worktree add ../stadium-hotfix hotfix/critical-bug
# 说明：
# - hotfix/critical-bug: 使用已存在的分支
```

### 2. 查看 Worktree 列表

```bash
git worktree list

# 输出示例：
# /Users/c/Apps/stadium-booking        4cf1cb5 [main]
# /Users/c/Apps/stadium-feature-auth   3298255 [feature/auth]
# /Users/c/Apps/stadium-hotfix         7a8b9c0 [hotfix/critical-bug]
#
# 说明：
# - 第一列：工作目录的完整路径
# - 第二列：该 worktree 当前所在的 commit hash
# - 第三列：该 worktree 当前所在的分支名
```

### 3. 切换到不同的 Worktree

```bash
# 使用 cd 进入 worktree 目录
cd ../stadium-feature-auth

# 查看当前 worktree 的状态
git status
git branch  # 会显示 * feature/auth
git log     # 会看到完整的提交历史

# 在 worktree 中进行任何 git 操作都和在主目录一样
git add .
git commit -m "feat: implement authentication"
git push origin feature/auth
```

### 4. 删除 Worktree

```bash
# 步骤 1：删除 worktree 目录
git worktree remove <目录路径>

# 示例：
git worktree remove /Users/c/Apps/stadium-feature-auth

# 步骤 2：删除对应的分支（可选）
git branch -d feature/auth

# 注意：
# - 如果分支上有未合并的提交，需要用 -D 强制删除
# - 删除 worktree 不会删除提交（提交在 .git 中）
# - 只有删除分支才会失去该分支的提交历史
```

## 实际工作流示例

### 场景 1：并行开发多个功能

```bash
# 背景：需要同时开发认证、支付、管理后台三个功能

# 1. 创建三个 worktree
cd /Users/c/Apps/stadium-booking  # 主目录

git worktree add ../stadium-auth feature/auth
git worktree add ../stadium-payment feature/payment
git worktree add ../stadium-admin feature/admin

# 2. 在不同的 terminal 窗口并行开发
# Terminal 1: 认证功能
cd /Users/c/Apps/stadium-auth
# 开发认证相关的代码
git add .
git commit -m "feat: implement WeChat login"
git push origin feature/auth

# Terminal 2: 支付功能
cd /Users/c/Apps/stadium-payment
# 开发支付相关的代码
git add .
git commit -m "feat: integrate WeChat Pay"
git push origin feature/payment

# Terminal 3: 管理后台
cd /Users/c/Apps/stadium-admin
# 开发管理后台的代码
git add .
git commit -m "feat: add admin panel"
git push origin feature/admin

# 3. 测试时可以同时运行三个版本（不同端口）
# Terminal 4: 主分支（main）
cd /Users/c/Apps/stadium-booking
cargo run --port 3000  # 运行主版本

# Terminal 5: 认证分支
cd /Users/c/Apps/stadium-auth
cargo run --port 3001  # 运行认证版本

# Terminal 6: 支付分支
cd /Users/c/Apps/stadium-payment
cargo run --port 3002  # 运行支付版本

# 4. 三个功能开发完成后，分别创建 PR 合并到 main
```

### 场景 2：开发中需要紧急修复

```bash
# 背景：你正在开发复杂功能，突然发现线上有 bug 需要紧急修复

# 1. 当前状态
cd /Users/c/Apps/stadium-booking
# 当前在 feature/new-complex-feature 分支
# 有大量未提交的代码

# 2. 不需要切换分支，直接创建 hotfix worktree
git worktree add ../stadium-hotfix hotfix/critical-bug

# 3. 在 hotfix worktree 中修复 bug
cd /Users/c/Apps/stadium-hotfix
# 修复 bug
git add .
git commit -m "hotfix: fix booking conflict issue"
git push origin hotfix/critical-bug

# 4. 回到原 worktree 继续开发
cd /Users/c/Apps/stadium-booking
# 未完成的代码完全保留，不受任何影响
# 继续开发...
```

### 场景 3：Code Review 不同版本

```bash
# 背景：需要同时 review 多个 PR

# 1. 为每个 PR 创建 worktree
git worktree add ../review-pr-123 origin/pr/123
git worktree add ../review-pr-456 origin/pr/456
git worktree add ../review-pr-789 origin/pr/789

# 2. 在不同的 worktree 中 review
cd ../review-pr-123
# review PR #123
git log  # 查看提交历史
git diff main  # 对比主分支

cd ../review-pr-456
# review PR #456
# ...

cd ../review-pr-789
# review PR #789
# ...

# 3. Review 完成后删除 worktree
cd /Users/c/Apps/stadium-booking
git worktree remove ../review-pr-123
git worktree remove ../review-pr-456
git worktree remove ../review-pr-789
```

### 场景 4：前后端分离开发

```bash
# 背景：后端和前端由不同团队开发，但需要紧密配合

# 后端团队
git worktree add ../backend-auth feature/backend-auth
git worktree add ../backend-payment feature/backend-payment

# 前端团队
git worktree add ../frontend-auth feature/frontend-auth
git worktree add ../frontend-payment feature/frontend-payment

# 后端开发认证 API
cd ../backend-auth/backend
cargo run  # 运行后端（端口 3000）

# 前端开发认证 UI
cd ../frontend-auth/frontend
npm run dev  # 运行前端（端口 8080）

# 后端开发支付 API
cd ../backend-payment/backend
cargo run --port 3001  # 运行后端（端口 3001）

# 前端开发支付 UI
cd ../frontend-payment/frontend
npm run dev --port 8081  # 运行前端（端口 8081）
```

## 项目推荐的分支策略

### 分支命名规范

```
main                              # 生产代码，保持稳定
├── feature/                      # 新功能开发
│   ├── auth-wechat               # 微信登录认证
│   ├── payment-integration       # 支付功能集成
│   ├── admin-panel               # 管理后台
│   ├── booking-system            # 预定系统
│   └── loyalty-program           # 会员积分系统
├── bugfix/                       # Bug 修复
│   ├── booking-conflict          # 预定冲突问题
│   ├── slot-lock-timeout         # 时段锁定超时
│   └── wallet-balance-error      # 钱包余额错误
├── refactor/                     # 代码重构
│   ├── api-response-format       # API 响应格式统一
│   ├── di-container              # 依赖注入容器优化
│   └── database-index            # 数据库索引优化
├── hotfix/                       # 紧急修复（从 main 直接分支）
│   ├── critical-security         # 安全漏洞修复
│   └── production-bug            # 生产环境紧急修复
└── release/                      # 版本发布
    ├── v1.0.0                    # v1.0.0 版本准备
    ├── v1.1.0                    # v1.1.0 版本准备
    └── v2.0.0                    # v2.0.0 版本准备
```

### 推荐的 Worktree 布局

```
/Users/c/Apps/
├── stadium-booking/               # 主目录（main 分支）
├── stadium-feat-auth/            # feature/auth-wechat
├── stadium-feat-payment/         # feature/payment-integration
├── stadium-feat-admin/           # feature/admin-panel
├── stadium-bugfix-conflict/      # bugfix/booking-conflict
└── stadium-hotfix-security/      # hotfix/critical-security
```

## 常见问题

### Q1: 删除 worktree 会丢失代码吗？

**不会。** 删除 worktree 只是删除工作目录，所有提交都保存在 `.git` 仓库中。

```bash
# 安全的删除流程
git worktree remove ../stadium-feature-auth  # 删除目录
git branch -d feature/auth                    # 删除分支（可选）
# 如果分支上有未合并的提交，git 会警告你
# 删除分支之前，可以先把分支 push 到远程保存
```

### Q2: 两个 worktree 改同一个文件会冲突吗？

Git 会检测冲突，但不阻止你修改。但提交时需要注意：

```bash
# Worktree 1
cd ../stadium-auth
echo "const version = '1.0'" > backend/src/config.rs
git add .
git commit -m "feat: add version config"  # ✓ 成功

# Worktree 2
cd ../stadium-payment
echo "const version = '2.0'" > backend/src/config.rs
git add .
git commit -m "feat: update version config"  # ✓ 成功

# 但当合并这两个分支时会产生冲突

# 建议：每个 worktree 改不同的模块，避免冲突
```

### Q3: 可以在 worktree 中创建子 worktree 吗？

可以，但不推荐。最好所有 worktree 都基于同一个主目录创建。

```bash
# 主目录
cd /Users/c/Apps/stadium-booking

# 推荐方式：所有 worktree 平级
git worktree add ../stadium-auth feature/auth
git worktree add ../stadium-payment feature/payment

# 不推荐方式：嵌套 worktree（容易搞混）
cd ../stadium-auth
git worktree add ../stadium-auth-feature-b feature/auth-b  # 混乱
```

### Q4: 如何知道当前在哪个 worktree？

```bash
# 方法 1：使用 pwd 或显示当前路径
pwd  # 显示完整路径
# /Users/c/Apps/stadium-auth

# 方法 2：使用 git worktree list 查看标记
git worktree list
# /Users/c/Apps/stadium-booking        4cf1cb5 [main]
# /Users/c/Apps/stadium-auth           3298255 [feature/auth] *
#                                    ↑
#                            * 表示当前所在的 worktree
```

### Q5: 如何把 worktree 的更改同步到主分支？

```bash
# 方法 1：使用 git merge
cd /Users/c/Apps/stadium-booking  # 切换到 main 分支
git merge feature/auth  # 合并 feature/auth 分支

# 方法 2：使用 rebase（保持线性历史）
cd /Users/c/Apps/stadium-booking
git rebase feature/auth  # 把 feature/auth 的提交 rebase 到 main

# 方法 3：创建 PR（推荐）
cd ../stadium-auth
git push origin feature/auth  # 推送到远程
# 在 GitHub/GitLab 上创建 PR，经过 code review 后合并
```

## 常用命令速查表

| 命令 | 说明 |
|------|------|
| `git worktree add <path> <branch>` | 创建新 worktree |
| `git worktree list` | 列出所有 worktree |
| `git worktree remove <path>` | 删除 worktree |
| `git worktree prune` | 清理失效的 worktree（目录已被删除但 worktree 记录还存在） |
| `git branch` | 查看所有分支（包括 worktree 中的分支） |
| `git branch -D <branch>` | 强制删除分支 |
| `git stash` | 暂存当前修改 |
| `git stash pop` | 恢复暂存的修改 |

## 项目实战示例

### 示例：你的项目的完整工作流

```bash
# === 场景：准备开始三个新功能的开发 ===

# 1. 切换到主目录
cd /Users/c/Apps/stadium-booking

# 2. 确保主分支是最新的
git checkout main
git pull origin main

# 3. 创建三个 worktree 用于并行开发
git worktree add ../stadium-wechat-login feature/wechat-login
git worktree add ../stadium-wechat-pay feature/wechat-pay
git worktree add ../stadium-admin-rbac feature/admin-rbac

# 4. 在不同的 terminal 中开始并行开发

# Terminal 1: 微信登录功能
cd /Users/c/Apps/stadium-wechat-login
# 后端：实现微信 code2session
cd backend/src
# 修改 auth.rs 添加微信登录逻辑
cd /Users/c/Apps/stadium-wechat-login/backend
cargo run

# Terminal 2: 前端微信登录 UI
cd /Users/c/Apps/stadium-wechat-login/frontend
npm run dev:weapp
# 修改登录页面，调用后端 API

# Terminal 3: 微信支付功能
cd /Users/c/Apps/stadium-wechat-pay
# 后端：实现微信支付
cd backend/src
# 修改 payment.rs 添加微信支付逻辑
cd /Users/c/Apps/stadium-wechat-pay/backend
cargo run --port 3001

# Terminal 4: 前端支付 UI
cd /Users/c/Apps/stadium-wechat-pay/frontend
npm run dev:weapp --port 8081
# 修改支付页面，调用后端 API

# Terminal 5: 管理 RBAC 功能
cd /Users/c/Apps/stadium-admin-rbac
# 后端：实现角色权限管理
cd backend/src
# 修改 admin.rs 添加 RBAC 逻辑
cd /Users/c/Apps/stadium-admin-rbac/backend
cargo run --port 3002

# Terminal 6: 前端管理后台
cd /Users/c/Apps/stadium-admin-rbac/frontend
npm run dev:weapp --port 8082
# 修改管理后台页面，调用后端 API

# 5. 每个功能开发完成后提交
cd /Users/c/Apps/stadium-wechat-login
git add .
git commit -m "feat: implement WeChat login integration"
git push origin feature/wechat-login

cd /Users/c/Apps/stadium-wechat-pay
git add .
git commit -m "feat: implement WeChat Pay integration"
git push origin feature/wechat-pay

cd /Users/c/Apps/stadium-admin-rbac
git add .
git commit -m "feat: implement admin RBAC system"
git push origin feature/admin-rbac

# 6. 在 GitHub/GitLab 上创建三个 PR
# - PR #1: feature/wechat-login → main
# - PR #2: feature/wechat-pay → main
# - PR #3: feature/admin-rbac → main

# 7. Code review 通过后，三个 PR 合并到 main

# 8. 清理 worktree
cd /Users/c/Apps/stadium-booking
git worktree remove ../stadium-wechat-login
git worktree remove ../stadium-wechat-pay
git worktree remove ../stadium-admin-rbac

# 9. 拉取最新的 main
git pull origin main

# 10. 开始下一批功能的开发...
```

## 最佳实践

### ✅ 推荐做法

1. **清晰的目录命名**
   ```bash
   # 好的命名：一眼就能看出是什么功能
   ../stadium-wechat-login
   ../stadium-payment-integration
   ../stadium-admin-rbac

   # 不好的命名：看不出是什么
   ../temp1
   ../worktree-2
   ../test-branch
   ```

2. **定期清理不需要的 worktree**
   ```bash
   # 开发完成后及时清理
   git worktree remove ../stadium-completed-feature
   git branch -d feature/completed
   ```

3. **使用一致的分支命名规范**
   ```bash
   feature/wechat-login    # 功能开发
   bugfix/booking-conflict # Bug 修复
   hotfix/critical-bug     # 紧急修复
   refactor/api-response   # 重构
   ```

4. **定期同步 main 分支到 feature 分支**
   ```bash
   cd ../stadium-wechat-login
   git checkout main
   git pull origin main
   git checkout feature/wechat-login
   git merge main  # 合并最新的 main
   ```

### ❌ 避免的做法

1. **不要在 worktree 中创建嵌套 worktree**
   ```bash
   # 避免：容易搞混目录结构
   cd ../stadium-auth
   git worktree add ../stadium-auth-sub feature/auth-sub
   ```

2. **不要在多个 worktree 中同时修改同一个文件**
   ```bash
   # 避免：容易产生合并冲突
   # worktree-1: 修改 backend/src/api/auth.rs
   # worktree-2: 也修改 backend/src/api/auth.rs
   ```

3. **不要长时间保留未使用的 worktree**
   ```bash
   # 避免：占用磁盘空间，容易忘记哪个 worktree 是干什么的
   # 建议及时清理已完成的工作
   ```

## 总结

Git Worktree 是一个强大的工具，可以让你：

- ✅ 同时进行多个任务，无需频繁切换分支
- ✅ 保留未完成的工作，不被临时任务打断
- ✅ 同时运行多个版本的代码进行测试对比
- ✅ 独立的工作环境，互不冲突

**适合场景：**
- 需要同时开发多个功能
- 开发过程中需要紧急修复 bug
- 需要 review 多个 PR
- 前后端分离开发
- 需要测试不同版本的代码

**不适合场景：**
- 只有一个任务需要开发（直接用传统方式更简单）
- 磁盘空间非常紧张（每个 worktree 都是一个完整的代码副本）

---

开始使用吧！推荐从简单的任务开始，熟悉后再应用到复杂的多任务并行开发中。
