---
myst:
  html_meta:
    "description": "How to set up the training locally"
    "property=og:description": "How to set up the training locally"
    "property=og:title": "Building and Checking the Quality of Documentation"
    "keywords": "Build, Check, quality, documentation"
---

(setup-build-label)=

# Building and Checking the Quality of Documentation

This document covers how to build the Training documentation and check it for quality.


(setup-build-installation-label)=

## Installation

(setup-build-installation-python-label)=

### Python

Python 3.8 or later is required.
A more recent Python is preferred.
Use your system's package manager or [pyenv](https://github.com/pyenv/pyenv) to install an appropriate version of Python.


(setup-build-installation-vale-label)=

### Vale

Vale is a linter for narrative text.
It checks spelling, English grammar, and style guides.
Plone documentation uses a custom spelling dictionary, with accepted and rejected spellings in `styles/Vocab/Plone`.

Use your operating system's package manager to [install Vale](https://vale.sh/docs/vale-cli/installation/).

Vale also has [integrations](https://vale.sh/docs/integrations/guide/) with various IDEs.

-   [JetBrains](https://vale.sh/docs/integrations/jetbrains/)
-   [Vim](https://github.com/dense-analysis/ale)
-   [VS Code](https://github.com/errata-ai/vale-vscode)

Plone documentation uses a file located at the root of the repository, `.vale.ini`, to configure Vale.
This file allows overriding rules or changing their severity.

The Plone Documentation Team selected the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/) for its ease of use—especially for non-native English readers and writers—and attention to non-technical audiences. 

```{note}
More corrections to spellings and Vale's configuration are welcome by submitting a pull request.
This is an easy way to become a contributor to Plone.
```

(setup-build-installation-clone-plone-training-label)=

### Clone `plone/training`

Clone the Plone Training repository, and change your working directory into the cloned project.
Then with a single command using `Makefile`, create a Python virtual environment, install project dependencies, build the docs, and view the results in a web browser by opening `/_build/html/index.html`.

```shell
git clone https://github.com/plone/training.git
cd training
make html
```


(setup-build-available-documentation-builds-label)=

## Available documentation builds

All build and check documentation commands use the file `Makefile`.

To see all available builds:

```shell
make help
```


### `html`

`html` is the long narrative version used for the online documentation and by the trainer.

```shell
make html
```

Open `/_build/html/index.html` in a web browser.


### `livehtml`

`livehtml` rebuilds Sphinx documentation on changes, with live-reload in the browser.

```shell
make livehtml
```

Open http://0.0.0.0:8000/ in a web browser.


(setup-build-make-presentation-label)=

### `presentation`

`presentation` is an abbreviated version of the documentation.
It is designed for projectors which are typically low resolution and have limited screen space.
Trainers may present this version using a projector during a training.

```shell
make presentation
```

Open `/_build/presentation/index.html` in a web browser.

Authors should read {ref}`authors-presentation-markup-label` for how to write markup for the presentation build.


### `linkcheck`

`linkcheck` checks all links.
See {ref}`authors-linkcheck-label` for configuration.

```shell
make linkcheck
```

Open `/_build/presentation/output.txt` for a list of broken links.


### `vale`

`vale` checks for American English spelling, grammar, syntax, and the Microsoft Developer Style Guide.
See {ref}`authors-english-label` for configuration.

```shell
make vale
```

See the output on the console for suggestions.


### `html_meta`

`html_meta` adds a meta data section to each chapter if missing.
See {ref}`authors-html-meta-data-label` for more info.

```shell
make html_meta
```


## Overriding configuration options

Both Sphinx and vale support overriding configuration options.
The following examples serve as tips for spotting mistakes in your training.

In Sphinx, you can use the `SPHINXOPTS` environment variable to set [configuration options](https://www.sphinx-doc.org/en/master/usage/configuration.html) of [`sphinx-build`](https://www.sphinx-doc.org/en/master/man/sphinx-build.html).
Syntax is in the following form.

```shell
make SPHINXOPTS="OPTION VALUE" BUILDER
```

The following example shows how to clean then build a live HTML preview of the trainings while suppressing syntax highlighting failures.

```shell
make SPHINXOPTS="-D suppress_warnings=['misc.highlighting_failure']" clean livehtml
```

You can also pass options to vale in the `VALEOPTS` environment variable.
In the following example, vale will not return a non-zero exit code when there are errors and will display warnings or errors only, not suggestions.

```shell
make vale VALEOPTS="--no-exit --minAlertLevel='warning'"
```
