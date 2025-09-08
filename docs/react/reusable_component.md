---
myst:
  html_meta:
    "description": "Refactor the app.js and create a new component so that we can use the markup."
    "property=og:description": "Refactor the app.js and create a new component so that we can use the markup."
    "property=og:title": "Convert To A Reusable Component"
    "keywords": "Plone, trainings, SEO, React, component, exercise, solution"
---

(reusable-component-label)=

# Convert To A Reusable Component

## Create A Reusable component

To reuse the markup of a FAQ item, we will split up the code.
The app component will contain just the data of the FAQ item and will render a newly created subcomponent called `FaqItem`.
The data is passed to the subcomponent using properties.
In the `FaqItem` component, you will have access to the properties with `props.question`.
The {file}`App.js` code will be changed to:

```{code-block} jsx
:emphasize-lines: 2,7-27
:linenos: true

import "./App.css";
import FaqItem from "./components/FaqItem";

function App() {
  return (
    <ul>
      <FaqItem
        question="What does the Plone Foundation do?"
        answer="
          The mission of the Plone Foundation is to protect and promote Plone.
          The Foundation provides marketing assistance, awareness, and
          evangelism assistance to the Plone community. The Foundation also
          assists with development funding and coordination of funding for
          large feature implementations. In this way, our role is similar to
          the role of the Apache Software Foundation and its relationship with
          the Apache Project."
      />
      <FaqItem
        question="Why does Plone need a Foundation?"
        answer="
          Plone has reached critical mass, with enterprise implementations and
          worldwide usage. The Foundation is able to speak for Plone, and
          provide strong and consistent advocacy for both the project and the
          community. The Plone Foundation also helps ensure a level playing
          field, to preserve what is good about Plone as new participants
          arrive."
      />
    </ul>
  );
}

export default App;
```

````{dropdown} Differences
:animate: fade-in-slide-down
:icon: question

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -1,31 +1,30 @@
 import "./App.css";
+import FaqItem from "./components/FaqItem";

 function App() {
   return (
     <ul>
-      <li className="faq-item">
-        <h2 className="question">What does the Plone Foundation do?</h2>
-        <p>
+      <FaqItem
+        question="What does the Plone Foundation do?"
+        answer="
           The mission of the Plone Foundation is to protect and promote Plone.
           The Foundation provides marketing assistance, awareness, and
           evangelism assistance to the Plone community. The Foundation also
-          assists with development funding and coordination of funding for large
-          feature implementations. In this way, our role is similar to the role
-          of the Apache Software Foundation and its relationship with the Apache
-          Project.
-        </p>
-      </li>
-      <li className="faq-item">
-        <h2 className="question">Why does Plone need a Foundation?</h2>
-        <p>
+          assists with development funding and coordination of funding for
+          large feature implementations. In this way, our role is similar to
+          the role of the Apache Software Foundation and its relationship with
+          the Apache Project."
+      />
+      <FaqItem
+        question="Why does Plone need a Foundation?"
+        answer="
           Plone has reached critical mass, with enterprise implementations and
           worldwide usage. The Foundation is able to speak for Plone, and
           provide strong and consistent advocacy for both the project and the
           community. The Plone Foundation also helps ensure a level playing
           field, to preserve what is good about Plone as new participants
-          arrive.
-        </p>
-      </li>
+          arrive."
+      />
     </ul>
   );
 }
```
````

## Exercise

Create the `FaqItem` component in a newly created folder called `components` which renders the same output.
Also move all the styling of the view to {file}`components/FaqItem.css`.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

{file}`components/FaqItem.jsx`

```{code-block} jsx
:linenos:

import "./FaqItem.css";

const FaqItem = (props) => {
  return (
    <li className="faq-item">
      <h2 className="question">{props.question}</h2>
      <p>{props.answer}</p>
    </li>
  );
};

export default FaqItem;
```
````

## Property Validation

React has a builtin mechanism to validate the properties being passed in into a component.
When incorrect values are passed, you will receive a warning in the console.
In the above example, you have to add an extra import:

```jsx
import PropTypes from "prop-types";
```

And the following static property to the function to validate the properties:

```jsx
FaqItem.propTypes = {
  question: PropTypes.string.isRequired,
  answer: PropTypes.string.isRequired,
};
```

If you now add a third empty `<FaqItem>` to {file}`App.js`, errors of missing properties on this component call will be reported in the JavaScript console of your browser.

```{code-block} jsx
:emphasize-lines: 2,13-16
:linenos: true

import "./FaqItem.css";
import PropTypes from "prop-types";

const FaqItem = (props) => {
  return (
    <li className="faq-item">
      <h2 className="question">{props.question}</h2>
      <p>{props.answer}</p>
    </li>
  );
};

FaqItem.propTypes = {
  question: PropTypes.string.isRequired,
  answer: PropTypes.string.isRequired,
};

export default FaqItem;
```
