.. _views1-label:

Views I
=======

In this part you will:

* Register a view
* Create and use a template for the view


Topics covered:

* zcml

.. _views1-simple-label:

A simple browser view
---------------------

Before writing the talk view itself we step back and talk *a little* about views and templates.

A view in Plone is usually a ``BrowserView``. It can hold a lot of cool python code but we will first focus on the template.

Edit the file ``browser/configure.zcml`` and register another view similar to the demoview already there:

..  code-block:: xml
    :linenos:
    :emphasize-lines: 29-34

    <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:browser="http://namespaces.zope.org/browser"
      xmlns:plone="http://namespaces.plone.org/plone"
      i18n_domain="ploneconf.site">

      <!-- Set overrides folder for Just-a-Bunch-Of-Templates product -->
      <include package="z3c.jbot" file="meta.zcml" />
      <browser:jbot
        directory="overrides"
        layer="ploneconf.site.interfaces.IPloneconfSiteLayer"
        />

      <!-- Publish static files -->
      <browser:resourceDirectory
        name="ploneconf.site"
        directory="static"
        />

      <browser:page
        name="training"
        for="*"
        template="templates/training.pt"
        permission="zope2.View"
        />

    </configure>

Add a file ``browser/templates/training.pt``

.. code-block:: html

    <h1>Hello World</h1>

* Restart Plone and open http://localhost:8080/Plone/@@training.
* You should now see "Hello World".

We now have everything in place to learn about page templates.

..  note::

    The view ``training`` has no python class registered for it but only a template. It acts as if it had an empty python class inheriting from ``Products.Five.browser.BrowserView`` but the way that happens is actually quite a bit of magic...
