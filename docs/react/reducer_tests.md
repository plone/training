---
html_meta:
  "description": "Write tests for our reducer. Since reducers are pure functions with input and output, we can write unit tests for them."
  "property=og:description": "Write tests for our reducer. Since reducer are pure funcitons with input and output, we can write unit tests for them."
  "property=og:title": "Reducer Tests"
  "keywords": "Plone, Training, exercise, solution, react,redux, reducers"
---

(reducer-tests-label)=

# Write Tests For Your Reducers

## Reducer Tests

Since reducers are pure functions with input and output, we can write unit tests for them.
We will start by adding a test for the `ADD_TODO` action in a file called {file}`reducers/faq.test.js`:

```{code-block} jsx
:emphasize-lines: 1-16
:linenos: true

import faq from "./faq";

describe("faq", () => {
  it("is able to handle the add faq item action", () => {
    expect(
      faq([], {
        type: "ADD_FAQ_ITEM",
        question: "What is the answer to life the universe and everything?",
        answer: 42
      })
    ).toEqual([{
      question: "What is the answer to life the universe and everything?",
      answer: 42
    }]);
  });
});
```

## Exercise

Add the unit tests for the edit and delete actions for the reducer.

````{admonition} Solution
:class: toggle

```{code-block} jsx
:emphasize-lines: 1-32
:lineno-start: 16
:linenos: true

it("is able to handle the edit faq item action", () => {
  expect(
    faq(
      [{
        question: "What is the answer to life the universe and everything?",
        answer: 42
      }], {
        type: "EDIT_FAQ_ITEM",
        index: 0,
        question: "What is the answer to life the universe and everything?",
        answer: 43
      }
    )
  ).toEqual([{
    question: "What is the answer to life the universe and everything?",
    answer: 43
  }]);
});

it("is able to handle the delete faq item action", () => {
  expect(
    faq(
      [{
        question: "What is the answer to life the universe and everything?",
        answer: 42
      }], {
        type: "DELETE_FAQ_ITEM",
        index: 0
      }
    )
  ).toEqual([]);
});
```
````
