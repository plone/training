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

## Header styling

We will start introducing the basic styling for the header.
We use the `theme/extras/custom.overrides` to apply general styling to our site theme.

```{note}
Use this rule of thumb when building Volto themes: use the default Semantic overrides system when the override is site-wide and applies to Semantic components.
When using your own components and specific theme styling, use instead `custom.overrides`.
Applying styling later using this method is much faster than doing it in the Semantic default components. Dont feel confused by the fact, that the header still does look a bit "weird" in comparison to the `plone.org` one
```

This :

```less
.ui.basic.segment.header-wrapper {
  background: #007eb6;
  color: @white;
  padding: 0 0 1em 0;
  .top-header {
    background-color: #1f1238;
    width: 100%;
    margin-bottom: 1em;
    .ui.container {
      display: flex;
      justify-content: flex-end;
      text-transform: uppercase;
      font-weight: bold;
      font-size: 11px;
      a {
        color: @white;
        margin-right: 10px;
      }
    }
  }
  .nav-wrapper {
    display: flex;
    align-items: baseline;
    text-transform: uppercase;

    .ui.secondary.pointing.menu .item,
    .ui.pointing.dropdown {
      color: @white;
      border: none;
      padding: 0.5em 0.8em;
      border-radius: 5px;
      margin-right: 5px;
      font-size: 14px;
      &:first-child {
        display: none;
      }

      &.active,
      &:hover {
        background-color: #1a0b31;
      }
    }

    .ui.button.search {
      background: transparent;
      padding: 0.5em 0.8em;
      border-radius: 5px;
      color: @white;
      font-weight: normal;
      text-transform: uppercase;

      &:hover {
        background-color: #1a0b31;
      }
      .icon {
        margin-bottom: -2px;
      }
    }
  }
}
```

Then we adjust the margin for the content area:

```less
.ui.basic.segment.content-area {
  padding-top: 0;
  margin-top: 0;
}
```


## Logo

We use [component shadowing](header-component-shadowing-label) to customize (and override) Volto original components.
Get the Plone logo (`Logo.svg`) from the `training-resources` you downloaded from the [google drive](https://drive.google.com/drive/folders/19nQkPiiwY5lhBNiTTZJaV-kpQ9rkYqiO?usp=sharing).

```{note}
Every time you add a file to the customizations folder or to the theme folder, you must restart Volto for changes to take effect.
From that point on, the hot reloading should kick in and reload the page automatically.
```


(voltohandson-header-component-label)=

## Header component

We will customize the existing Volto header, since the one we want does not differ much from the original.
We will do so by copying the original Volto `Header` component from the `omelette` folder `omelette/src/components/theme/Header/Header.jsx` folder into `src/customizations/components/theme/Header/Header.jsx`.

```{note}
If you have not worked with React that much so far you will notice that the Navigation component in Volto is not a javascipt function. This is because in React components can also be created from a js [class](https://legacy.reactjs.org/docs/react-component.html). Actually this was the preffered way to create components in earlier versions of React. Volto is currently undergoing the progress to switch to function components where possible. But as Volto has already a rather extensive codebase this is still an ongoing process.
<!-- Remove this when the Header.jsx component has been updated to a functional component. -->
```

We have to make some more changes to that component, such as removing the search widget and the `Anontools` component, adding the upper Header section and many more amendmends.

This will be the outcome:

```jsx
import { Container, Segment, Dropdown } from 'semantic-ui-react';
import {
  Anontools,
  Logo,
  Navigation,
  Icon,
  UniversalLink,
} from '@plone/volto/components';
import zoomSVG from '@plone/volto/icons/zoom.svg';
...

render() {
    return (
     <Segment basic className="header-wrapper" role="banner">
        <div className="top-header">
          <Container>
            <UniversalLink href="https://2022.ploneconf.org">
              Conference
            </UniversalLink>
            <UniversalLink href="https://docs.plone.org">
              Documentation
            </UniversalLink>
            <UniversalLink href="https://training.plone.org">
              Training
            </UniversalLink>
            <UniversalLink href="https://community.plone.org">
              Forum
            </UniversalLink>
            <UniversalLink href="https://discord.com/invite/zFY3EBbjaj">
              Chat
            </UniversalLink>
          </Container>
        </div>
        <Container>
          <div className="header">
            <div className="logo">
              <Logo />
            </div>
            <div className="nav-wrapper">
              <Navigation pathname={this.props.pathname} />
              <Dropdown text="More" pointing>
                <Dropdown.Menu>
                  <Dropdown.Item>
                    <UniversalLink href="/about-plone">
                      About Plone
                    </UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/conferences">
                      Conferences
                    </UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/donate">Donate</UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/download">Download</UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/features">Features</UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/events">Events</UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/news">News</UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/providers">Providers</UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/related">
                      Related websites
                    </UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/security">Security</UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/support">Support</UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/newsroom">Newsroom</UniversalLink>
                  </Dropdown.Item>
                  <Dropdown.Item>
                    <UniversalLink href="/products">Products</UniversalLink>
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
              <div className="tools-search-wrapper">
                <div className="tools-search">
                  <UniversalLink href="/search" className="ui button search">
                    <Icon name={zoomSVG} size="18px" color="white" />
                    Search
                  </UniversalLink>
                </div>
                {!this.props.token && (
                  <div className="tools">
                    <Anontools />
                  </div>
                )}
              </div>
            </div>
          </div>
        </Container>
      </Segment>
    );
  }
```


(header-component-shadowing-label)=

## Component shadowing

We use a technique called **component shadowing** to override an existing Volto component with our local custom version, without having to modify Volto's source code at all.
You have to place the replacing component in the same original folder path inside the `src/customizations` folder. Take the `src` directory in Volto as the root when recreating the path in `/customizations`.

```{note}
Component shadowing is very much like the good old Plone technique called "JBOT" ("just a bunch of templates"), but you can customize virtually any module in Volto, including actions and reducers, not only components.
```


## Page content

To have the header look as much as the `plone.org` page as possible you now can create the pages "get started", "community" and plone foundation to be featured in the navigation.
