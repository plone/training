---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(event-handlers-label)=

# Use Event Handlers

## Toggle Method

To show or hide the answer we will add a toggle handler to the class {file}`FaqItem.jsx`.
This method needs to be bound to the instance like this:

```{code-block} jsx
:emphasize-lines: 3
:lineno-start: 11
:linenos: true

constructor(props) {
  super(props);
  this.state = {
    show: false
  };
}
```

## Exercise

Write the toggle handler which will toggle the {file}`show` state variable
and set the new state using the {file}`setState` method:

````{admonition} Solution
:class: toggle

```{code-block} jsx
:emphasize-lines: 1-5
:lineno-start: 19
:linenos: true

toggle = () => {
  this.setState({
    show: !this.state.show
  });
}
```
````

## Click Handler

To call the newly created {file}`toggle` method we will add an on click handler to the question:

```{code-block} jsx
:emphasize-lines: 4-6
:lineno-start: 25
:linenos: true

render() {
  return (
    <li className="faq-item">
      <h2 onClick={this.toggle} className="question">
        {this.props.question}
      </h2>
      {this.state.show && <p>{this.props.answer}</p>}
    </li>
  );
}
```

````{admonition} Differences
:class: toggle

{file}`FaqItem.jsx`

```dpatch
--- a/src/components/FaqItem.jsx
+++ b/src/components/FaqItem.jsx
@@ -10,15 +10,24 @@ class FaqItem extends Component {

  constructor(props) {
    super(props);
    this.state = {
      show: false
    };
  }

+  toggle = () => {
+    this.setState({
+      show: !this.state.show
+    });
+  }
+
  render() {
    return (
      <li className="faq-item">
-        <h2 className="question">{this.props.question}</h2>
+        <h2 onClick={this.toggle} className="question">
+          {this.props.question}
+        </h2>
        {this.state.show && <p>{this.props.answer}</p>}
      </li>
    );
```

```{code-block} jsx
:linenos: true

import React, { Component } from "react";
import PropTypes from "prop-types";
import "./FaqItem.css";

class FaqItem extends Component {
  static propTypes = {
    question: PropTypes.string.isRequired,
    answer: PropTypes.string.isRequired
  };

  constructor(props) {
    super(props);
    this.state = {
      show: false
    };
  }

  toggle = () => {
    this.setState({
      show: !this.state.show
    });
  }

  render() {
    return (
      <li className="faq-item">
        <h2 onClick={this.toggle} className="question">
          {this.props.question}
        </h2>
        {this.state.show && <p>{this.props.answer}</p>}
      </li>
    );
  }
}

export default FaqItem;
```
````
