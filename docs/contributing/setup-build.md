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

Install [Enchant](https://abiword.github.io/enchant/) to check spelling.

```{seealso}
[Installation of Enchant from the PyEnchant documentation](https://pyenchant.github.io/pyenchant/install.html).
```

**macOS**

```shell
brew install enchant
```

**Ubuntu**

```shell
sudo apt-get install enchant
```

Clone the Training repository, then create a Python virtual environment, install project dependencies, activate the virtual environment, and build HTML version of the Training documentation.

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


### `spellcheck`

`spellcheck` checks the spelling of words.
See {ref}`authors-english-label` for configuration.

```shell
make spellcheck
```

Open `/_build/spellcheck/` for each training's misspellings.


### `html_meta`

`html_meta` adds a meta data section to each chapter if missing.
See {ref}`authors-html-meta-data-label` for more info.

```shell
make html_meta
```
