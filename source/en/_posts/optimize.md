---
title: Record an API 20x Performance Optimization
date: 2018-09-24
description: 'Synchronization One of the projects I took over has a core business providing user information synchronization functionality. This sync API is also connected to other related businesses, like creating accounts, querying information, downloading information, etc. Historical Issues This business has a long history, mainly for various product departments to call this interface, upload user information, provide online service support. And this synchronization interface, from launch to now, has been optimized for 35 versions! Current performance: synchronizing 26000 user information takes about 45 minutes. Callers often use it until they\'re terrified. So now it\'s in my hands.'
tags: [Web]
categories:
---

[](#Synchronization)Synchronization
One of the projects I took over has a core business providing user information synchronization functionality. This sync API is also connected to other related businesses, like creating accounts, querying information, downloading information, etc.

[](#Historical-Issues)Historical Issues
This business has a long history, mainly for various product departments to call this interface, upload user information, provide online service support. And this synchronization interface, from launch to now, has been optimized for 35 versions! Current performance: synchronizing 26000 user information takes about 45 minutes. Callers often use it until they're terrified. So now it's in my hands.

[](#Get-Started)Get Started
Understand requirements - communication, navigating various checkpoints. Read source code, draw flowcharts.
Investigate problem bottlenecks, monitoring system (prometheus) analyze response time, time consumption. Set breakpoints, logs, database statistics time consumption.
Meeting discussion, discuss pain points, make decisions, divide responsibilities, argue about solutions.
Meeting discussion, make decisions, divide responsibilities, argue about solutions.
Meeting discussion, finalize solution, development cycle, pull in an architect and technical director to review together.
While writing test cases, conceive.
Meeting, understand progress, solution feasibility.
Complete local batch testing, simulate client access. Introduce golang's built-in pprof tool.
Refactor database, optimize table structure, add indexes, etc.
Refactor branch process, code.
Development concentrated. Several problems appeared in between, several more meetings, continuously cutting encountered problems, and blind spots of previous problems, listing solutions one by one.
Merge
Unit testing
Stress testing

[](#Optimization-Points)Optimization Points
Database table adjustments, add indexes.
During synchronization phase, disconnect an external interface consuming nearly 1/3 of time, delay execution of external interface interaction process.
Batch processing, single user information, batch query, then local calculation, finally batch database insert.
Reasonably use goroutine.
Etc.

[](#Effect)Effect
Deployed to test environment, 26000 users synchronized within 50s. Optimized version synchronization speed achieved about 20x quality improvement! Temporarily making a note. Part of this version's work was completed the day "Mangkhut" typhoon arrived. Fortunately people are fine, returned home from company in the early morning.
Online performance, to be updated after I confirm the launch.

[](#Summary)Summary
When encountering problems, find the root cause, apply right medicine, reasonably use open source tools (like prometheus and pprof play important roles in analyzing bottlenecks). Every solved problem is my motivation to move forward in the next step.
