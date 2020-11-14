.. _volto_semantic_ui-label:

Semantic UI
============

.. sidebar:: Volto chapter

  .. figure:: _static/Volto.svg
     :alt: Volto Logo

  This chapter is about the react frontend Volto.

  Learn about templates in the classic frontend in chapter :doc:`zpt`

`Semantic UI` is a development framework that helps create beautiful, responsive layouts using human-friendly HTML. It provides a declarative API, shorthand props and many helpers that simplifies development.

Its React complement `Semantic UI React` provides React components while Semantic UI provides themes as CSS stylesheets with less variables and rules. 

Volto is per default, not mandatory, build on both: the Semantic UI theming and the Semantic UI React Components. 



Volto applies components from `Semantic UI React <https://react.semantic-ui.com/>`_ to compose a large part of the views. For example the component `Image <https://react.semantic-ui.com/elements/image/>`_ is used to render images.

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 14-18

    /**
    * EventView view component class.
    * @function EventView
    * @params {object} content Content object.
    * @returns {string} Markup of the component.
    */
    const EventView = ({ intl, content }) => (
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
          …

The above Semantic `Image` component is rendered as

.. code-block:: html
    :linenos:

    <img
      src="http://localhost:8080/Plone/my-documents/my-event/@@images/dd916f86-ac12-43b6-9e68-1e89956e9878.png"
      class="ui right floated image document-image">
