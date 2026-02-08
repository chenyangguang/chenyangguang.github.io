---
title: Flash Kill Scenario Summary
date: 2017-11-08
description: 'Even after seeing flash kill scenario solutions, still forget, because never actually experienced it. Must take time to summarize this scenario's response strategy. What day will need to handle this business? To prevent general bugs taking advantage during that time. 0x00 That Mountain, Those People, That Flash Kill'
tags: [Web, Computer Technology]
categories:
---

Even after seeing flash kill scenario solutions, still forget, because never actually experienced it. Must take time to summarize this scenario's response strategy. What day will need to handle this business? To prevent general bugs taking advantage during that time.

[](#0x00-That-Mountain,-Those-People,-That-Flash-Kill)0x00 That Mountain, Those People, That Flash Kill

Flash kill scenarios usually occur on event days, holiday promotions, "Double Eleven", Spring Festival train ticket抢购 etc. At this time, usually月黑风高, bugs easily take advantage of chaos.

Before flash kill starts, first enjoy a segment of <<Drawing Sword>> Li Yunlong attacking the county seat scene. When Japanese army from all directions reinforced平安县, Ding Wei's sector's blocking method was very clever:

At first didn't understand what the reinforcing enemies were doing, Ding Wei's strategy was: "First line troops let enemy cavalry pass,全力阻击 enemy infantry, second line troops must intercept enemy cavalry at the second crossing." Then discovered enemies不顾一切 rushing toward county seat, he understood, this troop was under死命令 rushing to county seat! If hard resistance, definitely heavy casualties, but couldn't withdraw troops, let enemy pass through defense sector. Highlight came, issued four orders:

Mobilize local armed forces and militia, bury mines along highway and both sides, high density;
Send small units, occupy highway's passes and high points,节节抗击. Slow enemy's attack edge;
Destroy all bridges in defense sector;
Front line troops withdraw from positions, open road, let enemies in. Use麻雀战, harass enemies.

"Principle is only one, at all costs阻敌增援."

Isn't this a vivid flash kill scene! People placing orders are the "Japanese army",不顾死活狂点狂刷 remaining inventory, submit forms, rush to "county seat (database)"! Buy! Buy! Buy! But you say my website can let you easily pass through my "defense sector"? So how to design and optimize my defense sector's blocking ability?

[](#Scene-Characteristics)Scene Characteristics
Large number of users initiate attacks at same time, causing instantaneous high traffic.
Access volume far exceeds inventory quantity.
Business process is placing orders and reducing inventory.

[](#Targeted-Architecture)Targeted Architecture
Flash Kill Page -> Server Site -> Service Layer -> Database Layer

Flash Kill Page
Staticize, in flash kill page, must make page static, except necessary static elements, all staticize, combine CDN to resist access to static page elements.
Forbid users from repeated submission, after submission button becomes unclickable or grayed out.
User flow limiting, same IP user only allows submitting one order within certain time.
CAPTCHA filling recognition.

Server Site:
Limit access frequency for a UID user within certain time.
Use message queue to cache requests, batch read, merge multiple request queries together, reduce database access次数.
redis cache query results, especially inventory quantity.

Service Layer
分时分段分批次 release tickets, "cavalry", "infantry" echelon release processing.
Order placement module (flash kill's core part), queue control asynchronous, make request queue, judge whether queue is full, if not full, put request in queue; if full, later requests return flash kill failure. Anyway, only let limited "troops" (requests) pass through per unit time to "county seat" (database).
Order placement, asynchronous payment.

[](#Key-Points)Key Points
Business separation, independent concurrent access.
High concurrency control, request volume interception.
Read-write separation (query and order placement separated independently).
Request queue control acceptance number, control concurrency.
Order and payment maintain consistency.

[](#0x01-Let-the-Storm-Come-More-Fiercely)0x01 Let the Storm Come More Fiercely
Key point is layer-by-layer blocking, block traffic pressure upstream. Reduce number of reinforcing troops (write operations) reaching the database.
Time left for Chinese team is running out, oh no, time left for bugs to reach database is running out... oh wrong, time left for reinforcing "enemy army" (write operations) to reach database is running out...

[](#0x02-References)0x02 References
[Flash Kill System Architecture Optimization Road. 58 Shen Jian](https://mp.weixin.qq.com/s?sn=fb28fd5e5f0895ddb167406d8a735548&__biz=MjM5ODYxMDA5OQ==&mid=2651959391&idx=1&scene=21&pass_ticket=5a1eixuRcaxaEfBB3VPh7z%2BRHowhFEJSqSWxYJTsomcQQ1yIU7LMGpQxjDey9Xgj)
[How to Design a Flash Kill System](http://blog.csdn.net/suifeng3051/article/details/52607544)
[Web System Large-Scale Concurrency – E-commerce Flash Kill and Panic Buying. Xu Hanbin](http://www.csdn.net/article/2014-11-28/2822858)
