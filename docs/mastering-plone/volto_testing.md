---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(volto-testing-label)=

# Testing in Plone

````{sidebar} Plone Frontend Chapter
```{figure} _static/plone-training-logo-for-frontend.svg
:alt: Plone frontend
:class: logo
```

For information on testing Plone backend see the separate training: {ref}`testing-plone-label`
````

It's a good practice to write tests for the main requirements of a project. The **requirements are getting clearer and a path for the development is pointed**.

This chapter is meant as a starting point for testing in Volto.

(testing-cypress)=

## Testing permissions, features and UI topics

We already added a content type `talk`. Let's write a test 'An editor can add a talk'.

1. Install cypress with

   > ```
   > yarn add cypress cypress-axe cypress-file-upload --dev -W
   > ```

2. Add a yarn script in your {file}`package.json`

   > ```
   > "scripts": {
   >     ...
   >     "cypress:open": "CYPRESS_API=plone cypress open"
   >   },
   > ```

3. Get some helper functions for an autologin, etc. from [Volto](https://github.com/plone/volto/tree/master/cypress/support).

4. Create a folder {file}`cypress/integration/` with a file {file}`content.js`

{file}`content.js`:

```{code-block} js
:emphasize-lines: 4,12, 32-33

describe('Add talk tests', () => {
  beforeEach(() => {
    // given a logged in editor and the site root
    cy.autologin();
    cy.visit('/');
    cy.waitForResourceToLoad('@navigation');
    cy.waitForResourceToLoad('@breadcrumbs');
    cy.waitForResourceToLoad('@actions');
    cy.waitForResourceToLoad('@types');
    cy.waitForResourceToLoad('?fullobjects');
  });
  it('As editor I can add a talk.', function () {
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

Go to your **backend folder**, open `Makefile` and add test commands:

```text
# Volto cypress tests

.PHONY: start-test-backend
start-test-backend: ## Start Test Plone Backend
  ZSERVER_PORT=55001 CONFIGURE_PACKAGES=plone.app.contenttypes,plone.restapi,kitconcept.volto,kitconcept.volto.cors APPLY_PROFILES=plone.app.contenttypes:plone-content,plone.restapi:default,kitconcept.volto:default-homepage ./bin/robot-server plone.app.robotframework.testing.PLONE_ROBOT_TESTING

.PHONY: start-test-frontend
start-test-frontend: ## Start Test Volto Frontend
  cd ../volto-ploneconf; RAZZLE_API_PATH=http://localhost:55001/plone yarn build && NODE_ENV=production node build/server.js

.PHONY: start-test
start-test: ## Start Test
  cd ../volto-ploneconf; yarn cypress:open
```

Start the test backend

```shell
make start-test-backend
```

Start the test frontend

```shell
make start-test-frontend
```

Start cypress

```shell
make start-test
```

You can step through each command of a test.

```{figure} _static/cypress_running.png

```

Cypress provides a helper to find the right selector.

```{figure} _static/cypress_selector.png

```

(testing-jest)=

## Testing the rendering of a component

- Create a {file}`Talk.test.js` file as a sibling of Talk.jsx
- The component to test is `Talk`. We let the test render this component with some props:

```{code-block} jsx
:emphasize-lines: 18-24
:linenos:

import React from 'react';
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
yarn test
```

See the snaphot in folder `__snapshots__`.
If this is a rendering you expected, you are good to go.

```html
// Jest Snapshot v1, https://goo.gl/fbAQLP exports[`renders a talk view
component with only required props 1`] = `
<div className="ui container" id="page-talk">
  <h1 className="documentFirstHeading">Talk : Security of Plone</h1>
  <div className="ui right floated segment" />
  <p className="documentDescription">What makes Plone secure?</p>
</div>
`;
```
