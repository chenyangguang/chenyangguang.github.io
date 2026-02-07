---
title: arch-key
date: 2019-05-12
description: 'arch 系统signature错误升级或者重装失败时，报 error\: krb5\: signature from … is unknown trust… invalid or corrupted package (PGP singature) 解决方法1pacman-key --refresh-keys 或者 1pacman -Sy archlinux-keyring'
tags:
categories:
---

[](#arch-系统signature错误)arch 系统signature错误
升级或者重装失败时，报 error: krb5: signature from … is unknown trust
… invalid or corrupted package (PGP singature)

[](#解决方法)解决方法
```q
pacman-key --refresh-keys
```

或者

```ebnf
pacman -Sy archlinux-keyring
```