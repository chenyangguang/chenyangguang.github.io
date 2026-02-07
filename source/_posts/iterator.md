---
title: 设计模式-迭代器模式
date: 2017-11-27
description: '0x00 迭代器模式迭代器类似于一个数据库中(MySQL的游标是单向的)的游标，可以在一个容器内翻滚，遍历所有的查看的元素. 定义Provide a way to access the elements of an arrgegate object sequentially without exposing its underlying representation.(它提供一种方法访问容器对象中'
tags:
categories:
---

[](#0x00-迭代器模式)0x00 迭代器模式
迭代器类似于一个数据库中(MySQL的游标是单向的)的游标，可以在一个容器内翻滚，遍历所有的查看的元素.

[](#定义)定义
**Provide a way to access the elements of an arrgegate object sequentially without exposing its underlying representation.**(它提供一种方法访问容器对象中的各个元素，而又不需暴露对象的内部细节．)

[](#角色)角色
Iterator 抽象迭代器, 定义和遍历元素的接口, 一般有固定的三个方法: first(), next(), hasNext().
ConcreteIterator 具体迭代器, 具体实现迭代器接口．
Aggregate 抽象容器, 提供创建具体迭代器角色的接口．
ConcreteAggregate 具体容器, 创建迭代器的对象．

[](#php实现)php实现1
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
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
<?php
/*
 * Iterator Pattern
 */
interface IIterator {
    public function next();
    public function hasNext();
    public function remove();
}

class ConcreteIterator implements IIterator {
    private $arr = [];
    public $cursor = 0;

    public function __construct($_arr)
    {
        $this->arr = $_arr;
    }

    public function hasNext()
    {
        return $this->cursor == count($this->arr) ? false : true;
    }

    public function next()
    {
        $result = null;
        if($this->hasNext()) {
            return ($this->arr)[$this->cursor++];
        }
        return $result;
    }

    // 开发系统时，如果用到迭代器的删除方法，应该完成两个功能: 1. 删除当前元素, 2. 当前游标指向下一个元素．
    public function remove()
    {
        $this->cursor = null;
        return true;
    }
}

interface Aggregate {
    public function add($obj);
    public function remove($obj);
    public function iterator();
}

class ConcreteAggregate implements Aggregate {
    private $arr = [];

    public function add($obj)
    {
        $this->arr[] = $obj;
    }

    public function iterator()
    {
        return new ConcreteIterator($this->arr);
    }

    public function remove($obj)
    {
        $this->remove($obj);
    }
}

class Client {
    public static function main()
    {
        $agg = new ConcreteAggregate();
        $agg->add('test');
        $agg->add('hello');
        $agg->add('world');
        $iterator = $agg->iterator();
        while ($iterator->hasNext()) {
            echo $iterator->next(), PHP_EOL;
        }
    }
}
(new Client())::main();
/*
test
hello
world
*/

[](#php-中自有的-Iterator-接口)php 中自有的 Iterator 接口
[php 原生迭代器](http://php.net/manual/en/spl.iterators.php).

1
2
3
4
5
6
7
8
Iterator extends Traversable {
/* 方法 */
abstract public mixed current ( void )
abstract public scalar key ( void )
abstract public void next ( void )
abstract public void rewind ( void )
abstract public boolean valid ( void )
}

提供了好几个方法.

[](#0x01-小结)0x01 小结
渐渐能摸着一些门道了．