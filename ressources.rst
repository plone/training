Ressources
==========

We have not yet talked about CSS and Javascript. At the moment these are considered static resources.

You can declare and access static resources with special urls. In the past, you could just create a static folder, add grok, and your static files have been registered
Unfortunately this functionality has been removed. Grok is a framework of its own and they implemented an alternative system for embedding resources, `fanstatic` Plone does not use fanstatic so Plone basically lost a functionality.

We are going to mimic this behavior with plone functionality by adding the following to our configure.zcml:

.. code-block:: xml

    <plone:static
        type="theme"
        name="ploneconf.talk"
        directory="static"
        />

For this to work we need to add another namespace-declaration into the header::

    xmlns:plone="http://namespaces.plone.org/plone"

Now all files we put in the static folder can be found via /++theme++/ploneconf.talk/somefile

How do our javascript and css files and up in the browser? Adding them directly into the html is not a good solution, having many css and js files slows page loading down.
Plone has a resource manager that is able to concatenate and compress js and css files, resources can be added conditionally and Plone automatically stops concatenating files when you are debugging plone in the foreground. The resources are managed in the Zope database, as need to write a genericsetup step.

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_javascripts" meta_type="JavaScripts Registry">
    <javascript authenticated="False" cacheable="True" compression="safe"
        conditionalcomment="" cookable="True" enabled="on" expression=""
        id="++theme++ploneconf.talk/ploneconf.js" inline="False"/>
    </object>

