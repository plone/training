Using third-party behaviors
===========================


Add teaser with collective.behavior.banner
------------------------------------------

There are a lot of addons in Plone for sliders/banners/teasers. We thought there should be a better one and created ``collective.behavior.banner``.

.. image:: http://imgs.xkcd.com/comics/standards.png

Like many addons it has not yet been released on pypi but only exists as code on github.

The training-buildout hold a section ``[sources]`` that tells buildout to download a specific addon not from pypi but from some code repositiory (usually github):

.. code-block:: cfg

    [sources]
    collective.behavior.banner = git https://github.com/starzel/collective.behavior.banner.git pushurl=git@github.com:starzel/collective.behavior.banner.git rev=af2dc1f21b23270e4b8583cf04eb8e962ade4c4d

Pinning the revision saves us from being surprised by changes in the code we might not want.

* Install the addon
* Create a new dexterity-ct ``Banner`` with **only** the behavior ``Banner`` enabled.
* Create a folder called ``banners``
* Add two banners into that folder using images taken from http://lorempixel.com/800/150/
* Add the Behavior ``Slider`` to the default-contenttype ``Page (Document)``
* Edit the frontpage and link to the new banners.


