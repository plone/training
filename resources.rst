.. _resources-label:

Resources
=========

..  warning::

    This chapter is still work-in-progress.

We have not yet talked about CSS and Javascript. At the moment these are considered static resources.

You can declare and access static resources with special urls. The `configure.zcml` of our package already has a declaration for resources:

.. code-block:: xml

    <browser:resourceDirectory
        name="ploneconf.site"
        directory="static" />

We want to change that a little to allow the resources to be editable and overrideable in the browser using the overrides-tab of the resource registry. Change it to the following:

.. code-block:: xml

    <plone:static
        name="ploneconf.site"
        type="plone"
        directory="static"
        />

Now all files we put in the `static` folder can be found via the url http://localhost:8080/Plone/++plone++ploneconf.site/the_real_filename.css

Let's create a file ``ploneconf.css`` in the `static` folder with some css:

.. code-block:: css
    :linenos:

    .sponsor {
        float: left;
        margin: 0 1em 1em 0;
    }

    .sponsor:hover {
        box-shadow: 0 0 8px #000000;
        -moz-box-shadow: 0 0 8px #000000;
        -webkit-box-shadow: 0 0 8px #000000;
    }

    header #portal-header #portal-searchbox .searchSection {
        display: none;
    }

    #content .event.summary {
        box-shadow: none;
        float: none;
        max-width: 100%;
    }

    .talkinfo #portal-column-content {
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.17);
        padding: 1em;
        background-color: #fff;
    }

    .talkinfo h1 {
        font-size: 20px;
    }

    .talkinfo .event.summary {
        background-color: #fff;
    }

If we now access http://localhost:8080/Plone/++plone++ploneconf.site/ploneconf.css we see our css-file.

Also add a ``ploneconf.js`` in the same folder but leave it empty for now. You could add some javascript to that file later.

How do our javascript and css files get used when visiting the page? So far the new files are accessible in the browser but we want Plone to use them everytime we access the page. Adding them directly into the html is not a good solution, having many css and js files slows down the page loading.

For this we need to register a *bundle* that contains these files. Plone will then make sure that all files that are part of this bundle are also deployed.
We need to register our resources with GenericSetup.

Open the file ``profiles/default/registry.xml`` and add the following:

.. code-block:: xml
    :linenos:

    <!-- the plonconf resources -->
    <records prefix="plone.resources/ploneconf-main"
             interface='Products.CMFPlone.interfaces.IResourceRegistry'>
      <value key="css">
        <element>++plone++ploneconf.site/ploneconf.css</element>
      </value>
      <value key="js">++plone++ploneconf.site/ploneconf.js</value>
    </records>

    <!-- the plonconf bundle -->
    <records prefix="plone.bundles/ursapharm-bundle"
             interface='Products.CMFPlone.interfaces.IBundleRegistry'>
      <value key="resources">
        <element>ploneconf-main</element>
      </value>
      <value key="enabled">True</value>
      <value key="compile">True</value>
      <value key="csscompilation">++plone++ploneconf.site/ploneconf.css</value>
      <value key="jscompilation">++plone++ploneconf.site/ploneconf.js</value>
      <value key="last_compilation"></value>
    </records>

The resources that are part of the registered bundle will now be deployed with every request.

For more infos please see http://docs.plone.org/adapt-and-extend/theming/resourceregistry.html or http://training.plone.org/5/theming/adv-resource-registry.html.
