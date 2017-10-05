.. _behaviors1-label:

Behaviors
=========

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <code>`):

    ..  code-block:: bash

        git checkout behaviors_1

In this part you will:

* Add another field to talks by using a behavior

Topics covered:

* Behaviors


.. only:: not presentation

    You can extend the functionality of your dexterity object by writing an adapter that adapts your dexterity object to add another feature or aspect.

    But if you want to use this adapter, you must somehow know that an object implements that. Also, adding more fields to an object would not be easy with such an approach.

.. _behaviors1-dexterity-label:

Dexterity Approach
------------------

.. only:: not presentation

    Dexterity has a solution for it, with special adapters that are called and registered by the name behavior.

    A behavior can be added to any content type through the web and at runtime.

    All default views (e.g. the add- and edit-forms) know about the concept of behaviors and when rendering forms, the views also check whether there are behaviors referenced with the current context and if these behaviors have a schema of their own, these fields get shown in addition.

.. _behaviors1-names-label:

Names and Theory
----------------

.. only:: not presentation

    The name behavior is not a standard term in software development. But it is a good idea to think of a behavior as an aspect. You are adding an aspect to your content type and you want to write your aspect in such a way that it works independently of the content type on which the aspect is applied. You should not have dependencies to specific fields of your object or to other behaviors.

    Such an object allows you to apply the `Open/closed principle`_ to your dexterity objects.

.. only:: presentation

    `Open/closed principle`_

.. _Open/closed principle: https://en.wikipedia.org/wiki/Open/closed_principle

.. _behaviors1-example-label:

Practical example
-----------------

.. only:: not presentation

    So, let us write our own small behavior.

    In the future, we want our presentation to be represented in Lanyrd (a Social Conference Directory - Lanyrd.com) too. For now we will just provide a link so that visitors can collaborate easily with the Lanyrd site.

    So for now, our behavior just adds a new field for storing the url to Lanyrd.

We want to keep a clean structure, so we create a :file:`behaviors` directory first, and include it into the zcml declarations of our :file:`configure.zcml`.

.. code-block:: xml

    <include package=".behaviors" />

Then, we add an empty :file:`behaviors/__init__.py` and a :file:`behaviors/configure.zcml` containing

.. only:: not presentation

    .. sidebar:: Advanced reference

        It can be a bit confusing when to use factories or marker interfaces and when not to.

        If you do not define a factory, your attributes will be stored directly on the object. This can result in clashes with other behaviors.

        You can avoid this by using the :py:class:`plone.behavior.AnnotationStorage` factory. This stores your attributes in an :ref:`Annotation <plone:annotations>`.
        But then you *must* use a marker interface if you want to have custom viewlets, browser views or portlets.

        Without it, you would have no interface against which you could register your views.

.. _social-behavior-zcml-label:

.. code-block:: xml
    :linenos:
    :emphasize-lines: 6-10

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

And a :file:`behaviors/social.py` containing:

.. _social-behavior-python-label:

.. code-block:: python
    :linenos:

    # -*- coding: utf-8 -*-
    from plone.autoform.interfaces import IFormFieldProvider
    from plone.supermodel import directives
    from plone.supermodel import model
    from zope import schema
    from zope.interface import alsoProvides


    class ISocial(model.Schema):

        directives.fieldset(
            'social',
            label=u'Social',
            fields=('lanyrd',),
        )

        lanyrd = schema.URI(
            title=u"Lanyrd link",
            description=u"Add URL",
            required=False,
        )

    alsoProvides(ISocial, IFormFieldProvider)

.. only:: not presentation

    Let's go through this step by step.

    #. We register a behavior in :ref:`behaviors/configure.zcml <social-behavior-zcml-label>`. We do not say for which content type this behavior is valid. You do this through the web or in the GenericSetup profile.
    #. We create a marker interface in :ref:`behaviors/social.py <social-behavior-python-label>` for our behavior and make it also a schema containing the fields we want to declare.
       We could just define schema fields on a zope.interface class, but we use an extended form from `plone.supermodel`_, else we could not use the fieldset features.
    #. We also add a `fieldset`_ so that our fields are not mixed with the normal fields of the object.
    #. We add a normal `URI`_ schema field to store the URI to lanyrd.
    #. We mark our schema as a class that also implements the `IFormFieldProvider`_ interface. This is a marker interface, we do not need to implement anything to provide the interface.

.. _behaviors1-adding-label:

Adding it to our talk
---------------------

.. only:: not presentation

    We could add this behavior now via the plone control panel. But instead, we will do it directly and properly in our GenericSetup profile

We must add the behavior to :file:`profiles/default/types/talk.xml`:

.. code-block:: xml
    :linenos:
    :emphasize-lines: 8

    <?xml version="1.0"?>
    <object name="talk" meta_type="Dexterity FTI" i18n:domain="plone"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n">
       ...
     <property name="behaviors">
      <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
      <element value="plone.app.content.interfaces.INameFromTitle"/>
      <element value="ploneconf.site.behaviors.social.ISocial"/>
     </property>
     ...
    </object>


.. _plone.supermodel: https://docs.plone.org/external/plone.app.dexterity/docs/schema-driven-types.html#schema-interfaces-vs-other-interfaces
.. _fieldset: https://docs.plone.org/develop/addons/schema-driven-forms/customising-form-behaviour/fieldsets.html?highlight=fieldset
.. _IFormFieldProvider: https://docs.plone.org/external/plone.app.dexterity/docs/advanced/custom-add-and-edit-forms.html?highlight=iformfieldprovider#edit-forms
.. _URI: http://docs.zope.org/zope.schema/fields.html#uri
