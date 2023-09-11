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
The wrapper expects an object field `styles` in the block's schema, so there's a helper available to enable it via a block `schemaEnhancer` that does this for you called `addStyling`.

```{note}
The style wrapper only will work if your block uses the `BlocksForm` component to define schema-driven block configuration settings.
```

```js
import { addStyling } from '@plone/volto/helpers/Extensions/withBlockSchemaEnhancer';

export const defaultStylingSchema = ({ schema, formData, intl }) => {

  addStyling({ schema, intl });

  return schema;
};
```

```{note}
The signature for a `schemaEnhancer` is `({schema, formData, intl})`. You can find the reference of the default schema in `@plone/volto/components/manage/Blocks/Block/StylesSchema`.
```

Then in the block's config:

```js
  config.blocks.blocksConfig.myBlock = {
    ...config.blocks.blocksConfig.myBlock,
    schemaEnhancer: defaultStylingSchema,
  };
```

This will add a new fieldset `Styling` at the end of your block schema settings with a single `styles` object field in it.

## Extending the default `styles` field in `Styling` fieldset

You can modify the default set of styles by using the `schemaEnhancer` function previously mentioned like this:

```js
import { addStyling } from '@plone/volto/helpers/Extensions/withBlockSchemaEnhancer';

export const defaultStylingSchema = ({ schema, formData, intl }) => {
  const BG_COLORS = [
    { name: 'transparent', label: 'Transparent' },
    { name: 'grey', label: 'Grey' },
  ];

  const colors =
    config.blocks?.blocksConfig?.[formData['@type']]?.colors || BG_COLORS;

  const defaultBGColor =
    config.blocks?.blocksConfig?.[formData['@type']]?.defaultBGColor;

  addStyling({ schema, intl });

  schema.properties.styles.schema.fieldsets[0].fields = [
    ...schema.properties.styles.schema.fieldsets[0].fields,
    'backgroundColor',
  ];
  schema.properties.styles.schema.properties.backgroundColor = {
    widget: 'color_picker',
    title: intl.formatMessage(messages.backgroundColor),
    colors,
    default: defaultBGColor,
  };

  return schema;
};
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

## Using `className` in your block view component

The resultant class names are injected as a `className` prop into the wrapped block.
Thus you can use it in the root component of your block view and edit components as follows:

```jsx
const BlockView = (props)=> (
  <div className={props.className}>
    // Block's code
  </div>
)
```

The resultant HTML would be the following:

```html
<div class="has--backgroundColor--ee22ee has--myCustomStyleField--red has--myCustom2StyleField--color--black has--myCustom2StyleField--color--MyGradient">
```

Then it's at your discretion how you define the CSS class names in your theme.

The block editor wrapper does the same for the block edit component, but it's automatically injected into the wrapper containers.

```html
<div data-rbd-draggable-context-id="0" data-rbd-draggable-id="9949a5fa-5d57-4e0c-a150-71149a31096c" class="block-editor-listing has--backgroundColor--ee22ee has--myCustomStyleField--red has--myCustom2StyleField--color--black has--myCustom2StyleField--color--MyGradient">
  ...
</div>
```

## `styleClassNameConverters`

If you need other style of classnames generated, you can use the classname
converters defined in `config.settings.styleClassNameConverters`, by
registering fieldnames suffixed with the converter name. For example, a style
data like:

```
{
  "styles": {
    "theme:noprefix": "primary",
    "inverted:bool": true,
  }
}
```

will generate classnames `primary inverted`. This relies on the `noprefix` and `bool` converters that are registered in Volto.

## `styleClassNameExtenders`

An array containing functions that extends how the StyleWrapper builds a list of styles. These functions have the signature `({ block, content, data, classNames }) => classNames`. Here are some examples of useful ones, for simplicity, they are compacted in one extender:

```js
  import { getPreviousNextBlock } from '@plone/volto/helpers';

  config.settings.styleClassNameExtenders = [
    ({ block, content, data, classNames }) => {
      let styles = [];
      const [previousBlock, nextBlock] = getPreviousNextBlock({
        content,
        block,
      });

      // Inject a class depending of which type is the next block
      if (nextBlock?.['@type']) {
        styles.push(`next--is--${nextBlock['@type']}`);
      }

      // Inject a class depending if previous is the same type of block
      if (data?.['@type'] === previousBlock?.['@type']) {
        styles.push('previous--is--same--block-type');
      }

      // Inject a class depending if next is the same type of block
      if (data?.['@type'] === nextBlock?.['@type']) {
        styles.push('next--is--same--block-type');
      }

      // Inject a class depending if it's the first of block type
      if (data?.['@type'] !== previousBlock?.['@type']) {
        styles.push('is--first--of--block-type');
      }

      // Inject a class depending if it's the last of block type
      if (data?.['@type'] !== nextBlock?.['@type']) {
        styles.push('is--last--of--block-type');
      }

      // Given a StyleWrapper defined `backgroundColor` style
      const previousColor =
        previousBlock?.styles?.backgroundColor ?? 'transparent';
      const currentColor = data?.styles?.backgroundColor ?? 'transparent';
      const nextColor = nextBlock?.styles?.backgroundColor ?? 'transparent';

      // Inject a class depending if the previous block has the same `backgroundColor`
      if (currentColor === previousColor) {
        styles.push('previous--has--same--backgroundColor');
      } else if (currentColor !== previousColor) {
        styles.push('previous--has--different--backgroundColor');
      }

      // Inject a class depending if the next block has the same `backgroundColor`
      if (currentColor === nextColor) {
        styles.push('next--has--same--backgroundColor');
      } else if (currentColor !== nextColor) {
        styles.push('next--has--different--backgroundColor');
      }

      return [...classNames, ...styles];
    },
  ];
```

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
const maxLinesSchemaEnhancer = (schema) => {
  schema.properties.styles.schema.fieldsets.push({
        title: 'Styling',
        id: 'default',
        fields: ['maxLines'],
      });
  schema.properties.styles.schema.properties.maxLines = {
        title: 'Max lines',
        description:
          "Limit description to a maximum number of lines by adding trailing '...'",
        type: 'number',
        default: 2,
        minimum: 0,
        maximum: 5,
      };
  return schema;
}
```

We'll assign it to the listing block:

```
import { composeSchema } from '@plone/volto/helpers';

// ... somewhere in the configuration function
  config.blocks.blocksConfig.listing.schemaEnhancer = composeSchema(
    config.blocks.blocksConfig.listing.schemaEnhancer,
    maxLinesSchemaEnhancer
  );
// ...
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
