Extending Plone with Add-ons
============================

Introduction
-------------

There are more than a thousand addons for Plone. We will cover only a handfull today.

* What types of addons are there
* How to find addons


Installing Addons
-----------------

Installation is a two-step process.
First, we must make the addons code available to Zope. This means, that Zope can import the code, buildout is responsible this.

Use ``vagrant ssh``to ssh to your vagrant, and change the buildout.cfg file in XXX.

In the section ``[instance]`` there is a variable called ``eggs``, which has multiple *eggs* as a value. Add the following eggs:

    * PloneFormGen
    * Products.LinguaPlone
    * collective.plonetruegallery

Usually, one enters the eggs by adding one more line per egg into the configuration.
You must write the egg name indented, this way Buildout understands that the current line is part of the last variable and not a new variable.

.. sourcecode:: bash

    $ bin/buildout
    $ bin/instance fg

Now the code is importable from within Plone and everything got registered via ZCML.
But your Plone-site has not yet been told to use this. For this, you have to install the addons in your Plone Site.

In your browser, go the control panel ``@@plone_control_panel``, and open the ``Addons`` Panel. You will see that you can install all 4 packages there.

Install them now.

This is what happens now: The GenericSetup profile of the product gets loaded. This does things like

* configuring new actions,
* registering new content types or
* creating some content/configuration objects in your Plone site.

Let' have a look at what we just installed.


PloneFormGen (Philip)
---------------------

There a various methods to create forms in Plone:

* pure html in a view
* z3c.form, formlib or in Python deform prgrammatically
* PloneFormGen

PFG allow you to create great forms ttw. Imagine the following possibilites.

* easy form to subscribe a newsletter?
* registration-form (Name, Food, Shirt-size etc.)
* Mail-Adapter
* DataSave Adapter

Written by Steve McMahon. You might want to buy him a beer.


Internationalisation with LinguaPlone and plone.app.multilingual (Philip)
-------------------------------------------------------------------------

* ``/plone_control_panel``
* install installieren
* add german as language einstellen

   * ``/@@language-controlpanel`` -> Deutsch und Englisch auswählen
   * ZMI -> portal_languages -> "Display flags for language selection" aktivieren

* ``/@@language-setup-folders`` -> Ordnerstruktur anlegen
* Create english frontpage
* Best prachtive about translating zum übersetzen (folder übersetzen, language_independent)

   * http://plone.org/products/linguaplone/issues/250

   * http://localhost:8080/Plone/@@language-setup-folders

   * Seit Plone4 ist der Standardweg von Übersetzungen, das jede Sprache einen eigenen Folder bekommt. Wenn Inhalte übersetzt werden, wird

* die Datei automatisch in den richtigen Ordner kopiert.


Add 'bling' with PloneTrueGallery (10min) (Patrick)
---------------------------------------------------
I LOVE THE
PloneTrueGallery.
It is a role model on how to write a Plone Extension.
Instead of creating custom content types for Galleries, it integrates
with the Plone functionality to choose different views for folderish content types.
Lets try it!...


Customizing the design with plone.app.themeeditor (20min) (Philip)
------------------------------------------------------------------

* Installation
* explain UI
* change Logo (download http://www.ploneconf.org/++theme++ploneconf.theme/images/logo.png)
* change Footer (colophon): add copyright (Phone: +31 26 44 22 700
  mailto:info@ploneconf.org)
* change some css:

.. sourcecode:: css

    #visual-portal-wrapper {
        margin: 0 auto;
        position: relative;
        width: 980px;
    }


export customizations
---------------------

* export the customizations as an egg (ploneconf.customisations)


inspect the egg
---------------

* what is where?
* jbot, static etc.


Wir können nun das Design unserer Webseite anpassen. Wir können Erweiterungen installieren und einfache Aktionen einrichten. Aber:

* Können wir auf unserer neuen Webseite Talks einreichen?
* Können wir in einer Liste die wichtigsten Eigenschaften jedes Talks anzeigen?
* Können wir Besucher den Talk bewerten lassen?

Wir müssen oft strukturierte Daten speichern oder anzeigen können, bis zu einem gewissen Grad auch noch TTW, aber irgendwann erreichen wir eine Grenze. Wir werden im zweiten Teil zeigen, wie man neue Contenttypen anlegt und wie man neue Funktionalitäten schreibt.

