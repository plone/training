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

It's good practice to write tests for the requirements of a project.
The requirements become clearer.
A path towards implementation is emerging.

This chapter is a starting point for testing in Volto.

````{card} Frontend chapter

For information on testing **backend** code, see the separate training: {ref}`testing-plone-label`
````

````{card}

Checkout `volto-ploneconf` at tag "vocabularies":

```shell
git checkout vocabularies
```

The code at the end of the chapter:

```shell
git checkout testing
```

More info in {doc}`code`
````


(testing-jest)=

## Testing the rendering of a component

With `jest` you can create snapshots of components.

Does this snapshot change after a change in the code, you can check if this snapshot change is intentionally caused, and if not, rethink your changes.

- Create a {file}`Talk.test.js` file as a sibling of {file}`Talk.jsx`
- You are testing the component `Talk`.
  The test is rendering the component with some props:

```{code-block} jsx
:emphasize-lines: 17-28
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
  const json = component.toJSON();
  expect(json).toMatchSnapshot();
});
```

Create a snapshot by running the tests:

```shell
make test
```

See the snapshot in folder `__snapshots__`.
If this is a rendering you expect, you are good to go.
For example you see that the heading is the talk title with preceding type of talk.

{file}`packages/volto-ploneconf/src/components/Views/__snapshots__/Talk.test.js.snap`

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
    <div
      className="ui dividing header"
    >
      Speaker
    </div>
  </div>
</div>
`;
```

```{seealso}
{doc}`plone6docs:volto/contributing/testing` in docs.plone.org.
```

(testing-cypress)=

## Testing permissions, features and user interface topics

With `Cypress` you can run browser-based acceptance tests.

The following simple test checks if an editor can add an instance of the custom content type `talk`.

The test mimics the editor visiting her site and adding a talk via the appropriate menu action.

Create a test file {file}`cypress/tests/content.cy.js`

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

With a frontend package NOT relying on a backend package, you could proceed with next step {ref}`testing-cypress-run`.

### Preparing acceptance backend with add-ons

For a test like above, with talks, the acceptance backend needs the backend package with content type talk to be installed.

Have a look at `/frontend/backend/`, where a backend with the add-on `ploneconf-site` is configured.
The configuration instructs to install the package from its repository and editable.
So you can proceed developing the backend package while working on the frontend package.
Necessary changes of the backend package while developing the couple of backend add-on and frontend add-on can be committed right out of `/frontend/backend/sources/ploneconf.site`.


(testing-cypress-run)=

### Run cypress tests

Go to your frontend folder, start the test backend and the test frontend.
Then run the acceptance tests:

It's recommended to start three individual terminal sessions, one each for running the Plone backend, the Volto frontend, and the acceptance tests.
All sessions should start from the `frontend` directory.

1.  In the first session, start the backend server.

    ```shell
    make backend-install
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

1.  In the main Cypress runner section, you will see all test specs.

1.  To run a test, interact with the file based tree that displays all possible tests to run, and click on the test spec you want to run.

Have a look in the code of `volto-ploneconf` to see that the continuous integration includes these cypress tests: `.github/workflows/acceptance.yml`.
Commits to pull requests trigger a run of the tests.

```{seealso}
Helper functions for an auto login, creating content, etc. from [Volto](https://github.com/plone/volto/tree/main/packages/volto/cypress/support).
```
