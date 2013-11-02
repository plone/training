
Customizing existing templates
==============================

To dive deeper into real plone-data we now look at some existing templates and customize them.

These are not templates based on BrowserViews but skin-templates. You should never write skin-templates but you will often have to customize them.


newsitem_view.pt
----------------

We want to show the date a News Item is published. This way people can see at a glance it the are looking at current or old news.

To do this we will customize the templates that is used to render News Items.

We'll basically do the same as when we used at ``plone.app.themeeditor``, but now we'll do it all by hand.

* Create the directoy ``browser/template_overrides``
* Add the following to ``browser/configure.zcml``:

.. code-block:: xml

    <include package="z3c.jbot" file="meta.zcml" />
    <browser:jbot directory="template_overrides" />

* Find the file ``Products/CMFPlone/skins/plone_content/newsitem_view.pt`` in the directory ``omelette``.
* Copy it into the new folder.
* Rename the new file from ``newsitem_view.pt`` to ``Products.CMFPlone.skins.plone_content.newsitem_view.pt``.
* Restart Plone

Now Plone should use the new file to override the original one.

Edit the template ``Products.CMFPlone.skins.plone_content.newsitem_view.pt`` and insert the following after line 32:

.. code-block:: html

        <p tal:content="python:context.Date()">
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

That folder still holds a multitude of useful scripts that are widely used. But they are all deprecated and will hopefully be gone in Plone 5 and replaced by proper python-methods.


folder_summary_view.pt
-----------------------

We use the view "Summary View" to list news-releases. They should also have the date. The template associated with that view is ``folder_summary_view.pt``.

Let's look for the template folder_summary_view.pt::

    Products/CMFPlone/skins/plone_content/folder_summary_view.pt

Make a copy and rename it::

    browser/template_overrides/Products.CMFPlone.skins.plone_content.folder_summary_view.pt

Add the following after line 25:

.. code-block:: html

    <p tal:condition="python:item_type == 'News Item'"
       tal:content="python:toLocalizedTime(item.Date)">
            News date
    </p>

The method ``toLocalizedTime`` is already defined in the template whose macro this temples uses. Why is that?

The secret is line 12 of ``folder_summary_view.pt``:

.. code-block:: html

    <metal:block
        define-macro="listing"
        extend-macro="context/folder_listing/macros/content-core">

``extend-macro`` tells Plone to extend the macro ``listing`` from the view ``folder_listing`` which is found in template ``Products/CMFPlone/skins/plone_content/folder_listing.pt``.

The template ``folder_summary_view.pt`` is one of the most widely used and most widely customized templates, so you might as well get to know it a little.

Our addition renders the date of the respective objects that the template iterates over (thus ``item`` instead of ``context`` since ``context`` would be the folder containing the nwws items).

The date is only displayed if the variable ``item_type`` (defined in line 57 of ``folder_listing.pt``) is ``News Item``.

There is a lot more going on in ``folder_listing.pt`` and ``folder_summary_view.pt`` but we'll leave it at that.



skin-templates
--------------

Why don't we always only use templates? Because we might want to do something more complicated than get an attribute form the context and render it's value in some html-tag.

There is a deprecated technology called 'skin-templates' that allows you to simply add some page-template (e.g. 'old_style_template.pt') to a certain folder in the ZMI or your egg) and you can access it in the browser by opening a url like http://localhost:8080/Plone/old_style_template and it will be rendered. But we don't use it and you too should not even though these skin-templates are still all over Plone.

The templates of the default content-types are skin-templates for example. You could append ``/document_view`` to any part of a plone-site to render the default template for documents. You will often get errors since the template ``document_view.pt`` expects the context to have a field 'text' that it attempts to render.

Skin templates and python-scripts in portal_skin are deprecated because:

* they use restricted python
* they have no nice way to attach python-code to them
* they are always callable for everything (they can't be easily bound to an interface)