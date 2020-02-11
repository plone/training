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

The type registration
---------------------

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
    from plone.namedfile.field import NamedBlobImage
    from plone.schema.email import Email
    from plone.supermodel import model
    from ploneconf.site import _
    from z3c.form.browser.checkbox import CheckBoxFieldWidget
    from z3c.form.browser.radio import RadioFieldWidget
    from zope import schema


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
            values=['Beginner', 'Advanced', 'Professionals'],
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


The instance class
------------------





.. seealso::

   * `Dexterity Developer Manual <https://docs.plone.org/external/plone.app.dexterity/docs/index.html>`_
   * `The standard behaviors <https://docs.plone.org/external/plone.app.dexterity/docs/reference/standard-behaviours.html>`_
