.. _thirdparty-label:

Using Third-Party Behaviors
===========================

..  warning::

    Skip this since collective.behavior.banner is not yet compatible with Plone 5.


.. _thirdparty-banner-label:

Add teaser with collective.behavior.banner
------------------------------------------

There are a lot of add-ons in Plone for sliders/banners/teasers. We thought there should be a better one and created ``collective.behavior.banner``.

.. figure:: _static/standards.png
   :align: center

Like many add-ons it has not yet been released on pypi but only exists as code on github.

The training buildout has a section ``[sources]`` that tells buildout to download a specific add-on not from pypi but from some code repository (usually github):

.. code-block:: cfg

    [sources]
    collective.behavior.banner = git https://github.com/collective/collective.behavior.banner.git pushurl=git@github.com:collective/collective.behavior.banner.git rev=af2dc1f21b23270e4b8583cf04eb8e962ade4c4d

Pinning the revision saves us from being surprised by changes in the code we might not want.

After adding the source, we need to add the egg to buildout:

.. code-block:: cfg

    eggs =
        Plone
        ...
        collective.behavior.banner
        ...

And rerun ``./bin/buildout``

* Install the add-on
* Create a new dexterity content type ``Banner`` with **only** the behavior ``Banner`` enabled.
* Create a folder called ``banners``
* Add two banners into that folder using images taken from http://lorempixel.com/800/150/
* Add the Behavior ``Slider`` to the default content type ``Page (Document)``
* Edit the front-page and link to the new banners.
