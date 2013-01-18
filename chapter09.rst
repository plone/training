

9. Creating a new content-type "Talk" with Dexterity (45min) (Philip)
=====================================================================

 * Dexterity - An introduction
 * Creating content-types TTW
 * Exporting content-types into code


What is a content-type?
-----------------------

A content-type is object that can store information and is editable by users.

Schema
    A definition of fields that comprise a content-type (in Django that would be the Model)
    These input to these fields can be stored in properties of an object.

    python, xml or ttw

FTI
    The "Factory Type Information" configures the content-type in Plone, assigns a name, an icon, additional features and possible views to it.

    xml or ttw

View
    A visual representation of the objecta and the content of it's fields.

    Written as python and zope page templates (a templating language)


Dexterity and Archetypes - A Comparison
---------------------------------------

There are two content-frameworks in Plone

* Dexterity is relatively new. Will be core in Plone 4.3 (4.3a2 is here to test)
* Archetypes is old, tried and tested (Around since Plone 1.0.4)
* Archetypes: Very widespread, almost all existing addons are based on Archetypes
* Plone's default content-types are Archetypes (unless you use plone.app.contentypes)

What do they have in common:

* add and edit-forms are created automatically from the schema

What are the differences?

* Dexterity: New, faster, no dark magic for getters und setters, modular
* Archetype had magic setter/getter - use talk.getAudience() for the field 'audience'
* Dexterity: fields are attributes: talk.audience instead of talk.getAudience()

TTW:
* Dexterity has a good TTW-story.
* Archetypes has no ttw-story
* Archetypes has ArchGenXML for UML-modeling (agx will bring this to Dexterity too)

Approaches:
* Schema in Dexterity: ttw, xml, python. interface = schema, often no class needded
* Schema in Archetypes: schema only in python

* Dexterity: easy permissions per field, easy custom forms
* Archetypes: permissions per field hard, custom forms even harder
* If you have to programm for old sites you need to know Archetypes!
* If you start new pages you could skip it.

Extending:
  * Dexterity has Behaviors: easily extendable. Just activate an behavior ttw and you ct is translateable (plone.app.multilingual). There might even be per-instance behaviors at one time...
  * Archetypes has archetypes.schemaextender. Powerfull but not as flexible

We use dexterity whenever possible beacause of these points.
We teach Dexterity and not Archetypes since it's much more accessible to beginners and has a great TTW-story.

Views:
* Both Dexterity and Archetypes have a default-view for content-types.
* Grok Views
* Display Forms
* Browser Views (zcml)
* TTW (is coming)


Installation
------------

Plone 4.2 already has version-pinnings for dexterity :-)

So all you need is to add plone.app.dexterity to your list of eggs::

    [eggs]
        Plone
        plone.app.dexterity
        ...

Run ./bin/buildout,

In this step we will create a CT called 'Talk' and try it. When it's ready we will move the code from the web to the file system and into our egg. Later we will expand on that type and add behaviors and a viewlet for Talks.

* restart the instance
* go to portal_quickinstaller
* install "Dexterity Content Types"


Creating content-types TTW
--------------------------

* Add new CT "Talk"

  * Multiple Choice "Audience" (beginner, advanced, pro)
  * Image "Image" (portrait)
  * Behaviors: Basic metadata, Name from title, Referenceable

* Test the content-type
* explain the base_view
* extend it (add Richtext "Details")
* Test again
* Export ("Export Type Profiles" and save file)
* delete type before installing the type from the file-system


Exporting content-types into code
---------------------------------

Let's assume we did this: Add new egg to buildout (we can remove plone.app.dexterity from buildout if we add it as a dependency in setup.py and metadata.xml)::

* extract code from exported tar-file and add to plonekonf/talk/profiles/default/
* restart instance
* install plonekonf.talk
* test type and look at the default-view


