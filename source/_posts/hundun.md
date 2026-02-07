---
title: 混沌？馄炖?
date: 2018-11-28
description: '闲来没事，看了下 gocolly，练手搞一个爬虫，搂了一遍最新的腾讯官网的招聘信息。这种不需要登陆的网站是最容易爬到的。很简单，还是给自己小结过一下。 因为无须登陆，所以这条虫子几乎是官网的基础的例子使用 Chrome 浏览器打开腾讯招聘官网,  F12, 随便在搜索框里面输入一点比如 go, 就进入一个分页的搜索结果列表页。定位到招聘的职位那几栏，发现是用的 table 框起来的。找官网的基本例'
tags:
categories:
---

闲来没事，看了下 [gocolly](https://github.com/gocolly/colly)，练手搞一个爬虫，搂了一遍最新的腾讯官网的招聘信息。
这种不需要登陆的网站是最容易爬到的。
很简单，还是给自己小结过一下。

因为无须登陆，所以这条虫子几乎是官网的基础的例子
使用 Chrome 浏览器打开[腾讯招聘官网](https://hr.tencent.com),  F12, 随便在搜索框里面输入一点比如 go, 就进入一个分页的搜索结果列表页。定位到招聘的职位那几栏，发现是用的 table 框起来的。找官网的基本例子依样画葫芦。

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
c.OnHTML("#position tbody tr", func(e *colly.HTMLElement) {
       writer.Write([]string{
           e.ChildText("td:nth-child(1)"),
           e.ChildText("td:nth-child(2)"),
           e.ChildText("td:nth-child(3)"),
           e.ChildText("td:nth-child(4)"),
           e.ChildText("td:nth-child(5)"),
           e.ChildAttr("a", "href"),
       })
})

结果爬取的结果除了想要的那些 tr 行之外，表头和地步的分页的数据也给弄进去了。
这不是我想要的，决定过滤一下。于是改进一下小版本的只搂需要的选项。

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
c.OnHTML("#position tbody tr", func(e *colly.HTMLElement) {
	itemClass := e.Attr("class")
	if strings.EqualFold(itemClass, "even") || strings.EqualFold(itemClass, "odd") {
		writer.Write([]string{
			e.ChildText("td:nth-child(1)"),
			e.ChildText("td:nth-child(2)"),
			e.ChildText("td:nth-child(3)"),
			e.ChildText("td:nth-child(4)"),
			e.ChildText("td:nth-child(5)"),
			e.ChildAttr("a", "href"),
		})
	}
})

只爬一页不够啊，我需要全部的招聘信息，然后再加一下获取下一页的链接。让它爬完一页之后接着下一页，直到爬完所有的招聘。

1
2
3
4
5
c.OnHTML("#next", func(h *colly.HTMLElement) {
	t := donain + h.Attr("href")
	log.Printf(t)
	c.Visit(t)
})

这样一来就拿到腾讯官网全量的数据了。
还是向 shawjia 学习，多提交一些自己的开源项目, 哪怕是最基本的练手的项目。
今天是个开始，这顿 [馄炖](https://github.com/chenyangguang/hundun) 就是个见证。(一直不知道开始的项目应该叫啥名，索性就处在混沌之中吧。)