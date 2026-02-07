---
title: 备忘录模式
date: 2017-12-01
description: '0x00 备忘录模式定义Without violating encapsulation, capture and externalize an object’s internal state so that the object can be restored to this state later.(在不破坏封装性的前提下，捕获一个对象的内部状态，并在这个对象外保存该状态．之后可将该对象恢复到之'
tags:
categories:
---

[](#0x00-备忘录模式)0x00 备忘录模式[](#定义)定义
**Without violating encapsulation, capture and externalize an object’s internal state so that the object can be restored to this state later.(在不破坏封装性的前提下，捕获一个对象的内部状态，并在这个对象外保存该状态．之后可将该对象恢复到之前保存的状态．)**

[](#角色)角色
Originator 发起人角色, 记录当前时刻的内部状态，负责定义哪些属于备份范围的状态，负责创建和恢复备忘录数据．
Memento 备忘录角色, 负责存储　Originator 发起人对象的内部状态，在需要的时候提供发起人需要的内部状态．
Caretaker 备忘录管理员角色, 对备忘录进行管理，保存和提供备忘录.

[](#php-实例)php 实例1
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
<?php
/*
 * Memento Pattern
 */

// 发起人
class Originator {
    private $state;

    public function getState()
    {
        return $this->state;
    }

    public function setState($_state)
    {
        $this->state = $_state;
    }

    // 新建备忘录
    public function createMemento()
    {
        return new Memento($this->state);
    }

    // 备忘录恢复
    public function restoreMemento(Memento $_memento)
    {
        $this->setState($_memento->getState());
    }
}

// 备忘录角色
class Memento {
    private $state;

    public function __contruct($_state)
    {
        $this->state = $_state;
    }

    public function getState()
    {
        return $this->state;
    }

    public function setState($_state)
    {
        $this->state = $_state;
    }
}

// 备忘录管理者
class Caretaker {
    private $memento;

    public function getMemento()
    {
        return $this->memento;
    }

    public function setMemento(Memento $_memento)
    {
        $this->memento = $_memento;
    }
}

class Client {
    public static function main()
    {
        $originator = new Originator();
        $caretaker = new Caretaker();
        $caretaker->setMemento($originator->createMemento());
        $originator->restoreMemento($caretaker->getMemento());
    }
}

[](#0x01-小结)0x01 小结[](#场景)场景
需要保存和恢复数据的相关状态场景
提供一个可回滚的操作
需要监控的副本中
数据库连接的事务管理就是用的备忘录模式．

[](#注意)注意
备忘录的生命周期需要主动管理, 备忘录创建出来就要在＂最近＂的代码中使用，建立就要使用，不使用立刻删除其引用，坐等GC处理它．
不要在频繁建立备份的场景中使用备忘录模式，因为: 
控制不了备忘录创建的对象数量
大对象的创建需要消耗资源，影响系统的性能