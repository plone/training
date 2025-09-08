---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(creating-initial-content-for-the-theme)=

# Theme Package V: Creating Initial Content

Our theme relies on some initial content structure, specifically the {file}`slider-images` folder with some images inside.

We will improve our theme package to create this content on install.

To do that we create the {file}`slider-images` folder in our {file}`setuphandlers.py` and load some example images into that folder.

We will add some images tp the {file}`theme/img` folder.
To create the folder and the images add the following code in your {file}`setuphandlers.py`:

```{code-block} python
:emphasize-lines: 2,5-6,22-23,31-67

# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

import os


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'ploneconf.theme:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    portal = api.portal.get()
    _create_content(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def _create_content(portal):
    if not portal.get('slider-images', False):
        slider = api.content.create(
            type='Folder',
            container=portal,
            title=u'Slider',
            id='slider-images'
        )
        for slider_number in range(1, 4):
            slider_name = u'slider-{0}'.format(str(slider_number))
            slider_image = api.content.create(
                type='Image',
                container=slider,
                title=slider_name,
                id=slider_name
            )
            slider_image.image = _load_image(slider_number)
        # NOTE: if your plone site is not a vanilla plone
        # you can have different workflows on folders and images
        # or different transitions names so this could fail
        # and you'll need to publish the images as well
        # or do that manually TTW.
        api.content.transition(obj=slider, transition='publish')


def _load_image(slider):
    from plone.namedfile.file import NamedBlobImage
    filename = os.path.join(
        os.path.dirname(__file__),
        'theme',
        'img',
        'slide-{0}.jpg'.format(slider),
    )
    return NamedBlobImage(
        data=open(filename, 'r').read(),
        filename=u'slide-{0}.jpg'.format(slider)
    )
```

```{note}
After adding this code to the file {file}`setuphandlers.py`, we need to restart Plone and uninstall/install our theme package add-on.
```
