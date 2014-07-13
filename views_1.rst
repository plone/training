Views I
=======

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout-directory:

    .. code-block:: bash

        cp -Rf src/ploneconf.site_sneak/chapters/14_views1/ src/ploneconf.site


A simple browser view
---------------------

We need to add some boilerplate-code to be able to create a view. Before we write the talk-view itself we need to step back and talk *a little* about views and templates.

A basic view in Plone is usually a ``BrowserView``. It can hold a lot of python-code but it can also be only a empty ``BrowserView``-class that renders a template when called. Such an empty class is what we create at first so we can concentrate on the template.

* Add a new directory ``src/ploneconf.site/ploneconf/site/browser``. By convention the dir ``browser`` should hold all UI displayed in the browser.
* Add an empty file ``browser/__init__.py``
* We need to tell Plone to consider this directory. Modify the existing ``configure.zcml`` and add

.. code-block:: xml

    <include package=".browser" />

Then add a file ``browser/configure.zcml``:

.. code-block:: xml
  :linenos:

  <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:browser="http://namespaces.zope.org/browser"
      i18n_domain="ploneconf.site">

      <browser:page
         name="demoview"
         for="*"
         class=".views.DemoView"
         template="templates/demoview.pt"
         permission="zope2.View"
         />

  </configure>

Add a file ``browser/views.py``::

    from Products.Five.browser import BrowserView

    class DemoView(BrowserView):
        """ This does nothing so far
        """

This might seem a lot of boilerplate if we only want to render a template but every bit of it can be changed to achieve different effects. It's not useless code but actually very powerful stuff. We only ignore it for now and concentrate on the template.

Add a directory ``browser/templates`` and add an file ``browser/templates/demoview.pt``

.. code-block:: html

    <h1>Hello World</h1>

* Restart Plone and open http://localhost:8080/Plone/@@demoview.
* You should see "Hello World".

We now have everything in place to learn about zope page templates.

