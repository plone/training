---
myst:
  html_meta:
    "description": "Create an express server to provide the initial data for the component. Write a redux middleware to fire a network request to get the initial data."
    "property=og:description": "Create an express server to provide the initial data for the component. Write a redux middleware to fire a network request to get the initial data."
    "property=og:title": "Creating A Simple Backend"
    "keywords": "Plone, training, exercise, solution, React, Node"
---

(external-data-label)=

# Using External Data

## Creating A Simple Backend

To persist our data, we will create a backend to fetch our initial data.
We will use `express` to create a simple server.
To install type:

```shell
yarn add express
```

Now we will create a simple server in the file {file}`server.js`

```{code-block} jsx
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
```

Then we can run our newly created server:

```shell
node server.js
```

Now it is time to write our action to fetch the items from the backend in the file `actions/index.js`:

```{code-block} jsx
:emphasize-lines: 1-7
:lineno-start: 19
:linenos:

export const getFaqItems = () => ({
  type: "GET_FAQ_ITEMS",
  request: {
    op: "get",
    path: "/"
  }
});
```

## Writing Middleware

Since the action itself doesn't do any API call, we will create middleware to do the job.
Redux middleware is a simple method which receives the store, the method to call the next action, and the action itself.
The middleware can then decide to do something based on the data in the action.
In our case we are looking for a property called `request`.
If that one is available, then we want to do an API call with the provided operation, path, and data, and fire a new action when the data is fetched.
We will create a file at {file}`middleware/api.js` and the implementation will look like this:

```{code-block} jsx
:linenos:

const api = store => next => action => {
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

export default api;
```

Finally we need to apply our middleware to the store in `App.js`:

```{code-block} jsx
:emphasize-lines: 2,6,10
:linenos: true

import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";

import rootReducer from "./reducers";
import Faq from "./components/Faq";
import api from "./middleware/api";

import "./App.css";

const store = createStore(rootReducer, applyMiddleware(api));

const App = () => {
  return (
    <Provider store={store}>
      <Faq />
    </Provider>
  );
};

export default App;
```

````{dropdown} Differences
:animate: fade-in-slide-down
:icon: question

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -1,12 +1,13 @@
 import { Provider } from "react-redux";
-import { createStore } from "redux";
+import { createStore, applyMiddleware } from "redux";

 import rootReducer from "./reducers";
 import Faq from "./components/Faq";
+import api from "./middleware/api";

 import "./App.css";

-const store = createStore(rootReducer);
+const store = createStore(rootReducer, applyMiddleware(api));

 const App = () => {
   return (

```
````

The last part is to change our reducer at `reducers/faq.js` to handle the `GET_FAQ_ITEMS_SUCCESS` action:

```{code-block} jsx
:emphasize-lines: 23-24
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
  case "GET_FAQ_ITEMS_SUCCESS":
    return action.data;
  default:
    return state;
  }
};

export default faq;
```
