---
myst:
  html_meta:
    "description": "How to support extensions per teaser block"
    "property=og:description": "How to support extensions per teaser block"
    "property=og:title": "Block Extensions"
    "keywords": "Volto, Block, Variations"
---

# Extending Teasers per type

The basic scenario is to add variations to a block so that it can give control over its look and feel. Sometimes its also possible for a need to have control over individual elements. For instance, Consider we have a teaaser grid in which we can have a base variation of its layout. Then we would left with styling and adjusting individual teasers. This is where extensions come into play.

In this chapter we will tweak our newly created variation to also support extensions per teaser block and then later we will add grid support to teasers.

## Block Extensions

Block extensions are the way to display a new form of your block for a particular block type. For instance if you have a teaserGrid, with block extensions you can control the styling and behaviour of individual teasers. The split of responsibilites is as follows: "the variation will control how the teasers layout and extension will control the individual rendering."

We already learn about the block variation in the former chapters. We will now add the teaser block extenttions the same way we do for variations.

```js
config.blocks.blocksConfig.teaser.extensions = {
  ...(config.blocks.blocksConfig.teaser.extensions || {}),
  cardTemplates: {
    items: [
      {
        id: "card",
        isDefault: true,
        title: "Card (default)",
        template: TeaserBlockImageDefault,
      },
      {
        id: "imageOnRight",
        isDefault: false,
        title: "Image Right",
        template: TeaserBlockImageRight,
      },
      {
        id: "imageOverlay",
        isDefault: false,
        title: "Image Overlay",
        template: TeaserBlockImageOverlay,
      },
    ],
  },
};
```

As for the training we created only three extensions namely `TeaserBlockImageDefault`, `TeaserBlockImageRight` and `TeaserBlockImageOverlay`.

In order to support these extension first we need to add a special fieldset to our variation schema so that we can seperate the concerns about individual teasers and put these extensions under it.

Luckily, In order to do that we have a helper in volto which automatic adds a select field where we want in the schema to display variations/extensions from a particualar block. As its a standalone method we can also add a variation from a completely different block like we do in SearchBlock in volto.

Go ahead and register that in index.js in our variation schemaEnhancer:

```jsx
import { addExtensionFieldToSchema } from '@plone/volto/helpers/Extensions/withBlockSchemaEnhancer';

config.blocks.blocksConfig.teaser.variations = [
    ...config.blocks.blocksConfig.teaser.variations,
    {
      id: 'image-top-variation',
      title: 'Image(Top) variation',
      template: TeaserBlockImageVariation,
      isDefault: false,
      schemaEnhancer: ({ schema, FormData, intl }) => {
        const extension = 'cardTemplates';
        schema.fieldsets.push({
          id: 'Cards',
          title: 'Cards',
          fields: [],
        });
        addExtensionFieldToSchema({
          schema,
          name: extension,
          items: config.blocks.blocksConfig.teaser.extensions[extension]?.items,
          intl,
          title: { id: 'Card Type' },
          insertFieldToOrder: (schema, extension) => {
            const cardFieldSet = schema.fieldsets.find(
              (item) => item.id === 'Cards',
            ).fields;
            if (cardFieldSet.indexOf(extension) === -1)
              cardFieldSet.unshift(extension);
          },
        });
        ...
```

Notice first we added a new fieldSet where our extensions will recide and the method `addExtensionFieldToSchema` imported volto core. This method as mentioned above adds a new field in the given fieldSet with the given extenionName `cardTemplates`.

```{note}
By default ``addExtensionFieldToSchema` adds the extewnsion field to default fieldSet, in order to ovverride that you can pass `insertFieldToOrder` method to specifiy where it should be added.

```

Woot. We will now have our extensions loaded into the schema. We will have to refactor our intial Variation code to adapt the extension now.

```{note}
The concept of extensions are only possible if the code of your block allows it. That is the reason why we created a variation out of a teaser block at the first place.
```

So our `TeaserBlockImageVariation` can be simplified now as:

```jsx
import React from "react";
import PropTypes from "prop-types";
import { useIntl } from "react-intl";
import cloneDeep from "lodash/cloneDeep";
import config from "@plone/volto/registry";

const TeaserBlockImageVariation = (props) => {
  const { data, extension = "cardTemplates" } = props;
  const intl = useIntl();

  const teaserExtenstions =
    config.blocks.blocksConfig?.teaser?.extensions[extension].items;
  let activeItem = teaserExtenstions.find(
    (item) => item.id === data[extension]
  );
  const extenionSchemaEnhancer = activeItem?.schemaEnhancer;
  if (extenionSchemaEnhancer)
    extenionSchemaEnhancer({
      schema: cloneDeep(config.blocks.blocksConfig?.teaser?.blockSchema),
      data,
      intl,
    });
  const ExtensionToRender = activeItem?.template;

  return ExtensionToRender ? (
    <div>
      <ExtensionToRender {...props} />
    </div>
  ) : null;
};

TeaserBlockImageVariation.propTypes = {
  data: PropTypes.objectOf(PropTypes.any).isRequired,
  isEditMode: PropTypes.bool,
};

export default TeaserBlockImageVariation;
```

We have added the "active extension" logic to this code and removed the templating code to their individual components under `extensions/` folder.
Notice that we can also add more schema Enhancers to our base variation schema if each extensions can provide it.

The `ExtensionToRender` will be selected extensions from `extensions/` folder.

Create a folder named `extensions/` within `components` and add three components provided below:

TeaserBlockImageDefault:

```jsx
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
  const creationDate = data.href?.[0]?.CreationDate;
  const formattedDate = formatDate({
    date: creationDate,
    format: {
      year: "numeric",
      month: "short",
      day: "2-digit",
    },
    locale: locale,
  });

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
                {data.creationDate && <p>{formattedDate}</p>}
                {!data.hide_description && <p>{data?.description}</p>}
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

TeaserBlockImageRight:

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

const TeaserBlockImageRight = (props) => {
  const { className, data, isEditMode } = props;
  const locale = config.settings.dateLocale || "en";
  const intl = useIntl();
  const href = data.href?.[0];
  const image = data.preview_image?.[0];
  const align = data?.styles?.align;
  const creationDate = data.href?.[0]?.CreationDate;
  const formattedDate = formatDate({
    date: creationDate,
    format: {
      year: "numeric",
      month: "short",
      day: "2-digit",
    },
    locale: locale,
  });

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
              <div className="content">
                {data?.head_title && (
                  <div className="headline">{data.head_title}</div>
                )}
                <h2>{data?.title}</h2>
                {data.creationDate && <p>{formattedDate}</p>}
                {!data.hide_description && <p>{data?.description}</p>}
              </div>
              {(href.hasPreviewImage || href.image_field || image) && (
                <div className="image-wrapper">
                  <Image
                    src={hasImageComponent ? href : defaultImageSrc}
                    alt=""
                    loading="lazy"
                  />
                </div>
              )}
            </div>
          </MaybeWrap>
        )}
      </>
    </div>
  );
};

TeaserBlockImageRight.propTypes = {
  data: PropTypes.objectOf(PropTypes.any).isRequired,
  isEditMode: PropTypes.bool,
};

export default TeaserBlockImageRight;
```

TeaserBlockImageOverlay:

```{code-block} jsx

import React from "react";
import PropTypes from "prop-types";
import { Message } from "semantic-ui-react";
import { defineMessages, useIntl } from "react-intl";
import cloneDeep from "lodash/cloneDeep";
import imageBlockSVG from "@plone/volto/components/manage/Blocks/Image/block-image.svg";
import { flattenToAppURL, isInternalURL } from "@plone/volto/helpers";
import { getTeaserImageURL } from "@plone/volto/components/manage/Blocks/Teaser/utils";
import { MaybeWrap } from "@plone/volto/components";
import { formatDate } from "@plone/volto/helpers/Utils/Date";
import { UniversalLink } from "@plone/volto/components";
import cx from "classnames";
import config from "@plone/volto/registry";
import "./styles.less";

const messages = defineMessages({
  PleaseChooseContent: {
    id: "Please choose an existing content as source for this element",
    defaultMessage:
      "Please choose an existing content as source for this element",
  },
});

const DefaultImage = (props) => <img {...props} alt={props.alt || ""} />;

const TeaserBlockImageOverlay = (props) => {
  const { className, data, isEditMode, extension = "cardTemplates" } = props;
  const locale = config.settings.dateLocale || "en";
  const intl = useIntl();
  const href = data.href?.[0];
  const image = data.preview_image?.[0];
  const align = data?.styles?.align;
  const creationDate = data.href?.[0]?.CreationDate;
  const formattedDate = formatDate({
    date: creationDate,
    format: {
      year: "numeric",
      month: "short",
      day: "2-digit",
    },
    locale: locale,
  });

  const teaserExtenstions =
    config.blocks.blocksConfig?.teaser?.extensions[extension].items;
  let activeItem = teaserExtenstions.find(
    (item) => item.id === data[extension]
  );
  const extenionSchemaEnhancer = activeItem?.schemaEnhancer;
  if (extenionSchemaEnhancer)
    extenionSchemaEnhancer({
      schema: cloneDeep(config.blocks.blocksConfig?.teaser?.blockSchema),
      data,
      intl,
    });

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
            <div className="teaser-item overlay">
              {(href.hasPreviewImage || href.image_field || image) && (
                <div className="image-wrapper">
                  <Image
                    src={hasImageComponent ? href : defaultImageSrc}
                    alt=""
                    loading="lazy"
                  />
                </div>
              )}

              <div className="gradiant">
                {data?.head_title && (
                  <div className="headline">{data.head_title}</div>
                )}
                <div style={{ display: "flex", flexDirection: "column" }}>
                  <h2>{data?.title}</h2>
                  {!data.hide_description && <p>{data?.description}</p>}
                  {data?.creationDate && (
                    <p style={{ color: "white" }}>{formattedDate}</p>
                  )}
                </div>
              </div>
            </div>
          </MaybeWrap>
        )}
      </>
    </div>
  );
};

TeaserBlockImageOverlay.propTypes = {
  data: PropTypes.objectOf(PropTypes.any).isRequired,
  isEditMode: PropTypes.bool,
};

export default TeaserBlockImageOverlay;
```

The styles.less is to be created as well:

```{code-block} less
:force: true

.gradiant {
  h2 {
    color: white;
  }
  position: absolute;
  bottom: 30px;
  display: flex;
  width: 100%;
  height: 200px;
  align-items: flex-end;
  padding: 1.5rem;
  background-image: linear-gradient(
    13.39deg,
    rgba(46, 62, 76, 0.65) 38.6%,
    rgba(46, 62, 76, 0.169) 59.52%,
    rgba(69, 95, 106, 0) 79.64%
  );
}

.teaser-item.overlay {
  display: flex;

  .image-wrapper {
    width: 100%;
  }
}

.has--objectFit--contain {
  img {
    object-fit: contain !important;
  }
}

.has--objectFit--cover {
  img {
    object-fit: cover !important;
  }
}

.has--objectFit--fill {
  img {
    object-fit: fill !important;
  }
}

.has--objectFit--scale-down {
  img {
    object-fit: scale-down !important;
  }
}
```

Great. We now have extension per teaser in our block which controls each item individually.

## Grid support to Teasers

As mentioned before we will add grid support in our project to be able to have a whole `teaserGrid` working properly along with our extended code. In order to demonstrate it, we need to list teasers in grid system. We'll use `@kitconcept/volto-blocks-grid` for that and extend it in our own ways.

First add `@kitconcept/volto-blocks-grid` in addons key and dependencies in package.json of your project's config.

In your project's config:

```{code-block} js
addons: [
    "@kitconcept/volto-blocks-grid",
     "volto-teaser-tutorial",
]

dependencies: [
    "@kitconcept/volto-blocks-grid": "*"
]
```

```{note}
Its essential that we load `volto-teaser-tutorial` after volto-blocks-grid so that we overrride teaser block the right way.
```

Now since, grid block from `@kitconcept/volto-blocks-grid` uses teaser from its blocksConfig we need to override it with our teaser block so that it is used instead of the one in `@kitconcept/volto-blocks-grid`.

In your volto-teaser-tutorial addon's `index.js`:

```{code-block} js
if (
  config.blocks.blocksConfig?.__grid?.blocksConfig?.teaser &&
  config.blocks.blocksConfig?.teaser
) {
  //This ensures that grid block uses our overrideen teaser
  config.blocks.blocksConfig.__grid.blocksConfig.teaser =
    config.blocks.blocksConfig.teaser;
}
```

Woot. We will now have a grid block with our teaser variations so that each teaser can now have its own set of extensions.
