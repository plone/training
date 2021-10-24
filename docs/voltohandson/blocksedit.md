---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
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

## Teaser block

Let's create a new block (not in the project specification) but can be handy too.
Create a new block called Teaser.
We will add the ability to select an existing object as source for showing in this block.

Follow the previous chapters to create a new basic block.

### Teaser block edit component

We will start this time with the `Edit.jsx` component. We'll be creating two children components:

`src/components/Blocks/Teaser/Edit.jsx`

```jsx
import React from "react";
import { SidebarPortal, withBlockExtensions } from "@plone/volto/components";
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

`src/components/Blocks/Teaser/TeaserData.jsx`

```jsx
import React from "react";
import { Segment } from "semantic-ui-react";
import { FormattedMessage } from "react-intl";
import { BlockDataForm } from "@plone/volto/components";
import schema from "./schema";

const TeaserData = (props) => {
  const { data, block, onChangeBlock } = props;
  const schema = schemaListing({ ...props });

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

`src/components/Blocks/Teaser/schema.js`

```js
export const schemaTeaser = (props) => {
  return {
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
```

`src/components/Blocks/Teaser/TeaserBody.jsx`

```jsx
import React from "react";
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Message } from "semantic-ui-react";
import { defineMessages, injectIntl } from "react-intl";
import imageBlockSVG from "@plone/volto/components/manage/Blocks/Image/block-image.svg";
import { getContent } from "@plone/volto/actions";
import { flattenToAppURL } from "@plone/volto/helpers";

const messages = defineMessages({
  PleaseChooseContent: {
    id: "Please choose an existing content as source for this element",
    defaultMessage:
      "Please choose an existing content as source for this element",
  },
});

const TeaserBody = ({ data, id, isEditMode, intl }) => {
  const contentSubrequests = useSelector((state) => state.content.subrequests);
  const dispatch = useDispatch();
  const results = contentSubrequests?.[id]?.data;

  React.useEffect(() => {
    if (data.href) {
      dispatch(getContent(data.href, null, id));
    }
  }, [dispatch, data, id]);

  return (
    <>
      {!data.href && (
        <Message>
          <div className="teaser-item default">
            <img src={imageBlockSVG} alt="" />
            <p>{intl.formatMessage(messages.PleaseChooseContent)}</p>
          </div>
        </Message>
      )}
      {data.href && results && (
        <div className="teaser-item">
          {(() => {
            const item = (
              <>
                {results.image && <img src={results.image.download} alt="" />}
                <h3>{results.title}</h3>
                <p>{results.description}</p>
              </>
            );
            if (!isEditMode) {
              return (
                <Link
                  to={flattenToAppURL(results["@id"])}
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
import TeaserViewBlock from "@package/components/Blocks/Teaser/View";
import TeaserEditBlock from "@package/components/Blocks/Teaser/Edit";
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
