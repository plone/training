
Customizing existing templates
==============================

To dive deeper into real plone-data we now look at some existing templates and customize them.


newsitem.pt
----------------

We want to show the date a News Item is published. This way people can see at a glance it the are looking at current or old news.

To do this we will customize the templates that is used to render News Items.

We'll basically do the same as when we used at ``portal_skins`` (we customized the footer), but now we'll do it all by hand in our package.

* Create the directoy ``browser/template_overrides``
* Add the following to ``browser/configure.zcml``:

.. code-block:: xml

    <browser:jbot directory="template_overrides" />

* For completeness, add :samp:`z3c.jbot` to the dependencies in :file:`setup.py` to the :samp:`install_requires` list.

* Find the file ``plone/app/contenttypes/browser/templates/newsitem.pt`` in the directory ``omelette`` (in vagrant this is in ``/home/vagrant/omelette``).
* Copy it into the new folder ``cp /home/vagrant/omelette/plone/app/contenttypes/browser/templates/newsitem.pt /vagrant/buildout/src/ploneconf.site/ploneconf/site/browser/template_overrides``
* Rename the new file from ``newsitem.pt`` to ``plone.app.contenttypes.browser.templates.newsitem.pt``.
* Restart Plone

Now Plone should use the new file to override the original one.

Edit the template ``plone.app.contenttypes.browser.templates.newsitem.pt`` and insert the following after line 39:

.. code-block:: html

        <p tal:content="python: context.Date()">
            The current Date
        </p>

* Open an existing news-item in the browser

This will show something like: ``2013-10-02 19:21:15``. Not very user-friendly. Let's extend the code and use one of many helpers plone offers.

.. code-block:: html

    <p tal:define="toLocalizedTime nocall:context/@@plone/toLocalizedTime;
                   date python:context.Date()"
       tal:content="python:toLocalizedTime(date)">
            The current Date in its local short-format
    </p>

Now we should see the date in a user-friendly format like ``17.02.2013``.

* With ``nocall:`` we prevent the method ``toLocalizedTime`` from being called, since we only want to make it available for use.
* The method ``toLocalizedTime`` is provided by the BrowserView ``Products.CMFPlone.browser.ploneview.Plone`` and runs the date-object through Plone's ``translation_service`` and returns the Date in the current locales format, thus transforming ``2013-02-17 19:21:15`` in ``17.02.2013``.

On older Plone-versions we used ``python:context.toLocalizedTime(context.Date(), longFormat=False)``. That called the python-script ``toLocalizedTime.py`` in the Folder ``Products/CMFPlone/skins/plone_scripts/``.

That folder ``plone_scripts`` still holds a multitude of useful scripts that are widely used. But they are all deprecated and will hopefully be gone in Plone 5 and replaced by proper python-methods in browserviews.


summary_view.pt
---------------

We use the view "Summary View" to list news-releases. They should also have the date. The template associated with that view is ``summary_view.pt``.

Let's look for the template folder_summary_view.pt::

    plone/app/contenttypes/browser/templates/summary_view.pt


Copy it to``browser/template_overrides/`` and rename it to ``plone.app.contenttypes.browser.templates.summary_view.pt``.

Add the following after line 29:

.. code-block:: html

    <p tal:condition="python:item_type == 'News Item'"
       tal:content="python:toLocalizedTime(item.Date())">
            News date
    </p>

The method ``toLocalizedTime`` is already defined in the template whose macro this temples uses. Why is that?

The secret is line 15 of ``summary_view.pt``:

.. code-block:: html

    <metal:block use-macro="context/standard_view/macros/entries">

``use-macro`` tells Plone to reuse the macro ``entries`` from the view ``standard_view`` which is found in template ``plone/app/contenttypes/browser/templates/standard_view.pt``.

The templates ``summary_view.pt`` and ``folder_summary_view.pt`` (which is the same but for folders, not collections) are very widely used and also widely customized, so you might as well get to know it a little.

Our addition renders the date of the respective objects that the template iterates over (thus ``item`` instead of ``context`` since ``context`` would be the collection aggregating the news items).

The date is only displayed if the variable ``item_type`` (defined in line 42 of ``standard_view.pt``) is ``News Item``.

There is a lot more going on in ``standard_view.pt`` and ``summary_view.pt`` but we'll leave it at that.

.. note::

    In default Plone without ``plone.app.contenttypes`` this would be ``folder_summary_view.pt``, a skin-template for Archetypes that can be found in the folder ``Products/CMFPlone/skins/plone_content/``. The customzed template would be ``Products.CMFPlone.skins.plone_content.folder_summary_view.pt``.

    The Archetypes-template for News Items is ``newsitems_view.pt`` from the same folder. The customized template would then have to be named ``Products.CMFPlone.skins.plone_content.folder_summary_view.pt``.

    Keep in mind that not only the names have changed but also the content!


Finding the right template
--------------------------

We changed the display of the listing of news-items at http://localhost:8080/Plone/news. But how do we know which template to customize?

If you don't know which template the page you're looking at uses you can do an educated guess, start a debug-session or use ``plone.app.debugtoolbar``.

1.  We could check the html with firebug and look for a structure in the content-area that looks unique. We could also look for the css-class of he body

    .. code-block:: html

        <body class="template-summary_view portaltype-collection site-Plone section-news subsection-aggregator icons-on userrole-anonymous" dir="ltr">

    The class ``template-summary_view`` tells us that the name of the view (but not necessarily the name of the template) is ``summary_view``. So we could search all ``*.zcml``-Files for ``name="summary_view"`` or search all templates calles ``summary_view.pt`` and probably find the view and also the corresponding template. But only probably because it would not tell us if the template is already being overridden.

2.  The safest method is using ``plone.app.debugtoolbar``.  We already have it in our buildout and only need to install it. It adds a "Debug"-Dropdown on top of the page. The Section "Published" shows the complete path to the template that is used to render the page you are seeing.

3.  The debug-session to find the template is a little more complicated. Since we have ``Products.PDBDebugMode`` in our buildout we can call ``/pdb`` on our page.

    The object that the url points to is by default ``self.context``. But the first problem is, that the url we're seeing is not the url of the collection where we want to modify since the collection is the default-page of the folder ``news``.

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

skin-templates
--------------

.. only:: manual

    Why don't we always only use templates? Because we might want to do something more complicated than get an attribute form the context and render it's value in some html-tag.

    There is a deprecated technology called 'skin-templates' that allows you to simply add some page-template (e.g. 'old_style_template.pt') to a certain folder in the ZMI or your egg) and you can access it in the browser by opening a url like http://localhost:8080/Plone/old_style_template and it will be rendered. But we don't use it and you too should not even though these skin-templates are still all over Plone.

    Since we use plone.app.contenttypes we do not encounter many skin-templates when dealing with content any more. But mor often than not you'll have to customize an old site that still uses skin-templates.

    Until now the templates of the default content-types are skin-templates for example. Since we use plone.app.contenttypes we do not encounter many skin-templates when dealing with content any more. But mor often than not you'll have to customize an old site that still uses skin-templates.
    You could append ``/document_view`` to any part of a plone-site to render the default template for documents. You will often get errors since the template ``document_view.pt`` expects the context to have a field 'text' that it attempts to render.

Skin templates and python-scripts in portal_skin are deprecated because:

* they use restricted python
* they have no nice way to attach python-code to them
* they are always callable for everything (they can't be easily bound to an interface)
