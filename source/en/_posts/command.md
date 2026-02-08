---
title: Design Pattern - Command Pattern
date: 2017-11-21
description: '0x00 Command Pattern Definition The Command pattern is a highly cohesive pattern, defined as: Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations. (将一个请求封装成一个对象，从而让你使用不同的请求把客户端参数化，对请求队列或者记录请求日志，可以提供命令的撤销和回复功能。)'
tags: [Design Patterns]
categories:
---

[](#0x00-Command-Pattern)0x00 Command Pattern[](#Definition)Definition
**The Command pattern is a highly cohesive pattern, defined as: Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.**
(将一个请求封装成一个对象，从而让你使用不同的请求把客户端参数化，对请求队列或者记录请求日志，可以提供命令的撤销和回复功能。)

[](#General-Classes)General Classes
Contains three roles:

Receiver - Receiver role, where commands are passed and executed.
Command - Command role, declares all commands that need to be executed.
Invoker - Caller role, receives commands and executes them.

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
<?php
/*
  command pattern
 */

// Generic Receiver class
abstract class Receiver {
    abstract function dosth();
}

// Concrete Receiver class
class ConcreteReceiver1 extends Receiver  {
    public function doSth() {
    }
}

class ConcreteReceiver2 extends Receiver {
    public function doSth() {

    }
}

// Abstract Command class
abstract class Command {
    abstract function execute();
}

// Concrete Command class
class ConcreteCommand1 extends Command {
    private $receiver;

    public function ConcreteCommand1(Receiver $_receiver) {
        $this->receiver = $_receiver;
    }

    public function execute() {
        $this->receiver->doSth();
    }
}

class ConcreteCommand2 extends Command {
    private $receiver;

    public function ConcreteCommand2(Receiver $_receiver) {
        $this->receiver = $_receiver;
    }

    public function execute() {
        $this->receiver->doSth();
    }
}

// Caller Invoker class
class Invoker {
    private $command;

    public function setCommand(Command $_command) {
        $this->command = $_command;
    }
    public function act() {
        $this->command->execute();
    }
}

// Scenario call
class client {
    public static function main() {
        $invoker = new Invoker();
        $receiver = new ConcreteReceiver1();
        $command = new ConcreteCommand1($receiver);
        $invoker->setCommand($command);
        $invoker->act();
    }
}

[](#0x01-Summary)0x01 Summary
Don't aim too high. Even if your journey is to the stars and seas, you must make solid preparations and keep your feet on the ground.
