---
myst:
  html_meta:
    "description": "Storybook"
    "property=og:description": "Storybook"
    "property=og:title": "Storybook"
    "keywords": "Volto, Plone, Storybook, CI, Documentation"
---

# Storybook

Volto provides integration with [Storybook][1], which is used to document and
demonstrate various UI component. You can check the current deployed version of
the Storybook at the [Plone 6 (dev) documentation website][2]

[1]: https://storybook.js.org/
[2]: https://6.docs.plone.org/storybook/


To run Volto's Storybook, with a clone of Volto you can run:

```
yarn storybook
```

Volto project generated using the scaffold also provide integration of
Storybook with Volto addons, so the stories contained in addons are discovered and included in the generated Storybook build.

A Volto storybook story would look like this:

```jsx
import { injectIntl } from 'react-intl';
import React from 'react';
import { BreadcrumbsComponent } from './Breadcrumbs';
import Wrapper from '@plone/volto/storybook';

export const Breadcrumb = injectIntl(({ children, ...args }) => {
  return (
    <Wrapper location={{ pathname: '/folder2/folder21/doc212' }}>
      <div className="ui segment form attached" style={{ width: '400px' }}>
        <BreadcrumbsComponent
          pathname=""
          items={[
            {
              '@id': 'https://volto.kitconcept.com/api/Members',
              title: 'Users',
            },
          ]}
          getBreadcrumbs={() => {}}
          {...args}
        />
      </div>
    </Wrapper>
  );
});
```

Notice the `<Wrapper>` component, which provides a minimal Volto "environment context" that to ensure that the deeply-integrated Volto components can function.

To create a static build of your storybook (which you can publish to a static
http server, for example github.io pages), you need to run:

```
yarn build-storybook
```
