---
title: 灵犀指 之 sed 妙用
date: 2019-05-20
description: '前奏今天又来了一个比之前更有意思的一个需求。 需要提取两项数据，1. 包含两层目录下面的不带后缀的文件名；2. 这些文件的修改时间。然后将这两个关联的数据插入一个表中，供后续和其他表关联查询使用。 1234find . -name &quot;*.zip&quot; -print  | xargs ls --full-time | head -n 3-rw------- 1 root root  ...'
tags: [灵犀指]
categories:
---

[](#前奏)前奏
今天又来了一个比之前更有意思的一个需求。

需要提取两项数据，1. 包含两层目录下面的不带后缀的文件名；2. 这些文件的修改时间。
然后将这两个关联的数据插入一个表中，供后续和其他表关联查询使用。

1
2
3
4
find . -name "*.zip" -print  | xargs ls --full-time | head -n 3
-rw------- 1 root root   4792 2019-02-18 09:27:47.113037320 +0800 ./5/0/02ef1fefebcef1fddf.zip
-rw------- 1 root root  11794 2019-03-19 10:04:15.777575937 +0800 ./5/0/305c3eae0cac4fcfd0.zip
-rw------- 1 root root   5813 2019-05-11 14:22:09.270733531 +0800 ./5/0/00640aa46bf544aacf.zip

如，把这三行的 2019-02-18 02ef1fefebcef1fddf 摘出来。

然后创建数据库:

1
2
3
4
5
6
7
CREATE TABLE 'tmp_code' (
    `id` int(11) unsigned NOT NULL auto_increment,
    `code` char(20) NOT NULL,
    `ctime` char(30) NOT NULL,
    PRIMARY KEY (`id`),
    KEY (`code`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

最后塞进去数据库。

[](#思路)思路
我的第一反应是： 先使用命令把
1
2
3
2019-02-18 02ef1fefebcef1fddf 
2019-03-19 305c3eae0cac4fcfd0
2019-05-11 0640aa46bf544aacfx

拿出来，然后使用我擅长的 vim 文本编辑器批量编辑。
确实也是可以实现。只需要使用 Ctrl + v 批量， 配合制作一两个宏。

[](#vim-宏拼接sql-技巧)vim 宏拼接sql 技巧
比如录制宏部分可以使用, 比如单独插入一个字段

[](#分别转化成单条插入sql-思路一)分别转化成单条插入sql(思路一)
第一行单独处理, 然后我们从第二行开始制作宏
1
2
3
4
5
6
7
8
qij
IINSERT INTO tmp_tb (code) values ('
Ctrl+[ 
A');
Ctrl+[
q    
-- 查看总行数n, 移动光标在第一行时,普通模式下执行(n-2)次回放宏：如 n = 100, 则执行时是 98@i
n-2@i

[](#或者vim批量编辑拼接成-insert-sql-思路2)或者vim批量编辑拼接成 insert sql (思路2)
  录制宏: 

1
2
3
4
5
6
q
ijI' 
Ctrl+[ 
A',
Ctrl+[
q

  查看总行数n, 移动光标在第一行时,普通模式下执行(n-1)次回放宏：如 n = 100, 则执行时是 99@i

```vim
n-1@i
```

  首行 输入 

1
2
insert into tmp_tb code values (
);

  然后把结尾的 ); 放到最后一行

[](#得高人指点-awk-和-sed-精要)得高人指点 awk 和 sed 精要
这里转而使用  awk 和 sed 实现一行搞定, 具体可以这样:

```bash
find . -name "*.zip" -print  | xargs ls --full-time | awk '{print $6,$9}' | sed -r 's#.*([0-9]{4}-[0-9]{2}-[0-9]{2}).*/(\S+)\.zip$#INSERT\ INTO\ tmp_tb\ \(ctime,code\)\ values\ (\1 \2)#' >> tmp_code.sql
```

逐一备注解释一下： 

```bash
find . -name "*.zip" -print
```

是为了 找到当前目录及子目录中所有的 .zip 结尾的文件。

“|” 是管道命令。 
紧接着将文件的更改时间打印出来  xargs ls –full-time  。 
然后，使用 [awk](https://chenyangguang.github.io/2017-04-25-awk/) [awk中介绍过](https://chenyangguang.github.io/2017-04-25-awk/) 的 awk 命令，默认空格作为分割符，将文本分离出来, $6, $9分别是空格分割的这么多列里，第六，第九列分别就是时间和文件信息的字符串。此时，时间已经拿到年月日，但是第九列却是带路径带后缀  ./5/0/02ef1fefebcef1fddf.zip 这样的字符串。
然后就到 sed 粉墨登场: 

```bash
sed -r 's#.*([0-9]{4}-[0-9]{2}-[0-9]{2}).*/(\S+)\.zip$#INSERT\ INTO\ tmp_tb\ \(ctime,code\)\ values\ (\1 \2)#'
```

sed 有一个绝妙的地方，就是可以使用像 (匹配模式) 这样的模式，匹配起来, 然后 使用 \1 , \2 这样拿到前面的匹配模式里原文的匹配的字符串，可以理解为一个变量。 单条 sed 一共可使用 9 个这样的匹配模式。

于是就可以完成这个需求了。 对于成千上万，特别是超过 vim 能承受的打开速度和编辑的文件来说，awk 和 sed 配合 其他比如 find, grep, xargs  等命令，简直是犹如神助!

最后用 
```bash
>> tmp_code.sql
```

把终端的标准输出都导入一个 tmp_code.sql 文件里面去。

数据库 
```bash
source tmp_code.sql
```

入库。收工。
人呀，只要你给机会，他什么事情都能干得出来。