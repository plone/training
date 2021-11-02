---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(voltohandson-blocksmainslider-label)=

# Blocks - Main Slider

The old [plone.com](https://web.archive.org/web/20210813064319/https://plone.com/) had a main slider on the front page that we will implement using a Volto block.
For simplicity we will use static content for this block, but eventually we could populate the contents for each slide using actual site content or some other arbitrarily sophisticated means.

We already have a basic block boilerplate from the last section.
For the slider feature, we will install a third party library that will provide a component that will take care of it.

## Install react-slick

We will use the react-slick library to help us animating a slider at the top of the page. To install it to your project run:

```shell
yarn add -W react-slick slick-carousel
```

## Add library styles

It's common that third party libraries provide their own default styling.
You should add this styling to the build.
Add the `slick-carousel` styles to the `theme/extras/custom.overrides`:

```less
@import (less) "~slick-carousel/slick/slick.css";
@import (less) "~slick-carousel/slick/slick-theme.css";
```

## Block view component

Copy `slider-image.png` from the `training-resources` folder to `src/components/Blocks/MainSlider` directory.

Use this code for the block view component `src/components/Blocks/MainSlider/View.jsx`.

```jsx
import React from "react";
import Slider from "react-slick";
import { Link } from "react-router-dom";
import { Button } from "semantic-ui-react";
import { Icon } from "@plone/volto/components";
import sliderPNG from "./slider-image.png";
import rightSVG from "@plone/volto/icons/right-key.svg";
import leftSVG from "@plone/volto/icons/left-key.svg";
import { withBlockExtensions } from "@plone/volto/helpers";

const NextArrow = ({ className, style, onClick }) => (
  <Button
    className={className}
    style={{ ...style, display: "block" }}
    onClick={onClick}
  >
    <Icon name={rightSVG} size="70px" color="#fff" />
  </Button>
);

const PrevArrow = ({ className, style, onClick }) => (
  <Button
    className={className}
    style={{ ...style, display: "block" }}
    onClick={onClick}
  >
    <Icon name={leftSVG} size="70px" color="#fff" />
  </Button>
);

const View = (props) => {
  return (
    <div
      className="block view mainslider full-width"
      style={{
        background: `url(${sliderPNG}) center no-repeat`,
      }}
    >
      <Slider
        customPaging={(dot) => <div />}
        dots={true}
        fade
        dotsClass="slick-dots slick-thumb"
        infinite
        speed={500}
        slidesToShow={1}
        slidesToScroll={1}
        nextArrow={<NextArrow />}
        prevArrow={<PrevArrow />}
      >
        <div>
          <div className="slide slide1">
            <h3>Plone</h3>
            <h1>
              The Ultimate <br />
              Open Source Enterprise CMS
            </h1>
            <Link to="/plone5">Learn about Plone 5</Link>
          </div>
        </div>
        <div>
          <div className="slide slide1">
            <h3>Plone 5.2</h3>
            <h1>
              The Future-Proofing Release: <br />
              Python 3 and REST API
            </h1>
            <Link to="/plone52">Learn about Plone 5.2</Link>
          </div>
        </div>
      </Slider>
    </div>
  );
};

export default withBlockExtensions(View);
```

We should have the main slider block in the home page now.
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

To style the block uses this styling:

```less
.ui.basic.segment.content-area {
  padding: 0;
  margin: 0;
}

.block.view.mainslider {
  .slide {
    display: flex;
    height: 339px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #fff;

    h1 {
      margin: 0 0 20px 0;
      font-size: 32px;
      font-weight: 700;
      text-align: center;
    }

    h3 {
      margin: 0 0 20px 0;
      font-size: 32px;
      font-weight: 300;
    }

    a {
      padding: 10px 20px;
      background-color: #00bef1;
      border-radius: 20px;
      color: #fff;
    }
  }

  .slick-arrow {
    width: initial;
    height: initial;
  }

  .slick-prev {
    z-index: 10;
    left: -18px;
    background: transparent !important;

    &::before {
      display: none;
    }
  }

  .slick-next {
    right: -32px;
    background: transparent !important;

    &::before {
      display: none;
    }
  }
}

body.has-toolbar .block.view.mainslider .slick-prev {
  left: calc(-18px + 80px);
}

body.has-toolbar .block.view.mainslider .slick-next {
  right: calc(80px - 38px);
}

.slick-slider {
  width: 100vw;

  img {
    width: 100%;
  }
}

body:not(.has-toolbar):not(.has-sidebar):not(.has-toolbar-collapsed):not(.has-sidebar-collapsed)
  .ui.wrapper
  > .full-width,
body.has-toolbar:not(.has-sidebar):not(.has-sidebar-collapsed)
  .ui.wrapper
  > .full-width,
body.has-toolbar-collapsed:not(.has-sidebar):not(.has-sidebar-collapsed)
  .ui.wrapper
  > .full-width {
  position: relative;
  right: 50%;
  left: 50%;
  width: 100vw !important;
  max-width: initial !important;
  margin-right: -50vw !important;
  margin-left: -50vw !important;
}
```

## Remove the Title block

By default, `plone.voltodemo` sets a homepage by default with a title and a description block.
Notice that the title block can't be removed.
This is by design, but it can be overriden in the applyConfig function:

```js
config.blocks.requiredBlocks = [];
```

at least for a moment, to remove the title block from the homepage.
After that you choose to leave the default or not.
You can also create setuphandlers or Generic Setup steps to populate the initial default blocks in your site.
