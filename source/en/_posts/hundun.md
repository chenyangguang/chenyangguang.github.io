---
title: Chaos? Wonton?
date: 2018-11-28
description: 'Bored, looked at gocolly, practicing made a web scraper, scraped the latest Tencent official recruitment information. Websites that don't require login are the easiest to scrape. Very simple, still let me summarize. Because no login needed, this crawler is basically the official website basic example. Use Chrome browser to open Tencent recruitment official website, F12, casually input something like go in the search box, enter a paginated search result list page. Locate the recruitment position columns, found they are framed with table. Find the official website basic example and copy it.'
tags: [Go, Code]
categories:
---

Bored, looked at [gocolly](https://github.com/gocolly/colly), practicing made a web scraper, scraped the latest Tencent official recruitment information.
Websites that don't require login are the easiest to scrape.
Very simple, still let me summarize.

Because no login needed, this crawler is basically the official website basic example
Use Chrome browser to open [Tencent recruitment official website](https://hr.tencent.com), F12, casually input something like go in the search box, enter a paginated search result list page. Locate the recruitment position columns, found they are framed with table. Find the official website basic example and copy it.

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

The scraped result besides the wanted tr rows, also brought in the header and footer pagination data.
This isn't what I wanted, decided to filter. So improved the small version to only scrape the needed options.

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

Only scraping one page isn't enough, I need all recruitment information, then also add getting the next page link. Let it crawl one page then continue to the next page, until all recruitment is crawled.

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

This way got all Tencent official website data.
Still learn from shawjia, submit more of my open source projects, even the most basic practice projects.
Today is a beginning, this [wonton](https://github.com/chenyangguang/hundun) is a witness. (Never knew what to name starting projects, simply stay in chaos.)
