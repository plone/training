---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(search-block-variation-label)=

# Search block variation


```{card}

In this part you will:

- Create a search block variation to display also the talks event date, room, audience and speaker name

Topics covered:

- block variation
```

````{card} Frontend chapter

Checkout `volto-ploneconf` at tag "upgrade_steps":

```shell
git checkout upgrade_steps
```

The code at the end of the chapter:

```shell
git checkout listing_variation
```

More info in {doc}`code`
````

```{figure} _static/listing_variation.png
:alt: block variation for the search block to show more than title and description

block variation for the search block to show more than title and description
```

```{figure} _static/listing_variation_edit.png
:alt: Apply listing variation

Apply listing variation
```


(search-block-variation-registration-label)=

## Create and register new block variation

Each block can be enhanced with variations of its layout.
We are writing a block variation for the search block.

First step is to create a new component `packages/volto-ploneconf/src/components/variations/TalkListingBlockVariation.jsx` with the code of an existing block variation `core/packages/volto/src/components/manage/Blocks/Listing/SummaryTemplate.jsx`.

We register our new variation on `config.blocks.blocksConfig.listing.variations`, as listing blocks and search blocks share their variations via this setting.

registration `packages/volto-ploneconf/src/index.js`:

```{code-block} jsx
:linenos:
:emphasize-lines: 12-20

import { TalkView, TalkListingBlockVariation } from './components';

const applyConfig = (config) => {
  config.views = {
    ...config.views,
    contentTypesViews: {
      ...config.views.contentTypesViews,
      talk: TalkView,
    },
  };

  config.blocks.blocksConfig.listing.variations = [
    ...config.blocks.blocksConfig.listing.variations,
    {
      id: 'talks',
      title: 'Talks',
      template: TalkListingBlockVariation,
    },
  ];

  return config;
};

export default applyConfig;
```


variation component `packages/volto-ploneconf/src/components/variations/TalkListingBlockVariation.jsx`:

```{code-block} jsx
:linenos:
:emphasize-lines: 37

import React from 'react';
import PropTypes from 'prop-types';
import { Label, Segment } from 'semantic-ui-react';
import { ConditionalLink, Component } from '@plone/volto/components';
import { When } from '@plone/volto/components/theme/View/EventDatesInfo';
import { flattenToAppURL } from '@plone/volto/helpers';

import { isInternalURL } from '@plone/volto/helpers/Url/Url';

const TalkListingBlockVariation = ({
  items,
  linkTitle,
  linkHref,
  isEditMode,
}) => {
  let link = null;
  let href = linkHref?.[0]?.['@id'] || '';
  const color_mapping_audience = {
    beginner: 'green',
    advanced: 'yellow',
    professional: 'purple',
  };

  if (isInternalURL(href)) {
    link = (
      <ConditionalLink to={flattenToAppURL(href)} condition={!isEditMode}>
        {linkTitle || href}
      </ConditionalLink>
    );
  } else if (href) {
    link = <a href={href}>{linkTitle || href}</a>;
  }

  return (
    <>
      <div className="items">
        {items.map((item) => (
          <Segment>
            <div className="listing-item" key={item['@id']}>
              <ConditionalLink item={item} condition={!isEditMode}>
                <Component componentName="PreviewImage" item={item} alt="" />
                <div className="listing-body">
                  <When
                    start={item.start}
                    end={item.end}
                    whole_day={item.whole_day}
                    open_end={item.open_end}
                  />
                  <h3>{item.title || item.id}</h3>
                  <p>{item.speaker}</p>
                  <p>
                    {item.room && (
                      <>
                        <b>Room: </b>
                        {item.room}
                        <br />
                      </>
                    )}
                    {item.audience?.length > 0 && (
                      <>
                        <b>Audience:</b>
                        {item.audience?.map((audience) => {
                          let color =
                            color_mapping_audience[audience] || 'green';
                          return (
                            <Label key={audience} color={color}>
                              {audience}
                            </Label>
                          );
                        })}
                      </>
                    )}
                  </p>
                  <p>{item.description}</p>
                </div>
              </ConditionalLink>
            </div>
          </Segment>
        ))}
      </div>

      {link && <div className="footer">{link}</div>}
    </>
  );
};

TalkListingBlockVariation.propTypes = {
  items: PropTypes.arrayOf(PropTypes.any).isRequired,
  linkMore: PropTypes.any,
  isEditMode: PropTypes.bool,
};

export default TalkListingBlockVariation;
```

This is a very basic block variation.
Block variations can have variations: See {doc}`plone6docs:volto/blocks/extensions` for advanced techniques.
