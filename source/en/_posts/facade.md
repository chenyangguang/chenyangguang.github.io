---
title: Facade Pattern
date: 2017-11-30
description: '0x00 Facade Pattern Appearance Pattern. Definition Provide a unified interface to a set of interface in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use. (要求一个子系统的外部与内部的通信必须通过一个统一的对象进行．) Roles F'
tags: [Design Patterns]
categories:
---

[](#0x00-Facade-Pattern)0x00 Facade Pattern
Appearance Pattern.

[](#Definition)Definition
** Provide a unified interface to a set of interface in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use. (要求一个子系统的外部与内部的通信必须通过一个统一的对象进行．)**

[](#Roles)Roles
Facade - Facade role, knows all functions and responsibilities, delegate class.
Subsystem - Subsystem role, the subsystem doesn't know the facade class exists.

[](#Advantages)Advantages
Reduces system interdependencies

[](#Disadvantages)Disadvantages
Doesn't conform to the Open-Closed Principle.

[](#Application-Scenarios)Application Scenarios
Suitable for:

Providing an interface for the outside world to access a complex module or subsystem.
Subsystem is relatively independent.
Prevent risk diffusion from low-level personnel.

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
89
90
91
92
93
94
95
96
97
98
99
100
101
<?php

// Subsystem
class SubsystemOne {
    public function dosthFir()
    {
        echo 'subsystem class one.';
    }
}
class SubsystemTwo {
    public function dosthSec()
    {
        echo 'subsystem class two.';
    }
}
class SubsystemThr {
    public function dosthThr()
    {
        echo 'subsystem class three.';
    }
}

// Facade class
class Facade {
    private $objOne;
    private $objTwo;
    private $objThree;
    private $context;

    public function __construct()
    {
        $this->objOne = new SubsystemOne();
        $this->objTwo = new SubsystemTwo();
        $this->objThr = new SubsystemThr();
        $this->context = new Context();
    }

    public function jobFir()
    {
        $this->objOne->dosthFir();
    }
    public function jobSec()
    {
        $this->objTwo->dosthSec();
    }
    public function jobThr()
    {
        $this->context->combineJob();
    }
}

// Encapsulation class, don't directly participate in subsystem business logic
class Context {
    private $objOne;
    private $objThr;

    public function __construct()
    {
        $this->objOne = new SubsystemOne();
        $this->objThr = new SubsystemThr();
    }

    public function combineJob()
    {
        $this->objOne->doSthFir();
        $this->objThr->doSthThr();
    }
}

[](#0x01-Summary)0x01 Summary
The facade doesn't participate in subsystem business logic. The Laravel framework uses quite a few Facades.
