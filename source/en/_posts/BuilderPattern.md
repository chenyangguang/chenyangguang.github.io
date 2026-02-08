---
title: Design Pattern - Builder Pattern
date: 2017-10-26
description: '0x00 Builder Pattern Definition Separate the construction of a complex object from its representation so that the same construction process can create different representations. (将一个复杂对象的构建与它的表示分离, 使得同样的构建过程可以创建不同的表示。)'
tags: [Design Patterns]
categories:
---

[](#0x00-Builder-Pattern)0x00 Builder Pattern[](#Definition)Definition
Separate the construction of a complex object from its representation so that the same construction process can create different representations.
(将一个复杂对象的构建与它的表示分离, 使得同样的构建过程可以创建不同的表示。)

![](/2017-10-26-BuilderPattern/photos/builder-pattern.png)

[](#Advantages)Advantages
Encapsulation - Clients don't need to know the internal details of the product.
Builders are independent and easy to extend.
Easy to control detail risks - Since specific builders are independent, gradual refinement during the construction process won't affect other modules.

[](#Use-Cases)Use Cases
When the same methods with different execution sequences produce different results, the Builder pattern can be adopted.
When multiple parts or components can be assembled into an object but produce different runtime results, this pattern can be used.
When the product class is very complex, or when different calling sequences of the product class produce different effects, using the Builder pattern is very appropriate.

[](#Note)Note
The Builder pattern focuses on part types and decoration process (sequence), which is the biggest difference between it and the Factory pattern.

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
<?php
abstract class AbstractQueryBuilder {
    abstract function getQuery();
}

abstract class AbstractQueryDirector {
    abstract function __construct(AbstractQueryBuilder $builder);
    abstract function buildQuery();
    abstract function getQuery();
}

class Model {
    private $sql = NULL;
    private $sql_table = NULL;
    private $sql_where = NULL;
    private $sql_limit = NULL;

    function __construct() {
    }

    function querySql() {
        return $this->sql;
    }

    function table($table) {
        $this->sql_table  = $table;
    }

    function where($where) {
        $this->sql_where = $where;
    }

    function limit ($limit) {
        $this->sql_limit = $limit;
    }

    function splicingQuery () {
        $this->sql = 'SELECT * FROM ';
        $this->sql .= $this->sql_table;
        $this->sql .= ' WHERE ' . $this->sql_where;
        $this->sql .= ' LIMIT ' . $this->sql_limit;
    }
}

class BaseQueryBuilder extends AbstractQueryBuilder {
    private $query = NULL;
    function __construct() {
        $this->query = new Model();
    }

    function table($table) {
        $this->query->table($table);
    }

    function where($where) {
        $this->query->where($where);
    }

    function limit($limit) {
        $this->query->limit($limit);
    }

    function splicingQuery() {
        $this->query->splicingQuery();
    }

    function getQuery() {
        return $this->query;
    }
}

class UserQueryDirector extends AbstractQueryDirector {
    private $builder = NULL;
    public function __construct(AbstractQueryBuilder $builder_sql) {
        $this->builder = $builder_sql;
    }

    public function buildQuery() {
        $this->builder->table('User');
        $this->builder->where('id < 10');
        $this->builder->limit('100');
        $this->builder->splicingQuery();
    }

    public function getQuery() {
        return $this->builder->getQuery();
    }
}

$queryBuilder = new BaseQueryBuilder();
$userDirector = new UserQueryDirector($queryBuilder);
$userDirector->buildQuery();
$userSql = $userDirector->getQuery();

var_dump($userSql->querySql());

// string(42) "SELECT * FROM User WHERE id < 10 LIMIT 100"

[](#0x01-Summary)0x01 Summary
Various design patterns have similarities. For example, encapsulation.
