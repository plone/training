(volto-overrides-label)=

# Customizing Volto Components

````{sidebar} Volto chapter
```{figure} _static/volto.svg
:alt: Volto Logo
:align: left
```

This chapter is about the React frontend Volto.

Solve the same tasks in Plone Classic in chapter {doc}`zpt_2`

---

**Get the code! ({doc}`More info <code>`)**

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
You have to place the replacing component in the same original folder path inside the `src/customizations` folder.

Every time you add a file to the customizations folder or to the theme folder, you must restart Volto for changes to take effect. From that point on, the hot reloading should kick in and reload the page automatically.

```{note}
Component shadowing is very much like the good old Plone technique called "JBOT" ("just a bunch of templates").

You can customize any module in Volto, including actions and reducers, not only components.
```

## The Logo

You can use this approach to change the Logo.
Create your own logo or download the logo from <https://www.starzel.de/plone-tutorial/Logo.svg/@@download> and add it to your Volto package ({file}`frontend`) using this path and name: `src/customizations/components/theme/Logo/Logo.svg`.

After a restart of Volto ({kbd}`ctrl + c` and {kbd}`yarn start`) your page should look like this:

```{figure} _static/volto_customized_logo.png
:alt: The customized Logo.
```

## The Footer

```{eval-rst}
.. todo::

    Customize the footer:

    * Copy ``omelette/src/components/theme/Footer/Footer.jsx`` to ``src/customizations/components/theme/Footer/Footer.jsx``
    * Restart Volto
    * Change something

```

## The News Item View

We want to show the date a News Item is published.
This way visitors can see at a glance if they are looking at current or old news.

This information is not shown by default.
So you will need to customize the way that is used to render a News Item.

The Volto component to render a News Item is in `omelette/src/components/theme/View/NewsItemView.jsx` (remember  chapter {ref}`volto-basics-label`?).

```jsx
/**
 * NewsItemView view component.
 * @module components/theme/View/NewsItemView
 */

import React from 'react';
import PropTypes from 'prop-types';
import { Container, Image } from 'semantic-ui-react';

import { flattenToAppURL, flattenHTMLToAppURL } from '@plone/volto/helpers';

/**
 * NewsItemView view component class.
 * @function NewsItemView
 * @params {object} content Content object.
 * @returns {string} Markup of the component.
 */
const NewsItemView = ({ content }) => (
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

After restarting Volto the new file is used when displaying a News Item.
To make sure your file is used add a small change before or after the text.
If it shows up you're good to go.

In you own projects you shoud always do a commit of the unchanged file and another commit after you changed the file.
This way you will have a commit in your git-history with the change you made.
You will thank yourself later for that clean diff!

To display the date add the following before the text:

```jsx
<p>{content.created}</p>
```

This will render something like `2020-10-19T10:51:21`.
Not very user friendly.
Let's use one of many helpers available in React.

Import the library [moment](https://momentjs.com/) at the top of the file and use it to format the date in a readable format.

```{code-block} jsx
:emphasize-lines: 9,44

/**
 * NewsItemView view component.
 * @module components/theme/View/NewsItemView
 */

import React from 'react';
import PropTypes from 'prop-types';
import { Container, Image } from 'semantic-ui-react';
import moment from 'moment';

import { flattenToAppURL, flattenHTMLToAppURL } from '@plone/volto/helpers';

/**
 * NewsItemView view component class.
 * @function NewsItemView
 * @params {object} content Content object.
 * @returns {string} Markup of the component.
 */

const NewsItemView = ({ content }) => (
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
    <p>{moment(content.created).format('ll')}</p>
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
But while the item is not yet published that value is not yet set and you will get a error.
So we'll add some simple logic to use the effective-date if it exists and the creation-date as a fallback.

```jsx
<p className="discreet">
  {(content.effective && moment(content.effective).format('ll')) ||
    moment(content.created).format('ll')}
</p>
```

## The Summary View

The listing of News Items in <http://localhost:3000/news> does not show any dates as well.

Customize the Summary View component that exists in `omelette/src/components/theme/View/SummaryView.jsx`.

Copy that file to `src/customizations/components/theme/View/SummaryView.jsx` and add the following after the description:

```jsx
<p className="discreet">
  {(item.effective && moment(item.effective).format('ll')) ||
    moment(item.created).format('ll')}
</p>
```

Don't forget to add the import of moment: `import moment from 'moment';` at the top.

Note how the component iterates over the variable `items` of `content`  with `{content.items.map((item) => (...)}`. Here `item` is the item in the Folder or Collection where this component is used.

## The Listing Block

When you edited the frontpage in {ref}`features-content-types-label` you may have added a Listing block to the frontpage. If not do so now.

You will see that the listing block does not display the date as well.

Copy `omelette/src/components/manage/Blocks/Listing/DefaultTemplate.jsx` to `src/customizations/components/manage/Blocks/Listing/DefaultTemplate.jsx` and add the dates as you did with the Summary View.

```{code-block} jsx
:emphasize-lines: 5,31-34
:linenos: true

import React from 'react';
import PropTypes from 'prop-types';
import { ConditionalLink } from '@plone/volto/components';
import { flattenToAppURL } from '@plone/volto/helpers';
import moment from 'moment';

import { isInternalURL } from '@plone/volto/helpers/Url/Url';

const DefaultTemplate = ({ items, linkMore, isEditMode }) => {
  let link = null;
  let href = linkMore?.href || '';

  if (isInternalURL(href)) {
    link = (
      <ConditionalLink to={flattenToAppURL(href)} condition={!isEditMode}>
        {linkMore?.title || href}
      </ConditionalLink>
    );
  } else if (href) {
    link = <a href={href}>{linkMore?.title || href}</a>;
  }

  return (
    <>
      <div className="items">
        {items.map((item) => (
          <div className="listing-item" key={item['@id']}>
            <ConditionalLink item={item} condition={!isEditMode}>
              <div className="listing-body">
                <h4>{item.title ? item.title : item.id}</h4>
                <p>
                  {(item.effective && moment(item.effective).format('ll')) ||
                    moment(item.created).format('ll')}
                </p>
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

## Localization

The result is fine if you have an english-speaking website but for other locales you want to configure `moment` to use your locale.
You could set it by hand with `moment.locale('fr');` (for french) but the code for this application should work with any language.

`NewsItemView` contains no code but directly returns the container.
You need to make a small change to allow setting the locale here.
Wrap the Container with `{}` and return the container.
Put the locale-setting before it.

```{code-block} jsx
:linenos: true
:emphasize-lines: 10,21-25,62

/**
 * NewsItemView view component.
 * @module components/theme/View/NewsItemView
 */

import React from 'react';
import PropTypes from 'prop-types';
import { Container, Image } from 'semantic-ui-react';
import moment from 'moment';
import { useIntl } from 'react-intl';

import { flattenToAppURL, flattenHTMLToAppURL } from '@plone/volto/helpers';

/**
 * NewsItemView view component class.
 * @function NewsItemView
 * @params {object} content Content object.
 * @returns {string} Markup of the component.
 */

const NewsItemView = ({ content }) => {
  const intl = useIntl();
  moment.locale(intl.locale);

  return (
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
      <p className="discreet">
        {(content.effective && moment(content.effective).format('lll')) ||
          moment(content.created).format('lll')}
      </p>
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

You can now do the same changes for the Summary View and the Listing Block. The Listing Block alread has some code in it so you would not need to wrap it in `{}` and add the `return ()` statement.

## Summary

- Component shadowing allows you to modify, extend and customize views in Volto.
- It is a powerful feature for making changes without the need for complex configuration or maintaining a fork of the code.
- You need to restart Volto when you add a new override.

```{seealso}
- <https://training.plone.org/5/volto/override-components.html>
- <https://training.plone.org/5/voltohandson/header.html#header-component>
- <https://training.plone.org/5/volto/override-views.html>
```
