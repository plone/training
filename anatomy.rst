The Anatomy of Plone
====================

Python, Zope, CMF, Plone, how does that all fit together?


Zope2
-----

.. only:: manual

    Zope is an application server. It serves applications that communicate with users via http.

    Before Zope, there usually was an Apache server that would call a script and give the request as an input. The script would then just print HTML to the standard output. Apache returned that to the user. Opening database connections, checking permission constraints, generating valid HTML, configuring caching, interpreting form data and everything you have to do on your own. When the second request comes in, you have to do everything again.

    Jim Fulton thought that this was slightly tedious. So he wrote code to handle requests. He believed that site content is object-oriented and that the URL should somehow point directly into the object hierarchy, so he wrote an object-oriented database, called ZODB.

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



Content Management Framework
----------------------------

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

.. only:: manual

    The Zope Toolkit, or ZTK as everybody calls it,is a new framework written by the same people who wrote Zope.

    It started with a complete rewrite of Zope 2 to Zope 3. Unfortunately, nobody started to use Zope 3, nobody migrated to Zope 3 because nobody knew how.

    But there were many useful things in Zope 3 that people wanted to use in Zope 2, thus the Zope community adapted some parts so that they could use them in Zope 2.
    Sometimes, a wrapper of some sorts was necessary, these usually are being provided by packages from the five namespace.

    To make the history complete, since people stayed on Zope 2, the Zope community renamed Zope 3 to Bluebream, so that people would not think that Zope 3 was the future. It wasn't any more.

Pyramid
-------

.. only:: manual

    Pyramid is a complete rewrite of Zope. It does less than Zope and is very pluggable. You can use it with a relational Database instead of ZODB if you want, or you use both databases or none of them.

    Apart from the fact that Pyramid was not forced to support all legacy functionality that can make things more complicated, the original developer had a very different stance on how software must be developed. While both Zope and Pyramid have a good test coverage, Pyramid also has good documentation, something that was very neglected in Zope and at times in Plone too.

    Wether the component architecture is better in Pyramid or not we don't dare to say, but we like it more. But maybe its just because it has documented.
