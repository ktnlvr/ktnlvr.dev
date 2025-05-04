---
title: Operator Overloading Bad
date: 2025-05-04T20:12:14,000+03:00
aliases:
    - /oob

brief: |
    How I instantly lost faith in operator overloading
---

[Enough](https://odin-lang.org/docs/faq/#why-does-odin-not-have-operator-overloading) [has been](https://cafe.elharo.com/programming/operator-overloading-considered-harmful/) [said](https://pages.cs.wisc.edu/~fischer/cs538.s08/lectures/Lecture08.4up.pdf) about how bad Operator Overloading is. This is the specific case that turned me into its hater.

```
# timestamp = "2025-05-04T20:12:14,000+03:00"
date, time = timestamp.split('T')

Y, M, D = date.split("-")
h, m, *_ = time.split(":")
Y %= 2000
```

Ignore how bad of an idea it is to do this little error handling. Granted, the error is partially faciliated by Python's lack of static typing. Cudos to one who have already spotted the mistake. For those who haven't, here's the error message:

```
TypeError: format string didn't convert all arguments
```

This should raise some eyebrows. It is honest and it being a `TypeError` is expected, after all the variables are strings. Anyone who used Python before 3.6 should already know whats up[^fstring].

Before syntax like `f"{Y}-{M}-{D}"` was possible, you would have to write something like `"%d-%02d-%02d" % (Y, M, D)`. This syntax has lingered on from **Python 1**, released in **1991**. I guess the percentage symbol for the formatting operator is in reference to the percentage symbol prepending the value placeholders, which are in turn a holdover from **1973**. 

Knowing that a feature from *50 years ago* caused a bug in my code instills in me some sort of primordial honor.

In the snippet from above the `%` is actually trying to do an in-place formatting of the string, trying to find a value placeholder to insert the `2000` into. This could have been prevented if a simple `.format` was preferred.

Please, unless you are doing math, collections or Haskell, don't use operator overloading.

[^fstring]: Bit of a spoiler, but f-strings were introduced in [Python 3.6](https://docs.python.org/3/whatsnew/3.6.html#pep-498-formatted-string-literals).
