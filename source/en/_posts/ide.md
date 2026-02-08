---
title: Emacs as golang IDE
date: 2018-11-27
description: 'IDE From my observation, many programmers like IDE because of engineering global queries, function definitions, copy-paste, other modular code block insertion, not much attraction. As Go Development IDE emacs as golang ide here has basic configuration. godef install can solve function definition source lookup. Just do it: C-c C-j, immediately trace to the end. Including go/src/ directory can trace to the end. Search uses Emacs' own find'
tags: [Emacs]
categories:
---

[](#IDE)IDE
From my observation, many programmers like IDE because of engineering global queries, function definitions, copy-paste, other modular code block insertion, not much attraction.

[](#As-Go-Development-IDE)As Go Development IDE
[emacs as golang ide](https://github.com/syl20bnr/spacemacs/tree/master/layers/%2Blang/go) here has basic configuration.
godef install can solve function definition source lookup. Just do it: C-c C-j, immediately trace to the end. Including go/src/ directory can trace to the end.
Search uses Emacs' own find-grep command, incredibly fast. Old way: Alt+x find-grep keywords to query. Effect as follows:

![](/2018-11-27-ide/emacs-command.png)

From the effect above, can see many search methods. If searching in current project directory, can use the projectle-grep command.
Solved these problems. Using Emacs to write code is not ordinary cool. There's an addictive feeling. Especially spacemacs combines strengths of both VIM and Emacs. Won't say more, let the code fly for a while!
