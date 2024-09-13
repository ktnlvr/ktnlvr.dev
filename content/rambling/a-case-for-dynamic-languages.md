---
title: A Case for Dynamic Languages
date: 2024-09-13T14:02:09,000+03:00
url: /acfdl

brief: |
    dynamic features tell us what static features are ought to be
draft: false
unlisted: true
---

Everything good in dynamically typed programming languages are things, not yet well described by the statically typed ones.

## HTBuilder

In Python everything is an object. All has attributes: properties and methods. If a method starts and ends with two underscores, it is called a dunder method. Dunder methods are reserved by the language to implement functionality like operator overloading, constructors and type coercion.

```
def __getattr__(self, attr: str):
    return ...
```

The dunder method above implements allows overriding attribute access[^get-attr]. Using `x.y` maps to `x.__getattr__(y)` if `x` does not have a method or a property `y`. Since *everything is an object*, this method can be attached to anything at definition- or run-time.

A Python module is a file containing Python statements. All defined objects inside a module are given to it as properties. A module is an object too.

```
Python 3.11.2 (main) [GCC 12.2.0] on Linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import math
>>> type(math)
<class 'module'>
>>> math.sin(0)
0.0
```

When `__getattr__(...)` is defined at module level, it gets attached to the module as a method upon import. Hence, it is possible to overwrite the attribute access in a module.

Module definitions can also be imported in two ways with basically the same underlying implementation.

```
# crude, but valid
import math
sin = math.sin
cos = math.cos

# pythonic
from math import sin, cos
```

Since this syntax counts as member access, it can be overriden with the dunder method explored above.

[HTBuilder](https://github.com/tvst/htbuilder) ("HT" for "Hyper Text") is a library of functions for declaratively constructing a string HTML DOM. Instead of listing all the possible tags, it just exports a factory function:

```
def __getattr__(tag):
    return HtmlTag(tag)
```

This allows using the library as follows:

```
>>> from htbuilder import b, i
>>> b(i("Hello, world!"))
<htbuilder.HtmlElement object at 0x7ffb63da9650>
>>> str(_)
'<b><i>Hello, world!</i></b>'
```

None of the tags are defined in the file itself[^no-tags-defined], hence it comes with builtin support for all the HTML tags you could want.

This type of trick is *impossible* to encode in any modern statically typed language. The semantics themselves are not too complicated, but treating modules as a *first class value* is not known to me.

## Polyfill

> A polyfill is a piece of code (usually JavaScript on the Web) used to provide modern functionality on older browsers that do not natively support it. -- [The MDN Glossary](https://developer.mozilla.org/en-US/docs/Glossary/Polyfill)

## SpongePowered Mixins

[^get-attr]: There are actually two dunder methods with similar functionality: `__getattr__` and `__getattribute__`. The former is invoked when looking up actual properties on an object failed. The latter is used to override the standard lookup.
[^no-tags-defined]: Well, it defines a list of `EMPTY_ELEMENTS`, but that information can not be derived from the property name alone.
