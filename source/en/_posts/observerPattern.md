---
title: Design Pattern - Observer Pattern
date: 2017-11-29
description: '0x00 Observer Pattern Also called Publish/Subscribe Pattern. Definition Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically. (定义对象间一对多的依赖关系'
tags: [Design Patterns]
categories:
---

[](#0x00-Observer-Pattern)0x00 Observer Pattern
Also called Publish/Subscribe Pattern (Publish/Subscribe).

[](#Definition)Definition
**Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically. (定义对象间一对多的依赖关系，使得每当一个对象改变状态，则所有依赖于它的对象都会得到通知并自动更新．)**

[](#Roles)Roles
Subject - Observed role, must be able to dynamically add and cancel observers, plays the role of observing observers and notifying observers.
Observer - Observer role, observers receive message notifications and update.
ConcreteSubject - Specific observed role, defines the observed's own business logic, also defines which events to notify.
ConcreteObserver - Specific observer role, each specific observer's own processing logic.

[](#Advantages)Advantages
Abstract coupling between observer and observed relationships, making it easy to extend.
Establish a trigger mechanism.

[](#Disadvantages)Disadvantages
When multi-level triggering, efficiency becomes poor.

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
<?php
/*
 * observer pattern
 */

//Observed
abstract class Subject {
    private $observers = [];
    public function addObserver(Observer $_observer)
    {
        array_push($this->observers, $_observer);
    }

    public function delObserver(Observer $_observer)
    {
        $key = array_search($this->observers, $_observer);
        if ($key !== false) {
            array_splice($this->observers, $key, 1);
        }
    }

    // Notify all observers
    public function notifyObservers()
    {
        foreach($this->observers as $observer) {
            $observer->update();
        }
    }
}

// Specific observed
class ConcreteSubjects extends Subject {
    public function doSth()
    {
        parent::notifyObservers();
    }
}

// Observer interface
interface Observer {
    public function update();
}

class ConcreteObserver implements Observer {
    public function update()
    {
        echo "Get it! Yes! Sir!";
    }
}

class Client {
    public static function main()
    {
        $subject = new ConcreteSubjects();
        $observers = new ConcreteObserver();
        $subject->addObserver($observers);
        $subject->doSth();
    }
}
(new Client())::main();

[](#Use-Cases)Use Cases
Separable non-combination related behavior scenarios.
Multi-level event trigger scenarios.
Cross-system message exchange scenarios, like message queue processing mechanisms.

[](#0x01-Summary)0x01 Summary
The Observer pattern needs to focus on solving two problems:

Broadcast chain - in an observer pattern, at most one object appears as both observer and observed, meaning messages are forwarded at most once (forwarded twice) is appropriate and well-controlled.
Asynchronous processing - need to consider thread safety and queues.
