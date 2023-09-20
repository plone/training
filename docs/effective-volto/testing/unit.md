---
myst:
  html_meta:
    "description": "Unit testing"
    "property=og:description": "Unit testing"
    "property=og:title": "Unit testing"
    "keywords": "Volto, Plone, CI, Jest, Testing"
---

# Unit testing

Unit testing in Volto is achieved using [Jest](https://jestjs.io/) as the test runner. Unit testing is best used to test components or utilities in isolation.

Here's an example of a unit test in Volto.


```{note}
Notice the use of snapshots to facilitate making broad assertions of how a component would render.
This type of testing is only useful as a "sanity check", as it can be tedious to model the complex behavior of components using the [@testing-library/react][1] package. But the "utility" and "service" type of code can be fully tests, in rich environment similar to Python's testing libraries.
```

[1]: https://testing-library.com/docs/react-testing-library/intro/

```jsx
import React from 'react';
import configureStore from 'redux-mock-store';
import { Provider } from 'react-intl-redux';
import { MemoryRouter } from 'react-router-dom';
import { waitFor, render, screen } from '@testing-library/react';

import Diff from './Diff';

const mockStore = configureStore();

jest.mock('react-portal', () => ({
  Portal: jest.fn(() => <div id="Portal" />),
}));

jest.mock('@plone/volto/helpers/Loadable/Loadable');
beforeAll(
  async () =>
    await require('@plone/volto/helpers/Loadable/Loadable').__setLoadables(),
);

describe('Diff', () => {
  it('renders a diff component', async () => {
    const store = mockStore({
      history: {
        entries: [
          {
            time: '2017-04-19T14:09:36+02:00',
            version: 1,
            actor: { fullname: 'Web Admin' },
          },
          {
            time: '2017-04-19T14:09:35+02:00',
            version: 0,
            actor: { fullname: 'Web Admin' },
          },
        ],
      },
      content: {
        data: {
          title: 'Blog',
          '@type': 'Folder',
        },
      },
      schema: {
        schema: {
          fieldsets: [
            {
              fields: ['title'],
            },
          ],
          properties: {
            title: {
              title: 'Title',
              type: 'string',
            },
          },
        },
      },
      diff: {
        data: [
          {
            title: 'My old title',
          },
          {
            title: 'My new title,',
          },
        ],
      },
      intl: {
        locale: 'en',
        messages: {},
      },
    });
    const { container } = render(
      <Provider store={store}>
        <MemoryRouter initialEntries={['/blog?one=0&two=1']}>
          <Diff />
        </MemoryRouter>
      </Provider>,
    );
    await waitFor(() => screen.getByTestId('DiffField'));
    expect(container).toMatchSnapshot();
  });
});
```

This example was chosen specifically because it shows two potential tricky situations in unit testing:

- lazy-loaded libraries, and
- stateful components, that change their rendered content during their lifecycle.

So, when dealing with lazy-loaded libraries, we have to mock the lazy-loading process and fully load them before we can do the test:

```js
jest.mock('@plone/volto/helpers/Loadable/Loadable');
beforeAll(
  async () =>
    await require('@plone/volto/helpers/Loadable/Loadable').__setLoadables(),
);
```

And to solve the second part, we use `await` the component to finish updating before we test its rendered output:

```js
    await waitFor(() => screen.getByTestId('DiffField'));
    expect(container).toMatchSnapshot();
```
