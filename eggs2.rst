.. _eggs2-label:

Creating Reusable Packages
==========================

We already created the package ``ploneconf.site``  much earlier.

In this part you will:

* Build your own standalone egg.

Topics covered:

* mr.bob


Now you are going to create a feature that is completely independent of the ploneconf site and can be reused in other packages.

To make the distinction clear, this is not a package from the namespace :samp:`ploneconf` but from :samp:`starzel`.

We are going to add a voting behavior.

For this we need:

  * A behavior that stores its data in annotations
  * A viewlet to present the votes
  * A bit of javascript
  * A bit of css
  * Some helper views so that the Javascript code can communicate with Plone

We move to the :file:`src` directory and again use a script called :file:`mrbob` from our project's :file:`bin` directory and the template from ``bobtemplates.plone`` to create the package.

.. code-block:: bash

    $ mkdir src
    $ cd src
    $ ../bin/mrbob -O starzel.votable_behavior bobtemplates:plone_addon

We press :kbd:`Enter` to all questions *except* our personal data and the Plone version. Here we enter :kbd:`5.0a3`.
