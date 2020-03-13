.. _dexterity1-label:

Dexterity II: Talk
==================

In this part you will:

* Create a new content type called *Talk*.


Topics covered:

* Schema
* Fields
* Widgets

The fti
-------

Add a file ``ploneconf/site/profiles/default/types/talk.xml``

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
     <property name="klass">ploneconf.site.content.talk.Talk</property>
     <property name="schema">ploneconf.site.content.talk.ITalk</property>
     <property name="behaviors">
      <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
      <element value="plone.app.content.interfaces.INameFromTitle"/>
      <element value="plone.app.versioningbehavior.behaviors.IVersionable" />
     </property>
     <property name="model_source"></property>
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


The type registration
---------------------

Add a file ``ploneconf/site/profiles/default/types.xml``:

..  code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_types" meta_type="Plone Types Tool">
     <object name="talk" meta_type="Dexterity FTI"/>
    </object>

The schema
----------

TODO:

* use a simplified schema without directives or vocabularies
* Then add some simple widget-directives
* In the sponsors-chapter discuss all fields, directives, permissions, defaults etc. like in dexterity_3
* extend to the final version like https://github.com/collective/ploneconf.site/pull/1/files#diff-943838c7d121f1043c9db05635b96930 in a later chapter

..  code-block:: python

    # -*- coding: utf-8 -*-
    from plone.app.textfield import RichText
    from plone.autoform import directives
    from plone.dexterity.content import Container
    from plone.namedfile.field import NamedBlobImage
    from plone.schema.email import Email
    from plone.supermodel import model
    from ploneconf.site import _
    from z3c.form.browser.checkbox import CheckBoxFieldWidget
    from z3c.form.browser.radio import RadioFieldWidget
    from zope import schema
    from zope.interface import implementer
    from zope.schema.vocabulary import SimpleTerm
    from zope.schema.vocabulary import SimpleVocabulary


    class ITalk(model.Schema):
        """Dexterity-Schema for Talks"""

        directives.widget(type_of_talk=RadioFieldWidget)
        type_of_talk = schema.Choice(
            title=_(u'Type of talk'),
            values=['Talk', 'Training', 'Keynote'],
            required=True,
            )

        details = RichText(
            title=_(u'Details'),
            description=_(u'Description of the talk (max. 2000 characters)'),
            max_length=2000,
            required=True,
            )

        directives.widget(audience=CheckBoxFieldWidget)
        audience = schema.Set(
            title=_(u'Audience'),
            value_type=schema.Choice(
                values=['Beginner', 'Advanced', 'Professionals'],
                ),
            required=False,
            )

        speaker = schema.TextLine(
            title=_(u'Speaker'),
            description=_(u'Name (or names) of the speaker'),
            required=False,
            )

        company = schema.TextLine(
            title=_(u'Company'),
            required=False,
            )

        email = Email(
            title=_(u'Email'),
            description=_(u'Email adress of the speaker'),
            required=False,
            )

        website = schema.TextLine(
            title=_(u'Website'),
            required=False,
            )

        twitter = schema.TextLine(
            title=_(u'Twitter name'),
            required=False,
            )

        github = schema.TextLine(
            title=_(u'Github username'),
            required=False,
            )

        image = NamedBlobImage(
            title=_(u'Image'),
            description=_(u'Portrait of the speaker'),
            required=False,
            )

        speaker_biography = RichText(
            title=_(u'Speaker Biography (max. 1000 characters)'),
            max_length=1000,
            required=False,
            )


    @implementer(ITalk)
    class Talk(Container):
        """Talk instance class"""


The instance class
------------------

.. todo::

    Discuss instance class


.. seealso::

   * `Dexterity Developer Manual <https://docs.plone.org/external/plone.app.dexterity/docs/index.html>`_
   * `The standard behaviors <https://docs.plone.org/external/plone.app.dexterity/docs/reference/standard-behaviours.html>`_
