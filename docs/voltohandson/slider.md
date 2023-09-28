---
myst:
  html_meta:
    "description": "Learn how to create a slideshow Block"
    "property=og:description": "Learn how to create a slideshow Block"
    "property=og:title": "Slider Block"
    "keywords": "Plone, Volto, Training, Blocks, Slider"
---

# Blocks - Slider Block

The most prominent element on the `plone.org` page is the Slider block with some of the latest news. As you are not quite ready yet to create a dynamic or editable block create a static version with screenhsots from the original as slides. I provided these in the [training ressources](https://github.com/plone/training/tree/main/docs/voltohandson/ressources)

We already have a basic block boilerplate from the last section. We will convert this now to a static non-configurable block that is thought as a one-of for the training.

## Block view component

Copy the slide 1-3 images from the [training-resources](https://github.com/plone/training/tree/main/docs/voltohandson/ressources) folder to `src/components/Blocks/Slider` directory.

Use this markup for the block view component `src/components/Blocks/slider/View.jsx`. We are using the `react-image-gallery` library to create a simple image carousel.

```jsx
import ImageGallery from 'react-image-gallery';
import Slide1Image from './slide1.png';
import Slide2Image from './slide2.png';
import Slide3Image from './slide3.png';

const View = (props) => {
  const slides = [
    {
      original: Slide1Image,
    },
    {
      original: Slide2Image,
    },
    {
      original: Slide3Image,
    },
  ];
  // we can't remove the nav arrows therefore we will use a workaround with empty markup
  const invisibleNav = () => {
    return <> </>;
  };

  return (
    <div className="block slider full-width">
      <ImageGallery
        items={slides}
        showFullscreenButton={false}
        showPlayButton={false}
        showBullets
        renderLeftNav={invisibleNav}
        renderRightNav={invisibleNav}
      />
    </div>
  );
};

export default View;
```

We should have the slider block in the home page now.
For now we will leave out how the edit component would look like for a later chapter.

## Block edit

So far th Block will only look as expected in the View mode of a page. To also see the slider in the View you can simply import the `View` Component of the Block into the edit and render it there:

```js
import React from "react";
import View from "./View";

const Edit = (props) => {
  return <View {...props} />;
};

export default Edit;
```

## Styling

To improve the style of the block add this to your `custom.overrides`:

```less
//slider block

.block.slider .image-gallery-content .image-gallery-slide .image-gallery-image {
    max-height: none;
  }

```

Now your Block should look at least very similar to the original on `plone.org`.
