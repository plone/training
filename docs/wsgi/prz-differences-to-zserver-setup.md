---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Differences to the ZServer setup

Maybe the most important difference is that configuration is now split into two files:

In addition to `zope.conf` there is now a file called `wsgi.ini` in the same directory (`parts/instance/etc` by default).
Opposed to the xml style syntax of the zope.conf, wsgi.ini (as the extension suggests) uses an ini style syntax.
More specifically its syntax is that defined by [Paste Deploy](https://pastedeploy.readthedocs.io/en/latest/#introduction), a package that provides a system for finding and configuring WSGI applications and servers.
Like waitress, PasteDeploy is another spinoff of the Pylons project.
Waitress is using PasteDeploy internally and defines PasteDeploy entry points.
It defines the Zope application entry point and configures the WSGI server, waitress in our case.
Most notably the logging configuration has moved from zope.conf to `wsgi.ini`.

```{note}
Configuring logging in `zope.conf` is no longer possible and will result in an error when trying to start the instance.
This is because the WSGI schema for `zope.conf` (defined in `wsgischema.xml` in the `Zope2/Startup` folder of the core zope package)
is more limited than the previously used Zope schema (defined in `zopeschema.xml` and moved to the `ZServer` package).
```

```{note}
- uWSGI also uses an INI style configuration file, but the content and also to some extent the purpose of the uWSGI config file are different from the waitress config file.
- Gunicorn uses Python source files for configuration, but INI style configuration from Paster applications will be passed to Gunicorn.
```
