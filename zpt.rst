.. _zpt-label:

Page Templates
==============

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/03_zpt_p5/ src/ploneconf.site


In this part you will:

* Learn to write page templates


Topics covered:

* TAL and TALES
* METAL
* Chameleon


Page Templates are HTML files with some additional information, written in TAL, METAL and TALES.

Page templates must be valid xml.

The three languages are:

* TAL: "Template Attribute Language"

  * Templating XML/HTML using special attributes

  * Using TAL we include expressions within html

* TALES: "TAL Expression Syntax"

  * defines the syntax and semantics of these expressions

* METAL: "Macro Expansion for TAL"

  * this enables us to combine, re-use and nest templates together

TAL and METAL are written like html attributes (href, src, title). TALES are written like the values of html attributes. A typical TAL attribute looks like this:

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

Let's try it. Open the file ``training.pt`` and add:

.. code-block:: html

    <html>
    <body>

        <p>red</p>

    </body>
    </html>


.. _zpt-tal-label:

TAL and TALES
-------------

Let's add some magic and modify the <p>-tag:

.. code-block:: html

    <p tal:content="string:blue">red</p>

This will result in:

.. code-block:: html

    <p>blue</p>

Without restarting Plone open http://localhost:8080/Plone/@@training.

The same happens with attributes. Replace the <p>-line with:

.. code-block:: html

    <a href="http://www.mssharepointconference.com"
       tal:define="a_fine_url string:http://www.ploneconf.org"
       tal:attributes="href a_fine_url"
       tal:content="string:An even better conference">
        A sharepoint conference
    </a>

results in:

.. code-block:: html

    <a href="http://www.ploneconf.org">
        An even better conference
    </a>

We used three TAL-Attributes here. This is the complete list of TAL-attributes:

``tal:define``
    define variables. We defined the variable ``a_fine_url`` to the string "http://www.ploneconf.org"

``tal:content``
    replace the content of an element. We replaced the default content above with "An even better conference"

``tal:attributes``
    dynamically change element attributes. We set the html attribute ``href`` to the value of the variable ``a_fine_url``

``tal:condition``
    tests whether the expression is true or false, and outputs or omits the element accordingly.

``tal:repeat``
    repeats an iterable element, in our case the list of talks.

``tal:replace``
    replace the content of an element, like ``tal:content`` does, but removes the element only leaving the content.

``tal:omit-tag``
    remove an element, leaving the content of the element.

``tal:on-error``
    handle errors.


python expressions
++++++++++++++++++

So far we only used one TALES expression (the ``string:`` bit). Let's use a different TALES expression now. With ``python:`` we can use python code. A simple example:

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

With python expressions

* you can only write single statements
* you could import things but you should not (example: ``tal:define="something modules/Products.PythonScripts/something;``).


tal:condition
+++++++++++++

``tal:condition``
    tests whether the expression is true or false.

* If it's true, then the tag is rendered.
* If it's false then the tag **and all its children** are removed and no longer evaluated.
* We can reverse the logic by prepending a ``not:`` to the expression.

Let's add another TAL Attribute to our above example::

    tal:condition="talks"

We could also test for the number of talks::

    tal:condition="python:len(talks) >= 1"

or if a certain talk is in the list of talks::

    tal:condition="python:'Deco is the future' in talks"


tal:repeat
++++++++++

Let's try another attribute:

.. code-block:: html

    <p tal:define="talks python:['Dexterity for the win!',
                                 'Deco is the future',
                                 'A keynote on some weird topic',
                                 'The talk that I did not submit']"
       tal:repeat="talk talks"
       tal:content="talk">
       A talk
    </p>

``tal:repeat``
    repeats an iterable element, in our case the list of talks.

We change the markup a little to construct a list in which there is an ``<li>`` for every talk:

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


path expressions
++++++++++++++++

Regarding TALES so far we used ``string:`` or ``python:`` or only variables. The next and most common expression are path expressions. Optionally you can start a path expression with ``path:``

Every path expression starts with a variable name. It can either be an object like ``context``, ``view`` or ``template`` or a variable defined earlier like ``talk``.

After the variable we add a slash ``/`` and the name of a sub-object, attribute or callable. The '/' is used to end the name of an object and the start of the property name. Properties themselves may be objects that in turn have properties.

.. code-block:: html

    <p tal:content="context/title"></p>

We can chain several of those to get to the information we want.

.. code-block:: html

    <p tal:content="context/REQUEST/form"></p>

This would return the value of the form dictionary of the HTTPRequest object. Useful for form handling.

The ``|`` ("or") character is used to find an alternative value to a path if the first path evaluates to ``nothing`` or does not exist.

.. code-block:: html

    <p tal:content="context/title | context/id"></p>

This returns the id of the context if it has no title.

.. code-block:: html

      <p tal:replace="talk/average_rating | nothing"></p>

This returns nothing if there is no 'average_rating' for a talk. What will not work is ``tal:content="python:talk['average_rating'] or ''"``. Who knows what this would yield?

.. only:: not presentation

    We'll get ``KeyError: 'average_rating'``. It is very bad practice to use ``|`` too often since it will swallow errors like a typo in ``tal:content="talk/averange_ratting | nothing"`` and you might wonder why there are no ratings later on...

    You can't and should not use it to prevent errors like a try/except block.

There are several **built-in variables**  that can be used in paths:

The most frequently used one is ``nothing`` which is the equivalent to None

..  code-block:: html

    <p tal:replace="nothing">
        this comment will not be rendered
    </p>

A dict of all the available variables is ``econtext``

..  code-block:: html

    <dl tal:define="path_variables_dict econtext">
      <tal:vars tal:repeat="variable path_variables_dict">
        <dt>${variable}</dt>
        <dd>${python:path_variables_dict[variable]}</dd>
      </tal:vars>
    </dl>

..  note::

    In Plone 4 that used to be ``CONTEXTS``

    ..  code-block:: html

        <dl tal:define="path_variables_dict CONTEXTS">
          <tal:vars tal:repeat="variable path_variables_dict">
            <dt tal:content="variable"></dt>
            <dd tal:content="python:path_variables_dict[variable]"></dd>
          </tal:vars>
        </dl>

Useful for debugging :-)


Pure TAL blocks
+++++++++++++++

We can use TAL attributes without HTML Tags. This is useful when we don't need to add any tags to the markup

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

    <tal:news condition="python:context.portal_type == 'News Item'">
        This text is only visible if the context is a News Item
    </tal:news>


handling complex data in templates
++++++++++++++++++++++++++++++++++

Let's move on to a little more complex data. And to another TAL attribute:

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

``tal:replace`` drops its own base tag in favor of the result of the TALES expression. Thus the original ``<img... >`` is replaced. But the result is escaped by default.

To prevent escaping we use ``structure``

.. code-block:: html

    <p>
        <img tal:define="tag string:<img src='https://plone.org/logo.png'>"
             tal:replace="structure tag">
    </p>

Now let's emulate a typical Plone structure by creating a dictionary.

.. code-block:: html
  :linenos:

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

We emulate a list of talks and display information about them in a table. We'll get back to the list of talks later when we use the real talk objects that we created with dexterity.

To complete the list here are the TAL attributes we have not yet used:

``tal:omit-tag``
    Omit the element tag, leaving only the inner content.

``tal:on-error``
    handle errors.

When an element has multiple TAL attributes, they are executed in this order:

1. define
2. condition
3. repeat
4. content or replace
5. attributes
6. omit-tag


Plone 5
-------

Plone 5 uses a new rendering engine called `Chameleon <https://chameleon.readthedocs.org/en/latest/>`_. Using the integration layer `five.pt <https://pypi.python.org/pypi/five.pt>`_ it is fully compatible with the normal TAL syntax but offers some additional features:

You can use ``${...}`` as short-hand for text insertion in pure html effectively making ``tal:content`` and ``tal:attributes`` obsolete. Here are some examples:

Plone 4 and Plone 5:

..  code-block:: html
    :linenos:

    <a tal:attributes="href string:${context/absolute_url}?ajax_load=1;
                       class python:context.portal_type.lower().replace(' ', '')"
       tal:content="context/title">
       The Title of the current object
    </a>

Plone 5 (and Plone 4 with five.pt) :

..  code-block:: html
    :linenos:

    <a href="${context/absolute_url}?ajax_load=1"
       class="${python:context.portal_type.lower().replace(' ', '')}">
       ${python:context.title}
    </a>

You can also add pure python into the templates:

..  code-block:: html
    :linenos:

    <div>
      <?python
      someoptions = dict(
          id=context.id,
          title=context.title)
      ?>
      This object has the id "${python:someoptions['id']}"" and the title "${python:someoptions['title']}".
    </div>


.. _zpt-metal-label:


Exercise 1
----------

Modify the following template and one by one solve the following problems:
:

..  code-block:: html

    <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                      'subjects': ('content-types', 'dexterity')},
                                     {'title': 'Mosaic will be the next big thing.',
                                      'subjects': ('layout', 'deco', 'views'),
                                      'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                     {'title': 'The State of Plone',
                                      'subjects': ('keynote',) },
                                     {'title': 'Diazo is a powerful tool for theming!',
                                      'subjects': ('design', 'diazo', 'xslt')},
                                     {'title': 'Magic templates in Plone 5',
                                      'subjects': ('templates', 'TAL'),
                                      'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
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

1. Display the subjects as comma-separated.

..  admonition:: Solution
    :class: toggle

    ..  code-block:: html
        :linenos:
        :emphasize-lines: 21

        <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                          'subjects': ('content-types', 'dexterity')},
                                         {'title': 'Mosaic will be the next big thing.',
                                          'subjects': ('layout', 'deco', 'views'),
                                          'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                         {'title': 'The State of Plone',
                                          'subjects': ('keynote',) },
                                         {'title': 'Diazo is a powerful tool for theming!',
                                          'subjects': ('design', 'diazo', 'xslt')},
                                         {'title': 'Magic templates in Plone 5',
                                          'subjects': ('templates', 'TAL'),
                                          'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                        ]">
            <tr>
                <th>Title</th>
                <th>Topics</th>
            </tr>
            <tr tal:repeat="talk talks">
                <td tal:content="talk/title">A talk</td>
                <td tal:define="subjects talk/subjects">
                    <span tal:replace="python:', '.join(subjects)">
                    </span>
                </td>
            </tr>
        </table>


2. Turn the title in a link to the url of the talk if there is one.

..  admonition:: Solution
    :class: toggle

    ..  code-block:: html
        :linenos:
        :emphasize-lines: 20

        <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                          'subjects': ('content-types', 'dexterity')},
                                         {'title': 'Mosaic will be the next big thing.',
                                          'subjects': ('layout', 'deco', 'views'),
                                          'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                         {'title': 'The State of Plone',
                                          'subjects': ('keynote',) },
                                         {'title': 'Diazo is a powerful tool for theming!',
                                          'subjects': ('design', 'diazo', 'xslt')},
                                         {'title': 'Magic templates in Plone 5',
                                          'subjects': ('templates', 'TAL'),
                                          'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                        ]">
            <tr>
                <th>Title</th>
                <th>Topics</th>
            </tr>
            <tr tal:repeat="talk talks">
                <td>
                    <a tal:attributes="href talk/url | nothing"
                       tal:content="talk/title">
                       A talk
                    </a>
                </td>
                <td tal:define="subjects talk/subjects">
                    <span tal:replace="python:', '.join(subjects)">
                    </span>
                </td>
            </tr>
        </table>

3. If there is no url turn it into a link to a google search for that talk's title

..  admonition:: Solution
    :class: toggle

    ..  code-block:: html
        :linenos:
        :emphasize-lines: 20, 21

        <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                          'subjects': ('content-types', 'dexterity')},
                                         {'title': 'Mosaic will be the next big thing.',
                                          'subjects': ('layout', 'deco', 'views'),
                                          'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                         {'title': 'The State of Plone',
                                          'subjects': ('keynote',) },
                                         {'title': 'Diazo is a powerful tool for theming!',
                                          'subjects': ('design', 'diazo', 'xslt')},
                                         {'title': 'Magic templates in Plone 5',
                                          'subjects': ('templates', 'TAL'),
                                          'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                        ]">
            <tr>
                <th>Title</th>
                <th>Topics</th>
            </tr>
            <tr tal:repeat="talk talks">
                <td>
                    <a tal:define="google_url string:https://www.google.com/search?q=${talk/title}"
                       tal:attributes="href talk/url | google_url"
                       tal:content="talk/title">
                       A talk
                    </a>
                </td>
                <td tal:define="subjects talk/subjects">
                    <span tal:replace="python:', '.join(subjects)">
                    </span>
                </td>
            </tr>
        </table>

4. Add alternating the css classes 'odd' and 'even' to the <tr>. (``repeat.<name of item in loop>.odd`` is True if the ordinal index of the current iteration is an odd number)

   Use some css to prove your solution:

   .. code-block:: css

      <style type="text/css">
        tr.odd {background-color: #ddd;}
      </style>

..  admonition:: Solution
    :class: toggle

    ..  code-block:: html
        :linenos:
        :emphasize-lines: 19

        <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                          'subjects': ('content-types', 'dexterity')},
                                         {'title': 'Mosaic will be the next big thing.',
                                          'subjects': ('layout', 'deco', 'views'),
                                          'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                         {'title': 'The State of Plone',
                                          'subjects': ('keynote',) },
                                         {'title': 'Diazo is a powerful tool for theming!',
                                          'subjects': ('design', 'diazo', 'xslt')},
                                         {'title': 'Magic templates in Plone 5',
                                          'subjects': ('templates', 'TAL'),
                                          'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                        ]">
            <tr>
                <th>Title</th>
                <th>Topics</th>
            </tr>
            <tr tal:repeat="talk talks"
                tal:attributes="class python: 'odd' if repeat.talk.odd else 'even'">
                <td>
                    <a tal:define="google_url string:https://www.google.com/search?q=${talk/title};
                                   "
                       tal:attributes="href talk/url | google_url;
                                       "
                       tal:content="talk/title">
                       A talk
                    </a>
                </td>
                <td tal:define="subjects talk/subjects">
                    <span tal:replace="python:', '.join(subjects)">
                    </span>
                </td>
            </tr>
        </table>

5. Only use python expressions.

..  admonition:: Solution
    :class: toggle

    ..  code-block:: html
        :linenos:

        <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                          'subjects': ('content-types', 'dexterity')},
                                         {'title': 'Mosaic will be the next big thing.',
                                          'subjects': ('layout', 'deco', 'views'),
                                          'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                         {'title': 'The State of Plone',
                                          'subjects': ('keynote',) },
                                         {'title': 'Diazo is a powerful tool for theming!',
                                          'subjects': ('design', 'diazo', 'xslt')},
                                         {'title': 'Magic templates in Plone 5',
                                          'subjects': ('templates', 'TAL'),
                                          'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                        ]">
            <tr>
                <th>Title</th>
                <th>Topics</th>
            </tr>
            <tr tal:repeat="talk python:talks"
                tal:attributes="class python: 'odd' if repeat.talk.odd else 'even'">
                <td>
                    <a tal:attributes="href python:talk.get('url', 'https://www.google.com/search?q=%s' % talk['title'])"
                       tal:content="python:talk['title']">
                       A talk
                    </a>
                </td>
                <td tal:content="python:', '.join(talk['subjects'])">
                </td>
            </tr>
        </table>

6. Use the new syntax of Plone 5

..  admonition:: Solution
    :class: toggle

    ..  code-block:: html
        :linenos:
        :emphasize-lines: 20, 24, 28

        <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                          'subjects': ('content-types', 'dexterity')},
                                         {'title': 'Mosaic will be the next big thing.',
                                          'subjects': ('layout', 'deco', 'views'),
                                          'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                         {'title': 'The State of Plone',
                                          'subjects': ('keynote',) },
                                         {'title': 'Diazo is a powerful tool for theming!',
                                          'subjects': ('design', 'diazo', 'xslt')},
                                         {'title': 'Magic templates in Plone 5',
                                          'subjects': ('templates', 'TAL'),
                                          'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                        ]">
            <tr>
                <th>Title</th>
                <th>Topics</th>
            </tr>

            <tr tal:repeat="talk python:talks"
                class="${python: 'odd' if repeat.talk.odd else 'even'}">
                <td>
                    <a href="${python:talk.get('url', 'https://www.google.com/search?q=%s' % talk['title'])}">
                        ${talk_title}
                    </a>
                </td>
                <td>
                    ${python:', '.join(talk['subjects'])}
                </td>
            </tr>
        </table>

7. Sort the talks alphabetically by title

..  admonition:: Solution
    :class: toggle

    ..  code-block:: html
        :linenos:
        :emphasize-lines: 19, 21

        <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                          'subjects': ('content-types', 'dexterity')},
                                         {'title': 'Mosaic will be the next big thing.',
                                          'subjects': ('layout', 'deco', 'views'),
                                          'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                         {'title': 'The State of Plone',
                                          'subjects': ('keynote',) },
                                         {'title': 'Diazo is a powerful tool for theming!',
                                          'subjects': ('design', 'diazo', 'xslt')},
                                         {'title': 'Magic templates in Plone 5',
                                          'subjects': ('templates', 'TAL'),
                                          'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                        ]">
            <tr>
                <th>Title</th>
                <th>Topics</th>
            </tr>

        <?python from operator import itemgetter ?>

            <tr tal:repeat="talk python:sorted(talks, key=itemgetter('title'))"
                class="${python: 'odd' if repeat.talk.odd else 'even'}">
                <td>
                    <a href="${python:talk.get('url', 'https://www.google.com/search?q=%s' % talk['title'])}">
                        ${talk_title}
                    </a>
                </td>
                <td>
                    ${python:', '.join(talk['subjects'])}
                </td>
            </tr>
        </table>


METAL and macros
----------------

Why is our output so ugly? How do we get our html to render in Plone the UI?

We use METAL (Macro Extension to TAL) to define slots that we can fill and macros that we can reuse.

We add to the ``<html>`` tag::

    metal:use-macro="context/main_template/macros/master"

And then wrap the code we want to put in the content area of Plone in:

.. code-block:: xml

    <metal:content-core fill-slot="content-core">
        ...
    </metal:content-core>

This will put our code in a section defined in the main_template called "content-core".

The template should now look like this:

.. code-block:: xml
  :linenos:

  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
        lang="en"
        metal:use-macro="context/main_template/macros/master"
        i18n:domain="ploneconf.site">
  <body>

  <metal:content-core fill-slot="content-core">

  <table tal:define="talks python:[{'title':'Dexterity for the win!',
                                    'subjects':('content-types', 'dexterity')},
                                   {'title':'Deco is the future',
                                    'subjects':('layout', 'deco')},
                                   {'title':'The State of Plone',
                                    'subjects':('keynote',) },
                                   {'title':'Diazo designs are great',
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

  </metal:content-core>

  </body>
  </html>

.. note::

    Since the training only used content from the template, not from the context that it is called on it makes little sense to have the edit bar. We hide it by setting the respective variable on the current request with python to 1: ``request.set('disable_border', 1)``.

    The easiest way to do this is to define a dummy variable. Dummy because it is never used except to allow us to execute some code.

    .. code-block:: xml

        <metal:block fill-slot="top_slot"
            tal:define="dummy python:request.set('disable_border', 1)" />


macros in browser views
+++++++++++++++++++++++

Define a macro in a new file ``macros.pt``

.. code-block:: html

    <div metal:define-macro="my_macro">
        <p>I can be reused</p>
    </div>

Register it as a simple BrowserView in zcml:

.. code-block:: xml

    <browser:page
      for="*"
      name="abunchofmacros"
      template="templates/macros.pt"
      permission="zope2.View"
      />

Reuse the macro in the template ``training.pt``:

.. code-block:: html

        <div metal:use-macro="context/@@abunchofmacros/my_macro">
            Instead of this the content of the macro will appear...
        </div>

Which is the same as:

.. code-block:: html

        <div metal:use-macro="python:context.restrictedTraverse('abunchofmacros')['my_macro']">
            Instead of this the content of the macro will appear...
        </div>

Restart your Plone instance from the command line, and then open http://localhost:8080/Plone/@@training to see this macro being used in our @@training browser view template.

.. _tal-access-plone-label:

Accessing Plone from the template
---------------------------------

In our template we have access to the context object on which the view is called on, the browser view itself (i.e. all python methods we'll put in the view later on), the request and response objects and with these we can get almost anything.

In templates we can also access other browser views. Some of those exist to provide easy access to methods we often need::

    tal:define="context_state context/@@plone_context_state;
                portal_state context/@@plone_portal_state;
                plone_tools context/@@plone_tools;
                plone_view context/@@plone;"

``@@plone_context_state``
    The BrowserView ``plone.app.layout.globals.context.ContextState`` holds useful methods having to do with the current context object such as ``is_default_page``

``@@plone_portal_state``
    The BrowserView ``plone.app.layout.globals.portal.PortalState`` holds methods for the portal like ``portal_url``

``@@plone_tools``
    The BrowserView ``plone.app.layout.globals.tools.Tools`` gives access to the most important tools like ``plone_tools/catalog``

These are very widely used and there are many more.


.. _tal-missing-label:

What we missed
--------------

There are some things we did not cover so far:

``tal:condition="exists:expression"``
    checks if an object or an attribute exists (seldom used)

``tal:condition="nocall:context"``
    to explicitly not call a callable.

If we refer to content objects, without using the nocall: modifier these objects are unnecessarily rendered in memory as the expression is evaluated.

``i18n:translate`` and ``i18n:domain``
    the strings we put in templates can be translated automatically.

There is a lot more about TAL, TALES and METAL that we have not covered. You'll only learn it if you keep reading, writing and customizing templates.

.. seealso::

  * http://docs.plone.org/adapt-and-extend/theming/templates_css/template_basics.html
  * Using Zope Page Templates: http://docs.zope.org/zope2/zope2book/ZPT.html
  * Zope Page Templates Reference: http://docs.zope.org/zope2/zope2book/AppendixC.html

.. _tal-chameleon-label:

Chameleon
---------

Chameleon is the successor of Zope Page Templates, it is used in Plone 5.

- Plip for Chameleon: https://dev.plone.org/ticket/12198
- Homepage: https://chameleon.readthedocs.org/en/latest/



