---
myst:
  html_meta:
    "description": "Learn How to code a custom View for a content type"
    "property=og:description": "Learn How to code a custom View for a content type"
    "property=og:title": "Content Type Views"
    "keywords": "Plone, Volto, Training, View, Content Types"
---

(voltohandson-contenttypeview-label)=

# Content types Views

We will create a content type through the web to match the ones that might live in `plone.com`.
We will use them as base for further developments on the project.

## Success Story

Create this content type using the Dexterity content type control panel at <http://localhost:3000/controlpanel/dexterity-types>.
Name it `Success Story`, then select it, go to the `Behaviors` tab, and add the `Blocks` and the `Lead Image` behaviors.

## Creating a view for a custom content type

Create a new file in `src/components/Views/SuccessStory.jsx`. Let's start simple:

```jsx
import React from "react";

const SuccessStoryView = (props) => {
  return <div>I'm the SuccessStoryView component!</div>;
};

export default SuccessStoryView;
```

Export it again from via the index file:

```js
export SuccessStoryView from "./Views/SuccessStory";
```

Then add to the configuration object:

```js
import {
  MainSliderViewBlock,
  MainSliderEditBlock,
  SuccessStoryView,
} from '@package/components';
//...
applyConfig(config) {
  config.views.contentTypesViews.success_story = SuccessStoryView;
  //...
}
```

Create a new `Success Story` content type, fill the title and save. And upload the `successstory-lead-image` from the training ressources as lead image". Your custom view should now be in place.

## Completing the new view

Our recently created view needs to show sensible content now. Let's add it. Edit `src/components/Views/SuccessStory.jsx`:

```{code-block} jsx
:emphasize-lines: 2,5
import React from "react";
import { DefaultView } from "@plone/volto/components";

const SuccessStoryView = (props) => {
  return <DefaultView {...props} />;
};

export default SuccessStoryView;
```

We are composing our view with Volto's default view component `DefaultView.jsx` to achieve the same features as the original one.
We might want to add stuff on the top or at the bottom.
In this case, `DefaultView.jsx` is rendering the existing blocks, however, we can have a content type with no blocks defined, then we can also modify what fields will show and how using plain JSX.
On `plone.com`, the Success Story content type used the lead image as banner on the top. Let's achieve that:

```jsx
import React from "react";
import { DefaultView } from "@plone/volto/components";
import { flattenToAppURL } from "@plone/volto/helpers";

const SuccessStoryView = (props) => {
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
    border: none;
    margin-bottom: 0;
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
