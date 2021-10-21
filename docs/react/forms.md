---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(forms-label)=

# Use Forms To Add An Item

## Add The Form

To be able to add FAQ items to the list we will start by adding an add form:

```{code-block} jsx
:emphasize-lines: 3,14-23
:lineno-start: 31
:linenos:

render() {
  return (
    <div>
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
      <form>
        <label>
          Question: <input name="question" type="text" />
        </label>
        <label>
          Answer: <textarea name="answer" />
        </label>
        <input type="submit" value="Add" />
      </form>
    </div>
  );
}
```

````{admonition} Differences
:class: toggle

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -30,16 +30,27 @@ class App extends Component {

  render() {
    return (
-      <ul>
-        {this.state.faq.map((item, index) => (
-          <FaqItem
-            question={item.question}
-            answer={item.answer}
-            index={index}
-            onDelete={this.onDelete}
-          />
-        ))}
-      </ul>
+      <div>
+        <ul>
+          {this.state.faq.map((item, index) => (
+            <FaqItem
+              question={item.question}
+              answer={item.answer}
+              index={index}
+              onDelete={this.onDelete}
+            />
+          ))}
+        </ul>
+        <form>
+          <label>
+            Question: <input name="question" type="text" />
+          </label>
+          <label>
+            Answer: <textarea name="answer" />
+          </label>
+          <input type="submit" value="Add" />
+        </form>
+      </div>
    );
  }
}
```
````

## Manage Field Values In The State

To manage the values of the fields in the form we will use the state.
Add a question and answer value to the state which contains the values of the inputs.
Add {file}`onChange` handlers to the input and textarea which will change the values in the state when the input changes.
This pattern is called controlled inputs.

````{admonition} Solution
:class: toggle

```{code-block} jsx
:emphasize-lines: 9-10,23-25,37-47,62-81
:linenos:

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
            "The mission of the Plone Foundation is to protect and promote Plone. The Foundation provides marketing assistance, awareness, and evangelism assistance to the Plone community. The Foundation also assists with development funding and coordination of funding for large feature implementations. In this way, our role is similar to the role of the Apache Software Foundation and its relationship with the Apache Project."
        },
        {
          question: "Why does Plone need a Foundation?",
          answer:
            "Plone has reached critical mass, with enterprise implementations and worldwide usage. The Foundation is able to speak for Plone, and provide strong and consistent advocacy for both the project and the community. The Plone Foundation also helps ensure a level playing field, to preserve what is good about Plone as new participants arrive."
        }
      ],
      question: "",
      answer: ""
    };
  }

  onDelete = (index) => {
    let faq = this.state.faq;
    faq.splice(index, 1);
    this.setState({
      faq
    });
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

  render() {
    return (
      <div>
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
        <form>
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

export default App;
```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -6,17 +6,23 @@ class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      faq: [
        {
          question: "What does the Plone Foundation do?",
-          answer: "The mission of the Plone Foundation is to protect and..."
+          answer:
+            "The mission of the Plone Foundation is to protect and promote Plone. The Foundation provides marketing assistance, awareness, and evangelism assistance to the Plone community. The Foundation also assists with development funding and coordination of funding for large feature implementations. In this way, our role is similar to the role of the Apache Software Foundation and its relationship with the Apache Project."
        },
        {
          question: "Why does Plone need a Foundation?",
-          answer: "Plone has reached critical mass, with enterprise..."
+          answer:
+            "Plone has reached critical mass, with enterprise implementations and worldwide usage. The Foundation is able to speak for Plone, and provide strong and consistent advocacy for both the project and the community. The Plone Foundation also helps ensure a level playing field, to preserve what is good about Plone as new participants arrive."
        }
-      ]
+      ],
+      question: "",
+      answer: ""
    };
  }

@@ -28,6 +34,18 @@ class App extends Component {
    });
  }

+  onChangeQuestion = (event) => {
+    this.setState({
+      question: event.target.value
+    });
+  }
+
+  onChangeAnswer = (event) => {
+    this.setState({
+      answer: event.target.value
+    });
+  }
+
  render() {
    return (
      <div>
@@ -43,10 +61,21 @@ class App extends Component {
        </ul>
        <form>
          <label>
-            Question: <input name="question" type="text" />
+            Question:
+            <input
+              name="question"
+              type="text"
+              value={this.state.question}
+              onChange={this.onChangeQuestion}
+            />
          </label>
          <label>
-            Answer: <textarea name="answer" />
+            Answer:
+            <textarea
+              name="answer"
+              value={this.state.answer}
+              onChange={this.onChangeAnswer}
+            />
          </label>
          <input type="submit" value="Add" />
        </form>
```
````

## Submit Handler

Now that our values are managed in the state we can write our submit handler.
Write an {file}`onSubmit` handler which reads the values from the state and add the new FAQ item to the list.
After the item is added the inputs should also reset to empty values.

````{admonition} Solution
:class: toggle

Make sure you bind the `onSubmit` handler.

```{code-block} jsx
:emphasize-lines: 1
:lineno-start: 11
:linenos:

Where is the code?
```

And add this to the body of the class.

```{code-block} jsx
:emphasize-lines: 1-14,29
:lineno-start: 50
:linenos:

onSubmit = (event) => {
  this.setState({
    faq: [
      ...this.state.faq,
      {
        question: this.state.question,
        answer: this.state.answer
      }
    ],
    question: "",
    answer: ""
  });
  event.preventDefault();
}

render() {
  return (
    <div>
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
```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -8,6 +8,7 @@ class App extends Component {
    this.state = {
      faq: [
        {
@@ -46,6 +47,21 @@ class App extends Component {
    });
  }

+  onSubmit = (event) => {
+    this.setState({
+      faq: [
+        ...this.state.faq,
+        {
+          question: this.state.question,
+          answer: this.state.answer
+        }
+      ],
+      question: "",
+      answer: ""
+    });
+    event.preventDefault();
+  }
+
  render() {
    return (
      <div>
@@ -59,7 +75,7 @@ class App extends Component {
            />
          ))}
        </ul>
-        <form>
+        <form onSubmit={this.onSubmit}>
          <label>
            Question:
            <input
```
````
