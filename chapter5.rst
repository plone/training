
5. Extending Plone with Addons (80min) (Patrick)
================================================

 * Introduction (10min)
 * Installing Addons (5min) (+ infos on uninstalling)
 * PloneFormGen (15min)
 * Internationalisation with LinguaPlone (20min) (Philip)
 * Add bling with PloneTrueGallery (10min) (Patrick)
 * Customizing the design with plone.app.themeeditor (20min) (Philip)
 * export egg

Zope is extensible, as is Plone.
Nowadays everybody installs eggs. Eggs are a bunch of python files, together with other needed files like page templates and the like and a bit of Metadata.

Eggs are a much much younger than Zope. Zope needed something like eggs before there were eggs, and the Zope Developers wrote their own system, which we still see at some parts. But more and more functionality is pushed into the eggs alone.

Now, how can one extend Plone? A number of extensions create new things that can just be added to plone, like content types. Other things change functionality, like how the search page works or how the site looks like overall.

There are three different ways to extend Plone:
skin folders. Remember acquisition? Skin Folders are an extension of acquistion. I have a folder portal_skins. This contains a bunch of folders. I have a property on the portal_skins, that defines in which order attributes or objects should be looked for in the skin folder. If in some folder there is a python script called getEmail, and I want it to send obfuscated emails, my addon would add another folder to the portal_skins, and would add itself to the ordering so that the new folder would be looked for before the original folder. This way I can override behavior.

The next thing is GenericSetup. As the name clearly implies, GenericSetup is part of CMF. It is badly documented.
GenericSetup lets you define persistent configuration in xml files. Genericsetup parses the xml files and updates the persistent configuration accordingly. This is a step you have to run on your own!
Typically you use GenericSetup to modify workflows or add new content type definitions.

The last thing is ZCML. A bit of history again. When Zope started, Object oriented Design was the totally awesome technology. Zope objects have more than 10 Base Classes. After a while, XML and Components became a hype (J2EE anyone). So the Zope developers wanted a completely new Zope, component based. It is easier to swap out components than always subclass. The whole thing was named Zope 3, did not gain traction, was renamed to Bluebream and died off. But the component architecture itself was quite successfull and was extracted into the Zope Toolkit, which is integrated in Zope and heavily used in Plone. This is what you want to use.
For customizing, you can create utilities, adapters and views(MultiAdapters).
What is the absolute simplest way to extend functionality?
Monkey Patching. In code, during load time I import some code and replace it with my own code.
If one can have multiple implementations for something, I could make a global dictionary where everybody just adds its functionality during boot up. This does not scale. Multiple plugins might overwrite each other. Here comes the Zope Component Architecture and ZCML. With ZCML I declare my utilities, adapters and browser views in ZCML, which is a XML dialect. During start up, Zope reads all these ZCML statements, validates that there are not two things trying to register the same things and only then registers everything. This is a good thing. ZCML is btw. only ONE way to declare your configuration, another technology is Grok, where some python magic allows you to decorate your code directly with some magic to make it an adapter. And these two ways of configuring can be mixed.
Many ppl hate ZCML and avoid Zope because of it. I just find it cumbersome but even for me as a developer, it offers a nice advantage. Because of zcml, whenever I need to find out, where something has been implemented, the zcml files are like a phone book for me.

Installation
------------
Installation is a two step process. First, we must make our code available to Zope. This means, it must be importable. This is handled by Buildout.
ssh to your vagrant, and modify the buildout.cfg files in training/zinstance.
PloneFormGen, Products.LinguaPlone and Products.PloneTrueGallery, collective.plonetruegallery
DO THIS NOW
RESTART
After that the code is available, the ZCML gets loaded, so browser views, adapters and so on are available, but Plone is not configured to use this.
For this, you have to install the extension in your Plone Site.
Go to the Products Panel.
This is what happens now: The GenericSetup profile of the product gets loaded. This does things like configuring new actions, registering new
content types or adding browser views.

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
