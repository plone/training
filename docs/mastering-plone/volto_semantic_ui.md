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
For example the component [Menu (Tabular)](https://react.semantic-ui.com/collections/menu/#types-tabular) is used to render tabular menues.

```{figure} _static/semantic_tabular_menu.png
:alt: Tabular menu with Semantic UI

Tabular menu with Semantic UI
```


```jsx
import React, { useState } from 'react';
import { Menu } from 'semantic-ui-react';

const TabbedMenuExample = () => {
  const [activeItem, setActiveItem] = useState('bio');

  const handleItemClick = (e, { name }) => {
    setActiveItem(name);
  };

  return (
    <Menu tabular>
      <Menu.Item
        name="bio"
        active={activeItem === 'bio'}
        onClick={handleItemClick}
      />
      <Menu.Item
        name="photos"
        active={activeItem === 'photos'}
        onClick={handleItemClick}
      />
    </Menu>
  );
};

export default TabbedMenuExample;
```

See next chapter {doc}`volto_theming` for theming with Semantic UI.
