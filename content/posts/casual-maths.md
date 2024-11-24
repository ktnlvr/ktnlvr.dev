---
title: Casual Maths
date: 2024-09-15T14:24:40,000+03:00
aliases:
    - /cm

brief: |
    my encounters with mathematics in a casual setting
draft: true
---

The question of "is math really useful?" keep cropping up in my life.

Here, by math I mean calculus, logic, geometry or anything else, where a not immediately intuitive solution to a problem can be guided by the forces of mathematical rigor alone.

The examples below are not intended to be complex. 

## USB Drive Transfer

I wanted to move a large file from my computer to an ancient flash drive. The file was 6.1 GB (= 6 100 000 Kb) and the initial transfer speed was 271 kB/s. As time went on, the speed would decrease over time. The process was taking a while and I wanted to estimate when it will be finished.

Luckily, the command also output seconds taken in real time so the progress was essentially timestamped:

| time (s) | speed (kB / s) |
| -------- | -------------- |
| 0        | 271            |
| 1661     | 264            |
| 3679     | 258            |
| 7027     | 252            |
| 11382    | 247            |
| 12024    | 246            |

The speed change looked linear enough, so we can get a rough slope over time. The change in velocity will be the difference of velocities over time. We can take

$$t = 12024$$

$$u = 271, v = 246$$

$$\Delta v = \dfrac{v - u}{t} = \dfrac{246 - 271}{12024} = -0.002 (\text{kB/s})$$

From here, we know the acceleration and hence can apply the familar formula from physics:

$$s = s_0 + v_0t + \dfrac{a t^2}{2}$$

$$6100000 = 0 + 271t + \dfrac{-0.002t^2}{2}$$

$$0 = -\dfrac{0.002t^2}{2} + 271t - 6100000$$

$$t = \dfrac{-271 \pm \sqrt{271^2 - 4 \cdot 6100000 \cdot (-0.002)}}{-6100000}$$

Plugging everything into a calculator and solving for $t$ yields $24774$ seconds, or just shy of __7 hours__.

Not all mathematical models are accurate to the world. An hour after taking the last measurement my laptop ran out of charge and the flash drive got irepparably corrupted.

## Cash Change

## Sandwich Curse

I don't have ingredients for sandwiches at home. Every time I buy them, I will have something leftover. This in turn motivates me to buy enough stuff to make more sandwiches, which in turn leaves something else leftover. The following problem is inspired by that conundrum.

When making a sandwich, you take 2 slices of bread, 1 piece of cheese and 3 pieces of lettuce. One loaf is split into 13 slices. One cheese wheel can be sliced into 17 pieces. One lettuce head contains circa 23 leaves.

Question: if you have an infinite supply of additional loaves, wheels and heads, how many sandwiches will you make before you run out of all the ingredients?

## Pizza Pizza Pie

This problem is two-part. A local pizza place sells $25\text{cm}$ pizzas for $16.5 \text{ EUR}$ and $35 \text{cm}$ pizzas for $28 \text{ EUR}$. Should you order 2 of $25 \text{cm}$ or 1 of $35 \text{cm}$? If each pizza has a $1\text{cm}$ border, how does that influence your decision?

A twist on a very classic problem. To solve the first question, we just calculate the area of each pizza and divide it by the cost. Let's understand the values that we are given: $d_1 = 25$ and $d_2 = 35$ for the diameters of the first and the second pizza respectively. $p_1 = 16.2$ and $p_2 = 28$ for the prices. The area of a circle is $A = \pi r^2$. By definition, radius is half of diameter, so substituting $r = 0.5d$ we get $A = \dfrac{\pi d^2}{4}$. Then we can calculate the pizza per price as follows:

$$x_1 = \frac{A_1}{p_1} = \dfrac{\pi d_1^2}{4 p_1} \approx \dfrac{3.14 \cdot 25^2}{4 \cdot 16.5} \approx 29.73 \frac{\text{cm}^2}{\text{EUR}}$$

Same can be done for the second pizza:

$$x_2 = \frac{A_2}{p_2} = \dfrac{\pi d_2^2}{4 p_2} \approx \dfrac{3.14 \cdot 35^2}{4 \cdot 28} \approx 34.34 \frac{\text{cm}^2}{\text{EUR}}$$
