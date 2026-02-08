---
lang: en
title: Design Pattern - Chain of Responsibility Pattern
date: 2017-11-22
description: '0x00 Chain of Responsibility Pattern Definition Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until'
tags: [Design Patterns]
categories:
---

[](#0x00-Chain-of-Responsibility-Pattern)0x00 Chain of Responsibility Pattern[](#Definition)Definition
**Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it. (使多个对象都有机会处理请求，从而避免了请求的发送者和接受者之间的耦合关系。将这些对象连成一条链，并沿着这条链传递该请求，直到有对象处理它为止。)**

[](#Key-Points)Key Points
Its focus and core are on "chain," having a chain to handle similar requests, deciding within the chain who will handle this request, and returning the corresponding result. Multiple ConcreteHandlers form the core "chain" of the Responsibility pattern.

[](#Advantages)Advantages
Separating requests and handling. The requester only needs to submit the request to the window, not caring who's handling it, while the handler only cares about their handling part, then submits to the next-level handler until completion. Flexible decoupling.

[](#Disadvantages)Disadvantages
Performance - each request traverses from the head of the chain to the tail of the chain. When the chain is long, there will be performance issues.
Debugging - can this only be troubleshooted by binary breakpoints...

[](#Note)Note
Limit the number of nodes in the chain to avoid ultra-long chains. Can judge in the setNext() method.

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
102
103
104
105
<?php
abstract class Handler {
    private  $nextHandler;
    public final function job(Request $_request) {
        $reponse = null;
        if ($this->getEmerLevel() == $_request->getRequestLevel()) {
            $response = $this->report($_request);
        } else {
            if ($this->nextHandler != null) {
                $response = $this->nextHandler->job($_request);
            }
        }
        return $response;
    }

    public function setNext(Handler $_handler) {
        $this->nextHandler = $_handler;
    }

    // Handle urgency level
    abstract function getEmerLevel();

    // Handle task
    abstract function report();
}

class Level {

}

class Request  {
    public function getRequestLevel() {
        return null;
    }
}

class Response {

}

// Three concrete handlers
class ConcreteHandler1 extends Handler {
    protected function report(Request $_request) {
        return null;
    }

    protected function getEmerLevel() {
        return null;
    }
}

class ConcreteHandler2 extends Handler {
    protected function report(Request $_request) {
        return null;
}

    protected function getEmerLevel() {
        return null;
    }
}
class ConcreteHandler3 extends Handler {
    protected function report(Request $_request) {
        return null;
    }
    protected function getEmerLevel() {
        return null;
    }
}

// Scenario class
class Client {
    public static function main() {
        $handler1 = new ConcreteHandler1();
        $handler2 = new ConcreteHandler2();
        $handler3 = new ConcreteHandler3();
        $handler1->setNext($handler2);
        $handler2->setNext($handler3);
        $res = $handler1->job(new Request());
    }
}

[](#0x01-Summary)0x01 Summary
The core of the Responsibility pattern is: initiate a request directly to the first handler, pass it successively to the next-level handler until finally returning the result, the entire request handling process is shielded.
