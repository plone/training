Turn talks into events
======================

We forgot something: A list of talks is great especially if you can sort it by your preferences. But if a visitor decides he wants to see a talk he needs to know when it will take place.

We need a schedule and for this we need to store the information when a talk will happen.

Luckily the type *Event* is based on reuseable behaviors from the package plone.app.event.

In this chapter we will

* enable this behavior for talks
* write an upgrade step to work around a bug in plone.app.event
* display the date in the talkview

First we enable the behavior ``IEventBasic`` for talks in ``profiles/default/types/talk.xml``

.. code-block:: xml
    :linenos:
    :emphasize-lines: 6

    <property name="behaviors">
      <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
      <element value="plone.app.content.interfaces.INameFromTitle"/>
      <element value="ploneconf.site.behavior.social.ISocial"/>
      <element value="ploneconf.site.interfaces.ITalk"/>
      <element value="plone.app.event.dx.behaviors.IEventBasic"/>
    </property>

If we set the behavior by hand or reinstall the addon we could now add new talks with new field for ``start`` and ``end``.

But because of a `bug in plone.app.event <https://github.com/plone/plone.app.event/issues/160>`_  does not expect existing objects to get the behavior. Since existing types have no values in the fields ``start`` and ``end`` we would get a traceback on inline-validation when we edit these. To work around this we create an upgrade-step that sets some an initial date.

Register the new upgrade step in ``upgrades.zcml``

.. code-block:: xml
    :linenos:

    <genericsetup:upgradeStep
      title="Add event-behavior to talks"
      description=""
      source="1001"
      destination="1002"
      handler="ploneconf.site.upgrades.turn_talks_to_events"
      sortkey="1"
      profile="ploneconf.site:default"
      />

Bump the profile-version to 1002 in ``profiles/default/metadata.xml``

Write the upgrade-step in ``upgrades.py``

.. code-block:: python
    :linenos:
    :emphasize-lines: 4, 6, 39-59

    # -*- coding: UTF-8 -*-
    from plone import api

    import datetime
    import logging
    import pytz


    default_profile = 'profile-ploneconf.site:default'

    logger = logging.getLogger('ploneconf.site')


    def upgrade_site(self):
        self.runImportStepFromProfile(default_profile, 'typeinfo')
        catalog = api.portal.get_tool('portal_catalog')
        portal = api.portal.get()
        if 'talks' not in portal:
            talks = api.content.create(
                container=portal,
                type='Folder',
                id='talks',
                title='Talks')
        else:
            talks = portal['talks']
        talks_url = talks.absolute_url()
        brains = catalog(portal_type='talk')
        for brain in brains:
            if talks_url in brain.getURL():
                continue
            obj = brain.getObject()
            logger.info('Moving %s' % obj.absolute_url())
            api.content.move(
                source=obj,
                target=talks,
                safe_id=True)


    def turn_talks_to_events(self):
        """Set a start- and end-date for old events to work around a
        bug in plone.app.event 1.1.1
        """
        api.portal.set_registry_record(
            'plone.app.event.portal_timezone',
            'Europe/London')
        self.runImportStepFromProfile(default_profile, 'typeinfo')

        tz = pytz.timezone("Europe/London")
        now = tz.localize(datetime.datetime.now())
        date = now + datetime.timedelta(days=30)
        date = date.replace(minute=0, second=0, microsecond=0)

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='talk')
        for brain in brains:
            obj = brain.getObject()
            if not getattr(obj, 'start', False):
                obj.start = obj.end = date
                obj.timezone = "Europe/London"

After we ran the upgrade-step we can now add a time to existing events. To display this we reuse a default event-summary view as documented in http://ploneappevent.readthedocs.org/en/latest/development.html#reusing-the-event-summary-view-to-list-basic-event-information

Edit ``browser/templates/talkview.pt``

.. code-block:: html
    :linenos:
    :emphasize-lines: 7

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="ploneconf.site">
    <body>
        <metal:content-core fill-slot="content-core" tal:define="widgets view/w">

            <tal:eventsummary replace="structure context/@@event_summary"/>

            <p>
                <span tal:content="context/type_of_talk">
                    Talk
                </span>
                suitable for
                <span tal:replace="structure widgets/audience/render">
                    Audience
                </span>
            </p>

            <div tal:content="structure widgets/details/render">
                Details
            </div>

            <div class="newsImageContainer">
                <img tal:condition="python:getattr(context, 'image', None)"
                     tal:attributes="src string:${context/absolute_url}/@@images/image/thumb" />
            </div>

            <div>
                <a class="email-link" tal:attributes="href string:mailto:${context/email}">
                    <strong tal:content="context/speaker">
                        Jane Doe
                    </strong>
                </a>
                <div tal:content="structure widgets/speaker_biography/render">
                    Biography
                </div>
            </div>

        </metal:content-core>
    </body>
    </html>
