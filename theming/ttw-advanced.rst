========================================================================
TTW advanced: intro to Diazo Theming, build custom rules through the web
========================================================================

A Plone theme takes uses ``Diazo`` techonology to make theming easier.

You can find extended information about Diazo and its integration package ``plone.app.theming`` in the official docs: `Diazo docs <http://docs.diazo.org>`_
and `plone.app.theming docs <http://docs.plone.org/external/plone.app.theming/docs/index.html#what-is-a-diazo-theme>`_.

For this part of the training you just need to know the basic principles of a Diazo theme:

* Plone renders the content of the page;
* Diazo rules inject the content into any static theme;

Copy barceloneta theme
----------------------

To create our playground we will copy the existing Barceloneta theme.

DESCRIBE HOW TO COPY

Anatomy of a Diazo theme
------------------------

GET TO THE THEME EDITOR

The most important files:

* ``manifest.cfg``: contains metadata about the theme;
* ``rules.xml``: contains the theme rules;
* ``index.html``: the static HTML of the theme.


Custom rules
------------
Let's open ``rules.xml``. You will see all the rules that are used in Barceloneta theme right now. We'll cover later the meaning of each rule, for the time being let's concentrate on how to hack these rules.

Suppose that we want to make the "above content" block (the one that contains breadcrumbs) conditional, and show it only for authenticated users and PUT HERE ANOTHER EXAMPLE (?).

Find this line:

.. code-block:: xml

    <replace css:content="#viewlet-above-content" css:theme="#above-content" />

This rule states that the element that come from the content (Plone) with the id `#viewlet-above-content` must replace the element with the id `#above-content` in the static theme.

We want to hide it for anynoymous users so we can take advantage of the base CSS classes the Plone exposes on the body (SHOW THE CLASSES).

The class we are looking for is `userrole-authenticated`. Add another property to the rule so that we get to this line of code:

.. code-block:: xml

    <replace
        css:if-content="body.userrole-authenticated"
        css:content="#viewlet-above-content"
        css:theme="#above-content" />

The attribute `css:if-content` allow us to put condition on the rules based on a CSS selector that acts on the content, thus the markup rendered by Plone.

In this way the rule will be applied only if the body element has the class `.userrole-authenticated`.

MORE EXAMPLES HERE?


Customize CSS
-------------

TODO

Hack styles
-----------

TODO
