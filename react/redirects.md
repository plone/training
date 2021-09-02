(redirects-label)=

# Navigate Using Redirects

If we want to navigate programmatically for example after submitting a form we have to use a different method.
In this example we will create a back button in the {file}`FaqItemView` to return to the overview.
First we will create the button:

```{code-block} jsx
:emphasize-lines: 1
:lineno-start: 36
:linenos: true

<button onClick={this.onBack}>Back</button>
```

Then we will add the handler to handle the back event.
This event will make use of the {file}`history` property passed by React Router.
This property has a push method which will push the new route.

```{code-block} jsx
:emphasize-lines: 1-3
:lineno-start: 27
:linenos: true

onBack() {
  this.props.history.push("/");
}
```

The full listing of our new {file}`FaqItemView` will look as follows:

```{code-block} jsx
:emphasize-lines: 13-15,18-21,27-29,36
:linenos: true

import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";

import { getFaqItems } from "../actions";

class FaqItemView extends Component {
  static propTypes = {
    faqItem: PropTypes.shape({
      question: PropTypes.string,
      answer: PropTypes.string
    }).isRequired,
    history: PropTypes.shape({
      push: PropTypes.func
    }).isRequired
  };

  constructor(props) {
    super(props);
  }

  componentDidMount() {
    this.props.getFaqItems();
  }

  onBack = () => {
    this.props.history.push("/");
  }

  render() {
    return (
      <div>
        <h2 className="question">{this.props.faqItem.question}</h2>
        <p>{this.props.faqItem.answer}</p>
        <button onClick={this.onBack}>Back</button>
      </div>
    );
  }
}

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

````{admonition} Differences
:class: toggle

```dpatch
--- a/src/components/FaqItemView.jsx
+++ b/src/components/FaqItemView.jsx
@@ -9,18 +9,31 @@ class FaqItemView extends Component {
    faqItem: PropTypes.shape({
      question: PropTypes.string,
      answer: PropTypes.string
     }).isRequired,
+    history: PropTypes.shape({
+      push: PropTypes.func
+   }).isRequired
  };

+  constructor(props) {
+    super(props);
+  }
+
  componentDidMount() {
    this.props.getFaqItems();
  }

+  onBack = () => {
+    this.props.history.push("/");
+  }
+
  render() {
    return (
      <div>
        <h2 className="question">{this.props.faqItem.question}</h2>
        <p>{this.props.faqItem.answer}</p>
+        <button onClick={this.onBack}>Back</button>
      </div>
    );
  }
```
````
