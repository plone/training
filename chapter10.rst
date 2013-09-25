10. Views I (60min) (Patrick und Patrick)
=========================================

A simple browser view
---------------------

First we need to add some boilerplate-code to be able to use a template. We could use paster again::

    $ cd src/plonekonf.talk/src
    $ ../../../bin/paster add browserview

Enter 'Demo' as answer to the only question asked.

This creates a the boilerplate that allows us to use a template without having to care about registering it in plone and providing a view for now.

We could also do it by hand. To do that we'd add the following to ``browser/configure.czml``:

.. code-block:: xml

    <browser:page
       name="demoview"
       for="*"
       class=".views.DemoView"
       template="templates/demoview.pt"
       permission="zope2.View"
       />

add a file views.py. It should hold::

    from Products.Five.browser import BrowserView

    class DemoView(BrowserView):
        """ This does nothing so far
        """

Add a directory ``templates`` inside the directory ``browser`` and and in it an empty file ``demoview.pt``

Restart the site and open http://localhost:8080/Plone/@@demoview.

You should see an empty page. We now have everything in place to learn about page templates.


Zope Page Templates
-------------------

Page Templates are HTML-files with some additional Information, written in TAL, METAL and TALES.

Page templates must be valid xml.

The three languages are.

* TAL: "Template Attribute Language"

  * Templating XML/HTML using special Attributes

  * Using TAL we include TALES-Expressions into html

* TALES: "TAL Expression Syntax"

  * defines how the expressions Ausdrücke, welche die TAL-Anweisungen auswerten, notiert werden müssen, damit der Zugriff auf Objekte, Eigenschaften und Methoden funktioniert

* METAL: "Macro Expansion for TAL"

  * this enables us to combine, re-use and nest templates together

TAL and METAL are written like html-attribues (url, src, title). TALES are written like the values of these attributes. A typical TAL-Statement looks like this:

.. code-block:: html

    <title tal:content="context/title">
        The Title of the content
    </title>

It's used to modify the output:

.. code-block:: html

    <p tal:content="string:I love red">I love blue</p>

results in:

.. code-block:: html

    <p>I love red</p>

Let's try it. Open the file ``demoview.pt`` and empty it since we don't need the text that was put in by default.

Instead enter the following:

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          lang="en"
          i18n:domain="plonekonf.talk">
    <body>

        <p>red</p>

    </body>
    </html>


Chameleon
---------

Chameleon is the successor of TAL and will be shipped in Plone 5.

- Plip for Chameleon: https://dev.plone.org/ticket/12198
- Homepage: http://www.pagetemplates.org/
- Integration-layer for Plone: `five.pt <https://pypi.python.org/pypi/five.pt>`_

In Plone 4 we still use the default ZPT.


TAL and TALES
-------------

Let's add some magic and modify the <p>-tag:

.. code-block:: html

    <p tal:content="string:blue">red</p>

This will result in:

.. code-block:: html

    <p>blue</p>

Try this out and (without restarting Plone) open http://localhost:8080/Plone/@@demo_view.

The same happens with attributes. Replace the <p>-line with:

.. code-block:: html

    <a href="http://www.mssharepointconference.com"
       tal:define="a_fine_url string:http://www.ploneconf.org"
       tal:attributes="href a_fine_url"
       tal:content="string:A even better conference">
        A sharepoint conference
    </a>

results in:

.. code-block:: html

    <a href="http://www.ploneconf.org">
        A even better conference
    </a>

We used three TAL-Attributes here. This is the complete list of TAL-attributes:

``tal:define``
    define variables. We definded the variable url to the string "http://www.ploneconf.org"

``tal:content``
    replace the content of an element. We replaced the default-content about some with "A even better conference"

``tal:attributes``
    dynamically change element attributes. We set the html-attribute ``href`` to the variable ``a_fine_url``

``tal:condition``
    tests, if the expression is true or false.

``tal:repeat``
    repeats an iterable element, in our case the list of talks.

``tal:replace``
    replace the content of an element like ``tal:content`` but removes the element only leaving the content.

``tal:omit-tag``
    remove an element, leaving the content of the element.

``tal:on-error``
    handle errors.


python-expressions
++++++++++++++++++

So far we only used one TALES expression (the ``string:``-bit). Let's use a different TALES-expression now. With ``python:`` we can use python-code. A simple example:

.. code-block:: html

    <p tal:define="title context/title"
       tal:content="python:title.upper()">
       A big title
    </p>

And another:

.. code-block:: html

    <p tal:define="talks python:['Dexterity for the win!',
                                 'Deco is the future',
                                 'A keynote on some weird topic',
                                 'The talk that I did not submit']"
       tal:content="python:talks[0]">
        A talk
    </p>

With python-expressions

* you can only write single statements
* you could import things but you should not (example: ``tal:define="something modules/Products.PythonScripts/something;``).


tal:condition
+++++++++++++

``tal:condition``
    tests, if the expression is true or false.

* If it's true, then the tag is rendered.
* If it's false then the tag **and all its cheildren** are removed and no longer evaluated.
* We can reverse the logic by prepending a ``not:`` to the expression.

Let's add another TAL-Attribute to our above example::

    ``tal:condition="talks"``

We could also test for the number of talks::

    tal:condition="python:len(talks) >= 1"

or if a certain talk is in the list of talks::

    tal:condition="python:'The talk that I did not submit' in talks"


tal:repeat
++++++++++

Let's try another statement:

.. code-block:: html

    <p tal:define="talks python:['Dexterity for the win!',
                                 'Deco is the future',
                                 'A keynote on some weird topic',
                                 'The talk that I did not submit']"
       tal:repeat="talk talks"
       tal:content="talk">
       A talk
    </p>

tal:repeat
    repeats an iterable element, in our case the list of talks.

We change the markup a little to construct a self-populating list:

.. code-block:: html

    <ul tal:define="talks python:['Dexterity for the win!',
                                  'Deco is the future',
                                  'A keynote on some weird topic',
                                  'The talk that I did not submit']">
        <li tal:repeat="talk talks"
            tal:content="talk">
              A talk
        </li>
        <li tal:condition="not:talks">
              Sorry, no talks yet.
        </li>
    </ul>


path-expressions
++++++++++++++++

Regarding TALES so far we used ``string:`` or ``python:`` or only variables. The next and most common expression are path-expressions. Optionally you can start a path-expression with ``path:``

Every path expression starts with a variable name. It can either an object like context, view or template or a variable defined earlier.

After the variable we add a slash (‘/’) and the name of a sub-object, attribute or callable. The '/' is used to end the name of an object and the start of the property name. Properties themselves may be objects that in turn have properties.

.. code-block:: html

    <p tal:content="context/title"></p>

We can chain several of those to get to the information we want.

.. code-block:: html

    <p tal:content="context/REQUEST/form"></p>

This would return the value of the form-dictionary of the HTTPRequest-object. Useful for form-handling.

The '|' ("or") character is used to find an alternative value to a path if the first path evaluates to 'Nothing' or does not exist.

.. code-block:: html

    <p tal:content="context/title | context/id"></p>

There are several built in variables that can be used in paths:

The most frequently used one is ``nothing`` which is the equivalent to None

.. code-block:: html

    <p tal:replace="nothing">
        this comment will not be rendered
    </p>

A dict of all the available variables is ``CONTEXTS``

.. code-block:: html

    <dl tal:define="path_variables_dict CONTEXTS">
      <tal:vars tal:repeat="variable path_variables_dict">
        <dt tal:content="variable"></dt>
        <dd tal:content="python:path_variables_dict[variable]"></dd>
      </tal:vars>
    </dl>

Useful for debugging :-)


pure TAL-blocks
+++++++++++++++

We can use TAL-attributes auch without HTML-Tags. This is useful when we don't need to add any tags to the markup

Syntax:

.. code-block:: html

    <tal:block attribute="expression">some content</tal:block>

Examples:

.. code-block:: html

    <tal:block define="id template/id">
    ...
      <b tal:content="id">The id of the template</b>
    ...
    </tal:block>

    <tal:news condition="python:context.content_type == 'News Item'">
        only visible for news
    </tal:news>


handling complex data in templates
++++++++++++++++++++++++++++++++++

Let's move on to a little more complex data. And to another TAL-atrribute:

tal:replace
    replace the content of an element and removes the element only leaving the content.

Example:

.. code-block:: html

    <p>
        <img tal:define="tag string:<img src='https://plone.org/logo.png'>"
             tal:replace="tag">
    </p>

this results in:

.. code-block:: html

    <p>
        &lt;img src='https://plone.org/logo.png'&gt;
    </p>

``tal:replace`` drops it's own base-tag in favor of the result of the TALES-expression. Thus the original ``<img... >`` is replaced. But the result is escaped by default.

To prevent escaping we use ``structure``

.. code-block:: html

    <p>
        <img tal:define="tag string:<img src='https://plone.org/logo.png'>"
             tal:replace="structure tag">
    </p>

Now let's emulate a typical Plone structure by creating a dictionary.

.. code-block:: html

    <table tal:define="talks python:[{'title':'Dexterity for the win!',
                                      'subjects':('content-types', 'dexterity')},
                                     {'title':'Deco is the future',
                                      'subjects':('layout', 'deco')},
                                     {'title':'The State of Plone',
                                      'subjects':('keynote',) },
                                     {'title':'Diazo designs dont suck!',
                                      'subjects':('design', 'diazo', 'xslt')}
                                    ]">
        <tr>
            <th>Title</th>
            <th>Topics</th>
        </tr>
        <tr tal:repeat="talk talks">
            <td tal:content="talk/title">A talk</td>
            <td tal:define="subjects talk/subjects">
                <span tal:repeat="subject subjects"
                      tal:replace="subject">
                </span>
            </td>
        </tr>
    </table>

We emulate a list of talks and display information obout them in a table. We'll get back to the list of talks later when we use the real talk-objects that we created with dexterity.

To complete the list here are the TAL-Attributes we have not yet used:

tal:omit-tag
    Omit the element tags, leaving only the inner content.

tal:on-error
    handle errors.

When an element has multiple statements, they are executed in this order:

1. define
2. condition
3. repeat
4. content or replace
5. attributes
6. omit-tag



METAL and macros
----------------

Why is our output so ugly? How do we get our html to render in Plone the UI?

We use METAL (Macro Extension to TAL) to define slots that we can fill and macros that we can reuse.

We add to the ``<html>``-tag::

    metal:use-macro="context/main_template/macros/master"

And then wrap the code we want to put in the content-area of Plone in:

.. code-block:: html

    <metal:content-core fill-slot="content-core">
        <p>Some content</p>
    </metal:content-core>

This will put our code in a section defined in the main_template called "content-core".


macros in browser-views
+++++++++++++++++++++++

writing a macro

.. code-block:: html

    <div metal:define-macro="my_macro">
        <p>I can be reused</p>
    </div>

in zcml:

.. code-block:: xml

    <browser:page
      for="*"
      name="plonekonf.talk.macros"
      template="templates/macros.pt"
      permission="zope2.View"
      />

use it the template:

.. code-block:: html

        <div metal:use-macro="view/context/@@plonekonf.talk.macros/my_macro">
            the macro
        </div>


Accessing Plone from the template
---------------------------------

In our template we have access to the context object on which the view is called on, the browser-view itself (i.e. all python-methods we'll put in the view later on), the request and response objects and with these we can get almost anything.

In templates we can also access other browser-views. Some of those exist to provide easy access to helper code snippets we often need (an basic api so to say)::

    tal:define="context_state context/@@plone_context_state;
                portal_state context/@@plone_portal_state;
                plone_tools context/@@plone_tools;
                plone_view context/@@plone;"

These helper-views are very widely used.

TODO: *Show these views and their uses*


Customizing existing templates
------------------------------

To dive deeper into real plone-data we now look at some existing templates and customize them.

newsitem_view.pt
++++++++++++++++

We want to show the date a News Item is published. This way people can see at a glance it the are looking at current or old news.

Explain how to find files in sublime :-)

Add the following at line 28:

.. code-block:: html

        <p tal:content="python:context.Date()">
                The current Date
        </p>

This will show something like: ``2013-10-02 19:21:15``. Not very user-friendly. So lets extend the code and use one of many helpers plone offers.

.. code-block:: html

        <p tal:content="python:context.toLocalizedTime(context.Date(),long_format=0)">
                The current Date in its local short-format
        </p>

Hier wird eine der vielen praktischen Hilfen, die Plone zur Verfügung stellt, verwendet.
Das script ``toLocalizedTime.py`` aus dem Ordner ``Products/CMFPlone/skins/plone_scripts/`` nimmt das Datums-Objekt entgegen und gibt die Zeit in dem lokal gültigen Format zurück und transformiert so ``2010-02-17 19:21:15`` in ``17.02.2010``.

Im Verzeichnis ``plone_scripts/`` finden sich noch viele praktische Sachen, von den man oft glaubt die selber schreiben zu müssen.
Beispielsweise ``unique.py``, das doppelte Elemente aus Listen entfernt.


folder_summary_view.pt
++++++++++++++++++++++

We use folder_summary_view.pt to list news-releases. They should also have the date.

Let's look for the template folder_summary_view.pt::

    training/parts/omelette/Products/CMFPlone/skins/plone_content/folder_summary_view.pt

copy it to::

    training/src/plonekonf.talk/src/plonekonf/talk/browser/template_overrrides/Products.CMFPlone.skins.plone_content.folder_summary_view.pt

Open the new file and explain...

Wir ändern an der Datei ``folder_summary_view.pt`` und fügen in Zeile 80 folgenden Code ein

.. code-block:: html

    <p tal:condition="python:item_type == 'News Item'"
       tal:content="python:item.toLocalizedTime(item.Date,long_format=0)">
            The current Date in it's local short-format
    </p>

Hier wird das Veröffentlichungsdatum des jeweiligen Objektes (daher ``item`` statt ``context`` denn ``context`` wäre in diesem Fall der Ordner in dem sich Items befinden) angezeigt.

Zunächst wird aber die in Zeile 61 definierte Variable ``item_type`` abgefragt und die Anzeige davon abhängig gemacht ob es sich um ein ``News Item`` (d.h. eine ``Nachricht``) handelt.

Der Inhalt des Ordners wird in Zeile 47 mit::

    here.getFolderContents()

ausgelesen. Tatsächlich etwas komplexer, da u.a. zunächst geprüft wird ob es sich um eine Collection handelt.

``getFolderContents`` ist übrigens auch ein Python-Script ``Products/CMFPlone/skins/plone_scripts/`` und liefert über eine Katalogabfrage alle Objekte innerhalb des jeweiligen Ordners.


What we missed
--------------

The are some things we did not cover so far:

``tal:condition="exists:expression"``
    checks if an object or an attribute exists (seldom used)

``tal:condition="nocall:context"``
    to explicitly not call a callable.

If we refer to content objects, without using the nocall: modifier these objects are unnecessarily rendered in memory as the expression is evaluated.

``i18n:translate`` and ``i18n:domain``
    the strings we put in templates can be translated automatically.

There is a lot more about TAL, TALES and METAL that we have not covered. You'll only learn it if you keep reading, writing and customizing templates.


skin-templates
--------------

Why don't we always only use templates? Because we might want to do somehing more complicated than get an attribute form the context and render it's value in some html-tag.

There is a deprecated technology called 'skin-templates' that allows you to simply add some page-template (e.g. 'old_style_template.pt') to a certain folder in the ZMI or your egg) and you can access it in the browser by opening a url like http://localhost:8080/Plone/old_style_template and it will be rendered. But we don't use it and you should not even though these skin-templates are still all over Plone.

The templates of the default content-types are skin-templates for example. You could append '/document_view' to any part of a plone-site. You will often get errors since the template document_view.pt expects the context to have a field 'text' that it attempts to render.

* use restricted python
* have no nive way to attach python-code to them
* allways exist for everything (they can't be easily bound to an interface)

