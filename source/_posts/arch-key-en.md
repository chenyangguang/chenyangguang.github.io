---
lang: en
title: arch-key
date: 2019-05-12
description: 'Arch system signature error When upgrading or reinstalling fails, reporting error: krb5: signature from … is unknown trust… invalid or corrupted package (PGP signature) Solution 1 pacman-key --refresh-keys or 1 pacman -Sy archlinux-keyring'
tags: [Tips]
categories:
---

[](#Arch-System-Signature-Error)Arch System Signature Error
When upgrading or reinstalling fails, reporting error: krb5: signature from … is unknown trust
… invalid or corrupted package (PGP signature)

[](#Solution)Solution
```q
pacman-key --refresh-keys
```

or

```ebnf
pacman -Sy archlinux-keyring
```
