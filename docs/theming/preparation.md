---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Preparation for the theming training

We will use the following tools during the training.

- npm (NodeJS)
- plonecli / bobtemplates.plone

## npm / NodeJS

Make sure you have a recent LTS-version of NodeJS >= v16.x.x

You could also use [NVM](https://github.com/nvm-sh/nvm) to manage different versions of NodeJS.


## plonecli / bobtemplates.plone

Install plonecli with Python3, on most Linux systems this can be done by:

```shell
$ pip3 install plonecli>=2.3
```

```{note}
Currently plonecli only supports Python 3.7-3.9, but not 3.10 yet!
```

This will also install bobtemplates.plone.

To update bobtemplates.plone:

```shell
$ pip3 install bobtemplates.plone --upgrade
```

You can check the versions of plonecli and bobtemplates.plone as follow:

```sh
$ plonecli -V
Available packages:

        plonecli : 2.3

        bobtemplates.plone: 6.0b16
```

## Testing the setup

To test the setup, use plonecli to create an addon:

```shell
plonecli create addon plonetheme.tester
```

```shell
$ cd plonetheme.tester
$ plonecli add theme_barceloneta
$ plonecli build serve
```

After that we have a working buildout and Plone is starting.

Now let's verify that npm/NodeJS is working fine.

```shell
$ cd src/plonetheme/tester/theme
$ npm install
$ npm run build
```