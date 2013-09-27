Extend Plone with Add-ons
==========================

There are more than a thousand addons for Plone. We will cover only a handfull today.

* What types of addons are there

How to find addons
------------------

* https://pypi.python.org/pypi - use the search form!
* http://plone.org/products
* https://github.com/collective >1000 repositories!
* https://github.com/plone  240 repos - not all of them are part of the core yet!
* http://news.gmane.org/gmane.comp.web.zope.plone.user search mailing list-archive
* Addon shortlist (work in progress): https://docs.google.com/spreadsheet/ccc?key=0At7ok0VqX0egdExISThOa0JBYjVUYi1pWmRDU0QyeUE#gid=0
* google
* ask


Installing Addons
-----------------

Installation is a two-step process.

First, we must make the addons code available to Zope. This means, that Zope can import the code, buildout is responsible for this.

Use ``vagrant ssh`` to ssh to your vagrant, and change the buildout.cfg file in XXX.

In the section ``[instance]`` there is a variable called ``eggs``, which has multiple *eggs* as a value. Add the following eggs:

    * ``Products.PloneFormGen``
    * ``Products.LinguaPlone``
    * ``collective.plonetruegallery``
    * ``plone.app.themeeditor``


Usually, one enters the eggs by adding one more line per egg into the configuration.
You must write the egg name indented, this way Buildout understands that the current line is part of the last variable and not a new variable.

.. sourcecode:: bash

    $ bin/buildout
    $ bin/instance fg

Now the code is importable from within Plone and everything got registered via ZCML.
But your Plone-site has not yet been told to use this. For this, you have to install the addons in your Plone Site.

In your browser, go the control panel ``@@plone_control_panel``, and open the ``Addons`` Panel. You will see that you can install all three packages there.

Install them now.

This is what happens: The GenericSetup profile of the product gets loaded. This does things like:

* configuring new actions,
* registering new content types or
* creating some content/configuration objects in your Plone site.

Let' have a look at what we just installed.


PloneFormGen
------------

There a various methods to create forms in Plone:

* pure html in a view
* z3c.form, formlib or in Python deform prgrammatically
* PloneFormGen

PFG allow you to create great forms ttw.
Let's write a registration-form for our conference

* Add a object of the new type 'Form Folder' in the site-root. Call it "Registration"
* Save and view the result
* Click in QuickEdit
* Remove field "Subject"
* Add fields for food-preference and shirt-size
* Add a DataSave Adapter
* Try it

Written by Steve McMahon. You might want to buy him a beer.


Internationalisation with LinguaPlone and plone.app.multilingual (Philip)
-------------------------------------------------------------------------

We're not doing this with out site.

* Go to the ``/plone_control_panel``
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


Add 'bling' with collective.plonetruegallery
--------------------------------------------
I LOVE THE PloneTrueGallery.

It is a role model on how to write a Plone Extension.
Instead of creating custom content types for Galleries, it integrates
with the Plone functionality to choose different views for folderish content types.

Lets try it!...


Customizing the design with plone.app.themeeditor
-------------------------------------------------

* Installation
* explain UI
* change Logo (download http://www.sixfeetup.com/blog/2011PloneConfLogo.gif - the brazil-logo is to big)
* change Footer (footer.pt):

  .. code-block:: html

      <p>&copy; 2013 by me! |
         Phone: +31 26 44 22 700 |
        <a href="mailto:info@ploneconf.org">
         Contact us
        </a>
      </p>

* Look at ``ploneCustom.css``. Recognize the changes we did before?:
* Add some more css to make our site a little responsive

.. code-block:: css

    @media only screen and (max-width: 980px) {
        #visual-portal-wrapper {
            position: relative;
            width: auto;
        }
    }

    @media only screen and (max-width: 768px) {
        #portal-columns > div {
            width: 97.75%;
            margin-left: -98.875%;
            clear: both;
        }

        .searchButton,
        .searchSection {
            display: none;
        }
    }



export customizations
---------------------

* export the customizations as an egg (ploneconf.theme)


inspect the package
--------------------

* what is where?
* jbot, static etc.


Wir können nun das Design unserer Webseite anpassen. Wir können Erweiterungen installieren und einfache Aktionen einrichten. Aber:

* Können wir auf unserer neuen Webseite Talks einreichen?
* Können wir in einer Liste die wichtigsten Eigenschaften jedes Talks anzeigen?
* Können wir Besucher den Talk bewerten lassen?

Wir müssen oft strukturierte Daten speichern oder anzeigen können, bis zu einem gewissen Grad auch noch TTW, aber irgendwann erreichen wir eine Grenze. Wir werden im zweiten Teil zeigen, wie man neue Contenttypen anlegt und wie man neue Funktionalitäten schreibt.

