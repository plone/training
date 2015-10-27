=================================
Advanced resources registry usage
=================================

In the Plone *resource registry* we can register our static resources, like
CSS and LESS files and also JavaScript resources.
We will cover here only CSS and LESS, but you can also do nice things
with your JavaScript resources (for example using *requirejs* to do the import
correctly without worrying about import order).
For details about this, look into the documentation of the *resource registry*
and in the JavaScript part of the training.


Registering CSS/LESS resources in the registry
==============================================

Because of the flexibility of LESS over CSS we will use only LESS files here,
but static CSS files can be registered in the same way. LESS files have the
advantage that we can use imports, and with ``reference-imports`` we can even
import only the parts of the files which we are really using.

Let's see how we can register a resource in the resource registry.
To do that, we add an ``IResourceRegistry`` entry into the ``registry.xml`` in
our ``profiles/default`` folder:

.. code-block:: xml

   <?xml version="1.0"?>
   <registry>
       <records prefix="plone.resources/tango-main"
                 interface='Products.CMFPlone.interfaces.IResourceRegistry'>
          <value key="css">
             <element>++theme++plonetheme.tango/css/main.less</element>
          </value>
       </records>
   </registry>

This registers a file named ``main.less`` (from our theme package named
``plonetheme.tango``) as a *resource* named ``tango-main``.
We can now add this resource to a *resource bundle* like the existing ``plone`` bundle:

.. code-block:: xml

   <?xml version="1.0"?>
   <registry>
       <records prefix="plone.resources/tango-main"
                 interface='Products.CMFPlone.interfaces.IResourceRegistry'>
          <value key="css">
             <element>++theme++plonetheme.tango/css/main.less</element>
          </value>
       </records>

       <records prefix="plone.bundles/plone"
                 interface='Products.CMFPlone.interfaces.IBundleRegistry'>
         <value key="resources" purge="false">
           <element>tango-main</element>
         </value>
       </records>
   </registry>

This has the advantage of reducing the number of bundles,
which also means reducing the amount of files which are loaded for the site,
because every bundle will result in *one* compiled CSS file and *one* compiled JavaScript file.
So if we have multiple LESS resources in the same bundle, they will be merged into one compiled
CSS file.

We can also create our own custom bundle which contains our resource (this is the way we
did it in the :doc:`theme-package` chapter):

.. code-block:: xml

   <?xml version="1.0"?>
   <registry>
       <records prefix="plone.resources/tango-main"
                 interface='Products.CMFPlone.interfaces.IResourceRegistry'>
          <value key="css">
             <element>++theme++plonetheme.tango/css/main.less</element>
          </value>
       </records>

       <!-- bundle definition -->
       <records prefix="plone.bundles/tango-bundle"
                 interface='Products.CMFPlone.interfaces.IBundleRegistry'>
         <value key="resources">
           <element>tango-main</element>
         </value>
         <value key="enabled">True</value>
         <value key="compile">True</value>
         <value key="csscompilation">++theme++plonetheme.tango/css/tango-compiled.css</value>
         <value key="last_compilation"></value>
       </records>
   </registry>

This can make sense if we only want to load that bundle under certain conditions,
like in a specific context.
This could lead to a smaller size of loaded static resources, when they are not all needed.

After making changes to the registry, like adding resources to a bundle,
you have to reload the registry configuration via an upgrade step, or via a reinstall of the package.

If you do change the bundle, it has to be built or rebuilt.
You can do this in the ``@@resourceregistry-controlpanel`` by clicking on
*Build* for the bundle involved, or by running the ``plone-compile-resources``
script as follows:

.. code-block:: bash

   $ ./bin/plone-compile-resources --bundle=plone --site-id=Plone

If you have created your own bundle, do the same for this bundle:

.. code-block:: bash

   $ ./bin/plone-compile-resources --bundle=tango-bundle --site-id=Plone

Default value for ``site-id`` is ``Plone`` so you only need to specify that if you're working with a different id for your site object.


Using resources in LESS-files
=============================

Let's have a look at our ``main.less`` file:

.. code-block:: sass

   /* bundle LESS file that will be compiled into tango-compiled.css */

   // ### PLONE IMPORTS ###

   //*// Font families
   //@import "@{barceloneta-fonts}";

   //*// Core variables and mixins
   @import "@{barceloneta-variables}";
       @import "@{barceloneta-mixin-prefixes}";
       @import "@{barceloneta-mixin-tabfocus}";
       @import "@{barceloneta-mixin-images}";
       @import "@{barceloneta-mixin-forms}";
       @import "@{barceloneta-mixin-borderradius}";
       @import "@{barceloneta-mixin-buttons}";
       @import "@{barceloneta-mixin-clearfix}";
   //  @import "@{barceloneta-mixin-gridframework}";
   //  @import "@{barceloneta-mixin-grid}";


   //*// Reset and dependencies
   @import "@{barceloneta-normalize}";
   @import "@{barceloneta-print}";

   //*// Core CSS
   @import "@{barceloneta-scaffolding}";
   @import "@{barceloneta-type}";
   @import "@{barceloneta-code}";
   //@import "@{barceloneta-deco}"; //uncomment for deco variant
   //@import "@{barceloneta-grid}";
   @import "@{barceloneta-tables}";
   @import "@{barceloneta-forms}";
   @import "@{barceloneta-buttons}";
   @import "@{barceloneta-states}";

   //*// Components
   @import "@{barceloneta-breadcrumbs}";
   @import "@{barceloneta-pagination}";
   @import "@{barceloneta-formtabbing}";
   @import "@{barceloneta-views}";
   @import "@{barceloneta-thumbs}";
   @import "@{barceloneta-alerts}";
   @import "@{barceloneta-portlets}";
   @import "@{barceloneta-controlpanels}";
   @import "@{barceloneta-tags}";
   @import "@{barceloneta-contents}";

   //*// Patterns
   @import "@{barceloneta-accessibility}";
   @import "@{barceloneta-toc}";
   @import "@{barceloneta-dropzone}";
   @import "@{barceloneta-modal}";
   @import "@{barceloneta-pickadate}";
   @import "@{barceloneta-sortable}";
   @import "@{barceloneta-tablesorter}";
   @import "@{barceloneta-tooltip}";
   @import "@{barceloneta-tree}";

   //*// Structure
   @import "@{barceloneta-header}";
   @import "@{barceloneta-sitenav}";
   @import "@{barceloneta-main}";
   //@import "@{barceloneta-footer}";
   @import "@{barceloneta-loginform}";
   @import "@{barceloneta-sitemap}";

   //*// Products
   @import "@{barceloneta-event}";
   @import "@{barceloneta-image}";
   @import "@{barceloneta-behaviors}";
   @import "@{barceloneta-discussion}";
   @import "@{barceloneta-search}";

   //*// Products
   @import "@{barceloneta-event}";
   @import "@{barceloneta-image}";
   @import "@{barceloneta-behaviors}";
   @import "@{barceloneta-discussion}";
   @import "@{barceloneta-search}";

   // ### END OF PLONE IMPORTS ###

   // include theme css as less
   @import (less) "business-casual.css";

   // include our custom less
   @import "custom.less";

Here we use different functionality of LESS and the resource registry.

At the bottom line for example, we use LESS-imports to import a second LESS file
which contains our custom LESS statements.
And we also import a CSS-file of the downloaded theme as a LESS-file, so we can
change parts of it using LESS-syntax.

Besides these two, we import stuff from Barceloneta. Here we can see that we use
the names of the registered resource registry resources of the Barceloneta theme
to import them. So if for example we want to import our registered resource
``tango-main``, we could import it as follows in our LESS-file:

.. code-block:: css

   @import "@{tango-main}";

or even with the ``reference`` option:

.. code-block:: css

   @import (reference) "@{tango-main}";

If you use the ``reference`` option on LESS-import, only the parts of this file
which are used are included in the compiled version (CSS).

So for example you have to trigger it like:

.. code-block:: css

   .greenBox{
       &:extend(.box);
       background: green;
   }

or with the ``all`` option, see http://lesscss.org/features/#extend-feature:

.. code-block:: css

   .greenBox{
       &:extend(.box all);
       background: green;
   }

Or just use it as a mixin like this:

.. code-block:: css

   .documentDescription{
     .intro-text;
   }

