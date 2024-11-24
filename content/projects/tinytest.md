---
title: tinytest
date: 2022-04-22T22:26:00,000+03:00
publishDate: 2023-03-20T00:27:27,486059205+02:00
aliases:
     - /tt

brief: miniscule zero-external-dependency C99 testing library
link: https://github.com/ktnlvr/tinytest
---

## What is `tinytest`?

Sometimes you just feel like throwing something together. When the something involves ancient runes like C[^for-int] you usually also want some tests in place, so if you mess up some allocations they get caught before th runtime is shipped[^rust?]. 

My initial instinct of using something more standard like gtest was mitigated by my desire to write 0 boilerplate. 

As always, the solution was reinventing the wheel.

## How does it work?

### Extraction

When you build your C file as a shared library your functions don't get mangled. That means that they retain the original name assigned to them, which is great for my purposes. Tinytest dynamically links the testable file to itself looking for all functions prefixed with `"tinytest_test__"`[^prefix].

Those functions are stored into a dynamically sized array relying on `malloc` and `realloc` to allocate heap space. All the test functions are assumed to match `void(void)` signature. 

For convinience and readability there is also a macro: `#define TINYTEST_TEST(name)`.

### Evaluation

When storing the test into the array test is uniquely identified the name of the test (the bit after the prefix)[^which-bit], a function pointer to the linked function and the original function's name. My initial though was to use regex, but that felt like an overkill.

After all tests are collected it runs them one by one in the main thread. Before running each test a jump buffer[^jump-buffer] is set up. If the test receives one of 5 signals[^signals] it is considered failed and the program moves on, by jumping to the jump buffer. This mechanism can be used to handle exception, so it behaves similarly in my case.

### Reporting

When all tests are ran, the results are printed in a nice colourful way using ANSI Terminal Control Codes[^ansi-term-codes]. The result includes whether the test was passing or not and the signal received. The colour can be turned off by a compilation flag `-DTINYTEST_CNF__NO_COLOR`[^cnf]. The total amount of successful tests is also tallied up and displayed. If at least one of the tests failed the colour will be red, otherwise green.

```
001: began executing always_passes
     always_passes passed...
002: began executing zero_division
     division by zero
     zero_division failed...
003: began executing illegal_instruction
     caught illegal instruction
     illegal_instruction failed...
004: began executing segfault
     segmentation violation
     segfault failed...
005: began executing abort
     abort signal was triggered
     abort failed...
Results: 1/5. Passing rate: 0.200
```

## Design Choices

### Commit Messages

At the time I was really into semantic commit messages. They require that all commits are prefixed with a type, like "`feat`", "`fix`", "`chore`", "`docs`" and so on. However, I find that they mostly clutter the git history. 

I don't find that when building a project alone they are of any benefit. Perhaps when running `git bisect` they might give up the bug culprit earlier?

### Language Version

There is something charming about making something as barebones. Modern programming languages have massive standard libraries[^C#-stdlib], but seing a thing so barebones work without difficulty is beyond enjoyable.

Sure, the actual OS might have been compiled with another C[^linux-kernel-c11], but the ABI is compatible.

## Conclusion

Even though this project is small I am still proud of it. I got to work with the ELF executable format, which I have never done before. *Looking for documentation was fun*. Even though it is not a production-ready project, it nevertheless is one that I put a lot of effort into. It is lacking a lot of the features modern testing engines include: IDE Support, Test Groups, Asserts & Expects, Multithreading, Backtracing. Due to that I will most certainly use `gtest` in my future endeavours. It is a frankenstein monster of different obscure C libraries, coming together as something compact and neetly functional. Love it! I should do more C.

[^rust?]: At the time I didn't know/care about Rust.
[^prefix]: [Here](https://github.com/Kittenlover229/tinytest/blob/f628854/tinytest.c#L70) you can see the line!
[^ansi-term-codes]: [Here](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#colors--graphics-mode) you can find more information about ANSI terminal codes.
[^cnf]: `CNF` presumably stands for **c**o**nf**ig. Weird abbreviation. 
[^signals]: [These ones](https://github.com/Kittenlover229/tinytest/blob/f628854e1d2d506f8406f7f63026552257b0ceda/tinytest.c#L105) to be specific.
[^which-bit]: The bold bit here exactly `tiny_test__`__`testname`__`__`.
[^jump-buffer]: [Link](https://en.cppreference.com/w/cpp/utility/program/setjmp) to the jump buffer on cppreference, not quite C but close enough.
[^for-int]: Initially the project was intended to be ANSI C (aka C89), but not having `for(int i = 0;` was bugging me too much. 
[^C#-stdlib]: Looking at you, C#
[^linux-kernel-c11]: As of writing this post, the version was C11. Check for yourselves [here](https://www.kernel.org/doc/html/latest/process/programming-language.html).
