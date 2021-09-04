(volto-custom-block-label)=

# Custom Block

````{sidebar} Volto chapter
```{figure} _static/volto.svg
:alt: Volto Logo
```

Create a specialized block with some extra behavior or look.
````

In case you need some special look of a paragraph, a special behavior like an image gallery or even need to display data as chart, then you want to create your own block.

A very simple use case where the default text block can be extended to achieve the requested look and behavior is the following:

Use Case: *The content of a page should be teasered: Show first part and the rest on click on "read more".*

```{figure} _static/volto_block_readmore.png
:alt: Volto text block with teasering behavior
```

```{figure} _static/volto_block_readmore_edit.png
:alt: Edit view with an additonal option
```

We extend the default Volto text block schema with an additional field "readmore".

{file}`src/customizations/components/manage/Blocks/Text/Schema.jsx`

```{code-block} jsx
:emphasize-lines: 8
:linenos: true

import BlockSettingsSchema from '@plone/volto/components/manage/Blocks/Block/Schema';

const Schema = {
    ...BlockSettingsSchema,
    fieldsets: [
        {
            ...BlockSettingsSchema.fieldsets[0],
            fields: ['readmore'],
        },
    ],
    properties: {
        readmore: {
        title: 'Read more',
        description: 'Hide following text. Show on Click.',
        type: 'boolean',
        },
    },
};

export default Schema;
```

We use the Volto `InlineForm` component to extend the sidebar.

{file}`src/customizations/components/manage/Blocks/Text/Edit.jsx`

```{code-block} jsx
:emphasize-lines: 15,16,19
:linenos: true

import { SidebarPortal } from '@plone/volto/components';
import InlineForm from '@plone/volto/components/manage/Form/InlineForm';

import schema from './Schema';

snip

render() {

snip

    return (
        <>
            <SidebarPortal selected={this.props.selected}>
                <InlineForm
                    schema={schema}
                    title={schema.title}
                    onChangeField={(id, value) => {
                        this.props.onChangeBlock(this.props.block, {
                            ...this.props.data,
                            [id]: value,
                        });
                    }}
                    formData={this.props.data}
                />
            </SidebarPortal>
```

You see the call of `onChangeBlock` which writes the value true or false to the block data.

With the above customizations the default text block has an additional attribute "readmore".

The default text block has no options to select, so it is per default configured to show the document properties pane in sidebar and not the block pane. The following modification forces the sidebar to show the block configuration pane instead.

{file}`src/config.js`

```{code-block} jsx
:emphasize-lines: 2,4,10
:linenos: true

const customizedBlocks = {
    text: {
        ...config.blocks.blocksConfig.text,
        sidebarTab: 1,
    },
};

export const blocks = {
    ...config.blocks,
    blocksConfig: {
        ...config.blocks.blocksConfig,
        ...customBlocks,
        ...customizedBlocks,
    },
};
```

The blocksConfig is modified by a setting for the text block: Show pane 1 (we have two panes: pane 0 with the document fields and pane 1 with the block fields which depend on the block type).

Now a view of the page can distinguish between content blocks to show and these to hide for further reading on click.

## Exercise

Add a field **highlighted** to a default text block. With this marker you can add a CSS rule to highlight the blocks marked. Where would you place this CSS rule?

## Prospect

That was easy. But what if we need a FAQ section and want to provide a nice form for question and answer pairs? See the next chapter where we create a new block type. We take the opportunity to create an add-on with this block type. So the feature can be easily applied to multiple projects.
