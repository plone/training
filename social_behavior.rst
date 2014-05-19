Social behavior
===============

You can extend the functionality of your dexterity object by writing an adapter that adapts your dexterity object to add another feature or aspect.

But if you want to use this adapter, you must somehow know that an object implements that. Also, you could not easily add more fields to an object with such an approach.

Dexterity Approach
------------------

Dexterity has a solution for it, with special adapters that are called and registered by the name behavior.

A behavior can be added to any content type through the web and during runtime.

All default views know about the concept of behaviors and when rendering forms, the views also check whether there are behaviors referenced with the current context and if these behavior have a schema of their own, these fields get shown in addition.

This this functionality in place, you can extend your content types during runtime, through the web.

Names and Theory
----------------

The name behavior is not a standard term in the software development. But it is a good idea to think of a behavior as an aspect. You are adding an aspect to your content type, you want to write your aspect in such a way, that it works independent of the content type on which the aspect is applied. You should not have dependencies to specific fields of your object or to other behaviors.

Such an object allows you to apply the `Open/closed principle`_ to your dexterity objects.

.. _Open/closed principle: https://en.wikipedia.org/wiki/Open/closed_principle

Practical example
-----------------

So, let us write our own small behavior.

In the future, we want our presentation be represented in Lanyrd too. For now we will just provide a link so that visitors can collaborate easily with the lanyrd site.

So for now, our behavior just adds a new field for storing the url to Lanyrd.

We want to keep a clean structure, so we create a behavior directory first, and include it into the zcml declarations.

.. code-block:: xml

    <include package=".behavior" />

Then, we add an empty ``__init__.py`` and a ``configure.zcml`` containing

.. sidebar:: Advanced reference

    The original documentation is doctest code, so no documentation and no debuggable test.

    It can be a bit confusing of when to use factory, or marker interfaces and when not.

    If you do not define a factory, your attributes will be stored directly on the object. This can result in clashes with other behaviors.

    You can avoid this by using the plone.behavior.AnnotationStorage factory. This one stores your attributes in an :ref:`Annotation <plone:annotations>`.
    But then you *must* use a marker interface if you want to have custom viewlets, browser views or portlets.

    Without it, you would have no interface against which you could register your views.



.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="ploneconf.site">

      <plone:behavior
          title="Social Behavior"
          description="Adds a link to lanyrd"
          provides=".social.ISocial"
          />

    </configure>

And a ``social.py`` containing::

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

Lets get through this step by step.

First, we register a behavior. We do not say for which content type this behavior is valid. You do this, through the web or in the GenericSetup profile.


