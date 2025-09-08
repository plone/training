---
myst:
  html_meta:
    "description": "Learn how to write an editable Volto Block"
    "property=og:description": "Learn how to write an editable Volto Block"
    "property=og:title": "Editable Blocks"
    "keywords": "Plone, Volto, Training, Blocks"
---

(voltohandson-editblocks-label)=

# Blocks - Edit components

The edit component part of a block anatomy is specially different to the view component because they have to support the UX for editing the block.
This UX can be very complex depending on the kind of block and the feature that it is trying to provide.
The project requirements will tell how far you should go with the UX story of each block, and how complex it will become.
You can use all the props that the edit component is receiving to model the UX for the block and how it will render.

See the complete list {ref}`voltohandson-introtoblocks-editprops-label`.

We have several UI/UX artifacts in order to model our block edit component UX.
The sidebar and the object browser are the main ones.

## Sidebar

We can use the new sidebar when building our blocks' edit components.
It's a new resource that is available in Volto 6.
You need to instantiate it this way:

```jsx
import { SidebarPortal } from '@plone/volto/components';

...

<SidebarPortal selected={props.selected}>
  ...
</SidebarPortal>
```

Everything that's inside the `SidebarPortal` component will be rendered in the sidebar.

## Schema

To define the fields that an editor in Volto can use to customize their blocks, we have a schema engine similar to how we define schemas for content types in Plone.
Each Block should have a `schema.js` file that contains the definition for the Blocks fields.

```js
export const schemaTeaser = (props) => {
  return {
    required: [],
    fieldsets: [
      {
        id: "default",
        title: "Default",
        fields: ["some_field"],
      },
    ],
    properties: {
      some_field: {
        title: "Some Field",
      },
    },
  };
};

export default schema;
```

We use the `BlockDataForm` component from Volto to then generate the interface from the schema.
Follow the next steps to see how.

## Teaser block

Let's create a new block (not in the project specification) but can be handy too.
Create a new block called Teaser.
We will add the ability to select an existing object as source for showing in this block.

Follow the previous chapters to create a new basic block.

### Teaser block edit component

We will start this time with the `Edit.jsx` component.
We will also create two children components:

`src/components/Blocks/Teaser/Edit.jsx`

```jsx
import React from "react";
import { SidebarPortal } from "@plone/volto/components";
import { withBlockExtensions } from "@plone/volto/helpers";
import TeaserData from "./TeaserData";
import TeaserBody from "./TeaserBody";

const Edit = (props) => {
  const { data, onChangeBlock, block, selected } = props;

  return (
    <>
      <TeaserBody data={data} id={block} isEditMode />
      <SidebarPortal selected={selected}>
        <TeaserData
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

`TeaserBody` will hold the actual visible content of the block:

`src/components/Blocks/Teaser/TeaserBody.jsx`

```jsx
import React from "react";
import { Link } from "react-router-dom";
import { Message } from "semantic-ui-react";
import { defineMessages, injectIntl } from "react-intl";
import imageBlockSVG from "@plone/volto/components/manage/Blocks/Image/block-image.svg";
import { flattenToAppURL } from "@plone/volto/helpers";

const messages = defineMessages({
  PleaseChooseContent: {
    id: "Please choose an existing content as source for this element",
    defaultMessage:
      "Please choose an existing content as source for this element",
  },
});

const TeaserBody = ({ data, id, isEditMode, intl }) => {
  const teaserData = data.teaser[0];

  return (
    <>
      {!teaserData ? (
        <Message>
          <div className="teaser-item default">
            <img src={imageBlockSVG} alt="" />
            <p>{intl.formatMessage(messages.PleaseChooseContent)}</p>
          </div>
        </Message>
      ) : (
        <div className="teaser-item">
          {(() => {
            const item = (
              <>
                {teaserData.hasPreviewImage && (
                  <img
                    src={`${flattenToAppURL(teaserData["@id"])}/@@images/${
                      teaserData.image_field
                    }/teaser`}
                    alt=""
                  />
                )}
                <h3>{teaserData.title}</h3>
                <p>{teaserData.description}</p>
              </>
            );
            if (!isEditMode) {
              return (
                <Link
                  to={flattenToAppURL(teaserData["@id"])}
                  target={data.openLinkInNewTab ? "_blank" : null}
                >
                  {item}
                </Link>
              );
            } else {
              return item;
            }
          })()}
        </div>
      )}
    </>
  );
};

export default injectIntl(TeaserBody);
```

`TeaserData` holds the code that will be contained in the sidebar:

`src/components/Blocks/Teaser/TeaserData.jsx`

```jsx
import React from "react";
import { BlockDataForm } from "@plone/volto/components";
import TeaserSchema from "./schema";

const TeaserData = (props) => {
  const { data, block, onChangeBlock } = props;
  const schema = TeaserSchema({ ...props });
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

export default TeaserData;
```

The schema defines the actual fields rendered in the sidebar and saved in the Block:

`src/components/Blocks/Teaser/schema.js`

```js
export const schemaTeaser = (props) => {
  return {
    required: [],
    fieldsets: [
      {
        id: "default",
        title: "Default",
        fields: ["teaser"],
      },
    ],
    properties: {
      teaser: {
        title: "Teaser",
        widget: "object_browser",
        mode: "link",
        allowExternals: true,
      },
    },
  };
};

export default schemaTeaser;
```

`src/components/Blocks/Teaser/View.jsx`

```jsx
import React from "react";
import TeaserBody from "./TeaserBody";
import { withBlockExtensions } from "@plone/volto/helpers";

const View = (props) => {
  return <TeaserBody {...props} />;
};

export default withBlockExtensions(View);
```

`src/config.js`

```js
import { TeaserViewBlock, TeaserEditBlock } from "@package/components";
//...
config.blocks.blocksConfig.teaser = {
  id: "teaser",
  title: "Teaser",
  icon: sliderSVG,
  group: "common",
  view: TeaserViewBlock,
  edit: TeaserEditBlock,
  restricted: false,
  mostUsed: true,
  security: {
    addPermission: [],
    view: [],
  },
};
```

and finally the styling:

```less
.teaser-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;

  img {
    width: 100%;
    margin-bottom: 20px;
  }

  a {
    color: @textColor;
  }

  h3 {
    margin: 0 0 20px 0;
  }
}
```
