---
lang: en
title: Design Pattern - Strategy Pattern
date: 2017-11-24
description: '0x00 Strategy Pattern Strategy pattern, also called policy pattern, uses object-oriented inheritance and polymorphism mechanisms. Definition Define a family of algorithms, encapsulate each one, and make them interchangeable. (定义一组算法，将每个算法都封装起来，并且使它们之间可以交换。)'
tags: [Design Patterns]
categories:
---

[](#0x00-Strategy-Pattern)0x00 Strategy Pattern
Strategy pattern, also called policy pattern, uses object-oriented inheritance and polymorphism mechanisms.

[](#Definition)Definition
**Define a family of algorithms, encapsulate each one, and make them interchangeable**. (定义一组算法，将每个算法都封装起来，并且使它们之间可以交换。)

[](#Three-Role-Composition)Three Role Composition
Context - Encapsulation role, also called context role, plays bridging encapsulation role shielding high-level modules from direct access to strategies and algorithms, encapsulating possible changes.
Strategy - Abstract strategy role, abstraction of strategy and algorithm family, usually an interface, defining methods and properties that each strategy or algorithm must have.
ConcreteStrategy - Specific strategy role, implements operations in abstract strategy, contains specific algorithms.

[](#Advantages)Advantages
Algorithms can be freely switched
As long as abstract strategy is implemented, becomes a member of strategy family, through encapsulation role to encapsulate it, ensuring "freely switchable" strategy provided externally.
Avoid using multiple conditional judgments
External access interface provided by strategy family is the encapsulation class, simplifies operations, avoids conditional statement judgments.
Easy to extend

[](#Disadvantages)Disadvantages
Number of strategy classes increases
Each strategy is a class, low possibility of reuse, number of classes continuously increases.
All strategy classes need to be exposed externally
Upper-level modules must know what strategies exist to further decide which one to use.

[](#Use-Cases)Use Cases
Scenarios where multiple classes differ only slightly in algorithms or behavior.
Scenarios where algorithms need free switching.
Scenarios where algorithm rules need to be shielded.

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
86
87
88
<?php

// Abstract strategy interface
interface Strategy {
    public function doSth();
}

// Specific strategy role
class ConcreteStrategy1 implements Strategy {
    public function doSth()
    {
        echo 'strategy 1';
    }
}

class ConcreteStrategy2 implements Strategy {
    public function doSth()
    {
        echo 'strategy 2';
    }
}

// Encapsulation role
class Context {
    private $strategy = null;
    public function Context(Strategy $_strategy)
    {
        $this->strategy = $_strategy;
    }

    public function doAct()
    {
        $this->strategy->doSth();
    }
}

// Scenario class
class Client {
    public static function main()
    {
        $strategy = new ConcreteStrategy1();
        $context = new Context($strategy);
        $context->doAct();
    }
}

// Call
(new Client())::main(); // output: strategy 1

[](#0x01-Summary)0x01 Summary
Similar to scenarios providing upper, middle, lower countermeasure selections, using strategy pattern is best.
