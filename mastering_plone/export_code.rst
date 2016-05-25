.. _export_code-label:

Return to Dexterity: Moving contenttypes into Code
===================================================


.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/02_export_code_p5/ src/ploneconf.site


In this part you will:

* Move the type *talk* into ``ploneconf.site``
* Improve the schema and the FTI


Topics covered:

* FTI
* type definitions with generic setup
* XML schema
* more widgets

Remember the *Talk* content type that we created through-the-web with Dexterity? Let's move that new content type into our add-on package so that it may be installed in other sites without TTW manipulation.

Steps:

* Return to the Dexterity control panel
* Export the Type Profile and save the file
* Delete the Type from the site before installing it from the file system
* Extract the files from the exported tar file and add them to our add-on package in ``profiles/default/``

.. note::

    From the buildout directory perspective that is ``src/ploneconf.site/src/ploneconf/site/profiles/default/``

The file ``profiles/default/types.xml`` tells Plone that there is a new content type defined in file ``talk.xml``.

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_types" meta_type="Plone Types Tool">
     <property name="title">Controls the available contenttypes in your portal</property>
     <object name="talk" meta_type="Dexterity FTI"/>
     <!-- -*- more types can be added here -*- -->
    </object>

Upon installing, Plone reads the file ``profiles/default/types/talk.xml`` and registers a new type in ``portal_types`` (you can find and inspect this tool in the ZMI!) with the information taken from that file.

..  code-block:: xml

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
      <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
      <element value="plone.app.content.interfaces.INameFromTitle"/>
     </property>
     <property name="schema"></property>
     <property
        name="model_source">&lt;?xml version='1.0' encoding='utf8'?&gt;
  &lt;model xmlns:lingua="http://namespaces.plone.org/supermodel/lingua" xmlns:users="http://namespaces.plone.org/supermodel/users" xmlns:form="http://namespaces.plone.org/supermodel/form" xmlns:i18n="http://xml.zope.org/namespaces/i18n" xmlns:security="http://namespaces.plone.org/supermodel/security" xmlns:marshal="http://namespaces.plone.org/supermodel/marshal" xmlns="http://namespaces.plone.org/supermodel/schema"&gt;
        &lt;schema&gt;
          &lt;field name="type_of_talk" type="zope.schema.Choice"&gt;
            &lt;description/&gt;
            &lt;title&gt;Type of talk&lt;/title&gt;
            &lt;values&gt;
              &lt;element&gt;Talk&lt;/element&gt;
              &lt;element&gt;Training&lt;/element&gt;
              &lt;element&gt;Keynote&lt;/element&gt;
            &lt;/values&gt;
          &lt;/field&gt;
          &lt;field name="details" type="plone.app.textfield.RichText"&gt;
            &lt;description&gt;Add a short description of the talk (max. 2000 characters)&lt;/description&gt;
            &lt;max_length&gt;2000&lt;/max_length&gt;
            &lt;title&gt;Details&lt;/title&gt;
          &lt;/field&gt;
          &lt;field name="audience" type="zope.schema.Set"&gt;
            &lt;description/&gt;
            &lt;title&gt;Audience&lt;/title&gt;
            &lt;value_type type="zope.schema.Choice"&gt;
              &lt;values&gt;
                &lt;element&gt;Beginner&lt;/element&gt;
                &lt;element&gt;Advanced&lt;/element&gt;
                &lt;element&gt;Professionals&lt;/element&gt;
              &lt;/values&gt;
            &lt;/value_type&gt;
          &lt;/field&gt;
          &lt;field name="speaker" type="zope.schema.TextLine"&gt;
            &lt;description&gt;Name (or names) of the speaker&lt;/description&gt;
            &lt;title&gt;Speaker&lt;/title&gt;
          &lt;/field&gt;
          &lt;field name="email" type="plone.schema.email.Email"&gt;
            &lt;description&gt;Adress of the speaker&lt;/description&gt;
            &lt;title&gt;Email&lt;/title&gt;
          &lt;/field&gt;
          &lt;field name="image" type="plone.namedfile.field.NamedBlobImage"&gt;
            &lt;description/&gt;
            &lt;required&gt;False&lt;/required&gt;
            &lt;title&gt;Image&lt;/title&gt;
          &lt;/field&gt;
          &lt;field name="speaker_biography" type="plone.app.textfield.RichText"&gt;
            &lt;description/&gt;
            &lt;max_length&gt;1000&lt;/max_length&gt;
            &lt;required&gt;False&lt;/required&gt;
            &lt;title&gt;Speaker Biography&lt;/title&gt;
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

Now our package has some real contents. So, we'll need to reinstall it (if installed before).

* Restart Plone.
* Re-install ploneconf.site (deactivate and activate).
* Test the type by adding an object or editing one of the old ones.
* Look at how the talks are presented in the browser.

The escaped inline xml is simply too ugly to look at. You should move it to a separate file!

Create a folder ``content`` with an empty ``__init__py``. In that create a file ``talk.xml`` that contains the real xml (copied from http://localhost:8080/Plone/dexterity-types/talk/@@modeleditor and beautified with some online xml formatter (http://lmgtfy.com/?q=xml+formatter))

..  code-block:: xml
    :linenos:

    <?xml version='1.0' encoding='utf8'?>
      <model xmlns:lingua="http://namespaces.plone.org/supermodel/lingua" xmlns:users="http://namespaces.plone.org/supermodel/users" xmlns:form="http://namespaces.plone.org/supermodel/form" xmlns:i18n="http://xml.zope.org/namespaces/i18n" xmlns:security="http://namespaces.plone.org/supermodel/security" xmlns:marshal="http://namespaces.plone.org/supermodel/marshal" xmlns="http://namespaces.plone.org/supermodel/schema">
        <schema>
          <field name="type_of_talk" type="zope.schema.Choice">
            <description/>
            <title>Type of Talk</title>
            <values>
              <element>Talk</element>
              <element>Training</element>
              <element>Keynote</element>
            </values>
          </field>
          <field name="details" type="plone.app.textfield.RichText">
            <description>Add a short description of the talk (max. 2000 characters)</description>/&gt;
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
                <element>Professional</element>
              </values>
            </value_type>
          </field>
          <field name="speaker" type="zope.schema.TextLine">
            <description>Name (or names) of the speaker</description>/&gt;
            <title>Speaker</title>
          </field>
          <field name="email" type="plone.schema.email.Email">
            <description>Adress of the speaker</description>/&gt;
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

Now we have to remove the model_source and instead reference the xml file in the FTI by using the property ``model_file``:

..  code-block:: xml

    <property name="model_source"></property>
    <property name="model_file">ploneconf.site.content:talk.xml</property>

..  note::

    The default types of Plone 5 also have an xml schema like this since that allows the fields of the types to be editable trough the web! Fields for types with a python schema are not editable ttw.

`Dexterity XML <http://docs.plone.org/external/plone.app.dexterity/docs/reference/dexterity-xml.html>`_ is very powerful. By editing it (not all features have a UI) you should be able to do everything you can do with a python schema.

Our talks use a dropdown for ``type_of_talk`` and a multiselect for ``audience``. Radio-buttons and checkboxes would be the better choice here. Modify the xml to make that change happen:

..  code-block:: xml
    :linenos:
    :emphasize-lines: 5, 20

    <?xml version="1.0" encoding="UTF-8"?>
    <model xmlns="http://namespaces.plone.org/supermodel/schema" xmlns:form="http://namespaces.plone.org/supermodel/form" xmlns:marshal="http://namespaces.plone.org/supermodel/marshal" xmlns:security="http://namespaces.plone.org/supermodel/security">
      <schema>
        <field name="type_of_talk" type="zope.schema.Choice"
          form:widget="z3c.form.browser.radio.RadioFieldWidget">
          <description />
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
        <field name="audience" type="zope.schema.Set"
          form:widget="z3c.form.browser.checkbox.CheckBoxFieldWidget">
          <description />
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
          <description />
          <required>False</required>
          <title>Image</title>
        </field>
        <field name="speaker_biography" type="plone.app.textfield.RichText">
          <description />
          <max_length>1000</max_length>
          <required>False</required>
          <title>Speaker Biography</title>
        </field>
      </schema>
    </model>


Exercise 1
++++++++++

Create a new package called ``collective.behavior.myfeature``. Inspect the directory structure of this package. Delete it after you are done.

..  admonition:: Solution
    :class: toggle

    .. code-block:: bash

        $ cd src
        $ ../bin/mrbob -O collective.behavior.myfeature bobtemplates:plone_addon

    Many packages that are part of Plone and some add-ons use a nested namespace such as ``plone.app.contenttypes``.


Exercise 2
++++++++++

Go to the ZMI and and in ``portal_types`` look for the definition of the new ``Talk`` content type. Now deactivate *Implicitly addable?* and save. Go back to the site can you identify what this change has caused? And why is that useful?

..  admonition:: Solution
    :class: toggle

    Go to http://localhost:8080/Plone/portal_types/Talk/manage_propertiesForm

    When disabling *Implicitly addable* you can no longer add Talks any more unless you change some container like the type *Folder*: Enable *Filter contenttypes?* for it and add *Talk* to the items that are allowed.

    With this method you can prevent content that only makes sense inside some defined structure to show up in places where they do not belong.

    The equivalent setting for disabling *Implicitly addable* in ``Talk.xml`` is:

    .. code-block:: xml

        <property name="global_allow">False</property>
