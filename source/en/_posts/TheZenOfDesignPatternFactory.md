---
title: Design Pattern - Factory Method Pattern
date: 2017-10-23
description: 'Design Pattern Move 2 - Factory Method Pattern, this pattern is used very frequently. So learn it a bit earlier. 0x00 Factory Method Pattern Definition Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to'
tags: [Design Patterns]
categories:
---

Design Pattern Move 2 - Factory Method Pattern, this pattern is used very frequently. So learn it a bit earlier.

[](#0x00-Factory-Method-Pattern)0x00 Factory Method Pattern[](#Definition)Definition
Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses. + Separate the construction of a complex object from its representation so the same construction can create different representation

(定义一个用于创建对象的接口，让子类决定实例化哪一个类。工厂方法使一个类的实例化延迟到其子类。)

[](#Interpretation)Interpretation
There can be many specific product classes, all inheriting from the abstract product class.
The abstract factory class is responsible for defining the production of product objects.
How to create a specific product object is implemented by the specific factory class.

[](#Advantages)Advantages
Good encapsulation, clear code structure. The creation of an object has conditional constraints. If a caller needs a specific product object, they only need to know the class name of the product. No need to know the arduous process of creating objects, reducing coupling between modules.
The extensibility of the Factory Method pattern. When increasing product classes, as long as you appropriately modify specific factory classes or extend a factory class, you can achieve "embracing change."
Masking product classes. Because the instantiation of product classes is the responsibility of factory classes, callers don't need to care about how product class implementations change, only about product interfaces. If the interface doesn't change, upper-level modules in the system don't need to change. For example: using the Factory Method pattern to connect to databases, switching from MySQL to Oracle only requires changing the driver name.
Decoupling framework.

[](#Use-Cases)Use Cases
The Factory Method pattern is a substitute for newing an object. If adding a factory class doesn't increase code complexity, it can be used wherever objects need to be generated.
Flexible, extensible frameworks can use the Factory Method pattern. Everything is an object. For example: it can be used in connection methods for http, udp protocols.
The Factory Method pattern can be used in heterogeneous projects.
Can be used in test-driven development frameworks.

[](#Extensions)Extensions
Reduce to Simple Factory pattern. Remove the abstract class and use the static keyword.
Upgrade to multiple factory classes.
Replace Singleton pattern. The core requirement of Singleton pattern is to have only one object in memory. Through the Factory Method pattern, you can produce only one object in memory.
Lazy initialization. After an object is consumed, it's not immediately released. The factory class maintains its initial state, waiting to be used again.

[](#0x01-Summary)0x01 Summary
For now, I understand the Factory Method pattern as: you give me an item name, throw it to the workshop, complete production.
