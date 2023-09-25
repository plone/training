---
myst:
  html_meta:
    "description": "How to use StyleWrapper(Styling Schemas) and StyleMenu"
    "property=og:description": "How to use StyleWrapper(Styling Schemas) and StyleMenu"
    "property=og:title": "Usage of StyleWrapper(Styling Schemas) and StyleMenu"
    "keywords": "Volto, StyleWrapper, StyleMenu"
---

# Usage of StyleWrapper(Styling Schemas) and StyleMenu

Its essential to also control the styling of Blocks and most importantly if the styling is done based on schema or not. 

## StyleWrapper(Styling Schemas)

In Volto we have a central wrapper named [`StyleWrapper`](https://github.com/plone/volto/blob/9667cf735e5c3e848de852d615941d98193e0a5e/src/components/manage/Blocks/Block/StyleWrapper.jsx#L1) which wraps around all the View template of Blocks. The job of stylewrapper is to build and inject style classNames into its children.

In the schema at any point in time, we can call a volto helper which adds `styles` fields. Which then gets converted into classNames with the prefix `--has`. Its upto the theme owner in which way they want to add css for it.
Simply, the job of StyleWrapper is to inject classNames(build from schema) into their children.

We see that in our Teaser config volto already calls the [addStyling](https://github.com/plone/volto/blob/9667cf735e5c3e848de852d615941d98193e0a5e/src/helpers/Extensions/withBlockSchemaEnhancer.js#L297) in the schema. The job of this function is to add styles field in the styling fieldset in schema provided.

```jsx
export const TeaserSchema = ({ intl }) => {
  const schema = {
    title: intl.formatMessage(messages.teaser),
    fieldsets: [
      {
        id: "default",
        title: "Default",
        fields: ["href", "title", "head_title", "description", "preview_image"],
      },
    ],

    properties: {
      href: {
        title: intl.formatMessage(messages.Target),
        widget: "object_browser",
        mode: "link",
        selectedItemAttrs: [
          "Title",
          "head_title",
          "Description",
          "hasPreviewImage",
          "image_field",
          "image_scales",
          "@type",
        ],
        allowExternals: true,
      },
      title: {
        title: intl.formatMessage(messages.title),
      },
      head_title: {
        title: intl.formatMessage(messages.head_title),
      },
      description: {
        title: intl.formatMessage(messages.description),
        widget: "textarea",
      },
      preview_image: {
        title: intl.formatMessage(messages.imageOverride),
        widget: "object_browser",
        mode: "image",
        allowExternals: true,
        selectedItemAttrs: ["image_field", "image_scales"],
      },
      openLinkInNewTab: {
        title: intl.formatMessage(messages.openLinkInNewTab),
        type: "boolean",
      },
    },
    required: [],
  };

  addStyling({ schema, intl });

  schema.properties.styles.schema.properties.align = {
    widget: "align",
    title: intl.formatMessage(messages.align),
    actions: ["left", "right", "center"],
    default: "left",
  };

  schema.properties.styles.schema.fieldsets[0].fields = ["align"];

  return schema;
};
```

and then we can manipulate those fields by adding whatever styles we want. Let's extend it and add one more style named as image object-fit css property.

In your variation schemaEnhancer:

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

      schema.properties.styles.schema.properties.objectFit = {
        title: "Object fit",
        description: "Css object fit property",
        choices: [
          ["cover", "cover"],
          ["contain", "contain"],
          ["fill", "fill"],
          ["scale-down", "scale-down"],
          ["none", "none"],
        ],
      };

      schema.properties.styles.schema.fieldsets[0].fields.push("objectFit");
      return schema;
    },
  },
];
```

As StyleWrapper wraps around our view component in `RenderBlocks`. The styleNames should be available in our component's rendered html.

```
<div class="block teaser has--align--left has--objectFit--contain">
    <a href="/teaser-view">
        <div class="teaser-item overlay">
            <div class="image-wrapper">
                <img src="/teaser-view/@@images/preview_image-600-dd112f14087d6a99687a9f94dd31a9a4.jpeg" alt="" loading="lazy">
            </div>
            <div class="gradiant">
                <div style="display: flex; flex-direction: column;">
                <h2>teaser View</h2>
                <p></p>
            </div>
        </div>
    </div>
    </a>
</div>
```

Go ahead and add classNames in your `css/less` files

```css
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

## StyleMenu

StyleMenu is not the part of Blocks engine instead its a volto-slate plugin and its used to style rich text content only.

In your policy package, you can add styleMenu configuration like:

```js
config.settings.slate.styleMenu = {
  ...(config.settings.slate.styleMenu || {}),
  blockStyles: [
    {
      cssClass: "primary",
      label: "Primary",
      icon: () => <Icon name={paintSVG} size="18px" />,
    },
    {
      cssClass: "secondary",
      label: "Secondary",
      icon: () => <Icon name={paintSVG} size="18px" />,
    },
    {
      cssClass: "tertiary",
      label: "Tertiary",
      icon: () => <Icon name={paintSVG} size="18px" />,
    },
  ],
};
```

Make sure to add relevant classNames in your css.
