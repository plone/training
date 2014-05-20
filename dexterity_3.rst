Dexterity Types III: Python
===========================

Without sponsors a conference would be hard to finance plus it is a good opportunity for plone-companies to advertise their services.

In this part we will:

* create the content-type *sponsor* that has a python-schema
* create a viewlet that shows the sponsors sorted by level
* discuss image-scales


Create a new file ``content/sponsor.py``.

.. code-block:: python
    :linenos:

    # -*- coding: UTF-8 -*-
    from plone.app.textfield import RichText
    from plone.autoform import directives
    from plone.namedfile import field as namedfile
    from plone.supermodel.directives import fieldset
    from plone.supermodel.model import Schema
    from z3c.form.browser.radio import RadioFieldWidget
    from zope import schema
    from zope.schema.vocabulary import SimpleVocabulary
    from zope.schema.vocabulary import SimpleTerm

    from ploneconf.site import MessageFactory as _


    LevelVocabulary = SimpleVocabulary(
        [SimpleTerm(value=u'platinum', title=_(u'Platinum Sponsor')),
         SimpleTerm(value=u'gold', title=_(u'Gold Sponsor')),
         SimpleTerm(value=u'silver', title=_(u'Silver Sponsor')),
         SimpleTerm(value=u'bronze', title=_(u'Bronze Sponsor'))]
        )


    class ISponsor(Schema):
        """Dexterity-Schema for Sponsors
        """

        directives.widget(level=RadioFieldWidget)
        level = schema.Choice(
            title=_(u"Sponsoring Level"),
            vocabulary=LevelVocabulary,
            required=True
        )

        text = RichText(
            title=_(u"Text"),
            required=False
        )

        url = schema.URI(
            title=_(u"Link"),
            required=False
        )

        fieldset('Images', fields=['logo', 'advertisment'])
        logo = namedfile.NamedBlobImage(
            title=_(u"Logo"),
            required=False,
        )

        advertisment = namedfile.NamedBlobImage(
            title=_(u"Advertisment (Gold-sponsors and above)"),
            required=False,
        )

        directives.read_permission(notes="cmf.AddPortalMember")
        directives.write_permission(notes="cmf.AddPortalMember")
        notes = RichText(
            title=_(u"Secret Notes (only for site-admins)"),
            required=False
        )


Register the new type in ``profiles/default/types/sponsor.xml``

.. code-block:: xml
    :linenos:
    :emphasize-lines: 27

    <?xml version="1.0"?>
    <object name="sponsor" meta_type="Dexterity FTI" i18n:domain="plone"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n">
     <property name="title" i18n:translate="">Sponsor</property>
     <property name="description" i18n:translate="">None</property>
     <property name="icon_expr">string:${portal_url}/document_icon.png</property>
     <property name="factory">sponsor</property>
     <property name="add_view_expr">string:${folder_url}/++add++sponsor</property>
     <property name="link_target"></property>
     <property name="immediate_view">view</property>
     <property name="global_allow">True</property>
     <property name="filter_content_types">True</property>
     <property name="allowed_content_types"/>
     <property name="allow_discussion">False</property>
     <property name="default_view">sponsorview</property>
     <property name="view_methods">
      <element value="view"/>
      <element value="sponsor"/>
     </property>
     <property name="default_view_fallback">False</property>
     <property name="add_permission">cmf.AddPortalContent</property>
     <property name="klass">plone.dexterity.content.Container</property>
     <property name="behaviors">
      <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
      <element value="plone.app.content.interfaces.INameFromTitle"/>
     </property>
     <property name="schema">ploneconf.site.content.sponsor.ISponsor</property>
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
