(volto-semantic-ui-label)=

# Semantic UI

````{sidebar} Plone Frontend Chapter
```{figure} _static/plone-training-logo-for-frontend.svg
:alt: Plone frontend 
:align: left
:class: logo
```

Learn about templates in the classic frontend in chapter {doc}`zpt`
````

`Semantic UI` is a development framework that helps create beautiful, responsive layouts using human-friendly HTML. It provides a declarative API, shorthand props and many helpers that simplifies development.

Its React complement [Semantic UI React](https://react.semantic-ui.com/) provides `React components` while Semantic UI provides `themes` as CSS stylesheets with less variables and rules.

Volto is per default, not mandatory, build on both: the Semantic UI theming and the Semantic UI React Components.

Volto applies `components` from `Semantic UI React` to compose a large part of the views. For example the component [List](https://react.semantic-ui.com/elements/list/) is used to render lists.

```jsx
<List items={content.subjects} />
```

The above Semantic `List` component renders the list of subjects of the context content object. One example is the EventView.

Another example is the [container](https://react.semantic-ui.com/elements/container/) component, that wraps content to be rendered with a margin depending on the browser window size / media query.
You have seen this component already in the news item view.

See next chapter for theming with Semantic UI.
