---
lang: en
title: Design Pattern - Prototype Pattern
date: 2017-11-06
description: 'Design Pattern Move 7 - Prototype Pattern. 0x00 Prototype Pattern Definition Specify the kinds of objects to create using prototypical instance, and create new objects by copying this prototype. (用原型实例指定创建对象的种类, 并且通过拷贝这些原型创建新的对象。)'
tags: [Design Patterns]
categories:
---

Design Pattern Move 7 - Prototype Pattern.

[](#0x00-Prototype-Pattern)0x00 Prototype Pattern[](#Definition)Definition
Specify the kinds of objects to create using prototypical instance, and create new objects by copying this prototype.
(用原型实例指定创建对象的种类, 并且通过拷贝这些原型创建新的对象。)

General class diagram

![](/2017-11-06-TheZenOfDesignPatternPrototype/photos/prototype.png)

[](#Advantages)Advantages
Excellent performance. The Prototype pattern copies binary streams in memory, which is much better performance than directly newing an object, especially when producing large numbers of objects in a loop. The disadvantage is also reduced constraints.

[](#Disadvantages)Disadvantages
Escaping constructor constraints, copying directly in memory, the constructor is not executed. The advantage is reduced constraints.

[](#Use-Cases)Use Cases
When class initialization consumes very many resources, such as: data, hardware resources.
Scenarios with performance and security requirements. When newing an object requires very cumbersome data preparation or access permissions, the Prototype pattern can be used.
Scenarios where an object has multiple modifiers. When an object needs to provide access to other objects, and each caller may need to modify its value, consider using the Prototype pattern to copy multiple objects for callers to use.
The Prototype pattern can be used together with the Factory Method pattern. Create an object through the clone method, then provide it to callers through the factory method.

[](#Note)Note
Constructor will not be executed.
Shallow copy and deep copy.
When using the clone method, don't add the final keyword to class member variables.

[](#PHP-Example)PHP Example[](#0x01-Summary)0x01 Summary
The Prototype pattern first produces a class containing a large amount of shared information, then copies it (shadow clones), modifies detailed information, and establishes a complete personalized object.
