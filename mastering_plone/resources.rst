.. _resources-label:

Resources
=========

We have not yet talked about CSS and Javascript. At the moment these are considered static resources.

You can declare and access static resources with special urls. The `configure.zcml` of our package already has a declaration for a resource-folder :file:`static`.

.. code-block:: xml

    <plone:static
        name="ploneconf.site"
        type="plone"
        directory="static"
        />

All files we put in the :file:`static` folder can be accessed via the url http://localhost:8080/Plone/++plone++ploneconf.site/the_real_filename.css

Another feature of this folder ist that the resouces you put in there are editable and overrideable in the browser using the overrides-tab of the resource registry.

Let's create a file :file:`ploneconf.css` in the :file:`static` folder with some CSS:

.. code-block:: css
    :linenos:

    header #portal-header #portal-searchbox .searchSection {
        display: none;
    }

    body.userrole-contributor #formfield-form-widgets-IEventBasic-start,
    body.userrole-contributor #formfield-form-widgets-IEventBasic-end > *,
    body.userrole-contributor #formfield-form-widgets-IEventBasic-whole_day,
    body.userrole-contributor #formfield-form-widgets-IEventBasic-open_end {
        display: none;
    }

    body.userrole-reviewer #formfield-form-widgets-IEventBasic-start,
    body.userrole-reviewer #formfield-form-widgets-IEventBasic-end > *,
    body.userrole-reviewer #formfield-form-widgets-IEventBasic-whole_day,
    body.userrole-reviewer #formfield-form-widgets-IEventBasic-open_end {
        display: block;
    }

The css is not very exciting. It hides the :guilabel:`only in current section` below the search-box (we could also overwrite the viewlet, but ...). It also hides the event-fields we added in :ref:`events-label` from people submitting their talks.
For exiting css you take the training :ref:`theming-label`.

If we now access http://localhost:8080/Plone/++plone++ploneconf.site/ploneconf.css we see our css-file.

Also add a :file:`ploneconf.js` in the same folder but leave it empty for now. You could add some JavaScript to that file later.

How do our JavaScript and CSS files get used when visiting the page?
So far the new files are accessible in the browser but we want Plone to use them every time we access the page.
Adding them directly into the HTML is not a good solution, having many CSS and JS files slows down the page loading.

For this we need to register a *bundle* that contains these files. Plone will then make sure that all files that are part of this bundle are also deployed.
We need to register our resources with GenericSetup.

Open the file :file:`profiles/default/registry.xml` and add the following:

.. code-block:: xml
    :linenos:

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
