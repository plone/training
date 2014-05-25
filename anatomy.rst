The Anatomy of Plone
====================

Python, Zope, CMF, Plone, how does that all fit together?


Zope2
-----

* Zope is a web application framework that Plone runs on top of.
* It serves applications that communicate with users via http.

.. only:: manual

    Before Zope, there usually was an Apache server that would call a script and give the request as an input. The script would then just print HTML to the standard output. Apache returned that to the user. Opening database connections, checking permission constraints, generating valid HTML, configuring caching, interpreting form data and everything you have to do on your own. When the second request comes in, you have to do everything again.

    Jim Fulton thought that this was slightly tedious. So he wrote code to handle requests. He believed that site content is object-oriented and that the URL should somehow point directly into the object hierarchy, so he wrote an object-oriented database, called `ZODB <http://www.zodb.org/en/latest/>`_.

    Then there were transactions, so that it became a real database and after a while there were python scripts that could be edited through the web.
    One missing piece is important and complicated: ``Acquisition``.

    Acquisition is a kind of magic. Imagine a programming system where you do not access the file system and where you do not need to import code. You work with objects. An object can be a folder that contains more objects, an HTML page, data, or another script. To access an object, you need to know where the object is. Objects are found by paths that look like URLs, but without the domain name. Now Acquisition allows you to write an incomplete path. An incomplete path is a relative path, it does not explicitly state that the path starts from the root, it starts relative to where the code object is. If Zope cannot resolve the path to an object relative to your code, I tries the same path in the containing folder. And then the folder containing the folder.

    This might sound weird, what do I gain with this?

    You can have different data or code depending on your ``context``. Imagine you want to have header images differing for each section of your page, sometimes even differing for a specific subsection of your site. So you define a path header_image and put a header image at the root of your site. If you want a folder to with a different header image, you put the header image into this folder.
    Please take a minute to let this settle and think, what this allows you to do.

    - contact forms with different e-mail addresses per section
    - different CSS styles for different parts of your site
    - One site, multiple customers, everything looks different for each customer.

    Basically this is Zope.

    .. seealso::

        http://www.zope.org/the-world-of-zope
        http://docs.zope.org/zope2/zope2book/


Content Management Framework
----------------------------

* `CMF (Content Management Framework) <http://old.zope.org/Products/CMF/index.html/>`_ is add-on for Zope to build Content Management Systems (like Plone).


.. only:: manual

    After many successfully created websites based on Zope, a number of recurring requirements emerged, and some Zope developers started to write CMF, the Content Management Framework.

    The CMF offers many services that help you to write a CMS based on Zope.
    Most objects you see in the ZMI are part of the CMF somehow.

    The developers behind CMF do not see CMF as a ready to use CMS. They created a CMS Site which was usable out of the box, but made it deliberately ugly, because you have to customize it anyway.

    We are still in prehistoric times here. There were no eggs, Zope did not consist of 100 independent software components but was one big blob.

    Later we will see a lot of GenericSetup. This is also part of CMF. When we will talk about GenericSetup, we might not speak too fondly of it.

    GenericSetup is like it is, because it is from the stone age and didn't adapt very well. This helps in understanding why GenericSetup is what it is.


Zope Toolkit / Zope3
--------------------

* Zope 3 was originally intended as a ground-up rewrite of Zope.
* Plone uses parts of it provided by the `Zope Toolkit (ZTK) <http://docs.zope.org/zopetoolkit/>`_.

.. only:: manual

    Unfortunately, nobody started to use Zope 3, nobody migrated to Zope 3 because nobody knew how.

    But there were many useful things in Zope 3 that people wanted to use in Zope 2, thus the Zope community adapted some parts so that they could use them in Zope 2.
    Sometimes, a wrapper of some sorts was necessary, these usually are being provided by packages from the five namespace.

    To make the history complete, since people stayed on Zope 2, the Zope community renamed Zope 3 to Bluebream, so that people would not think that Zope 3 was the future. It wasn't any more.

    .. seealso::

        http://plone.org/documentation/faq/zope-3-and-plone


Zope Component Architecture (ZCA)
---------------------------------

The `Zope Component Architecture <http://muthukadan.net/docs/zca.html>`_ is a system which allows for application pluggability and complex dispatching based on objects which implement an interface. Pyramid uses the ZCA “under the hood” to perform view dispatching and other application configuration tasks.


Pyramid
-------

* `Pyramid <http://docs.pylonsproject.org/en/latest/docs/pyramid.html>`_ is a Python web application development framework that is often seen as the successor to Zope.
* It does less than Zope, is very pluggable and `uses the Zope Component Architecture <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/zca.html>`_.

.. only:: manual

    You can use it with a relational Database instead of ZODB if you want, or you use both databases or none of them.

    Apart from the fact that Pyramid was not forced to support all legacy functionality that can make things more complicated, the original developer had a very different stance on how software must be developed. While both Zope and Pyramid have a good test coverage, Pyramid also has good documentation, something that was very neglected in Zope and at times in Plone too.

    Wether the component architecture is better in Pyramid or not we don't dare to say, but we like it more. But maybe its just because it has documented.
