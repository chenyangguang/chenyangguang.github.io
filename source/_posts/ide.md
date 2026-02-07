---
title: Emacs as golang IDE
date: 2018-11-27
description: 'IDE据我观察，很多程序员们喜欢 IDE 的原因在于工程化全局查询，函数定义, 复制粘贴， 其他的模块化插入代码块，是没有太多吸引力的。 作为 Go 开发 IDEemacs as golang ide 这里有基本的配置。godef 安装一下可以解决函数定义的出处查找问题。没事就来一下\: C-c C-j, 立马追到底。包括 go/src/ 目录也能追杀到底。查找使用 Emacs 本身的查找 find'
tags: [Emacs]
categories:
---

[](#IDE)IDE
据我观察，很多程序员们喜欢 IDE 的原因在于工程化全局查询，函数定义, 复制粘贴， 其他的模块化插入代码块，是没有太多吸引力的。

[](#作为-Go-开发-IDE)作为 Go 开发 IDE
[emacs as golang ide](https://github.com/syl20bnr/spacemacs/tree/master/layers/%2Blang/go) 这里有基本的配置。
godef 安装一下可以解决函数定义的出处查找问题。没事就来一下: C-c C-j, 立马追到底。包括 go/src/ 目录也能追杀到底。
查找使用 Emacs 本身的查找 find-grep 命令快的不行, 老方式： Alt+x find-grep 要查询的关键字 。效果图如下：

![](/2018-11-27-ide/emacs-command.png)

从上面的效果途中可以看到很多中查找方式，如果要在当前工程目录找，可以使用 projectle-grep 这个命令。
解决了这几个问题。Emacs 用来写代码不是一般的爽。有一种上瘾的感觉。特别是 spacemacs 兼顾了 VIM 与 Emacs 两者的长处。不多说了，先让代码飞一会儿!