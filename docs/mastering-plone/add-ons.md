---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": "Plone, Volto, add-on, customizing"
---

(add-ons-label)=

# Extending Plone with add-on packages

```{card}
Backend chapter

For frontend add-ons see chapter {ref}`volto-addon-label`
```


Plone add-ons enrich the CMS by

- adding content types
- adding behaviors with new fields, relations and other features for existing and custom content types
- adding blocks to add elementary content snippets to a page
- designing the layout
- customizing the editor experience
- adding content assembling features for overview pages

Plone 6 knows two groups of add-ons: Add-ons for Plone and such for the frontend Volto.

Plone backend add-ons provide

- content types
- behaviors to enrich content types

Plone frontent add-ons provide
- new blocks
- variations and enhancements of blocks
- a theme to design the layout of a site
- components independent of blocks like a dropdown navigation

Both can be tightly coupled, if a frontend feature depends on a new content type, a new behavior or any other change needed in data structure.
For example an add-on that has the goal to provide a bookmarking feature depends on a backend add-on that handels the storing of the bookmarks.

Have a look at the curated lists of add-ons:  


[backend add-ons](https://github.com/collective/awesome-plone#readme)  
[frontend add-ons](https://github.com/collective/awesome-volto#readme)



(add-ons-find-label)=

## How to find appropriate add-ons

It can be very hard to find the right add-on for your requirements.
Here are some tips.

- Make a list of required features.

- Find candidates on PyPi, npm  or Github:

  - curated list of [backend add-ons](https://github.com/collective/awesome-plone#readme)
  - curated list of [frontend add-ons](https://github.com/collective/awesome-volto#readme)
  - Python packages on Pypi: <https://pypi.org/search/?c=Framework+%3A%3A+Plone>
  - Plone add-ons on Github: <https://github.com/collective>
  - Plone core packages on Github: <https://github.com/plone>
  - Google (e.g. [Plone+Slider](http://www.google.com/?q=Plone+slider))
  - Javascript packages on npm: <https://www.npmjs.com/search?q=Volto>

- Once you have a shortlist, test these add-ons.
  Here are the main issues you need to test before you install an add-on on a production site:

  - Test all required features.
    Read but do not trust the documentation.
  - Check if the add-on runs on your required Plone and Python version.
  - Check if it is currently maintained.
  - Does it have i18n-support and is the user interface translated to your language?
  - Does it uninstall cleanly?
    A tough one.
    See <https://lucafbb.blogspot.com/2013/05/how-to-make-your-plone-add-on-products.html> for the reason why.
  - Check for unwanted dependencies.

- Once you found an add-on you like, you can ask the community if you made a good choice or if you missed something:

  - Message Board: <https://community.plone.org>
  - There is also a talk that discusses in depth how to find the right add-on: <https://www.youtube.com/watch?v=Sc6NkqaSjqw>

- Either extend an existing add-on to ﬁt your needs or create a new add-on that does exactly what you need.


(add-ons-installing-label)=

## Installing Plone add-ons

We have two groups of add-ons: backend and frontend.

The training setup starts without any frontend add-on.
Later on we will add features via a frontend addon.
See chapter {doc}`volto_addon` how to install a frontend add-on.

The training setup starts with one backend add-on `ploneconf.site`.
Let's see how it is installed.


### Making a backend add-on package available to Zope

First, we must make the add-on package available to Zope.
This means that Zope can import the code.

A backend add-on is a Python package.
Therefore we install it with pip.

Look at the {file}`requirements.txt` file. 
You add a package to the configuration by adding a new line containing the package name.

If the add-on is not released on [PyPI](https://pypi.org/), we tell Zope where to find the package on `Github` or another repository platform by including the necessary information in {file}`mx.ini`.

```ini
[training.votable]
url=git@github.com:collective/training.votable.git
branch=main
; tag=volto
```

Adding the package to `instance.yaml` causes the generation of the Zope configuration to make the package available in a Zope app.

```yaml
  load_zcml:
    package_includes:
      ["ploneconf.site",]
```

Running `make build` has three effects:
- The build installs the python package with `pip`.
- The build generates in `instance/` a Zope instance configuration that makes the package available in our Zope app.
- As soon as the Zope app is started via `make start`, the add-on can be enabled per Plone instance.
  A Zope app can include multiple Plone instances.
  So an add-on can be enabled per Plone instance.

```{seealso}
Documentation {doc}`plone6docs:install/manage-add-ons-packages`
```

### Enabling add-ons in your Plone site

An add-on can be enabled per Plone instance.

In your browser, go to `Site Setup` at `http://localhost:3000/controlpanel`, and open the `Add-ons` Panel. You will see a list of available add-ons.

```{figure} _static/site_setup.png
:alt: Link to Site Setup

Link to Site Setup
```

Enable `ploneconf.site` now if you haven't done already.

This is what happens: The GenericSetup profile of the product gets loaded. This does things like:

- Registering new content types
- Registering behaviors
- Configuring new actions
- Create catalog indexes

All this is configured in the default GenericSetup profile, which can be found in `backend/sources/<package name>/src/<package name>/profiles/default`.
In the next chapters we will add here our content type `talk`, configure a catalog index, and some more.



(add-ons-summary-label)=

## Summary

We have seen in short how to extend a vanilla Plone website with third party add-ons to add new functionality.
Even if you do not use many of these, they are nonetheless an inspiration on how to implement features in Plone.



For frontend add-ons see chapter {ref}`volto-addon-label`
