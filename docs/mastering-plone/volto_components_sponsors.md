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

Create a React component for content fetched from the backend

````{card} Frontend chapter

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout event
```

Code for the end of this chapter:

```shell
git checkout sponsors
```
````

In the previous chapter {doc}`dexterity_3` you created the `sponsor` content type.
Now let's learn how to display content of this type.

```{card}
To be solved task in this part:

- Advert to sponsors on all pages, sorted by level

In this part you will:

- Display data from fetched content

Topics covered:

- Create React component
- Use React action of Volto to fetch data from Plone via REST API
- Style component with Semantic UI
```

```{figure} _static/volto_component_sponsors.png
:alt: Sponsors component
```

```{only} not presentation
For sponsors we will stay with the default view as we will only display the sponsors in the footer and do not modify their own pages.
The default-view of Volto does not show any of the custom fields you added to the sponsors.
Using what you learned in {doc}`volto_talkview` you should be able to write a view for sponsors if you wanted to.
```

(volto-component-component-label)=

## A React component

React components let you split the UI into independent, reusable pieces, and think about each piece in isolation.

- You can write a view component for the current context - like the `TalkView`.
- You can write a view component that can be selected as view for a set of content objects like the TalkListView.
- You can also write components that are visible on all content objects. In classic Plone we use _viewlets_ for that.
- Volto comes with several components like header, footer, sidebar. In fact everything of the UI is build of nested components.
- Inspect existing components with the React Developer Tools.

(volto-component-sponsors-label)=

## The Sponsors Component

We will now see how to achieve in Volto frontend the equivalent to the Plone viewlet of chapter {doc}`dexterity_3`.

**Steps to take**

- Copy and customize Footer component.
- Create component to fetch data from backend and to display the fetched data.

(volto-component-customizing-label)=

### Customizing the Footer

You can override any component that lives inside Volto's source folder `frontend/omelette/src/components` and adapt it to your needs, without touching the original component.

The sponsors shall live in the footer of a page. To customize the given footer component we copy the `Footer.jsx` file {file}`frontend/omelette/src/components/theme/Footer/Footer.jsx` from Volto. We insert the copied file to our app regarding the original folder structure but inside our customizations folder {file}`frontend/src/customizations/components/theme/Footer/Footer.jsx`.

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

This will show an additional component. It is visible on all pages as it is a subcomponent of the `Footer` component. Later on it can be made conditional if necessary.

To create the component `Sponsors` we add a folder {file}`frontend/src/components/Sponsors/` with a file {file}`Sponsors.jsx`. In this file we can now define our new component.

Start with a placeholder to see that your registration actually works:

```{code-block} jsx
:linenos:

import React from 'react';

const Sponsors = () => {
  return <h3>Our sponsors</h3>;
};

export default Sponsors;
```

A component is just a function that returns markup.

Go back to your modified `Footer` component.
The `Footer` component needs to know where to find the added `Sponsor` component.
We import the `Sponsor` component at the top of our modified `Footer` component.

{file}`frontend/src/customizations/components/theme/Footer/Footer.jsx`:

```{code-block} jsx
:linenos:

import { Sponsors } from '@package/components';
```

After restarting the frontend with `yarn start`, we are now ready to visit an arbitrary page to see the new component.
A restart is necessary on newly added files. As long as you just edit existing files of your app, your browser is updating automagically by app configuration.

(volto-component-datafetching-label)=

### Getting the sponsors data

With our `Sponsors` component in place we can take the next step and explore Volto some more to figure out how it does data fetching.

As the data is in the backend, we need to find a way to address it.
Volto provides various predefined actions to communicate with the backend (fetching data, creating content, editing content, etc.).
A Redux action communicates with the backend and has a common pattern:
It addresses the backend via REST API and updates the global app store according to the response of the backend.
A component calls an action and has hereupon access to the global app store (shortened: store) with the fetched data.

For more information which actions are already provided by Volto have a look at {file}`frontend/omelette/src/actions`.

Our component will use the action `searchContent` to fetch data of all sponsors.
It takes as arguments the path where to search, the information what to search and an argument with which key the data should be stored in the store.
Remember: the result is stored in the global app store.

So if we call the action `searchContent` to fetch data of sponsors, that means data of the instances of content type `sponsor`, then we can access this data from the store.

The Hook `useEffect` lets you perform side effects in `function components`. We use it to fetch the sponsors data from the backend.

```{code-block} jsx
:linenos:

const dispatch = useDispatch();

React.useEffect(() => {
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
- Another option is `metadata_fields`, which allows to get more attributes (selection of Plone catalog metadata columns) than the default search without a performance expensive fetch via option fullobjects.

Possible **sort criterions** are indices of the Plone catalog.


```{code-block} jsx
:linenos:
:emphasize-lines: 10

const dispatch = useDispatch();

React.useEffect(() => {
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

```{seealso}
{doc}`plone6docs:plone.restapi/docs/source/endpoints/searching`
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

React.useEffect(() => {
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

<List>
  {keys(sponsors).map((level) => {
    return (
      <List.Item key={level} className={'sponsorlevel ' + level}>
        <h3>{level.toUpperCase()}</h3>
        <List horizontal>
          {sponsors[level].map((item) => (
            <List.Item key={item['@id']} className="sponsor">
              {item.logo ? (
                <Image
                  className="logo"
                  as="a"
                  href={item.url}
                  target="_blank"
                  src={flattenToAppURL(item.logo.scales.preview.download)}
                  size="small"
                  alt={item.title}
                  title={item.title}
                />
              ) : (
                <a href={item['@id']}>{item.title}</a>
              )}
            </List.Item>
          ))}
        </List>
      </List.Item>
    );
  })}
</List>
```

````{dropdown} Complete code of the Sponsors component
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:linenos:

import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Segment, List, Image } from 'semantic-ui-react';
import { keys, isEmpty } from 'lodash';

import { flattenToAppURL } from '@plone/volto/helpers';
import { searchContent } from '@plone/volto/actions';

const groupedSponsorsByLevel = (array = []) =>
  array.reduce((obj, item) => {
    let token = item.level?.token || 'bronze';
    obj[token] ? obj[token].push(item) : (obj[token] = [item]);
    return obj;
  }, {});

const Sponsors = () => {
  const dispatch = useDispatch();
  const sponsors = useSelector((state) =>
    groupedSponsorsByLevel(state.search.subrequests.sponsors?.items),
  );

  const content = useSelector((state) => state.workflow.transition);

  React.useEffect(() => {
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

  return !isEmpty(sponsors) ? (
    <Segment basic textAlign="center" className="sponsors" inverted>
      <div className="sponsorheader">
        <h3 className="subheadline">SPONSORS</h3>
      </div>
      <List>
        {keys(sponsors).map((level) => {
          return (
            <List.Item key={level} className={'sponsorlevel ' + level}>
              <h3>{level.toUpperCase()}</h3>
              <List horizontal>
                {sponsors[level].map((item) => (
                  <List.Item key={item['@id']} className="sponsor">
                    {item.logo ? (
                      <Image
                        className="logo"
                        src={flattenToAppURL(item.logo.scales.preview.download)}
                        size="small"
                        alt={item.title}
                        title={item.title}
                      />
                    ) : (
                      <span>{item.title}</span>
                    )}
                  </List.Item>
                ))}
              </List>
            </List.Item>
          );
        })}
      </List>
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

The Semantic UI compontent _Image_ is used to display the logo. It cares about the markup of an html image node with all necessary attributes in place.

We also benefit from Semantic UI component _List_ to build our list of sponsors. The styling can be customized but these predefined components help simplifying the code and achieve an app wide harmonic style.

```{seealso}
Chapter {doc}`volto_semantic_ui`
```

See the new footer. A restart is not necessary as we didn't add a new file. The browser updates automagically by configuration.

```{figure} _static/volto_component_sponsors.png
:align: left
:alt: Sponsors component
```

(volto-component-exercise-label)=

## Exercise

Modify the component to display a sponsor logo as a link to the sponsors website. The address is set in sponsor field "url". See the documentation of [Semantic UI React](https://react.semantic-ui.com/elements/image/#types-link).

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 3-5

<Image
  className="logo"
  as="a"
  href={item.url}
  target="_blank"
  src={flattenToAppURL(item.logo.scales.preview.download)}
  size="small"
  alt={item.title}
  title={item.title}
/>
```

The Semantic Image component is now rendered with a wrapping anchor tag.

```{code-block} html

<a
  target="_blank"
  title="Gold Sponsor Violetta Systems"
  class="ui small image logo"
  href="https://www.nzz.ch">
    <img
      src="/sponsors/violetta-systems/@@images/d1db77a4-448d-4df3-af5a-bc944c182094.png"
      alt="Violetta Systems">
</a>
```
````

% volto-component-summary-label:

## Summary

You know how to fetch data from backend. With the data you are able to create a component displayed at any place in the website.
