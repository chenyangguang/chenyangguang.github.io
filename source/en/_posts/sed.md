---
title: Tips - Clever Uses of sed
date: 2019-05-20
description: 'Prelude Today came another more interesting requirement than before. Need to extract two items of data: 1. Filename without extension under two directories; 2. Modification time of these files. Then insert these two associated data into a table for subsequent related queries with other tables. 1234find . -name "*.zip" -print | xargs ls --full-time | head -n 3-rw------- 1 root root ...'
tags: [Tips]
categories:
---

[](#Prelude)Prelude
Today came another more interesting requirement than before.

Need to extract two items of data: 1. Filename without extension under two directories; 2. Modification time of these files. Then insert these two associated data into a table for subsequent related queries with other tables.

1
2
3
4
find . -name "*.zip" -print  | xargs ls --full-time | head -n 3
-rw------- 1 root root   4792 2019-02-18 09:27:47.113037320 +0800 ./5/0/02ef1fefebcef1fddf.zip
-rw------- 1 root root  11794 2019-03-19 10:04:15.777575937 +0800 ./5/0/305c3eae0cac4fcfd0.zip
-rw------- 1 root root   5813 2019-05-11 14:22:09.270733531 +0800 ./5/0/00640aa46bf544aacf.zip

For example, extract the 2019-02-18 02ef1fefebcef1fddf from these three lines.

Then create database:

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

Finally insert into database.

[](#Idea)Idea
My first reaction was: First use command to get

1
2
3
4
5
2019-02-18 02ef1fefebcef1fddf
2019-03-19 305c3eae0cac4fcfd0
2019-05-11 0640aa46bf544aacfx

out, then use my skilled vim text editor for batch editing.
Indeed can be implemented. Just need to use Ctrl + v batch, combined with making one or two macros.

[](#vim-Macro-Splicing-sql-Technique)vim Macro Splicing sql Technique
For recording macro part can use, like inserting a single field separately

[](#Convert-to-Single-Insert-sql-Respectively-Idea-1)Convert to Single Insert sql Respectively (Idea 1)
Handle first line separately, then we start making macro from second line
1
2
3
4
5
6
7
8
9
qij
IINSERT INTO tmp_tb (code) values ('
Ctrl+[
A');
Ctrl+[
q
-- View total lines n, when cursor on first line, execute (n-2) macro replays in normal mode: if n = 100, execute 98@i
n-2@i

[](#Or-vim-Batch-Edit-Splice-Into-insert-sql-Idea2)Or vim Batch Edit Splice Into insert sql (Idea 2)
Record macro:

1
2
3
4
5
6
7
8
9
q
ijI'
Ctrl+[
A',
Ctrl+[
q

View total lines n, when cursor on first line, execute (n-1) macro replays in normal mode: if n = 100, execute 99@i

```vim
n-1@i
```

First line input

1
2
insert into tmp_tb code values (
);

Then put the ending ); on the last line

[](#Guided-by-Expert-awk-and-sed-Essence)Guided by Expert awk and sed Essence
Here instead use awk and sed to handle it in one line, specifically like this:

```bash
find . -name "*.zip" -print  | xargs ls --full-time | awk '{print $6,$9}' | sed -r 's#.*([0-9]{4}-[0-9]{2}-[0-9]{2}).*/(\S+)\.zip$#INSERT\ INTO\ tmp_tb\ \(ctime,code\)\ values\ (\1 \2)#' >> tmp_code.sql
```

Explanation one by one:

```bash
find . -name "*.zip" -print
```

Is to find all files ending with .zip in current directory and subdirectories.

"|" is the pipe command.
Then print out file modification times xargs ls –full-time.
Then, use [awk](https://chenyangguang.github.io/2017-04-25-awk/) [introduced in awk](https://chenyangguang.github.io/2017-04-25-awk/) command, defaulting space as separator, separating text, $6, $9 are sixth and ninth columns among space-separated many columns, respectively time and file information strings. At this point, time has year month day, but ninth column is with path and extension ./5/0/02ef1fefebcef1fddf.zip such string.

Then sed takes the stage:

```bash
sed -r 's#.*([0-9]{4}-[0-9]{2}-[0-9]{2}).*/(\S+)\.zip$#INSERT\ INTO\ tmp_tb\ \(ctime,code\)\ values\ (\1 \2)#'
```

sed has a wonderful feature, can use pattern like (match pattern), match it, then use \1, \2 to get the matched strings from earlier match patterns, can be understood as a variable. Single sed can use up to 9 such match patterns.

Thus can complete this requirement. For thousands or tens of thousands, especially files exceeding vim's opening speed and editing capability, awk and sed combined with other commands like find, grep, xargs etc., simply like divine help!

Finally use
```bash
>> tmp_code.sql
```

To import all terminal standard output into a tmp_code.sql file.

Database
```bash
source tmp_code.sql
```

Import into database. Done.
People, as long as you give them a chance, they can do anything.

