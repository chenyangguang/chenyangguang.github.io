---
title: From Ubuntu to Arch
date: 2018-05-19
description: 'Escaping Ubuntu to Arch Cause First, Ubuntu 16.04 was upgraded to Ubuntu 18.04, and every time it started, it went directly to a grub shell interface, and the system couldn't start. The second time I installed Ubuntu 18.04, then installed a lot of development software, and when upgrading again, it crashed again! I was a bit angry, spent two days reinstalling the system. But this time I switched to Arch. Why? Because the Arch website says it has higher customizability (needs more tinkering), and it has rolling updates (What are you doing?).'
tags: [Arch]
categories:
---

[](#Escaping-Ubuntu-to-Arch)Escaping Ubuntu to Arch
Cause First, Ubuntu 16.04 was upgraded to Ubuntu 18.04, and every time it started, it went directly to a grub shell interface, and the system couldn't start. The second time I installed Ubuntu 18.04, then installed a lot of development software, and when upgrading again, it crashed again! I was a bit angry, spent two days reinstalling the system. But this time I switched to Arch. Why? Because the Arch website says it has higher customizability (needs more tinkering), and it has rolling updates (What are you doing?).

[](#Arch-System-USB-Installation)Arch System USB Installation
Let me record this. The first day, my installation method was according to some person's recommendation on Zhihu, and I got stuck in several places. For example, networking, for example, mounting. Later it proved that as long as you carefully read the documents on the Arch official wiki (martial arts secrets), you basically won't create any "weird tricks." The premise is, you must read it through.

[](#Feelings-of-Switching-to-Arch)Feelings of Switching to Arch
Speed is faster than Ubuntu. In all martial arts, only speed is unbreakable. I don't know if it's because of Arch's binary package installation method, or because there are very few unrelated dependencies installed. Under Arch, surfing the internet almost never lags. Even watching YouTube videos is very smooth!

High installation efficiency. Under Arch, **sudo pacman -S smartgit**, just select the number and press enter to install the dependencies. Installation is so fast. Under Ubuntu, installing smartgit requires several steps. For example, if you install the smartgit package, you need to use the same command to find the missing dependency packages (javaxxxxxx). I also have to mention that using "yaourt" to install **AUR** type software is really convenient. For example, installing **nmap** to scan host IPs and ports:

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
==> (Here select the number and press enter)

Almost all the relatively new software and development tools needed are there. And they're all installed with just two or three command-line commands. For example, docker, vim, emacs, docker, git, smartgit, nodejs, npm, nvm, python (comes with the system), php, nginx, apache, mysql, mariadb, postgresql, virtualbox, tmux, zsh (seems to come with it), shadowsocks (this is excellent, just download the package, start it from the command line, add a proxy extension to the browser and you're out!), etc. And these software are almost all very new versions in the mainstream! This suits my taste.

[](#Summary)Summary
Through the process of migrating from Ubuntu to Arch, I deepened my understanding of mounting, partitioning, and many commands for building systems.
Choose a nearby source, like Tsinghua's.
There's nothing that can't be solved with one command; if that doesn't work, use two!
During installation, I made mistakes. For example, at first I skipped the official wiki and directly followed someone's online recommendation, reading a bit here, a bit there. As a result, this installation was half done, that process was half done, and some annoying problems appeared for a while. Fortunately, in the end, I returned to the official wiki, read it through, and read specific chapters carefully, and solved everything smoothly.
Installing Arch definitely requires internet connection. The simplest way is to directly use the command line wifi-menu to bring up the list of wireless Wi-Fi, select the Wi-Fi you know the password for, then enter the password.
Choose a graphical desktop interface, like xfce, and install it.
Once connected to the internet, the first priority is to get out. No need to explain why. Everything else follows naturally.
Installing blackarch from an Arch system is very convenient. blackarch contains about 1900+ hacker weapons! A powerful and rich arsenal! I checked it out, and it seems blackarch is made by the same team as the kali system!
Then, if you can solve it quickly with command line, don't spend time choosing icons. For example, when playing a video, I found there was no sound in playback! Just install alsamixer. In the command line, directly start alsamixer, and everything for controlling volume is there. Let me post a picture.

![](/images/full.jpg)
