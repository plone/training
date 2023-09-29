---
myst:
  html_meta:
    "description": "Icons used in Volto"
    "property=og:description": "Icons used in Volto"
    "property=og:title": "Icons"
    "keywords": "Volto, Plone, frontend, React, Icons, svg, pastanaga"
---

# Icons

Volto has a pre-defined set of SVG icons from the Pastanaga UI icon system. You can find them in the code repo in [here](https://github.com/plone/volto/tree/master/src/icons). They are also browseable in https://pastanaga.io/icons/.

The following example shows how to display one of these icons.

```js
import addUserSVG from '@plone/volto/icons/add-user.svg';
import { Icon } from '@plone/volto/components';

<Icon name={addUserSVG} size="24px" />;
```

```{note}
These icons are intended to be used only in the "official" Plone Pastanaga UI.
Please refrain from using them on personal projects unless they are based on Plone.
```

## Custom icons

If you have your own svg file that you wish to load with the `<Icon>`
component, you have to make sure you place it, in your addon or project code,
in a folder called `icons`. So, if you have a file in `src/icons/myicon.svg`,
you can use it like:

```
import { Icon } from '@plone/volto/components';
import myIconSVG from 'my-volto-addon/icons/myicon.svg';

<Icon name={myIconSVG} size="24px" />;

```

The `icons` folder is an absolute must, because otherwise it won't be loaded by
[Volto's svg webpack loader](https://github.com/plone/volto/blob/5eb332829956dbf0505283b176008c9364ccf2f9/webpack-plugins/webpack-svg-plugin.js#L10)
