---
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

Make sure you have a recent LTS-version of NodeJS >= v12.22.x or v14.x.x

## plonecli / bobtemplates.plone

Install plonecli with Python3, on most Linux systems this can be done by:

```shell
pip3 install plonecli --user
```

This will also install bobtemplates.plone, but we will need the current beta version.

So let's update bobtemplates.plone:

```shell
pip3 install bobtemplates.plone>=6.0b8 --user
```




```{code-block}
:lineno-start: 1

npm install
npm run watch
```