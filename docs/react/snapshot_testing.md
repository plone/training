---
myst:
  html_meta:
    "description": "Snapshot testing to test the rendered output of the Faqitem component."
    "property=og:description": "Snapshot testing to test the rendered output of the Faqitem component."
    "property=og:title": "Snapshot Testing"
    "keywords": "Plone, training, snaphot testing, test, React"
---

(snapshot-testing-label)=

# Use Snapshot Testing

To test the render output of a specific component, we can use snapshot testing.

First we will create a file called {file}`FaqItem.test.js`.
We will also delete the {file}`App.test.js` file, because we have deleted all the initial content of `App.js` and tests refer to those.
Here we will render the component and assert the markup.

```{code-block} jsx
:linenos:

import React from "react";
import { render } from "@testing-library/react";

import FaqItem from "./FaqItem";

describe("FaqItem", () => {
  it("renders a FAQ item", () => {
    const view = render(
      <FaqItem
        question="What is the answer to life the universe and everything?"
        answer="42"
      />
    );
    expect(view).toMatchSnapshot();
  });
});
```

To run our tests we will run the command:

```shell
yarn test
```

This will output our test results:

```console
PASS  src/components/FaqItem.test.js

Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
Snapshots:   1 passed, 1 total
Time:        0.538s
Ran all test suites related to changed files.
```
