---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Setup

To install Plone and example packages for this training, first clone [collective.jstraining](https://github.com/collective/collective.jstraining), then execute the following commands:

```shell
git clone https://github.com/collective/collective.jstraining.git
cd collective.jstraining
./bootstrap.sh
```

```{note}
To be able to install the JavaScript development tools, you need [NodeJS](https://nodejs.org/en/download/) installed on your development computer.
```

## Installing Mockup

Optionally you can download Mockup source code and install it in development mode.

Mockup is already included in the [training buildout](https://github.com/collective/collective.jstraining).

Uncomment the "mockup" line in the buildout's `auto-checkout` section.

After that, run buildout:

```shell
bin/buildout -N
```

```{warning}
If you are running buildout inside vagrant, always remember to use specify {file}`vagrant.cfg`: {command}`bin/buildout -Nc vagrant.cfg`
```
