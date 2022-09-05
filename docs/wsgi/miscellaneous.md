---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Can I talk to the supervisor?

Miscellaneous topics that are related to Plone and WSGI but do not fit anywhere else (yet).

## Install Plone using pip

The official Zope documentation provides instructions on how to [install Zope with pip](https://zope.readthedocs.io/en/latest/INSTALL.html#installing-zope-with-pip).
It uses pip's `-c` option to specify a `constraints.txt` file that contains the version information (the known good set of package versions), similar to `versions.cfg` in `zc.buildout`.
This is at the moment not possible with Plone because of a bug in `z3c.autoinclude`.
`z3c.autoinclude` is not capable of resolving module paths of `pip` installed packages.
See [this pull request](https://github.com/zopefoundation/z3c.autoinclude/pull/2) for some information.

## Protocols other than HTTP (FTP, WebDAV, ...)

Currently there is no straightforward way for using protocols other than HTTP in a Plone WSGI setup, FTP and WebDAV being the most important ones.
See <https://github.com/plone/Products.CMFPlone/issues/2537>.
