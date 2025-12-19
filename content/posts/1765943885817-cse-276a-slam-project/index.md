---
title: "SLAM from Scratch"
date: 2025-12-17
draft: false
description: "CSE 276A Class Project"
tags: ["robotics"]
---

### GitHub Repo: [github.com/bhackel/rubikpi_ros2](https://github.com/bhackel/rubikpi_ros2)

# SLAM from Scratch

This project covers implementing a complete SLAM pipeline using an Extended Kalman Filter, from dead-reckoning and AprilTag localization to occupancy grid mapping and autonomous coverage planning on a differential-drive robot.

The codebase is a mix of Python and C++ with ROS2 Jazzy.

The hardware platform is a Waveshare Wave Rover differential-drive base with a Rubik Pi 3 running the control software. A Raspberry Pi camera module provides the sole sensor input for AprilTag-based localization in the 10ft x 10ft workspace.

### Final Results

The final system demonstrates autonomous coverage of the space. The robot uses a combination of EKF SLAM localization and smart planning to visit all explorable cells in the occupancy grid while maintaining localization accuracy within ±10cm.

<iframe width="560" height="315" src="https://www.youtube.com/embed/y-iNzdthmXc" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Project 1: The Basics

The 1st project is a simple dead-reckoning-based waypoint navigation. I performed basic calibration by measuring the motor's average speed when commanding a certain float value.

<iframe width="560" height="315" src="https://www.youtube.com/embed/FrbNmGu4ps4" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Project 2: Simple Localization

The 2nd project significantly scaled things up with AprilTag-based localization on top of dead-reckoning. Here I used a prebuilt tag localization library to make things easier, and wrote code to take the tag's position in the camera frame and transform it backwards to understand the robot's pose in the world frame. I also performed camera calibration to drastically improve the accuracy of the localizations.

![Hw2 Map](images/hw2%20map.png)

<iframe width="560" height="315" src="https://www.youtube.com/embed/TlwX7WG_nHs" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Project 3: Raw SLAM

The 3rd project is where the challenges began. We developed our own EKF SLAM implementation for our specific robot. This included the general Predict + Update steps based on our robot's kinematic model, and also specific values for our system noise matrix Q and measurement noise matrix. We performed 40 calibration tests for calculating uncertainty in linear and angular velocity, and uncertainty in the camera's ability to accurately localize AprilTags.

For SLAM, we selected an Extended Kalman Filter over particle filter approaches. While particle filters excel in non-Gaussian environments and handle multi-modal distributions well, our sparse AprilTag setup with few landmarks and known starting position made the EKF's Gaussian assumption reasonable.

![HW3 Map](images/hw3%20map.png)

Our results showed significant improvement, with an average tag localization error of 17cm after one pass, which was down from approximately 40-50cm before camera calibration.

![HW3 Results](images/hw3%20results.png)

One issue we struggled to solve was off-axis localization. For tags that are towards the edges of the camera view, the tag localization code would consistently believe the tags were much further away than they actually are. We avoided this issue by restricting our camera's field-of-view to around 60 degrees, but a better solution would be preferred. We tried recalibrating the camera multiple times, even using an extremely planar calibration surface, but still struggled to get good measurement accuracy for these cases. The evidence pointed toward limitations in the camera calibration model itself. We believe the standard pinhole camera model with radial distortion correction likely doesn't fully capture our lens's behavior at extreme angles.

<iframe width="560" height="315" src="https://www.youtube.com/embed/A2PRGUle0nY" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Project 4: Path Planning

The 4th project focuses on path planning. An obstacle is added into the center of the workspace to block the robot, which must be navigated around.

![HW4 Map](images/hw4%20map.png)

Here we implemented a Probabilistic Roadmap Planner. Our custom algorithm randomly samples collision-free configurations, builds a k-Nearest-Neighbors roadmap for each point, then runs Dijkstra's algorithm on the graph to find the shortest path. An important parameter in our algorithm is the `safety_margin`, which is a radius representing the allowed boundary between the robot and any obstacles. We adjust the safety margin to be the robot's radius to generate a fast path, and increase it to generate the safest path.

We chose PRM as a learning exercise to understand sampling-based motion planning. For our case with a static obstacle, simpler approaches like A\* would have worked equally well, but implementing PRM from scratch provided deeper insight into configuration space sampling and graph-based planning techniques.

![HW4 Paths](images/hw4%20path%20planning.png)

The video for this project shows an impressive fast-path result where the robot sneaks past the obstacle.

<iframe width="560" height="315" src="https://www.youtube.com/embed/3p6C6o8Oi9U" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Project 5: Putting it All Together

The 5th and final project combines concepts from all previous projects together to create a performance-guarantee. The idea is to drive the robot around the entire workspace and guarantee that our implementation can cover the entire area with some accuracy.

![Hw5 Progression](images/hw5%20filling%20the%20grid.png)

At the core of our system is a 2D occupancy grid. At the start, the node requests the area bounds from the EKF SLAM node. The area is discretized into 10cm by 10cm cells. Each cell is in one of 3 states: UNVISITED, VISITED, and WALL. On each update (10Hz), all cells in the robot's footprint are marked as VISITED.

For navigation to each cell, we search for cells in an increasing radius around the robot. The highest priority level is avoiding WALL cells, such that we do not drive out-of-bounds. The next level scores the cells at the current radius according to factors like heading alignment and neighbor density to make the process more efficient. In the case where no UNVISITED cells are found, we simply drive randomly.

![hw5 control flow](images/hw5%20control%20flow.png)

The goal here is to mimic a Roomba-type robot to cover the entire space. Prioritizing cells in front of the robot reduces the need to turn and subsequently lose localization accuracy. We prioritize cells with few VISITED neighbors to get more coverage faster. Finally the random walk at the end means that a user who is not satisfied with the cleaning performance can simply let the robot to continue to run.

<iframe width="560" height="315" src="https://www.youtube.com/embed/y-iNzdthmXc" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


## Unexpected issues

During development especially during the early stages we encountered many unexpected issues:

1. Battery charge affects motor speeds

    When calibrating the dead-reckoning linear and angular velocity, we found that over the few hours of testing, our results would slowly drift down. We ultimately determined that swapping in a new battery every 2 hours significantly improved the consistency, especially with turning speeds.

2. Franklin Antonio Hall Wi-Fi is terrible

    When starting out on Project 3, we spent a full 6 hours debugging Wi-Fi issues on the robot related to the building's poor connectivity. We ended up just moving our space somewhere else since the time spent hunting for a quiet 10ft x 10ft tile area was less than debugging the terrible Wi-Fi.

3. Skid-Steer without Skidding
    
    For a strange reason the robot is a 4-wheel differential drive model but with rubber traction wheels. This meant that we needed to add tape around the wheels so that we could turn in-place by commanding one side forward and one side backwards. We eventually settled on some male Velcro-like tape that significantly reduced wheel friction and drastically improved our turning. 
