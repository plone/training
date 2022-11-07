---
myst:
  html_meta:
    "description": "Learn how to create a slideshow Block"
    "property=og:description": "Learn how to create a slideshow Block"
    "property=og:title": "Highlight Block"
    "keywords": "Plone, Volto, Training, Blocks, Highlight"
---

# Blocks - Highlight Block

The most prominent element on the `plone.org` page is the highlight block advertising the conference

We already have a basic block boilerplate from the last section. We will conver this now to a static non-configurable block that is thought as a one-of for the conference.

## Block view component

Copy `2022-ploneconf.png` from the `training-resources` folder to `src/components/Blocks/highlight` directory.

Use this code for the block view component `src/components/Blocks/highlight/View.jsx`.

```jsx
import React from "react";
import { Container } from "semantic-ui-react";
import ploneConfImg from "./2022-ploneconf.png";

const HighlightView = (props) => {
  return (
    <div className="full-width">
      <div className="block highlight">
        <Container className="inner">
          <h1>Plone - The Ultimate Enterprise CMS</h1>
          <a href="https://2022.ploneconf.org">
            <img src={ploneConfImg} alt="2022 plone conf" />
          </a>
          <h2>Join the Plone Conference 2022 in Namur, Belgium!</h2>
          <a className="ui button" href="https://2022.ploneconf.org/tickets">
            Get your tickets now!
          </a>
        </Container>
      </div>
    </div>
  );
};

export default HighlightView;
```

We should have the highlight block in the home page now.
For now we will leave out how the edit component would look like for a later chapter.

## Block edit

So far th Block will only look as expected in the View mode of a page. To also see the slider in the View you can simply import the `View` Component of the Block into the edit and render it there:

```js
import React from "react";
import View from "./View";

const HighlightEdit = (props) => {
  return <View {...props} />;
};

export default HighlightEdit;
```

## Styling

To style the block uses this styling:

```less
// full width-blocks
.full-width {
  max-width: none !important;
  margin-right: -50vw !important;
  margin-left: -50vw !important;
}
// highlight

.block.highlight {
  display: flex;
  width: 100% !important;
  justify-content: center;
  background: #113156;
  padding-top: 68px;
  padding-bottom: 48px;
  .inner {
    text-align: center;
    color: @white;
    a.ui.button {
      background: #1f9092;
      color: @white;
    }
  }
}
```

Now your Block should now look at least very similar to the original on `plone.org`.
