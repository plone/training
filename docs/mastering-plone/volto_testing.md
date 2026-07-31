---
myst:
  html_meta:
    "description": "testing basics"
    "property=og:description": "testing basics"
    "property=og:title": "Testing"
    "keywords": "testing, Volto"
---

(volto-testing-label)=

# Testing

It's good practice to write tests for the requirements of a project.
The requirements become clearer.
A path towards implementation is emerging.

This chapter is a starting point for testing in Volto.

````{card}

For information on testing **backend** code, see the separate training: {ref}`testing-plone-label`
````

````{card}

Check out `mastering-plone-project` at tag `search`:

```shell
git checkout search
```

The code at the end of the chapter:

```shell
git checkout testing
```

More info in {doc}`code`
````


(testing-vitest)=

## Test the rendering of a component

With `vitest` you can create snapshots of components.

If the snapshot changes after a change in the code, you can check if the snapshot change was intentionally caused, and if not, rethink your changes.

- Create a {file}`TalkView.test.js` file as a sibling of {file}`frontend/packages/volto-ploneconf-site/src/components/Views/TalkView.jsx`
- You are testing the component `TalkView`.
  The test renders the component with some props:

```{code-block} jsx
:emphasize-lines: 17-28
:linenos:

import { render } from '@testing-library/react';
import { Provider } from 'react-intl-redux';
import configureStore from 'redux-mock-store';
import TalkView from './TalkView';
const mockStore = configureStore();

const store = mockStore({
  intl: {
    locale: 'en',
    messages: {},
  },
});

test('renders a talk view component with only required props', () => {
  const { container } = render(
    <Provider store={store}>
      <TalkView
        content={{
          title: 'Security of Plone',
          description: 'What makes Plone secure?',
          type_of_talk: { title: 'Talk', token: 'talk' },
          details: {
            'content-type': 'text/html',
            data: '<p>some details about this <strong>talk</strong>.</p>',
            encoding: 'utf8',
          },
        }}
      />
    </Provider>,
  );
  expect(container).toMatchSnapshot();
});
```

Create a snapshot by running the tests:

```shell
make frontend-test
```

See the snapshot in folder `__snapshots__`.
If this is a rendering you expect, you are good to go.
For example you see that the heading is the talk title with preceding type of talk.

{file}`packages/volto-ploneconf/src/components/Views/__snapshots__/Talk.test.js.snap`

```js
// Vitest Snapshot v1, https://vitest.dev/guide/snapshot.html

exports[`renders a talk view component with only required props 1`] = `
<div>
  <div
    class="ui container"
    id="view-wrapper talk-view"
  >
    <h1
      class="documentFirstHeading"
    >
      <span
        class="type_of_talk"
      >
        talk
        : 
      </span>
      Security of Plone
    </h1>
    <p
      class="documentDescription"
    >
      What makes Plone secure?
    </p>
    <div
      class="ui right floated segment"
    />
    <div>
      <p>
        some details about this 
        <strong>
          talk
        </strong>
        .
      </p>
    </div>
    <div
      class="ui clearing segment"
    >
      <p />
      <img
        class="ui small right floated image"
        item="[object Object]"
      />
    </div>
  </div>
</div>
`;
```

```{seealso}
{doc}`plone6docs:volto/contributing/testing`
```

(testing-cypress)=

## Run an end-to-end acceptance test

With **Cypress** you can run browser-based acceptance tests.

The following simple test checks if an editor can add an instance of the custom content type `talk`.

The test mimics the editor visiting her site and adding a talk via the appropriate menu action.

Create a test file {file}`frontend/cypress/tests/content.cy.js`

```{code-block} js
:emphasize-lines: 4, 18, 23, 40
:linenos:

describe('content type tests', () => {
  beforeEach(() => {
    cy.intercept('GET', `/**/*?expand*`).as('content');
    cy.createUser({
      username: 'editor',
      fullname: 'Editor',
      roles: ['Member', 'Reader', 'Contributor'],
    });
    cy.visit('/');
    cy.wait('@content');
  });

  afterEach(() => {
    cy.removeUser('editor', 'password');
  });

  it('As editor I can add a talk.', function () {
    cy.autologin('editor', 'password');

    cy.visit('/');
    cy.wait('@content');

    // when I add a talk with title, type and details
    cy.get('#toolbar-add').click();
    cy.get('#toolbar-add-talk').click();
    // title
    cy.get('input[name="title"]')
      .type('Security in Plone')
      .should('have.value', 'Security in Plone');
    // type of talk
    cy.get(
      '#field-type_of_talk > .react-select__control > .react-select__value-container',
    )
      .click()
      .type('talk{enter}');
    // details
    cy.get('.field-wrapper-details .slate-editor').type('This is the text.');
    cy.get('#toolbar-save').click();

    // Then a new talk should have been created
    cy.url().should('eq', Cypress.config().baseUrl + '/security-in-plone');
    // Then the title should read 'Talk: Security in Plone' with the type of talk mentioned
    cy.get('body').contains('Talk: Security in Plone');
  });
});
```

To run the acceptance tests, it's recommended to start three individual terminal sessions, one each for running the backend, the frontend, and the tests themselves.

1.  In the first session, start the backend server.

    ```shell
    make acceptance-backend-start
    ```

1.  In the second session, start the frontend server.

    ```shell
    make acceptance-frontend-dev-start
    ```

1.  In the third session, start the Cypress test runner.

    ```shell
    make acceptance-test
    ```

1.  In the Cypress window, choose `E2E Testing`, since Volto's tests are end-to-end tests.

1.  In the next section, select the browser you want Cypress to run in.
    Although the core tests use Electron by default, you can choose your preferred browser for the tests development.

1.  In the main Cypress runner section, you will see all test specs.

1.  To run a test, click on the test spec you want to run.

```{seealso}
Helper functions for an auto login, creating content, etc. from [Volto](https://github.com/plone/volto/tree/main/packages/volto/cypress/support).
```
