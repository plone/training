---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Unit tests

Unit tests are the first type that we are going to cover.

They are the quickest to run and the easiest to write because they don't need special environments or configuration to be executed.

We are going to use a Python unit testing library called `unittest`.

```{note}
More detailed documentation can be found in the [unittest documentation](https://docs.python.org/2.7/library/unittest.html).
```

## Create our first unit test

First, we create a new file in the `tests` folder.

Let's call it `test_unit.py`:

```{literalinclude} _snippets/test_unit.py
:language: python
:lines: 1, 4-11
```

Now we run it:

```shell
bin/test
```

If we are working on a single test and we don't want to run all our tests, we tell the testrunner which test to run:

```shell
bin/test -t test_a_feature
```

### Exercise 1

Create a new test and play with assertions (try also to make your assertions fail, to see what happens and to view the traceback information useful for debugging).

### Exercise 2

If in your package there are some helper methods that don't need CMS, Zope, or Plone features but they simply transform an input into an output, you could import them and test them in an unittest.

Create a new file in our package with a method that takes a number and returns this number multiplied by 2, and then write an unittest for this.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

File `helper_functions.py`:

```python
# -*- coding: utf-8 -*-

def double_number(x):
    return x * 2
```

In `tests/test_unit.py`:

```{literalinclude} _snippets/test_unit.py
:emphasize-lines: 3,13-16
:language: python
```
````
