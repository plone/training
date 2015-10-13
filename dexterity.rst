.. _dexterity1-label:

Dexterity I: "Through The Web"
==============================

In this part you will:

* Create the new content type *talk*


Topics covered:

* Content types
* Archetypes and Dexterity
* Fields
* Widgets


.. _dexterity1-what-label:

What is a content type?
-----------------------

A content type is a variety of object that can store information and is editable by users. We have different contenttypes to reflect the different kinds of information about which we need to collect and display information. Pages, folders, events, news items, files (binary) and images are all contenttypes.

It is common in developing a web site that you'll need customized versions of common contenttypes, or perhaps even entirely new types.

Remember the requirements for our project? We wanted to be able to solicit and edit conference talks. We could use the ``page`` content type for that purpose. But we need to make sure we collect certain bits of information about a talk and we couldn't be sure to get that information if we just asked potential presenters to create a page. Also, we'll want to be able to display talks featuring that special information, and we'll want to be able to show collections of talks. A custom content type will be ideal.

.. _dexterity1-contains-label:

The makings of a Plone content type
-----------------------------------

Every Plone content type has the following parts:

Schema
    A definition of fields that comprise a content type;
    properties of an object.

FTI
    The "Factory Type Information" configures the content type in Plone, assigns it a name, an icon, additional features and possible views to it.

Views
    A view is a representation of the object and the content of its fields that may be rendered in response to a request. You may have one or more views for an object. Some may be visual — intended for display as web pages — others may be intended to satisfy AJAX requests and be in formats like JSON or XML.


.. _dexterity1-comparison-label:

Dexterity and Archetypes - A Comparison
---------------------------------------

There are two content frameworks in Plone

* Dexterity: new and the coming default
* Archetypes: old, tried and tested
* Archetypes: widespread, used in many add-ons
* Plone 4.x: Archetypes is the default, with Dexterity available
* Plone 5.x: Dexterity is the default, with Archetypes available
* For both, add and edit forms are created automatically from a schema

What are the differences?

* Dexterity: New, faster, modular, no dark magic for getters and setters
* Archetype had magic setter/getter - use ``talk.getAudience()`` for the field ``audience``
* Dexterity: fields are attributes: ``talk.audience`` instead of ``talk.getAudience()``

TTW:

* Dexterity has a good TTW story.
* Archetypes has no TTW story.
* UML-modeling: `ArchGenXML <http://docs.plone.org/old-reference-manuals/archgenxml/index.html>`_ for Archetypes, `agx <http://agx.me>`_ for Dexterity

Approaches for Developers:

* Schema in Dexterity: TTW, XML, Python. Interface = schema, often no class needed
* Schema in Archetypes: Schema only in Python

* Dexterity: Easy permissions per field, easy custom forms.
* Archetypes: Permissions per field hard, custom forms even harder.
* If you have to program for old sites you need to know Archetypes!
* If starting fresh, go with Dexterity.

Extending:

* Dexterity has Behaviors: easily extendable. Just activate a behavior TTW and your content type is e.g. translatable (plone.app.multilingual).
* Archetypes has archetypes.schemaextender. Powerful but not as flexible.

We have only used Dexterity for the last few years.
We teach Dexterity and not Archetypes because it's more accessible to beginners, has a great TTW story and is the future.

Views:

* Both Dexterity and Archetypes have a default view for contenttypes.
* Browser Views provide custom views.
* TTW (future)
* Display Forms


.. Installation
   ------------

   .. note ::

    ..    We can skip this step since we installed ``plone.app.contenttypes`` when creating our Plone site in the beginning.


..    You don't have to modify the buildout since Plone 4.2+ ships with Dexterity. You just have to activate it in the control-panel for Add-ons.

..    This time, for no obvious reason other than getting more comfortable with the ZMI, we'll use ``portal_quickinstaller`` to install Dexterity.

..    * go to portal_quickinstaller
..    * install "Dexterity contenttypes"


.. _dexterity1-modify-label:

Modifying existing types
------------------------

* Go to the control panel http://localhost:8080/Plone/@@dexterity-types
* Inspect some of the existing default-types
* Select the type ``News Item`` and add a new field ``Hot News`` of type ``Yes/No``
* In another tab add a News Item and you see the new field.
* Go back to the schema-editor and click on `Edit XML Field Model <http://localhost:8080/Plone/dexterity-types/News%20Item/@@modeleditor>`_.
* Note that the only field in the xml-schema of the News Item is the one we just added. All others are provided by behaviors.
* Edit the form-widget-type so it says:

  .. code-block:: xml

    <form:widget type="z3c.form.browser.checkbox.SingleCheckBoxFieldWidget"/>

* Edit the News Item again. The widget changed from a radio field to a check box.
* The new field ``Hot News`` is not displayed when rendering the News Item. We'll take care of this later.


.. seealso::

   http://docs.plone.org/external/plone.app.contenttypes/docs/README.html#extending-the-types

.. _dexterity1-create-ttw-label:

Creating contenttypes TTW
--------------------------

In this step we will create a content type called *Talk* and try it out. When it's ready we will move the code from the web to the file system and into our own add-on. Later we will extend that type, add behaviors and a viewlet for Talks.

* Add new content type "Talk" and some fields for it:

  * Add Field "Type of talk", type "Choice". Add options: talk, keynote, training
  * Add Field "Details", type "Rich Text" with a maximal length of 2000
  * Add Field "Audience", type "Multiple Choice". Add options: beginner, advanced, pro
  * Check the behaviors that are enabled:  Dublin Core metadata, Name from title. Do we need them all?

* Test the content type
* Return to the control panel http://localhost:8080/Plone/@@dexterity-types
* Extend the new type

  * "Speaker", type: "Text line"
  * "Email", type: "Email"
  * "Image", type: "Image", not required
  * "Speaker Biography", type: "Rich Text"

* Test again

Here is the complete xml-schema created by our actions.

.. code-block:: xml
  :linenos:

  <model xmlns:lingua="http://namespaces.plone.org/supermodel/lingua"
       xmlns:users="http://namespaces.plone.org/supermodel/users"
       xmlns:security="http://namespaces.plone.org/supermodel/security"
       xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
       xmlns:form="http://namespaces.plone.org/supermodel/form"
       xmlns="http://namespaces.plone.org/supermodel/schema">
    <schema>
      <field name="type_of_talk" type="zope.schema.Choice">
        <description/>
        <title>Type of talk</title>
        <values>
          <element>Talk</element>
          <element>Training</element>
          <element>Keynote</element>
        </values>
      </field>
      <field name="details" type="plone.app.textfield.RichText">
        <description>Add a short description of the talk (max. 2000 characters)</description>
        <max_length>2000</max_length>
        <title>Details</title>
      </field>
      <field name="audience" type="zope.schema.Set">
        <description/>
        <title>Audience</title>
        <value_type type="zope.schema.Choice">
          <values>
            <element>Beginner</element>
            <element>Advanced</element>
            <element>Professionals</element>
          </values>
        </value_type>
      </field>
      <field name="speaker" type="zope.schema.TextLine">
        <description>Name (or names) of the speaker</description>
        <title>Speaker</title>
      </field>
      <field name="email" type="plone.schema.email.Email">
        <description>Adress of the speaker</description>
        <title>Email</title>
      </field>
      <field name="image" type="plone.namedfile.field.NamedBlobImage">
        <description/>
        <required>False</required>
        <title>Image</title>
      </field>
      <field name="speaker_biography" type="plone.app.textfield.RichText">
        <description/>
        <max_length>1000</max_length>
        <required>False</required>
        <title>Speaker Biography</title>
      </field>
    </schema>
  </model>


.. _dexterity1-ttw-to-code-label:

Moving contenttypes into code
------------------------------

It's awesome that we can do so much through the web. But it's also a dead end if we want to reuse this content type in other sites.

Also, for professional development, we want to be able to use version control for our work, and we'll want to be able to add the kind of business logic that will require programming.

So, we'll ultimately want to move our new content type into a Python package. We're missing some skills to do that, and we'll cover those in the next couple of chapters.

.. seealso::

   * `Dexterity Developer Manual <http://docs.plone.org/external/plone.app.dexterity/docs/index.html>`_
   * `The standard behaviors <http://docs.plone.org/external/plone.app.dexterity/docs/reference/standard-behaviours.html>`_


.. _dexterity1-excercises-label:

Exercises
---------

Exercise 1
++++++++++

Modify Pages to allow uploading an image as decoration (like News Items do).

..  admonition:: Solution
    :class: toggle

    * Go to the dexterity control panel (http://localhost:8080/Plone/@@dexterity-types)
    * Click on *Page* (http://127.0.0.1:8080/Plone/dexterity-types/Document)
    * Select the tab *Behaviors* (http://127.0.0.1:8080/Plone/dexterity-types/Document/@@behaviors)
    * Check the box next to *Lead Image* and save.

    The images are displayed above the title.

Exercise 2
++++++++++

Create a new content type called *Speaker* and export the schema to a XML File.
It should contain the following fields:

* Title, type: "Text Line"
* Email, type: "Email"
* Homepage, type: "URL" (optional)
* Biography, type: "Rich Text" (optional)
* Company, type: "Text Line" (optional)
* Twitter Handle, type: "Text Line" (optional)
* IRC Handle, type: "Text Line" (optional)
* Image, type: "Image" (optional)

Do not use the IDublinCore or the IBasic behavior since a speaker should not have a description.

We could use this content type later to convert speakers into Plone users. We could then link them to their talks.

..  admonition:: Solution
    :class: toggle

    The schema should look like this:

    ..  code-block:: xml

        <model xmlns:lingua="http://namespaces.plone.org/supermodel/lingua"
               xmlns:users="http://namespaces.plone.org/supermodel/users"
               xmlns:security="http://namespaces.plone.org/supermodel/security"
               xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
               xmlns:form="http://namespaces.plone.org/supermodel/form"
               xmlns="http://namespaces.plone.org/supermodel/schema">
          <schema>
            <field name="title" type="zope.schema.TextLine">
              <title>Name</title>
            </field>
            <field name="email" type="plone.schema.email.Email">
              <title>Email</title>
            </field>
            <field name="homepage" type="zope.schema.URI">
              <required>False</required>
              <title>Homepage</title>
            </field>
            <field name="biography" type="plone.app.textfield.RichText">
              <required>False</required>
              <title>Biography</title>
            </field>
            <field name="company" type="zope.schema.TextLine">
              <required>False</required>
              <title>Company</title>
            </field>
            <field name="twitter_handle" type="zope.schema.TextLine">
              <required>False</required>
              <title>Twitter Handle</title>
            </field>
            <field name="irc_name" type="zope.schema.TextLine">
              <required>False</required>
              <title>IRC Handle</title>
            </field>
            <field name="image" type="plone.namedfile.field.NamedBlobImage">
              <required>False</required>
              <title>Image</title>
            </field>
          </schema>
        </model>

..  seealso::

    * `Dexterity XML <http://docs.plone.org/external/plone.app.dexterity/docs/reference/dexterity-xml.html>`_
    * `Model-driven types <http://docs.plone.org/external/plone.app.dexterity/docs/model-driven-types.html#model-driven-types>`_
