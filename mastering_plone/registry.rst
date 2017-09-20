.. _registry-label:

Manage Settings with Registry, Controlpanels and Vocabularies
=============================================================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <code>`):

    ..  code-block:: bash

        git checkout registry


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

Open the file :file:`profiles/default/registry.xml`. You already registered several new settings in there:

- You enabled self registration
- You stored a site-logo
- You registered additional criteria useable for Collections


Adding the following code to :file:`registry.xml`. This creates a new value in the registry upon installation of the package.

..  code-block:: xml

    <record name="ploneconf.talk_submission_open">
      <field type="plone.registry.field.Bool">
        <title>Allow talk submission</title>
        <description>Allow the submission of talks for anonymous users</description>
        <required>False</required>
      </field>
      <value>False</value>
    </record>

When creating a new site a lot of settings are created in the same way. See https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/profiles/dependencies/registry.xml to see how :py:mod:`Products.CMFPlone` registers values.

..  code-block:: xml

    <record name="ploneconf.date_of_conference">
      <field type="plone.registry.field.Date">
        <title>First day of the conference</title>
        <required>False</required>
      </field>
      <value>2016-10-17</value>
    </record>


Accessing and modifying values in the registry
----------------------------------------------

In python you can access the registry like this:


..  code-block:: python

    from plone.registry.interfaces import IRegistry
    from zope.component import getUtility

    registry = getUtility(IRegistry)
    start = registry.get('ploneconf.date_of_conference')

:py:mod:`plone.api` holds methods to make this even easier:

..  code-block:: python

    from plone import api
    api.portal.get_registry_record('ploneconf.date_of_conference')
    api.portal.set_registry_record('ploneconf.talk_submission_open', True)


Add a custom controlpanel
-------------------------

When you want to add a custom controlpanel it is usually more convenient to register the fields not manually like above but as field in a schema, similar to a content-types schema.

For this you define a interface for the schema and a view that auto-generates a form from the schema. In :file:`browser/configure.zcml` add:

..  code-block:: xml

    <browser:page
        name="ploneconf-controlpanel"
        for="Products.CMFPlone.interfaces.IPloneSiteRoot"
        class=".controlpanel.PloneconfControlPanelView"
        permission="cmf.ManagePortal"
        />

Add a file :file:`browser/controlpanel.py`:

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
            default=date(2016, 10, 17),
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


With this way of using fields you don't have to register the values in :file:`registry.xml`, instead you have to register the interface:

..  code-block:: xml

    <records interface="ploneconf.site.browser.controlpanel.IPloneconfControlPanel"
             prefix="ploneconf" />

After reinstalling the package (to load the registry-entry) you can access the controlpanel at http://localhost:8080/Plone/@@ploneconf-controlpanel.

To make it show up in the general controlpanel at http://localhost:8080/Plone/@@overview-controlpanel you have to register it with GenericSetup.
Add a file :file:`profiles/default/controlpanel.xml`:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_controlpanel">
      <configlet
          title="Ploneconf Settings"
          action_id="ploneconf-controlpanel"
          appId="ploneconf-controlpanel"
          category="Products"
          condition_expr=""
          icon_expr=""
          url_expr="string:${portal_url}/@@ploneconf-controlpanel"
          visible="True">
        <permission>Manage portal</permission>
      </configlet>
    </object>

Again, after applying the profile (reinstall the package or write a upgrade-step) your controlpanel shows up in http://localhost:8080/Plone/@@overview-controlpanel.


Vocabularies
------------

Do you remember the field `rooms`? We provided several options to chose from.
But who says that the next conference will have the same rooms?
These values should be configurable by the admin.
The admin could go to the dexterity-controlpanel and change the values but we will use a different approach.
We will allow the rooms to be added in the controlpanel and use these values in the talk-schema by registering a vocabulary.

Add a new field to :py:class:`IPloneconfControlPanel`:

.. code-block:: python
   :linenos:

    rooms = schema.Tuple(
        title=u'Available Rooms for the conference',
        default=(u'101', u'201', u'Auditorium'),
        missing_value=None,
        required=False,
        value_type=schema.TextLine()
    )

Create a file :file:`vocabularies.py` and write the vocabulary:

.. code-block:: python
   :linenos:

    # -*- coding: utf-8 -*-
    from plone import api
    from plone.i18n.normalizer.interfaces import IIDNormalizer
    from zope.component import queryUtility
    from zope.interface import implementer
    from zope.schema.interfaces import IVocabularyFactory
    from zope.schema.vocabulary import SimpleVocabulary

    @implementer(IVocabularyFactory)
    class RoomsVocabularyFactory(object):

        def __call__(self, context):
            values = api.portal.get_registry_record('ploneconf.rooms')
            normalizer = queryUtility(IIDNormalizer)
            items = [(normalizer.normalize(i), i) for i in values]
            return SimpleVocabulary.fromItems(items)

    RoomsVocabulary = RoomsVocabularyFactory()


Note:

* `RoomsVocabulary` is a instance of :py:class:`RoomsVocabularyFactory`.
* We normalize values to create a vocabulary since the value of a SimpleVocabulary has to be ASCII. We use one of many useful normalizers that Plone provides.

Register a vocabulary in :file:`configure.zcml` as `ploneconf.site.vocabularies.Rooms`:

.. code-block:: xml

    <utility
        name="ploneconf.site.vocabularies.Rooms"
        component="ploneconf.site.vocabularies.RoomsVocabulary" />

Use the vocabulary in the talk-schema. Edit :file:`content/talk.xml`

.. code-block:: xml
   :linenos:
   :emphasize-lines: 7

    <field name="room"
           type="zope.schema.Choice"
           form:widget="z3c.form.browser.radio.RadioFieldWidget"
           security:write-permission="cmf.ReviewPortalContent">
      <description></description>
      <title>Room</title>
      <vocabulary>ploneconf.site.vocabularies.Rooms</vocabulary>
    </field>

Now a admin can configure the rooms available for the conference. We could use the same pattern for the fields `type_of_talk` and `audience`.

.. seealso::

  https://docs.plone.org/external/plone.app.dexterity/docs/advanced/vocabularies.html

.. note::

    In a python-schema that would look like this:

    .. code-block:: python

        directives.widget(room=RadioFieldWidget)
        room = schema.Choice(
            title=_(u'Room'),
            vocabulary='ploneconf.site.vocabularies.Rooms',
            required=False,
        )
