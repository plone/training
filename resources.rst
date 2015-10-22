.. _resources-label:

Resources
=========

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/12_resources_p5/ src/ploneconf.site


We have not yet talked about CSS and Javascript. At the moment these are considered static resources.

You can declare and access static resources with special urls. The configure.zcml of our package already has a declaration for resources:

.. code-block:: xml

    <browser:resourceDirectory
      name="ploneconf.site"
      directory="static" />

Now all files we put in the `static` folder can be found via the url http://localhost:8080/Plone/++resource++ploneconf.site/something.js

Let's create a ``ploneconf.css`` in the `static` folder.

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

    /* Styles for ploneconf */
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

    /* Some css fixs to the default Plone 5-Theme */
    .formHelp {
        display: block;
    }

    .field span.option {
        display: block;
    }

    .field span.option input[type="checkbox"].required,
    .field span.option input[type="radio"].required {
        margin-right: 0.4em;
    }

    .field span.option input[type="checkbox"].required:after,
    .field span.option input[type="radio"].required:after {
        color: transparent;
        content: '';
    }

    textarea {
        height: 100px !important;
    }

    .select2-container-multi .select2-choices .select2-search-field input {
        min-width: 200px !important;
    }

    .pat-textareamimetypeselector {
        display: none;
    }

    /* Small fixes for toolbar */
    #edit-zone a {
        outline: 0
    }

    #edit-zone.plone-toolbar-top.expanded  nav > ul > li {
        border-right: 1px dotted #888;
    }

    #edit-zone.plone-toolbar-top.expanded  nav > ul a > span + span {
        padding: 0 8px 0 0;
    }


If we access http://localhost:8080/Plone/++resource++ploneconf.site/ploneconf.css we see our css-file.

Also add a ``ploneconf.js`` in the same folder but leave it empty.

How do our javascript and css files get used when visiting the page? Adding them directly into the html is not a good solution, having many css and js files slows down the page loading.

With ``portal_css`` and ``portal_javascript`` Plone has resource managers that are able to merge and compress js and css files. Resources can be added conditionally and Plone automatically stops merging files when you are debugging Plone in the foreground.

We need to register our resources with GenericSetup.

Add a new file ``profiles/default/cssregistry.xml``

.. code-block:: xml
    :linenos:

    <?xml version="1.0"?>
    <object name="portal_css">
      <stylesheet
          title=""
          applyPrefix="False"
          authenticated="False"
          bundle=""
          cacheable="True"
          compression="safe"
          conditionalcomment=""
          cookable="True"
          enabled="True"
          expression=""
          id="++resource++ploneconf.site/ploneconf.css"
          media=""
          rel="stylesheet"
          rendering="import"/>
    </object>

Add a new file ``profiles/default/jsregistry.xml``

.. code-block:: xml
    :linenos:

    <?xml version="1.0"?>
    <object name="portal_javascripts">
      <javascript
        authenticated="False"
        bundle=""
        cacheable="True"
        compression="safe"
        conditionalcomment=""
        cookable="True"
        enabled="on"
        expression=""
        id="++resource++ploneconf.site/ploneconf.js"
        inline="False"/>
    </object>
