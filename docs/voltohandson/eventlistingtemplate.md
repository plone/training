---
myst:
  html_meta:
    "description": "Learn How to code a custom template for the listing block"
    "property=og:description": "Learn How to code a custom template for the listing block"
    "property=og:title": "Events listing template"
    "keywords": "Plone, Volto, Training, Block, Listing"
---

# Events listing template

One of the most used blocks in Volto is the listing block. It allows editors to automatically list contents on a page that fit a certain criteria (e.g. all pages of a specific content type). To always display content in the most visually useful way (you might want a list of upcoming events look different to a list of the latest projects of your company) the listing has the possibility to appear in different visual templates. In vanilla volto those are the `default`, `summary` and `image gallery` templates. To learn how to create a new listing template we will recreate the Plone upcoming events listing from a bit further down the page.

```{image} /_static/ploneorg-event-listing.png
:align: center
:alt: plone.org event listing
```

## create some dummy events to display

At the moment of writing this training there were 2 Events "Plone Conf 2022" and "2022 Meeting of the Plone Foundation". To have some events to display in your listing, create at least 2 pages of the type event somewhere on the page with a title, date and location.

## create the actual template

Inside of your `components/Blocks/` directory create a new folder called `listing` and in there a file `eventListingTemplate.jsx`. Before we create the proper template we will first create a simple mock like this:

```jsx
import React from "react";

const eventListingTemplate = ({ items }) => {
  return (
    <div>
      <h2>Events:</h2>
      {items.map((item) => (
        <ul>
          <li>{item.title}</li>
        </ul>
      ))}
    </div>
  );
};

export default eventListingTemplate;
```

Export the component from the `index.js` as you already did with the Block View components and import it to your `config.js`:

```js
import {
  HighlightBlockView,
  HighlightBlockEdit,
  DownloadLinkBlockEdit,
  DownloadLinkBlockView,
  eventListingTemplate,
}
```

After that you can add your template to the list of available listing templates by adding this to the `applyConfig` function:

```js
config.blocks.blocksConfig.listing.variations = [
  ...config.blocks.blocksConfig.listing.variations,
  {
    id: "eventListing",
    title: "Events",
    template: eventListingTemplate,
  },
];
```

This should be enough to show make the "Events" template choosable when adding a listing Block. Add a listing Block to your page, and set it to filter for elements of the `Type` `Event`. Choose `Events` as the template at the top of your block.

## Style the template properly

To style the template, replace the code from `eventListingTemplate.jsx` with:

```jsx
import React from "react";
import { Grid } from "semantic-ui-react";
import { UniversalLink } from "@plone/volto/components";
import moment from "moment";

const eventListingTemplate = ({ items }) => {
  console.log(items);
  return (
    <Grid columns={3}>
      <Grid.Column width={4}>
        <div className="text-col">
          <h2>
            <UniversalLink href="/events">Upcoming events</UniversalLink>
          </h2>
          <p>
            The Plone community regularly meets for sprints, conferences,
            training classes, and symposia.
          </p>
          <UniversalLink href="/add?type=Event" className="ui button">
            Add an event
          </UniversalLink>
          <br />
          <UniversalLink href="/add?type=sprint" className="ui button">
            Add a sprint
          </UniversalLink>
          <br />
          <UniversalLink href="/add?type=News Item" className="ui button">
            Add a news item
          </UniversalLink>
          <br />
          <UniversalLink href="events" className="ui button">
            All events
          </UniversalLink>
        </div>
      </Grid.Column>
      <Grid.Column width={8} className="listing-col">
        <Grid columns={2}>
          {items.map((item) => (
            <Grid.Column width={5} className="item">
              <UniversalLink href={item["@id"]}>
                <div className="date">
                  {moment(item.start).format("MMMM D, YYYY")}
                </div>
                <div className="item-body">
                  <h3>{item.title}</h3>
                  <p className="location">{item.location}</p>
                </div>
              </UniversalLink>
            </Grid.Column>
          ))}
        </Grid>
      </Grid.Column>
    </Grid>
  );
};

export default eventListingTemplate;
```

Note that the `moment` js is imported into the component to properly format the dates of the events.

To finish the styling, now paste the provided CSS to your `custom.overrides`:

```less
.block.listing.eventListing {
  background: #e8eef2;

  .text-col {
    background: #d8e2e9;
    margin: 15px;
    padding: 15px;

    h2 {
      font-size: 30px;
    }
    p {
      font-size: 21px;
      font-weight: 300;
    }
    a.ui.button {
      color: @white;
      font-weight: normal;
      background-color: #00608b;
      border: solid 1px #004767;
      margin-bottom: 10px;
    }
  }

  .listing-col {
    .item {
      background: @white;
      padding: 0;
      margin: 1em;
      .date {
        background: #1f1238;
        color: @white;
        text-transform: uppercase;
        text-align: right;
        padding: 5px 10px;
        font-weight: 600;
        font-size: 20px;
      }
      .item-body {
        margin: 10px;
        h3 {
          font-size: 24px;
          margin-bottom: 10px;
          font-weight: bold;
        }
        .location {
          color: @grey;
          font-weight: bold;
        }
      }
    }
  }
}
```
