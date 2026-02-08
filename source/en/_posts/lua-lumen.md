---
title: lua
date: 2018-04-26
description: 'Lua Introduction Recently wanted to spend a few days systematically learning Lua because while reading "Redis in Action" I found Lua can match with redis to produce stacked performance. nginx+Lua+redis combination can further enhance redis's power. Tutorial Lua is a powerful, open-source, lightweight, embedded scripting language written in standard C. Provides procedural, object-oriented, functional, data-driven programming methods. Design Purpose Embed into applications, provide'
tags: [Lua]
categories:
---

[](#Lua-Introduction)Lua Introduction
Recently wanted to spend a few days systematically learning Lua because while reading "Redis in Action" I found Lua can match with redis to produce stacked performance. nginx+Lua+redis combination can further enhance redis's power.

[](#Tutorial)Tutorial
Lua is a powerful, open-source, lightweight, embedded scripting language written in standard C. Provides procedural, object-oriented, functional, data-driven programming methods.

[](#Design-Purpose)Design Purpose
Embed into applications, provide flexible extension and customization features for applications.

[](#Features)Features
Lightweight: Written in standard C and open source in source form, after compilation only 100+ k, very convenient to embed into other programs.
Extensible: Lua provides very easy-to-use extension interfaces and mechanisms: provided by host (usually C or C++) these functions, use like built-in functions.
Other features: Automatic memory management; provides a general type table (**table**), used to implement arrays, hash tables, sets, objects; language built-in pattern matching; closures (**closure**); functions can also be viewed as values; provides multithreading, etc.

[](#Application-Scenarios)Application Scenarios
Game development
Independent application scripts
Web application scripts
Extensions and database plugins: MySQL Proxy and MySQL WorkBench
Security systems, like intrusion detection systems

[](#Installation)Installation  1
2
3
4
5
6
cd ~
curl -R -O http://www.lua.org/ftp/lua-5.3.0.tar.gz
tar zxf lua-5.3.0.tar.gz
cd lua-5.3.0
make linux test
make install

[](#Getting-Started)Getting Started1
2
3
4
5
➜  ~ lua -i
Lua 5.2.3  Copyright (C) 1994-2013 Lua.org, PUC-Rio
> print("Hello Lua!")
Hello Lua!
>

There's no command like **exit** to exit! Just Ctrl + c, heh.

[](#First-Blood-Demo)First Blood Demo!1
2
3
4
5
➜ touch first-blood.lua
➜ lua echo 'print("hello world lua!")' > first-blood.lua
echo print("hello world lua") > first-blood.lua
➜  lua lua first-blood.lua
hello world lua!

[](#Two-Comment-Styles)Two Comment Styles1
2
3
4
5
-- single line commentary for lua
--[[
print('multiple')
print('commentary')
]]--

[](#Eight-Data-Types)Eight Data Types
nil
boolean
number, double-precision floating-point real numbers
string
userdata, represents any C data structure stored in variables
function, functions written in C or Lua
thread, represents independent execution lines, used for executing coroutines
table, Lua's table, actually an **associative array**, array indices can be numbers or strings. Use **{}** to construct and create.

[](#Basics)Basics
**Numbers**, **letters**, and **underscores** form valid variables, **case-sensitive**.
Default variables are all global, use **local** to explicitly declare local variables. No need to declare before use, default value is **nil**, to delete a variable directly set that variable value to **nil**.
String concatenation uses **..**.
**#** calculates string length.
Indexing starts from **1**!
**table** length is not fixed, when adding new data length automatically grows. Uninitialized values are **nil**.
**Thread** VS **Coroutine**: Threads can run multiple simultaneously, coroutines can only run one at any time, and only running coroutines will pause when **suspend**ed.
Table indices can use **[i]** or **.** operation, like: table1["fix"], table.fix.
**^** and **..** are right-associative, other operators are left-associative.

[](#Loop-Control)Loop Control
for loop
while
repeat … until
break, jump out of current loop statement, and execute the statement immediately following the script.

[](#Functions)Functions
Lua functions can **return** multiple result values.
Lua functions can use **…** in the parameter list as variable arguments.
Functions can be passed as parameters to functions, a bit like in **Lisp**.

[](#Operations)Operations
Besides addition, subtraction, multiplication, division, remainder, special operator symbol **^** power;
Relational operator symbols **~=** means not equal;
Logical operator symbol trio: and, or, not;
**..** connects, **#** unary operator, returns string or table length (pirnt(#'abc')).

Operator precedence ranking:

1
2
3
4
5
6
7
8
^
not - (unary)
* /
+ -
..
< > <= >= ~= ==
and
or

[](#References)References
[Lua Official Website](https://www.Lua.org/)
[Lua Basic Online Tutorial](http://www.runoob.com/Lua/Lua-tutorial.html)
[github source code](https://github.com/lua/lua)
[Lua wiki tools](http://lua-users.org/wiki/)
