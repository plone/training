---
myst:
  html_meta:
    "description": "Add state to the App component."
    "property=og:description": "Add state to the App component."
    "property=og:title": "How To Use State In Your Component"
    "keywords": "Plone, trainings, SEO, React, component, exercise, solution"
---

(state-label)=

# How To Use State In Your Component

## Store Questions And Answers In The State

To manipulate the FAQ, we will move all the data to the state of the component.
The state of the component is the local state of that specific component.
When the state changes, the component re-renders itself.
We can initialize the state in our functional component body using the `useState` hook.

```{code-block} jsx
:emphasize-lines: 6-15,19-21
:linenos: true

import { useState } from "react";
import "./App.css";
import FaqItem from "./components/FaqItem";

function App() {
  const [faqList, setFaqList] = useState([
    {
      question: "What does the Plone Foundation do?",
      answer: "The mission of the Plone Foundation is to protect and...",
    },
    {
      question: "Why does Plone need a Foundation?",
      answer: "Plone has reached critical mass, with enterprise...",
    },
  ]);

  return (
    <ul>
      {faqList.map((item, index) => (
        <FaqItem key={index} question={item.question} answer={item.answer} />
      ))}
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
@@ -1,30 +1,24 @@
+import { useState } from "react";
 import "./App.css";
 import FaqItem from "./components/FaqItem";

 function App() {
+  const [faqList, setFaqList] = useState([
+    {
+      question: "What does the Plone Foundation do?",
+      answer: "The mission of the Plone Foundation is to protect and...",
+    },
+    {
+      question: "Why does Plone need a Foundation?",
+      answer: "Plone has reached critical mass, with enterprise...",
+    },
+  ]);
+
   return (
     <ul>
-      <FaqItem
-        question="What does the Plone Foundation do?"
-        answer="
-          The mission of the Plone Foundation is to protect and promote Plone.
-          The Foundation provides marketing assistance, awareness, and
-          evangelism assistance to the Plone community. The Foundation also
-          assists with development funding and coordination of funding for
-          large feature implementations. In this way, our role is similar to
-          the role of the Apache Software Foundation and its relationship with
-          the Apache Project."
-      />
-      <FaqItem
-        question="Why does Plone need a Foundation?"
-        answer="
-          Plone has reached critical mass, with enterprise implementations and
-          worldwide usage. The Foundation is able to speak for Plone, and
-          provide strong and consistent advocacy for both the project and the
-          community. The Plone Foundation also helps ensure a level playing
-          field, to preserve what is good about Plone as new participants
-          arrive."
-      />
+      {faqList.map((item, index) => (
+        <FaqItem key={key} question={item.question} answer={item.answer}
+       />
+      ))}
     </ul>
   );
 }
```
````

## Exercise

To save space in the view, we want to show and hide the answer when you click on the question.
Add a state variable to the `FaqItem` component, which keeps the state of the answer being shown or not, and adjust the render method to show or hide the answer.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

{file}`components/FaqItem.jsx`

```{code-block} jsx
:emphasize-lines: 6,10
:linenos: true

import { useState } from "react";
import "./FaqItem.css";
import PropTypes from "prop-types";

const FaqItem = (props) => {
  const [isAnswer, setAnswer] = useState(false);
  return (
    <li className="faq-item">
      <h2 className="question">{props.question}</h2>
      {isAnswer && <p>{props.answer}</p>}
    </li>
  );
};

FaqItem.propTypes = {
  question: PropTypes.string.isRequired,
  answer: PropTypes.string.isRequired,
};

export default FaqItem;
```

```dpatch
--- a/src/components/FaqItem.jsx
+++ b/src/components/FaqItem.jsx
@@ -1,11 +1,13 @@
+import { useState } from "react";
 import "./FaqItem.css";
 import PropTypes from "prop-types";

 const FaqItem = (props) => {
+  const [isAnswer, setAnswer] = useState(false);
   return (
     <li className="faq-item">
       <h2 className="question">{props.question}</h2>
-      <p>{props.answer}</p>
+      {isAnswer && <p>{props.answer}</p>}
     </li>
   );
 };
```
````
