---
title: "Teams Auto Joiner"
date: 2021-03-01
draft: false
description: "Automated voice call joiner"
tags: ["automation", "python"]
---

## Repo: [github.com/bhackel/Teams-Auto-Joiner-BCP](https://github.com/bhackel/Teams-Auto-Joiner-BCP)

## What is it

This was a high school project that started during COVID when everything was remote. Our school used Microsoft Teams to conduct class meetings. As a challenge, I wanted to automate the call joining process so that I could be more responsible and wake up to class on time. This project involves using Selenium to control a browser where the user is signed into Teams. Then, by monitoring for upcoming meetings, it can join those meetings, disable camera and microphone, and then wait. After the call has ended, or everyone has left the meeting, then it will automatically leave the call.

## Learning takeaways

This was my first time creating a tool for my friends to use as well. Therefore, I used a python package that bundled my project into an executable that I could provide to my friends. I had them run through the app while I was watching to see where they would get stuck or confused. Then, I would make improvements to those parts of the app.