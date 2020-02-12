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

We will now add the content from the field ``details`` after the ``DefaultView``.

..  code-block:: js
    :emphasize-lines: 5,7,9-10

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

* ``<> </>`` is a shorthand for a segment. The return-value of react needs to be one element only.
* The variable ``props`` is used to pass the json-representation of the content object (i.e. a talk) to the view. We create a new variable ``content`` with the same value (``props``) to make it more explicit that this is the content object.
* ``content.details`` is the value of richtext-field ``details``:

  ..  code-block:: json

      {
        'content-type': 'text/html',
        data: '<p>foo bar...</p>',
        encoding: 'utf8'
      };

  See https://plonerestapi.readthedocs.io/en/latest/serialization.html#richtext-fields.

* ``content.details.data`` holds the raw html. To render it properly we use ``dangerouslySetInnerHTML`` (see https://reactjs.org/docs/dom-elements.html#dangerouslysetinnerhtml)

The result is not really beautiful because the text sticks to the left border of the page.
You need to wrap it in a ``Container`` to get the same styling as the content of ``DefaultView``:

..  code-block:: js
    :emphasize-lines: 3,10,12

    import React from 'react';
    import { DefaultView } from '@plone/volto/components';
    import { Container } from 'semantic-ui-react';

    const TalkView = props => {
      const { content } = props;
      return (
        <>
          <DefaultView {...props} />
          <Container>
            <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
          </Container>
        </>
      );
    };
    export default TalkView;

* ``Container`` is a component from `Semantic UI React <https://react.semantic-ui.com/elements/container/>`_ and needs to be imported before it is used.

We now decide to display the type of talk in the title (E.g. "Keynote: The Future of Plone").
This means we cannot use ``DefaultView`` anymore since that displays the title like this: ``<h1 className="documentFirstHeading">{content.title}</h1>``.
Instead we display the title and description ourselves.

This has multiple benefits:

* All content can now be wrapped in the same ``Container`` which cleans up the html.
* We can control where the speaker-portrait is displayed. We can now move all information on the speaker into a separate box. The speaker-portrait is picked up by the DefaultView because the field's name is ``image`` (same as the image from the behavior ``plone.leadimage``).

..  code-block:: js
    :emphasize-lines: 8-14

    import React from 'react';
    import { Container } from 'semantic-ui-react';

    const TalkView = props => {
      const { content } = props;
      return (
        <Container id="page-talk">
          <h1 className="documentFirstHeading">
            <span class="type_of_talk">{content.type_of_talk.title} </span>
            {content.title}
          </h1>
          {content.description && (
            <p className="documentDescription">{content.description}</p>
          )}
          <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
        </Container>
      );
    };
    export default TalkView;

* ``content.type_of_talk`` is the json of the value from the choice-field ``type_of_talk``: ``{token: "training", title: "Training"}``. To display it we use the title.
* The ``&&`` in ``{content.description && (<p>...</p>)}`` makes sure that this paragraph is only rendered if the talk actually has a description.


Next we add a block with info on the speaker:

..  code-block:: js
    :emphasize-lines: 2,16-30

    import React from 'react';
    import { Container, Icon, Segment } from 'semantic-ui-react';

    const TalkView = props => {
      const { content } = props;
      return (
        <Container id="page-talk">
          <h1 className="documentFirstHeading">
            <span class="type_of_talk">{content.type_of_talk.title} </span>
            {content.title}
          </h1>
          {content.description && (
            <p className="documentDescription">{content.description}</p>
          )}
          <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
          <Segment clearing>
            <h3>{content.speaker}</h3>
            <p>{content.company || content.website}</p>
            <a href={`mailto:${content.email}`}>
              <Icon name="mail" />
              {content.email}
            </a>
            {content.speaker_biography && (
              <div
                dangerouslySetInnerHTML={{
                  __html: content.speaker_biography.data,
                }}
              />
            )}
          </Segment>
        </Container>
      );
    };
    export default TalkView;

* We use the component `Segment <https://react.semantic-ui.com/elements/segment/#variations-clearing>`_ for the box
* We use the component `Icon <https://react.semantic-ui.com/elements/icon/>`_ to siplac the mail icon.
* ``{`mailto:${content.email}`}`` is a `template literal <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals>`_

Next we add the image:

..  code-block:: js
    :emphasize-lines: 2,3,24-30

    import React from 'react';
    import { Container, Icon, Image, Segment } from 'semantic-ui-react';
    import { flattenToAppURL } from '@plone/volto/helpers';

    const TalkView = props => {
      const { content } = props;
      return (
        <Container id="page-talk">
          <h1 className="documentFirstHeading">
            <span class="type_of_talk">{content.type_of_talk.title} </span>
            {content.title}
          </h1>
          {content.description && (
            <p className="documentDescription">{content.description}</p>
          )}
          <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
          <Segment clearing>
            <h3>{content.speaker}</h3>
            <p>{content.company || content.website}</p>
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
      );
    };
    export default TalkView;


* We use the component `Image <https://react.semantic-ui.com/elements/image/#variations-circular>`_
* We use ``flattenToAppURL`` to turn the Plone-url of the image to the Volto-url, e.g. it turns http://localhost:8080/Plone/talks/dexterity-for-the-win/@@images/9fb3d165-82f4-4ffa-804f-2afe1bad8124.jpeg into http://localhost:3000/talks/dexterity-for-the-win/@@images/9fb3d165-82f4-4ffa-804f-2afe1bad8124.jpeg.
* Open the React Developer Tools in your browser and inspect the property ``image`` of TalkView and its property ``scale``. If you look at the `documentation for the serialization of image-fields <https://plonerestapi.readthedocs.io/en/latest/serialization.html#file-image-fields>`_ you can find out where that information comes from.

Next we add the audience:

..  code-block:: js
    :emphasize-lines: 2,7-11,22-35

    import React from 'react';
    import { Container, Icon, Image, Label, Segment } from 'semantic-ui-react';
    import { flattenToAppURL } from '@plone/volto/helpers';

    const TalkView = props => {
      const { content } = props;
      const color_mapping = {
        Beginner: 'green',
        Advanced: 'yellow',
        Professional: 'red',
      };

      return (
        <Container id="page-talk">
          <h1 className="documentFirstHeading">
            <span class="type_of_talk">{content.type_of_talk.title} </span>
            {content.title}
          </h1>
          {content.description && (
            <p className="documentDescription">{content.description}</p>
          )}
          {content.audience.map(item => {
            let audience = item.title;
            let color = color_mapping[audience] || 'blue';
            return (
              <Label
                as="a"
                href={`/search?audience=${audience}&portal_type=talk`}
                key={audience}
                color={color}
              >
                {audience}
              </Label>
            );
          })}
          <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
          <Segment clearing>
            <h3>{content.speaker}</h3>
            <p>{content.company || content.website}</p>
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
      );
    };
    export default TalkView;


* We use the component `Label <https://react.semantic-ui.com/elements/label/>`_ to render the audience as a tag.
* We map the values that are available in the field to colors.

XXX

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
