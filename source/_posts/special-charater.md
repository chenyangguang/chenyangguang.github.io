---
title: 诡异的202d 和 202c
date: 2019-05-30
description: '诡异的 202D 和 202C你们看下面这两行有啥不一样?1select count(a.id) as count from  a left join  b on a.code = b.code left join  c on a.id = c.id where a.ctime &amp;gt;= 1559059200 and a.ctime &amp;lt; 1559145600 and a.p...'
tags: [笔记]
categories:
---

诡异的 202D 和 202C
你们看下面这两行有啥不一样?

```sql
select count(a.id) as count from  a left join  b on a.code = b.code left join  c on a.id = c.id where a.ctime >= 1559059200 and a.ctime = 1559059200 and a.ctime < 1559145600 and a.phone = 15038135711;有啥不一样两个？
```

看上去差不多吧？其实如果你真实运行，就会发现第一句末尾的15038135711会报错。
一般的IDE是傻傻分不清有啥不一样的。但是放在 vim 或者 Emacs 里面一眼就是别出来了。⚫️  哈哈。