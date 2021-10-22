---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(react-styling-label)=

# Styling Your Component

## Add stylesheet

To add a stylesheet we simply import the {file}`css` file:

```jsx
import "./App.css";
```

## Exercise

Style the component so that the dot on each item is removed and the question is underlined.

````{admonition} Solution
:class: toggle

{file}`App.css`

```{code-block} css
:linenos:

.faq-item {
  list-style-type: none;
}

.question {
  text-decoration: underline;
}
```

{file}`App.js`

```{code-block} jsx
:emphasize-lines: 2,8-9,20-21
:linenos:

import React, { Component } from "react";
import "./App.css";

class App extends Component {
  render() {
    return (
      <ul>
        <li className="faq-item">
          <h2 className="question">What does the Plone Foundation do?</h2>
          <p>
            The mission of the Plone Foundation is to protect and promote Plone.
            The Foundation provides marketing assistance, awareness, and
            evangelism assistance to the Plone community. The Foundation also
            assists with development funding and coordination of funding for
            large feature implementations. In this way, our role is similar to
            the role of the Apache Software Foundation and its relationship with
            the Apache Project.
          </p>
        </li>
        <li className="faq-item">
          <h2 className="question">Why does Plone need a Foundation?</h2>
          <p>
            Plone has reached critical mass, with enterprise implementations and
            worldwide usage. The Foundation is able to speak for Plone, and
            provide strong and consistent advocacy for both the project and the
            community. The Plone Foundation also helps ensure a level playing
            field, to preserve what is good about Plone as new participants
            arrive.
          </p>
        </li>
      </ul>
    );
  }
}

export default App;
```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -1,11 +1,12 @@
import React, { Component } from "react";
+import "./App.css";

class App extends Component {
  render() {
    return (
      <ul>
-        <li>
-          <h2>What does the Plone Foundation do?</h2>
+        <li className="faq-item">
+          <h2 className="question">What does the Plone Foundation do?</h2>
          <p>
            The mission of the Plone Foundation is to protect and promote Plone.
            The Foundation provides marketing assistance, awareness, and
@@ -16,8 +17,8 @@ class App extends Component {
            the Apache Project.
          </p>
        </li>
-        <li>
-          <h2>Why does Plone need a Foundation?</h2>
+        <li className="faq-item">
+          <h2 className="question">Why does Plone need a Foundation?</h2>
          <p>
              Plone has reached critical mass, with enterprise implementations and
            worldwide usage. The Foundation is able to speak for Plone, and
```
````
