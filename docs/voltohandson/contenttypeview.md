---
myst:
  html_meta:
    "description": "Learn How to code a custom View for a content type"
    "property=og:description": "Learn How to code a custom View for a content type"
    "property=og:title": "Content Type Views"
    "keywords": "Plone, Volto, Training, View, Content Types"
---

# Sprint content type

On our listing template are several buttons to add different content types. Among them is also one for adding Sprints. As this is not a content type that currently exists in our Plone instance we will use it as an example on how to create a new content type and a custom view for it.

## Create Sprint content type

Create this content type using the Dexterity content type control panel at <http://localhost:3000/controlpanel/dexterity-types>.
Name it `Sprint`, then select it, go to the `Behaviors` tab, and add the `Blocks` and the `event Basic` behaviors and save those.

## Create the new view component

For creating a new View we will now create a new Folder within `src/components/` called `Views`. In there create the file `SprintView.jsx` which will contain the markup for our view.

We will use the default `Document` view and add the Event Information on top. Beware that we are not modeling this View after the actual one from `plone.org`, but creating our own version on how the View for the Sprint type might look like.

This what the code for it might look like:

```jsx
import React from "react";
import { DefaultView } from "@plone/volto/components";
import { Container } from "semantic-ui-react";
import moment from "moment";

const SprintView = (props) => {
  const { content } = props;
  return (
    <Container>
      <p>
        From {moment(content.start).format("MMMM D, YYYY")} to{" "}
        {moment(content.end).format("MMMM D, YYYY")}
      </p>
      <DefaultView {...props} />
    </Container>
  );
};

export default SprintView;
```

The content key of the props will contain all the information about your content object.
Export this component as well via the `src/components/index.js` and import it to `config.js`.
To make the `sprint` type use this view you need to assign it in the `applyConfig` function:

```js
config.views.contentTypesViews.sprint = sprintView;
```

Now, when you add a new sprint it will display the dates at the top above the main content.
