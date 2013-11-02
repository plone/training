The Anatomy of Plone
====================

Zope, Plone, GenericSetup, CMF, Acquisition, what is all that actually?

.. only:: manual

    Zope is an application server. It serves applications that communicate with users via http.

    Before Zope, there usually was an Apache server that would call a script and give the request as an input. The script would then just print HTML to the standard output. Apache returned that to the user. Opening database connections, checking permission constraints, generating valid HTML, configuring caching, interpreting form data and everything you have to do on your own. When the second request comes in, you have to do everything again.

    Jim Fulton thought that this was slightly tedious. So he wrote code to handle requests. He believed that site content is object oriented and that the URL should somehow point directly into the object hierarchy, so he wrote an object oriented database, called ZODB.

    Then there were transactions, so that it became a real database and after a while there were python scripts that could be edited through the web.
    One missing piece is important and complicated: ``Acquisition``.

    Acquisition is a kind of magic. Imagine a programming system where you do not access the file system and where you do not need to import code. You work with objects. An object can be a folder that contains more objects, a HTML page, data, or another script. To access an object, you need to know where the object is. Objects are found by paths that look like URLs, but without the domain name. Now Acquisition allows you to write an incomplete path. An incomplete path is a relative path, it does not explicitly state that the path starts from the root, it starts relative to where the code object is. If Zope cannot resolve the path to an object relative to your code, I tries the same path in the containing folder. And then the folder containing the folder.

    This might sound weird, what do I gain with this?

    You can have different data or code depending on your ``context``. Imagine you want to have header images differing for each section of your page, sometimes even differing for a specific subsection of your site. So you define a path header_image and put a header image at the root of your site. If you want a folder to have a different header image, you put the header image into this folder.
    Please take a minute to let this settle and think, what this allows you to do.

    - contact forms with different e-mail adresses per section
    - different CSS styles for different parts of your site
    - One site, multiple customers, everything looks different for each customer.

    Basically this is Zope.

    After many successfully created websites based on Zope, a number of recurring requirements emerged, and some Zope developers started to write CMF, the Content Management Framework.
    The CMF offers many services that help you to write a CMS based on Zope.
    Most objects you see in the ZMI are part of the CMF somehow.
    The developers behind CMF do not see CMF as a ready to use CMS. They created a CMS Site which was usable out of the box, but made it deliberately ugly, because you have to customize it anyway.

    This is one way to do it. The Plone founders Alexander Limi and Alan Runyan thought differently, and created a CMS that was usable and beautiful out of the box, based on CMF. They named it Plone.

    Here are two numbers, without further comment:

    Last German Zope conference (2010): 80 visitors (There is no international Zope conference)

    First German Plone conference (2012): 150 visitors

    The Plone and Zope community are very similar. Even though in the past, a lot of Zope developers who did not use Plone envied Plone for its success and tried to marginalize the Plone success with bad mouthing. If you meet a Zope developer making bad remarks about Plone, be kind to him. It is hard to accept that your superior, cleaner system is not used by anybody, because Plone is user friendly and beautiful.

    Because there is such a big overlap of the communities, it can sometimes be confusing, where some functionality is coming from.

    - CMFEditions: Written by Plone developers
    - GenericSetup: Written by CMF developers

    Summarizing all this in a single sentence:

        We run Zope the application server. Our main application is Plone.

