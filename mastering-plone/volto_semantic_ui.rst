.. _volto_semantic_ui-label:

Semantic UI
============

.. sidebar:: Volto chapter

  .. figure:: _static/Volto.svg
     :alt: Volto Logo

  This chapter is about the react frontent Volto.

  Learn about templates in the classic frontend in chapter :doc:`zpt`

Semantic is a development framework that helps create beautiful, responsive layouts using human-friendly HTML. It provides a declarative API, shorthand props and many helpers that simplifies development.

Volto uses the components from `Semantic UI React <https://react.semantic-ui.com/>`_ to compose a large part of the views. For example the component `Image <https://react.semantic-ui.com/elements/image/>`_ is used to render images.

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 14-18

    /**
     * EventView view component class.
     * @function EventView
     * @params {object} content Content object.
     * @returns {string} Markup of the component.
     */
    const EventView = ({ content }) => (
      <Container className="view-wrapper event-view">
        {content.title && <h1 className="documentFirstHeading">{content.title}</h1>}
        {content.description && (
          <p className="documentDescription">{content.description}</p>
        )}
        {content.image && (
          <Image
            className="document-image"
            src={content.image.scales.thumb.download}
            floated="right"
          />
        )}
        <Segment floated="right">
          {/* TODO I18N INTL */}
          {content.subjects.length > 0 && (
            <>
              <Header dividing sub>
                What
              </Header>
              <List items={content.subjects} />
            </>
          )}
          <Header dividing sub>
            When
          </Header>
          <When
            start={content.start}
            end={content.end}
            whole_day={content.whole_day}
            open_end={content.open_end}
          />
          {content.recurrence && (
            <>
              <Header dividing sub>
                All dates
              </Header>
              <Recurrence recurrence={content.recurrence} start={content.start} />
            </>
          )}
          {content.location && (
            <>
              <Header dividing sub>
                Where
              </Header>
              <p>{content.location}</p>
            </>
          )}
          {content.contact_name && (
            <>
              <Header dividing sub>
                Contact Name
              </Header>
              <p>
                {content.contact_email ? (
                  <a href={`mailto:${content.contact_email}`}>
                    {content.contact_name}
                  </a>
                ) : (
                  content.contact_name
                )}
              </p>
            </>
          )}
          {content.contact_phone && (
            <>
              <Header dividing sub>
                Contact Phone
              </Header>
              <p>{content.contact_phone}</p>
            </>
          )}
          {content.attendees.length > 0 && (
            <>
              <Header dividing sub>
                Attendees
              </Header>
              <List items={content.attendees} />
            </>
          )}
          {content.event_url && (
            <>
              <Header dividing sub>
                Web
              </Header>
              <p>
                <a href={content.event_url}>Visit external website</a>
              </p>
            </>
          )}
        </Segment>
        {content.text && (
          <div
            dangerouslySetInnerHTML={{
              __html: flattenHTMLToAppURL(content.text.data),
            }}
          />
        )}
      </Container>
    );


The above Semantic Image component is rendered as

.. code-block:: html
    :linenos:

    <img
      src="http://localhost:8080/Plone/my-documents/my-event/@@images/dd916f86-ac12-43b6-9e68-1e89956e9878.png"
      class="ui right floated image document-image">
