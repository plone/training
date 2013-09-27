Social behavior
===============

Now let's write our own small behavior. This thime we don't add a lot of logic but only a additional field:

* link to lanyrd-site for the talk

We register a folder called behavior in our configure.zcml

.. code-block:: xml

    <include package=".behavior" />

We add an empty __init__.py and a configute.czml containing

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="plonekonf.talk">

      <include package="plone.behavior" file="meta.zcml" />

      <include package="plone.directives.form" file="meta.zcml" />
      <include package="plone.directives.form" />

      <plone:behavior
          title="Social Behavior"
          description="Adds a link to lanyrd"
          provides=".social.ISocial"
          />

    </configure>

And a social.py containing::

    # -*- coding: utf-8 -*-
    from plone.directives import form
    from zope import schema
    from zope.interface import alsoProvides

    class ISocial(form.Schema):

        form.fieldset(
                'social',
                label=u'Social',
                fields=('lanyrd',),
            )

        lanyrd = schema.URI(
                title=u"Lanyrd-link",
                description=u"Add URL",
                required=False,
            )

    alsoProvides(ISocial, form.IFormFieldProvider)

* explain

TAG: 16_SOCIAL_BEHAVIOR

