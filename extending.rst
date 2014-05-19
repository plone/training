Extending Plone
===============

Zope is extensible and so is Plone.

If you want to install an Add-on, you are going to install an Egg. Eggs consist of python files together with other needed files like page templates and the like and a bit of Metadata, bundled to a single archive file.

Eggs are younger than Zope. Zope needed something like eggs before there were eggs, and the Zope developers wrote their own system. Old, outdated Plone systems contain a lot of code that is not bundled in an egg. Older code did not have metadata to register things, instead you needed a special setup method. We don't need this method but you might see it in other code. It is usually used to register Archetypes code. Archetypes is the old content type system. We use Dexterity.


Extension technologies
----------------------

How do you extend Plone? This depends on what type of extension you want to create.

* You can create extensions with new types of objects to add to your Plone site. Usually these are content types.
* You can create an extension that changes or extends functionality. For example to change the way Plone displays search results, or to make pictures searchable by adding a converter from jpg to text.


skin_folders
^^^^^^^^^^^^

Do you remember Acquisition? The Skin Folders we used to put in our css-code extend the concepts of Acquistion. Your Plone site has a folder named ``portal_skins``. This folder has a number of sub folders. The ``portal_skins`` folder has a property that defines in which order Plone searches for attributes or objects in each sub folder.

The Plone logo is in a skin folder.

By default, your site has a custom folder, and items are first searched for in that folder.

To customize the logo, you copy it into the custom folder, and change it there. This way you can change templates, CSS styles, images and behavior, because a container may contain python scripts.


GenericSetup
^^^^^^^^^^^^

The next thing is *GenericSetup*. As the name clearly implies, *GenericSetup* is part of CMF.

GenericSetup is tough to master, I am afraid.

*GenericSetup* lets you define persistent configuration in XML files. *GenericSetup* parses the XML files and updates the persistent configuration according to the configuration. This is a step you have to run on your own!

You will see many objects in Zope or the ZMI that you can customize through the web. If they are well behaving, they can export their configuration via *GenericSetup* and import it again.

Typically you use *GenericSetup* to change workflows or add new content type definitions.


Components
^^^^^^^^^^

The last way to extend Plone is via *Components*.

A bit of history is in order.

When Zope started, object-oriented Design was **the** silver bullet.

Zope objects have more than 10 base classes.

After a while, XML and Components became the next silver bullet (Does anybody remember J2EE?).

Based on their experiences with Zope in the past, they thought that a component system configured via xml might be the way to go to keep the code more maintainable

As the new concepts were radically different from the old Zope concepts, the Zope developers renamed the new project to Zope 3. But it did not gain traction, the community somehow renamed it to Bluebream and this died off.

But the component architecture itself is quite successful and the Zope developer extracted it into the Zope Toolkit. The Zope toolkit is part of Zope, and Plone developers use it extensively.


This is what you want to use.


What are components, what is ZCML
---------------------------------

What is the absolute simplest way to extend functionality?

Monkey Patching.

It means that I change code in other files while my file gets loaded.

If I would want to have an extensible registry of icons for different content types, I could create a global dictionary, and whoever implements a new icon for a different content type, would add an entry to my dictionary during import time.

This does not scale. Multiple plugins might overwrite each other, you would explain people that they have to reorder the imports, and then, suddenly, you will to import feature A before B, B before C and C before A, or else you application won't work.

The Zope Component Architecture with its ZCML configuration is the answer for your problems.

With ZCML you declare utilities, adapters and browser views in ZCML, which is a XML dialect.

During startup, Zope reads all these ZCML statements, validates that there are not two declarations trying to register the same components and only then registers everything.

This is a good thing. ZCML is by the way only *one* way to declare your configuration.

Grok pvides another way, where some python magic allows you to decorate your code directly with a decorator to make it an adapter. You can use both ZCML and grok together.

Please be aware that not everybody loves Grok. Some parts of the Plone community think that there may only be one configuration language, others are against adding the relative big dependency of Grok to Plone. One real problem is the fact that you cannot customize components declared with grok with jbot. In any case, if you start to write an extension that is reusable, convert your grok declarations to ZCML to get maximum acceptance.

Many people hate ZCML and avoid Zope because of it using XML.

Personally, I just find it cumbersome but even for me as a developer it offers a nice advantage.

Thanks to ZCML, I hardly ever have a hard time to find out what and where extensions or customizations. For me, ZCML files are like a phone book.

