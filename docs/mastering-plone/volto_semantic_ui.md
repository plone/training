---
myst:
  html_meta:
    "description": "Base for Pastanaga theme and development helper"
    "property=og:description": "Base for Pastanaga theme and development helper"
    "property=og:title": "Semantic UI and Plone"
    "keywords": "theming"
---

(volto-semantic-ui-label)=

# Semantic UI

````{sidebar} Plone Frontend Chapter
```{figure} _static/plone-training-logo-for-frontend.svg
:alt: Plone frontend
:class: logo
```

Learn about templates in the classic frontend in chapter {doc}`zpt`
````

`Semantic UI` is a development framework that helps create beautiful, responsive layouts using human-friendly HTML.
It provides a declarative API, shorthand props and many helpers that simplifies development.

Its React complement [Semantic UI React](https://react.semantic-ui.com/) provides `React components` while Semantic UI provides `themes` as CSS style sheets with less variables and rules.

Volto is per default, not mandatory, build on both: the Semantic UI theming and the Semantic UI React Components.

Volto applies `components` from `Semantic UI React` to compose a large part of the views.
For example the component [Label](https://react.semantic-ui.com/elements/label/) is used to render votes on talks during this training.

```jsx
import React from 'react'
import { Icon, Label } from 'semantic-ui-react'

const LabelExampleBasic = () => (
  <Label>
    <Icon name='mail' /> 23
  </Label>
)

export default LabelExampleBasic
```

Another example is the [container](https://react.semantic-ui.com/elements/container/) component, that wraps content to be rendered with a margin depending on the browser window size / media query.
You have seen this component already in the news item view.

See next chapter {doc}`volto_theming` for theming with Semantic UI.
