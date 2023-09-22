### create a simple listing block variation

We will create a variation for listing block, the approach is the same we did for teasers. A new variation which will control the layout and extensions which will take care of individual items styling.

First of all let's add a styling fieldset in the current schema of volto's default listing block .

In your addon config:

```js
if (config.blocks.blocksConfig.listing) {
  config.blocks.blocksConfig.listing.title = "Listing (Tutorial)";
  config.blocks.blocksConfig.listing.schemaEnhancer = addStylingFieldset;
}
```

Create a file named `helpers.js` and add the relevant schema enhancer for it:

```js
import { cloneDeep } from "lodash";
import imageNarrowSVG from "@plone/volto/icons/image-narrow.svg";
import imageFitSVG from "@plone/volto/icons/image-fit.svg";
import imageWideSVG from "@plone/volto/icons/image-wide.svg";
import imageFullSVG from "@plone/volto/icons/image-full.svg";

export const ALIGN_INFO_MAP = {
  narrow_width: [imageNarrowSVG, "Narrow width"],
  container_width: [imageFitSVG, "Container width"],
  wide_width: [imageWideSVG, "Wide width"],
  full: [imageFullSVG, "Full width"],
};

export const addStylingFieldset = ({ schema }) => {
  const applied = schema?.properties?.styles;

  if (!applied) {
    const resSchema = cloneDeep(schema);

    resSchema.fieldsets.push({
      id: "styling",
      fields: ["styles"],
      title: "Styling",
    });
    resSchema.properties.styles = {
      widget: "object",
      title: "Styling",
      schema: {
        fieldsets: [
          {
            id: "default",
            title: "Default",
            fields: ["size"],
          },
        ],
        properties: {
          size: {
            widget: "align",
            title: "Section size",
            actions: Object.keys(ALIGN_INFO_MAP),
            actionsInfoMap: ALIGN_INFO_MAP,
          },
        },
        required: [],
      },
    };
    return resSchema;
  }

  return schema;
};
```

This function will inject styles field into the schema if isn't present already. We can add relevant styling here. Volto will build classNames based on the styles as mentioned in the earlier chapters. We will have to provide our own css for the generated classNames.

```less
#main .has--size--narrow_width,
#main .narrow_width,
[class~="narrow_view"] [id="page-document"] > * {
  max-width: var(--narrow-text-width, 500px) !important;
}

#main .container_width,
#main .has--size--container_width,
.view-wrapper > *,
[class~="view-defaultview"] [id="page-document"] > *,
[class~="view-viewview"] [id="page-document"] > * {
  max-width: var(--container-text-width, 1120px) !important;
}
```

In order to have a control over individual items in the listing let's create a sample variation of listing block.

```js
import ListingVariation from 'volto-teaser-tutorial/components/ListingBlockVariation';


 config.blocks.blocksConfig.listing.variations = [
    ...(config.blocks.blocksConfig.listing.variations || [])
    {
      id: 'tutorial',
      isDefault: false,
      title: 'Sample Variation',
      template: ListingVariation,
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
        return schema;
      },
    },
 ]

```

Notice that here we will keep the schemaEnhancer configuration of teaser extensions. For better readability we can also move these lines of code into a `baseSchemaEnhancer` which will serve for both listing and teaser block extensions. But we can leave it up to the user for now.

Finally we write our own variation for ListingBlock:

ListingVariation.jsx

```jsx
import React from "react";
import PropTypes from "prop-types";
import cloneDeep from "lodash/cloneDeep";
import { useIntl } from "react-intl";
import { ConditionalLink, UniversalLink } from "@plone/volto/components";
import { flattenToAppURL } from "@plone/volto/helpers";
import config from "@plone/volto/registry";

import { isInternalURL } from "@plone/volto/helpers/Url/Url";

const ListingVariation = (props) => {
  const {
    items,
    linkTitle,
    linkHref,
    isEditMode,
    data,
    extension = "cardTemplates",
  } = props;
  let link = null;
  let href = linkHref?.[0]?.["@id"] || "";

  if (isInternalURL(href)) {
    link = (
      <ConditionalLink to={flattenToAppURL(href)} condition={!isEditMode}>
        {linkTitle || href}
      </ConditionalLink>
    );
  } else if (href) {
    link = <UniversalLink href={href}>{linkTitle || href}</UniversalLink>;
  }

  const intl = useIntl();

  const teaserExtenstions =
    config.blocks.blocksConfig?.teaser?.extensions[extension].items;
  let activeItem = teaserExtenstions.find(
    (item) => item.id === props?.[extension]
  );
  const extenionSchemaEnhancer = activeItem?.schemaEnhancer;
  if (extenionSchemaEnhancer)
    extenionSchemaEnhancer({
      schema: cloneDeep(config.blocks.blocksConfig?.teaser?.blockSchema),
      data: data || props,
      intl,
    });
  const ExtensionToRender = activeItem?.template;

  return (
    <>
      <div className="items">
        {items.map((item) => (
          <div className="listing-item" key={item["@id"]}>
            <ExtensionToRender
              data={{
                ...item,
                href: [item?.["@id"]],
                preview_image: item.image_scales.preview_image,
              }}
              {...props}
            />
          </div>
        ))}
      </div>

      {link && <div className="footer">{link}</div>}
    </>
  );
};

ListingVariation.propTypes = {
  items: PropTypes.arrayOf(PropTypes.any).isRequired,
  linkMore: PropTypes.any,
  isEditMode: PropTypes.bool,
};
export default ListingVariation;
```

We will now have the per listing item styling support like we have for teaser blocks. We can also add more styling schema with the help of its individual schema extenders.
