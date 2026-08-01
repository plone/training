---
myst:
  html_meta:
    "description": "How to fetch data from the backend"
    "property=og:description": "How to fetch data from the backend"
    "property=og:title": "The Sponsors component"
    "keywords": "REST API, Semantic UI"
---

(volto-sponsors-component-label)=

# The Sponsors component

In a previous chapter, {doc}`dexterity_3`, you created the sponsor content type.
Now let's learn how to display content of this type.

```{card}
In this part you will:

- Add a component advertising sponsors at the bottom of all pages
- Display data from fetched content

Topics covered:

- Display a React component in a slot
- Use a Volto Redux action to fetch data from Plone backend via the REST API
- Style the component with Semantic UI
```

````{card}

Check out `mastering-plone-project` at tag `searchable`:

```shell
git checkout searchable
```

The code at the end of the chapter:

```shell
git checkout sponsors
```

More info in {doc}`code`
````

```{only} not presentation
For sponsors we will stay with the default view as we will only display the sponsors in the footer and not modify their own pages.
Using what you learned in {doc}`volto_talkview` you should be able to write a view for sponsors if you want to.
```

```{figure} _static/volto_component_sponsors.png
:alt: Sponsors component
```

(volto-component-component-label)=

## Slots

React components let you split the UI into independent, reusable pieces, and think about each piece in isolation.
Volto comes with several components like header, footer, and sidebar.
In fact everything in the UI is built of nested components.

We've already seen how to register a custom component as the view for a content type.
In this case we'll do something different, and add a component to a slot.
A slot is a defined plugin point in the existing Volto components where add-ons can show their own components.
Adding a sponsors component to the `belowContent` slot will let it be displayed below every content view.

```{seealso}
{doc}`plone6docs:volto/configuration/slots`
```


(volto-component-sponsors-label)=

## The Sponsors component

To create the component `Sponsors` we add a folder {file}`frontend/packages/volto-ploneconf-site/src/components/Sponsors/` with a file {file}`Sponsors.jsx`.
In this file we can now define our new component.

Start with a placeholder to see that your registration actually works:

```{code-block} jsx
:linenos:

const Sponsors = () => {
  return <h3>Our sponsors</h3>;
};

export default Sponsors;
```

A component is just a function that returns JSX markup.

Now we can configure this component to be shown in the `belowContent` slot.
Edit the file {file}`frontend/packages/volto-ploneconf-site/config/settings.ts`.

```{code-block} tsx
:linenos:
:emphasize-lines: 5, 31-35

import type { ConfigType } from '@plone/registry';
import type { BlockExtension, ViewsConfig } from '@plone/types';
import TalkView from '../components/Views/TalkView';
import TalkListingBlockVariation from '../components/variations/TalkListingBlockVariation';
import Sponsors from '../components/Sponsors/Sponsors';

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

  config.registerSlotComponent({
    slot: 'belowContent',
    name: 'sponsors',
    component: Sponsors,
  });

  return config;
}
```

After restarting the frontend with `make frontend-start`, we are now ready to visit an arbitrary page to see the new component.

```{tip}
A restart is necessary for Volto to find newly added files.
As long as you just edit existing files of your app, your browser will update automatically.
```

(volto-component-datafetching-label)=

## Fetch the sponsors data

With our `Sponsors` component in place we can take the next step and explore Volto some more to figure out how it does data fetching.

As the data is in the backend, we need to find a way to fetch it.
Volto provides various predefined actions to communicate with the backend (fetching content, creating content, editing content, etc.).
A Redux action communicates with the backend and has a common pattern.
It makes a request to the backend via the REST API and updates the global app store (in browser memory) according to the response of the backend.
A component can call actions, and select data from the store.

For more information which actions are already provided by Volto have a look at {file}`frontend/core/packages/volto/src/actions`.

Our component will use the action `searchContent` to fetch the data of all sponsors.
It takes as arguments the path where to search, the search parameters, and an argument with which key the data should be stored in the store.
Remember: the result is stored in the global app store.

So if we call the action `searchContent` to fetch data of sponsors (that is, all content items with type `sponsor`), then we can access this data from the store.

The React hook `useEffect` lets you perform side effects after a component is rendered.
We use it to fetch the sponsors data from the backend when the component is first loaded.

```{code-block} jsx
:linenos:
:emphasize-lines: 1-3, 6-20

import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { searchContent } from '@plone/volto/actions/search/search';

const Sponsors = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(
      searchContent(
        '/',
        {
          portal_type: ['sponsor'],
          review_state: 'published',
          sort_on: 'effective',
          metadata_fields: ['level', 'url'],
        },
        'sponsors',
      ),
    );
  }, [dispatch]);

  return <h3>Our sponsors</h3>;
};

export default Sponsors;
```

### Search options

- The default representation for search results is a summary that contains only the most basic information like **title, review state, type, path and description**.
- `metadata_fields` lets us specify additional catalog metadata columns that we'd like to include in the results.
- We could also pass the option `fullobjects: true` to get the full serialization of all fields from the content item.
  However this requires loading each object fully instead of just using data in the catalog, so it is slower.
- `sort_on` specifies which catalog index should be used to sort the results.

````{tip}
Check which results you get in the Network tab of the browser developer tools:

```{figure} _static/search_response.png
:alt: search response
```
````

```{seealso}
REST API Documentation {doc}`plone6docs:plone.restapi/docs/source/endpoints/searching`
```


(volto-component-store-label)=

## Use the fetched data

Let's connect our component to the data which has been fetched into the store.
The hook `useSelector` allows a component to select a specific part of the data in the store.

```{tip}
It's worth exploring the store of our app with the Redux Dev Tools.
There you can see what is stored in `state.search.subrequests.sponsors`.
And you can walk through time and watch how the store is changing.
```

```{code-block} jsx
:linenos:

const sponsors = useSelector((state) =>
  groupedSponsorsByLevel(state.search.subrequests.sponsors?.items),
);
```

Now the component has access to the sponsors data, and will re-render when it is updated after the `searchContent` action has finished.

````{note}
This note is advanced and can be skipped on a first reading.

So far we fetch the sponsors data once, after the component is first mounted.
The mounting is done once on the first visit of a page of our app.
What if a new sponsor is added or a sponsor is published?
We want to achieve a re-rendering of the component when the user publishes a new sponsor.
To subscribe to these changes in workflow status, we extend the dependencies of the `useEffect` hook.

```{code-block} jsx
:emphasize-lines: 1,15
:linenos:

const workflowTransition = useSelector((state) => state.workflow.transition);

useEffect(() => {
  dispatch(
    searchContent(
      '/',
      {
        portal_type: ['sponsor'],
        review_state: 'published',
        sort_on: 'effective',
        metadata_fields: ['level', 'url'],
      },
      'sponsors',
    ),
  );
}, [dispatch, workflowTransition]);
```

Listening to this subscription the component fetches the data from the store if a workflow state changes.
````


(volto-component-presentation-label)=

## Render the sponsor data

With the data fetched and accessible in the variable `sponsors`, we can
now render the sponsors data.

We prepare the sponsors data as a dictionary grouped by sponsor level:

```js
const groupedSponsorsByLevel = (array = []) =>
  array.reduce((obj, item) => {
    let token = item.level?.token || 'bronze';
    obj[token] ? obj[token].push(item) : (obj[token] = [item]);
    return obj;
  }, {});
```

Which results in an dictionary Object available with our subscription `sponsors`:

```js
{
  bronze: [sponsordata1, sponsodata2]
}
```

Now we can show a nested list.

```{code-block} jsx
:linenos:

{Object.keys(sponsors).map((level) => {
  return (
    <div key={level} className={'sponsorlevel ' + level}>
      <h3>{level.toUpperCase()}</h3>
      <div className="ui centered grid">
        <div className="centered row">
          {sponsors[level].map((item) => (
            <div key={item['@id']} className="sponsor column">
              <Component
                componentName="PreviewImage"
                item={item}
                image_field="logo"
                imageField="logo"
                alt={item.title}
                width="100"
                height="auto"
                className="ui image"
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
})}
```

````{dropdown} Complete code of the Sponsors component
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:linenos:

import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Component from '@plone/volto/components/theme/Component/Component';
import { searchContent } from '@plone/volto/actions/search/search';

const groupedSponsorsByLevel = (array = []) =>
  array.reduce((obj, item) => {
    let token = item.level || 'bronze';
    obj[token] ? obj[token].push(item) : (obj[token] = [item]);
    return obj;
  }, {});

const Sponsors = () => {
  const dispatch = useDispatch();
  const sponsors = useSelector((state) =>
    groupedSponsorsByLevel(state.search.subrequests.sponsors?.items),
  );

  useEffect(() => {
    dispatch(
      searchContent(
        '/',
        {
          portal_type: ['sponsor'],
          review_state: 'published',
          sort_on: 'effective',
          metadata_fields: ['level', 'url'],
        },
        'sponsors',
      ),
    );
  }, [dispatch]);

  return sponsors && Object.keys(sponsors).length > 0 ? (
    <div className="ui container">
      <div className="ui basic center aligned segment sponsors">
        <div className="sponsorheader">
          <h2 className="subheadline">SPONSORS</h2>
        </div>
        {Object.keys(sponsors).map((level) => {
          return (
            <div key={level} className={'sponsorlevel ' + level}>
              <h3>{level.toUpperCase()}</h3>
              <div className="ui centered grid">
                <div className="centered row">
                  {sponsors[level].map((item) => (
                    <div key={item['@id']} className="sponsor column">
                      <Component
                        componentName="PreviewImage"
                        item={item}
                        image_field="logo"
                        imageField="logo"
                        alt={item.title}
                        width="100"
                        height="auto"
                        className="ui image"
                      />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  ) : (
    <></>
  );
};

export default Sponsors;
```
````

We group the sponsors by sponsorship level.

An object `sponsors` using the sponsorship level as key helps to build rows with sponsors by sponsorship level.

The Volto component `PreviewImage` is used to display the logo.

We also benefit from the [Semantic UI](https://semantic-ui.com/) grid component to build our list of sponsors.
The styling can be customized but these predefined components help simplify the code and achieve an app-wide harmonic style.

See the new footer.
A restart is not necessary, as we didn't add a new file.

```{figure} _static/volto_component_sponsors.png
:align: left
:alt: Sponsors component
```

(volto-component-exercise-label)=

## Exercise

Modify the component to display a sponsor logo as a link to the sponsors website.
The address is stored in sponsor field `url`.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
import ConditionalLink from '@plone/volto/components/manage/ConditionalLink/ConditionalLink';

<ConditionalLink
  to={item.url}
  openLinkInNewTab={true}
  condition={item.url}
>
  <Component
    componentName="PreviewImage"
    item={item}
    image_field="logo"
    imageField="logo"
    alt={item.title}
    width="100"
    height="auto"
    className="ui image"
  />
</ConditionalLink>
```

The image component is now rendered with a wrapping anchor tag.

```{code-block} html
<a
  href="https://www.rohberg.ch" 
  target="_blank"
  rel="noopener noreferrer"
  class="external">
    <img
    src="/sponsors/orangenkiste/@@images/image-170-1914fccf158dd627126054f9c7bb1b17.png"
    width="170" height="170"
    class="ui image responsive"
    srcset="/sponsors/orangenkiste/@@images/image-32-36422a6365defe3ee485bbecaa5cfeda.png 32w, /sponsors/orangenkiste/@@images/image-64-c28b7f3d3c5b0c1de514fbf81091c43c.png 64w, /sponsors/orangenkiste/@@images/image-128-307f157f27fecd23ec2896b44f6ac4aa.png 128w"
    fetchpriority="high"
    alt="Orangenkiste"
    image_field="image"
    >
</a>
```
````

(volto-component-summary-label)=

## Summary

You know how to fetch data from backend.
With the data you are able to create a component displayed at any place in the website.
