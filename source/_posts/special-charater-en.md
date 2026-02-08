---
lang: en
title: Weird 202D and 202C
date: 2019-05-30
description: 'Weird 202D and 202C Look at these two lines below, what\'s different? 1select count(a.id) as count from a left join b on a.code = b.code left join c on a.id = c.id where a.ctime >= 1559059200 and a.ctime...'
tags: [Notes]
categories:
---

Weird 202D and 202C
Look at these two lines below, what's different?

```sql
select count(a.id) as count from  a left join  b on a.code = b.code left join  c on a.id = c.id where a.ctime >= 1559059200 and a.ctime = 1559059200 and a.ctime < 1559145600 and a.phone = 15038135711;有啥不一样两个？
```

Look similar? Actually if you run them, you'll find the first line's ending 15038135711 will error.
Normal IDEs stupidly can't tell the difference. But put in vim or Emacs and spot it immediately. ⚫️ Haha.
