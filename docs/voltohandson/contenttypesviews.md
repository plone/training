---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(voltohandson-contenttypeview-label)=

# Content types Views

We will create a content type through the web to match the ones that might live in `plone.org`.
We will use them as base for further developments on the project.

## Success Story

Create this content type using `Control Panel`->\`\`Dexterity Content Types\`\`->\`\`Add new content type\`\`.
Name it `Success Story`, then select it, got to the `Behaviors` tab, and add the `Tiles` and the `Lead Image` behaviors.

## Creating a view for a custom content type

Create a new file in `src/components/Views/SuccessStory.jsx`. Let's start simple:

```jsx
import React from 'react';

const SuccessStoryView = props => {
  return <div>I'm the SuccessStoryView component!</div>;
};

export default SuccessStoryView;
```

Then add to the configuration object:

```js
import SuccessStory from "@package/components/Views/SuccessStory";

...

export const views = {
  ...defaultViews,
  contentTypesViews: {
    ...defaultViews.contentTypesViews,
    success_story: SuccessStory
  }
};
```

Create a new `Success Story` content type, fill the title and save. Your custom view should be in place.

## Completing the new view

Our recently created view needs to show sensible content now. Let's add it. Edit `src/components/Views/SuccessStory.jsx`:

```{code-block} jsx
:emphasize-lines: 2,5

 import React from 'react';
 import { DefaultView } from '@plone/volto/components';

 const SuccessStoryView = props => {
   return <DefaultView {...props} />;
 };

 export default SuccessStoryView;
```

We are composing our view with Volto's default view component `DefaultView.jsx` to achieve the same features as the original one.
We might want to add stuff on the top or at the bottom.
In this case, `DefaultView.jsx` is rendering the existing blocks, however, we can have a content type with no blocks defined, then we can also modify what fields will show and how using plain JSX.
On `plone.org`, the Success Story content type uses the lead image as banner on the top. Let's achieve that:

```jsx
import React from 'react';
import { DefaultView } from '@plone/volto/components';
import { flattenToAppURL } from '@plone/volto/helpers';

const SuccessStoryView = props => {
  const { content } = props;
  return (
    <>
      <img
        className="lead image"
        alt={content.image_caption}
        src={flattenToAppURL(content.image.download)}
      />
      <DefaultView {...props} />
    </>
  );
};

export default SuccessStoryView;
```

and companion styling, for now removing breadcrumbs here as well:

```less
.contenttype-success_story {
  .ui.basic.segment.header-wrapper {
    margin: 0;
  }

h1.documentFirstHeading {
  margin-bottom: 0;
  border: none;
  color: #00608c;
  font-size: 4.5em;
  line-height: 1.25em;

  &::before {
    display: none;
  }
}

.lead.image {
    width: 100%;
  }
}
```

We can add any other field from the content type to the page, we only need to give it structure and styling, as desired.
