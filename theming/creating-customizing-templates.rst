========================================
Creating and customizing Plone templates
========================================

Overriding a Plone template
===========================

A large part of the Plone UI are provided by BrowserView or Viewlet templates.

All viewlets and there managers (sortable containers) you can see when you call the url
``./@@manage-viewlets``).

.. note:: to override them from the ZMI, you can go to ``./portal_view_customizations``.

To overrides them from your theme product, the easiest way is to use
``z3c.jbot`` (Just a Bunch of Templates).

Since jbot is already included in the bobtemplates.plone theme skeleton, you can just start using it, by putting in ``src/plonetheme/tango/browser/overrides`` all the templates you want to override.
But you will need to name them by prefixing the template
name by its complete path to its original version.

For instance, to override ``colophon.pt`` from plone.app.layout, knowing this
template in a subfolder named ``viewlets``, you need to name it
``plone.app.layout.viewlets.colophon.pt``.

.. note:: ZMI > portal_view_customizations is an handy way to find the template path.

You can now restart Plone to see the effect.

Overriding Event Item template
******************************

The path to the template is ``plone/app/event/browser/event_view.pt``, so the full dotted name for our template should be: ``plone.app.event.browser.event_view.pt``. Create a new file with this dotted name into the overrides folder.

Let's say we want move the full text of the event item before the event details block.
So we copy over the original template code and change the order of the two blocks:

.. code-block:: xml

   <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
         xmlns:tal="http://xml.zope.org/namespaces/tal"
         xmlns:metal="http://xml.zope.org/namespaces/metal"
         xmlns:i18n="http://xml.zope.org/namespaces/i18n"
         lang="en"
         metal:use-macro="context/main_template/macros/master"
         i18n:domain="plone.app.event">
   <body>

   <metal:content-core fill-slot="content-core">
   <metal:block define-macro="content-core">
   <tal:def tal:define="data nocall:view/data">

     <div class="event clearfix" itemscope itemtype="http://data-vocabulary.org/Event">

       <ul class="hiddenStructure">
         <li><a itemprop="url" class="url" href="" tal:attributes="href data/url" tal:content="data/url">url</a></li>
         <li itemprop="summary" class="summary" tal:content="data/title">title</li>
         <li itemprop="startDate" class="dtstart" tal:content="data/start/isoformat">start</li>
         <li itemprop="endDate" class="dtend" tal:content="data/end/isoformat">end</li>
         <li itemprop="description" class="description" tal:content="data/description">description</li>
       </ul>

       <div id="parent-fieldname-text" tal:condition="data/text">
         <tal:text content="structure data/text" />
       </div>

       <tal:eventsummary replace="structure context/@@event_summary"/>

     </div>

   </tal:def>
   </metal:block>
   </metal:content-core>

   </body>
   </html>

You can now restart Plone to see the effect.

Creating a new Plone template
=============================

Create dynamic slider content in Plone
**************************************

We need a custom View in Plone to render our dynamic content for the slider.
They are different ways to create Views, for now we use a very simple template-only-view thru jbot and theming-plugins. The bobtemplates.plone skeleton has everything you need already on board.

The only think we need is adding a folder named ``views`` in our theme folder.
Here we now create a template file named ``slider-images.pt``.

.. code-block:: bash

   maik@planetmobile:~/develop/plone/plonetheme.tango/src/plonetheme/tango/theme
   $ tree views/
   views/
   └── slider-images.pt

The template code looks like this:

.. code-block:: xml

   <div id="carousel-example-generic" class="carousel slide">
    <!-- Indicators -->
    <ol class="carousel-indicators hidden-xs">
        <li tal:repeat="item context/keys"
            data-target="#carousel-example-generic"
            data-slide-to="${python:repeat.item.index}"
            class="${python: repeat.item.start and 'active' or ''}"></li>
    </ol>

    <!-- Wrapper for slides -->
    <div class="carousel-inner">
        <div tal:repeat="item context/values"
            class="item ${python: repeat.item.start and 'active' or ''}">
            <img tal:define="scales item/@@images"
                tal:replace="structure python: scales.tag('image', scale='large', css_class='img-responsive img-full')" />
        </div>
    </div>

    <!-- Controls -->
    <a class="left carousel-control" href="#carousel-example-generic" data-slide="prev">
        <span class="icon-prev"></span>
    </a>
    <a class="right carousel-control" href="#carousel-example-generic" data-slide="next">
        <span class="icon-next"></span>
    </a>
   </div>

This is all to create a very simple template only View. You can test the view now.
The View needs some images to show, so we create a folder in Plone named ``slider-images`` and put some images inside. Then we call the View like this ``/slider-images/@@slider-images`` on this folder.
This will render our markup we need to fill the slider.

Take over the dynamic slider content from Plone
***********************************************

Now that we have our slider-images View which renders our HTML markup for the slider, we need to include that on the front-page. For that we use the possibility of Diazo to load the content from other URL's with the href-attribute.

.. code-block:: xml

   <!-- dynamic slider content -->
   <replace
     css:theme="#carousel-example-generic"
     css:content="#carousel-example-generic"
     href="/slider-images/@@slider-images" />

