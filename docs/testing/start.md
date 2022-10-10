---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# How to test a Plone add-on

To better understand how to test a Plone add-on, the best thing is to create a new Plone package from scratch
and use it to see different testing techniques.

We are going to use the [plonecli](https://pypi.org/project/plonecli/) tool heavily because it lets you create new Plone packages
and related features such as content types, views, and vocabularies, all using simple commands.

## Create Package

First, we need to install plonecli:

```shell
pip install plonecli --user
```

```{note}
This command will install plonecli in the user site-packages according to the official documentation.
Feel free to install it using your preferred alternative method (virtualenv, pipenv, pyenv).
```

```{note}
If you have already installed plonecli, please update at least bobtemplates.plone to the most recent version (>= 5.0.1) because there are
some important fixes needed for this training.
```

Now we can create a new package:

```shell
plonecli create addon plonetraining.testing
```

## Buildout

Run buildout:

```shell
cd plonetraining.testing
plonecli build
```

```{note}
This command will create a virtualenv, install dependencies and run buildout.
```

Let's run some tests! plonecli provides some default tests when creating a new package:

```shell
plonecli test
```

Let's run all tests, including robot tests (we will cover these later):

```shell
plonecli test --all
```

```{note}
If you get an error about missing `geckodriver`, you will have to install `geckodriver`.
On macOS, you can use `brew install geckodriver`.
On Ubuntu, you can use `apt install firefox-geckodriver`.
Then re-run `plonecli test --all`.
```
