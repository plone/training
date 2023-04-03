---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(volto-overrides-label)=

# Customizing Volto Components

````{sidebar} Plone Frontend Chapter
```{figure} _static/plone-training-logo-for-frontend.svg
:alt: Plone frontend
:class: logo
```
---

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout initial
```

Code for the end of this chapter:

```shell
git checkout overrides
```
````

In this part you will:

- Find out how news items are displayed
- Customize existing components

Topics covered:

- Customize existing views with Component Shadowing
- Content Type Views
- Listing Views
- Blocks

(volto-overrides-componentshadowing-label)=

## Component shadowing

We use a technique called **component shadowing** to override an existing Volto component with our local custom version, without having to modify Volto's source code at all.
You have to place the replacing component in the same original folder path inside the `src/customizations` folder of your app.

Every time you add a file to the customizations folder or to the theme folder, you must restart Volto for changes to take effect.
From that point on, the hot reloading should kick in and reload the page automatically on changes.

You can customize any module in Volto, including actions and reducers, not only components.

The Volto code can be found in {file}`/omelette/`.

## The Logo

You can use this approach to change the Logo.

Create your own logo as a svg image or [download a logo](https://www.starzel.de/plone-tutorial/Logo.svg/@@download) and add it to your Volto app ({file}`frontend`) using this path and name: `src/customizations/components/theme/Logo/Logo.svg`.

After a restart of Volto ({kbd}`ctrl + c` and {kbd}`yarn start`) your page should look like this:

```{figure} _static/volto_customized_logo.png
:alt: The customized Logo.
```

## The Footer

Customize the footer by copying ``omelette/src/components/theme/Footer/Footer.jsx`` to your customization folder at ``src/customizations/components/theme/Footer/Footer.jsx``
After a restart you can change this Footer component and the changes are shown immediately due to hot reloading.


## The News Item View

We want to show the date a News Item is published.
This way visitors can see at a glance if they are looking at current or old news.

This information is not shown by default.
So you need to customize the way a News Item is rendered.

The Volto component to render a News Item is in `/omelette/src/components/theme/View/NewsItemView.jsx`.

```{code-block} jsx
:linenos:
/**
 * NewsItemView view component.
 * @module components/theme/View/NewsItemView
 */

import React from 'react';
import PropTypes from 'prop-types';
import { Container, Image } from 'semantic-ui-react';
import {
  hasBlocksData,
  flattenToAppURL,
  flattenHTMLToAppURL,
} from '@plone/volto/helpers';
import RenderBlocks from '@plone/volto/components/theme/View/RenderBlocks';

/**
 * NewsItemView view component class.
 * @function NewsItemView
 * @params {object} content Content object.
 * @returns {string} Markup of the component.
 */
const NewsItemView = ({ content }) =>
  hasBlocksData(content) ? (
    <div id="page-document" className="ui container viewwrapper event-view">
      <RenderBlocks content={content} />
    </div>
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
          className="documentImage"
          alt={content.title}
          title={content.title}
          src={
            content.image['content-type'] === 'image/svg+xml'
              ? flattenToAppURL(content.image.download)
              : flattenToAppURL(content.image.scales.mini.download)
          }
          floated="right"
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
- `content` is passed to `NewsItemView` and represents the content item as it is serialized by the REST API.

- The view displays various attributes of the News Item using `content.title`, `content.description` or `content.text.data`

- You can inspect all data that `content` holds using the React Developer Tools for [Firefox](https://addons.mozilla.org/de/firefox/addon/react-devtools/) or [Chrome](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi):

```{figure} _static/volto_react_devtools.png
:align: center
```
````

Copy that file into `src/customizations/components/theme/View/NewsItemView.jsx`.

After restarting Volto, the new file is used when displaying a News Item.
To make sure your file is used, add a small change before the blocks `<RenderBlocks content={content} />`.
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
Not very user friendly.
Let's use one of many helpers available in Volto.

Import the component `FormattedDate` from `@plone/volto/components` at the top of the file and use it to format the date in a readable format.

```{code-block} jsx
:emphasize-lines: 14,26-28
:linenos:

/**
 * NewsItemView view component.
 * @module components/theme/View/NewsItemView
 */

import React from 'react';
import PropTypes from 'prop-types';
import { Container, Image } from 'semantic-ui-react';
import {
  hasBlocksData,
  flattenToAppURL,
  flattenHTMLToAppURL,
} from '@plone/volto/helpers';
import { FormattedDate } from '@plone/volto/components';
import RenderBlocks from '@plone/volto/components/theme/View/RenderBlocks';

/**
 * NewsItemView view component class.
 * @function NewsItemView
 * @params {object} content Content object.
 * @returns {string} Markup of the component.
 */
const NewsItemView = ({ content }) =>
  hasBlocksData(content) ? (
    <div id="page-document" className="ui container viewwrapper event-view">
      <p>
        <FormattedDate date={content.created} includeTime />
      </p>
      <RenderBlocks content={content} />
    </div>
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
          className="documentImage"
          alt={content.title}
          title={content.title}
          src={
            content.image['content-type'] === 'image/svg+xml'
              ? flattenToAppURL(content.image.download)
              : flattenToAppURL(content.image.scales.mini.download)
          }
          floated="right"
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

Now another issue appears. There are various dates associated with any content object:

- The date the item is created: `content.created`
- The date the item is last modified `content.modified`
- The date the item is published `content.effective`

In fact you most likely want to show the date when the item was published.
But while the item is not yet published, that value is not yet set and you will get a error.
So we'll add some simple logic to use the effective date only if it exists.

```jsx
{content.review_state === 'published' && content.effective && (
  <p>
    <FormattedDate date={content.effective} includeTime />
  </p>
)}
```

As we are in the HTML part of our React component, we surround the JavaScript code with curly braces.
Inside Javascript we embrace html in rounded braces.


## The Listing Block

When you edited the frontpage in {ref}`features-content-types-label`, you may have added a Listing block to the frontpage. If not, please do so now.

You will see that the listing block does not display the date as well.

Copy `omelette/src/components/manage/Blocks/Listing/DefaultTemplate.jsx` to `src/customizations/components/manage/Blocks/Listing/DefaultTemplate.jsx` and add the date inside the iteration over list items.

The React developer tools provide a selector to find the component we need to override.

```{figure} _static/inspect_components.png
:alt: A News Item with publishing date.
```

```{code-block} jsx
:emphasize-lines: 3,30-34
:linenos:

import React from 'react';
import PropTypes from 'prop-types';
import { ConditionalLink, FormattedDate } from '@plone/volto/components';
import { flattenToAppURL } from '@plone/volto/helpers';

import { isInternalURL } from '@plone/volto/helpers/Url/Url';

const DefaultTemplate = ({ items, linkTitle, linkHref, isEditMode }) => {
  let link = null;
  let href = linkHref?.[0]?.['@id'] || '';

  if (isInternalURL(href)) {
    link = (
      <ConditionalLink to={flattenToAppURL(href)} condition={!isEditMode}>
        {linkTitle || href}
      </ConditionalLink>
    );
  } else if (href) {
    link = <a href={href}>{linkTitle || href}</a>;
  }

  return (
    <>
      <div className="items">
        {items.map((item) => (
          <div className="listing-item" key={item['@id']}>
            <ConditionalLink item={item} condition={!isEditMode}>
              <div className="listing-body">
                <h4>{item.title ? item.title : item.id}</h4>
                {item.review_state === 'published' && item.effective && (
                  <p className="discreet">
                    <FormattedDate date={item.effective} includeTime />
                  </p>
                )}
                <p>{item.description}</p>
              </div>
            </ConditionalLink>
          </div>
        ))}
      </div>

      {link && <div className="footer">{link}</div>}
    </>
  );
};
DefaultTemplate.propTypes = {
  items: PropTypes.arrayOf(PropTypes.any).isRequired,
  linkMore: PropTypes.any,
  isEditMode: PropTypes.bool,
};
export default DefaultTemplate;
```

The result should look like this:

```{figure} _static/volto_customized_listing_block.png
:alt: The customized Listing Block.
```


## Summary

- Component shadowing allows you to modify and extend views and other components in Volto.
- It is a powerful feature for making changes without the need for complex configuration or maintaining a fork of the code.
- You need to restart Volto when you add a new override.

```{seealso}
Volto Hands-On training: {ref}`voltohandson-header-component-label`
```
