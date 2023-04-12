---
myst:
  html_meta:
    "description": "Add a delete button and onDelete handler to remove the question from the list."
    "property=og:description": "Add a delete button and onDelete handler to remove the question from the list."
    "property=og:title": "Use Callbacks To Delete An Item"
    "keywords": "Plone, training, SEO, exercise, solution, React"
---

(callbacks-label)=

# Use Callbacks To Delete An Item

## Add Delete Button

To be able to manage our FAQ entries, we start by adding a delete button to remove an item from the list.
Add the delete button to the `FaqItem` view in the {file}`FaqItem.jsx` file.
Create an empty `onDelete` handler which is called when the button is pressed.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 11,19
:linenos: true

import { useState } from "react";
import "./FaqItem.css";
import PropTypes from "prop-types";

const FaqItem = (props) => {
  const [isAnswer, setAnswer] = useState(false);

  const toggle = () => {
    setAnswer(!isAnswer);
  };
  const ondelete = () => {};

  return (
    <li className="faq-item">
      <h2 className="question" onClick={toggle}>
        {props.question}
      </h2>
      {isAnswer && <p>{props.answer}</p>}
      <button onClick={ondelete}>Delete</button>
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
@@ -8,6 +8,7 @@ const FaqItem = (props) => {
   const toggle = () => {
     setAnswer(!isAnswer);
   };
+  const ondelete = () => {};

   return (
     <li className="faq-item">
@@ -15,6 +16,7 @@ const FaqItem = (props) => {
         {props.question}
       </h2>
       {isAnswer && <p>{props.answer}</p>}
+      <button onClick={ondelete}>Delete</button>
     </li>
   );
 };
```
````

## Write The `onDelete` Handler

Now that we have our dummy handler ready, we need to add functionality to the handler.
Since the list of FAQ items is managed by our `App` component, we cannot directly remove the item.
Rewrite the `FaqItem` component so that both a unique identifier of the FAQ item and a callback to remove the FAQ item can be passed to this component.
Also complete the `onDelete` handler such that it will call the callback with the correct identifier.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 11-13,29-30
:linenos: true

import { useState } from "react";
import "./FaqItem.css";
import PropTypes from "prop-types";

const FaqItem = (props) => {
  const [isAnswer, setAnswer] = useState(false);

  const toggle = () => {
    setAnswer(!isAnswer);
  };
  const ondelete = () => {
    props.onDelete(props.index);
  };

  return (
    <li className="faq-item">
      <h2 className="question" onClick={toggle}>
        {props.question}
      </h2>
      {isAnswer && <p>{props.answer}</p>}
      <button onClick={ondelete}>Delete</button>
    </li>
  );
};

FaqItem.propTypes = {
  question: PropTypes.string.isRequired,
  answer: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  onDelete: PropTypes.func.isRequired,
};

export default FaqItem;

```

```dpatch
--- a/src/components/FaqItem.jsx
+++ b/src/components/FaqItem.jsx
@@ -8,7 +8,9 @@ const FaqItem = (props) => {
   const toggle = () => {
     setAnswer(!isAnswer);
   };
-  const ondelete = () => {};
+  const ondelete = () => {
+    props.onDelete(props.index);
+  };

   return (
     <li className="faq-item">
@@ -24,6 +26,8 @@ const FaqItem = (props) => {
 FaqItem.propTypes = {
   question: PropTypes.string.isRequired,
   answer: PropTypes.string.isRequired,
+  index: PropTypes.number.isRequired,
+  onDelete: PropTypes.func.isRequired,
 };

 export default FaqItem;
```
````

## Write A Dummy Delete Handler

Now we're ready to change the `App` component to add a dummy `onDelete` handler.
Add the `onDelete` handler to the `App` component, which logs the index of the FAQ item to the console.
Make sure to pass the index and the callback to the `FaqItem` component to wire everything together:

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 17-20,23-30
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

  const onDelete = (index) => {
    console.log(index);
  };

  return (
    <ul>
      {faqList.map((item, index) => (
        <FaqItem
          key={index}
          question={item.question}
          answer={item.answer}
          index={index}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
}

export default App;
```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -14,10 +14,20 @@ function App() {
     },
   ]);

+  const onDelete = (index) => {
+    console.log(index);
+  };
+
   return (
     <ul>
       {faqList.map((item, index) => (
-        <FaqItem key={index} question={item.question} answer={item.answer} />
+        <FaqItem
+          key={index}   
+          question={item.question}
+          answer={item.answer}
+          index={index}
+          onDelete={onDelete}
+        />
       ))}
     </ul>
   );
```
````

## Delete The FAQ Item From The List

The last step is to remove the item from the list.
Write the `onDelete` handler which removes the item from the list and creates the new state.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 1-5
:lineno-start: 17
:linenos: true

  const onDelete = (index) => {
    let faq = [...faqList];
    faq.splice(index, 1);
    setFaqList(faq);
  };
```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -15,7 +15,9 @@ function App() {
   ]);

   const onDelete = (index) => {
-    console.log(index);
+    let faq = [...faqList];
+    faq.splice(index, 1);
+    setFaqList(faq);
   };

   return (

```
````
