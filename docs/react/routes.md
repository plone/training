---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(routes-label)=

# Using Different Routes

## Routing

In this chapter we will add routing so we can navigate to a specific FAQ item.
First we will install {file}`react-router`:

```shell
yarn add react-router-dom
```

Next we will define the routes we want to use.
We will use the {file}`BrowserRouter` to define our routes.
We will have a view at the root and a view at {file}`/faq/1` where '1' is the index of the FAQ item.
Our new `App.js` will look like this:

```{code-block} jsx
:emphasize-lines: 4,8,19-24
:linenos:

import React, { Component } from "react";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import { BrowserRouter, Route } from "react-router-dom";

import rootReducer from "./reducers";
import Faq from "./components/Faq";
import FaqItemView from "./components/FaqItemView";
import api from "./middleware/api";

import "./App.css";

const store = createStore(rootReducer, applyMiddleware(api));

class App extends Component {
  render() {
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
  }
}

export default App;
```

````{admonition} Differences
:class: toggle

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -1,9 +1,11 @@
import React, { Component } from "react";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
+import { BrowserRouter, Route } from "react-router-dom";

import rootReducer from "./reducers";
import Faq from "./components/Faq";
+import FaqItemView from "./components/FaqItemView";
import api from "./middleware/api";

import "./App.css";
@@ -14,7 +16,12 @@ class App extends Component {
  render() {
    return (
      <Provider store={store}>
-        <Faq />
+        <BrowserRouter>
+          <div>
+            <Route exact path="/" component={Faq} />
+            <Route path="/faq/:index" component={FaqItemView} />
+          </div>
+        </BrowserRouter>
      </Provider>
    );
  }
```
````

## Writing The View

Now we will create the {file}`FaqItemView` component at `components/FaqItemView.js`.
This will render the full FAQ item.
The code will look something like this:

```{code-block} jsx
:emphasize-lines: 31
:linenos:

import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";

import { getFaqItems } from "../actions";

class FaqItemView extends Component {
  static propTypes = {
    faqItem: PropTypes.shape({
      question: PropTypes.string,
      answer: PropTypes.string
    }).isRequired
  };

  componentDidMount() {
    this.props.getFaqItems();
  }

  render() {
    return (
      <div>
        <h2 className="question">{this.props.faqItem.question}</h2>
        <p>{this.props.faqItem.answer}</p>
      </div>
    );
  }
}

export default connect(
  (state, props) => {
    // Todo
  },
  { getFaqItems }
)(FaqItemView);
```

## Exercise

React Router add a property called {file}`match` to all nested components.
This property contains all the information about the matched route including the parameters
so {file}`props.match.params.index` contains the index of the faq item.
Complete the {file}`connect` call to return the correct data:

````{admonition} Solution
:class: toggle

```{code-block} jsx
:emphasize-lines: 3-6
:lineno-start: 29
:linenos:

export default connect(
  (state, props) => {
    const index = parseInt(props.match.params.index, 10);
    return {
      faqItem: index < state.faq.length ? state.faq[index] : {}
    };
  },
  { getFaqItems }
)(FaqItemView);
```
````

To test your view navigate to <http://localhost:3000/faq/0>
