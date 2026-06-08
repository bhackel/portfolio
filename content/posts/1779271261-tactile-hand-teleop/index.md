---
title: "Tactile-Sensing Hand + Teleop"
date: 2026-06-04
draft: false
description: "A sub-$200 robotic hand with FSR fingertip sensing that grasps without crushing, plus VR teleop on the ARCTOS arm"
---

![Robotic hand on the ARCTOS arm next to a dumbbell](media/11.jpg)

## Summary

This was my CSE 145/237D capstone with Triton Droids at UCSD. We built a sub-$200 robotic hand with force-sensing resistors on all four fingertips that can grasp things without crushing them. Then we added vision, VR teleop, and simulation, and mounted it on a teleoped ARCTOS arm.

I led the project and did the electronics. I made the prototype board, wrote the ESP32 firmware, and printed the calibration weights.

GitHub: [cse-145-237d-tactile-hands](https://github.com/triton-droids/cse-145-237d-tactile-hands)

The MVP was a hand that stops squeezing when it feels enough force. Here it grabs a paper cup and stops closing once the fingertips hit the threshold.

![Force-aware grasp of a paper cup](media/02.gif)

## Hardware

The hand is the [AmazingHand](https://github.com/pollen-robotics/AmazingHand) from Pollen Robotics. It has 4 fingers and 8 [Feetech SCS0009](https://www.feetechrc.com/) servos, two per finger.

We put four [Pololu FSR #2728](https://www.pololu.com/product/2728) sensors on the fingertips. Each one sits in a 22kΩ voltage divider read by an ESP32-S3, which samples its 12-bit ADC and streams force values over USB serial. We built the board on a solderable breadboard with decoupling caps near the ADC, vertical headers for the FSR leads, and some status LEDs, all in a 3D-printed enclosure on the back of the hand.

![FSR fingertip with live force readout over serial](media/01.gif)

## Calibration

FSRs are nonlinear and noisy, so getting trustworthy numbers was the annoying part. We stacked 3D-printed PLA weights on a printed plate and logged raw ADC at seven points. A power-law fit `F = 1.07e-9·r^3.16` came out to 17.1 g RMSE and 25.7 g max error, which is under our 1 N target on all four fingers.

## Force-aware grasping

With force calibrated, the loop sets grip strength from the live fingertip readings. When the force crosses the threshold, a red LED turns on and the grip stops closing. We showed this repeatedly on a paper cup and a few other simple objects, with force logs and video.

The loop reacts to measured force, not predicted force, so a fast close overshoots the threshold. We just close slowly to avoid that. The AmazingHand also doesn't have much reach or grip range, so it does better on bigger objects like a cup than on small ones.

## Reach goals

After the MVP was done at week six, each of us took one reach goal and worked on it in parallel, then integrated at the end.

### Vision

Thomas built a webcam pipeline with MediaPipe Hands and OpenCV. It reads per-finger curl from the tracked joints and maps it to servo commands, so the hand copies your hand.

![MediaPipe Hands skeleton on a tracked hand](media/04.gif)

![Robotic hand mirroring a human hand](media/03.gif)

### Simulation

Ali brought the AmazingHand up in MuJoCo with working finger kinematics and trained an in-hand cube-rotation policy. We didn't get to transfer it to the real hand.

![AmazingHand in MuJoCo](media/05.gif)

### VR teleop

Sidath did the teleop. We started on the Quest 2, but its APK pipeline was a pain to drive from Python, so we switched to Valve Index controllers. They set up much faster with OpenVR and have per-finger tracking. Controller pose streams over ROS 2.

![Valve Index controller pose streaming over ROS 2](media/06.gif)

First we drove the sim with the controller.

<video controls width="100%">
    <source src="media/07.mp4" type="video/mp4">
</video>

<video controls width="100%">
    <source src="media/08.mp4" type="video/mp4">
</video>

### ARCTOS arm

Then we mounted the hand on a 3D-printed [ARCTOS](https://arctosrobotics.com/) 6-DOF arm and drove it over VR teleop. We kept tuning the frame calibration, smoothing, and IK toward pick-and-place.

<video controls width="100%">
    <source src="media/09.mp4" type="video/mp4">
</video>

We also fine-tuned a YOLO26 model on a custom dataset for object recognition. The idea was to give each detected object its own force threshold.

## Possible Future Features

Transferring the in-hand rotation policy from sim to the real hand. That's the big one we didn't get to.

The fingers don't do adduction/abduction yet.

The force loop is purely reactive, so it overshoots on fast closes. Some kind of anticipatory control would fix that.

The arm IK and smoothing still need work before it can do reliable autonomous pick-and-place.
