(volto-talkview-label)=

# Volto View Components: A Default View for "Talk"

````{sidebar}
```{figure} _static/plone-training-logo-for-frontend.svg
:alt: Plone frontend 
:align: left
```

This chapter is about the React frontend Volto.

Solve the same tasks in Plone Classic UI in chapter {doc}`views_2`

---

**Get the code! ({doc}`More info <code>`)**

Code for the beginning of this chapter:

```shell
git checkout theming
```

Code for the end of this chapter:

```shell
git checkout talkview
```
````

To be solved task in this part:

- Create a view to display talks in a nice way

In this part you will:

- Register a react view component for talks
- Write the component

Topics covered:

- Views
- Displaying data stored in fields of content types
- React Basics

In Volto the default visualization for your new content type "talk" only shows the title, description and the image.

```{container} volto
This paragraph might be rendered in a custom way.
```

```{note}
In Plone the default view iterates over all fields in your schema and displays the stored data. In Volto this feature is not implemented yet.
```

Since we want to show the data we need to write a custom view for talks that is used in Volto.

In the folder {file}`frontend` you need to add a new file {file}`src/components/Views/Talk.jsx` (create the folder {file}`Views` first.)

As a first step the file will hold a placeholder only:

```jsx
import React from 'react';

const TalkView = props => {
  return <div>I am the TalkView component!</div>;
};

export default TalkView;
```

Also add a convenience-import of the new component to {file}`src/components/index.js`:

```jsx
import TalkView from './Views/Talk';

export { TalkView };
```

This is is a common practice and allows us to import the new view as `import { TalkView } from './components';` instead of `import { TalkView } from './components/Views/Talk';`.

Now register the new component as default view for talks in {file}`src/config.js`.

```{code-block} jsx
:emphasize-lines: 1,7-10

import { TalkView } from './components';

[...]

config.views = {
  ...config.views,
  contentTypesViews: {
    ...config.views.contentTypesViews,
    talk: TalkView,
  },
};
```

- This extends the Volto default setting `config.views.contentTypesViews` with the key/value pair `talk: TalkView`.
- It uses the [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax).

When Volto is running (with `yarn start`) it picks up these changes and displays the placeholder in place of the previously used default-view.

Now we will improve this view step by step.
First we reuse the component `DefaultView.jsx` in our custom view:

```{code-block} jsx
:emphasize-lines: 2,5

import React from 'react';
import { DefaultView } from '@plone/volto/components';

const TalkView = props => {
  return <DefaultView {...props} />;
};
export default TalkView;
```

We will now add the content from the field `details` after the `DefaultView`.

```{code-block} jsx
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
```

- `<> </>` is a fragment. The return-value of react needs to be one single element.

- The variable `props` is used to pass the json-representation of the content object (i.e. a talk) to the view. We create a new variable `content` with the same value (`props`) to make it more explicit that this is the content object.

- `content.details` is the value of richtext-field `details`:

  ```jsx
  {
    'content-type': 'text/html',
    data: '<p>foo bar...</p>',
    encoding: 'utf8'
  };
  ```

  See <https://plonerestapi.readthedocs.io/en/latest/serialization.html#richtext-fields>.

- `content.details.data` holds the raw html. To render it properly we use `dangerouslySetInnerHTML` (see <https://reactjs.org/docs/dom-elements.html#dangerouslysetinnerhtml>)

The result is not really beautiful because the text sticks to the left border of the page.
You need to wrap it in a `Container` to get the same styling as the content of `DefaultView`:

```{code-block} jsx
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
```

- `Container` is a component from [Semantic UI React](https://react.semantic-ui.com/elements/container/) and needs to be imported before it is used.

We now decide to display the type of talk in the title (E.g. "Keynote: The Future of Plone").
This means we cannot use `DefaultView` anymore since that displays the title like this: `<h1 className="documentFirstHeading">{content.title}</h1>`.
Instead we display the title and description ourselves.

This has multiple benefits:

- All content can now be wrapped in the same `Container` which cleans up the html.
- We can control where the speaker portrait is displayed. We can now move all information on the speaker into a separate box. The speaker portrait is picked up by the DefaultView because the fields name is `image` (same as the image from the behavior `plone.leadimage`).

With this changes we do discard the title-tag in the HTML head though. This will change the name occuring in the browser tab or browser head to the current site url. To use the content title instead, you'll have to import the `Helmet` component, which allows to overwrite all meta tags for the HTML head like the page-title.

```{code-block} jsx
:emphasize-lines: 3,9-16

import React from 'react';
import { Container } from 'semantic-ui-react';
import { Helmet } from '@plone/volto/helpers';

const TalkView = props => {
  const { content } = props;
  return (
    <Container id="page-talk">
      <Helmet title={content.title} />
      <h1 className="documentFirstHeading">
        <span class="type_of_talk">{content.type_of_talk.title}: </span>
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
```

- `content.type_of_talk` is the json of the value from the choice field `type_of_talk`: `{token: "training", title: "Training"}`. To display it we use the title.
- The `&&` in `{content.description && (<p>...</p>)}` makes sure that this paragraph is only rendered if the talk actually has a description.

Next we add a block with info on the speaker:

```{code-block} jsx
:emphasize-lines: 2,16-30

import React from 'react';
import { Container, Header, Icon, Segment } from 'semantic-ui-react';

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
        {content.speaker && <Header dividing>{content.speaker}</Header>}
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
```

- We use the component [Segment](https://react.semantic-ui.com/elements/segment/#variations-clearing) for the box.
- We use the component [Icon](https://react.semantic-ui.com/elements/icon/) to display the mail icon.
- `` {`mailto:${content.email}`} `` is a [template literal](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals)

Next we add the image:

```{code-block} jsx
:emphasize-lines: 2,3,24-30

import React from 'react';
import { Container, Header, Icon, Image, Segment } from 'semantic-ui-react';
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
        {content.speaker && <Header dividing>{content.speaker}</Header>}
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
          avatar
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
```

- We use the component [Image](https://react.semantic-ui.com/elements/image/#variations-avatar)
- We use `flattenToAppURL` to turn the Plone url of the image to the Volto url, e.g. it turns <http://localhost:8080/Plone/talks/dexterity-for-the-win/@@images/9fb3d165-82f4-4ffa-804f-2afe1bad8124.jpeg> into <http://localhost:3000/talks/dexterity-for-the-win/@@images/9fb3d165-82f4-4ffa-804f-2afe1bad8124.jpeg>.
- Open the React Developer Tools in your browser and inspect the property `image` of TalkView and its property `scale`. If you look at the [documentation for the serialization of image-fields](https://plonerestapi.readthedocs.io/en/latest/serialization.html#file-image-fields) you can find out where that information comes from.

Next we add the audience:

```{code-block} jsx
:emphasize-lines: 2,7-11,22-30

import React from 'react';
import { Container, Header, Icon, Image, Label, Segment } from 'semantic-ui-react';
import { flattenToAppURL } from '@plone/volto/helpers';

const TalkView = props => {
  const { content } = props;
  const color_mapping = {
    Beginner: 'green',
    Advanced: 'yellow',
    Professional: 'purple',
  };

  return (
    <Container id="page-talk">
      <h1 className="documentFirstHeading">
        {content.type_of_talk.title || content.type_of_talk.token}:{' '}
        {content.title}
      </h1>
      {content.description && (
        <p className="documentDescription">{content.description}</p>
      )}
      {content.audience?.map((item) => {
        let audience = item.title || item.token;
        let color = color_mapping[audience] || 'green';
        return (
          <Label key={audience} color={color}>
            {audience}
          </Label>
        );
      })}
      <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
      <Segment clearing>
        {content.speaker && <Header dividing>{content.speaker}</Header>}
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
          avatar
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
```

- With `{content.audience?.map(item => {...})}` we iterate over the individual values of the field `audience` if that exists.
- `?.` is [optional chaining](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining)
- [map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) is used to iterate over the array `audience` using a [Arrow-function (=>)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions) in which `item` is one item in audience.
- The `item` is a object like `{'title': 'Advanced', 'token': 'Advanced'}`. We need to use `item.title || item.token` in case `title` is `null` which happens in simple fields as ours.
- We map the values that are available in the field to colors and use blue as a fallback.

As a last step we show the last few fields `website` and `company`, `github` and `twitter`:

```{code-block} jsx
:emphasize-lines: 36-42,50-66

import React from 'react';
import { flattenToAppURL } from '@plone/volto/helpers';
import { Container, Image, Icon, Label, Segment } from 'semantic-ui-react';

const TalkView = props => {
  const { content } = props;
  const color_mapping = {
    Beginner: 'green',
    Advanced: 'yellow',
    Professional: 'purple',
  };

  return (
    <Container id="page-talk">
      <h1 className="documentFirstHeading">
        {content.type_of_talk.title || content.type_of_talk.token}:{' '}
        {content.title}
      </h1>
      {content.description && (
        <p className="documentDescription">{content.description}</p>
      )}
      {content.audience?.map((item) => {
        let audience = item.title || item.token;
        let color = color_mapping[audience] || 'green';
        return (
          <Label key={audience} color={color}>
            {audience}
          </Label>
        );
      })}
      {content.details && (
        <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
      )}
      <Segment clearing>
        {content.speaker && <Header dividing>{content.speaker}</Header>}
        {content.website ? (
          <p>
            <a href={content.website}>
              {content.company || content.website}
            </a>
          </p>
        ) : (
          <p>{content.company}</p>
        )}
        {content.email && (
          <p>
            Email: <a href={`mailto:${content.email}`}>{content.email}</a>
          </p>
        )}
        {content.twitter && (
          <p>
            Twitter:{' '}
            <a href={`https://twitter.com/${content.twitter}`}>
              {content.twitter.startsWith('@')
                ? content.twitter
                : '@' + content.twitter}
            </a>
          </p>
        )}
        {content.github && (
          <p>
            Github:{' '}
            <a href={`https://github.com/${content.github}`}>
              {content.github}
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
    </Container>
  );
};
export default TalkView;
```
