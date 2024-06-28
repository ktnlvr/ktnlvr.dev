---
title: 1brc
date: 2024-06-27T11:41:10,000+03:00

brief: parsing 1 billion (with a b) rows of temperature data
link: https://github.com/ktnlvr/1brc
draft: true
unlisted: true
---

## Problem Statement

There is a randomly generated UTF-8 text file with ~1B lines formatted like `station;temperature\n`. Find the per station maximum, minimum and average. Display them in alphabetical order. Sample data:

```
Hamburg;12.0
Bulawayo;8.9
Palembang;38.8
Hamburg;34.2
St. John's;15.2
Cracow;12.6
```

## Making the data

Usually for problems like these the data standard is well-defined. Challengemakers for events like [Advent Of Code](https://adventofcode.com/) go to great lengths to ensure that the data format is well-understood. Websites like codeforces show bounds on the input data, which was not the case here.

For instance, the displayed data has one decimal of precision. Not significant figures, just one decimal place. Is all data like this? Given the data is from real world, we can also ask trivia questions. Is this Celcius or Fahrenheit? Or Kelvin and everyone is frozen to death? Or maybe this is a legacy system written in COBOL and it produces only Rankine? Sadly the dataset doesn't answer.

I will assume that the data will always be given with one decimal place of precision. I will also assume that negative values are possible in the range from the coldest to the hottest temperatures in the world. As of writing this, the coldest is `-89.2°C` and the hottest `56.7°C`.

### Distribution

Temperature[^temperature-normal] tends to be normally distributed. The [Python](https://github.com/gunnarmorling/1brc/blob/main/src/main/python/create_measurements.py) generator for the original challenge, however, assumes that the data is uniform. I will be using a generator with normally-distributed datapoints, simply because I find it more interesting. I can also compare the calculated average to the mean and see how many standard deviations away my maxima and minima are.

For debugging purposes, the randomizer is seeded with `69420` and equipped with its own naive (slow) python implementation.s

### What about `-0.0`?

When testing the generator I noticed that some temperature values showing up as `-0.0`, which is, of course a totally expected behaviour I thought about.

## Implementation

'Countertests'[^kapun] are integral to competetive programming, they create the data in such way that it slows down or breaks a specific algorithm, prevent the test from passing. Luckily, the world usually doesn't countertest, so I will not be considering them.

### `mmap`? `mmap`.

### Caveat emptor

[^kapun]: [An algorithm](https://codeforces.com/blog/entry/99973) that counters [polynomial hashing](https://codeforces.com/blog/entry/100027)
[^temperature-normal]: [This seems like a credible source](https://archive.ipcc.ch/ipccreports/tar/wg1/088.htm), it shows diagrams of temperature being normally-distributed.