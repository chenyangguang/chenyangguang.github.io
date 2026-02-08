---
title: Mediator Pattern
date: 2017-11-12
description: '0x00 Mediator Pattern In real life, there are shadows of mediators everywhere: the command center of the Shenzhou spacecraft, airport dispatch centers, the C (controller) in MVC frameworks, media gateways, rental intermediaries, etc. The Mediator pattern is also called the Arbitrator pattern. Definition Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling'
tags: [Design Patterns]
categories:
---

[](#0x00-Mediator-Pattern)0x00 Mediator Pattern
In real life, there are shadows of mediators everywhere: the command center of the Shenzhou spacecraft, airport dispatch centers, the C (controller) in MVC frameworks, media gateways, rental intermediaries, etc. The Mediator pattern is also called the **Arbitrator pattern**.

[](#Definition)Definition
Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly, and it lets you vary their interaction independently. (用一个中介对象封装一系列的对象交互，中介者是各对象不需要显示地相互作用，从而使其耦合松散，而且可以独立地改变它们之间的交互。)

[](#Components)Components
Mediator - Abstract mediator role, defines a unified interface for communication between colleague roles.
Concrete Mediator - Specific mediator role, implements collaborative behavior by coordinating various colleague roles, so it must depend on colleague roles.
Colleague - Colleague role, communication between each colleague role and other colleague roles must go through the "peacemaker" **mediator**. The behavior of each colleague class is divided into two types:
Self-initiated behavior: The colleague's own behavior, such as changing its own state, handling its own behavior, etc., which doesn't need to rely on the mediator.
Dependent methods: Behaviors that can only be completed with the mediator's help.

[](#Advantages)Advantages
The Mediator pattern reduces dependencies between classes. Colleague classes only depend on the mediator, transforming **one-to-many** dependencies into **one-to-one** dependencies. While reducing dependencies, it also lowers coupling between classes.

[](#Disadvantages)Disadvantages
As logic complexity increases, the original direct interdependencies among N objects are transferred to dependencies between the mediator and colleague classes. The mediator's logic gradually becomes more complex and increasingly bloated.

[](#Use-Cases)Use Cases
When multiple objects are **tightly coupled** (a spider web structure appears in the class diagram), using a mediator is a good choice.
By the way, are those agents and secretaries also examples of the Mediator pattern?

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
<?php

// Generic abstract mediator
abstract class Mediator {
    protected  $colleague;

    public function getColleague() {
        return $this->colleague;
    }

    public function setColleague(ConcreteColleague $conColl) {
        $this->colleague = $conColl;
    }

    abstract public function doSth();
}

// Generic mediator
class ConcreteMediator extends  Mediator {
    public function dosth() {}
}

// Abstract colleague class
abstract class Colleague {
    protected $mediator;

    public function Colleague(Mediator $_mediator) {
        $this->mediator = $_mediator;
    }
}

// Concrete colleague class
class ConcreteColleague extends Colleague {
    public function ConcreteColleague(Mediator $_mediator) {
        parent::setColleague($_mediator);
    }

    // Self-initiated behavior
    public function selfMethod() {}

    // Dependent method
    public function relyMethod() {
        parent::doSth(); // Delegate to mediator
    }
}
?>

[](#Summary)Summary
Literally, mediators and proxies share some vague similarities. So what's the difference between a mediator and a proxy?
