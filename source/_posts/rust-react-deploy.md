---
title: Rust + React 全栈项目部署从 macOS 交叉编译部署到阿里云 Ubuntu 踩坑实录
date: 2026-02-16
description: "记录将 Rust + React 全栈项目从 macOS 开发环境部署到阿里云 Ubuntu 服务器的完整过程，包括 PostgreSQL/Nginx 安装、HTTPS 证书配置、交叉编译、OpenSSL 依赖问题解决等"
tags: [Rust, React, 部署, 阿里云, Ubuntu, Nginx, PostgreSQL]
categories:
---

# Rust 项目从 macOS 交叉编译部署到 Ubuntu 服务器的踩坑实录

>  记录了将一个 Rust + React 全栈项目从 macOS 开发环境部署到阿里云 Ubuntu 服务器的完整过程，包括 PostgreSQL/Nginx 安装、HTTPS 证书配置、交叉编译、OpenSSL 依赖问题解决等。


<!-- more -->


## 背景

项目是一个球场预订系统：
- **后端**: Rust + Axum + Sea-ORM + PostgreSQL
- **前端**: React + Vite + Ant Design (Admin 管理后台)
- **目标服务器**: 阿里云 Ubuntu 22.04

## 一、服务器基础环境配置

### 1.1 安装 PostgreSQL

```bash
# 安装
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# 启动并设置开机自启
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 设置 postgres 用户密码
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'your_password';"
```

### 1.2 安装 Nginx

```bash
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 1.3 配置 HTTPS 证书（通配符域名）

由于需要支持 `*.gitvim.com` 通配符域名，必须使用 DNS 验证方式。

**推荐使用 acme.sh**（比 certbot 更好用）：

```bash
# 安装 acme.sh
curl https://get.acme.sh | sh
source ~/.bashrc

# 配置阿里云 API（用于 DNS 验证）
export Ali_Key="your_access_key_id"
export Ali_Secret="your_access_key_secret"

# 申请通配符证书
acme.sh --issue --dns dns_ali \
  -d xxx.com \
  -d www.xxx.com \
  -d "*.xxx.com" \
  --server letsencrypt

# 安装证书到 Nginx 目录
mkdir -p /etc/nginx/ssl/gitvim
acme.sh --install-cert -d xxx.com \
  --key-file       /etc/nginx/ssl/gitvim/key.pem \
  --fullchain-file /etc/nginx/ssl/gitvim/cert.pem \
  --reloadcmd      "nginx -s reload"
```

**注意**：acme.sh 默认使用 ZeroSSL，建议切换到 Let's Encrypt：

```bash
acme.sh --register-account -m your-email@example.com --server letsencrypt
acme.sh --set-default-ca --server letsencrypt
```

## 二、交叉编译：最大的坑

### 2.1 问题：服务器下载太慢

服务器在国内，下载 Rust 工具链和编译依赖非常慢。解决方案：**本地编译好再上传**。

### 2.2 工具选择：cross vs cargo-zigbuild

| 工具 | 优点 | 缺点 |
|------|------|------|
| cross | 官方推荐，兼容性好 | 需要 Docker |
| cargo-zigbuild | 不需要 Docker | 某些 crate 兼容性问题 |

我选择 **cross**，因为项目依赖较复杂。

### 2.3 安装 cross

```bash
# 需要 Docker Desktop 运行
cargo install cross
```

### 2.4 创建 Cross.toml 配置

```toml
# backend/Cross.toml
[target.x86_64-unknown-linux-gnu]
pre-build = [
    "apt-get update && apt-get install -y libssl-dev pkg-config"
]
```

### 2.5 第一个坑：OpenSSL 版本不兼容

**现象**：
```
./stadium_backend: error while loading shared libraries: libssl.so.1.0.0: cannot open shared object file
```

**原因**：服务器是 OpenSSL 3.x，而 cross 编译的二进制链接的是 OpenSSL 1.0.0。

**尝试方案 1 - 静态编译**：
```bash
OPENSSL_STATIC=1 cross build --release --target x86_64-unknown-linux-gnu
```
结果：仍然失败，静态链接没有生效。

**最终方案 - 使用 rustls 替代 OpenSSL**：

修改 `Cargo.toml`，将依赖从 native-tls 改为 rustls：

```toml
# 原来（依赖系统 OpenSSL）
reqwest = { version = "0.12", features = ["json"] }

# 改为（使用 rustls，纯 Rust 实现）
reqwest = { version = "0.12", features = ["json", "rustls-tls"], default-features = false }
```

```bash
# 编译
cross build --release --target x86_64-unknown-linux-gnu
```

**为什么 rustls 更好？**
- 纯 Rust 实现，无 C 依赖
- 静态链接，二进制可移植
- 更安全，内存安全保证

### 2.6 编译成功后的打包

```bash
# 创建部署目录
mkdir -p deploy/backend deploy/admin

# 复制后端二进制
cp target/x86_64-unknown-linux-gnu/release/stadium_backend deploy/backend/

# 复制配置文件
cp backend/.env.example deploy/backend/

# 构建前端
cd admin && npm run build
cp -r dist ../deploy/admin/

# 打包
tar -czvf stadium-deploy.tar.gz deploy/
```

## 三、部署流程

### 3.1 上传到服务器

```bash
scp stadium-deploy.tar.gz root@xxx.com:/opt/
```

### 3.2 服务器上解压和配置

```bash
cd /opt
tar -xzvf stadium-deploy.tar.gz
cd deploy/backend

# 配置环境变量
cp .env.example .env
nano .env
```

`.env` 关键配置：
```env
DATABASE_URL=postgresql://stadium_admin:password@localhost:5432/stadium
JWT_SECRET=your-random-secret-key
JWT_ADMIN_SECRET=another-random-secret-key
SERVER_PORT=3000
DEV_MODE=0
```

### 3.3 数据库初始化

```bash
# 创建用户和数据库
sudo -u postgres psql << 'EOF'
CREATE USER stadium_admin WITH PASSWORD 'your_password';
CREATE DATABASE stadium OWNER stadium_admin;
GRANT ALL PRIVILEGES ON DATABASE stadium TO stadium_admin;
\c stadium
GRANT ALL ON SCHEMA public TO stadium_admin;
EOF

# 运行迁移（如果有迁移工具）
# ./migration
```

### 3.4 创建 systemd 服务

```bash
cat > /etc/systemd/system/stadium-backend.service << 'EOF'
[Unit]
Description=Stadium Booking Backend
After=network.target postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/deploy/backend
ExecStart=/opt/deploy/backend/stadium_backend
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable stadium-backend
systemctl start stadium-backend
```

### 3.5 配置 Nginx 反向代理

```nginx
# /etc/nginx/sites-available/gitvim
server {
    listen 80;
    server_name xxx.com www.xxx.com *.xxx.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name xxx.com www.xxx.com *.xxx.com;

    ssl_certificate /etc/nginx/ssl/gitvim/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/gitvim/key.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;

    # Admin 前端
    location / {
        root /opt/deploy/admin/dist;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
    }
}
```

```bash
ln -sf /etc/nginx/sites-available/gitvim /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

## 四、问题总结

### 问题 1：OpenSSL 版本不兼容

| 现象 | 解决方案 |
|------|----------|
| `libssl.so.1.0.0: cannot open shared object file` | 使用 rustls 替代 native-tls |

### 问题 2：通配符证书需要 DNS 验证

| 现象 | 解决方案 |
|------|----------|
| certbot HTTP 验证不支持通配符 | 使用 acme.sh + DNS 验证 |

### 问题 3：cross 编译需要 Docker

| 现象 | 解决方案 |
|------|----------|
| `Cannot connect to the Docker daemon` | 启动 Docker Desktop |

### 问题 4：数据库用户认证失败

| 现象 | 解决方案 |
|------|----------|
| `password authentication failed for user` | 检查 .env 配置和 PostgreSQL 用户权限 |

## 五、最佳实践

1. **优先使用 rustls**：避免 OpenSSL 依赖问题，二进制更可移植
2. **本地交叉编译**：避免服务器编译慢的问题
3. **使用 systemd 管理服务**：自动重启、日志管理
4. **HTTPS 必配**：acme.sh 自动续期
5. **打包部署**：只上传必要文件，减小传输体积

## 六、快速部署清单

```bash
# 本地
cross build --release --target x86_64-unknown-linux-gnu
cd admin && npm run build
tar -czvf deploy.tar.gz deploy/
scp deploy.tar.gz root@server:/opt/

# 服务器
cd /opt && tar -xzvf deploy.tar.gz
systemctl start stadium-backend
systemctl reload nginx
```

---

**参考资料**：
- [cross - Cross Compiling Rust](https://github.com/cross-rs/cross)
- [rustls - A TLS library in Rust](https://github.com/rustls/rustls)
- [acme.sh - Let's Encrypt Client](https://github.com/acmesh-official/acme.sh)
