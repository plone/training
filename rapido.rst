Rapido
======

In this part you will:

* create a "Like" button on any talk so visitors can vote,
* display the total of votes will be displayed next to the button,
* create a Top 5 page,
* reset the votes on workflow change.

Topics covered:

* Create a Rapido app
* Insert Rapido blocks in Plone pages
* Implement scripts in Rapido

What is Rapido?
---------------

.. only:: presentation

    * A Plone add-on,
    * it extends your Plone site features,
    * entirely through the theming tool.

.. only:: not presentation

    Rapido is a Plone add-on allowing to implement custom features on top of Plone.

    It is a simple yet powerful way to extend the behavior of your Plone site without using the Plone underlying frameworks.

    The unique interface to build applications with rapido.plone is the **Plone theming tool**.

    It implies it can be achieved in the **file system** or through the theming **inline editor**.

    A Rapido application is just a piece of your current theme, it can be imported, exported, copied, modified, etc. like the rest of the theme. But in addition to layout and design elements, it might contain some business logic implemented in Python.

Few comparisons
---------------

.. only:: presentation

    * It focuses on features, not on content types like Dexterity,
    * It can be displayed using Diazo or as a Mosaic tile but cannot manage design or layouts,
    * It is easier than regular Plone development.

.. only:: not presentation

    * Compare to **Dexterity**:

        * Dexterity focuses on content types, and content types can only use the Plone business logic, you cannot implement your own logic,
        * but Rapido allows to store data but not **Plone contents** (at least, not directly like Dexterity does).

    * Compare to **Diazo** and **Mosaic**:

        * Diazo manages the Plone theme,
        * Mosaic allows to manage layouts by positionning tiles,
        * Rapido cannot do that, but a Rapido block can be called from a Diazo rule or displayed in a Mosaic tile.

    * Compare to manual Plone development:

        * Rapido is simpler: no need to learn about any framework, no need to create Python eggs,
        * but Rapido code runs in restricted mode, so you cannot import any unsafe Python module in your code.

Installation
------------

.. only:: presentation

    Our pre-set Plone instances already provide Rapido.

.. only:: not presentation

    Modify ``buildout.cfg`` to add Rapido as a dependency::

        eggs =
            ...
            rapido.plone

    Run your buildout::

        $ bin/buildout -N

    Then go to Plone control panel / Add-ons http://localhost:8080/Plone/prefs_install_products_form, and install Rapido.

Principles
----------

.. only:: presentation

    * Rapido application
    * block
    * element
    * record

.. only:: not presentation

    * Rapido application: it contains the features you implement, physically it is just a folder,
    * block: it displays a chunck of HTML which can be inserted in your Plone pages,
    * element: elements are the dynamic components of your blocks, they can be input fields, buttons, just computed HTML. They can also return JSON if you call them from a JS app,
    * records: a Rapido app is able to store data into records. Records are just basic value dictionaries.

How to create a Rapido app
--------------------------

.. only:: presentation

    * a folder in our Diazo theme::

        /rapido/<app-name>

    * a sub-folder with blocks::

        /rapido/<app-name>/blocks


.. only:: not presentation
    
    A Rapido app is defined by a set of files in our Diazo theme.

    The files need to be in a specific location::

        /rapido/<app-name>

Here is a typical layout for a rapido app::

    /rapido
        /myapp
            settings.yaml
            /blocks
                stats.html
                stats.py
                stats.yaml
                tags.html
                tags.py
                tags.yaml

Blocks and elements
-------------------

.. only:: presentation

    * Blocks are the app components.
    * They contain elements (fields, buttons, etc.)
    * A block is defined by 3 files:

        - a YAML file to declare elements,
        - an HTML (or .pt) file for the layout,
        - a Python file to implement the logic.

.. only:: not presentation

    The app components are `blocks`. A block is defined by a set of 3 files (HTML,
    Python, and YAML files) located in the ``blocks`` folder.

    The **YAML file** defines the elements. An element is any dynamically generated
    element in a block, it can be a form field (input, select, etc.), but
    also a button (``ACTION``), or even just a piece of generated HTML (``BASIC``).

    The **HTML file** contains the layout of the block. The templating mechanism is
    super simple, elements are just enclosed in brackets, like this:
    ``{my_element}``.

    The **Python file** contains the application logic. We will see later how exactly we use those Python files.

Exercise 1: Create the vote block
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's start by displaying a static counter showing "0 votes" on all talks.

First, we need to create a ``rating`` Rapido app.

..  admonition:: Solution
    :class: toggle

    * Go to the Plone theming control panel http://localhost:8080/Plone/@@theming-controlpanel
    * Copy the Barceloneta theme, name it ``training`` and enable it immediately,
    * Add a new folder named ``rapido``,
    * And add a subfolder named ``rating``.

    The Rapido app is initialized.

And now, we need to create a ``rate`` block.

..  admonition:: Solution
    :class: toggle

    * Add a folder named ``blocks`` in ``rating``,
    * In ``blocks``, add a file named ``rate.html``,
    * In the file, put the following content:
        
        .. code-block:: html

            <span>0 votes</span>

Once the block is ready, and you can display it by calling its URL:

http://localhost:8080/Plone/@@rapido/rating/block/rate

But we would prefer to display it inside our existing Plone pages.

Include Rapido blocks in Plone pages
------------------------------------

We can include Rapido blocks in Plone pages using Diazo rules.

The `include` rule is able to load another URL than the current page, extract a piece of HTML from it, and include it in a regular Diazo rules (`after`, `before`, etc.).

So the following rule:

.. code-block:: xml

    <after css:content="#content">
        <include href="@@rapido/stats/block/stats" css:content="form"/>
    </after>

would insert the `stats` block under the Plone main content.

Rapido rules can be added directly in our theme's main ``rules.xml``, but it is a good practice to put them in a dedicated file rule file which can be located in our app folder.

The app specific rules file can by included in the main rules files that way:

.. code-block:: xml

    <xi:include href="rapido/myapp/rules.xml" />

Exercise 2: Display the vote block in Plone pages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Insert the ``rate`` block content under the Plone page main heading.

..  admonition:: Solution
    :class: toggle

    * in the main ``rules.xml``, add the following line at the begining of the ``<rules>`` tag:

        .. code-block:: xml

            <xi:include href="rapido/rating/rules.xml" />

    * In the ``rating`` folder, add a new file named ``rules.xml`` containing:

        .. code-block:: xml

            <?xml version="1.0" encoding="utf-8"?>
            <rules xmlns="http://namespaces.plone.org/diazo"
                   xmlns:css="http://namespaces.plone.org/diazo/css"
                   xmlns:xhtml="http://www.w3.org/1999/xhtml"
                   xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                   xmlns:xi="http://www.w3.org/2001/XInclude">

                <after css:content=".documentFirstHeading" css:if-content=".template-view.portaltype-talk">
                    <include href="@@rapido/rating/block/rate" css:content="form"/>
                </after>
             
            </rules>

        Let's detail what it does:

        * the ``after`` rule targets the page title (identified by the ``.documentFirstHeading`` selector), but only applies when we are viewing a talk (``.template-view.portaltype-talk``),
        * the ``include`` rule retrieves the Rapido block content.

Now, if you visit a talk page, you see the counter below the heading.

Make our blocks dynamic
-----------------------

.. only:: presentation

    * We can include dynamic **elements** in our block layout.
    * Elements will be declared in the YAML file.
    * They will computed using code provided in the Python file.

.. only:: not presentation

    The YAML file allows to declare elements.
    The Python files allows to implement the element value using a function named after the element id.
    And the HTML file can display elements using the curly brackets notation.
    The 3 files must have the same name (only the extensions change).

    As mentionned earlier, the **Python file** contains the application logic.

    It is a set of Python functions which names refer to the element or the event they are related to.

    For a ``BASIC`` element for instance, we are supposed to provide a function having
    the same name as the element, its returned value will be inserted in the block at
    the location of the element.

    For an ``ACTION``, we are supposed to provide a function having the same name as
    the element, it will be executed when a user clicks on the action button.

A typical element will defined and used that way:

* definition in the YAML file:

    .. code-block:: yaml

        elements:
            answer:
                type: BASIC

* implementation in the Python file:

    .. code-block:: python

        def answer(context):
            return 42

* insertion in the HTML template:

    .. code-block:: html

        <span>Answer to the Ultimate Question of Life, the Universe, and Everything: {answer}</span>

Exercise 3: Create an element to display the votes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's replace the "0" value in your rate block with a computed value.

You need to add an element to your block.
For now the Python function will just return 10.

..  admonition:: Solution
    :class: toggle

        * In the ``blocks`` folder, add a new file named ``rate.yaml`` containing:

            .. code-block:: yaml

                elements:
                    display_votes:
                        type: BASIC

        * Add also a file named ``rate.py`` containing:

            .. code-block:: python

                def display_votes(context):
                    return 10

        * And change the existing ``rate.html`` that way:

            .. code-block:: html

                <span>{display_votes} votes</span>


Now, if you refresh your talk page, the counter will display the value returned by your Python function.

Create actions
--------------

An action is a regular element, but it is rendered as a button.

Its associated Python function in the Python file will be called when the user clicks on the button.

Example:

* YAML:

    .. code-block:: yaml

        elements:
            change_page_title:
                type: ACTION
                label: Change the title

* Python:

    .. code-block:: python

        def change_page_title(context):
            context.content.title = "A new title"

* HTML:

    .. code-block:: html

        <span>{change_page_title}</span>


Everytime the user clicks the action, the block is reloaded (so elements are refreshed).

When the block is inserted in a Plone page using a Diazo rule, the reloading will just replace the current page with the bare block.
Usually this is not what we want. If we want them to preserve the current Plone page, we need to activate the AJAX mode in the YAML file:

    .. code-block:: yaml

        target: ajax

Exercise 4: Add the Like button
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add a Like button to the block. For now, the action itself will do nothing, let's just insert it at the right place, and make sure the block is refreshed properly when we click.

..  admonition:: Solution
    :class: toggle

    * in ``rate.yaml``, add the following new element:

        .. code-block:: yaml

            target: ajax
            elements:
                like:
                    type: ACTION
                    label: Like

    * in ``rate.py``, add a new function:

        .. code-block:: python

            def like(context):
                # do nothing for now

    * and in ``rate.html``:

        .. code-block:: html

            <span>{like} {display_votes} votes</span>

Store data
----------

Each Rapido app provides an internal storage utility able to store records.

Records are not Plone objects, they are just simple dictionnaries of basic data (strings, numbers, dates, etc.). There is no constraint on the dictionnary items but Rapido will always set an ``id`` item, so this key is reserved.

Something like::

    {'id': 'record_1', 'name': 'Eric', 'age': 42}

could a valid record.

The Rapido Python API allows to create, get or delete records:

.. code-block:: python

    record = context.app.create_record(id="my-record")
    record = context.app.get_record("other-record")
    context.app.delete_record("other-record")

The record items are managed like regular Python dictionnary items:

.. code-block:: python

    record.get('age', 0)
    'age' in record
    record['age'] = 42
    del record['age']

Exercise 5: Count votes
^^^^^^^^^^^^^^^^^^^^^^^

The button is OK now, now let's focus on counting votes. To count the votes on a talk, you need store some information:

- an identifier for the talk (we will take the talk path using the Plone ``absolute_url_path()`` method)
- the total votes it gets

Let's implement the ``like`` function:

- first we need to get the current talk: the Rapido ``context`` allows to get the current Plone content using ``context.content``,
- then we need to get the record corresponding to the current talk,
- if it does not exist, we need to create it,
- and then we need to increase its current total votes by 1.

..  admonition:: Solution
    :class: toggle

    .. code-block:: python

        def like(context):
            current_talk = context.content
            talk_path = current_talk.absolute_url_path()
            record = context.app.get_record(talk_path)
            if not record:
                record = context.app.create_record(id=talk_path)
                record['total'] = 0
            record['total'] += 1

.. only:: not presentation

    Note: we cannot just use the content ``id`` attribute as a valid identifier because it is not unique at site level, so we prefer the path.

Now let's make sure to display the proper total in the ``display_votes`` element:

- here also, we need to get the current talk,
- then we get the corresponding record,
- and we get its current total votes

    .. code-block:: python

        def display_votes(context):
            talk_path = context.content.absolute_url_path()
            record = context.app.get_record(talk_path)
            if not record:
                return 0
            return record['total']

HTML templating vs TAL templating
---------------------------------

HTML templating
^^^^^^^^^^^^^^^

The Rapido HTML templating is very simple.
It is just plain HTML with curly bracket notations to insert elements:

.. code-block:: html

    <p>This is my message: {message}</p>

If the element is not an object, we can render its properties:

.. code-block:: python

    def doc(context):
        return context.content

.. code-block:: html

    <p>This is my title: {doc.title}</p>

And if the element is a dictionary, we can access its items:

.. code-block:: python

    def stats(context):
        return {'avg': 10, 'total': 120}

.. code-block:: html

    <p>Average: {stats[avg]}</p>

Ît is easy to use but it cannot perform loops or conditional insertion.

TAL templating
^^^^^^^^^^^^^^

TAL templating is the templating format used in the core of Plone.
If HTML templating is too limitating, Rapido allows to use TAL instead.

We just need to provide a file with the ``.pt`` extension instead of the HTML file.

The block elements are available in the ``elements`` object:

.. code-block:: python

    def my_title(context):
        return "Chapter 1"

.. code-block:: html

    <h1 tal:content="elements/my_title"></h1>

Elements can be used as conditions:

.. code-block:: python

    def is_footer(context):
        return True

.. code-block:: html

    <footer tal:condition="elements/is_footer">My footer</footer>

If an element returns an iterable object (list, dictionnary), we can make a loop:

.. code-block:: python

    def links(context):
        return [
            {'url': 'https://validator.w3.org/', 'title': 'Markup Validation Service'},
            {'url': 'https://www.w3.org/Style/CSS/', 'title': 'CSS'},
        ]

.. code-block:: html

    <ul>
        <li tal:repeat="link elements/links">
            <a tal:attributes="link/url"
               tal:content="link/title"></a>
        </li>
    </ul>

The current Rapido context is available in the ``context`` object:

.. code-block:: html

    <h1 tal:content="context/content/title"></h1>

See the `TAL commands documentation <http://www.owlfish.com/software/simpleTAL/tal-guide.html>`_ for more details about TAL.

Create custom views
-------------------

For now, we have just added small chuncks of HTML in existing pages. But Rapido also allows to create a new page (a Plone developer would name it a new **view**).

Let's imagine we want to display one of our Rapido block in the main content area instead of the regular content. We could do it with a simple ``replace`` Diazo rule:

.. code-block:: xml

    <replace css:content="#content">
        <include href="@@rapido/stats/block/stats" css:content="form"/>
    </replace>

But if we do that, the regular content will not be accessible anymore. What if we want to be able to access both the regular content with its regular URL, and have an extra URL to display our block as main content?

Rapido allows to declare **neutral views**.

By adding ``@@rapido/view/<any-name>`` to a content URL we get the content's
default view. The ``any-name`` value can actually be **anything**, we do not really care, we just use it to match a Diazo rule in charge of replacing the default content with our block:

.. code-block:: xml

    <rules if-path="@@rapido/view/show-stats">
        <replace css:content="#content">
            <include css:content="form" href="/@@rapido/stats/block/stats" />
        </replace>      
    </rules>

Now if we visit for instance::

    http://localhost:8080/Plone/page1/@@rapido/view/show-stats

we do see our block instead of the regular page content.

(And if we visit http://localhost:8080/Plone/page1, we get the regular content of course.)

Exercise 5: Create the Top 5 page
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's create a block to display the Talks Top 5:

- It needs to be a specific view.
- We will use a TAL template (but for now the content will be fake and static).
- Visitors will access it from a footer link.

..  admonition:: Solution
    :class: toggle

    First we create a ``top5.pt`` file in the ``blocks`` folder with the following content:

    .. code-block:: html

        <h1 class="documentFirstHeading">Talks Top 5</h1>
        <section id="content-core">Empty for now</section>

    Now we add the following to our ``rules.xml`` file:

    .. code-block:: xml

        <rules if-path="@@rapido/view/talks-top-5">
            <replace css:content-children="#content">
                <include css:content="form" href="/@@rapido/rating/block/top5" />
            </replace>      
        </rules>

    And then we declare a new action in our footer:

    - go to Site Setup / Actions
    - add a new action in Site actions category with name "Top 5" and as URL::

        string:${globals_view/navigationRootUrl}/talks-top-5

Index and query records
-----------------------

Rapido record items can be indexed, so we can filter or sort records easily.

Indexing is declared in the block YAML file using the ``index_type`` property. Example:

.. code-block:: yaml

    target: ajax
    elements:
        firstname:
            type: BASIC
            index_type: field

The ``index_type`` property can have two possible values:

- ``field``: such index matches exact values, and support comparison queries, range queries, and sorting.
- ``text``: such index matches contained words (applicable for text values only).

Queries use the *CQE format* (`see documentation <http://docs.repoze.org/catalog/usage.html#query-objects>`_.

Example (assuming `author`, `title` and `price` are existing indexes):

.. code-block:: python

    context.app.search(
        "author == 'Conrad' and 'Lord Jim' in title",
        sort_index="price")

To update a record indexing, we can use the Rapido Python API:

.. code-block:: python

    myrecord.save() # this will also run the on_save event
    myrecord.reindex() # this will just (re-)index the record

We can also reindex all the records using the ``refresh`` URL command::

    http://myserver.com/Plone/@@rapido/<app-id>/refresh


Exercise 6: Compute the top 5
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We want to be able to sort the records according their votes:

- we need to declare the ``total`` item as an indexed element,
- we need to refresh all our stored record,
- we need to update the ``top5`` block to display the first 5 ranked talks.

..  admonition:: Solution
    :class: toggle

    We add the following to ``rate.yaml`` containing:

    .. code-block:: yaml

        elements:
            ...
            total:
                type: BASIC
                index_type: field

    We call the refresh URL to make sure our existing votes are indexed:

        http://localhost:8080/Plone/@@rapido/rating/refresh

    Now let's change the ``top5`` block:

    - we create ``top5.yaml``:

        .. code-block:: yaml

            elements:
                talks:
                    type: BASIC

    - we create ``top5.py``:

        .. code-block:: python

            def talks(context):
                search = context.app.search(
                    "total>0", sort_index="total", reverse=True)[:5]
                results = []
                for record in search:
                    content = context.api.content.get(path=record["id"])
                    results.append({
                        'url': content.absolute_url(),
                        'title': content.title,
                        'total': record["total"]
                    })
                return results

    - we update ``top5.pt``:

        .. code-block:: html

            <h1 class="documentFirstHeading">Talks Top 5</h1>
            <section id="content-core">
                <ul>
                    <li tal:repeat="talk elements/talks">
                        <a tal:attributes="href talk/url"
                            tal:content="element/title">the talk</a>
                        (<span tal:content="element/total">10</span>)
                    </li>
                </ul>
            </section>

Create custom content-rules
---------------------------

Plone content rules allows to trigger a given action depending on an event (content modified, content created, etc.) and a list of criteria (only for such content types, only in this folder, etc.).

Plone provides a set of useful ready-to-use content rule actions, like moving a content somewhere, notifying an email address, executing a workflow change, etc.

Rapido allows to implement our own actions easily.

Rapido just declares a generic "Rapido action" to the Plone content rules system. It allows to enter the following parameters:

- the app id,
- the block id,
- the function name.

The ``content`` property in the function's ``context`` allows to access the content rule targeted content.

For instance, to turn the content title in uppercase everytime we modified a content, we would use a function like this:

.. code-block:: python

    def upper(context):
        context.content.title = context.content.title.upper()

Exercise 7: Reset the votes on workflow change
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We would like to reset the votes when we change the workflow status of a talk.

We will need to:

- create a new block to handle our ``reset`` function,
- add a content rule to our Plone site,
- assign the rule to the proper location.

..  admonition:: Solution
    :class: toggle

    - we create ``contentrule.py``:

      .. code-block:: python

        def reset(context):
            talk_path = context.content.absolute_url_path()
            record = context.app.get_record(talk_path)
            if record:
                record['total'] = 0

    - we go to Site setup / Content rules, we add a rule with event "State has changed",
    - we add a condition on the content type to only target Talks,
    - we add a Rapido action where application will be ``rating``, block will be ``contentrule`` and method will be ``reset``,
    - we activate the rule for the whole site. 

Other topics
------------

The following Rapido features haven't been covered by this training:

- use Rapido blocks as tiles in Mosaic,
- use blocks as form to create, display and edit records directly,
- access control,
- Rapido JSON REST API.

You can find information about those features and also interesting use cases in the `Rapido documentation <http://rapidoplone.readthedocs.io/en/latest/>`_.
