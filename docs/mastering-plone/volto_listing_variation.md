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

- Add more indexes and criteria
- Create a search block variation

Topics covered:

- block variation
```

````{card} Frontend chapter

Check out `mastering-plone-project` at tag `upgrade_steps`:

```shell
git checkout upgrade_steps
```

The code at the end of the chapter:

```shell
git checkout listing_variation
```

More info in {doc}`code`
````

We've already created a {doc}`custom_search` that lists all the talks, but it would be nice to improve it to show more information about each talk and allow filtering by additional facets.
Let's add a variation of the search block to display talks with their event date, room, audience and speaker name.
The result will look like this:

```{figure} _static/listing_variation.png
:alt: block variation for the search block to show more than title and description

block variation for the search block to show more than title and description
```


(search-block-variation-indexes-label)=

## Add catalog indexes

In order to add facets for the audience and room, we have to make sure they are indexed.
We'll also add them as metadata columns so they are included in the search results data.

Update {file}`backend/src/ploneconf/site/profiles/default/catalog.xml`.

```{code-block} xml
:emphasize-lines: 17-38

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

While we're at it, we also added more metadata columns that we'll need in one of the next chapters.
We will need to search for sponsors and get the results with the values of the `url` and `level` fields.

We add a metadata column for these fields to avoid loading full content objects while searching.
This would be okay, but slower.
The search request gets an attribute from catalog brains unless the attribute is not available, then fetches the real object.


(search-block-variation-criteria-label)=

## Add collection criteria

The following additional criteria allow us to create a search block constrained to talks with facets to filter for audience, speaker and room.

`backend/src/ploneconf/site/profiles/default/registry/querystring.xml`

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


## Add upgrade step

A reinstallation of the add-on would leave the new catalog indexes empty.
Therefore we write an upgrade step to not only add indexes and criteria, but also reindex all talks.

`backend/src/ploneconf/site/profiles/default/metadata.xml`:

```{code-block} xml
:emphasize-lines: 3

<?xml version="1.0" encoding="utf-8"?>
<metadata>
  <version>1002</version>
  <dependencies>
    <dependency>profile-plone.volto:default</dependency>
    <dependency>profile-plone.app.caching:default</dependency>
    <dependency>profile-plone.app.caching:with-caching-proxy</dependency>
  </dependencies>
</metadata>
```

`backend/src/ploneconf/site/upgrades/v1002.py`:

```python
from plone import api

import logging


logger = logging.getLogger(__name__)


def update_indexes(setup_tool):
    # Reindexing content
    for brain in api.content.find(portal_type=["talk", "sponsor"]):
        obj = brain.getObject()
        obj.reindexObject()
        logger.info(f"{obj.id} reindexed.")
```

`backend/src/ploneconf/site/upgrades/configure.zcml`:

```{code-block} xml
:emphasize-lines: 23-38

<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    >

  <genericsetup:upgradeSteps
      profile="ploneconf.site:default"
      source="1000"
      destination="1001"
      >
    <genericsetup:upgradeDepends
        title="Update types"
        description="Run the typeinfo import step"
        import_steps="typeinfo"
        />
    <genericsetup:upgradeStep
        title="Clean up site structure"
        description="Move talks to to their page"
        handler="ploneconf.site.upgrades.v1001.cleanup_site_structure"
        />
  </genericsetup:upgradeSteps>

  <genericsetup:upgradeSteps
      profile="ploneconf.site:default"
      source="1001"
      destination="1002"
      >
    <genericsetup:upgradeDepends
        title="Update catalog and querystring configuration"
        description="Run catalog and registry import steps"
        import_steps="catalog plone.app.registry"
        />
    <genericsetup:upgradeStep
        title="Reindex talks"
        description="Populate new indexes"
        handler="ploneconf.site.upgrades.v1002.update_indexes"
        />
  </genericsetup:upgradeSteps>

</configure>
```

```{tip}
From time to time you may want to reindex catalog indexes manually.
To do so, go to <http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes>, select the new indexes and click {guilabel}`Reindex`.
You can also rebuild the whole catalog by going to the {guilabel}`Advanced` tab and clicking {guilabel}`Clear and Rebuild`.
This can take some time in a large site!
```


(upgrade-steps-search-block-label)=

## Create a search block for talks

As soon as you run the upgrade steps, you can now add a search block to your 'schedule' page that provides facets to filter for audience, et cetera.

```{figure} _static/search_block.png
:alt: search block

search block
```


(search-block-variation-registration-label)=

## Create and register a new block variation

Some blocks can be enhanced with variations of their layout.
We are writing a block variation for the search block.

First, create a new component `frontend/packages/volto-ploneconf-site/src/components/variations/TalkListingBlockVariation.jsx` by copying the code of an existing block variation, `frontend/core/packages/volto/src/components/manage/Blocks/Listing/SummaryTemplate.jsx`.

```{code-block} jsx
:linenos:
:emphasize-lines: 4, 8-12, 36-41, 43-65

import PropTypes from 'prop-types';
import ConditionalLink from '@plone/volto/components/manage/ConditionalLink/ConditionalLink';
import Component from '@plone/volto/components/theme/Component/Component';
import { When } from '@plone/volto/components/theme/View/EventDatesInfo';

import { flattenToAppURL, isInternalURL } from '@plone/volto/helpers/Url/Url';

const colorMapping = {
  beginner: 'green',
  advanced: 'yellow',
  professional: 'purple',
};

const SummaryTemplate = ({ items, linkTitle, linkHref, isEditMode }) => {
  let link = null;
  let href = linkHref?.[0]?.['@id'] || '';

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
                        let color = colorMapping[audience] || 'green';
                        return (
                          <div className={`ui label ${color}`} key={audience}>
                            {audience}
                          </div>
                        );
                      })}
                    </>
                  )}
                </p>
                <p>{item.description}</p>
              </div>
            </ConditionalLink>
          </div>
        ))}
      </div>

      {link && <div className="footer">{link}</div>}
    </>
  );
};

SummaryTemplate.propTypes = {
  items: PropTypes.arrayOf(PropTypes.any).isRequired,
  linkMore: PropTypes.any,
  isEditMode: PropTypes.bool,
};

export default SummaryTemplate;
```

We register our new variation in `config.blocks.blocksConfig.listing.variations`.
(Listing blocks and search blocks share their variations via this setting.)

Update `frontend/packages/volto-ploneconf-site/src/config/settings.ts`:

```{code-block} jsx
:linenos:
:emphasize-lines: 2, 4, 21-28

import type { ConfigType } from '@plone/registry';
import type { BlockExtension, ViewsConfig } from '@plone/types';
import TalkView from '../components/Views/TalkView';
import TalkListingBlockVariation from '../components/variations/TalkListingBlockVariation';

export default function install(config: ConfigType) {
  // Language settings
  config.settings.defaultLanguage = 'en';
  // Additional language settings for Volto 19 and above, add as many supported languages as needed
  // Languages not added to supportedLanguages will not be included in the build
  // config.settings.supportedLanguages = ['en'];

  config.views = {
    ...(config.views as ViewsConfig),
    contentTypesViews: {
      ...config.views.contentTypesViews,
      talk: TalkView,
    },
  };

  config.blocks.blocksConfig.listing.variations = [
    ...(config.blocks.blocksConfig.listing.variations as BlockExtension[]),
    {
      id: 'talks',
      title: 'Talks',
      template: TalkListingBlockVariation,
    },
  ];

  return config;
}
```



Now select the new variation to apply it to the search block.

```{figure} _static/listing_variation_edit.png
:alt: Apply listing variation

Apply listing variation
```

This is a basic block variation.
See {doc}`plone6docs:volto/blocks/extensions` for advanced techniques.
