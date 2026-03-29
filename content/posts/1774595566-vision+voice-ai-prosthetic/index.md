---
title: "Vision+Voice AI Prosthetic"
date: 2026-03-27
draft: false
description: "Proof-of-concept of adding vision plus voice input to a prosthetic"
---

![Prosthetic worn on arm](<media/main picture.jpeg>)

## Demo

<video controls width="100%">
    <source src="media/full%20demo.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

## Summary

This project is a proof-of-concept of what adding both vision and voice input to a prosthetic could enable for advanced control.

## Existing Research

Current research has already done automatic grasp selection using vision: [PMC5325038](https://pmc.ncbi.nlm.nih.gov/articles/PMC5325038/). Other research has used vision with EMG trigger for prosthetic grasp selection: [frobt.2024.1312554](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2024.1312554/full). Other research has targeted robotic arms for LLM-based grasp selection: [arXiv:2310.05239](https://arxiv.org/html/2310.05239v1). **However no project combines all methods into a Vision+Language EMG-triggered prosthetic project**.

## Implementation

### Hardware

This project uses the AmazingHand from Pollen robotics: [AmazingHand](https://github.com/pollen-robotics/AmazingHand).

![Front view of hand](<media/cam view.jpeg>)

The AmazingHand is a 8-DOF 4-finger robotic hand with 8 Feetech SCS0009 servos.

![Back of hand showing servos](<media/back view.jpeg>)

I modified the palm plate to fit a XIAO ESP32 Sense: [XIAO ESP32S3 Sense](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html), which provides a camera, microphone, WiFi, and BLE in a tiny low-cost package.

![XIAO ESP32S3 Sense camera module](<media/xiao esp32 sense.jpeg>)

![ESP32 mounting inside wrist](<media/esp32 mounting.jpeg>)

For power, the servo bus adapter is placed inside the prosthesis grip.

![Grip interior](<media/grip interior.jpeg>)

A 2S RC battery connects to a buck converter down to 5V, which powers the whole system.

![Battery pack on forearm](<media/battery pack.jpeg>)

After a grip is selected, the user toggles the grip on/off using a Myoware EMG sensor.

![MyoWare EMG sensor on wrist](<media/myoware sensor.jpeg>)

### Software

The XIAO ESP32 Sense captures images every 15 seconds, while recording audio in between the images. It connects to the configured WiFi network and makes HTTP requests to a local computer.

The local computer runs a Python web server that receives the audio and image. It sends the audio to Groq cloud for transcription (free) and then sends the image plus transcript to Claude Sonnet 4.5 (paid, ~$0.0025/image). The system prompt asks for a grip selection, which is then sent back to the ESP32.

![Voice command grip selection](<media/image and audio grip selection.jpeg>)

The ESP32 receives the new grip, or none if no object was confidently identified. Then, it waits for the EMG to exceed a threshold. When it is crossed, the grip is toggled on/off.

![Vision-based grip analysis with EMG data](<media/grip analysis with EMG data.jpeg>)

The ESP32 communicates using UART with a Servo Bus Adapter board to control the Feetech motors.

## Possible Future Features

Currently there is no way to know what grip was selected. This could be informed using vibrational motors with specific patterns.

Grips are either 100% on or 100% off. I am unsure how to solve this.

EMG sensing was extremely flaky with my setup. I struggled to trigger the grips consistently.

A future iteration of this project could use a wrist joint. Then the camera could servo the hand towards the targeted object.