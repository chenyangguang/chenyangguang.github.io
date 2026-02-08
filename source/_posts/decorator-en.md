---
lang: en
title: Design Pattern - Decorator Pattern
date: 2017-11-23
description: '0x00 Decorator Pattern Definition Attach additional responsibilities to an object dynamically keeping the same interface. Decorators provide a flexible alternative to subclassing for extending functionality. (动态地给一个对象添加一些额外的职责。就增加功能来说，装饰模式相比生成子类更为灵活。) **'
tags: [Design Patterns]
categories:
---

[](#0x00-Decorator-Pattern)0x00 Decorator Pattern[](#Definition)Definition
**Attach additional responsibilities to an object dynamically keeping the same interface. Decorators provide a flexible alternative to subclassing for extending functionality. (动态地给一个对象添加一些额外的职责。就增加功能来说，装饰模式相比生成子类更为灵活。) **

[](#Four-General-Class-Roles)Four General Class Roles
Component - Abstract component, serving as the core, most primitive object interface or abstract class.
ConcreteComponent - Concrete component, implementation of the interface or abstract class.
Decorator - Decorator role, in properties must have a private variable pointing to the Component abstract component.
ConcreteDecorator - Specific decorator role

[](#Advantages)Advantages
Decorator class and decorated class can develop independently without coupling to each other. The Component class doesn't need to know about the Decorator class. The Decorator class extends the Component class's functionality from the outside, and the Decorator doesn't need to know the specific component.
The Decorator pattern is an alternative to inheritance relationships.
Dynamically extend the functionality of an implementation class.

[](#Disadvantages)Disadvantages
Multi-layer complex decoration, when the number increases, will increase system complexity, while bringing time and difficulty to troubleshooting.

[](#PHP-Example)PHP Example1
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

<?php
/*
 * decorator pattern
 */

abstract class Component {
    abstract function doSth();
}

class ConcreteComponent extends Component {
    public function doSth() {
        echo 'concrete component';
    }
}

// Abstract decorator class
abstract class Decorator extends Component {
    private $component = null;
    public function Decorator(Component $_component) {
        $this->component = $_component;
    }

    public function doSth()
    {
        $this->component->doSth();
    }
}

// Concrete decorator class
class ConcreteDecorator1 extends Decorator {
    public function ConcreteDecorator1(Component $_component) {
        parent::__construct($_component);
    }

    private function deco1() {
        echo 'decorator 1 ';
    }

    public function doSth() {
        $this->deco1();
        parent::doSth();
    }
}
class ConcreteDecorator2 extends Decorator {
    public function ConcreteDecorator2(Component $_component) {
        parent::__construct($_component);
    }

    private function deco2() {
        echo 'decorator 2 ';
    }

    public function doSth() {
        $this->deco2();
        parent::doSth();
    }
}

$component = new ConcreteComponent();
$component = new ConcreteDecorator1($component);
$component = new ConcreteDecorator2($component);
echo $component->doSth();

// decorator 2 decorator 1 concrete component

[](#0x01-Summary)0x01 Summary
Advantages and disadvantages coexist. Sometimes advantages can also turn into disadvantages. Vice versa.
