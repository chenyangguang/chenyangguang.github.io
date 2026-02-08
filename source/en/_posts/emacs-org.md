---
title: Emacs Stroll -- org-mode Two or Three Things about link
date: 2017-08-15
description: 'org-link Within emacs, use Alt + X to bring up the helm interface. The helm interface can be brought up directly in input mode. Unlike vim. Input org-link can see various operations related to links in org-mode. helm is very friendly, just input the command name with relevant keywords, and it lists all commands containing this keyword. And when inputting these keywords for queries, the order doesn't matter! Links under org-mode are in this style'
tags: [Emacs, Editor]
categories:
---

[](#org-link)org-link
Within emacs, use Alt + X to bring up the helm interface. The helm interface can be brought up directly in input mode. Unlike vim. Input org-link can see various operations related to links in org-mode. helm is very friendly, just input the command name with relevant keywords, and it lists all commands containing this keyword. And when inputting these keywords for queries, the order doesn't matter!

Links under org-mode are in this style [[[http://www.gnu.org/software/emacs/][GNU](http://www.gnu.org/software/emacs/][GNU) Emacs]], [http://wowubuntu.com/markdown/](markdown的链接方式), roughly the same. Normally org-link comes with three brackets, inside the first bracket is the link address, can be file path, image address, http hyperlink, the second bracket is the description of this link, description can be empty like [[[http://www.gitvim.com]]。](http://www.gitvim.com]]。)

List a few commonly used link operations:

org-insert-link
As the name suggests, add a hyperlink copy with link and description, first input link, then input description.

org-toggle-link-display
Can switch display between link and description, convenient for modifying description and link address.

org-store-link
Used for... this is weird

org-previous-link & org-next-link
Twins, commands to jump forward and backward between links.

[](#Summary)Summary
Emacs is a heavy tool of the program kingdom. Think about it, stop where appropriate.
