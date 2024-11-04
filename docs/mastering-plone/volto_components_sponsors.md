---
myst:
  html_meta:
    "description": "How to fetch data from the backend"
    "property=og:description": "How to fetch data from the backend"
    "property=og:title": "The Sponsors Component, how to fetch data from the backend"
    "keywords": "REST API, Semantic UI"
---

(volto-sponsors-component-label)=

# The Sponsors Component

In a previous chapter {doc}`dexterity_3` you created the `sponsor` content type.
Now let's learn how to display content of this type.

```{card}
To be solved task in this part:

- Advert to sponsors on all pages, sorted by level

In this part you will:

- Display data from fetched content

Topics covered:

- Create React component
- Use React action of Volto to fetch data from Plone backend via REST API
- Style component with Semantic UI
```

````{card} Frontend chapter

Checkout `volto-ploneconf` at tag "listing_variation":

```shell
git checkout listing_variation
```

The code at the end of the chapter:

```shell
git checkout sponsors
```

More info in {doc}`code`
````


```{figure} _static/volto_component_sponsors.png
:alt: Sponsors component
```

```{only} not presentation
For sponsors we will stay with the default view as we will only display the sponsors in the footer and do not modify their own pages.
Using what you learned in {doc}`volto_talkview` you should be able to write a view for sponsors if you wanted to.
```

(volto-component-component-label)=

## A React component

React components let you split the UI into independent, reusable pieces, and think about each piece in isolation.

- You can write a view component for the current context - like the `TalkView`.
- You can also write components that are visible on all views of content objects.
- Volto comes with several components like header, footer, sidebar. In fact everything of the UI is build of nested components.
- Inspect existing components with the React Developer Tools.


(volto-component-sponsors-label)=

## The Sponsors Component

**Steps to take**

- Copy and customize the Footer component.
- Create component to fetch data from backend and to display the fetched data.

(volto-component-customizing-label)=

### Customizing the Footer

You can override any component that lives inside Volto's source folder `core/packages/volto/src/components` and adapt it to your needs, without touching the original component.

The sponsors shall live in the footer of a page. To customize the given footer component we copy the `Footer.jsx` file {file}`core/packages/volto/src/components/theme/Footer/Footer.jsx` from Volto. We insert the copied file to our app regarding the original folder structure but inside our customizations folder {file}`packages/ploneconf.site/src/customizations/components/theme/Footer/Footer.jsx`.

In this file `Footer.jsx` we can now modify the to be rendered html by adding a subcomponent `Sponsors`.

Be aware that the following code is JSX. JSX is Javascript that can handle html in a handy way. What you see is a component defined as an arrow function. The function returns markup consisting of enriched html: The tag `<Sponsors />` forces a rendering of the Sponsors component.

```{code-block} jsx
:emphasize-lines: 4
:linenos:

const Footer = ({ intl }) => (
  <Segment role="contentinfo" vertical padded>
    <Container>
      <Sponsors />
      <Segment
        basic
        inverted
        color="grey"
        textAlign="center"
        className="discreet"
      >
```

This will show an additional component.
It is visible on all pages as it is a subcomponent of the `Footer` component.
Later on it can be made conditional if necessary.

To create the component `Sponsors` we add a folder {file}`src/components/Sponsors/` with a file {file}`Sponsors.jsx`. In this file we can now define our new component.

Start with a placeholder to see that your registration actually works:

```{code-block} jsx
:linenos:

const Sponsors = () => {
  return <h3>Our sponsors</h3>;
};

export default Sponsors;
```

A component is just a function that returns markup.

Go back to your modified `Footer` component.
The `Footer` component needs to know where to find the added `Sponsor` component.
We import the `Sponsor` component at the top of our modified `Footer` component.

{file}`src/customizations/components/theme/Footer/Footer.jsx`:

```{code-block} jsx
:linenos:

import { Sponsors } from '@package/components';
```

For an import using the alias '@package/components', we need to add a conveniance import in the root `src/components/index.js`.

```{code-block} jsx
import TalkView from './Views/Talk';
import Sponsors from './Sponsors/Sponsors';

export { Sponsors, TalkView };
```

After restarting the frontend with `make start`, we are now ready to visit an arbitrary page to see the new component.
A restart is necessary on newly added files. As long as you just edit existing files of your app, your browser is updating automagically by app configuration.

(volto-component-datafetching-label)=

### Getting the sponsors data

With our `Sponsors` component in place we can take the next step and explore Volto some more to figure out how it does data fetching.

As the data is in the backend, we need to find a way to address it.
Volto provides various predefined actions to communicate with the backend (fetching data, creating content, editing content, etc.).
A Redux action communicates with the backend and has a common pattern:
It addresses the backend via REST API and updates the global app store according to the response of the backend.
A component calls an action and has hereupon access to the global app store (shortened: store) with the fetched data.

For more information which actions are already provided by Volto have a look at {file}`core/packages/volto/src/actions`.

Our component will use the action `searchContent` to fetch data of all sponsors.
It takes as arguments the path where to search, the information what to search and an argument with which key the data should be stored in the store.
Remember: the result is stored in the global app store.

So if we call the action `searchContent` to fetch data of sponsors, that means data of the instances of content type `sponsor`, then we can access this data from the store.

The Hook `useEffect` lets you perform side effects in `function components`. We use it to fetch the sponsors data from the backend.

```{code-block} jsx
:linenos:

const dispatch = useDispatch();

useEffect(() => {
  dispatch(
    searchContent(
      '/',
      {
        portal_type: ['sponsor'],
        review_state: 'published',
        fullobjects: true,
      },
      'sponsors',
    ),
  );
}, [dispatch]);
```

#### Search options

- The default representation for search results is a summary that contains only the most basic information like **title, review state, type, path and description**.
- With the option `fullobjects` all available field values are present in the fetched data.
- Another option is `metadata_fields`, which allows to get more attributes (selection of Plone catalog metadata columns) than the default search. The search is done without a performance expensive fetch via option `fullobjects` as soon as the attributes are available from catalog as metadata.

Possible **sort criteria** are indices of the Plone catalog.


```{code-block} jsx
:linenos:
:emphasize-lines: 10

const dispatch = useDispatch();

useEffect(() => {
  dispatch(
    searchContent(
      '/',
      {
        portal_type: ['News Items'],
        review_state: 'published',
        sort_on: "effective",
      },
      'sponsors',
    ),
  );
}, [dispatch]);
```

Check which info you get with the search request in Google developer tools:

```{figure} _static/search_response.png
:alt: search response
```

```{seealso}
REST API Documentation {doc}`plone6docs:plone.restapi/docs/source/endpoints/searching`
```


(volto-component-store-label)=

### Connection of component and store

Let's connect the store to our component. The Selector Hook `useSelector` allows a `function component` to connect to the store.

It's worth exploring the store of our app with the Redux Dev Tools which are additional Dev Tools to React Dev Tools.
There you can see what is stored in `state.search.subrequests.sponsors`.
And you can walk through time and watch how the store is changing.

```{code-block} jsx
:linenos:

const sponsors = useSelector((state) =>
  groupedSponsorsByLevel(state.search.subrequests.sponsors?.items),
);
```

With these both: dispatching the action and a connection to the state in place, the component can call the predefined action `searchContent` and has access to the fetched data via its constant `sponsors`.

The next step is advanced and can be skipped on a first reading.
As by now we fetch the sponsors data on mounting event of the component.
The mounting is done once on the first visit of a page of our app.
What if a new sponsor is added or a sponsor is published?
We want to achieve a re-rendering of the component on changed sponsorship.
To subscribe to these changes in sponsorship, we extend our already defined connection.

```{code-block} jsx
:emphasize-lines: 1,15
:linenos:

const content = useSelector((state) => state.workflow.transition);

useEffect(() => {
  dispatch(
    searchContent(
      '/',
      {
        portal_type: ['sponsor'],
        review_state: 'published',
        fullobjects: true,
      },
      'sponsors',
    ),
  );
}, [dispatch, content]);
```

Listening to this subscription the component fetches the data from the store if a workflow state changes.

(volto-component-presentation-label)=

### Presentation of the prepared data

With the data fetched and accessible in the component constant `sponsors` we can
now render the sponsors data. 

We prepare the sponsors data as a dictionary grouped by sponsor level: groupedSponsorsByLevel.

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

With the subscription `sponsors` we can now show a nested list.

```{code-block} jsx
:linenos:

{keys(sponsors).map((level) => {
  return (
    <div key={level} className={'sponsorlevel ' + level}>
      <h3>{level.toUpperCase()}</h3>
      <Grid centered>
        <Grid.Row centered>
          {sponsors[level].map((item) => (
            <Grid.Column key={item['@id']} className="sponsor">
              <Component
                componentName="PreviewImage"
                item={item}
                alt={item.title}
                responsive={true}
                className="ui image"
              />
            </Grid.Column>
          ))}
        </Grid.Row>
      </Grid>
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
import { Segment, Grid } from 'semantic-ui-react';
import { keys, isEmpty } from 'lodash';

import { ConditionalLink, Component } from '@plone/volto/components';
import { searchContent } from '@plone/volto/actions';

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

  return !isEmpty(sponsors) ? (
    <Segment basic textAlign="center" className="sponsors">
      <div className="sponsorheader">
        <h2 className="subheadline">SPONSORS</h2>
      </div>
      {keys(sponsors).map((level) => {
        return (
          <div key={level} className={'sponsorlevel ' + level}>
            <h3>{level.toUpperCase()}</h3>
            <Grid centered>
              <Grid.Row centered>
                {sponsors[level].map((item) => (
                  <Grid.Column key={item['@id']} className="sponsor">
                    <Component
                      componentName="PreviewImage"
                      item={item}
                      alt={item.title}
                      responsive={true}
                      className="ui image"
                    />
                  </Grid.Column>
                ))}
              </Grid.Row>
            </Grid>
          </div>
        );
      })}
    </Segment>
  ) : (
    <></>
  );
};

export default Sponsors;
```
````

We group the sponsors by sponsorship level.

An Object `sponsors` using the sponsorship level as key helps to build rows with sponsors by sponsorship level.

The Volto component `Image` is used to display the logo.
It cares about the markup of an html image node with all necessary attributes in place.

We also benefit from [Semantic UI React](https://react.semantic-ui.com/) component `Grid` to build our list of sponsors. The styling can be customized but these predefined components help simplifying the code and achieve an app wide harmonic style.

See the new footer. A restart is not necessary as we didn't add a new file. The browser updates automagically by configuration.

```{figure} _static/volto_component_sponsors.png
:align: left
:alt: Sponsors component
```

(volto-component-exercise-label)=

## Exercise

Modify the component to display a sponsor logo as a link to the sponsors website. The address is set in sponsor field "url".

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 1-5, 13

<ConditionalLink
  to={item.url}
  openLinkInNewTab={true}
  condition={item.url}
>
  <Component
    componentName="PreviewImage"
    item={item}
    alt={item.title}
    responsive={true}
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

% volto-component-summary-label:

## Summary

You know how to fetch data from backend. With the data you are able to create a component displayed at any place in the website.
