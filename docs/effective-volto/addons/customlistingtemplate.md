---
myst:
  html_meta:
    "description": "Create a custom Listing block template"
    "property=og:description": "Create a custom Listing block template"
    "property=og:title": "Create a custom Listing block template"
    "keywords": "Volto, Plone, Volto Blocks, Listing block"
---

# Create a custom Listing block variation

The Listing block is one of the most versatile blocks, and a driver to many of
Volto's more "advanced" technologies, such as variations.

It can be shaped into many forms, such as sliders, carousels, cards and more.
To develop a new variation, take a look at one of the existing Listing block
variations, such as the
[SummaryTemplate](https://github.com/plone/volto/blob/43ea1b68e643c53065a6fb5f613cbeb5008b0389/src/components/manage/Blocks/Listing/SummaryTemplate.jsx):

The principle is simple: the component receives and renders the list of items
(result proxies) from the Listing block.

Create {file}`src/components/manage/Blocks/Listing/CardsTemplate.jsx`

```
const CardsTemplate = ({ items, linkTitle, linkHref, isEditMode }) => {
  return items.map((item) => <div key={item.['@id']}>{item.title}</div>);
}
```

To register the new block variation, add it to the existing variations:

```
import { CardsTemplate } from './components';

export const applyConfig = (config) => {
  config.blocks.blocksConfig.listing.variations.push({
    id: 'cards',
    template: CardsTemplate,
  });
  return config;
}
```
