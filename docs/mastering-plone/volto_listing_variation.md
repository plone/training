---
myst:
  html_meta:
    "description": "Customize the layout of the search results"
    "property=og:description": "Customize the layout of the search results"
    "property=og:title": "Search block variation"
    "keywords": "Plone, search, results, meta data"
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

(upgrade-steps-catalog-label)=

## Add catalog indexes

For the next chapter we need to search for sponsors and get the results with the values of field 'url' and 'level.
We add a metadata column for these fields to not wake up objects on search request.
This would be OK, but time consuming.
The search request gets an attribute from catalog brains unless the attribute is not available, then fetches the real object.

Add the new meta data columns 'level' and 'url' to {file}`profiles/default/catalog.xml`

```{code-block} xml

  <column value="level" />
  <column value="url" />
```

While we are at it, we also add some more indexes and criteria for fields of type talk.
With these indexes and criteria we can create listing and search blocks with facets.

```{code-block} xml
:emphasize-lines: 18-36

<?xml version="1.0" encoding="utf-8"?>
<object name="portal_catalog">
  <index meta_type="BooleanIndex"
         name="featured"
  >
    <indexed_attr value="featured" />
  </index>
  <column value="featured" />

  <index meta_type="KeywordIndex"
         name="type_of_talk"
  >
    <indexed_attr value="type_of_talk" />
  </index>
  <column value="type_of_talk" />


  <index meta_type="FieldIndex"
         name="speaker"
  >
    <indexed_attr value="speaker" />
  </index>
  <index meta_type="KeywordIndex"
         name="audience"
  >
    <indexed_attr value="audience" />
  </index>
  <index meta_type="FieldIndex"
         name="room"
  >
    <indexed_attr value="room" />
  </index>

  <column value="speaker" />
  <column value="audience" />
  <column value="room" />


  <column value="level" />
  <column value="url" />
</object>
```

This adds new indexes for the three fields we want to show in the listing.
Note that _audience_ is a {py:class}`KeywordIndex` because the field is multi-valued, but we want a separate index entry for every value in an object.

A reinstallation of the add-on would leave the new catalog indexes empty.
Therefore we write an upgrade step to not only add indexes and criteria, but also reindex all talks:

`src/ploneconf/site/upgrades/v1001.py`:

```python
def update_indexes(setup_tool):
    # Indexes and metadata
    setup_tool.runImportStepFromProfile(default_profile, "catalog")
    # Criteria
    setup_tool.runImportStepFromProfile(default_profile, "plone.app.registry")
    # Reindexing content
    for brain in api.content.find(portal_type=["talk", "sponsor"]):
        obj = brain.getObject()
        obj.reindexObject()
        logger.info(f"{obj.id} reindexed.")
```

`src/ploneconf/site/upgrades/configure.zcml`:

```{code-block} xml
:emphasize-lines: 21-25
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    >

  <genericsetup:upgradeSteps
      profile="ploneconf.site:default"
      source="1000"
      destination="1001"
      >
    <genericsetup:upgradeStep
        title="Update types"
        description="Enable new behaviors et cetera"
        handler="ploneconf.site.upgrades.v1001.update_types"
        />
    <genericsetup:upgradeStep
        title="Clean up site structure"
        description="Move talks to to their page"
        handler="ploneconf.site.upgrades.v1001.cleanup_site_structure"
        />
    <genericsetup:upgradeStep
        title="Update catalog"
        description="Add and populate new indexes. Add criteria."
        handler="ploneconf.site.upgrades.v1001.update_indexes"
        />
  </genericsetup:upgradeSteps>

</configure>
```

From time to time you may want to update the catalog manually. To do so, go to <http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes>, select the new indexes and click {guilabel}`Reindex`.
You can also rebuild the whole catalog by going to the {guilabel}`Advanced` tab and clicking {guilabel}`Clear and Rebuild`.


(upgrade-steps-collection-criteria-label)=

## Add collection criteria

The following additional criteria allow us to create a search block constrained to talks with facets to filter for audience, speaker and room.

`profiles/default/registry/querystring.xml`

```{code-block} xml

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.speaker"
  >
    <value key="title">Speaker</value>
    <value key="enabled">True</value>
    <value key="sortable">True</value>
    <value key="operations">
      <element>plone.app.querystring.operation.string.is</element>
      <element>plone.app.querystring.operation.string.contains</element>
    </value>
    <value key="group"
           i18n:translate=""
    >Metadata</value>
  </records>

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.audience"
  >
    <value key="title">Audience</value>
    <value key="enabled">True</value>
    <value key="sortable">False</value>
    <value key="operations">
      <element>plone.app.querystring.operation.selection.any</element>
      <element>plone.app.querystring.operation.selection.all</element>
      <element>plone.app.querystring.operation.selection.none</element>
    </value>
    <value key="group"
           i18n:translate=""
    >Metadata</value>
    <value key="vocabulary">ploneconf.audiences</value>
  </records>

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.room"
  >
    <value key="title">Room</value>
    <value key="enabled">True</value>
    <value key="sortable">False</value>
    <value key="operations">
      <element>plone.app.querystring.operation.selection.any</element>
      <element>plone.app.querystring.operation.selection.all</element>
      <element>plone.app.querystring.operation.selection.none</element>
    </value>
    <value key="group"
           i18n:translate=""
    >Metadata</value>
    <value key="vocabulary">ploneconf.rooms</value>
  </records>
```

```{seealso}
For a full list of all existing QueryField declarations see https://github.com/plone/plone.app.querystring/blob/master/plone/app/querystring/profiles/default/registry.xml#L197.

For a full list of all existing operations see https://github.com/plone/plone.app.querystring/blob/master/plone/app/querystring/profiles/default/registry.xml#L1.
```


(upgrade-steps-search-block-label)=

## Apply the new criterion to create a search block for talks

As soon as you run the upgrade steps, you can now add a search block to your 'schedule' page that provides facets to filter for audience, et cetera.

```{figure} _static/search_block.png
:alt: search block

search block
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

This is a basic block variation.
Block variations can have variations: See {doc}`plone6docs:volto/blocks/extensions` for advanced techniques.
