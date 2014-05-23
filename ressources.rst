Ressources
==========

We have not yet talked about CSS and Javascript. At the moment these are considered static resources.

You can declare and access static resources with special urls. The configure.zcml of our package already has a declaration for resources:

.. code-block:: xml

    <browser:resourceDirectory
      name="ploneconf.site"
      directory="resources" />

Now all files we put in the resources-folder can be found via the url http://localhost:8080/Plone/++resource++ploneconf.site/something.js

Let's create a ``ploneconf.css`` and a ``plonconf.js`` in that folder.

.. code-block:: css

    #visual-portal-wrapper {
        margin: 0 auto;
        position: relative;
        width: 1024px;
    }

    @media only screen and (max-width: 980px) {
       #visual-portal-wrapper {
           position: relative;
           width: auto;
       }
    }

    @media only screen and (max-width: 768px) {
       #portal-columns > div {
           width: 97.75%;
           margin-left: -98.875%;
           clear: both;
       }

       .searchButton,
       .searchSection {
           display: none;
       }
    }

If we access http://localhost:8080/Plone/++resource++ploneconf.site/ploneconf.css we see our css-file.

How do our javascript and css files get used when visiting the page? Adding them directly into the html is not a good solution, having many css- and js-files slows page loading down.

With ``portal_css`` and ``portal_javascript`` Plone has resource managers that are able to merge and compress js and css files. Resources can be added conditionally and Plone automatically stops merging files when you are debugging plone in the foreground.

We need to register our resources with GenericSetup.

Add a new file ``profiles/default/cssregistry.xml``

.. code-block:: xml

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
