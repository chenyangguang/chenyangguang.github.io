---
lang: en
title: Design Pattern - Abstract Factory Pattern
date: 2017-10-24
description: '0x00 Abstract Factory Pattern Definition Provide an interface for creating families of related or dependent objects without specifying their concrete classes (为创建一组相关或相互依赖的对象提供一个接口, 而且无须指定它们的具体类。) The general class diagram for the Abstract Factory pattern:'
tags: [Design Patterns]
categories:
---

[](#0x00-Abstract-Factory-Pattern)0x00 Abstract Factory Pattern[](#Definition)Definition
Provide an interface for creating families of related or dependent objects without specifying their concrete classes
(为创建一组相关或相互依赖的对象提供一个接口, 而且无须指定它们的具体类。)

The general class diagram for the Abstract Factory pattern:

![](/2017-10-24-TheZenOfDesignPatternAbstractFactory/photos/abstract-factory.png)

![](/2017-10-24-TheZenOfDesignPatternAbstractFactory/photos/abstract-factory-source.png)

[](#Difference-from-Factory-Method-Pattern)Difference from Factory Method Pattern
Sub-factories must all inherit from or implement the same abstract class or interface.
Each factory must contain multiple factory methods.
Each factory's methods must be consistent.

[](#Advantages)Advantages
Encapsulation - The implementation class of each product is not something the high-level module needs to care about. It only cares about interfaces and abstractions, not how objects are created. As long as you know which factory class it is, you can create a needed object.
Constraints within product families are non-public and implemented within factories.

[](#Disadvantages)Disadvantages
Product family expansion is very difficult. Need to modify both abstract classes and implementation classes simultaneously.

[](#Use-Cases)Use Cases
When an object family has the same constraints, the Abstract Factory pattern can be used. For example, PHP running on Linux and Windows looks the same, meaning it has the same constraint: operating system type. Then you can use the Abstract Factory pattern to produce PHP installation paths under different operating systems.

[](#PHP-Implementation)PHP Implementation1
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
<?php

abstract class population {}
abstract class income {}

class ShenzhenPopulation {}
class ShenzhenIncome {}
class BeijingPopulation {}
class BeijingIncome {}

interface NationalStatisticsAbstractFactory {
    public function statisticsPopulation();
    public function statisticsIncome();
}

class ShenzhenFactory implements NationalStatisticsAbstractFactory {
    public function statisticsPopulation() {
        return new ShenzhenPopulation();
    }

    public function statisticsIncome() {
        return new ShenzhenIncome();
    }
}

class BeijingFactory implements NationalStatisticsAbstractFactory {
    public function statisticsPopulation (){
        return new BeijingPopulation();
    }

    public function statisticsIncome () {
        return new BeijingIncome();
    }
}

Both the Shenzhen and Beijing factory classes (ShenzhenFactory, BeijingFactory) inherit from the National Statistics Abstract Interface (NationalStatisticsAbstractFactory). ShenzhenFactory and BeijingFactory each contain methods for statisticsIncome (statistics income) and statisticsPopulation (statistics population).

[](#0x01-Summary)0x01 Summary
Design patterns need to be savored slowly and are worth spending time researching.
