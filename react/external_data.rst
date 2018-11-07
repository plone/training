.. _external_data-label:

===================
Using External Data
===================

Creating A Simple Backend
=========================

To persist our data we will create a backend to fetch our initial data.
We will use :file:`express` to create a simple server.
To install type:

.. code-block:: console

    $ yarn add express

Now we will create a simple server in the file :file:`server.js`

.. code-block:: jsx
    :linenos:

    const express = require("express");
    const app = express();
    const port = 3001;

    const faq = [
      {
        question: "What does the Plone Foundation do?",
        answer: "The mission of the Plone Foundation is to protect and..."
      },
      {
        question: "Why does Plone need a Foundation?",
        answer: "Plone has reached critical mass, with enterprise..."
      }
    ];

    app.get("/", (req, res) => {
      res.header("Access-Control-Allow-Origin", "*");
      res.json(faq);
    });

    app.listen(port, () => console.log(`Listening on port: ${port}`));

Then we can run our newly created server:

.. code-block:: console

    $ node server.js

Now it is time to write our action to fetch the items from the backend in the file ``actions/index.js``:

.. code-block:: jsx
    :linenos: 
    :lineno-start: 19
    :emphasize-lines: 1-7

    export const getFaqItems = () => ({
      type: "GET_FAQ_ITEMS",
      request: {
        op: "get",
        path: "/"
      }
    });

Writing Middleware
==================

Since the action itself doesn't do any api call we will create middleware to do the job.
Redux middleware is a simple method which receives the store,
the method to call the next action and the action itself.
The middleware can then decide to do something based on the data in the action.
In our case we are looking for a property called :file:`request`.
If that one is available we want to do an api call with the provided operation,
path and data and fire a new a new action when the data is fetched.
We will create a file at ``middleware/api.js`` and the implementation will look like this:

.. code-block:: jsx
    :linenos:

    export default store => next => action => {
      const { request, type, ...rest } = action;

      if (!request) {
        return next(action);
      }

      next({ ...rest, type: `${type}_PENDING` });

      const actionPromise = fetch(`http://localhost:3001${request.path}`, {
        method: request.op,
        body: request.data && JSON.stringify(request.data)
      });

      actionPromise.then(response => {
        response.json().then(data => next({ data, type: `${type}_SUCCESS` }));
      });

      return actionPromise;
    };

Finally we need to apply our middleware to the store in ``App.js``:

.. code-block:: jsx
    :linenos: 
    :emphasize-lines: 3,7,11

    import React, { Component } from "react";
    import { Provider } from "react-redux";
    import { createStore, applyMiddleware } from "redux";

    import rootReducer from "./reducers";
    import Faq from "./components/Faq";
    import api from "./middleware/api";

    import "./App.css";

    const store = createStore(rootReducer, applyMiddleware(api));

    class App extends Component {
      render() {
        return (
          <Provider store={store}>
            <Faq />
          </Provider>
        );
      }
    }

    export default App;


..  admonition:: Differences
    :class: toggle

    .. code-block:: dpatch

        --- a/src/App.js
        +++ b/src/App.js
        @@ -1,13 +1,14 @@
        import React, { Component } from "react";
        import { Provider } from "react-redux";
        -import { createStore } from "redux";
        +import { createStore, applyMiddleware } from "redux";

        import rootReducer from "./reducers";
        import Faq from "./components/Faq";
        +import api from "./middleware/api";

        import "./App.css";

        -const store = createStore(rootReducer);
        +const store = createStore(rootReducer, applyMiddleware(api));

        class App extends Component {
          render() {

Last part is to change our reducer at ``reducers/faq.js`` to handle the ``GET_FAQ_ITEMS_SUCCESS`` action:

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 23-24

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
      case "GET_FAQ_ITEMS_SUCCESS":
        return action.data;
      default:
        return state;
      }
    };

    export default faq;
