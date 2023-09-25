---
myst:
  html_meta:
    "description": "How to extend volto blocks"
    "property=og:description": "How to extend volto blocks"
    "property=og:title": "Extend volto blocks"
    "keywords": "Volto, Training, Extend block"
---

### Extend volto blocks

There are various ways of extending Volto blocks from core behaviour. The component shadowing is the plain old way of customizing components in volto. But it comes with its own problems like keeping the shadowed component up to date with latest fixes and features.
In the modern day volto development we can directly extend blocks in form of variations and extensions and populate each of them with their own schemas.

Let us take an example for a teaser block which we already have in volto core. In our addon `volto-teaser-tutorial` we will step by step extend each component that we have in volto core.

The most simple customization is the View of the Teaser. The volto core teaser block confiugration looks like:

```jsx
  teaser: {
    id: 'teaser',
    title: 'Teaser',
    icon: imagesSVG,
    group: 'common',
    view: TeaserViewBlock,
    edit: TeaserEditBlock,
    restricted: false,
    mostUsed: true,
    sidebarTab: 1,
    blockSchema: TeaserSchema,
    dataAdapter: TeaserBlockDataAdapter,
    variations: [
      {
        id: 'default',
        isDefault: true,
        title: 'Default',
        template: TeaserBlockDefaultBody,
      },
    ],
  },
```

Plain and simple. Every block in Volto have Edit and View stock components. You can customize each of them individually by either shadowing or directly like:

```
config.blocks.blocksConfig.teaser.view = MyTeaserView

```

Let's replace our Main teaser view with our `MyTeaserView` component:

```jsx
const MyDataProvider = (props) => {
  const enhancedChildren = React.Children.map(props.children, (child) => {
    if (React.isValidElement(child)) {
      return React.cloneElement(child, {
        ...props,
        enhancedProp: "some-enhanced-prop",
      });
    }
    return child;
  });

  return enhancedChildren;
};

const TeaserView = (props) => {
  return (
    <MyDataProvider>
      <TeaserBody {...props} />
    </MyDataProvider>
  );
};

export default withBlockExtensions(TeaserView);
```

Here, the View component renders a TeaserBody which will be a result of an active variation, we will come to that in later chapters.

Notice we are wrapping our TeaserBody variation in a DataProvider which may inject some extra props along with its original ones.

```{note} 💡
The React.cloneElement() API creates a clone of an element and returns a new React element. The cool thing is that the resulting element will have all of the original element’s props, with the new props merged in.
```
