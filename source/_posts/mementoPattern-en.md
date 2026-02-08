---
lang: en
title: Memento Pattern
date: 2017-12-01
description: '0x00 Memento Pattern Definition Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later. (在不破坏封装性的前提下，捕获一个对象的内部状态，并在这个对象外保存该状态．之后可将该对象恢复到之'
tags: [Design Patterns]
categories:
---

[](#0x00-Memento-Pattern)0x00 Memento Pattern[](#Definition)Definition
**Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later. (在不破坏封装性的前提下，捕获一个对象的内部状态，并在这个对象外保存该状态．之后可将该对象恢复到之前保存的状态．)**

[](#Roles)Roles
Originator - Originator role, records current moment's internal state, responsible for defining which states belong to backup range, responsible for creating and restoring memento data.
Memento - Memento role, responsible for storing Originator object's internal state, provides the internal state needed by the originator when needed.
Caretaker - Memento administrator role, manages mementos, saves and provides mementos.

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

// Originator
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

    // Create new memento
    public function createMemento()
    {
        return new Memento($this->state);
    }

    // Restore memento
    public function restoreMemento(Memento $_memento)
    {
        $this->setState($_memento->getState());
    }
}

// Memento role
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

// Memento manager
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

[](#0x01-Summary)0x01 Summary[](#Scenarios)Scenarios
Scenarios where need to save and restore related data states
Provide a rollback operation
In monitored copies
Database connection's transaction management uses the memento pattern.

[](#Note)Note
Memento lifecycle needs active management. Mementos should be used in "nearest" code after creation, create then use, if not using immediately delete its reference, wait for GC to handle it.
Don't use memento pattern in scenarios of frequently creating backups, because:
Can't control the number of objects created by mementos
Creating large objects consumes resources, affecting system performance
