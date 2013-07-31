
5. Extending Plone with Addons (80min) (Patrick)
================================================

Zope is extensible and so is Plone.
If you want to to install an Addon, you are going to install an Egg. Eggs consist of python files together with other needed files like page templates and the like and a bit of Metadata, bundled to a single archive file.

Eggs are a much much younger than Zope. Zope needed something like eggs before there were eggs, and the Zope developers wrote their own system. Old, outdated Plone systems contain a lot of code that is not bundled in an egg. Older code did not have metadata to register things, instead you needed a special setup method. We don't need this method but you might see it in other code. It is usually used to register Archetypes code. Archetypes is the old content type system. We use Dexterity.


Extension technologies
----------------------

Ok, how do you extend Plone? This depends on what type of extension you want to create.
You can create extensions with new types of objects to add to your plone site. Usually these are content types. You can create an extention that changes or extends functuionality. For example to change the way search results are displayed, or to make pictures searchable by adding a converter from jpg to text.

skin_folders
^^^^^^^^^^^^
Do you remember acquisition? Skin Folders are an extension of acquistion. Your plone site has a folder named ``portal_skins``. This contains a number of folders. The ``portal_skins`` folder has a property that defines in which order attributes or objects should be looked for in the skin folder.

The plone logo is in a skin folder.
By default, your site has a custom folder, and items are first searched for in that folder.

To customize the logo, you copy it into the custom folder, and modify it there. This way you can modify templates, css styles, images and behavior, because a container may contain python scripts.

GenericSetup
^^^^^^^^^^^^^
The next thing is *GenericSetup*. As the name clearly implies, *GenericSetup* is part of CMF.

It is tough to master, I am afraid.

*GenericSetup* lets you define persistent configuration in xml files. *Genericsetup* parses the xml files and updates the persistent configuration accordingly. This is a step you have to run on your own!

You will see many objects in Zope or the ZMI that you can customize through the web. If they are well behaving, they can export their configuration via *GenericSetup* and import it again.

Typically you use *GenericSetup* to modify workflows or add new content type definitions.

ZCML
^^^^
The last way is via *ZCML*.

A bit of history again.
When Zope started, object oriented Design was **the** silver bullet.
Zope objects have more than 10 base classes.
After a while, XML and Components became the next silver bullet (J2EE anyone).
The Zope developers decided that these new silver bullets look much, much cooler in their colts so they decided rewrite zope with this technology.
It is easier to swap out components than to always subclass.
The whole thing was named Zope 3, did not gain traction, was renamed to Bluebream and died off.

The component architecture itself was quite successfull and was extracted into the Zope Toolkit, which is integrated in Zope and heavily used in Plone.
    This is what you want to use.


What is ZCML
------------
What is the absolute simplest way to extend functionality?
Monkey Patching. In code, during load time I import some code and replace it with my own code.

If I would want to have an extensible registry of icons for different content types, I could create a global dictionary, and whoever implements a new icon for a different content type, would add an entry to my dictionary during import time.

This does not scale. Multiple plugins might overwrite each other, you would explain people that they have reorder the imports, and then, suddenly, you will to import feature A before B, B before C and C before A, else you application won't work.


Here comes the Zope Component Architecture and ZCML to your rescue.
With ZCML you declare your utilities, adapters and browser views in ZCML, which is a XML dialect.
During startup, Zope reads all these ZCML statements, validates that there are not two things trying to register the same things and only then registers everything.

This is a good thing. ZCML is by the way only *one* way to declare your configuration.
Another way is provided by is Grok, where some python magic allows you to decorate your code directly with some magic to make it an adapter. Both implementations can be mixed.
We will mostly use grok in later code examples. The you will see what *magic* actually means.

Many people hate ZCML and avoid Zope because of it being XML.
Personally, I just find it cumbersome but even for me as a developer it offers a nice advantage.
Thanks to zcml, I hardly ever have a hard time to find out what and where extensions or customizations. For me, zcml files are like a phone book.

Installation
------------
Installation is a two step process.
First, we must make our code available to Zope.
This means, it must be importable and that is handled by Buildout.

*ssh* to your vagrant, and modify the buildout.cfg files in training/zinstance.

There is a variable named eggs, which contains multiple *eggs* Add the following eggs:

    * PloneFormGen
    * Products.LinguaPlone
    * Products.PloneTrueGallery
    * collective.plonetruegallery

Usually, one enters the eggs by adding one more line per egg into the configuration.
The egg name must be indented, this way buildout understands that the current line is part of the last variable and not a new variable.

.. sourcecode:: bash

    $ bin/buildout
    $ bin/instance fg


Now the code is importable from within plone and everything got registered via zcml.
But Plone is not configured to use this.
For this, you have to install the extension in your Plone Site.

In your browser, go the plone control panel, and open the Products Panel. You will see that all 4 Products can be installed there.

Install them now.

This is what happens now: The GenericSetup profile of the product gets loaded. This does things like configuring new actions, registering new
content types or creating some content/configuration objects in your plone site.


WIP
VVVxxx

PTG
---
I LOVE PTG.
What does it do?
It is a rolemodel on how to write a Plone Extension.
Instead of creating custom content types for Galleries, it integrates with the plone functionality to choose different views for folderish content types.
Lets try it!...


Introduction (Patrick)
----------------------

 * 1684 Erweiterungen auf http://plone.org/products
 * http://pypi.python.org/
 * Beispiele:

   * collective.plonetruegallery
   * Singing&Dancing


Installing Addons (Patrick)
---------------------------

 * in buildout eintragen (zeigen)
 * /manage -> portal_quickinstaller oder -> plone_control_panel -> "Erweiterungen"


PloneFormGen (Philip)
---------------------

There a various methods to create forms in Plone:

* pure html in a view
* z3c.form, formlib or in Python deform prgrammatically
* PloneFormGen

Mit PFG kann man professionelle Formulare zusammenklicken. Wenn man bedenkt was die Alternatven sind wird klar wie cool PFG ist. Der angeblich komfortablen Formulargenerator in Typo3 ist ja schon schlimm. In Plone könnte man Formulare auch von Hand in html schreiben und in Python auslesen was oft auch eine einfache Methode ist. Wenn es komplexer sein soll dann eben z3c.forms. Aber dazu muss man ja immer programmieren. Wir machen das jetzt mal nicht sondern klicken uns ein Anmeldeformular für die Plone-Konferenz zusammen.

http://konferenz.plone.de/anmeldung

In fact the guys at fourdigts embedd the form in a iframe. Let's pretend otherwise.

* easy form to subscribe a newsletter?
* registration-form (Name, Food, Shirt-size etc.)
* Mail-Adapter
* DataSave Adapter


Internationalisation with LinguaPlone (Philip)
----------------------------------------------

* /plone_control_panel
* install installieren
* add german as language einstellen

   * /@@language-controlpanel -> Deutsch und Englisch auswählen
   * ZMI -> portal_languages -> "Display flags for language selection" aktivieren

* @@language-setup-folders -> Ordnerstruktur anlegen
* Englische Startseite anlegen
* Infos zum übersetzen (folder übersetzen, language_independent)

   http://plone.org/products/linguaplone/issues/250
   http://localhost:8080/Plone/@@language-setup-folders
   Seit Plone4 ist der Standardweg von Übersetzungen, das jede Sprache
   einen eigenen Folder bekommt. Wenn Inhalte übersetzt werden, wird

* die Datei automatisch in den richtigen Ordner kopiert.


Add 'bling' with PloneTrueGallery (10min) (Patrick)
---------------------------------------------------


Customizing the design with plone.app.themeeditor (20min) (Philip)
------------------------------------------------------------------

* Installation
* explain UI
* change Logo (dowmload http://www.ploneconf.org/++theme++ploneconf.theme/images/logo.png)
* change Footer (colophon): add copyright (Phone: +31 26 44 22 700
  mailto:info@ploneconf.org)
* change some css::

    #visual-portal-wrapper {
        margin: 0 auto;
        position: relative;
        width: 980px;
    }


export customisations
---------------------

* export the customisations as an egg (ploneconf.customisations)


inspect the egg
---------------

* what is where?
* jbot, static etc.


Wir können nun das Design unserer Webseite anpassen. Wir können Erweiterungen installieren und einfache Aktionen einrichten. Aber:

* Können wir auf unserer neuen Webseite Talks einreichen?
* Können wir in einer Liste die wichtigsten Eigenschaften jedes Talks anzeigen?
* Können wir Besucher den Talk bewerten lassen?

Wir müssen oft strukturierte Daten speichern oder anzeigen können, bis zu einem gewissen Grad auch noch TTW, aber irgendwann erreichen wir eine Grenze. Wir werden im zweiten Teil zeigen, wie man neue Contenttypen anlegt und wie man neue Funktionalitäten schreibt.


5.1 Theming
===========

* Diazo
* Downloading and activating a theme
* Creating a new theme
* Diazo Theme editor
* Rules
* Old-school Themeing
* Deliverance
