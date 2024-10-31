---
title: Turing-Complete Module Exports
date: 2024-09-13T14:02:09,000+03:00
url: /mafcv

brief: |
    modules deserve to have their exports easily controlled
draft: true
unlisted: false
---

Everything good in dynamically typed programming languages are things, not yet well expressed by the statically typed ones. I will die fighting on that hill.

## Introduction

All the examples below will be in Python[^python-3.7]. I did my best to avoid verbose syntax and Python-specific semantics. One rule to keep in mind: *everything is an object*. This principle means that everything has members: methods and fields.

This includes everything that would be a primitive in other languages: `int`, `bool`, no one is safe!

```
# `.bit_count()` is a method on integers
# that counts the 1s in the binary
# representation of the number
# 13 is 0b1101

>>> (13).bit_count()
3
```

### Dunder Methods

If a method starts and ends with two underscores, it is called a dunder (**d**ouble **under**score) method. Dunder methods are reserved by the language to implement operator overloading[^operator-overloading], constructors and type coercion and other semantic-level fluff.

```
class Vec2:
    # Python requires an explicit 'this'
    # usually denoted `self` for all 
    # member functions

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(lhs, rhs):
        return Vec2(lhs.x + rhs.x, lhs.y + rhs.y)

a = Vec2(2, 3)
b = Vec2(8, 9)
c = a + b

assert c.x == 2 + 8
assert c.y == 3 + 9
```


One of the things that can be overloaded is member access. If the method `__getattr__` (get attribute) is defined, it will be called whenever an unset member is accessed. For instance, `x.y` is equivalent to using `x.__getattr__(y)` if no member `y` exists on the object `x`.

```
class DictionaryObject:
    # supply the dictionary in the constructor
    def __init__(self, dictionary: dict):
        self._dictionary = dictionary

    # called when a member is accessed
    def __getattr__(self, value: str) -> str:
        return self.dictionary[value]

dictionary = {'foo': 'bar'}
do = DictionaryObject(dictionary)

# accessing a set property
assert do._dictionary is dictionary

# accessing the value for 'foo'
# directly with a method call
assert do.__getattr__('foo')

# `.foo` is unset
# falling back to __getattr__
# key 'foo' resolved from the dictionary
assert do.foo == 'bar'

# `.qua` is unset
# falling back to __getattr__
# key 'qua' is not in the dictionary
# throw an error from __getattr__
assert do.qua
```

Make sure to understand what exactly is happening at every step in the snippet above. Since *everything is an object*, this method can be attached to anything! Notice, how the call to `self.dictionary` does not go through `__getattr__`, because the field is defined on the object in the constructor.

This might seem like an awful idea. Usually, property access is an operation that doesn't mutate anything. It might feel like nothing is sacred anymore and you can't trust a single line of code. That is to some extent true, you can realistically even hide a full-on database call behind the `__getattr__`. However, being horryfing doesn't stop it from being useful. 

Firstly, you can imagine the example above to be a good tool when dealing with JSON data. Sure, a typed model class is better, but it just always is. If that's your only point, go use a type-checked language. For everyone who stayed, 
the class above was deemed useful enough to [be in the standard library](https://docs.python.org/3/library/types.html#types.SimpleNamespace)!

Secondly, keep reading, let me cook.

### Pythonic Modules

A Python module is a file containing definitions. All defined objects inside a module are given to it as properties. It's an object too after all!

```
>>> import math
>>> type(math)
<class 'module'>
>>> math.sin(0)
0.0
```

When something is defined at module-level, it is attached to the module as a member. This is the main tool of code reuse.

```
# example.py
def sqr(x):
    return x * x

>>> import example
>>> maths.sqr(4)
16
```

Module definitions can also be imported in two ways with basically the same underlying implementation.

```
# crude, but valid
import math
sin = math.sin
cos = math.cos

# idiomatic
from math import sin, cos
from example import sqr
```

Since this syntax counts as member access, it can be overriden with the dunder method like in any other object. This is where the magic lies.

```
# counter.py
i = 0
def __iadd__(self, rhs):
    global i
    i += rhs

>>> import counter
>>> counter.__iadd__(2)
>>> counter += 4
>>> counter.i
6
```

Notice how `counter` is not imported from anywhere in particular, instead the import brings the `counter` object itself into the scope and calls the `__iadd__`.


When `__getattr__(...)` is defined at module level, it gets attached to the module as a method upon import. Hence, it is possible to overwrite the attribute access in a module.

```
# attrprinter.py

def __getattr__(self, value):
    print(f"Access to {value}!")

>>> from attrprinter import LionKing, alphabet, _
Access to LionKing!
Access to alphabet!
Access to _!
```


## Use Cases

It makes sense to see how that would work on a practical example. Luckily, a wild occurance of that is in a crate that inspired me to write about this in the first place.

### HTBuilder

[HTBuilder](https://github.com/tvst/htbuilder) ("HT" for "Hyper Text") is a library of functions for declaratively constructing a string representation of an HTML DOM. Instead of listing all the possible tags, it just exports a factory function[^codegolf]:

```
def __getattr__(tag):
    return HtmlTag(tag)
```

This allows using the library as follows:

```
>>> from htbuilder import b, i
>>> hello = b(i("Hello, world!"))
<htbuilder.HtmlElement object at 0x7ffb63da9650>
>>> str(hello)
'<b><i>Hello, world!</i></b>'
```

None of the tags are defined in the file itself[^no-tags-defined], hence it comes with builtin support for all the HTML tags you could want.

This type of trick is *impossible* to encode in any modern statically typed language known to me. The semantics themselves are not too complicated, but treating modules as a *first class value* is not very popular.

### SymPy

[SymPy](https://sympy.org) is a symbolic mathematics library written entirely in Python. it supports everything from basic algebra to calculus and linear algebra, as well as (with some extension) a plethora of [other](https://github.com/bjodah/chempy "Chemistry") [research](https://galgebra.readthedocs.io "Geometric Algebra") [areas](https://lcapy.readthedocs.io/ "Linear... circuit analysis? I'm not even sure what that is").

```
>>> from sympy import symbols, sin, cos, pi
>>> x, y, z = symbols("x, y, z")
>>> expr = cos(x) + sin(y)
>>> expr.subs(cos(x), y)
z + sin(y)
>>> expr.subs(x, 0).subs(y, pi / 2)
2
```

Wonderful stuff. However, pay close attention to the `symbols(...)` call. Doesn't it seem cumbersome to you? Wouldn't it be wonderful to do something like...

```
>>> from sympy.abc import x, y, z
```

Well, behold! You can already do that, the [`abc`](https://docs.sympy.org/latest/modules/abc.html) module is specifically designed to do that, it houses all the usual variables you could need.

One possible issue is that variables under the same name might get mixed up, for instance if we have a parabola and hooke's law meet in the same expression they might get mixed up:

```
# hooke.py
from sympy.abc import x, k
F = -k * x

# parabola.py
from sympy.abc import x
y = x**2 - x - 1


>>> from hooke import F, x as hookes_x, k
>>> from parabola import y, x as pararbola_x

# as expected, the x refers to the same object
>>> hookes_x is parabola_x
True

# J will be our placeholder to see all the substituted locations
>> from sympy.abc import J

# work = force * displacement
>>> W = F * y
>>> W
(-k*x) * (x**2 - x - 1)

>>> W.subs(hookes_x, J)
(-J*k) * (J**2 - J - 1)
```

Oh no! Two variables that were irrelevant got mixed up! Notice how importing them from appropriate modules didn't change anything. To be fair, the same issue could arise on sheet of paper. After all, you are using the same symbol to mean two different things.

In their "[Best Practices](https://docs.sympy.org/latest/explanation/best-practices.html)" section SymPy themselves recommend using the aforementioned `symbols` function to define symbols:

> Define symbols with [`symbols()`](https://docs.sympy.org/latest/modules/core.html#sympy.core.symbol.symbols) or [`Symbol()`](https://docs.sympy.org/latest/modules/core.html#sympy.core.symbol.Symbol). The `symbols()` function is the most convenient way to create symbols. It supports creating one or more symbols at once. ([source](https://docs.sympy.org/latest/explanation/best-practices.html#defining-symbols))

As of writing this, the implementation defines all the symbols inside `abc` [manually](https://github.com/sympy/sympy/blob/9f8a5d50c675a9a677f873180b1b067cff7ce4ba/sympy/abc.py#L64-L80). Beyond that, it also contains a note describing the easiest way *to avoid typos* in the variable names! I wish there was a way of avoiding that.

``` 
def __getattr__(self, var: str):
    return Symbol(var)
```

The snippet above effectively cuts out circa 30% of the code in the file without breaking compatibility. Lovely, isn't it?

### Pint

[Pint](https://pint.readthedocs.io/) brings units to Python. Meters, newtons, gigaparsecs per hertz - you can have them all!

### Express.js

JS? I thought this post only uses Python.

While I'm sure that this specific mechanism appears in some Python packages too, I don't know any specific examples of that. Besides, the syntax is rather transparent.

```
import express from 'express';
import { createClient } from 'redis'; 

let app = express();
let db = createClient();
```

Woah! Or not, it may not jump at you the first time you look at this. Let me rewrite this one in Python.

```
import express
from redis import create_client

app = express()
db = create_client()
```

Woah indeed! For `express` we are calling the module itself, instead of importing it like for `redis`. Queer. This is a bit different from overriding the attribute getter, but the magic words are almost the same. The Pythonic version would use the `__call__` dunder method. It defines the semantics of calling the object. *Everything is an object*, remember? Even functions.

We can replicate this in terms of a classic web framework `Flask`. The code below simply proxies the call of the module to 

```
# flask.py
__call__ = Flask

>>> import flask
>>> app = flask()
```

## Conclusion

As I argued previously, this concept does not exist in the modern programming languages. Can we at least come up with a name for it? This concept is not even googleable.

*P.S. Actually, if you read this far and come up with a nicer name, send it to me and I'll change the article -- <artur.roos@ktnlvr.dev>.*

[^python-3.7]: The specific version used is Python ≥ 3.7, since it is the earliest version that allows the sourcery that I'll be demonstrating.
[^operator-overloading]: This type of overloading is very useful when it comes to representing mathematical objects. It can be argued that it's bad practice, since you never know how the underyling operation is used, but that is really only noticeable in severe cases like the [`std::ostream::operator<<`](https://en.cppreference.com/w/cpp/io/basic_ostream/operator_ltlt) in C++. 
[^get-attr]: There are actually two dunder methods with similar functionality: `__getattr__` and `__getattribute__`. The former is invoked when looking up actual properties on an object failed. The latter is used to override the standard lookup.
[^no-tags-defined]: Well, it defines a list of `EMPTY_ELEMENTS` for self-closing elements like `<br>` and `<img>`, but that information can not be derived from the property name alone.
[^codegolf]: Actually, this can be done even more compactly: `__getattr__ = HtmlTag`
