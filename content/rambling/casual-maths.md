---
title: Casual Maths
date: 2024-09-15T14:24:40,000+03:00
url: /cm

brief: |
    my encounters with mathematics in a casual setting
draft: false
unlisted: true
---

The question of "is math really useful?" keep cropping up in my life.

Here, by math I mean calculus, logic, geometry or anything else, where a not immediately intuitive solution to a problem can be guided by the forces of mathematical rigor alone.

The examples below are not intended to be complex. 

## USB Drive Transfer

I wanted to move a large file from my computer to an ancient flash drive. The file was 6.1 GB (= 6100000Kb) and the initial transfer speed was 271 kB/s. As time went on, the speed would decrease over time. The process was taking a while and I wanted to estimate when it will be finished.

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

\[t_0 = 0, t_1 = 12024\]

\[v_0 = 271, v_1 = 246\]

\[\Delta v = \dfrac{v_1 - v_0}{t_1 - t_0} = \dfrac{246 - 271}{12024 - 0} = -0.002 (kB/s)\]

From here, we know the acceleration and hence can apply the familar formula from physics:

\[s = s_0 + v_0t + \dfrac{a t^2}{2}\]

\[6100000 = 0 + 271t + \dfrac{-0.002t^2}{2}\]

Plugging everything into a calculator and solving for `t` yields 24774 seconds, or just shy of __7 hours__.

## Cash Change
