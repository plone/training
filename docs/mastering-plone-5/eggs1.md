---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-eggs1-label)=

# Write Your Own Add-Ons to Customize Plone

````{sidebar} Get the code!

Code for the beginning of this chapter:

```shell
git checkout buildout_1
```

Code for the end of this chapter:

```shell
git checkout eggs1
```

{doc}`code`
````

(plone5-eggs1-create-label)=

In this part you will:

- Create a custom Python package {py:mod}`ploneconf.site` to hold all the code
- Modify buildout to install that package

Topics covered:

- {py:mod}`mr.bob` and {py:mod}`bobtemplates.plone`
- the structure of python packages

## Creating the package

Your own code has to be organized as a [Python package](https://docs.python.org/2/tutorial/modules.html#packages). A python package is directory that follows certain conventions to hold python modules.

We are going to use [bobtemplates.plone](https://pypi.org/project/bobtemplates.plone) to create a skeleton package. You only need to fill in the blanks.

{py:mod}`bobtemplates.plone` offers several Plone-specific templates for {py:mod}`mr.bob`, a project template builder similar to {py:mod}`cookiecutter`.

Enter the {file}`src` directory (*src* is short for *sources*) and call a script called {command}`mrbob` from our buildout's {file}`bin` directory:

```shell
$ cd src
$ ../bin/mrbob -O ploneconf.site bobtemplates.plone:addon
```

````{warning}
Before version 2.0.0 of {py:mod}`bobtemplates.plone` the command to create a add-on was different:

```shell
$ ../bin/mrbob -O ploneconf.site bobtemplates:plone_addon
```
````

You have to answer some questions about the add-on. Press {kbd}`Enter` (i.e. choosing the default value) for most questions except where indicated (enter your GitHub username if you have one, do not initialize a GIT repository, Use Plone 5.2 and python 3.7):

```
--> Author's name [Philip Bauer]:

--> Author's email [bauer@starzel.de]:

--> Author's GitHub username: pbauer

--> Package description [An add-on for Plone]:

--> Do you want me to initialize a GIT repository in your new package? (y/n) [y]: n

--> Plone version [5.1]: 5.2

--> Python version for virtualenv [python2.7]: python3.7

git init is disabled!
Generated file structure at /Users/pbauer/workspace/training_buildout/src/ploneconf.site
```

```{only} not presentation
If this is your first python package, this is a very special moment.

You generated a package with a lot files. It might look like too much boilerplate but all files in this package serve a clear purpose and it will take some time to learn about the meaning of each of them.
```

## Eggs

When a python package is production-ready you can choose to distribute it as an egg over the python package index, [pypi](https://pypi.org). This allows everyone to install and use your package without having to download the code from github. The over 270 python packages that are used by your current Plone instance are also distributed as eggs.

(plone5-eggs1-inspect-label)=

## Inspecting the package

In {file}`src` there is now a new folder {file}`ploneconf.site` and in there is the new package. Let's have a look at some of the files:

{file}`buildout.cfg`, {file}`.travis.yml`, {file}`.coveragerc`, {file}`requirements.txt`, {file}`MANIFEST.in`, {file}`.gitignores`, {file}`.gitattributes`,

: You can ignore these files for now. They are here to create a buildout only for this package to make distributing and testing it easier.

{file}`README.rst`, {file}`CHANGES.rst`, {file}`CONTRIBUTORS.rst`, {file}`DEVELOP.rst`, {file}`docs/`

: The documentation of your package goes in here.

{file}`setup.py`

: This file configures the package, its name, dependencies and some metadata like the author's name and email address. The dependencies listed here are automatically downloaded when running buildout.

{file}`src/ploneconf/site/`

: The python code of your package itself lives inside a special folder structure.
  That seems confusing but is necessary for good testability.
  Our package contains a [namespace package](https://peps.python.org/pep-0420/) called *ploneconf.site* and because of this there is a folder {file}`ploneconf` with a {file}`__init__.py` and in there another folder {file}`site` and in there finally is our code.
  From the buildout's perspective your code is in {file}`{your buildout directory}/src/ploneconf.site/src/ploneconf/site/{real code}`

```{note}
Unless discussing the buildout we will from now on silently omit these folders when describing files and assume that {file}`{your buildout directory}/src/ploneconf.site/src/ploneconf/site/` is the root of our package!
```

{file}`configure.zcml` ({file}`src/ploneconf/site/configure.zcml`)

: The phone book of the distribution. By reading it you can find out which functionality is registered using the component architecture. There are more registrations in other zcml-files in this add-ons (e.g. {file}`browser/configure.zcml`, {file}`upgrades.zcml` and {file}`permissions.zcml`) that are included in your main {file}`configure.zcml`

{file}`setuphandlers.py` ({file}`src/ploneconf/site/setuphandlers.py`)

: This holds code that is automatically run when installing and uninstalling our add-on.

{file}`interfaces.py` ({file}`src/ploneconf/site/interfaces.py`)

: Here a browserlayer is defined in a straightforward python class. We will need it later.

{file}`testing.py`

: This holds the setup for running tests.

{file}`tests/`

: This holds the tests.

{file}`browser/`

: This directory is a python package (because it has a {file}`__init__.py`) and will by convention hold most things that are visible in the browser.

{file}`browser/configure.zcml`

: The phonebook of the browser package. Here views, resources and overrides are registered.

{file}`browser/overrides/`

: This folder is here to allow overriding existing default Plone templates.

{file}`browser/static/`

: A directory that holds static resources (images/css/js). The files in here will be accessible through URLs like `++resource++ploneconf.site/myawesome.css`

{file}`locales/`

: This directory can hold translations of text used in the package to allow for multiple languages of your user-interface.

{file}`profiles/default/`

: This folder contains the GenericSetup profile. During the training we will put some XML files here that hold configuration for the site.

{file}`profiles/default/metadata.xml`

: Version number and dependencies that are auto-installed when installing our add-on.

% profiles/uninstall/
% This folder holds another GenericSetup profile. The steps in here are executed on uninstalling.

(plone5-eggs1-include-label)=

## Including the package in Plone

Before we can use our new package we have to tell Plone about it. Look at {file}`buildout.cfg` and see how `ploneconf.site` is included in `auto-checkout`, `eggs` and `test`:

```{code-block} cfg
:emphasize-lines: 2, 30, 38

auto-checkout +=
    ploneconf.site
#    starzel.votable_behavior

parts =
    checkversions
    instance
    mrbob
    packages
    robot
    test
    zopepy

eggs =
    Plone
    Pillow

# development tools
    plone.api
    plone.reload
    Products.PDBDebugMode
    plone.app.debugtoolbar
    Products.PrintingMailHost
    pdbpp

# TTW Forms
    collective.easyform

# The add-on we develop in the training
    ploneconf.site

# Voting on content
#    starzel.votable_behavior

zcml =

test-eggs +=
    ploneconf.site [test]
```

This tells Buildout to add the egg {py:mod}`ploneconf.site`. The sources for this eggs are defined in the section `[sources]` at the bottom of {file}`buildout.cfg`.

```{code-block} cfg
:emphasize-lines: 2

[sources]
ploneconf.site = git https://github.com/collective/ploneconf.site.git pushurl=git@github.com:collective/ploneconf.site.git
starzel.votable_behavior = git https://github.com/collective/starzel.votable_behavior.git pushurl=git://github.com/collective/starzel.votable_behavior.git
```

This tells buildout to not download it from pypi but to do a checkout from GitHub put the code in {file}`src/ploneconf.site`.

```{note}
The package {py:mod}`ploneconf.site` is now downloaded from GitHub and automatically in the branch master. {py:mod}`ploneconf.site` can be called an egg even though it has not been released on pypi. Plone can use it like it uses an egg.
```

````{note}
If you do **not** want to use the prepared package for ploneconf.site from GitHub but write it yourself (we suggest you try that) then add the following instead:

```{code-block} cfg
:emphasize-lines: 2

[sources]
ploneconf.site = fs ploneconf.site path=src
starzel.votable_behavior = git https://github.com/collective/starzel.votable_behavior.git pushurl=git://github.com/collective/starzel.votable_behavior.git
```

This tells buildout to expect `ploneconf.site` in {file}`src/ploneconf.site`.
The directive `fs` allows you to add eggs on the filesystem without a version control system.
````

Now run buildout to reconfigure Plone with the updated configuration:

```shell
$ ./bin/buildout
```

After restarting Plone with {command}`./bin/instance fg` the new add-on {py:mod}`ploneconf.site` is available for install like EasyForm or Plone True Gallery.

We will not install it now since we did not add any of our own code or configuration yet. Let's do that next.

## Exercises

1. Create a new package called {py:mod}`collective.behavior.myfeature`. Inspect the directory structure of this package. Delete it after you are done. Many packages that are part of Plone and some add-ons use a *nested namespace* such as {py:mod}`plone.app.contenttypes`.
2. Open <https://github.com/plone/bobtemplates.plone> and read about the templates and subtemplates it provides.

## Summary

- You created the package {py:mod}`ploneconf.site` to hold your code.
- You added the new package to buildout so that Plone can use it.
