---
myst:
  html_meta:
    'description': 'Learn how to create a volto Block with sidebar'
    'property=og:description': 'Learn how to create a volto Block with sidebar'
    'property=og:title': 'Download Block'
    'keywords': 'Plone, Volto, Training, Blocks, Downloads'
---

# Configurable Downloadlink Block

The next section (skipping the simple text) on `plone.org` is the Banner with Download Button for Plone. We will use this to learn how to create a Block that is configurable by an editor.

## Initital Block setups

The initial setup for this Block is the same as for the `highlight` Block. Create a new folder in `src/components/Blocks` called `download` and in there `View.jsx` as well as `Edit.jsx`. For now give them the same initial content as we did with the highlight:

```jsx
import React from 'react';

const View = (props) => {
  return <div>I'm the Highlight view component!</div>;
};

export default View;
```

And for `Edit.jsx` correspondingly. Export the blocks via the `index.js` and register the block in `config.js` and add it to the page. You can use the same SVG as for the highlight but you can also pick something of you choice from https://pastanaga.io/icons/. All the icons there are available in Volto by default.

## Create the schema for your Block

First you have to identify what fields the Block needs an editor to be able to edit and of what type. In our case those will be the following:

- title: The field that contains "Get the latest Plone" in the original
- description/subtitle: The text underneath the title
- buttontext: text displayed on the red button
- buttonlink: where the button should link to
- other link text: The text underneath the button
- other link: where the other text (Older releases) will link to

To define these fields we will create a schema inside the new file `schema.js` within the `download` folder. Then paste the following into `schema.js`:

```js
export const schemaDownload = (props) => {
  return {
    required: [],
    fieldsets: [
      {
        id: 'default',
        title: 'Default',
        fields: ['title', 'description'],
      },
      {
        id: 'link',
        title: 'Links',
        fields: ['buttonTitle', 'buttonLink', 'otherLinkText', 'otherLink'],
      },
    ],
    properties: {
      title: {
        title: 'Title',
        widget: 'text',
      },
      description: {
        title: 'Description',
        widget: 'text',
      },
      buttonTitle: {
        title: 'Button Title',
        widget: 'text',
      },
      buttonLink: {
        title: 'Button link',
        widget: 'object_browser',
        mode: 'link',
        allowExternals: true,
      },
      otherLinkText: {
        title: 'Other link text',
        widget: 'text',
      },
      otherLink: {
        title: 'Other link',
        widget: 'object_browser',
        mode: 'link',
        allowExternals: true,
      },
    },
  };
};

export default schemaDownload;
```

The `properties` key will contain all the fields, while the `fieldsets` key assignes the fields to different fieldsets. In the `required` array you can define certain fields as required. If you have already experience in working with classic Plone, you will notice, that this is very similar to how you would create content types there.

## Implement schema in sidebar

To implement the schema in the sidebar of your block you will have to create another component called `Data.jsx` in which the schema will be transformed to proper react inputs. Paste the following into the `Data.js` block:

```jsx
import React from 'react';
import { BlockDataForm } from '@plone/volto/components';
import Schema from './schema';

const DownloadData = (props) => {
  const { data, block, onChangeBlock } = props;
  const schema = Schema({ ...props });
  return (
    <BlockDataForm
      schema={schema}
      title={schema.title}
      onChangeField={(id, value) => {
        onChangeBlock(block, {
          ...data,
          [id]: value,
        });
      }}
      formData={data}
      block={block}
    />
  );
};

export default DownloadData;
```

The `BlockDataForm` component will transform the `schema.js` data into a usable sidebar.
Last but not least you need to amend `Edit.jsx` to use that sidebar:

```jsx
import React from 'react';
import { SidebarPortal } from '@plone/volto/components';
import { withBlockExtensions } from '@plone/volto/helpers';
import DownloadData from './Data';
import View from './View';

const downloadLinkEdit = (props) => {
  const { data, onChangeBlock, block, selected } = props;
  return (
    <>
      <View {...props} />
      <SidebarPortal selected={selected}>
        <DownloadData
          key={block}
          {...props}
          data={data}
          block={block}
          onChangeBlock={onChangeBlock}
        />
      </SidebarPortal>
    </>
  );
};

export default withBlockExtensions(downloadLinkEdit);
```

## Create the View

You are now able to edit the content of your Block, but will still see your default "This is the View" text. To change that amend `View.jsx` as follows:

```jsx
import React from 'react';
import { Grid, Container } from 'semantic-ui-react';
import { UniversalLink } from '@plone/volto/components';

const downloadLinkView = (props) => {
  const { data } = props;
  return (
    <div className="block download">
      <Container>
        <Grid columns={2}>
          <Grid.Column>
            <h2>{data.title}</h2>
            <p className="description">{data.description}</p>
          </Grid.Column>
          <Grid.Column>
            {data.buttonLink?.length > 0 && data.buttonTitle && (
              <UniversalLink
                href={data.buttonLink[0]['@id']}
                className="ui button"
              >
                {data.buttonTitle}
              </UniversalLink>
            )}
            <br />
            {data.otherLink?.length > 0 && data.otherLinkText && (
              <UniversalLink
                href={data.otherLink[0]['@id']}
                className="other-link"
              >
                {data.otherLinkText}
              </UniversalLink>
            )}
          </Grid.Column>
        </Grid>
      </Container>
    </div>
  );
};

export default downloadLinkView;
```

Note that all the fields defined in the schema and filled via the sidebar can now be accessed from the `data` key of the blocks props. You can use `console.log(data)` to see the details.

To make the block look somewhat like its example we only need to add the following CSS to our `custom.overrides`:

```less
// Download block

.block.download {
  background: #e8eef2;
  .ui.container {
    padding: 40px 200px;
  }

  h2 {
    font-size: 30px;
    font-weight: bold;
  }
  .description {
    font-size: 21px;
  }

  a.ui.button {
    background: #cc2b00;
    font-size: 18px;
    color: @white;
    border-radius: 6px;
    padding: 14px 20px;
    font-weight: normal;
    margin-bottom: 10px;
  }
  a.other-link {
    color: #175758;
    font-weight: bold;
  }
}
```

When done the block should look very much like on `plone.org`.
