---
myst:
  html_meta:
    "description": "How to work with block variations schema"
    "property=og:description": "How to work with block variations schema"
    "property=og:title": "Teaser block variations Schema"
    "keywords": "Volto, Blocks, Variations, schemaEnhancers"
---

# Teaser block variations Schema

Now that we have learnt on how to add a new variation to a teaser block. Sometimes its important to also have schemas of those variations merged into the main schema. So each variation can come up with its own set of schema. We can use `schemaEnhancers` for this purpose.

schemaEnhancers works on the concept of composition. They are just functions which take original schema, formdata and intl and return modified schema based on its arguments.

In our variation, let's add a schemaEnhancer to modify existing schema and add a `CreationDate` from catalog metadata brain.

```js
config.blocks.blocksConfig.teaser.variations = [
  ...config.blocks.blocksConfig.teaser.variations,
  {
    id: "image-top-variation",
    title: "Image(Top) variation",
    template: TeaserBlockImageVariation,
    isDefault: false,
    schemaEnhancer: ({ schema, FormData, intl }) => {
      schema.fieldsets[0].fields.push("creationDate");
      schema.properties.creationDate = {
        title: "Show creation Date",
        type: "boolean",
      };
      schema.properties.href.selectedItemAttrs.push("CreationDate");
      return schema;
    },
  },
];
```

And then in your code of that variation, you should consume that field accordingly.

```js
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
```

`data.href` contains the catalog brain properties which are requested via `selectedItemAttrs`. CreationDate is one of them. Notice we are using formatDate from Volto helpers which is used to parse date into respective formats on the basis of locales.

Finally render it conditionally on the basis of `data.creationDate`

```jsx
{
  data?.creationDate && <p style={{ color: "white" }}>{formattedDate}</p>;
}
```

The whole component looks like:

```jsx
import React from "react";
import PropTypes from "prop-types";
import { Message } from "semantic-ui-react";
import { defineMessages, useIntl } from "react-intl";
import imageBlockSVG from "@plone/volto/components/manage/Blocks/Image/block-image.svg";
import { flattenToAppURL, isInternalURL } from "@plone/volto/helpers";
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

  const Image = config.getComponent("Image").component || DefaultImage;
  const { openExternalLinkInNewTab } = config.settings;

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
                    item={props["@type"] === "listing" ? null : image || href}
                    src={
                      props["@type"] === "listing"
                        ? addAppURL(`${href}/${image?.download}`)
                        : null
                    }
                    imageField={image ? image.image_field : href.image_field}
                    alt=""
                    loading="lazy"
                    responsive={true}
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
