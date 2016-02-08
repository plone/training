.. _extending-label:

Extending Plone
===============

In this part you will:

* Get an overview other the technologies used to extend Plone

Topics covered:

* Skin folders
* GenericSetup
* Component Architecture
* ZCML


Zope is extensible and so is Plone.

.. only:: not presentation

    If you want to install an add-on, you are going to install an Egg — a form of Python package. Eggs consist of Python files together with other needed files like page templates and the like and a bit of Metadata, bundled to a single archive file.

    There is a huge variety of Plone-compatible packages available. Most are listed in the `Python Package Index <https://pypi.python.org/pypi>`_. A more browseable listing is available at the `Plone.org add-on listing <https://plone.org/products/>`_. The source repository for many public Plone add-ons is `the GitHub Collective <https://github.com/collective>`_. You may also create your own packages or maintain custom repositories.

    Eggs are younger than Zope. Zope needed something like eggs before there were eggs, and the Zope developers wrote their own system. Old, outdated Plone systems contain a lot of code that is not bundled in an egg. Older code did not have metadata to register things, instead you needed a special setup method. We don't need this method but you might see it in other code. It is usually used to register Archetypes code. Archetypes is the old content type system. Instead, we use the new content type system Dexterity.


.. _extending-technologies-label:

Extension technologies
----------------------

How do you extend Plone?

This depends on what type of extension you want to create.

.. only:: not presentation


    * You can create extensions with new types of objects to add to your Plone site. Usually these are contenttypes.
    * You can create an extension that changes or extends functionality. For example to change the way Plone displays search results, or to make pictures searchable by adding a converter from jpg to text.


skin_folders
^^^^^^^^^^^^

.. only:: presentation

    * Very old style
    * Very quick
    * Very unmaintainable

.. only:: not presentation

    Do you remember Acquisition? The Skin Folders extends the concepts of Acquisition. Your Plone site has a folder named ``portal_skins``. This folder has a number of sub folders. The ``portal_skins`` folder has a property that defines in which order Plone searches for attributes or objects in each sub folder.

    The Plone logo is in a skin folder.

    By default, your site has a ``custom`` folder, and items are first searched for in that folder.

    To customize the logo, you copy it into the ``custom`` folder, and change it there. This way you can change templates, CSS styles, images and behavior, because a container may contain python scripts.

    Skin-folder style customization may be accomplished TTW via the ZMI, or with add-on packages. Many older-style packages create their own skin folder and add it to the skin layer for Plone when installed.

.. only:: not presentation

    .. warning::

        This is deprecated technology.


GenericSetup
^^^^^^^^^^^^

.. only:: presentation

    * Old style
    * Limited use cases
    * Full of surprises

.. only:: not presentation

    The next thing is *GenericSetup*. As the name clearly implies, *GenericSetup* is part of CMF.

    GenericSetup is tough to master, I am afraid.

    *GenericSetup* lets you define persistent configuration in XML files. *GenericSetup* parses the XML files and updates the persistent configuration according to the configuration. This is a step you have to run on your own!

    You will see many objects in Zope or the ZMI that you can customize through the web. If they are well behaving, they can export their configuration via *GenericSetup* and import it again.

    Typically you use *GenericSetup* to change workflows or add new content type definitions.

    GenericSetup profiles may also be built into Python packages. Every package that is listed on the add-on package list inside a Plone installation has a GS profile that details how it fits into Plone. Packages that are part of Plone itself may have GS profiles, but are excluded from the active/inactive listing.


Component Architecture
^^^^^^^^^^^^^^^^^^^^^^

.. only:: presentation

    * State of the art
    * verbose
    * cryptic
    * Powerful and flexible

.. only:: not presentation

    The last way to extend Plone is via *Components*.

    A bit of history is in order.

    When Zope started, object-oriented Design was **the** silver bullet.

    Object-oriented design is good at modeling inheritance, but breaks down when an object has multiple aspects that are part of multiple taxonomies.

    Some object-oriented programming languages like Python handle this through multiple inheritance. But it's not a good way to do it. Zope objects have more than 10 base classes. Too many namespaces makes code that's hard to maintain. Where did that method/attribute come from?

    After a while, XML and Components became the next silver bullet (Does anybody remember J2EE?).

    Based on their experiences with Zope in the past, Zope developers thought that a component system configured via XML might be the way to go to keep the code more maintainable.

    As the new concepts were radically different from the old Zope concepts, the Zope developers renamed the new project to Zope 3. But it did not gain traction, the community somehow renamed it to Bluebream and this died off.

    But the component architecture itself is quite successful and the Zope developers extracted it into the Zope Toolkit. The Zope toolkit is part of Zope, and Plone developers use it extensively.

    This is what you want to use.


.. _extending-components-label:

What are components, what is ZCML
---------------------------------

.. only:: not presentation

    What is the absolute simplest way to extend functionality?

    Monkey Patching.

    It means that you change code in other files while my file gets loaded.

    If you want to have an extensible registry of icons for different contenttypes, you could create a global dictionary, and whoever implements a new icon for a different content type would add an entry to my dictionary during import time.

    This approach, like subclassing via multiple inheritance, does not scale. Multiple plugins might overwrite each other, you would explain to people that they have to reorder the imports, and then, suddenly, you will be forced to import feature A before B, B before C and C before A, or else your application won't work.

    The Zope Component Architecture with its ZCML configuration is an answer to these problems.

    With ZCML you declare utilities, adapters and browser views in ZCML, which is an XML dialect. ZCML stands for Zope Component Markup Language.

    Components are differentiated from one another by the interfaces (formal definitions of functionality) that they require or provide.

    During startup, Zope reads all these ZCML statements, validates that there are not two declarations trying to register the same components and only then registers everything. All components are registered by interfaces required and provided. Components with the same interfaces may optionally also be named.

    This is a good thing. ZCML is, by the way, only *one* way to declare your configuration.

    Grok provides another way, where some Python magic allows you to use decorators to register Python classes and functions as components. You can use ZCML and Grok together if you wish.

    Some like Grok because it allows you to do nearly everything in your Python source files. No additional XML wiring required. If you're XML-allergic, Grok is your ticket to Python nirvana.

    Not everybody loves Grok. Some parts of the Plone community think that there should only be one configuration language, others are against adding the relative big dependency of Grok to Plone. One real problem is the fact that you cannot customize components declared with grok with jbot (which we'll discuss later). Grok is not allowed in the Plone core for these reasons.

    The choice to Grok or not to Grok is yours to make. In any case, if you start to write an extension that is reusable, convert your grok declarations to ZCML to get maximum acceptance.

    Personally, I just find it cumbersome but even for me as a developer it offers a nice advantage: thanks to ZCML, I hardly ever have a hard time to find what and where extensions or customizations are defined. For me, ZCML files are like a phone book.

