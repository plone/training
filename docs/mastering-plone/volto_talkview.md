---
myst:
  html_meta:
    "description": "Display content type"
    "property=og:description": "Display content type"
    "property=og:title": "Volto View Component: A Default View for a Talk"
    "keywords": "view, content type"
---

(volto-talkview-label)=

# Volto view component: A default view for a "Talk"

```{card}
In this part we will:

- Create a view to display a talk
- Register a React view component for content type talk
- Write the view component

Tools and techniques covered:

- View for a content type
- Displaying data stored in fields of a content type
- React Basics
```

````{card} Frontend chapter

Checkout `volto-ploneconf` at tag "overrides":

```shell
git checkout overrides
```

The code at the end of the chapter:

```shell
git checkout talkview
```

More info in {doc}`code`
````

## Creating and registering a new view component

The default visualization for the new content type `talk` lists the field values according to the type schema.

To show the talk data in a nice way, display the speaker portrait and add some components, we create a custom view for type talk.

In the folder {file}`frontend` you need to add a new file {file}`packages/volto-ploneconf/src/components/Views/Talk.jsx`.
Create the folder {file}`Views` first.

As a first step, the file will hold only a placeholder.
A view is a React component.
So we write a component function that just returns the info about what it will be.

```jsx
const TalkView = (props) => {
  return <div>I am the TalkView component!</div>;
};

export default TalkView;

```

Also add a convenience import of the new component to {file}`src/components/index.js`:

```jsx
import TalkView from './Views/Talk';

export { TalkView };
```

This is a common practice and allows to import the new view component as `import { TalkView } from './components';` instead of `import { TalkView } from './components/Views/Talk';`.

Now register the new component as the default view for `talks` in {file}`packages/volto-ploneconfig/src/index.js`.

```{code-block} jsx
:emphasize-lines: 1,6-8

import { TalkView } from './components';

const applyConfig = (config) => {
  config.views = {
    ...config.views,
    contentTypesViews: {
      ...config.views.contentTypesViews,
      talk: TalkView,
    },
  };
  return config;
};

export default applyConfig;
```

- This extends the Volto default setting `config.views.contentTypesViews` with the key/value pair `talk: TalkView`.
- It uses the [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to take the default settings and overrides what needs to be overridden.

A restarted Volto (with `make start`) picks up these configuration modifications and displays the placeholder in place of the previously used default view.


## Enhancing the view

Now we're improving this view step by step.
First we reuse the component `DefaultView.jsx` in our custom view:

```{code-block} jsx
:emphasize-lines: 1,4

import { DefaultView } from '@plone/volto/components';

const TalkView = (props) => {
  return <DefaultView {...props} />;
};
export default TalkView;
```

We will now add the content from the field `details` after the `DefaultView`.

```{code-block} jsx
:emphasize-lines: 5,7,8

import { DefaultView } from '@plone/volto/components';

const TalkView = (props) => {
  return (
    <>
      <DefaultView {...props} />
      <div dangerouslySetInnerHTML={{ __html: props.content.details.data }} />
    </>
  );
};
export default TalkView;
```

- `<> </>` is a fragment. The return value of React needs to be one single element.
- The variable `props` receives data from the parent component.
  As the TalkView component is registered as a content type view, it receives the content data and some more.
  We will use the content part.
  So we introduce a constant `content` to be more explicit.
- `content.details` is the value of the RichText field `details` with mime type, encoding and the data:

  ```jsx
  {
    'content-type': 'text/html',
    data: '<p>foo bar...</p>',
    encoding: 'utf8'
  };
  ```

  See {doc}`plone6docs:plone.restapi/docs/source/usage/serialization`.

- `content.details.data` holds the raw HTML. To render it, we use `dangerouslySetInnerHTML` (see https://legacy.reactjs.org/docs/dom-elements.html#dangerouslysetinnerhtml).

Please check the 'components' tab of Google developer tools for property `content` of the `TalkView` component to see the field values of your talk instance.

The result isn't beautiful, because the text sticks to the left border of the page.
You need to wrap it in a `Container` to get the same styling as the content of `DefaultView`:

```{code-block} jsx
:emphasize-lines: 1,11,13

import { Container as SemanticContainer } from 'semantic-ui-react';
import { DefaultView } from '@plone/volto/components';
import config from '@plone/volto/registry';

const TalkView = (props) => {
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;
  return (
    <>
      <DefaultView {...props} />
      <Container>
        <div dangerouslySetInnerHTML={{ __html: props.content.details.data }} />
      </Container>
    </>
  );
};
export default TalkView;

```

`Container` is either a registered component or a component from [Semantic UI React](https://react.semantic-ui.com/elements/container/) and needs to be imported before it is used.

We now decide to display the type of talk in the title (for example: "Keynote: The Future of Plone").
This means we cannot use `DefaultView` anymore since that displays the title like this: `<h1 className="documentFirstHeading">{content.title}</h1>`.
Instead we display the title and description in a custom way.

This has multiple benefits:

- All content can now be wrapped in the same `Container` which cleans up the HTML.
- We can control where the speaker portrait is displayed.
  We can now move all information on the speaker into a separate box.
  The speaker portrait is picked up by the DefaultView because the fields name is `image`, which is the same as the image from the behavior `plone.leadimage`.

```{code-block} jsx
:emphasize-lines: 9,18
:linenos:

import { Container as SemanticContainer } from 'semantic-ui-react';
import config from '@plone/volto/registry';

const TalkView = (props) => {
  const { content } = props;
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;
  return (
    <Container id="view-wrapper talk-view">
      <h1 className="documentFirstHeading">
        <span className="type_of_talk">{content.type_of_talk.token}: </span>
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

- `content.type_of_talk` is the value from the choice field `type_of_talk`: `{token: "training", title: null}`. We display the token.
  Later on we will map the tokens to titles with vocabularies.
- The `&&` in `{content.description && (<p>...</p>)}` makes sure, that this paragraph is only rendered, if the talk actually has a description.

Next we add a segment with info on the speaker:

```{code-block} jsx
:emphasize-lines: 3-4,22-37

import {
  Container as SemanticContainer,
  Header,
  Segment,
} from 'semantic-ui-react';
import config from '@plone/volto/registry';

const TalkView = (props) => {
  const { content } = props;
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;
  return (
    <Container id="view-wrapper talk-view">
      <h1 className="documentFirstHeading">
        <span className="type_of_talk">{content.type_of_talk.token}: </span>
        {content.title}
      </h1>
      {content.description && (
        <p className="documentDescription">{content.description}</p>
      )}
      <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
      <Segment clearing>
        {content.speaker && <Header dividing>{content.speaker}</Header>}
        <p>{content.company || content.website}</p>
        {content.email && (
          <p>
            Email: <a href={`mailto:${content.email}`}>{content.email}</a>
          </p>
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

- We use the component [Segment](https://react.semantic-ui.com/elements/segment/#variations-clearing) for the box.
- `` {`mailto:${content.email}`} `` is a [template literal](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals)

Next we add the image:

```{code-block} jsx
:emphasize-lines: 4,32-38

import {
  Container as SemanticContainer,
  Header,
  Image,
  Segment,
} from 'semantic-ui-react';
import { flattenToAppURL } from '@plone/volto/helpers';
import config from '@plone/volto/registry';

const TalkView = (props) => {
  const { content } = props;
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;
  return (
    <Container id="view-wrapper talk-view">
      <h1 className="documentFirstHeading">
        <span className="type_of_talk">{content.type_of_talk.token}: </span>
        {content.title}
      </h1>
      {content.description && (
        <p className="documentDescription">{content.description}</p>
      )}
      <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
      <Segment clearing>
        {content.speaker && <Header dividing>{content.speaker}</Header>}
        <p>{content.company || content.website}</p>
        {content.email && (
          <p>
            Email: <a href={`mailto:${content.email}`}>{content.email}</a>
          </p>
        )}
        <Image
          src={flattenToAppURL(content.image?.scales?.preview?.download)}
          size="small"
          floated="right"
          alt={content.speaker}
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

- We use the Semantic UI component [Image](https://react.semantic-ui.com/elements/image/#variations-avatar)
- We use `flattenToAppURL` to turn the Plone URL of the image to the Volto URL, for example it turns <http://localhost:8080/Plone/talks/dexterity-for-the-win/@@images/9fb3d165-82f4-4ffa-804f-2afe1bad8124.jpeg> into <http://localhost:3000/talks/dexterity-for-the-win/@@images/9fb3d165-82f4-4ffa-804f-2afe1bad8124.jpeg>.
- Open the React Developer Tools in your browser and inspect the property `content` of the TalkView component, its attribute `image` and its attribute `scales`. If you look at the [documentation for the serialization of image-fields](https://6.docs.plone.org/plone.restapi/docs/source/usage/serialization.html#file-image-fields) you can find out where that information comes from.
- To deal with talks without speaker image, we check for the existence of the image with `content.image?.scales?.preview?.download`.
  The expression with question marks returns `undefined` if `content` has no `image` key or `content.image` has no `scales` key and so forth.
  `?.` is the [optional chaining](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining) operator.

Next we add the audience:

```{code-block} jsx
:emphasize-lines: 5, 15-19, 29-36

import {
  Container as SemanticContainer,
  Header,
  Image,
  Label,
  Segment,
} from 'semantic-ui-react';
import { flattenToAppURL } from '@plone/volto/helpers';
import config from '@plone/volto/registry';

const TalkView = (props) => {
  const { content } = props;
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;
  const color_mapping = {
    beginner: 'green',
    advanced: 'yellow',
    professional: 'purple',
  };
  return (
    <Container id="view-wrapper talk-view">
      <h1 className="documentFirstHeading">
        <span className="type_of_talk">{content.type_of_talk.token}: </span>
        {content.title}
      </h1>
      {content.description && (
        <p className="documentDescription">{content.description}</p>
      )}
      {content.audience?.map((item) => {
        let color = color_mapping[item.token] || 'green';
        return (
          <Label key={item.token} color={color}>
            {item.token}
          </Label>
        );
      })}
      <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
      <Segment clearing>
        {content.speaker && <Header dividing>{content.speaker}</Header>}
        <p>{content.company || content.website}</p>
        {content.email && (
          <p>
            Email: <a href={`mailto:${content.email}`}>{content.email}</a>
          </p>
        )}
        <Image
          src={flattenToAppURL(content.image?.scales?.preview?.download)}
          size="small"
          floated="right"
          alt={content.speaker}
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

- With `{content.audience?.map(item => {...})}` we iterate over the individual values of the choice field `audience` if that exists.
- [map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) is used to iterate over the array `audience` using an [Arrow-function (=>)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions) in which `item` is one item in audience.
- The `item` is an `Object` like `{'title': null, 'token': 'advanced'}`.
- We map the available field values to colors and use green as a fallback.

As a last step we show the last few fields `website` and `company`, `github` and `twitter`:

```{code-block} jsx
:emphasize-lines: 36-42,50-67

import {
  Container as SemanticContainer,
  Header,
  Image,
  Label,
  Segment,
} from 'semantic-ui-react';
import { flattenToAppURL } from '@plone/volto/helpers';
import config from '@plone/volto/registry';

const TalkView = (props) => {
  const { content } = props;
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;
  const color_mapping = {
    beginner: 'green',
    advanced: 'yellow',
    professional: 'purple',
  };
  return (
    <Container id="view-wrapper talk-view">
      <h1 className="documentFirstHeading">
        <span className="type_of_talk">{content.type_of_talk.token}: </span>
        {content.title}
      </h1>
      {content.description && (
        <p className="documentDescription">{content.description}</p>
      )}
      {content.audience?.map((item) => {
        let color = color_mapping[item.token] || 'green';
        return (
          <Label key={item.token} color={color}>
            {item.token}
          </Label>
        );
      })}
      <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
      <Segment clearing>
        {content.speaker && <Header dividing>{content.speaker}</Header>}
        {content.website ? (
          <p>
            <a href={content.website}>{content.company || content.website}</a>
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
            X:{' '}
            <a href={`https://x.com/${content.twitter}`}>
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
        <Image
          src={flattenToAppURL(content.image?.scales?.preview?.download)}
          size="small"
          floated="right"
          alt={content.speaker}
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

## Summary

- We create a view for a content type to display the data of an instance.
- We handle the case of missing values.
