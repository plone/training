.. _redux-label:

=======================
Use Redux To Store Data
=======================

Introduction
============

Currently we have the state of the FAQ list in the :file:`App` component and pass all handlers and data down to the :file:`FaqItem` component.
When your application will contain more sub components this can become very complex.
To manage your application state we will introduce Redux here.
Redux is a state management system which is composed of a store which contains data,
a set of reducers which handle (part of) this state and it's changes and actions which are used to trigger state changes.

A reducer is pure function which takes the previous state and an action and returns a new state based on the data of the action.
The new state is then saved to the store.
Components can then read data from the store and render a view.
When a change needs to be made to the application state the view will fire an action which will be handled by the reducer again etc.
So it's a unidirectional flow.

Installing
==========

To install Redux we will run the following command:

.. code-block:: console

    $ yarn add redux react-redux

Actions
=======

We will start by creating actions.
We will create a file :file:`actions/index.js` with the :file:`addFaqItem` action:

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 1-5

    export const addFaqItem = (question, answer) => ({
      type: "ADD_FAQ_ITEM",
      question,
      answer
    });

Write the :file:`editFaqItem` and :file:`deleteFaqItem` actions.

..  admonition:: Solution
    :class: toggle

    .. code-block:: jsx
        :linenos:
        :lineno-start: 7
        :emphasize-lines: 1-6,8-11

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

Reducers
========

Next we will create the reducer by creating the ``reducers/faq.js`` file.
As stated earlier a reducer is pure function which takes the previous state and an action and returns the new state,
it will look like this:

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 1-3,5

    const faq = (state = [], action) => {
      // Do something
    };

    export default faq;

Finish the reducer so that it can handle the :file:`ADD_FAQ_ITEM`,
:file:`EDIT_FAQ_ITEM` and :file:`DELETE_FAQ_ITEM` actions.

..  admonition:: Solution
    :class: toggle

    .. code-block:: jsx
        :linenos:
        :emphasize-lines: 2-25

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

Combine Multiple Reducers
=========================

When our application grows we will have multiple reducers handling a specific part of the data.
We will combine all reducers into one index reducer so we can set all reducers in one store.
We will create the file :file:`reducers/index.js`

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 1-2,4-6

    import { combineReducers } from "redux";
    import faq from "./faq";

    export default combineReducers({
      faq
    });
