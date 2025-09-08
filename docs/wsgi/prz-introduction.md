---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(prz-label)=

# Deploying Plone with WSGI using zc.buildout, plone.recipe.zope2instance and Waitress

The `plone.recipe.zope2instance` creates and configures a Zope instance in a buildout part.
To provide a smooth transition to Plone 5.2 and WSGI it tries to guess sensible defaults.
The goal in providing WSGI support in `plone.recipe.zope2instance` was to keep the buildout configuration close to the ZServer configuration.
Many options formerly used for ZServer are working in pretty much the same way for WSGI.
WSGI is the default in recent `plone.recipe.zope2instance` versions.
It can be overridden by ZServer for Python 2.
[Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable) is the default WSGI server configured by `plone.recipe.zope2instance`.
Waitress is a pure Python WSGI server implementation originating from the Pylons project.

With this information in mind, creating a minimial WSGI buildout for Plone is fairly easy.
A working example is contained in `basic.cfg` in the training buildout, here are the file contents:

```ini
[buildout]
extensions = mr.developer
parts = instance
extends = https://dist.plone.org/release/5.2-latest/versions.cfg
auto-checkout =
    plone.recipe.zope2instance
    wsgitraining.site
sources = sources

[sources]
plone.recipe.zope2instance = git https://github.com/plone/plone.recipe.zope2instance.git
wsgitraining.site = fs wsgitraining.site

[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
eggs =
    Plone
    wsgitraining.site
```

As you can see, we are using a custom add-on named `wsgitraining.site` contained in the buildout.
We will not use the add-on immediately so you don't need to activate it yet.
We use `mr.developer` to checkout the source code of this add-on.
We also use a source checkout of the `plone.recipe.zope2instance` buildout recipe to get the latest (maybe not yet released on PyPI) functionality for this training.

As a first exercise in this training run the above buildout configuration from the command line:

Activate your virtualenv if you haven't done so already:

```shell
~/wsgitraining$ . bin/activate
```

Run buildout:

```shell
(wsgitraining) ~/wsgitraining$ buildout -c basic.cfg
```

After a successful buildout, you can start Plone in the foreground as usual.
Start `zeo` first:

```shell
(wsgitraining) ~/wsgitraining$ bin/zeo start
```

Then start the application server:

```shell
(wsgitraining) ~/wsgitraining$ bin/instance fg
```

You can then create a Plone instance by pointing your browser to `http://localhost:8080`.
