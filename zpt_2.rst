.. _zpt2-label:

Customizing Existing Templates
==============================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/04_zpt_2_p5/ src/ploneconf.site

In this part you will:

* Customize existing templates

Topics covered:

* omelette/packages
* z3c.jbot
* moment pattern
* listings
* skins

To dive deeper into real plone data we now look at some existing templates and customize them.


.. _zpt2-news-label:

The view for News Items
-----------------------

We want to show the date a News Item is published. This way people can see at a glance if they are looking at current or old news.

To do this we will customize the template that is used to render News Items.

We use ``z3c.jbot`` for overriding templates. The package already has the necessary configuration in ``browser/configure.zcml``.

* Find the file ``newsitem.pt`` in ``packages/plone/app/contenttypes/browser/templates/`` (in vagrant this directory is in ``/home/vagrant/packages``, otherwise it is in your buildout directory).
* Copy that file into the folder ``browser/overrides/`` of our package. If you use vagrant you'd have to use::

    cp /home/vagrant/packages/plone/app/contenttypes/browser/templates/newsitem.pt /vagrant/buildout/src/ploneconf.site/src/ploneconf/site/browser/overrides/

* Rename the new file from ``newsitem.pt`` to ``plone.app.contenttypes.browser.templates.newsitem.pt``.
* Restart Plone

Now Plone will use the new file to override the original one.

Edit the new file ``plone.app.contenttypes.browser.templates.newsitem.pt`` and insert the following before the ``<div id="parent-fieldname-text"``...:

..  code-block:: html

    <p tal:content="python: context.Date()">
        The current Date
    </p>

Since we use Plone 5 and Chameleon we could also write:

..  code-block:: html

    <p>
        ${python: context.Date()}
    </p>

* Open an existing news item in the browser

This will show something like: ``2015-02-21T12:01:31+01:00``. Not very user-friendly. Let's extend the code and use one of many helpers plone offers.

..  code-block:: html

    <p>
        ${python: plone_view.toLocalizedTime(context.Date())}
    </p>

This will render ``Feb 21, 2015``.

* ``plone_view`` is the BrowserView ``Products.CMFPlone.browser.ploneview.Plone`` and it is defined in the ``main_template`` (Products/CMFPlone/browser/templates/main_template.pt) of Plone 5 like this ``plone_view context/@@plone;`` and thus always available.
* The method ``toLocalizedTime`` runs a date object through Plone's ``translation_service`` and returns the Date in the current locales format, thus transforming ``2015-02-21T12:01:31+01:00`` to ``Feb 21, 2015``.

The same in a slightly different style:

..  code-block:: html

    <p tal:define="toLocalizedTime nocall:context/@@plone/toLocalizedTime;
                   date python:context.Date()"
       tal:content="python:toLocalizedTime(date)">
            The current Date in its local short format
    </p>

Here we first get the plone view and then the method ``toLocalizedTime`` and we use ``nocall:`` to prevent the method toLocalizedTime from being called, since we only want to make it available for later use.

.. note::

    On older Plone versions (using Archetypes) we used ``python:context.toLocalizedTime(context.Date(), longFormat=False)``. That called the python script ``toLocalizedTime.py`` in the Folder ``Products/CMFPlone/skins/plone_scripts/``.

    That folder ``plone_scripts`` holds a multitude of useful scripts that are still widely used. But they are all deprecated and most of theme are gone in Plone 5 and replaced by proper python methods in BrowserViews.


We could also leave the formatting to the frontend. Plone 5 comes with the `moment pattern <http://plone.github.io/mockup/dev/#pattern/moment>`_ that uses the library `moment.js <http://plone.github.io/mockup/dev/#pattern/moment>`_ to format dates. Try the relative calendar format:

..  code-block:: html

    <p class="pat-moment"
       data-pat-moment="format:calendar">
        ${python: context.Date()}
    </p>

Now we should see the date in a user-friendly format like ``Today at 12:01 PM``.


.. _zpt2-summary-label:

The Summary View
----------------

We use the view "Summary View" to list news releases. They should also have the date. The template associated with that view is ``listing_summary.pt``.

Let's look for the template folder_summary_view.pt::

    plone/app/contenttypes/browser/templates/listing_summary.pt


Copy it to ``browser/overrides/`` and rename it to ``plone.app.contenttypes.browser.templates.listing_summary.pt``.

Add the following after line 28:

..  code-block:: html

    <p tal:condition="python:item_type == 'News Item'">
      ${python:plone_view.toLocalizedTime(item.Date())}
    </p>

After you restart the instance and look at the new folder again you'll see the dates.

Our addition renders the date of the respective objects that the template iterates over (thus ``item`` instead of ``context`` since ``context`` would be either a collection aggregating the news items or a folder containing a news item).

The date is only displayed if the variable ``item_type`` is ``News Item``.

Let's take a closer look at that template. How does it know that ``item_type`` is the name of the content type?

The first step to uncovering that secret is line 14 of ``listing_summary.pt``:

.. code-block:: html

    <metal:block use-macro="context/@@listing_view/macros/entries">

``use-macro`` tells Plone to reuse the macro ``entries`` from the view ``listing_view``. That view is defined in ``packages/plone/app/contenttypes/browser/configure.zcml``.  It uses the template ``plone/app/contenttypes/browser/templates/listing.pt``. That makes overriding that much easier :-)

That template ``listing.pt`` defines the slot ``entries`` like this:

..  code-block:: html

    <metal:listingmacro define-macro="listing">
      <tal:results define="batch view/batch">
        <tal:listing condition="batch">
          <div class="entries" metal:define-slot="entries">
            <tal:repeat="item batch" metal:define-macro="entries">
              <tal:block tal:define="obj item/getObject;
                                     item_url item/getURL;
                                     item_id item/getId;
                                     item_title item/Title;
                                     item_description item/Description;
                                     item_type item/PortalType;
                                     item_modified item/ModificationDate;
                                     item_created item/CreationDate;
                                     item_icon item/getIcon;
                                     item_type_class python:'contenttype-' + view.normalizeString(item_type);
                                     item_wf_state item/review_state;
                                     item_wf_state_class python:'state-' + view.normalizeString(item_wf_state);
                                     item_creator item/Creator;
                                     item_link python:item_type in view.use_view_action and item_url+'/view' or item_url;
                                     item_has_image python:view.has_image(obj);
                                     item_is_event python:view.is_event(obj)">

    ...

Here the ``item_type`` is defined as ``item_type item/PortalType``. Let's dig a little deeper and find out what ``item`` and  ``PortalType`` are.

``tal:repeat="item batch"`` tells the template to iterate over an iterable ``batch`` which is defined as ``batch view/batch``.

``view`` is always the BrowserView for which the template is registered. In our case this is either ``plone.app.contenttypes.browser.collection.CollectionView`` if you called that view on a collection, or ``plone.app.contenttypes.browser.folder.FolderView`` for folders. You might remember that both are defined in ``configure.zcml``

Luckily the first is a class that inherits from the second:

..  code-block:: python

    class CollectionView(FolderView):

``batch`` is a method in ``FolderView`` that turns ``results`` into batches. ``results`` exists in both classes. This means, in case the item we are looking at is a collection the method ``results`` of ``CollectionView``, will be used and in case it's a folder the one in ``FolderView``.

To be continued...


.. note::

    In Plone 4 without ``plone.app.contenttypes`` the template to customize would be ``folder_summary_view.pt``, a skin template for Archetypes that can be found in the folder ``Products/CMFPlone/skins/plone_content/``. The customized template would be ``Products.CMFPlone.skins.plone_content.folder_summary_view.pt``.

    The Archetypes template for News Items is ``newsitems_view.pt`` from the same folder. The customized template would then have to be named ``Products.CMFPlone.skins.plone_content.newsitems_view.pt``.

    Keep in mind that not only the names and locations have changed but also the content!


.. _zpt2-finding-label:

Finding the right template
--------------------------

We changed the display of the listing of news items at http://localhost:8080/Plone/news. But how do we know which template to customize?

If you don't know which template is used by the page you're looking at you can make an educated guess, start a debug session or use ``plone.app.debugtoolbar``.

1.  We could check the html with firebug and look for a structure in the content area that looks unique. We could also look for the css class of the body

    .. code-block:: html

        <body class="template-summary_view portaltype-collection site-Plone section-news subsection-aggregator icons-on userrole-anonymous" dir="ltr">

    The class ``template-summary_view`` tells us that the name of the view (but not necessarily the name of the template) is ``summary_view``. So we could search all ``*.zcml``-Files for ``name="summary_view"`` or search all templates called ``summary_view.pt`` and probably find the view and also the corresponding template. But only probably because it would not tell us if the template is already being overridden.

2.  The safest method is using ``plone.app.debugtoolbar``.  We already have it in our buildout and only need to install it. It adds a "Debug"-Dropdown on top of the page. The Section "Published" shows the complete path to the template that is used to render the page you are seeing.

    .. warning::

       plone.app.debugtoolbar is not yet compatible with Plone 5. It kind of works but looks really ugly...

3.  The debug session to find the template is a little more complicated. Since we have ``Products.PDBDebugMode`` in our buildout we can call ``/pdb`` on our page.

    The object that the url points to is by default ``self.context``. But the first problem is that the url we're seeing is not the url of the collection where we want to modify since the collection is the default page of the folder ``news``.

    .. code-block:: python

        >>> (Pdb) self.context
        <Folder at /Plone/news>
        >>> (Pdb) obj = self.context.aggregator
        >>> (Pdb) obj
        <Collection at /Plone/news/aggregator>
        >>> (Pdb) context_state = obj.restrictedTraverse('@@plone_context_state')
        >>> (Pdb) template_id = context_state.view_template_id()
        >>> (Pdb) template_id
        'summary_view'
        >>> (Pdb) view = obj.restrictedTraverse('summary_view')
        >>> (Pdb) view
        <Products.Five.metaclass.SimpleViewClass from /Users/philip/.cache/buildout/eggs/plone.app.contenttypes-1.1b2-py2.7.egg/plone/app/contenttypes/browser/templates/summary_view.pt object at 0x10b00cd90>
        >>> view.index.filename
        u'/Users/philip/workspace/training_without_vagrant/src/ploneconf.site/ploneconf/site/browser/template_overrides/plone.app.contenttypes.browser.templates.summary_view.pt'

    Now we see that we already customized the template.

    Here is a method that could be used in a view or viewlet to display that path :

    ..  code-block:: python

        def get_template_path(self):
            context_state = api.content.get_view(
                'plone_context_state',
                self.context,
                self.request)
            view_template_id = context_state.view_template_id()
            view = self.context.restrictedTraverse(view_template_id)
            return view.index.filename


.. _zpt2-skins-label:

skin templates
--------------

.. only:: not presentation

    Why don't we always only use templates? Because we might want to do something more complicated than get an attribute from the context and render its value in some html tag.

    There is a deprecated technology called 'skin templates' that allows you to simply add some page template (e.g. 'old_style_template.pt') to a certain folder in the ZMI or your egg and you can access it in the browser by opening a url like http://localhost:8080/Plone/old_style_template and it will be rendered. But we don't use it and you too should not, even though these skin templates are still all over Plone.

    Since we use ``plone.app.contenttypes`` we do not encounter many skin templates when dealing with content any more. But more often than not you'll have to customize an old site that still uses skin templates.

Skin templates and python scripts in portal_skins are deprecated because:

* they use restricted python
* they have no nice way to attach python code to them
* they are always callable for everything (they can't easily be bound to an interface)
