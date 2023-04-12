---
myst:
  html_meta:
    "description": "Add routes to our App. Create a view for the individual FAQ entries."
    "property=og:description": "Add routes to our App. Create a view for the individual FAQ entries."
    "property=og:title": "Routing"
    "keywords": "Plone, training, exercise, solution, React, react-router-dom"
---

(routes-label)=

# Using Different Routes

## Routing

In this chapter we will add routing so that we can navigate to a specific FAQ item.
First we will install `react-router-dom`:

```shell
yarn add react-router-dom
```

Next we will define the routes we want to use.
We will use `BrowserRouter` to define our routes.
We will have a view at the root, and a view at `/faq/1`, where `1` is the index of the FAQ item.
Our new {file}`App.js` will look like this:

```{code-block} jsx
:emphasize-lines: 3,7,17-22
:linenos: true

import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import { BrowserRouter, Route } from "react-router-dom";

import rootReducer from "./reducers";
import Faq from "./components/Faq";
import FaqItemView from "./components/FaqItemView";
import api from "./middleware/api";

import "./App.css";

const store = createStore(rootReducer, applyMiddleware(api));

const App = () => {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <div>
          <Route exact path="/" component={Faq} />
          <Route path="/faq/:index" component={FaqItemView} />
        </div>
      </BrowserRouter>
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
@@ -1,8 +1,10 @@
 import { Provider } from "react-redux";
 import { createStore, applyMiddleware } from "redux";
+import { BrowserRouter, Route } from "react-router-dom";

 import rootReducer from "./reducers";
 import Faq from "./components/Faq";
+import FaqItemView from "./components/FaqItemView";
 import api from "./middleware/api";

 import "./App.css";
@@ -12,7 +14,12 @@ const store = createStore(rootReducer, applyMiddleware(api));
 const App = () => {
   return (
     <Provider store={store}>
-      <Faq />
+      <BrowserRouter>
+        <div>
+          <Route exact path="/" component={Faq} />
+          <Route path="/faq/:index" component={FaqItemView} />
+        </div>
+      </BrowserRouter>
     </Provider>
   );
 };
```
````

## Writing The View

Now we will create the `FaqItemView` component at {file}`components/FaqItemView.js`.
This will render the full FAQ item.
The code will look something like this:

```{code-block} jsx
:emphasize-lines: 8
:linenos: true

import { useEffect } from "react";
import { getFaqItems } from "../actions";
import { useSelector, useDispatch } from "react-redux";
import { useParams } from "react-router-dom";

const FaqItemView = () => {
  const dispatch = useDispatch();
  const faqItem = "Todo";

  useEffect(() => {
    dispatch(getFaqItems());
  }, [dispatch]);

  return (
    <div>
      <h2 className="question">{faqItem.question}</h2>
      <p>{faqItem.answer}</p>
    </div>
  );
};

export default FaqItemView;
```

## Exercise

React Router has a hook called `useParams` which returns an object of key/value pairs of URL parameters.
The return object contains all the params of the match route, including our `index` params.
Remove the `Todo` string, and write a function for the `useSelector` hook to fetch the correct data from the store.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 1,3-5
:lineno-start: 7
:linenos: true

  const { index } = useParams();
  const dispatch = useDispatch();
  const faqItem = useSelector((state) =>
    state.faq.length ? state.faq[index] : {}
  );
```
````

To test your view navigate to <http://localhost:3000/faq/0>.
