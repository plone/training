---
myst:
  html_meta:
    'description': 'Learn How to customize the Header of the page'
    'property=og:description': 'Learn How to customize the Header of the page'
    'property=og:title': 'Header customization'
    'keywords': 'Plone, Volto, Training, Theme, Header'
---

(voltohandson-header-label)=

# Header

## Some dummy content

So that our Navigation shows more than just the homepage, you should add some dummy pages like on [plone.org](plone.org) to your site using the add page menu in the top left of the page. Add some pages like:

- Why Plone?
- Get Started
- Services Community
- Foundation
- News & Events

## Header styling

We will start introducing the basic styling for the header. Inside the theme folder created in the last lesson create another folder `extras` and a file `custom.overrides` so you have `theme/extras/custom.overrides` in our addon. Use this file to apply general styling to our site theme.

```{note}
Use this rule of thumb when building Volto themes: use the default Semantic overrides system when the override is site-wide and applies to Semantic components.
When using your own components and specific theme styling, use instead `custom.overrides`.
Applying styling later using this method is much faster than doing it in the Semantic default components. Dont feel confused by the fact, that the header still does look a bit "weird" in comparison to the `plone.org` one
```

This:

```less
.ui.basic.segment.header-wrapper {
  position: relative;
  border-bottom: 1px solid @lightGrey;

  &.ui.segment {
    padding-top: 0em;
    padding-bottom: 0em;
  }

  &.padding-bottom {
    padding-bottom: 100px;
  }

  .header {
    flex-wrap: nowrap;
    align-items: center;
    justify-content: space-between;

    .logo-nav-wrapper {
      flex-grow: unset;
    }
  }

  .ui.secondary.pointing.menu .item {
    font-family: 'Poppins';
    text-transform: none;
    color: @black;

    &:first-child {
      display: none;
    }
  }
}
```


## Logo

We use [component shadowing](header-component-shadowing-label) to customize (and override) Volto original components.
Get the Plone logo (`Logo.svg`) from the resources from the [github repo](https://github.com/plone/training/tree/main/docs/voltohandson/ressources).

```{hint}
Remember: every time you add a file to the customizations folder or to the theme folder, you must restart Volto for changes to take effect.
From that point on, the hot reloading should kick in and reload the page automatically.
```


(voltohandson-header-component-label)=

## Header component

We will customize the existing Volto header only a bit, since the one we want does not differ much from the original.
We will do so by copying the original Volto `Header` component from the `omelette` folder `omelette/src/components/theme/Header/Header.jsx` folder into `src/customizations/components/theme/Header/Header.jsx`.

```{note}
If you have not worked with React that much so far you will notice that the Navigation component in Volto is not a javascipt function. This is because in React components can also be created from a js [class](https://legacy.reactjs.org/docs/react-component.html). Actually this was the preffered way to create components in earlier versions of React. Volto is currently undergoing the progress to switch to function components where possible. But as Volto has already a rather extensive codebase this is still an ongoing process.
<!-- Remove this when the Header.jsx component has been updated to a functional component. -->
```

We have to make some more changes to that component, such as replacing the search widget with a simple button, removing the `Anontools` component, adding the "try now" link and centering the navigation.
Your outcome could look something like this:

```jsx
import { Container, Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';

import { Logo, Navigation, Icon } from '@plone/volto/components';
import zoomSVG from '@plone/volto/icons/zoom.svg';

const Header = ({ pathname }) => {
  return (
    <Segment basic className="header-wrapper" role="banner">
      <Container>
        <div className="header">
          <div className="logo-nav-wrapper">
            <div className="logo">
              <Logo />
            </div>
          </div>
          <div className="nav-wrapper">
            <Navigation pathname={pathname} />
          </div>
          <div className="tools-search-wrapper">
            <a className="try-now-link" href="demo.plone.org">
              Try now
            </a>
            <div className="search">
              <button className="search-button" aria-label="search">
                <Icon name={zoomSVG} size="18px" />
              </button>{' '}
            </div>
          </div>
        </div>
      </Container>
    </Segment>
  );
};

export default Header;

Header.propTypes = {
  token: PropTypes.string,
  pathname: PropTypes.string.isRequired,
  content: PropTypes.objectOf(PropTypes.any),
};

Header.defaultProps = {
  token: null,
  content: null,
};

```


(header-component-shadowing-label)=

## Component shadowing

We use a technique called **component shadowing** to override an existing Volto component with our local custom version, without having to modify Volto's source code at all.
You have to place the replacing component in the same original folder path inside your addons the `src/customizations` folder. Take the `src` directory in Volto as the root when recreating the path in `src/addon/<your-addon-name>/customizations`.

```{note}
Component shadowing is very much like the good old Plone technique called "JBOT" ("just a bunch of templates"), but you can customize virtually any module in Volto, including actions and reducers, not only components.
```
