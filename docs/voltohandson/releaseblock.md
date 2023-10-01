---
myst:
  html_meta:
    'description': 'Learn how to create a volto Block with sidebar'
    'property=og:description': 'Learn how to create a volto Block with sidebar'
    'property=og:title': 'Release Block'
    'keywords': 'Plone, Volto, Training, Blocks, Release'
---

# Configurable Release Block

The next Block we will . We will use this to learn how to create a Block that is configurable by an editor.

## Initital Block setups

The initial setup for this Block is the same as for the `slider` Block. Create a new folder in `src/components/Blocks` called `release` and in there `View.jsx` as well as `Edit.jsx`. For now give them the same initial content as we did with the slider:

```jsx
import React from 'react';

const View = (props) => {
  return <div>I'm the Release view component!</div>;
};

export default View;
```

And for `Edit.jsx` correspondingly. Export the blocks via the `index.js` and register the block in `config.js` like you did with the slider. Now you can add it to your page. You can use the same SVG as for the release but you can also pick something of you choice from [pastanaga ui](https://pastanaga.io/icons/). All the icons there are available in Volto by default.

## Create the schema for your Block

First you have to identify what fields the Block needs an editor to be able to edit and of what type. In our case those will be the following:

- title: The field that contains "Get the latest Plone" in the original
- description/subtitle: The text underneath the title
- buttontext: text displayed on the red button
- buttonlink: where the button should link to
- image: Logo of current Plone release

To define these fields we will create a schema inside the new file `schema.js` within the `release` folder. Then paste the following into `schema.js`:

```js
export const schemaRelease = (props) => {
  return {
    required: [],
    fieldsets: [
      {
        id: 'default',
        title: 'Default',
        fields: ['title', 'description', 'image', 'imageAlt'],
      },
      {
        id: 'button',
        title: 'Button',
        fields: ['buttonTitle', 'buttonLink'],
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
      image: {
        title: 'Image',
        widget: 'object_browser',
        mode: 'image',
      },
      imageAlt: {
        title: 'Image alt text',
        widget: 'text',
      },
    },
  };
};

export default schemaRelease;
```

The `properties` key will contain all the fields, while the `fieldsets` key assignes the fields to different fieldsets. In the `required` array you can define certain fields as required. If you have already experience in working with classic Plone, you will notice, that this is very similar to how you would create content types there.

## Implement schema in sidebar

To implement the schema in the sidebar of your block you will have to create another component called `Data.jsx` in which the schema will be transformed to proper react inputs. Paste the following into the `Data.jsx` file:

```jsx
import { BlockDataForm } from '@plone/volto/components';
import Schema from './schema';

const ReleaseData = (props) => {
  const { data, block, onChangeBlock, blocksConfig } = props;
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
      onChangeBlock={onChangeBlock}
      formData={data}
      block={block}
      blocksConfig={blocksConfig}
    />
  );
};

export default ReleaseData;
```

The `BlockDataForm` component will transform the `schema.js` data into a usable sidebar. You now can add that sidebar to your Blocks
Last but not least you need to amend `Edit.jsx` to use that sidebar:

```jsx
import { SidebarPortal } from '@plone/volto/components';
import { withBlockExtensions } from '@plone/volto/helpers';
import ReleaseData from './Data';
import View from './View';

const Edit = (props) => {
  const { data, onChangeBlock, block, selected } = props;
  return (
    <>
      <View {...props} />
      <SidebarPortal selected={selected}>
        <ReleaseData
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

export default withBlockExtensions(Edit);
```

## Create the View

You are now able to edit the content of your Block, but will still see your default "This is the View" text. To change that amend `View.jsx` as follows:

```jsx
import { Container } from 'semantic-ui-react';
import { UniversalLink } from '@plone/volto/components';

const ReleaseView = (props) => {
  const { data } = props;
  return (
    <div className="block release full-width">
      <Container>
        <h2>{data.title}</h2>
        <div className="text-button-wrapper">
          <p>{data.description}</p>
          {data.buttonLink && (
            <UniversalLink
              className="button-link"
              href={data.buttonLink[0]['@id']}
              openInNewTab
            >
              {data.buttonTitle}
            </UniversalLink>
          )}
        </div>
        {data.image.length > 0 && (
          <img
            src={`${data.image[0]['@id']}/@@images/image`}
            alt={data.imageAlt}
          />
        )}
      </Container>
    </div>
  );
};

export default ReleaseView;
```

Note that all the fields defined in the schema and filled via the sidebar can now be accessed from the `data` key of the blocks props. You can use `console.log(data)` to see the details.

To make the block look like its twin on plone.org we only need to add the following CSS to our `custom.overrides`:

```less
// Release block
.block.release {
  background: #f0f8fc;
  padding: 20px 0;
  h2 {
    font-weight: bold;
  }
  .text-button-wrapper {
    display: flex;
    justify-content: space-between;

    p {
      width: 600px;
      font-size: 1.25rem;
      color: #595959;
      font-weight: 300;
    }

    a {
      border-radius: 0;
      color: @white;
      background: @blue;
      border: 2px solid @blue;
      font-weight: normal;
      padding: 14px 20px 16px 22px;
      display: inline-block;
      line-height: 1em;
      height: 56px;
      margin-right: 150px;
      &::after {
        background-image: url(https://plone.org/static/media/arrow-right-white.141ecd63.svg);
        display: inline-block;
        width: 22px;
        height: 22px;
        margin-left: 1.5em;
        background-repeat: no-repeat;
        background-size: cover;
        content: '';
        vertical-align: text-top;
      }

      &:hover {
        background: @white;
        color: @blue;

        &::after {
          background-image: url(https://plone.org/static/media/arrow-right.c1b96a21.svg);
        }
      }
    }
  }
}
```
## Release

When done, you can enter edit mode on your frontpage and add the respective text as on the original `plone.org`.

For the image create a new Image-type Plone content object and upload the Plone 6 image from the training ressources. Then Choose that Image in the edit toolbar of your Block.
