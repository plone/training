---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-export-code-label)=

# Return to Dexterity: Moving contenttypes into Code

````{sidebar} Get the code!

Code for the beginning of this chapter:

```shell
git checkout eggs1
```

Code for the end of this chapter:

```shell
git checkout export_code
```

{doc}`code`
````

In this part you will:

- Move the _Talk_ type into {py:mod}`ploneconf.site`
- Improve the schema and the FTI

Topics covered:

- Content type definitions with generic setup
- FTI
- XML schema
- more widgets

Remember the _Talk_ content type that we created through-the-web with Dexterity? Let's move that new content type into our add-on package so that it may be installed in other sites without TTW manipulation.

Steps:

- Return to the Dexterity control panel
- Export the _Talk_ Type Profile and save the file
- Delete the _Talk_ from the site before installing it from the file system
- Extract the files from the exported tar file and add them to our add-on package in {file}`profiles/default/`

```{note}
From the buildout directory perspective that is {file}`src/ploneconf.site/src/ploneconf/site/profiles/default/`
```

The file {file}`profiles/default/types.xml` tells Plone that there is a new content type defined in file {file}`talk.xml`.

```xml
<?xml version="1.0"?>
<object name="portal_types" meta_type="Plone Types Tool">
 <property name="title">Controls the available contenttypes in your portal</property>
 <object name="talk" meta_type="Dexterity FTI"/>
 <!-- -*- more types can be added here -*- -->
</object>
```

Upon installing, Plone reads the file {file}`profiles/default/types/talk.xml` and registers a new type in `portal_types` (you can find and inspect this tool in the ZMI!) with the information taken from that file.

```xml
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
    <element value="plone.dublincore"/>
    <element value="plone.namefromtitle"/>
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
```

Now our package has new configuration for Generic Setup. Generic Setup store the configiuration for the site in the folder {file}`profiles/`. This configuration is applied to your site upon installing the package. So, we'll need to reinstall it (if installed before).

- Restart Plone.
- Re-install ploneconf.site (deactivate and activate).
- Test the type by adding an object or editing one of the old ones.
- Look at how the talks are presented in the browser.

The escaped inline xml is simply too ugly to look at. You should move it to a separate file!

Create a new folder {file}`content` in the main directory (from the buildout directory perspective that is {file}`src/ploneconf.site/src/ploneconf/site/content/`). Inside add an empty file {file}`__init__.py` and a file {file}`talk.xml` that contains the real XML (copied from <http://localhost:8080/Plone/dexterity-types/talk/@@modeleditor> and beautified with some online XML formatter (<https://www.google.com/?q=xml+formatter>))

```{code-block} xml
:linenos:

<?xml version='1.0' encoding='utf8'?>
  <model xmlns="http://namespaces.plone.org/supermodel/schema"
         xmlns:form="http://namespaces.plone.org/supermodel/form"
         xmlns:i18n="http://xml.zope.org/namespaces/i18n"
         xmlns:lingua="http://namespaces.plone.org/supermodel/lingua"
         xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
         xmlns:security="http://namespaces.plone.org/supermodel/security"
         xmlns:users="http://namespaces.plone.org/supermodel/users">
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
```

Now remove the ugly model_source and instead point to the new XML file in the FTI by using the property `model_file`:

```xml
<property name="model_source"></property>
<property name="model_file">ploneconf.site.content:talk.xml</property>
```

`ploneconf.site.content:talk.xml` points to a file {file}`talk.xml` to be found in the Python path `ploneconf.site.content`. The {file}`__init__.py` is needed to turn the folder {file}`content` into a Python package. It is best-practice to add schemas in this folder, and in later chapters you will add new types with pythons-schemata in the same folder.

```{note}
The default types of Plone 5 also have an xml schema like this since that allows the fields of the types to be editable trough the web! Fields for types with a python schema are not editable ttw.
```

## Changing a widget

[Dexterity XML](https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/dexterity-xml.html) is very powerful. By editing it (not all features have a UI) you should be able to do everything you can do with a Python schema.
Sadly not every feature also is exposed in the UI of the dexterity schema editor. For example you cannot yet change the widgets or permissions for fields in the UI. We need to do this in the xml- or python-schema.

Our talks use a dropdown for {guilabel}`type_of_talk` and a multiselect for {guilabel}`audience`. Radio-buttons and checkboxes would be the better choice here. Modify the XML to make that change happen:

```{code-block} xml
:emphasize-lines: 11, 26
:linenos:

<?xml version="1.0" encoding="UTF-8"?>
<model xmlns="http://namespaces.plone.org/supermodel/schema"
       xmlns:form="http://namespaces.plone.org/supermodel/form"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n"
       xmlns:lingua="http://namespaces.plone.org/supermodel/lingua"
       xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
       xmlns:security="http://namespaces.plone.org/supermodel/security"
       xmlns:users="http://namespaces.plone.org/supermodel/users">
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
```

## Protect fields with permissions

We also want to have a add a new field `room` to show where a talk will take place.
Our case-study says the speakers will submit the talks online.
How should they know in which room the talk will take place (if it got accepted at all)?
So we need to hide this field from them by requiring a permission that they do not have.

Let's assume the prospective speakers will not have the permission to review content (i.e. edit submitted content and publish it) but the organizing commitee has.
You can then protect the field using the permission `Review portal content` in this case the name of the permission-utility for this permission: `cmf.ReviewPortalContent`.

We only want to prevent writing, not reading, so we'll only manage the `write-permission`:

```{code-block} xml
:emphasize-lines: 38-50
:linenos:

<?xml version="1.0" encoding="UTF-8"?>
<model xmlns="http://namespaces.plone.org/supermodel/schema"
       xmlns:form="http://namespaces.plone.org/supermodel/form"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n"
       xmlns:lingua="http://namespaces.plone.org/supermodel/lingua"
       xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
       xmlns:security="http://namespaces.plone.org/supermodel/security"
       xmlns:users="http://namespaces.plone.org/supermodel/users">
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
    <field name="audience"
           type="zope.schema.Set"
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
    <field name="room"
           type="zope.schema.Choice"
           form:widget="z3c.form.browser.radio.RadioFieldWidget"
           security:write-permission="cmf.ReviewPortalContent">
      <description></description>
      <required>False</required>
      <title>Room</title>
      <values>
        <element>101</element>
        <element>201</element>
        <element>Auditorium</element>
      </values>
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
```

```{seealso}
- <https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/dexterity-xml.html>
- <https://github.com/plone/plone.autoform/blob/master/plone/autoform/supermodel.txt>
```

### Exercise 1

Go to the ZMI and look for the definition of the new `Talk` content type in `portal_types`. Now deactivate {guilabel}`Implicitly addable?` and save. Go back to the site. Can you identify what this change has caused? And why is that useful?

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

Go to <http://localhost:8080/Plone/portal_types/talk/manage_propertiesForm>

When disabling *Implicitly addable* you can no longer add Talks any more unless you change some container like the type *Folder*: Enable *Filter contenttypes?* for it and add *Talk* to the items that are allowed.

With this method you can prevent content that only makes sense inside some defined structure to show up in places where they do not belong.

The equivalent setting for disabling {guilabel}`Implicitly addable` in {file}`Talk.xml` is:

```xml
<property name="global_allow">False</property>
```
````

## Summary

- You can now create new content-types and store them in a reproduceable way
- You installed the package to apply the Generic Setup configuration
- You learned how to read and modify the content type schema in xml
