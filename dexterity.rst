Creating content-types with Dexterity
=====================================


What is a content-type?
-----------------------

A content-type is object that can store information and is editable by users.

Schema
    A definition of fields that comprise a content-type
    properties of an object

FTI
    The "Factory Type Information" configures the content-type in Plone, assigns a name, an icon, additional features and possible views to it.

View
    The visual representation of the object and the content of it's fields.


Dexterity and Archetypes - A Comparison
---------------------------------------

Two content-frameworks in Plone

* Dexterity: new and the coming default
* Archetypes: old, tried and tested
* Archetypes: widespread though addons
* Plone 4.x: Archetypes
* Plone 5.x: Dexterity-versions
* add and edit-forms are created automatically from a schema

What are the differences?

* Dexterity: New, faster, no dark magic for getters und setters. modular
* Archetype had magic setter/getter - use talk.getAudience() for the field 'audience'
* Dexterity: fields are attributes: talk.audience instead of talk.getAudience()

TTW:

* Dexterity has a good TTW-story.
* Archetypes has no ttw-story
* Archetypes has ArchGenXML for UML-modeling (agx will bring this to Dexterity too)

Approaches for Developers:

* Schema in Dexterity: ttw, xml, python. interface = schema, often no class needed
* Schema in Archetypes: schema only in python

* Dexterity: easy permissions per field, easy custom forms
* Archetypes: permissions per field hard, custom forms even harder
* If you have to programm for old sites you need to know Archetypes!
* If you start new pages you could skip it.

Extending:

* Dexterity has Behaviors: easily extendable. Just activate an behavior ttw and you ct is translateable (plone.app.multilingual). There might even be per-instance behaviors at one time...
* Archetypes has archetypes.schemaextender. Powerfull but not as flexible

We use dexterity whenever possible because of these points.
We teach Dexterity and not Archetypes since it's much more accessible to beginners, has a great TTW-story and is the future.

Views:

* Both Dexterity and Archetypes have a default-view for content-types.
* Grok Views
* Display Forms
* Browser Views (zcml)
* TTW (future)


Installation
------------

You don't have modify the buildout since Plone 4.3.x already ships with Dexterity. You just have to activate it in the control-panel for Add-ons.

This time for no obvous reason other than getting more comfortable with the ZMI we'll use ``portal_quickinstaller`` to install Dexterity.

* go to portal_quickinstaller
* install "Dexterity Content Types"

In this step we will create a CT called 'Talk' and try it. When it's ready we will move the code from the web to the file system and into our egg. Later we will expand on that type and add behaviors and a viewlet for Talks.

Creating content-types TTW
--------------------------

* There now is a new entry in ``plone_control_panel`` called "Dexterity Content Types".
* Add new content type "Talk" and some fields for it:

  * Add Field "Audience", type "Multiple Choice". Add options: beginner, advanced, pro
  * Image "Image" (portrait)
  * Check the behaviors that are enabled: Basic metadata, Name from title, Referenceable

* Test the content-type
* Return to the control panel http://localhost:8080/Plone/@@dexterity-types
* Extend the new type by adding a Richtext-field "Details"
* Test again

Here is the xml-scheme created by our actions:

.. code-block:: xml

  <model xmlns:security="http://namespaces.plone.org/supermodel/security"
         xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
         xmlns:form="http://namespaces.plone.org/supermodel/form"
         xmlns="http://namespaces.plone.org/supermodel/schema">
    <schema>
      <field name="audience" type="zope.schema.Set">
        <description/>
        <title>Audience</title>
        <value_type type="zope.schema.Choice">
          <values>
            <element>beginner</element>
            <element>advanced</element>
            <element>pro</element>
          </values>
        </value_type>
      </field>
      <field name="image" type="plone.namedfile.field.NamedBlobImage">
        <description>Some image</description>
        <required>False</required>
        <title>Image</title>
      </field>
      <field name="details" type="plone.app.textfield.RichText">
        <description/>
        <title>Details</title>
      </field>
    </schema>
  </model>


Moving content-types into code
---------------------------------

We want version-control and more extendability so we move our new content-types into code.

* Export the Type Profile and save the file
* Delete type from the site before installing the type from the file-system
* Extract the files from the exported tar-file and add them to ``plonekonf/talk/profiles/default/``

Here is the result. The file ``types.xml`` tells plone that there is a new content type defined in file ``talk.xml``.

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_types" meta_type="Plone Types Tool">
     <property name="title">Controls the available content types in your portal</property>
     <object name="talk" meta_type="Dexterity FTI"/>
     <!-- -*- extra stuff goes here -*- -->
    </object>

Upon installing Plone reads the file ``types/talk.xml`` and registers a new type in ``portal_types`` with the information derived from that file.

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="talk" meta_type="Dexterity FTI" i18n:domain="plone"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n">
     <property name="title" i18n:translate="">Talk</property>
     <property name="description" i18n:translate="">None</property>
     <property name="icon_expr">string:${portal_url}/document_icon.png</property>
     <property name="factory">talk</property>
     <property name="add_view_expr">string:${folder_url}/++add++talk</property>
     <property name="link_target"></property>
     <property name="immediate_view">view</property>
     <property name="global_allow">True</property>
     <property name="filter_content_types">True</property>
     <property name="allowed_content_types"/>
     <property name="allow_discussion">False</property>
     <property name="default_view">view</property>
     <property name="view_methods">
      <element value="view"/>
     </property>
     <property name="default_view_fallback">False</property>
     <property name="add_permission">cmf.AddPortalContent</property>
     <property name="klass">plone.dexterity.content.Container</property>
     <property name="behaviors">
      <element value="plone.app.content.interfaces.INameFromTitle"/>
      <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
     </property>
     <property name="schema"></property>
     <property name="model_source">&lt;model
        xmlns:security="http://namespaces.plone.org/supermodel/security"
        xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
        xmlns:form="http://namespaces.plone.org/supermodel/form"
        xmlns="http://namespaces.plone.org/supermodel/schema"&gt;
        &lt;schema&gt;
          &lt;field name="audience" type="zope.schema.Set"&gt;
            &lt;description/&gt;
            &lt;title&gt;Audience&lt;/title&gt;
            &lt;value_type type="zope.schema.Choice"&gt;
              &lt;values&gt;
                &lt;element&gt;beginner&lt;/element&gt;
                &lt;element&gt;advanced&lt;/element&gt;
                &lt;element&gt;pro&lt;/element&gt;
              &lt;/values&gt;
            &lt;/value_type&gt;
          &lt;/field&gt;
          &lt;field name="image" type="plone.namedfile.field.NamedBlobImage"&gt;
            &lt;description&gt;Portrait of the speaker&lt;/description&gt;
            &lt;required&gt;False&lt;/required&gt;
            &lt;title&gt;Image&lt;/title&gt;
          &lt;/field&gt;
          &lt;field name="details" type="plone.app.textfield.RichText"&gt;
            &lt;description/&gt;
            &lt;title&gt;Details&lt;/title&gt;
          &lt;/field&gt;
        &lt;/schema&gt;
      &lt;/model&gt;</property>
     <property name="model_file"></property>
     <property name="schema_policy">dexterity</property>
     <alias from="(Default)" to="(dynamic view)"/>
     <alias from="edit" to="@@edit"/>
     <alias from="sharing" to="@@sharing"/>
     <alias from="view" to="(selected layout)"/>
     <action title="View" action_id="view" category="object" condition_expr=""
        description="" icon_expr="" link_target="" url_expr="string:${object_url}"
        visible="True">
      <permission value="View"/>
     </action>
     <action title="Edit" action_id="edit" category="object" condition_expr=""
        description="" icon_expr="" link_target=""
        url_expr="string:${object_url}/edit" visible="True">
      <permission value="Modify portal content"/>
     </action>
    </object>

* restart Plone
* install plonekonf.talk

Got to the ZMI and look at the definition of the new type in ``portal_types``.

* Test the type by adding an object or editing one of the old ones.
* Look at how the talks are presented in the browser.

Now let's see if we can't improve the default view. To do this we first need to learn about templates.

Read more about developing with Dexterity here: http://developer.plone.org/reference_manuals/external/plone.app.dexterity/
