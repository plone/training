---
myst:
  html_meta:
    "description": "Style the React component."
    "property=og:description": "Style the React component."
    "property=og:title": "Styling your React component"
    "keywords": "Plone, trainings, SEO, style, CSS, React, component, exercise, solution"
---

(react-styling-label)=

# Styling Your Component

## Add style sheet

To add a style sheet, we import the CSS file:

```jsx
import "./App.css";
```

## Exercise

Style the component so that the dot on each item is removed and the question is underlined.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

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
:emphasize-lines: 1,6-7,18-19
:linenos: true

import "./App.css";

function App() {
  return (
    <ul>
      <li className="faq-item">
        <h2 className="question">What does the Plone Foundation do?</h2>
        <p>
          The mission of the Plone Foundation is to protect and promote Plone.
          The Foundation provides marketing assistance, awareness, and
          evangelism assistance to the Plone community. The Foundation also
          assists with development funding and coordination of funding for large
          feature implementations. In this way, our role is similar to the role
          of the Apache Software Foundation and its relationship with the Apache
          Project.
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

export default App;
```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -1,8 +1,10 @@
+import "./App.css";
+
 function App() {
   return (
     <ul>
-      <li>
-        <h2>What does the Plone Foundation do?</h2>
+      <li className="faq-item">
+        <h2 className="question">What does the Plone Foundation do?</h2>
         <p>
           The mission of the Plone Foundation is to protect and promote Plone.
           The Foundation provides marketing assistance, awareness, and
@@ -13,8 +15,8 @@ function App() {
           Project.
         </p>
       </li>
-      <li>
-        <h2>Why does Plone need a Foundation?</h2>
+      <li className="faq-item">
+        <h2 className="question">Why does Plone need a Foundation?</h2>
         <p>
           Plone has reached critical mass, with enterprise implementations and
           worldwide usage. The Foundation is able to speak for Plone, and
```
````
