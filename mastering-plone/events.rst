.. _events-label:

Turning Talks into Events
=========================

.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

       git checkout dexterity_2

   Code for the end of this chapter::

        git checkout events


We forgot something: a list of talks is great, especially if you can sort it according to your preferences. But if a visitor decides she wants to actually go to see a talk she needs to know when it will take place.

We need a schedule and for this we need to store the information when a talk will happen.

Luckily the default type *Event* is based on reusable behaviors from the package :py:mod:`plone.app.event` that we can reuse.

In this chapter you will

* enable this behavior for talks
* display the date in the talkview and talklistview


Add date fields
---------------

Instead of adding Datetime-fields to the talk schema we will use the behavior ``plone.eventbasic``.

Enable the behavior ``plone.eventbasic`` for talks in :file:`profiles/default/types/talk.xml`.

.. code-block:: xml
    :linenos:
    :emphasize-lines: 6

    <property name="behaviors">
      <element value="plone.dublincore"/>
      <element value="plone.namefromtitle"/>
      <element value="plone.versioning"/>
      <element value="ploneconf.featured"/>
      <element value="plone.eventbasic"/>
    </property>

After you activate the behavior by hand or you reinstalled the add-on you will now have some additional fields for ``start``, ``end``, ``open_end`` and ``whole_day``.

Display the dates
-----------------

Now we need to update the event view to show this information.

Unfortuanely displaying dates and times is not as simple as it might sound since we'd have to account for diffrent use cases that all look diffrent:

Here are some examples how dates might be displayed if they are full-day events, open-ended events or events with a defined end-time.

* Apr 22, 2020 from 3:00 PM to 5:00 PM
* Apr 22, 2020
* Apr 22, 2020 7:00 PM
* Apr 22, 2020 to Apr 24, 2020
* Apr 22, 2020 7:00 PM to Apr 29, 2020 8:00 PM

Now consider that dates are displayed different in other languages and it really gets compicated.

So it would be a good idea to reuse a component that already deals with these use-cases.
Since we use the same behavior that the default content type Event in Plone uses the default event-view might have what we need.

Add a event und use the React Developer Tools to inspect the component that displays the date.
It is called ``When`` and is defined in ``frontend/node_modules/@plone/volto/src/components/theme/View/EventDatesInfo.jsx``.

We'll reuse it in :file:`frontend/src/components/Views/Talk.jsx`:

.. code-block:: js

    <When
      start={content.start}
      end={content.end}
      whole_day={content.whole_day}
      open_end={content.open_end}
    />

We'll let us inspire by the event-view and add a ``<Segment floated="right">`` that will contain the date but also the room and the audience.
In this box we will also use ``<Header dividing sub>`` (from `seamantic-ui <https://react.semantic-ui.com/elements/header/#types-subheaders>`_ to separate the data.

.. code-block:: js
    :emphasize-lines: 5,12,29-65

    import React from 'react';
    import { flattenToAppURL } from '@plone/volto/helpers';
    import {
      Container,
      Header,
      Image,
      Icon,
      Label,
      Segment,
    } from 'semantic-ui-react';
    import { Helmet } from '@plone/volto/helpers';
    import { When } from '@plone/volto/components/theme/View/EventDatesInfo';

    const TalkView = props => {
      const { content } = props;
      const color_mapping = {
        Beginner: 'green',
        Advanced: 'yellow',
        Professional: 'red',
      };

      return (
        <Container id="page-talk">
          <Helmet title={content.title} />
          <h1 className="documentFirstHeading">
            {content.type_of_talk.title || content.type_of_talk.token}:{' '}
            {content.title}
          </h1>
          <Segment floated="right">
            {content.start && !content.hide_date && (
              <>
                <Header dividing sub>
                  When
                </Header>
                <When
                  start={content.start}
                  end={content.end}
                  whole_day={content.whole_day}
                  open_end={content.open_end}
                />
              </>
            )}
            {content.room && (
              <>
                <Header dividing sub>
                  Where
                </Header>
                <p>{content.room.title}</p>
              </>
            )}
            {content.audience && (
              <Header dividing sub>
                Audience
              </Header>
            )}
            {content.audience.map(item => {
              let audience = item.title || item.token;
              let color = color_mapping[audience] || 'green';
              return (
                <Label key={audience} color={color}>
                  {audience}
                </Label>
              );
            })}
          </Segment>
          {content.description && (
            <p className="documentDescription">{content.description}</p>
          )}
          {content.details && (
            <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
          )}
          {content.speaker && (
            <Segment clearing>
              <Header dividing>{content.speaker}</Header>
              {content.website ? (
                <p>
                  <a href={content.website}>{content.company}</a>
                </p>
              ) : (
                <p>{content.company}</p>
              )}
              {content.email && (
                <p>
                  <a href={`mailto:${content.email}`}>
                    <Icon name="mail" /> {content.email}
                  </a>
                </p>
              )}
              {content.twitter && (
                <p>
                  <a href={`https://twitter.com/${content.twitter}`}>
                    <Icon name="twitter" />{' '}
                    {content.twitter.startsWith('@')
                      ? content.twitter
                      : '@' + content.twitter}
                  </a>
                </p>
              )}
              {content.github && (
                <p>
                  <a href={`https://github.com/${content.github}`}>
                    <Icon name="github" /> {content.github}
                  </a>
                </p>
              )}
              {content.image && (
                <Image
                  src={flattenToAppURL(content.image.scales.preview.download)}
                  size="small"
                  floated="right"
                  alt={content.image_caption}
                  avatar
                />
              )}
              {content.speaker_biography && (
                <div
                  dangerouslySetInnerHTML={{
                    __html: content.speaker_biography.data,
                  }}
                />
              )}
            </Segment>
          )}
        </Container>
      );
    };
    export default TalkView;

The result should look like this:

.. figure:: _static/event_view_volto.png


Hiding fields from certain users
--------------------------------

Similar to the field ``room``, the problem now appears that speakers submitting their talks should not be able to set a time and day for their talks.

Sadly it is not easy to modify permissions of fields provided by behaviors (unless you write the behavior yourself).
At least in this case we can take the easy way out since the field does not contain secret information: we will simply hide the fields from contributors using css and show them for reviewers. We will do so in chapter :ref:`resources-label` when we add some CSS files.

Modify :file:`frontend/theme/extras/custom.overrides` and add:

.. code-block:: less

    // Hide date fields from contributors
    body.userrole-contributor {
      #default-start.field,
      #default-end.field,
      #default-whole_day.field,
      #default-open_end.field {
        display: none;
      }
    }

    body.userrole-reviewer {
      #default-start.field,
      #default-end.field,
      #default-whole_day.field,
      #default-open_end.field {
        display: block;
      }
    }


Display the date in the listing
-------------------------------

.. todo::

  Adapt ``TalkListView`` to handle the date and time.


Exercise 1
++++++++++

Find out where ``event_summary`` comes from and describe how you could override it.

..  admonition:: Solution
    :class: toggle

    Use your edit


Exercise
++++++++

Find out where the event behavior is defined and which fields it offers.

..  admonition:: Solution
    :class: toggle

    The name you used to enable the behavior :file:`Talk.xml` is registered in zcml.
    So ``name="plone.eventbasic"`` should be easy to find.
    You will find it in :file:`backend/packages/plone/app/event/dx/configure.zcml` and it points to ``IEventBasic`` in :file:`packages/plone.app.event/plone/app/event/dx/behaviors.py`

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
            directives.widget(
                'start',
                DatetimeFieldWidget,
                default_timezone=default_timezone,
                klass=u'event_start'
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
            directives.widget(
                'end',
                DatetimeFieldWidget,
                default_timezone=default_timezone,
                klass=u'event_end'
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
            directives.widget(
                'whole_day',
                SingleCheckBoxFieldWidget,
                klass=u'event_whole_day'
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
            directives.widget(
                'open_end',
                SingleCheckBoxFieldWidget,
                klass=u'event_open_end'
            )

    Note how it uses ``defaultFactory`` to set an initial value.

Summary
-------

* You reused a existing behavior to add new fields
* You reused a existing component to display the date
* You did not have to write your own datetime fields and indexers \o/

.. note::

    To meet the same requirements in classic Plone see the chapter :doc:`events_classic`
