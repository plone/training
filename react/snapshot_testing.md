(snapshot-testing-label)=

# Use Snapshot Testing

To test the rendered output of a specific component we can use snapshot testing.
We need to install the {file}`react-test-render` package first:

```console
$ yarn add react-test-renderer --dev
```

Then we will create a file called {file}`FaqItem.test.js`.
Here we will render the component and assert the markup.

```{code-block} jsx
:linenos: true

import React from "react";
import renderer from "react-test-renderer";

import FaqItem from "./FaqItem";

describe("FaqItem", () => {
  it("renders a FAQ item", () => {
    const component = renderer.create(
      <FaqItem
        question="What is the answer to life the universe and everything?"
        answer="42"
      />
    );
    const json = component.toJSON();
    expect(json).toMatchSnapshot();
  });
});
```

To run our tests we will run the command:

```console
$ yarn test
```

This will output our test results:

```console
PASS  src/components/FaqItem.test.js
PASS  src/App.test.js

Test Suites: 2 passed, 2 total
Tests:       2 passed, 2 total
Snapshots:   1 passed, 1 total
Time:        1.491s
Ran all test suites related to changed files.
```
