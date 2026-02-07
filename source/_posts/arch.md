---
title: 从 ubuntu 到 arch
date: 2018-05-19
description: '逃离 ubuntu 转投 arch起因先是 ubuntu16.04 升级到 ubuntu18.04, 结果每次开机直接进入了一个grub的　shell 界面, 系统无法启动了。第二次装了ubuntu18.04, 然后后面装了不少开发软件，再升级时，又挂了！有点来气，花了两天时间重装系统。不过，这次是换成了 arch。为啥，因为 arch 官网上介绍说它的定制性更高（更需要折腾），而且是滚动更新(W'
tags:
categories:
---

[](#逃离-ubuntu-转投-arch)逃离 ubuntu 转投 arch
起因先是 ubuntu16.04 升级到 ubuntu18.04, 结果每次开机直接进入了一个grub的　shell 界面, 系统无法启动了。第二次装了ubuntu18.04, 然后后面装了不少开发软件，再升级时，又挂了！有点来气，花了两天时间重装系统。不过，这次是换成了 arch。为啥，因为 arch 官网上介绍说它的定制性更高（更需要折腾），而且是滚动更新(What are you 弄啥咧?)。

[](#arch-系统的-u-盘安装)arch 系统的 ｕ 盘安装
记录一下，头一天的时候，我的安装方式是按照知乎某个人的推荐装的，结果好几个地方卡死了。比如联网，比如挂载。后来证明，只要熟读 arch 官网　wiki 上面的文档(武功秘籍)，基本上是不会整出一些”奇门遁甲”的啥”幺蛾子”的。前提是，一定要通读。

[](#切到-arch-的感受)切到 arch 的感受
速度比 ubuntu 快。天下武功，唯快不破。不知道是否因为 arch 的二进制包的安装方式，还是 安装的无关的依赖很少的缘故，在 arch 下面上网几乎不卡。即使看 youtube 视频也是非常流畅!
安装效率高。arch 下面 **sudo pacman -S smartgit**, 需要安装的依赖，直接选数字然后回车就好了。安装好快。而 ubuntu 下面安装 smartgit 的需要好几个步骤，比如你安装了 smartgit包，好需要相同的命令去找缺失的依赖包(javaxxxxxx)。还得说下使用 “yaourt” 去安装 **AUR** 类型的软件真的是很便利。比如 安装个 **nmap** 扫描一下主机ip和端口:

1
2
3
4
5
6
7
8
9
10
11
12
13
14
➜  blog git:(master) ✗ yaourt nmap
1 extra/nmap 7.70-2 [installed]
    Utility for network discovery and security auditing
2 community/vulscan 2.0-2
    A module which enhances nmap to a vulnerability scanner
3 blackarch/autonse 20.82a6e18-1 (blackarch blackarch-automation)
    Massive NSE (Nmap Scripting Engine) AutoSploit and AutoScanner.
4 blackarch/brutespray 116.bd65d69-2 (blackarch blackarch-automation blackarch-cracker)
...
32 aur/umit 1.0-1 (67) (0.20)
    A powerful nmap frontend.
==> Enter n° of packages to be installed (e.g., 1 2 3 or 1-3)
==> ---------------------------------------------------------
==> (这里选数字然后回车就可以了)

几乎所有需要的比较新的软件和开发工具都有了。而且都是命令行三两下就安装好了。比如 docker, vim，emacs, docker, git, smartgit, nodejs, npm, nvm, python(系统自带了), php, nginx, apache, mysql, mariadb, postgresql， virtualbox, tmux, zsh(这个好像是自带了), shadowsocks(这个好极了,就下个package, 再命令行启动一下，浏览器加个 proxy 扩展就直接翻出去了!)等, 而且这些软件几乎都是主流中非常新的版本！这个比较和我心意。

[](#小结)小结
通过 ubuntu 迁移到 arch 的过程，中间加深了对挂载，分区，以及搭建系统的很多命令的认知。
选一个就近的源，比如清华的。
没有什么是不能用一条命令解决不了的，如果不行就用两条! 
安装过程中，有犯错，比如一开始略过官方 wiki 直接参照网上某个人的推荐，东看一点，细看一点，结果这个装了一半，那个流程也是一半，都出现了一些一时令人懊恼的问题。还好最后回归官网 wiki 通读，针对具体的章节细读，才顺利解决了。
安装 arch 一定要联网。最简单是直接通过命令行的 wifi-menu 调出无线 wifi　的列表，选择自己知道密码的那个 wifi, 然后输入密码。
选一个图形界面桌面，比如 xfce, 安装。
在联网的基础上，第一要务是先翻出去。道理不用多说。其他都是水到渠成了。
从 arch 系统中 安装 blackarch 非常方便。blackarch 包含大概 1900 多个黑客武器! 强大而丰富的武器库！我去扒了一下，貌似 blackarch 还是 kali 系统的那个团队搞的!
然后，能用命令行快速解决的，就不要多花时间去选个图标了。比如一开视频，发现，播放没有声音! 装个 alsamixer　即可, 命令行里面直接调起 alsamixer, 控制音量啥的，都在里面了。弄张图吧。

![](/images/full.jpg)