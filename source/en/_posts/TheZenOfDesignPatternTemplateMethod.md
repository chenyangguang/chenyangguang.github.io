---
title: Design Pattern - Template Method Pattern
date: 2017-10-25
description: 'Design Pattern Move 4 - Template Method Pattern. 0x00 Factory Method Pattern Definition Define the skeleton of an algorithm in an operation, deferring some step to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure'
tags: [Design Patterns]
categories:
---

Design Pattern Move 4 - Template Method Pattern.

[](#0x00-Factory-Method-Pattern)0x00 Factory Method Pattern[](#Definition)Definition
Define the skeleton of an algorithm in an operation, deferring some step to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure
(定义一个操作中的算法的框架, 而将一些步骤延迟到子类中。使得子类可以不改变一个算法的结构即可重定义该算法的某些特定步骤。)

General class diagram

![](/2017-10-25-TheZenOfDesignPatternTemplateMethod/photos/Template-method.png)

[](#Advantages)Advantages
Encapsulate the immutable parts, extend the variable parts. Encapsulate the algorithm's immutable parts in the parent class, extend variable parts through inheritance.
Extract common parts for easy maintenance.
Behavior controlled by parent class, implemented by child class. Basic methods are implemented by child classes, so child classes can add corresponding functions through extension, conforming to the Open-Closed Principle.

[](#Disadvantages)Disadvantages
The Template Method pattern is like Ouyang Feng practicing the Nine Yin Scripture in reverse. The authentic "Nine Yin Scripture" or general martial arts secrets should begin with an outline, like the Dugu Nine Swords. First, the abstract class is responsible for declaring the most abstract and general object attributes and methods - the General Formula, then娓娓道来 the Breaking Sword Formula, Breaking Saber Formula, Breaking Palm Formula, Breaking Rope Formula, Breaking Whip Formula, Breaking Spear Formula, Breaking Arrow Formula, Breaking Qi Formula - these specific attributes and methods of implementation classes. But Ouyang Feng's Template Method pattern, following Huang Rong's recitation of the reversed "Nine Yin Scripture," with head and tail swapped, the abstract class defines some abstract methods to be implemented by child classes. The result of child class execution affects the parent class's result, so the child class influences the parent class, resulting in madness. "Who am I? Who is Ouyang Feng?"

[](#Use-Cases)Use Cases
When multiple child classes have common methods and basically the same logic.
Important and complex algorithms. The core algorithm can be designed as a template method, and surrounding related detail functions are implemented by each child class.
When refactoring, extract the same code to the parent class and constrain its behavior through hook functions.
Specific examples: file upload; data tracking and reporting, etc.

[](#Note)Note
To prevent malicious operations, template methods are generally added with the final keyword and are not allowed to be overridden.
Basic methods in abstract templates should be designed as protected type as much as possible, conforming to the Law of Demeter. Properties or methods that don't need to be exposed should be set to protected type as much as possible. Implementation classes, unless necessary, try not to expand access permissions in the parent class.

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
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
<?php
// Dugu Nine Swords
abstract class Dugujiujian {
    // protected protects the secret moves of Dugu Nine Swords sword technique, rather let it rot on Mount Huashan than easily pass it to Huashan disciples
    protected abstract function zongjueStyle();
    protected abstract function pojianStyle();
    protected abstract function podaoStyle();
    protected abstract function pozhangStyle();
    protected abstract function poqiStyle();

    // final keyword restricts, can't randomly change the sword manual essentials
    final public function useDujiujian ()
    {
        $this->zongjueStyle();
        $this->pojianStyle();
        $this->podaoStyle();
        $this->pozhangStyle();

        // If internal energy is profound, teach Breaking Qi Formula
        if(!$this->isGonglishenhou()) {
            echo( 'Internal energy insufficient, practice in the Jianghu for a few more decades before comprehending Breaking Qi Formula!' . PHP_EOL );
        } else {
            $this->poqiStyle();
        }
    }

    // Hook method
    protected function isGonglishenhou()
    {
        return true;
    }
}

class Fengqingyang extends Dugujiujian {
    protected $deepNeili = true;
    protected function zongjueStyle() {
        echo('Feng Qingyang is teaching General Formula' . PHP_EOL);
    }

    protected function pojianStyle() {
        echo('Feng Qingyang is teaching Breaking Sword Formula' . PHP_EOL);
    }

    protected function podaoStyle() {
        echo('Feng Qingyang is teaching Breaking Saber Formula' . PHP_EOL);
    }

    protected function pozhangStyle() {
        echo('Feng Qingyang is teaching Breaking Palm Formula' . PHP_EOL);
    }

    protected function poqiStyle() {
        echo('Feng Qingyang is teaching Breaking Qi Formula' . PHP_EOL);
    }

    protected function isGonglishenhou () {
        return $this->deepNeili;
    }

    // Whether to teach Breaking Qi Formula is determined by internal energy
    public function checkGongli($deepNeili) {
        return $this->deepNeili = (bool) $deepNeili;
    }
}

class linghuchong extends Dugujiujian {
    protected function zongjueStyle()
    {
        echo('Linghu Chong is learning General Formula' . PHP_EOL);
    }

    protected function pojianStyle()
    {
        echo('Linghu Chong is learning Breaking Sword Formula' . PHP_EOL);
    }

    protected function podaoStyle()
    {
        echo('Linghu Chong is learning Breaking Saber Formula' . PHP_EOL);
    }

    protected function pozhangStyle()
    {
        echo('Linghu Chong is learning Breaking Palm Formula' . PHP_EOL);
    }

    protected function poqiStyle()
    {
        echo('Linghu Chong is learning Breaking Qi Formula' . PHP_EOL);
    }

    protected function isGonglishenhou()
    {
        return false;
    }
}

class chuanshouDugujiujian {
    public static function main ()
    {
        $fengqingyang = new Fengqingyang();
        $deepNeili = 1;
        if(!$deepNeili) {
            $fengqingyang->checkGongli($deepNeili);
        }
        $fengqingyang->useDujiujian();

        $deepNeili = 0;
        $linghuchong = new Linghuchong();
        $linghuchong->useDujiujian();
    }
}

chuanshouDugujiujian::main();

    // Feng Qingyang is teaching General Formula
    // Feng Qingyang is teaching Breaking Sword Formula
    // Feng Qingyang is teaching Breaking Saber Formula
    // Feng Qingyang is teaching Breaking Palm Formula
    // Feng Qingyang is teaching Breaking Qi Formula
    // Linghu Chong is learning General Formula
    // Linghu Chong is learning Breaking Sword Formula
    // Linghu Chong is learning Breaking Saber Formula
    // Linghu Chong is learning Breaking Palm Formula
    // Internal energy insufficient, practice in the Jianghu for a few more decades before comprehending Breaking Qi Formula!

[](#0x01-Summary)0x01 Summary
Using the story of Feng Qingyang teaching Linghu Chong the Dugu Nine Swords to simulate the Template Method pattern, although a bit stiff, it's also my understanding of the Template Method pattern. Anyway, I have to implement it myself, slowly digesting and absorbing. Even if eating it with mustard, swallow it first.
