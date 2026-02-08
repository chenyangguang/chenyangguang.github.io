---
title: Golang way
date: 2018-03-01
description: 'Go Introduction I've always heard that Go has built-in support for concurrent programming, so I sharpened my knife and jumped into the pit. Getting Started Features Go language can do implicit definition, but there's no implicit type conversion. All memory in Go is initialized. Variable naming uses camelCase, first word lowercase, first letter of each new word capitalized. If global variables need to be used by external packages, the first letter also needs to be capitalized.'
tags: [Go]
categories:
---

[](#Go-Introduction)Go Introduction
I've always heard that Go has built-in support for concurrent programming, so I sharpened my knife and jumped into the pit.

[](#Getting-Started)Getting Started[](#Features)Features
Go language can do implicit definition, but there's no implicit type conversion.
All memory in Go is initialized.
Variable naming uses camelCase, first word lowercase, first letter of each new word capitalized. If global variables need to be used by external packages, the first letter also needs to be capitalized.

[](#Basic-Types-and-Operators)Basic Types and Operators
Two values of the same type can be compared using **==** or **!=**. Values of different types cannot be compared.
Go supports integer and floating-point numbers, and natively supports complex numbers, with bitwise operations using two's complement. int is the fastest type, try to use float64.

Leave a space between the * and pointer name to prevent it from being mistaken for a multiplication expression. When used before a pointer, you get the value stored at the address pointed to by this pointer; this is a dereference (indirect reference) operator, also called pointer transfer. The advanced application of pointers is passing a variable's reference (such as a function parameter), so you don't pass a copy of the variable. Note: In Go, pointer arithmetic like pointer++ in C is not allowed.

Special flow control, **select** structure is used for **channel** selection. Parentheses around conditional statements can be omitted. Use parentheses when necessary to improve precedence. **switch** can accept **case** judgments of any type of value or expression of the same type. And **for** can use multiple counters simultaneously in the loop body.

[](#The-Essence-of-goroutine-and-channel)The Essence of goroutine and channel
**goroutine** is the concurrent execution body of Go programs, **channel** is the connection between them, a communication mechanism that allows one goroutine to send special values to another goroutine. Each channel is a conduit of a specific type, called the channel's element type. Channel creation uses make. Channel has two operations, send and receive, collectively called communication. Using the ancient magical symbol **<-**. close(ch) closes the channel, make() can create two types of channels, buffered channels with a positive second parameter, others are unbuffered channels.

[](#References)References
[The Way to Go](https://github.com/Unknwon/the-way-to-go_ZH_CN)
[Go Official Website](https://golang.org/)
