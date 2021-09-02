(lifecycle-methods-label)=

# Use Lifecycle Methods

Lifecycle methods are methods which are called on specific external events.
For example the {file}`componentDidMount` method is called when the component gets added to the dom.
We can use this method to do additional calls.
For example in our case we want to fetch the initial data from the backend.

```{code-block} jsx
:emphasize-lines: 1-3
:lineno-start: 31
:linenos: true

componentDidMount() {
  this.props.getFaqItems();
}
```

The {file}`getFaqItems` method is mapped using the connect call.
The full {file}`Faq` component will now look like this:

```{code-block} jsx
:emphasize-lines: 6,16-17,31-33,95
:linenos: true

import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";

import FaqItem from "./FaqItem";
import { addFaqItem, getFaqItems } from "../actions";

class Faq extends Component {
  static propTypes = {
    faq: PropTypes.arrayOf(
      PropTypes.shape({
        question: PropTypes.string.isRequired,
        answer: PropTypes.string.isRequired
      })
    ),
    addFaqItem: PropTypes.func.isRequired,
    getFaqItems: PropTypes.func.isRequired
  };

  constructor(props) {
    super(props);
    this.state = {
      question: "",
      answer: ""
    };
  }

  componentDidMount() {
    this.props.getFaqItems();
  }

  onChangeQuestion = (event) => {
    this.setState({
      question: event.target.value
    });
  }

  onChangeAnswer = (event) => {
    this.setState({
      answer: event.target.value
    });
  }

  onSubmit = (event) => {
    this.props.addFaqItem(this.state.question, this.state.answer);
    this.setState({
      question: "",
      answer: ""
    });
    event.preventDefault();
  }

  render() {
    return (
      <div>
        <ul>
          {this.props.faq.map((item, index) => (
            <FaqItem
              question={item.question}
              answer={item.answer}
              index={index}
            />
          ))}
        </ul>
        <form onSubmit={this.onSubmit}>
          <label>
            Question:
            <input
              name="question"
              type="text"
              value={this.state.question}
              onChange={this.onChangeQuestion}
            />
          </label>
          <label>
            Answer:
            <textarea
              name="answer"
              value={this.state.answer}
              onChange={this.onChangeAnswer}
            />
          </label>
          <input type="submit" value="Add" />
        </form>
      </div>
    );
  }
}

export default connect(
  (state, props) => ({
    faq: state.faq
  }),
  { addFaqItem, getFaqItems }
)(Faq);
```

````{admonition} Differences
:class: toggle

```dpatch
--- a/src/components/Faq.jsx
+++ b/src/components/Faq.jsx
@@ -3,7 +3,7 @@ import { connect } from "react-redux";
import PropTypes from "prop-types";

import FaqItem from "./FaqItem";
-import { addFaqItem } from "../actions";
+import { addFaqItem, getFaqItems } from "../actions";

class Faq extends Component {
  static propTypes = {
@@ -13,7 +13,8 @@ class Faq extends Component {
        answer: PropTypes.string.isRequired
      })
    ),
-    addFaqItem: PropTypes.func.isRequired
+    addFaqItem: PropTypes.func.isRequired,
+    getFaqItems: PropTypes.func.isRequired
  };

  constructor(props) {
@@ -27,6 +28,10 @@ class Faq extends Component {
    };
  }

+  componentDidMount() {
+    this.props.getFaqItems();
+  }
+
  onChangeQuestion = (event) => {
    this.setState({
      question: event.target.value
@@ -89,5 +94,5 @@ export default connect(
  (state, props) => ({
    faq: state.faq
  }),
-  { addFaqItem }
+  { addFaqItem, getFaqItems }
)(Faq);
```
````
