---
lang: en
title: Design Pattern - Composite Pattern
date: 2017-11-28
description: '0x00 Composite Pattern The Composite pattern, also called the Synthesis pattern. Definition Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly. (将抽象对象组合成树形结构以表示＂部分－整天＂的层次结构，使得用户对单个对象和组合对象的使用具有一致性．)'
tags: [Design Patterns]
categories:
---

[](#0x00-Composite-Pattern)0x00 Composite Pattern
The Composite pattern, also called the Synthesis pattern.

[](#Definition)Definition
**Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly. (将抽象对象组合成树形结构以表示＂部分－整天＂的层次结构，使得用户对单个对象和组合对象的使用具有一致性．)**

[](#Key-Roles)Key Roles
Component - Abstract component, defines common properties and methods for objects participating in the combination, can define some default properties or behaviors.
Leaf - Leaf component, leaf object with no remaining branches, belongs to the minimum unit of traversal.
Composite - Branch component, branch object, combines branch nodes and leaf nodes to form a tree structure.

[](#Advantages)Advantages
Simple high-level module calls - all nodes in a tree structure are Components. For callers, there's no difference between parts and the whole. That is, high-level modules don't need to care whether they're handling a single object or an entire composite structure, simplifying high-level module code.
Nodes can be freely added
If you want to add a branch node or leaf node, just find its parent node. Easy to extend.

[](#Disadvantages)Disadvantages
Leaves and branches directly use implementation classes, limiting the scope of interface usage.

[](#Use-Cases)Use Cases
Scenarios for maintaining and displaying "part-whole" relationships, such as tree menus, file and folder management.
Scenarios where independent modules or functions can be separated from a whole.

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
<?php

// Abstract component
abstract class Component {
    public function doSth() {}
}

// Branch component
class Composite extends Component {
    private $compArr = [];
    public function add(Component $_component)
    {
        array_push($this->compArr, $_component);
    }

    public function remove(Component $_component)
    {
        $key = array_search($_component, $this->compArr);
        if (!$key !== false) {
            array_splice($this->compArr, $key, 1);
        }
    }

    public function getChildren()
    {
        return $this->compArr;
    }
}

// Leaf component
class Leaf extends Component {
    public function doSth()
    {}
}

class Client {
    public static function main()
    {
        $root = new Composite();
        $root->doSth();
        $branch = new Composite();
        $root->add($branch);
        $leaf = new Leaf();
        $branch->add($leaf);
    }
    public static function showTree(Composite $root)
    {
    }
}

[](#0x-Summary)0x Summary
Whether you're there or not, design patterns are always there...
