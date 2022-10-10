---
myst:
  html_meta:
    "description": "Block Styling"
    "property=og:description": "Block Styling"
    "property=og:title": "Block Styling"
    "keywords": "Volto, Plone, Volto blocks styling, CSS"
---

# Block Styling

The block style wrapper is part of a block anatomy.
It allows you to inject styles from the block schema into the block wrapper in the form of class names.
It wraps the block edit and the view components.

It can be used by directly mapping unique values to CSS properties.
For example, `background-color` could be mapped to a single color.
Although that is a simple use case, the real intent of style wrappers is to allow the definition of complex CSS through a full set of styles mapped to a CSS class.
For example, often applying a background color is not enough, and you need to also modify the font color to make it readable because of contrast issues.
The style object field can be extended to hold any number of fields, depending on your needs.
The resultant set of class names to be injected are built by concatenating the key-value pairs of the `styles` object field, separated by `--` and prefixing the result with the `has--` prefix.
The class name generator algorithm supports up to one level of nested objects, constructing the concatenated CSS class from the nested structure as well.
See below for an example.

## Enabling Style Wrapper in a block

The wrapper is always present in the rendering of both the view and edit components.
If you want to add the default set of styles, you need to enable them with the following flag:

```js
  // (in your block config object)
  my_custom_block: {
    // (more block settings)
    enableStyling: true,
  }
```

```{note}
This will work if your block uses the `BlocksForm` component to define schema-driven block configuration settings.
```

This will add a new fieldset `Styling` at the end of your block schema settings with a single `styles` object field in it.
By default, this object field has only one field: `align`. It is configured by `defaultSchema` in `src/components/manage/Blocks/Block/StylesSchema.jsx`.

## Extending the default `styles` field in `Styling` fieldset

You can modify the default set of styles by using a `schemaEnhancer` function in the same way that you would for any block schema enhancer.
Use the `stylesSchema` key in your block configuration object as follows:

```js
  // (in your block config object)
  my_custom_block: {
    // (more block settings)
    enableStyling: true,
    stylesSchema: myCustomStyleSchema
  }
```

```{note}
The signature for a `schemaEnhancer` is `({schema, formData, intl})`. You can find the reference of the default schema in `@plone/volto/components/manage/Blocks/Block/StylesSchema`.
```

## The `styles` field

The `styles` field is mapped to an `objectWidget`.
The `stylesSchema` adds the fields into this field, creating an object that is the sum of all of the fields assigned to it and its values.

```json
{
  "styles": {
    "backgroundColor": "#ee22ee",
    "myCustomStyleField": "red",
    "myCustom2StyleField": {
      "color": "black",
      "gradient": "MyGradient"
    }
  }
}
```

## Using `className` in your block

The resultant class names are injected as a `className` prop into the wrapped block.
Thus you can use it in the root component of your block view and edit components as follows:

```jsx
const BlockView = (props)=> (
  <div className={props.className}>
    // Block's code
  </div>
)
```

Same for the block edit component.
The resultant HTML would be the following:

```html
<div class="has--backgroundColor--ee22ee has--myCustomStyleField--red has--myCustom2StyleField--color--black has--myCustom2StyleField--color--MyGradient">
```

Then it's at your discretion how you define the CSS class names in your theme.

### Using CSS variables

Once you start using the style wrapper you'll realise that simply using the
classes to form selectors can't cover all the possible combinations (specially
if you reuse the same StyleWrapper schema across many blocks, to provide
a unified look and feel for the website). One possible solution to this problem
is to use
[CSS Variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties),
and reference those variables from your stylesheets.

For example, let's say we want to limit the description in the listing block to
a fixed number of lines.

We'll have the following styles schema:

```js
const StyleSchema = () => (
  {
    fieldsets: [
      {
        title: 'Styling',
        id: 'default',
        fields: ['maxLines'],
      }
    ],
    properties: {
      maxLines: {
        title: 'Max lines',
        description:
          "Limit description to a maximum number of lines by adding trailing '...'",
        type: 'number',
        default: 2,
        minimum: 0,
        maximum: 5,
      },
    },
    required: [],
  });
```

We'll assign it to the listing block:

```
config.blocks.blocksConfig.listing.enableStyling = true;
config.blocks.blocksConfig.listing.stylesSchema = StyleSchema;
```

For the CSS part, we add the following code:

```less
each(range(5), {
  .has--maxLines-@{value} {
    --max-lines: @value;
  }
});
```

This generates 5 CSS classes, such as `has--maxLines--3`, which only define
a variable, the `--max-lines`. Having the variable applied at the "root" of our
listing block, together with a mixin, we can now target directly those elements
that should be affected (and, because it's a mixin, we have greater flexibility
and centralized control):

```less
.useMaxLines() {
  display: -webkit-box;
  overflow: hidden;

  -webkit-box-orient: vertical;
  -webkit-line-clamp: var(--max-lines, 5);
}

.listing-item {
  p {
    .useMaxLines();
  }
}
```

## Main edit wrapper class injection

Under the hood, there is yet another class injection happening in the main Block Engine Wrapper.
This is in place to help properly position the block in the current layout.

Each block in the Block Engine has a main wrapper with an automatic class name `block-editor-<block_id> <block_align>`, as shown in the following example:

```html
<div data-rbd-draggable-context-id="0" data-rbd-draggable-id="9949a5fa-5d57-4e0c-a150-71149a31096c" class="block-editor-listing center">
  ...
</div>
```

You can use it for further control over the positioning and layout of the block.
