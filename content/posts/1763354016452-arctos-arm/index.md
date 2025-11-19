---
title: "ARCTOS Arm"
date: 2025-09-17
draft: false
description: "Assembling 6-DOF 3D-Printed Open Source Robotic Arm"
tags: ["robotics", "3d printing"]
---



# ARCTOS 6-DOF 3D-Printed Robotic Arm Assembly

During the summer, I took over assembly and electrical
wiring work for my friend's robotic arm project. The
following article describes the month-long process of
various assembly challenges. 

![Naked robot arm](media/IMG_4743.jpeg)

I received the arm like this. The two cycloidal gearboxes were assembled, but the arm was not attached to the base, and none of the stepper motors, hall-effect sensors, or belts were installed.

![First stepper](media/IMG_4749.jpeg)

I began by routing the 2 power and 2 CAN wires from the base of the robot. Then, I spliced off dedicated wires to the first motor. This splicing technique was something I did not see many people doing for the ARCTOS, but it gives much cleaner wiring than WAGO clips.

![2nd Motor Wiring](media/IMG_4762.jpeg)

![3rd Motor Wiring](media/IMG_4761.jpeg)

I followed with the 2nd and 3rd motors, carefully routing the wire through the robot, and splicing off. At this point, I attached the top to the base and installed the motors with a little difficulty.

![4th Motor Gearbox](media/IMG_4764.jpeg)

With the easy things out of the way, next up was installing the 4th motor planetary gearbox. This caused significant issues because the design or assembly was misaligned, and the gearbox did not fit properly.

<video controls width="100%">
    <source src="media/IMG_4765.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

To solve this, I used a spade drill bit and did some serious damage.

![Carnage](media/IMG_4767.jpeg)

Luckily, eventually everything fit together. Don't mind the damage.

<video controls width="100%">
    <source src="media/IMG_4781.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

At this point, I wanted to see some arm movement, so I set up the software to connect to the CAN bus and sent a basic motion command for all joints.

<video controls width="100%">
    <source src="media/IMG_4864.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

The next stage was the trickiest part of the entire build. Although the assembly steps for this were relatively simple, I struggled immensely to get the planetary gearboxes to turn consistently.

<video controls width="100%">
    <source src="media/IMG_4835.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

To improve the smoothness of the gearbox, some users suggested spinning the parts quickly with a drill. This helped, but ultimately I just reprinted on a Bambu printer and it fixed all my problems.

![Hall sensor](media/IMG_4868.jpeg)

After this, I began installing some of the hall-effect sensors.

<video controls width="100%">
    <source src="media/IMG_4869.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

This let me test the homing of the first axis, which worked great and started the ability of the robot to go to chosen angles.

<video controls width="100%">
    <source src="media/IMG_4989.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

I then installed the gripper, which went smoothly. The strength was impressive, but the current draw seems high and I think will cause damage in the future.

<video controls width="100%">
    <source src="media/IMG_4921.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

One unsolved problem is the C cycloidal gearbox making crunching sounds when running. I believe there is some mis-assembled disc that is snapping past the metal bars. The fix will require a re-assembly at some point.

![Outside](media/IMG_5053.jpeg)

As I finished before class started, we used the robot for club tabling to attract new members. Yay