---
myst:
  html_meta:
    "description": "How to approach the blocks schema and variations"
    "property=og:description": "How to approach the blocks schema and variations"
    "property=og:title": "Blocks schema and variations"
    "keywords": "Volto, Blocks, Schema"
---

# Blocks schema and variations

In the previous chapter we just replaced or enhanced our View component by directly mutating the View in the Blocks engine. Now since all the blocks in principle should be schema based and should use `BlockDataForm` we do have another concept of extending Blocks with respect to schema.

The `BlockDataForm` renders a schemaEnhanced form ready to be used along with the variations support.

The variations are various "View" mode options that your block might have whether its layout, the designs or a completely enhanced form of a block.

You may know the variations from the listing-block already:

```{image} _static/variations.png
:alt: The variations of the listing block
```

To create a new variation we don't need to shadow or customize the block.

So in the default schema for teaser block we have:

```js
 teaser: {
    id: 'teaser',
    title: 'Teaser',
    icon: imagesSVG,
    group: 'common',
    view: TeaserViewBlock,
    edit: TeaserEditBlock,
    restricted: false,
    mostUsed: true,
    sidebarTab: 1,
    blockSchema: TeaserSchema,
    dataAdapter: TeaserBlockDataAdapter,
    variations: [
      {
        id: 'default',
        isDefault: true,
        title: 'Default',
        template: TeaserBlockDefaultBody,
      },
    ],
  },
```

Notice the *variations* key, in which we can have multiple view templates for a given block. Right now its going to use the default one which is the [TeaserBlockDefaultBody](https://github.com/plone/volto/blob/985e419396b4d00567d12e7e309ea420012e9cc7/src/components/manage/Blocks/Teaser/DefaultBody.jsx#L1).

We are going to create a new variation of this teaser block. This variation is essential because using it we will create block extensions per teaser. Later we can also enhance this variation with the new schema.

Go ahead and extend the in the variations key of the teaser-block in `index.js` like this:

```js
import TeaserBlockImageVariation from 'volto-teaser-tutorial/components/TeaserBlockImageVariation';

const applyConfig = (config) => {
  // ...
  config.blocks.blocksConfig.teaser.variations = [
    ...config.blocks.blocksConfig.teaser.variations,
    {
      id: 'image-top-variation',
      title: 'Image(Top) variation',
      template: TeaserBlockImageVariation,
    },
  ]
  return config;
}

export default applyConfig;
```

We should create this view template in our `components/TeaserBlockImageVariation.jsx`

TeaserBlockImageVariation.jsx:

```{code-block} jsx

import React from "react";
import PropTypes from "prop-types";
import { Message } from "semantic-ui-react";
import { defineMessages, useIntl } from "react-intl";

import imageBlockSVG from "@plone/volto/components/manage/Blocks/Image/block-image.svg";

import { flattenToAppURL, isInternalURL } from "@plone/volto/helpers";
import { getTeaserImageURL } from "@plone/volto/components/manage/Blocks/Teaser/utils";
import { MaybeWrap } from "@plone/volto/components";
import { formatDate } from "@plone/volto/helpers/Utils/Date";
import { UniversalLink } from "@plone/volto/components";
import cx from "classnames";
import config from "@plone/volto/registry";

const messages = defineMessages({
  PleaseChooseContent: {
    id: "Please choose an existing content as source for this element",
    defaultMessage:
      "Please choose an existing content as source for this element",
  },
});

const DefaultImage = (props) => <img {...props} alt={props.alt || ""} />;

const TeaserBlockImageDefault = (props) => {
  const { className, data, isEditMode } = props;
  const locale = config.settings.dateLocale || "en";
  const intl = useIntl();
  const href = data.href?.[0];
  const image = data.preview_image?.[0];
  const align = data?.styles?.align;

  const hasImageComponent = config.getComponent("Image").component;
  const Image = config.getComponent("Image").component || DefaultImage;
  const { openExternalLinkInNewTab } = config.settings;
  const defaultImageSrc =
    href && flattenToAppURL(getTeaserImageURL({ href, image, align }));

  return (
    <div className={cx("block teaser", className)}>
      <>
        {!href && isEditMode && (
          <Message>
            <div className="teaser-item placeholder">
              <img src={imageBlockSVG} alt="" />
              <p>{intl.formatMessage(messages.PleaseChooseContent)}</p>
            </div>
          </Message>
        )}
        {href && (
          <MaybeWrap
            condition={!isEditMode}
            as={UniversalLink}
            href={href["@id"]}
            target={
              data.openLinkInNewTab ||
              (openExternalLinkInNewTab && !isInternalURL(href["@id"]))
                ? "_blank"
                : null
            }
          >
            <div className="teaser-item default">
              {(href.hasPreviewImage || href.image_field || image) && (
                <div className="image-wrapper">
                  <Image
                    src={hasImageComponent ? href : defaultImageSrc}
                    alt=""
                    loading="lazy"
                  />
                </div>
              )}
              <div className="content">
                {data?.head_title && (
                  <div className="headline">{data.head_title}</div>
                )}
                <h2>{data?.title}</h2>
              </div>
            </div>
          </MaybeWrap>
        )}
      </>
    </div>
  );
};

TeaserBlockImageDefault.propTypes = {
  data: PropTypes.objectOf(PropTypes.any).isRequired,
  isEditMode: PropTypes.bool,
};

export default TeaserBlockImageDefault;
```

After this you will be able to choose variations for this block from the Blocks Settings sidebar.
Right now this variation only shows default variation of Teaser block.
You could decide to modify the template here already though.
In the coming chapter we are gonna enhance this variation with extension per teaser.

```{note}
The [Body](https://github.com/plone/volto/blob/9667cf735e5c3e848de852d615941d98193e0a5e/src/components/manage/Blocks/Teaser/Body.jsx#L13) component in Teaser block also supports adding variations from component registry. You can read more about component registry in following chapters.
```
