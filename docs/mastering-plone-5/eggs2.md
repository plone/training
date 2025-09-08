---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-eggs2-label)=

# Creating Reusable Packages

We already created the package {py:mod}`ploneconf.site`  much earlier.

In this part you will:

- Build your own standalone egg.

Topics covered:

- {py:mod}`mr.bob`

Now you are going to create a feature that is independent of the ploneconf site and can be reused in other packages.

To make the distinction clear, this is not a package from the namespace {samp}`ploneconf` but from {samp}`starzel`.

We are going to add a voting behavior.

For this we need:

> - A behavior that stores its data in annotations
> - A viewlet to present the votes
> - A bit of JavaScript
> - A bit of CSS
> - Some helper views so that the JavaScript code can communicate with Plone

We move to the {file}`src` directory and again use a script called {file}`mrbob` from our project's {file}`bin` directory
and the template from `bobtemplates.plone` to create the package.

If the {file}`src` directory does not exist yet, create it:

```shell
mkdir src
```

Go inside the {file}`src` folder and create the package:

```shell
cd src
$ ../bin/mrbob -O starzel.votable_behavior bobtemplates.plone:addon
```

We press {kbd}`Enter` to all questions *except* our personal data and the Plone version.
Here we enter {kbd}`5.2`.
