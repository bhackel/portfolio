---
title: "(WIP) Low-cost High-DoF Hand"
date: 2026-06-23
draft: false
description: ""
---


Robot hands have fallen into two main camps. One is tendon based, like Shadow Hand and Optimus's hand. The other is micro-servo based, which I see more short-term potential in.

The issue is these hands are **extremely expensive** for some reason. The Wuji hand is $16,000.

If one wants to DIY one, you need compact servos. Therefore you look to Dynamixel, who is leading the industry. These new **XM335** servos compose the Robotis hand and are **$190** each.

![Robotis hand](media/robotis-hand.gif)

![Dynamixel XM335 servo](media/xm335.png)

I see that price and think, theres no way!? Then I am reminded of the humble 9g micro servo, which sells for below $1 each. I think there's a great opportunity for a low-cost hobbyist hand using this.

However, **the 9g servo is not the correct shape**.

![9g (S90G) servo motor parts](media/s90g-servo-parts.jpg)

The only existing work I found so far is this. However this design has 2 major flaws. First, it uses less-than-9g servos to solve the 9g-doesnt-fit issue. This means significantly less output torque, which is why it can only do hand signing. Secondly, the servo mounting is not stable, as it only uses the servo horn as the attachment point.

[This DIY Robotic Hand Can Sign the Entire ASL Alphabet Ambidextrously](https://www.hackster.io/news/this-diy-robotic-hand-can-sign-the-entire-asl-alphabet-ambidextrously-39eb87103383)

![DIY robotic hand signing the ASL alphabet](media/asl-hand.jpg)

Therefore I want to make 9g servos work, for both lower cost and higher torque.

I noticed a large open-air gap in the motor. If we can reorient the DC motor 90 degrees, we can gain that space back, and get the correct servo profile.

Below is a rough CAD of what that consists of. The first gear connecting the DC motor to the gearbox will be replaced by a crown gear. Then, the motor can be reoriented to save space.

![Reorienting the DC motor 90 degrees](media/motor-reorient.png)

![Resin print (left) vs FDM print on the X1C (right)](media/print-comparison.jpg)

These gears have extremely tiny teeth, which means cheap FDM printing unfortunately cannot be used. Resin printing is necessary to get the fine details of the gear teeth for good gear meshing, especially at the high expected speeds.


### Some unsorted pictures

![Wuji 2 motor locations](media/wuji-motor-locations.png)

![Wuji 2 gear reductions](media/wuji-gear-reductions.png)

![Wuji 2 worm gear](media/wuji-worm-gear.png)

{{< youtubeLite id="j6EWW0fvo30" label="Wuji Hand: What's Different in Its Design? With Scott Walter and Marwa ElDiwiny" >}}

{{< youtubeLite id="7QYedp3ozjw" label="Yield over Strength, Stand over Time | Wuji Hand 2" >}}



[ROBOTIS Hand Series](https://www.robotis.us/robotis-hand/)

[DYNAMIXEL XM335-T323-T](https://robotis.us/xm335-t323-t/)


