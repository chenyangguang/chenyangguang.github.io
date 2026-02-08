---
lang: en
title: Design Pattern - Iterator Pattern
date: 2017-11-27
description: '0x00 Iterator Pattern The iterator is like a cursor in a database (MySQL cursor is one-way), can roll inside a container, traverse all viewed elements. Definition Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation. (It provides a method to access each element in a container object without exposing the object\'s internal details.)'
tags: [Design Patterns]
categories:
---

[](#0x00-Iterator-Pattern)0x00 Iterator Pattern
The iterator is like a cursor in a database (MySQL cursor is one-way), can roll inside a container, traverse all viewed elements.

[](#Definition)Definition
**Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.** (它提供一种方法访问容器对象中的各个元素，而又不需暴露对象的内部细节．)

[](#Roles)Roles
Iterator - Abstract iterator, defines and traverses element interfaces, generally has three fixed methods: first(), next(), hasNext().
ConcreteIterator - Specific iterator, specifically implements the iterator interface.
Aggregate - Abstract container, provides interface for creating specific iterator roles.
ConcreteAggregate - Specific container, object that creates iterators.

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
<?php
/*
 * Iterator Pattern
 */
interface IIterator {
    public function next();
    public function hasNext();
    public function remove();
}

class ConcreteIterator implements IIterator {
    private $arr = [];
    public $cursor = 0;

    public function __construct($_arr)
    {
        $this->arr = $_arr;
    }

    public function hasNext()
    {
        return $this->cursor == count($this->arr) ? false : true;
    }

    public function next()
    {
        $result = null;
        if($this->hasNext()) {
            return ($this->arr)[$this->cursor++];
        }
        return $result;
    }

    // When developing systems, if using iterator's delete method, should complete two functions: 1. Delete current element, 2. Current cursor points to next element.
    public function remove()
    {
        $this->cursor = null;
        return true;
    }
}

interface Aggregate {
    public function add($obj);
    public function remove($obj);
    public function iterator();
}

class ConcreteAggregate implements Aggregate {
    private $arr = [];

    public function add($obj)
    {
        $this->arr[] = $obj;
    }

    public function iterator()
    {
        return new ConcreteIterator($this->arr);
    }

    public function remove($obj)
    {
        $this->remove($obj);
    }
}

class Client {
    public static function main()
    {
        $agg = new ConcreteAggregate();
        $agg->add('test');
        $agg->add('hello');
        $agg->add('world');
        $iterator = $agg->iterator();
        while ($iterator->hasNext()) {
            echo $iterator->next(), PHP_EOL;
        }
    }
}
(new Client())::main();
/*
test
hello
world
*/

[](#PHP's-Built-in-Iterator-Interface)PHP's Built-in Iterator Interface
[PHP Native Iterator](http://php.net/manual/en/spl.iterators.php).

1
2
3
4
5
6
7
8
9
Iterator extends Traversable {
/* Methods */
abstract public mixed current ( void )
abstract public scalar key ( void )
abstract public void next ( void )
abstract public void rewind ( void )
abstract public boolean valid ( void )
}

Provides quite a few methods.

[](#0x01-Summary)0x01 Summary
Gradually getting some feel for it.
