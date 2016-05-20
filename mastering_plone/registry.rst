.. _registry-label:

Storing Settings in the Registry and create control-panels
==========================================================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout directory:

    .. code-block:: bash

        TODO

.. _eggs1-create-label:


In this part you will:

* Store a custom setting in a registry
* Create a controlpanel using z3c.form to allow setting that value


Topics covered:

* plone.app.registry
* controlpanels


The Registry
------------

The registry is used to get and set values stored in records. Each record contains the actual value, as well as a field that describes the record in more detail. It has a nice dict-like API.

All global settings in Plone 5 are stored in the registry.

The registry itself is provided by `plone.registry <https://pypi.python.org/pypi/plone.registry>`_ and the UI to interact with it by `plone.app.registry <https://pypi.python.org/pypi/plone.app.registry>`_

Almost all settings in ``/plone_control_panel`` are actually stored in the registry and can be modified using its UI directly.

Open http://localhost:8080/Plone/portal_registry and filter for ``displayed_types``. You see can modify the content types that should be shown in the navigation and site map. The values are the same as in http://localhost:8080/Plone/@@navigation-controlpanel but the later form is customized for usability.

A setting
---------

Let's store two values in the registry:

- The date of the conference
- Is talk submission open or closed

You cannot create values ttw, instead they need to be registered using Generic Setup.

Open the file ``profiles/default/registry.xml``. You already registered several new settings in there:

- You enabled self registration
- You stored a site-logo
- You registered additional criteria useable for Collections


Adding the following code to ``registry.xml`` creates a new value in the registry upon installation of the package.

..  code-block:: xml

    <record name="ploneconf.talk_submission_open">
        <field type="plone.registry.field.Bool">
            <title>Allow talk submission</title>
            <description>Allow the submission of talks for anonymous users</description>
            <required>False</required>
        </field>
        <value>False</value>
    </record>

When creating a new site a lot of settings are created in the same way. See https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/profiles/dependencies/registry.xml to see how ``Products.CMFPlone`` registers values.

..  code-block:: xml

  <record name="ploneconf.date_of_conference">
    <field type="plone.registry.field.Date">
        <title>First day of the conference</title>
        <required>False</required>
    </field>
    <value>2015-10-14</value>
  </record>


Accessing and modifying values in the registry
----------------------------------------------

In python you can access the registry like this:


..  code-block:: python

    from plone.registry.interfaces import IRegistry
    from zope.component import getUtility

    registry = getUtility(IRegistry)
    start = registry.get('ploneconf.date_of_conference')

``plone.api`` holds methods to make this even easier:

..  code-block:: python

    from plone import api
    api.portal.get_registry_record('ploneconf.date_of_conference')
    api.portal.set_registry_record('ploneconf.talk_submission_open', True)


Add a custom controlpanel
-------------------------

When you want to add a custom controlpanel it is usually more convenient to register the fields not manually like above but as field in a schema, similar to a content-types schema.

For this you define a interface for the schema and a view that auto-generates a form from the schema.

..  code-block:: xml

    <browser:page
        name="ploneconf-controlpanel"
        for="Products.CMFPlone.interfaces.IPloneSiteRoot"
        permission="cmf.ManagePortal"
        class=".controlpanel.PloneconfControlPanelView"
    />

Add a file ``controlpanel.py``:

..  code-block:: python

    # -*- coding: utf-8 -*-
    from datetime import date
    from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
    from plone.app.registry.browser.controlpanel import RegistryEditForm
    from plone.z3cform import layout
    from zope import schema
    from zope.interface import Interface


    class IPloneconfControlPanel(Interface):

        date_of_conference = schema.Date(
            title=u'First day of the conference',
            required=False,
            default=date(2015,10,14),
        )

        talk_submission_open = schema.Bool(
            title=u'Allow talk submission',
            description=u'Allow the submission of talks for anonymous user',
            default=False,
            required=False,
        )


    class PloneconfControlPanelForm(RegistryEditForm):
        schema = IPloneconfControlPanel
        schema_prefix = "ploneconf"
        label = u'Ploneconf Settings'


    PloneconfControlPanelView = layout.wrap_form(
        PloneconfControlPanelForm, ControlPanelFormWrapper)


With this way of using fields you don't have to register the values in ``registry.xml``, instead you have to register the interface:

..  code-block:: xml

    <records interface="ploneconf.site.controlpanel.IPloneconfControlPanel"
             prefix="ploneconf" />
