---
title: "Stock Checkers"
date: 2021-09-01
draft: false
description: "Notify when things are in stock"
tags: ["python", "automation"]
---

Back during the COVID stimulus era, there were many things that went completely out of stock everywhere. I waited months to get my RTX 3070 from a virtual queue because there were so few available. Since I love automation, I wanted to create a bot to watch for these types of things. However, good bots like `stockdrops` already existed. I decided to create a few bots in more specialized areas, such as on the hardware trading forum r/hardwareswaps. My bot would watch for new posts of a certain title containing an item that I was interested in. Then, it would spam me with emails and messages in hopes that I could be the first to reply.

Another bot that I worked on in the same domain is my `classdrops` bot. This would apply a similar idea to the world of intro-level undergraduate computer science classes at my university. Since these were in low supply, my bot would notify me whenever a slot opened up so that I could immediately enroll into it.

### Classdrops: [github.com/bhackel/classdrops](https://github.com/bhackel/classdrops)

### HardwareSwapDrops [github.com/bhackel/hardwareswapdrops](https://github.com/bhackel/hardwareswapdrops)