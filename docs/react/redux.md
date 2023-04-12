---
myst:
  html_meta:
    "description": "Add redux to our App for managing the state throughout the App."
    "property=og:description": "Add redux to our App for managing the state throughout the App."
    "property=og:title": "Use Redux to Store Data"
    "keywords": "Plone, training, exercise, solution, React, Redux"
---

(redux-label)=

# Use Redux To Store Data

## Introduction

Currently we have the state of the FAQ list in the `App` component and pass all handlers and data down to the `FaqItem` component.
When your application will contain more subcomponents, this can become very complex.
To manage your application state, we will introduce Redux here.
Redux is a state management system which is composed of a store.
This store contains data, a set of reducers which handle (part of) this state and its changes, and actions which are used to trigger state changes.

A reducer is pure function which takes the previous state and an action, and returns a new state based on the data of the action.
The new state is then saved to the store.
Components can then read data from the store and render a view.
When a change needs to be made to the application state, the view will fire an action which will be handled by the reducer again, and so on.
This is a unidirectional flow.

## Installing

To install Redux, we will run the following command:

```shell
yarn add redux react-redux
```

## Actions

We will start by creating actions.
We will create a file {file}`actions/index.js` with the `addFaqItem` action:

```{code-block} jsx
:emphasize-lines: 1-5
:linenos:

export const addFaqItem = (question, answer) => ({
  type: "ADD_FAQ_ITEM",
  question,
  answer
});
```

Write the `editFaqItem` and `deleteFaqItem` actions.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 1-6,8-11
:lineno-start: 7
:linenos:

export const editFaqItem = (index, question, answer) => ({
  type: "EDIT_FAQ_ITEM",
  index,
  question,
  answer
});

export const deleteFaqItem = index => ({
  type: "DELETE_FAQ_ITEM",
  index
});
```
````

## Reducers

Next we will create the reducer by creating the `reducers/faq.js` file.
As stated earlier, a reducer is a pure function which takes the previous state and an action, and returns the new state.
It will look like this:

```{code-block} jsx
:emphasize-lines: 1-3,5
:linenos:

const faq = (state = [], action) => {
  // Do something
};

export default faq;
```

Finish the reducer so that it can handle the `ADD_FAQ_ITEM`, `EDIT_FAQ_ITEM`, and `DELETE_FAQ_ITEM` actions.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 2-25
:linenos:

const faq = (state = [], action) => {
  let faq;
  switch (action.type) {
    case "ADD_FAQ_ITEM":
      return [
        ...state,
        {
          question: action.question,
          answer: action.answer
        }
      ];
    case "EDIT_FAQ_ITEM":
      faq = [...state];
      faq[action.index] = {
        question: action.question,
        answer: action.answer
      };
      return faq;
    case "DELETE_FAQ_ITEM":
      faq = [...state];
      faq.splice(action.index, 1);
      return faq;
    default:
      return state;
  }
};

export default faq;
```
````

## Combine Multiple Reducers

When our application grows, we will have multiple reducers handling a specific part of the data.
We will combine all reducers into one index reducer, such that we can set all reducers in one store.
We will create the file {file}`reducers/index.js`.

```{code-block} jsx
:emphasize-lines: 1-2,4-6
:linenos:

import { combineReducers } from "redux";
import faq from "./faq";

export default combineReducers({
  faq
});
```
