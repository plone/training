---
myst:
  html_meta:
    "description": "Small customizations by overriding existing code"
    "property=og:description": "Small customizations by overriding existing code"
    "property=og:title": "Customize Volto components"
    "keywords": "Plone, Volto, customization, shadowing, component"
---

(volto-overrides-label)=

# Customize Volto components

```{card}
In this part you will customize existing components and views.

Tools and techniques covered:

- Component shadowing
- Content type views
```

````{card}

Check out `mastering-plone-project` at tag `talks`:

```shell
git checkout talks
```

The code at the end of the chapter:

```shell
git checkout overrides
```

More info in {doc}`code`
````


(volto-overrides-componentshadowing-label)=

## Component shadowing

We use a technique called **component shadowing** to override an existing Volto component with our local custom version, without having to modify Volto's source code at all.
You have to create a new file inside {file}`frontend/packages/volto-ploneconf-site/src/customizations/` in the same subpath where the original file is found inside {file}`frontend/core/packages/volto/src/`.

Every time you add a file to your app, you have to restart Volto in order for it to discover the new file.
From that point on, hot module reloading should kick in and reload the page automatically on changes.

You can customize any module in Volto, including actions and reducers, not only components.

The Volto code can be found in {file}`frontend/core/packages/volto/`.


### Example: Customize the footer

The React developer tools provide a selector to find the component we need to override.

```{figure} _static/inspect_components_1.png
:alt: Footer component.
```

```{figure} _static/inspect_components_2.png
:alt: Footer component file.
```

Customize the footer by copying {file}`frontend/core/packages/volto/src/components/theme/Footer/Footer.jsx` to your customization folder at {file}`frontend/packages/volto-ploneconf-site/src/customizations/components/theme/Footer/Footer.jsx`.  
After a restart you can change this Footer component and the changes are shown immediately due to hot module reloading.


## Customize the News Item view

We want to show the date a News Item is published.
This way visitors can see at a glance if they are looking at current news.
This information isn't shown by default.
So you need to customize the way a News Item is rendered.

A News Item has date attributes.
The attributes of a content type instance are defined by the schema of a content type and possible behaviors.
These date attributes are available when the content is fetched by the frontend.
But let's first have a look how these attributes are used in a Volto component.

```{seealso}
We had a look at schemas in {doc}`dexterity` and {doc}`dexterity_2_talk`.
We will add a behavior later in {doc}`behaviors_1`.
```

The Volto view component to render a News Item is in {file}`frontend/core/packages/volto/src/components/theme/View/NewsItemView.jsx`.

```{code-block} jsx
:linenos:
/**
 * NewsItemView view component.
 * @module components/theme/View/NewsItemView
 */

import React from 'react';
import PropTypes from 'prop-types';
import { Container as SemanticContainer } from 'semantic-ui-react';
import { hasBlocksData } from '@plone/volto/helpers/Blocks/Blocks';
import { flattenHTMLToAppURL } from '@plone/volto/helpers/Url/Url';
import RenderBlocks from '@plone/volto/components/theme/View/RenderBlocks';
import config from '@plone/volto/registry';

/**
 * NewsItemView view component class.
 * @function NewsItemView
 * @params {object} content Content object.
 * @returns {string} Markup of the component.
 */
const NewsItemView = ({ content }) => {
  const Image = config.getComponent({ name: 'Image' }).component;
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;

  return hasBlocksData(content) ? (
    <Container id="page-document" className="view-wrapper newsitem-view">
      <RenderBlocks content={content} />
    </Container>
  ) : (
    <Container className="view-wrapper">
      {content.title && (
        <h1 className="documentFirstHeading">
          {content.title}
          {content.subtitle && ` - ${content.subtitle}`}
        </h1>
      )}
      {content.description && (
        <p className="documentDescription">{content.description}</p>
      )}
      {content.image && (
        <Image
          className="documentImage ui right floated image"
          alt={content.title}
          title={content.title}
          item={content}
          imageField="image"
          responsive={true}
        />
      )}
      {content.text && (
        <div
          dangerouslySetInnerHTML={{
            __html: flattenHTMLToAppURL(content.text.data),
          }}
        />
      )}
    </Container>
  );
};

/**
 * Property types.
 * @property {Object} propTypes Property types.
 * @static
 */
NewsItemView.propTypes = {
  content: PropTypes.shape({
    title: PropTypes.string,
    description: PropTypes.string,
    text: PropTypes.shape({
      data: PropTypes.string,
    }),
  }).isRequired,
};

export default NewsItemView;
```

````{note}
- `content` is passed to `NewsItemView` and represents the content item as it was serialized by the REST API.
  The `content` data has been fetched by an action on navigating to route `http://localhost:3000/my-news-item`.

- The view displays various attributes of the News Item using `content.title`, `content.description` or `content.text.data`.

- You can inspect all data in the `content` object using the React Developer Tools for [Firefox](https://addons.mozilla.org/de/firefox/addon/react-devtools/) or [Chrome](https://chromewebstore.google.com/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi):

```{figure} _static/volto_react_devtools.png
:align: center
```
````

Copy this file from {file}`frontend/core/packages/volto/src/components/theme/View/NewsItemView.jsx` to {file}`frontend/packages/volto-ploneconf-site/src/customizations/components/theme/View/NewsItemView.jsx`.

After restarting Volto, the new file is used when displaying a News Item.
To make sure your file is taken into effect, add a small change before the blocks `<RenderBlocks content={content} />`.
If it shows up you're good to go.

```{tip}
In you own projects you should always do a commit of the unchanged file and another commit after you changed the file.
This way you will have a commit in your git history with the change you made.
You will thank yourself later for that clean diff!
```

To display the date add the following before the text:

```jsx
<p>{content.created}</p>
```

This will render something like *2022-10-02T21:58:54*.
This isn't user friendly.
Let's use one of many helpers available in Volto.

Import the component `FormattedDate` from `@plone/volto/components` at the top of the file and use it to format the date in a human readable format.

```{code-block} jsx
:emphasize-lines: 10,28-30
:linenos:

/**
 * NewsItemView view component.
 * @module components/theme/View/NewsItemView
 */

import React from 'react';
import PropTypes from 'prop-types';
import { Container as SemanticContainer } from 'semantic-ui-react';
import { hasBlocksData } from '@plone/volto/helpers/Blocks/Blocks';
import FormattedDate from '@plone/volto/components/theme/FormattedDate/FormattedDate';
import { flattenHTMLToAppURL } from '@plone/volto/helpers/Url/Url';
import RenderBlocks from '@plone/volto/components/theme/View/RenderBlocks';
import config from '@plone/volto/registry';

/**
 * NewsItemView view component class.
 * @function NewsItemView
 * @params {object} content Content object.
 * @returns {string} Markup of the component.
 */
const NewsItemView = ({ content }) => {
  const Image = config.getComponent({ name: 'Image' }).component;
  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;

  return hasBlocksData(content) ? (
    <Container id="page-document" className="view-wrapper newsitem-view">
      <p>
        <FormattedDate date={content.created} includeTime />
      </p>{' '}
      <RenderBlocks content={content} />
    </Container>
  ) : (
    <Container className="view-wrapper">
      {content.title && (
        <h1 className="documentFirstHeading">
          {content.title}
          {content.subtitle && ` - ${content.subtitle}`}
        </h1>
      )}
      {content.description && (
        <p className="documentDescription">{content.description}</p>
      )}
      {content.image && (
        <Image
          className="documentImage ui right floated image"
          alt={content.title}
          title={content.title}
          item={content}
          imageField="image"
          responsive={true}
        />
      )}
      {content.text && (
        <div
          dangerouslySetInnerHTML={{
            __html: flattenHTMLToAppURL(content.text.data),
          }}
        />
      )}
    </Container>
  );
};

/**
 * Property types.
 * @property {Object} propTypes Property types.
 * @static
 */
NewsItemView.propTypes = {
  content: PropTypes.shape({
    title: PropTypes.string,
    description: PropTypes.string,
    text: PropTypes.shape({
      data: PropTypes.string,
    }),
  }).isRequired,
};

export default NewsItemView;
```

The result should look like this:

```{figure} _static/volto_news_with_date.png
:alt: A News Item with publishing date.
```

Now another issue appears.
There are various dates associated with any content object:

- The date the item was created: `content.created`
- The date the item was last modified: `content.modified`
- The date the item was published: `content.effective`

In fact you most likely want to show the date when the item has been published.
But while the item isn't yet published, this value isn't yet set, and you will get an error.
So we'll add some simple logic to show the effective date only if it exists.

```jsx
{content.review_state === 'published' && content.effective && (
  <p>
    <FormattedDate date={content.effective} includeTime />
  </p>
)}
```

As we're in the HTML part of our React component, we surround the JavaScript code with curly braces.


## Summary

- With component shadowing, views and other components in Volto can be modified and extended.
- Component shadowing a powerful mechanism to make changes without the need of complex configuration or maintaining a fork of the code.
- You need to restart Volto when you add a new override.

```{seealso}
Volto Hands-On training: {ref}`voltohandson-header-component-label`
```
