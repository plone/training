---
myst:
  html_meta:
    "description": "Learn how to create the highlight Block"
    "property=og:description": "Learn how to create the highlight Block"
    "property=og:title": "Mainslider Block"
    "keywords": "Plone, Volto, Training, Blocks, Slider"
---

(voltohandson-highlightsblock-label)=

# Blocks - Highlights

## Basics

Exercise: Create the highlights basic block using `src/components/Blocks/Highlights/View.jsx` and `src/components/Blocks/Highlights/Edit.jsx` and configure it.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

`src/components/Blocks/Highlights/View.jsx`

```jsx
import React from 'react';

const View = props => {
  return <div>I am the highlights view component!</div>;
};

export default View;
```


`src/components/Blocks/Highlights/Edit.jsx`

```jsx
import React from 'react';

const Edit = props => {
  return <div>I am the highlights edit component!</div>;
};

export default Edit;
```
`src/components/index.js`

```js
//...
export HighlightsEditBlock from './Blocks/Highlights/Edit';
export HighlightsViewBlock from './Blocks/Highlights/View';
```

`src/config.js`

```js

// ...
    config.blocks.blocksConfig.highlights = {
      id: 'highlights',
      title: 'Highlights',
      icon: sliderSVG,
      group: 'common',
      view: HighlightsViewBlock,
      edit: HighlightsEditBlock,
      restricted: false,
      mostUsed: true,
      security: {
        addPermission: [],
        view: [],
      },
    },
```
````

## Structure and styling

After setting the basics, let's add some structure and styling to the view component:

```jsx
import React from "react";
import { Grid } from "semantic-ui-react";
import highlightPlonePNG from "./highlights-plone.png";
import highlightNewsPNG from "./highlights-news.png";

const View = (props) => {
  return (
    <div className="block highlights">
      <Grid columns="3">
        <Grid.Column>
          <div className="highlight">
            <div className="highlight-header">
              <img src={highlightPlonePNG} alt="" />
              <h2>Why Use Plone</h2>
            </div>
            <div className="highlight-body">Body here</div>
          </div>
        </Grid.Column>
        <Grid.Column>
          <div className="highlight">
            <div className="highlight-header">
              <img src={highlightNewsPNG} alt="" />
              <h2>Recent Plone launches</h2>
            </div>
            <div className="highlight-body">Body here</div>
          </div>
        </Grid.Column>
        <Grid.Column>
          <div className="highlight">
            <div className="highlight-header">
              <img src={highlightPlonePNG} alt="" />
              <h2>Why Use Plone</h2>
            </div>
            <div className="highlight-body">Body here</div>
          </div>
        </Grid.Column>
      </Grid>
    </div>
  );
};

export default View;
```

```less
.highlight {
  .highlight-header {
    display: flex;
    flex-direction: column;
    align-items: center;

    h2 {
      text-align: center;
      text-transform: uppercase;
    }
  }
}
```

Copy the required resources `highlights-plone.png` and `highlights-news.png` from the `training-resources` folder to `src/components/Blocks/Highlights` directory.

## Recent launches behavior

We will provide behavior to this column, by querying Plone about the recents `Success Story`.
We will use the `plone.restapi` `@search` endpoint for that.
This is a static behavior, so we can implement it in the view component.
We don't want to bloat the view component, so we will create a specific component for it called `RecentSuccessStories.jsx` in the block directory:

```jsx
import React from "react";

const RecentSuccessStories = (props) => {
  return <div>The list of success stories</div>;
};

export default RecentSuccessStories;
```

and we will add it to the Block render. Notice that we are passing the id prop from the parent component:

```{code-block} jsx
:emphasize-lines: 1,6,19

import RecentSuccessStories from './RecentSuccessStories';

// ...

 const View = props => {
   const { id } = props;

   return (

 // ...

 <Grid.Column>
   <div className="highlight">
     <div className="highlight-header">
       <img src={highlightNewsPNG} alt="" />
       <h2>Recent Plone launches</h2>
     </div>
     <div className="highlight-body">
       <RecentSuccessStories id={id} />
     </div>
   </div>
 </Grid.Column>

 // ...
```

and then, the `RecentSuccessStories.jsx` component:

```jsx
import React from "react";
import { searchContent } from "@plone/volto/actions";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";

const RecentSuccessStories = (props) => {
  const { id } = props;
  const searchSubrequests = useSelector((state) => state.search.subrequests);
  const dispatch = useDispatch();
  const results = searchSubrequests?.[id]?.items;

  React.useEffect(() => {
    dispatch(
      searchContent(
        "/",
        {
          sort_on: "created",
          metadata_fields: "_all",
          portal_type: ["success_story"],
        },
        id
      )
    );
  }, [dispatch, id]);

  return (
    <ul>
      {results &&
        results.map((story) => (
          <li key={story["@id"]}>
            <Link to={story["@id"]}>{story.title}</Link>
          </li>
        ))}
    </ul>
  );
};

export default RecentSuccessStories;
```

We make use of the `useSelector` and `useDispatch` hooks from the `react-redux` library.
They are used to subscribe our component to the store changes (`useSelector`) and for issuing Redux actions (`useDispatch`) from our components.
Maybe you are used to use the `connect` react-redux HOC, this is still a valid way of wiring our components to the store, but hooks simplify the code.

This is the complete view component (`View.jsx`) for this block:

```jsx
import React from "react";
import { Grid } from "semantic-ui-react";
import { Link } from "react-router-dom";
import RecentSuccessStories from "./RecentSuccessStories";
import highlightPlonePNG from "./highlights-plone.png";
import highlightNewsPNG from "./highlights-news.png";
import highlightLogosJPG from "./highlights-logos.jpg";
import highlightPCJPG from "./highlights-small-ploneconf.png";

const View = (props) => {
  const { id } = props;

  return (
    <div className="block highlights">
      <Grid columns="3">
        <Grid.Column>
          <div className="highlight">
            <div className="highlight-header">
              <img src={highlightPlonePNG} alt="" />
              <h2>Why Use Plone</h2>
            </div>
            <div className="highlight-body">
              <p>
                Plone has an{" "}
                <a
                  className="external-link"
                  href="https://plone.org/"
                  target="_blank"
                  rel="noopener noreferrer"
                  title=""
                >
                  active, thriving community
                </a>{" "}
                that holds{" "}
                <a
                  className="external-link"
                  href="https://plone.org/events"
                  target="_blank"
                  rel="noopener noreferrer"
                  title=""
                >
                  annual conferences, regional symposia, and many sprints
                </a>{" "}
                all over the world.
              </p>
              <p>
                <em>
                  <span className="title">
                    <strong>
                      See{" "}
                      <a
                        className="external-link"
                        href="https://plone.org/news/2017/plones-outstanding-security-track-record"
                        target="_blank"
                        rel="noopener noreferrer"
                        title=""
                      >
                        our statement about Plone's outstanding security track
                        record
                      </a>
                    </strong>{" "}
                    and a recent security hoax.
                  </span>
                </em>
              </p>
              <p>
                <a
                  className="external-link"
                  href="https://2019.ploneconf.org/"
                  target="_blank"
                  rel="noopener noreferrer"
                  title=""
                >
                  Plone Conference 2019 will be in Ferrara, Italy
                </a>
                <span>!&nbsp;</span>
              </p>
              <dl className="image-inline captioned">
                <a
                  className="external-link"
                  href="https://2019.ploneconf.org/"
                  target="_blank"
                  rel="noopener noreferrer"
                  title=""
                >
                  <dt>
                    <img
                      src={highlightPCJPG}
                      alt="Plone Conference 2019"
                      title="Plone Conference 2019"
                      height="100"
                      width="200"
                    />
                  </dt>
                  <dd className="image-caption">Plone Conference 2019</dd>
                </a>
              </dl>
              <Link to="/about">Learn more about Plone...</Link>
            </div>
          </div>
        </Grid.Column>
        <Grid.Column>
          <div className="highlight">
            <div className="highlight-header">
              <img src={highlightNewsPNG} alt="" />
              <h2>Recent Plone launches</h2>
            </div>
            <div className="highlight-body">
              <RecentSuccessStories id={id} />
            </div>
          </div>
        </Grid.Column>
        <Grid.Column>
          <div className="highlight">
            <div className="highlight-header">
              <img src={highlightPlonePNG} alt="" />
              <h2>Why Use Plone</h2>
            </div>
            <div className="highlight-body">
              <img src={highlightLogosJPG} alt="" />
            </div>
          </div>
        </Grid.Column>
      </Grid>
    </div>
  );
};

export default View;
```

Copy the additional required resources `highlights-logos` and `highlights-small-ploneconf` from the `training-resources` folder to `src/components/Blocks/Highlights` directory.
