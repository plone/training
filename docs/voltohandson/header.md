---
html_meta:
  "description": "Learn How to customize the Header of the page"
  "property=og:description": "Learn How to customize the Header of the page"
  "property=og:title": "Header customization"
  "keywords": "Plone, Volto, Training, Theme, Header"
---

(voltohandson-header-label)=

# Header

## Header styling

We will start introducing the basic styling for the header.
We use the `theme/extras/custom.overrides` to apply general styling to our site theme.

```{note}
Use this rule of thumb when building Volto themes: use the default Semantic overrides system when the override is site-wide and applies to Semantic components.
When using your own components and specific theme styling, use instead `custom.overrides`.
Applying styling later using this method is much faster than doing it in the Semantic default components.
```

We want this styling in the Header component:

```less
.ui.basic.segment.header-wrapper {
  border-bottom: 1px solid #939393;
  margin-bottom: 20px;
  background-color: #191919;
}

.ui.basic.segment .header .logo-nav-wrapper {
  justify-content: space-between;
}

.logo .ui.image {
  height: 50px;
}
```

So we have the familiar black background of `plone.org`, the right logo height, and the proper flex distribution for the header elements.
Please notice the specificity of the CSS class declarations.
We need them in order to override the original theme.
This is rather common when overriding SemanticUI theme styles because of the high specificity enforced by SemanticUI.

We adjust the navigation menu to match the one on `plone.org`:

```less
.navigation .ui.secondary.pointing.menu {
  min-height: initial;
  margin: 0;

  a.item {
    padding: 5px 10px !important;
    border: none;
    margin: 0;
    color: #fff;
    font-size: 14px;
    font-weight: bold;

    &:not(:last-child) {
      margin-right: 5px;
    }

    &:hover {
      background: #212020;
      color: #00a1df;
    }
  }
}
```

Then we adjust the margin for the homepage:

```less
.siteroot .ui.basic.segment.header-wrapper {
  margin-bottom: 0;
}
```

## Logo

We use [component shadowing](#component-shadowing) to customize (and override) Volto original components.
Get the Plone logo (`Logo.svg`) from the `training-resources` you downloaded from the [google drive](https://drive.google.com/drive/folders/1xDleXE8Emhr9xn_pnZaGfO9_HmU31L9e?usp=sharing).

```{note}
Every time you add a file to the customizations folder or to the theme folder, you must restart Volto for changes to take effect.
From that point on, the hot reloading should kick in and reload the page automatically.
```

## Header component

We will customize the existing Volto header, since the one we want does not differ much from the original.
We will do so by copying the original Volto `Header` component from the `omelette` folder `omelette/src/components/theme/Header/Header.jsx` folder into `src/customizations/components/theme/Header/Header.jsx`.

```{note}
If you have not worked with React that much so far you will notice that the Navigation component in Volto is not a javascipt function. This is because in React components can also be created from a js [class](https://reactjs.org/docs/react-component.html). Actually this was the preffered way to create components in earlier versions of React. Volto is currently undergoing the progress to switch to function components where possible.
<!-- Remove this when the Header.jsx component has been updated to a functional component. -->
```

We have to make some more changes to that component, such as removing the search widget and the `Anontools` component.

This will be the outcome:

```js
import { Logo, Navigation } from '@plone/volto/components';

...

render() {
    return (
      <Segment basic className="header-wrapper" role="banner">
        <Container>
          <div className="header">
            <div className="logo-nav-wrapper">
              <div className="logo">
                <Logo />
              </div>
              <Navigation pathname={this.props.pathname} />
            </div>
          </div>
        </Container>
      </Segment>
    );
  }
```

## Component shadowing

We use a technique called **component shadowing** to override an existing Volto component with our local custom version, without having to modify Volto's source code at all.
You have to place the replacing component in the same original folder path inside the `src/customizations` folder. Take the `src` directory in Volto as the root when recreating the path in `/customizations`.

```{note}
Component shadowing is very much like the good old Plone technique called "JBOT" ("just a bunch of templates"), but you can customize virtually any module in Volto, including actions and reducers, not only components.
```
