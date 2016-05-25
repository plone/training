.. _events-label:

Turning Talks into Events
=========================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/10_events_p5/ src/ploneconf.site


We forgot something: A list of talks is great especially if you can sort it by your preferences. But if a visitor decides he wants to actually go to see a talk he needs to know when it will take place.

We need a schedule and for this we need to store the information when a talk will happen.

Luckily the default type *Event* is based on reusable behaviors from the package plone.app.event.

In this chapter we will

* enable this behavior for talks
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

After we activate the behavior by hand or reinstalled the add-on we will now have some additional fields for ``start`` and ``end``.

To display the new field we reuse a default event summary view as documented in http://ploneappevent.readthedocs.org/en/latest/development.html#reusing-the-event-summary-view-to-list-basic-event-information

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


Exercise 1
++++++++++

Find out where ``event_summary`` comes from and describe how you could override it.

..  admonition:: Solution
    :class: toggle

    Use your editor or grep to search all zcml-files in the folder ``packages`` for the string ``name="event_summary"``

    ..  code-block:: bash

        $ grep -sirn --include \*.zcml 'name="event_summary"' ./packages
        ./plone/app/event/browser/configure.zcml:74:        name="event_summary"
        ./plone/app/event/browser/configure.zcml:83:        name="event_summary"

    The relevant registration is:

    ..  code-block:: xml

        <browser:page
          for="plone.event.interfaces.IEvent"
          name="event_summary"
          class=".event_summary.EventSummaryView"
          template="event_summary.pt"
          permission="zope2.View"
          layer="..interfaces.IBrowserLayer"
          />

    So there is a class ``plone.app.event.browser.event_summary.EventSummaryView`` and a template ``event_summary.pt`` that could be overridden with ``z3c.jbot`` by copying it as ``plone.app.event.browser.event_summary.pt`` in ``browser/overrides``.


Exercise 2
++++++++++

Find out where the event behavior is defined and which fields it offers.

..  admonition:: Solution
    :class: toggle

    The id with which the behavior is registered in ``Talk.xml`` is a python path. So ``plone.app.event.dx.behaviors.IEventBasic`` can be found in ``packages/plone.app.event/plone/app/event/dx/behaviors.py``

    ..  code-block:: python

        class IEventBasic(model.Schema, IDXEvent):
            """ Basic event schema.
            """
            start = schema.Datetime(
                title=_(
                    u'label_event_start',
                    default=u'Event Starts'
                ),
                description=_(
                    u'help_event_start',
                    default=u'Date and Time, when the event begins.'
                ),
                required=True,
                defaultFactory=default_start
            )

            end = schema.Datetime(
                title=_(
                    u'label_event_end',
                    default=u'Event Ends'
                ),
                description=_(
                    u'help_event_end',
                    default=u'Date and Time, when the event ends.'
                ),
                required=True,
                defaultFactory=default_end
            )

            whole_day = schema.Bool(
                title=_(
                    u'label_event_whole_day',
                    default=u'Whole Day'
                ),
                description=_(
                    u'help_event_whole_day',
                    default=u'Event lasts whole day.'
                ),
                required=False,
                default=False
            )

            open_end = schema.Bool(
                title=_(
                    u'label_event_open_end',
                    default=u'Open End'
                ),
                description=_(
                    u'help_event_open_end',
                    default=u"This event is open ended."
                ),
                required=False,
                default=False
            )

    Note how it uses ``defaultFactory`` to set an initial value.

