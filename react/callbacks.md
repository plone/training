(callbacks-label)=

# Use Callbacks To Delete An Item

## Add Delete Button

To be able to manage our FAQ entries we start by adding a delete button to remove an item from the list.
Add the delete button to the {file}`FaqItem` view in the {file}`FaqItem.jsx` file
and create an empty {file}`onDelete` handler which is called when the button is pressed.

````{admonition} Solution
:class: toggle

```{code-block} jsx
:emphasize-lines: 14,26,35
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

  onDelete = () => {}

  render() {
    return (
      <li className="faq-item">
        <h2 onClick={this.toggle} className="question">
          {this.props.question}
        </h2>
        {this.state.show && <p>{this.props.answer}</p>}
        <button onClick={this.onDelete}>Delete</button>
      </li>
    );
  }
}

export default FaqItem;
```

```dpatch
--- a/src/components/FaqItem.jsx
+++ b/src/components/FaqItem.jsx
@@ -11,6 +11,7 @@ class FaqItem extends Component {
  constructor(props) {
    super(props);
    this.state = {
      show: false
    };
@@ -22,6 +23,8 @@ class FaqItem extends Component {
    });
  }

+  onDelete = () => {}
+
  render() {
    return (
      <li className="faq-item">
@@ -29,6 +32,7 @@ class FaqItem extends Component {
          {this.props.question}
        </h2>
        {this.state.show && <p>{this.props.answer}</p>}
+        <button onClick={this.onDelete}>Delete</button>
      </li>
    );
  }
```
````

## Write The onDelete Handler

Now that we have our dummy handler ready we need to add functionality to the handler.
Since the list of FAQ items is managed by our {file}`App` component we can not directly remove the item.
Rewrite the {file}`FaqItem` component so that a unique identifier of the FAQ item
and a callback to remove the FAQ item can be passed to this component.
Also complete the {file}`onDelete` handler so it will call the callback with the correct identifier.

````{admonition} Solution
:class: toggle

```{code-block} jsx
:emphasize-lines: 7-10,28-30
:linenos: true

import React, { Component } from "react";
import PropTypes from "prop-types";
import "./FaqItem.css";

class FaqItem extends Component {
  static propTypes = {
    question: PropTypes.string.isRequired,
    answer: PropTypes.string.isRequired,
    index: PropTypes.number.isRequired,
    onDelete: PropTypes.func.isRequired
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

  onDelete = () => {
    this.props.onDelete(this.props.index);
  }

  render() {
    return (
      <li className="faq-item">
        <h2 onClick={this.toggle} className="question">
          {this.props.question}
        </h2>
        {this.state.show && <p>{this.props.answer}</p>}
        <button onClick={this.onDelete}>Delete</button>
      </li>
    );
  }
}

export default FaqItem;
```

```dpatch
--- a/src/components/FaqItem.jsx
+++ b/src/components/FaqItem.jsx
@@ -5,7 +5,9 @@ import "./FaqItem.css";
class FaqItem extends Component {
  static propTypes = {
    question: PropTypes.string.isRequired,
-    answer: PropTypes.string.isRequired
+    answer: PropTypes.string.isRequired,
+    index: PropTypes.number.isRequired,
+    onDelete: PropTypes.func.isRequired
  };

  constructor(props) {
@@ -23,7 +25,9 @@ class FaqItem extends Component {
    });
  }

-  onDelete = () => {}
+  onDelete = () =>  {
+    this.props.onDelete(this.props.index);
+  }

  render() {
    return (
```
````

## Write A Dummy Delete Handler

Now we're ready to change the {file}`App` component to add a dummy {file}`onDelete` handler.
Add the {file}`onDelete` handler to the {file}`App` component which logs the index of the FAQ item to the console.
Make sure to pass the index and the callback to the {file}`FaqItem` component to wire everything together:

````{admonition} Solution
:class: toggle

```{code-block} js
:emphasize-lines: 8,25-27,33-38
:linenos: true

import React, { Component } from "react";
import FaqItem from "./components/FaqItem";
import "./App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      faq: [
        {
          question: "What does the Plone Foundation do?",
          answer:
            "The mission of the Plone Foundation is to protect and..."
        },
        {
          question: "Why does Plone need a Foundation?",
          answer:
            "Plone has reached critical mass, with enterprise..."
        }
      ]
    };
  }

  onDelete = (index) => {
    console.log(index);
  }

  render() {
    return (
      <ul>
        {this.state.faq.map((item, index) => (
          <FaqItem
            question={item.question}
            answer={item.answer}
            index={index}
            onDelete={this.onDelete}
          />
        ))}
      </ul>
    );
  }
}

export default App;
```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -5,6 +5,7 @@ import "./App.css";
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      faq: [
        {
@@ -19,11 +20,20 @@ class App extends Component {
    };
  }

+  onDelete = (index) => {
+    console.log(index);
+  }
+
  render() {
    return (
      <ul>
-        {this.state.faq.map(item => (
-          <FaqItem question={item.question} answer={item.answer} />
+        {this.state.faq.map((item, index) => (
+          <FaqItem
+            question={item.question}
+            answer={item.answer}
+            index={index}
+            onDelete={this.onDelete}
+          />
        ))}
      </ul>
    );
```
````

## Delete The FAQ Item From The List

The last step is to remove the item from the list.
Write the {file}`onDelete` handler which removes the item from the list and creates the new state.

````{admonition} Solution
:class: toggle

```{code-block} jsx
:emphasize-lines: 1-7
:lineno-start: 23
:linenos: true

onDelete = (index) => {
  let faq = this.state.faq;
  faq.splice(index, 1);
  this.setState({
    faq
  });
}
```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -21,7 +21,11 @@ class App extends Component {
  }

  onDelete = (index) => {
-    console.log(index);
+    let faq = this.state.faq;
+    faq.splice(index, 1);
+    this.setState({
+      faq
+    });
  }

  render() {
```
````
