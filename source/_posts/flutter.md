---
title: zsh 中 flutter 中不起作用的问题
date: 2019-05-18
description: 'flutter 起飞最近每次在 zsh 命令行中都是只能临时设置 flutter 路径，或者非得跑到 flutter 安装的 bin 目录中才能启用  flutter , 今天到官网一看才知道，原来 ~/.zshrc 开机加载之后，并没有启动 ~/.bash_profile 于是解决的办法是：在 ~/.zshrc 的末尾加一行,1source ~/.bash_profile 但是我有点疑问是其他命'
tags:
categories:
---

[](#flutter-起飞)flutter 起飞
最近每次在 zsh 命令行中都是只能临时设置 flutter 路径，或者非得跑到 flutter 安装的 bin 目录中才能启用  flutter , 今天到官网一看才知道，原来 ~/.zshrc 开机加载之后，并没有启动 ~/.bash_profile

于是解决的办法是：在 ~/.zshrc 的末尾加一行,

```bash
source ~/.bash_profile
```

但是我有点疑问是其他命令都是可以通过 ~/.zshrc 加的，那样

```bash
source ~/.zshrc
```

就好了呀。
怪哉, 怪哉……