---
title: "Cheggbog"
date: 2022-12-15
draft: false
description: "Automated Chegg Discord and Telegram bot using keyboard automation"
tags: ["web scraping", "automation", "python"]
---

## Repo: [github.com/bhackel/cheggbog](https://github.com/bhackel/cheggbog)

Disclaimer: This was a project that started back in high school, and I've since stopped development for it due to the morally questionable nature of the project.

## General

Cheggbog is a fully featured discord and telegram bot for scraping Chegg links. It allows the users to send the bot a message containing a link, and it will reply with the answer for that link.

## Background

The incentive for this project was a desire to split the cost of a Chegg account with multiple friends. The issue with this is that Chegg only allows 2 devices to be logged in at a time, which prevents people from sharing their accounts.

To avoid this, I initially looked around for existing solutions for Chegg discord bots. Most bots seemed to be private and paid, and the ones that were public did not work.

## Code

The first iteration of this bot used Selenium, which is software that can control a browser directly. This worked for a while, but eventually Chegg started implementing anti-bot measures that prevented Selenium from working

In order to fix this problem, I decided to look at the process from a different angle - rather than using automation tools and trying to avoid looking like a bot, my code could instead pretend to be a human and interact with the website naturally.

Therefore, the next and current solution was to run the bot in a virtual machine, with access to a regular Chrome browser

![Cheggbog Virtual Machine](cheggbog%201.jpg)

To automate it, the bot would do the following

1. Open the given link in Chrome
2. Wait for page to load
3. Format the page nicely using Javascript
4. Take a screenshot of the whole page
5. Save the image
6. Send the image back to the user

![Cheggbog discord](cheggbog%202.jpg)

This way, the bot avoids detection by Chegg.