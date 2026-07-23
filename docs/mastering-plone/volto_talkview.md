---
myst:
  html_meta:
    "description": "Display content type"
    "property=og:description": "Display content type"
    "property=og:title": "Content views"
    "keywords": "view, content type"
---

(volto-talkview-label)=

# Content views

```{card}
In this part we will:

- Create a component to display a talk
- Register the component as the default view for the talk content type
- Write the view component

Tools and techniques covered:

- View for a content type
- Displaying data stored in fields of a content type
- React basics
```

````{card} Frontend chapter

Check out `mastering-plone-project` at tag "overrides":

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

We will create a custom view for the talk content type in order to show the talk data in a nice way, display the speaker portrait, and add some components.

In the folder {file}`frontend` you need to add a new file {file}`packages/volto-ploneconf-site/src/components/Views/Talk.jsx`.
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

Now register the new component as the default view for `talk` in {file}`packages/volto-ploneconf-site/src/config/settings.ts`.

```{code-block} tsx
:emphasize-lines: 2-3,12-18

import type { ConfigType } from '@plone/registry';
import type { ViewsConfig } from '@plone/types';
import TalkView from '../components/Views/TalkView';

export default function install(config: ConfigType) {
  // Language settings
  config.settings.defaultLanguage = 'en';
  // Additional language settings for Volto 19 and above, add as many supported languages as needed
  // Languages not added to supportedLanguages will not be included in the build
  // config.settings.supportedLanguages = ['en'];

  config.views = {
    ...(config.views as ViewsConfig),
    contentTypesViews: {
      ...config.views.contentTypesViews,
      talk: TalkView,
    },
  };

  return config;
}
```

- This extends the Volto default setting `config.views.contentTypesViews` with the key/value pair `talk: TalkView`.
- It uses the [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to take the default settings and overrides what needs to be overridden.

A restarted Volto (with `make start`) picks up these configuration modifications and displays the placeholder in place of the previously used default view.


## Enhance the view

Now let's improve this view step by step.
First we reuse the component `DefaultView.jsx` in our custom view:

```{code-block} jsx
:emphasize-lines: 1,4

import DefaultView from '@plone/volto/components/theme/View/DefaultView';

const TalkView = (props) => {
  return <DefaultView {...props} />;
};
export default TalkView;
```

We will now add the content from the field `details` after the `DefaultView`.

```{code-block} jsx
:emphasize-lines: 5,7,8

import DefaultView from '@plone/volto/components/theme/View/DefaultView';

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

- `<> </>` is a fragment. The return value from a React component needs to be one single element.
- The variable `props` receives data from the parent component.
  As the TalkView component is registered as a content type view, it receives the content data and some more.
  We will use the content part.
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

Please check the 'components' tab of Google developer tools for the property `content` of the `TalkView` component to see the field values of your talk instance.

The result isn't beautiful, because the text sticks to the left border of the page.
You need to wrap it in a `Container` to get the same styling as the content of `DefaultView`:

```{code-block} jsx
:emphasize-lines: 1,6-7,11,13

import { Container as SemanticContainer } from 'semantic-ui-react';
import DefaultView from '@plone/volto/components/theme/View/DefaultView';
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

Container is either a registered component or a component from [Semantic UI React](https://react.semantic-ui.com/elements/container/) and needs to be imported before it is used.

We now decide to display the type of talk in the title (for example: "Keynote: The Future of Plone").
This means we cannot use `DefaultView` anymore since that displays the title like this: `<h1 className="documentFirstHeading">{content.title}</h1>`.
Instead we display the title and description in a custom way.

This has multiple benefits:

- All content can now be wrapped in the same `Container` which cleans up the HTML.
- We can control where the speaker portrait is displayed.
  We can now move all information on the speaker into a separate box.
  The speaker portrait is picked up by the DefaultView because the fields name is `image`, which is the same as the image from the behavior `plone.leadimage`.

```{code-block} jsx
:emphasize-lines: 9-18
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
:emphasize-lines: 17-34

import { Container as SemanticContainer } from 'semantic-ui-react';
import config from '@plone/volto/registry';

const TalkView = (props) => {
  const { content } = props;
  const Container = config.getComponent({ name: 'Container' }).component || SemanticContainer;
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
      <div className="ui clearing segment">
        {content.speaker && (
          <div className="ui dividing header">{content.speaker}</div>
        )}
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
      </div>
    </Container>
  );
};
export default TalkView;
```

- We use CSS classes from [Semantic UI](https://semantic-ui.com/) for the segment and header.
- `` `mailto:${content.email}` `` is a [template literal](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals)

Next we add the image:

```{code-block} jsx
:emphasize-lines: 8,29-33

import { Container as SemanticContainer } from 'semantic-ui-react';
import config from '@plone/volto/registry';

const TalkView = (props) => {
  const { content } = props;
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;
  const Image = config.getComponent({ name: 'Image' }).component;
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
      <div className="ui clearing segment">
        {content.speaker && (
          <div className="ui dividing header">{content.speaker}</div>
        )}
        <p>{content.company || content.website}</p>
        {content.email && (
          <p>
            Email: <a href={`mailto:${content.email}`}>{content.email}</a>
          </p>
        )}
        {content.image && <Image
          item={content}
          alt={content.speaker}
          className="ui small right floated image"
        />}
        {content.speaker_biography && (
          <div
            dangerouslySetInnerHTML={{
              __html: content.speaker_biography.data,
            }}
          />
        )}
      </div>
    </Container>
  );
};
export default TalkView;
```

- We use the Volto Image component (see {doc}`plone6docs:volto/development/images`), which renders an `img` element with multiple image sizes in a `srcset` so the browser can download the most appropriate one.
- Open the React Developer Tools in your browser and inspect the property `content` of the TalkView component, its attribute `image` and its attribute `scales`. If you look at the [documentation for the serialization of image fields](https://6.docs.plone.org/plone.restapi/docs/source/usage/serialization.html#file-image-fields) you can find out where that information comes from.
- To deal with talks without a speaker image, we check for the existence of the image with `content.image &&`.

Next we add the audience:

```{code-block} jsx
:emphasize-lines: 4-8, 24-31

import { Container as SemanticContainer } from 'semantic-ui-react';
import config from '@plone/volto/registry';

const colorMapping = {
  Beginner: 'green',
  Advanced: 'yellow',
  Professional: 'purple',
};

const TalkView = (props) => {
  const { content } = props;
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;
  const Image = config.getComponent({ name: 'Image' }).component;
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
        let color = colorMapping[item.token] || 'green';
        return (
          <div className={`ui label ${color}`} key={item.token}>
            {item.token}
          </div>
        );
      })}
      <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
      <div className="ui clearing segment">
        {content.speaker && (
          <div className="ui dividing header">{content.speaker}</div>
        )}
        <p>{content.company || content.website}</p>
        {content.email && (
          <p>
            Email: <a href={`mailto:${content.email}`}>{content.email}</a>
          </p>
        )}
        <Image
          item={content}
          alt={content.speaker}
          className="ui small right floated image"
        />
        {content.speaker_biography && (
          <div
            dangerouslySetInnerHTML={{
              __html: content.speaker_biography.data,
            }}
          />
        )}
      </div>
    </Container>
  );
};
export default TalkView;
```

- With `{content.audience?.map(item => {...})}` we iterate over the individual values of the choice field `audience` if that exists.
- [map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) is used to iterate over the array `audience` using an [Arrow-function (=>)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions) in which `item` is one item in audience.
- The `item` is an `Object` like `{'title': null, 'token': 'advanced'}`.
- We map the available field values to colors and use green as a fallback.

As a last step we show the last few fields `website`, `company`, and `github`:

```{code-block} jsx
:emphasize-lines: 37-43,49-56

import { Container as SemanticContainer } from 'semantic-ui-react';
import config from '@plone/volto/registry';

const colorMapping = {
  Beginner: 'green',
  Advanced: 'yellow',
  Professional: 'purple',
};

const TalkView = (props) => {
  const { content } = props;
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;
  const Image = config.getComponent({ name: 'Image' }).component;
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
        let color = colorMapping[item.token] || 'green';
        return (
          <div className={`ui label ${color}`} key={item.token}>
            {item.token}
          </div>
        );
      })}
      <div dangerouslySetInnerHTML={{ __html: content.details.data }} />
      <div className="ui clearing segment">
        {content.speaker && (
          <div className="ui dividing header">{content.speaker}</div>
        )}
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
        {content.github && (
          <p>
            Github:{' '}
            <a href={`https://github.com/${content.github}`}>
              {content.github}
            </a>
          </p>
        )}
        <Image
          item={content}
          alt={content.speaker}
          className="ui small right floated image"
        />
        {content.speaker_biography && (
          <div
            dangerouslySetInnerHTML={{
              __html: content.speaker_biography.data,
            }}
          />
        )}
      </div>
    </Container>
  );
};
export default TalkView;
```

## Summary

- We create a view for a content type to display the data of an instance.
- We handle the case of missing values.
