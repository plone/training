---
myst:
  html_meta:
    "description": "testing basics"
    "property=og:description": "testing basics"
    "property=og:title": "Testing Volto add-on"
    "keywords": "testing, Volto"
---

(volto-testing-label)=

# Testing

````{card} Frontend chapter

For information on testing **backend** code, see the separate training: {ref}`testing-plone-label`
````

It's a good practice to write tests for the main requirements of a project. The **requirements are getting clearer and a path for the development is pointed**.

This chapter is meant as a starting point for testing in Volto.

(testing-cypress)=

## Testing permissions, features and UI topics

We already added a content type `talk`. Let's write a test 'An editor can add a talk'.

1. Install docker.

2. Have a look at some helper functions for an autologin, etc. from [Volto](https://github.com/plone/volto/tree/main/packages/volto/cypress/support).

3. Create a test file {file}`cypress/tests/content.cy.js`

{file}`content.cy.js`:

```{code-block} js
:emphasize-lines: 4,9-10, 27-28

describe('Add talk tests', () => {
  beforeEach(() => {
    // given a logged in editor and the site root
    cy.autologin();
  });
  it('As editor I can add a talk.', function () {
    cy.visit('/');
    // when I add a talk with title, type and details
    cy.get('#toolbar-add').click();
    cy.get('#toolbar-add-talk').click();
    cy.get('input[name="title"]')
      .type('Security in Plone')
      .should('have.value', 'Security in Plone');
    cy.get(
      '#default-type_of_talk .react-select-container > .react-select__control .icon',
    )
      .click()
      .type('Talk{enter}');
    cy.get('#default-details .public-DraftEditor-content')
      .type('This is the text.')
      .get('span[data-text]')
      .contains('This is the text.');
    cy.get('#toolbar-save').click();

    // then a new talk should have been created
    cy.url().should('eq', Cypress.config().baseUrl + '/security-in-plone');
    cy.get('body').contains('Security in Plone');
    cy.get('body').contains('This is the text.');
  });
});
```

Go to your **frontend folder**, start the test backend and the test frontend.
Then run the acceptance tests:

It's recommended to start three individual terminal sessions, one each for running the Plone backend, the Volto frontend, and the acceptance tests.
All sessions should start from the `frontend` directory.

1.  In the first session, start the backend server.

    ```shell
    make acceptance-backend-start
    ```

1.  In the second session, start the frontend server.

    ```shell
    make acceptance-frontend-dev-start
    ```

1.  In the third session, start the Cypress tests runner.

    ```shell
    make acceptance-test
    ```

1.  In the Cypress pop-up test style, choose `E2E Testing`, since Volto's tests are end-to-end tests.

1.  In the next section, select the browser you want Cypress to run in.
    Although the core tests use `headless Electron` by default, you can choose your preferred browser for the tests development.

2.  In the main Cypress runner section, you will see all of the test specs.

3.  To run a test, interact with the file based tree that displays all possible tests to run, and click on the test spec you need to run.


(testing-jest)=

## Testing the rendering of a component

- Create a {file}`Talk.test.js` file as a sibling of Talk.jsx
- The component to test is `Talk`.
  We let the test render this component with some props:

```{code-block} jsx
:emphasize-lines: 17-23
:linenos:

import renderer from 'react-test-renderer';
import { Provider } from 'react-intl-redux';
import configureStore from 'redux-mock-store';
import Talk from './Talk';
const mockStore = configureStore();

const store = mockStore({
  intl: {
    locale: 'en',
    messages: {},
  },
});

test('renders a talk view component with only required props', () => {
  const component = renderer.create(
    <Provider store={store}>
      <Talk
        content={{
          title: 'Security of Plone',
          description: 'What makes Plone secure?',
          type_of_talk: { title: 'Talk', token: 'Talk' },
        }}
      />
    </Provider>,
  );
  const json = component.toJSON();
  expect(json).toMatchSnapshot();
});
```

If you now run the test, a snaphot of the rendered component will be created.

```shell
make test
```

See the snaphot in folder `__snapshots__`.
If this is a rendering you expected, you are good to go.

```html
// Jest Snapshot v1, https://goo.gl/fbAQLP

exports[`renders a talk view component with only required props 1`] = `
<div
  className="ui container"
  id="view-wrapper talk-view"
>
  <h1
    className="documentFirstHeading"
  >
    <span
      className="type_of_talk"
    >
      Talk
      : 
    </span>
    Security of Plone
  </h1>
  <p
    className="documentDescription"
  >
    What makes Plone secure?
  </p>
  <div
    className="ui right floated segment"
  />
  <div
    dangerouslySetInnerHTML={
      Object {
        "__html": "<p>some details about this <strong>talk</strong>.</p>",
      }
    }
  />
  <div
    className="ui clearing segment"
  >
    <p />
    <img
      className="ui small avatar right floated image"
    />
  </div>
</div>
`;
```
