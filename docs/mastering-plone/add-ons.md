---
myst:
  html_meta:
    "description": "Extending Plone with features via existing backend add-ons"
    "property=og:description": "Extending Plone with features via existing backend add-ons"
    "property=og:title": "Extend Plone with add-on packages"
    "keywords": "Plone, Volto, add-on, customizing"
---

(add-ons-label)=

# Extend Plone with add-on packages

```{card}

In this chapter you will learn how to select and install Plone add-ons.

The creation of a custom add-on is explained in {doc}`voting-story/index`
```

````{card}

Check out `mastering-plone-project` at tag `initial`:

```shell
git checkout initial
```

The code at the end of the chapter:

```shell
git checkout addons
```

More info in {doc}`code`
````

Plone add-ons enrich the CMS by

- adding content types
- adding behaviors with new fields, relations and other features for existing and custom content types
- adding blocks to add elementary content snippets to a page
- designing the layout
- customizing the editor experience
- adding content assembling features for overview pages

Plone has two groups of add-ons: add-ons for the Plone backend and add-ons for the frontend Volto.

Plone backend add-ons provide

- content types
- behaviors to enrich content types

Plone frontend add-ons provide

- new blocks
- variations and enhancements of blocks
- a theme to design the layout of a site
- components independent of blocks like a dropdown navigation

Both can be coupled, if a frontend feature depends on a new content type, a new behavior, or any other change needed in data structure.
For example, an add-on that has the goal to provide a bookmarking feature depends on a backend add-on that handles the storing of the bookmarks.


(add-ons-find-label)=

## How to find appropriate add-ons

It can be hard to find the right add-on for your requirements.
Here are some tips.

- Make a list of required features.

- Find candidates on PyPI, npm  or GitHub:

  - curated list of [awesome backend add-ons](https://github.com/collective/awesome-plone/blob/main/README.md)
  - curated list of [awesome frontend add-ons](https://github.com/collective/awesome-volto#readme)
  - Python packages on PyPI: <https://pypi.org/search/?c=Framework+%3A%3A+Plone>
  - Plone add-ons on GitHub: <https://github.com/collective>
  - Plone core packages on GitHub: <https://github.com/plone>
  - Google (for example [Plone+Slider](http://www.google.com/?q=Plone+slider))
  - JavaScript packages on npm: <https://www.npmjs.com/search?q=Volto>

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
  - There is also a talk that discusses in depth how to find the right add-on: <https://www.youtube-nocookie.com/embed/Sc6NkqaSjqw?privacy_mode=1>

- Either extend an existing add-on to ﬁt your needs or create a new add-on that does exactly what you need.


(add-ons-install-form-block-label)=

## Example: the form block add-on

For our case study, it would be nice to have a contact form to send questions to the conference organizers.
We can use the [Plone form block add-on](https://github.com/plone/form-block) for this.

It is released in two packages:

- [`plone.formblock`](https://pypi.org/project/plone.formblock/) is the backend add-on
- [`@plone/volto-form-block`](https://www.npmjs.com/package/@plone/volto-form-block) is the frontend add-on

We have to add both of these to our project.

## Install the backend add-on

First, we must add the backend add-on as a dependency, so that its code will be available.

Edit the file {file}`backend/pyproject.toml` and add `plone.formblock` to the `dependencies`:

```{code-block} toml
:linenos:
:emphasize-lines: 6

dependencies = [
    "Products.CMFPlone==6.2.1",
    "plone.api",
    "plone.restapi",
    "plone.volto",
    "plone.formblock==1.0.0a3",
]
```

It's a good idea to "pin" the add-on to a specific version, to make sure that it won't get accidentally upgraded when you don't expect it, if there is a new release of the add-on in the future.

Now re-install the project with the new dependencies:

```shell
make backend-install
```

This runs `uv sync` which updates the Python virtual environment with the dependencies listed in `pyproject.toml`.
Now when the backend is restarted, the code for the add-on is available.

Backend add-ons usually also need to be installed in a specific Plone site.

In your browser, go to `Site Setup` at `http://localhost:3000/controlpanel`, and open the `Add-ons` control panel.
You will see a list of available add-ons.
Click to install the form block add-on.

````{card}
```{image} _static/addons.png
:alt: Plone `Add-ons` control panel, showing available configuration options
```
+++
_Add-ons control panel, showing available configuration options._
````

```{seealso}
Documentation {doc}`plone6docs:admin-guide/add-ons`
```

## Install the frontend add-on

We also need to install the code for the frontend add-on.
Update the `addons` and `dependencies` in {file}`frontend/packages/volto-ploneconf-site/package.json`:

```{code-block} json
:emphasize-lines: 2, 5

"addons": [
  "@plone/volto-form-block"
],
"dependencies": {
  "@plone/volto-form-block": "^1.0.0-alpha.0",
},
```

```{tip}
`dependencies` tells the package manager `pnpm` to install the code.
`addons` tells Volto to load the add-on's configuration.
```

Now re-install the frontend with the new dependencies:

```shell
make frontend-install
```

After you restart the frontend, you should be able to add a form block.

```{tip}
To confirm that the frontend add-on is installed, go to http://localhost:3000/controlpanel and look at the list of Add-ons at the bottom.
```

(add-ons-summary-label)=

## Summary

We have seen in short how to extend a vanilla Plone website with third party add-ons to add new functionality.
Even if you do not use many of these, they can be useful examples of how to implement features in Plone.
