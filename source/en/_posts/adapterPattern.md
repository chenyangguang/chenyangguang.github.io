---
title: Design Pattern - Adapter Pattern
date: 2017-11-26
description: '0x00 Adapter Pattern The Adapter pattern, also called the Transformer pattern, Wrapper pattern. The Decorator pattern is also a type of Wrapper pattern. High-voltage current used during power transmission cannot be directly used when transported to households thousands of miles away, otherwise it would directly burn out appliances. This requires voltage reduction, using an adapter to convert high-voltage current into 220v (China) current suitable for household appliances. Definition Convert the interface of a class into another interf'
tags: [Design Patterns]
categories:
---

[](#0x00-Adapter-Pattern)0x00 Adapter Pattern
The Adapter pattern, also called the Transformer pattern, Wrapper pattern. The Decorator pattern is also a type of Wrapper pattern. High-voltage current used during power transmission cannot be directly used when transported to households thousands of miles away, otherwise it would directly burn out appliances. This requires voltage reduction, using an adapter to convert high-voltage current into 220v (China) current suitable for household appliances.

[](#Definition)Definition
**Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.** (将一个类的接口变换成客户端所期待的另一种接口，从而使原本因接口不匹配而无法在一起工作的两个类能够在一起工作。)

[](#Roles)Roles
Target - Target role, the target interface expected to be provided finally. Exists.
Adaptee - Source role, the interface that needs to be transformed. Exists.
Adapter - Adapter role, the core role.

[](#Advantages)Advantages
Enables two completely unrelated classes to work together.
Increases class transparency.
Improves class reusability.
Flexible.

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
<?php
interface Target {
    public function job();
}

class ConcreteTarget implements Target {
    public function job() {
        echo '220 v current can be used normally' . PHP_EOL;
    }
}

class Adaptee {
    public function doSth() {
        echo '25000 V high-voltage current can also be used' . PHP_EOL;
    }
}

class Adapter extends Adaptee implements Target {
    public function job() {
        parent::doSth();
    }
}

class Client {
    public static function main() {
        $target  = new ConcreteTarget();
        $target->job();
        $target2 = new Adapter();
        $target2->job();
    }
}
(new Client())::main();
// 220 v current can be used normally
// 25000 V high-voltage current can also be used

[](#0x01-Summary)0x01 Summary
