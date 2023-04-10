---
myst:
  html_meta:
    "description": "Add event handlers to show or hide the answer in FaqItem component."
    "property=og:description": "Add event handlers to show or hide the answer in FaqItem component."
    "property=og:title": "Use Event Handlers"
    "keywords": "Plone, training, exercise, solution, React"
---

(event-handlers-label)=

# Use Event Handlers

## Toggle Function

To show or hide the answer, we will add a toggle function to the component {file}`FaqItem.jsx`.

## Exercise

Write the toggle handler which will toggle the `isAnswer` state variable and set the new state using the `setAnswer` function:

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 1-3
:lineno-start: 8
:linenos: true

  const toggle = () => {
    setAnswer(!isAnswer);
  };
```
````

## Click Handler

To call the newly created `toggle` function, we will add an `onClick` handler to the question:

```{code-block} jsx
:emphasize-lines: 3-5
:lineno-start: 12
:linenos: true

  return (
    <li className="faq-item">
      <h2 className="question" onClick={toggle}>
        {props.question}
      </h2>
      {isAnswer && <p>{props.answer}</p>}
    </li>
  );
```

````{dropdown} Differences
:animate: fade-in-slide-down
:icon: question

{file}`FaqItem.jsx`

```dpatch
--- a/src/components/FaqItem.jsx
+++ b/src/components/FaqItem.jsx
@@ -4,9 +4,16 @@ import PropTypes from "prop-types";

 const FaqItem = (props) => {
   const [isAnswer, setAnswer] = useState(false);
+
+  const toggle = () => {
+    setAnswer(!isAnswer);
+  };
+
   return (
     <li className="faq-item">
-      <h2 className="question">{props.question}</h2>
+      <h2 className="question" onClick={toggle}>
+        {props.question}
+      </h2>
       {isAnswer && <p>{props.answer}</p>}
     </li>
   );
```

```{code-block} jsx
:linenos:

import { useState } from "react";
import "./FaqItem.css";
import PropTypes from "prop-types";

const FaqItem = (props) => {
  const [isAnswer, setAnswer] = useState(false);

  const toggle = () => {
    setAnswer(!isAnswer);
  };

  return (
    <li className="faq-item">
      <h2 className="question" onClick={toggle}>
        {props.question}
      </h2>
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
````
