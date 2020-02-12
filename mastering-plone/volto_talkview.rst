.. _volto_talkview-label:

Volto View Components: A Default View for "Talk"
================================================

.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

       git checkout volto_addon

   Code for the end of this chapter::

        git checkout volto_talkview

In this part you will:

* Register a react view component for talks
* Write the component


Topics covered:

* Views
* Displaying data stored in fields of content types
* React Basics

In Volto the default visualization for your new content type "talk" only shows the title, description and the image.

.. note::

    In Plone the default view iterates over all fields in your schema and displays the stored data. In Volto this feature is not implemented yet.

Since we want to show the data we need to write a custom view for talks that is used in Volto.

In the folder :file:`volto` you need to add a new file ``src/components/Views/Talk.jsx`` (create the folder ``Views`` first.)

As a first step the file will hold a placeholder only:

..  code-block:: js

    import React from 'react';

    const TalkView = props => {
      return <div>I'm the TalkView component!</div>;
    };
    export default TalkView;

Now register the new component as default view for talks in ``src/config.js``.

..  code-block:: js
    :emphasize-lines: 1,7-10

    import { TalkView } from './components';

    [...]

    export const views = {
      ...defaultViews,
      contentTypesViews: {
        ...defaultViews.contentTypesViews,
        talk: TalkView,
      },
    };

This extends ``defaultViews.contentTypesViews`` with the key/value pair ``talk: TalkView``.

When Volto is running (with ``yarn start``) it should automatically pick up these changes and display the placeholder in place of the previously used default-view.

Now we will improve this view step by step.

First we reuse the component ``DefaultView.jsx`` in our custom view:

..  code-block:: js
    :emphasize-lines: 2,5

    import React from 'react';
    import { DefaultView } from '@plone/volto/components';

    const TalkView = props => {
      return <DefaultView {...props} />;
    };
    export default TalkView;

We are composing our view with Volto's default view component ``DefaultView.jsx`` to achieve the same features as the original one.
We will now add the content from the field ``details`` at the bottom.

..  code-block:: js

    import React from 'react';
    import { DefaultView } from '@plone/volto/components';

    const TalkView = props => {
      const { content } = props;
      return (
        <>
          <DefaultView {...props} />
          <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
        </>
      );
    };
    export default TalkView;


* The variable ``props`` is used to pass the json-representation of the content object (i.e. a talk) to the view. We assign a new variable ``content`` with that same value (``props``) to make it more explicit that this is the content object.
* ``content.details`` is the json-representation of the richtext-field ``details``:

  ..  code-block:: json

      {
        'content-type': 'text/html',
        data: '<p>foo bar...</p>',
        encoding: 'utf8'
      };

* ``content.details.data`` holds the raw html of the field ``details``. To render it properly we use ``dangerouslySetInnerHTML``


Next steps:

* Use ``Container`` to style text block
* No longer use DefaultView to customize Title
* Add other fields
* Map values to colors

The final view (draft):

..  code-block:: js

    import React from 'react';
    import { flattenToAppURL } from '@plone/volto/helpers';
    import { Container, Image, Icon, Label, Segment } from 'semantic-ui-react';

    const color_mapping = {
      professional: 'red',
      pro: 'red',
      beginner: 'green',
      advanced: 'yellow',
    };

    const TalkView = props => {
      const { content } = props;
      return (
        <>
          <Container id="page-talk">
            <h1 className="documentFirstHeading">
              {content.type_of_talk.title}: {content.title}
            </h1>
            {content.description && (
              <p className="documentDescription">{content.description}</p>
            )}
            {content.audience.map(item => {
              let audience = item.title;
              let visual = audience.charAt(0).toUpperCase() + audience.slice(1);
              let color = color_mapping[audience] || 'green';
              return (
                <Label
                  as="a"
                  href={`/search?audience=${audience}`}
                  key={audience}
                  tag
                  color={color}
                >
                  {visual}
                </Label>
              );
            })}
            {content.details && (
              <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
            )}
            <Segment clearing>
              <h3>{content.speaker}</h3>
              <a href={`mailto:${content.email}`}>
                <Icon name="mail" />
                {content.email}
              </a>
              <Image
                src={flattenToAppURL(content.image.scales.preview.download)}
                size="small"
                floated="right"
                alt={content.image_caption}
                circular
              />
              {content.speaker_biography && (
                <div
                  dangerouslySetInnerHTML={{
                    __html: content.speaker_biography.data,
                  }}
                />
              )}
            </Segment>
          </Container>
        </>
      );
    };
    export default TalkView;
