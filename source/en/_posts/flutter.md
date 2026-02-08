---
title: Flutter not working in zsh
date: 2019-05-18
description: 'Flutter Taking Off Recently, every time in the zsh command line, I could only temporarily set the flutter path, or had to go to the flutter installation bin directory to enable flutter. Today I checked the official website and found out that after ~/.zshrc loads on startup, it doesn't start ~/.bash_profile. So the solution is: add a line at the end of ~/.zshrc, 1 source ~/.bash_profile But I have a question: other commands can be added through ~/.zshrc, then 1 source ~/.zshrc works fine. Strange, strange...'
tags: [Tips]
categories:
---

[](#Flutter-Taking-Off)Flutter Taking Off
Recently, every time in the zsh command line, I could only temporarily set the flutter path, or had to go to the flutter installation bin directory to enable flutter. Today I checked the official website and found out that after ~/.zshrc loads on startup, it doesn't start ~/.bash_profile.

So the solution is: add a line at the end of ~/.zshrc,

```bash
source ~/.bash_profile
```

But I have a question: other commands can be added through ~/.zshrc, then

```bash
source ~/.zshrc
```

works fine.
Strange, strange...
