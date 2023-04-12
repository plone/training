---
myst:
  html_meta:
    "description": "An introduction to useEffect hook. Using useEffect for doing the side effects for the component. In this case we are fetching the initial data."
    "property=og:description": "An introduction to useEffect hook. Using useEffect for doing the side effects for the component. In this case we are fetching the initial data."
    "property=og:title": "useEffect Hook"
    "keywords": "Plone, training, SEO, React, hook, exercise, solution"
---

(useEffect-label)=

# useEffect Hook

The `useEffect` hook is called on specific external events.
For example the `useEffect` hook is called after the component is rendered.
We can use this hook to do additional calls.
In our case we want to fetch the initial data from the backend.

```{code-block} jsx
:emphasize-lines: 1-3
:lineno-start: 29
:linenos: true

  useEffect(() => {
    dispatch(getFaqItems());
  }, [dispatch]);
```

The `getFaqItems` method is called using the dispatch hook.
The full `Faq` component will now look like this:

```{code-block} jsx
:emphasize-lines: 1,4, 29-31
:linenos: true

import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";

import { addFaqItem, getFaqItems } from "../actions";
import FaqItem from "./FaqItem";

function Faq() {
  const faqList = useSelector((state) => state.faq);
  const dispatch = useDispatch();

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const onChangeAnswer = (e) => {
    setAnswer(e.target.value);
  };

  const onChangeQuestion = (e) => {
    setQuestion(e.target.value);
  };

  const onSubmit = (e) => {
    e.preventDefault();
    setQuestion("");
    dispatch(addFaqItem(question, answer));
    setAnswer("");
  };

  useEffect(() => {
    dispatch(getFaqItems());
  }, [dispatch]);

  return (
    <div>
      <ul>
        {faqList.map((item, index) => (
          <FaqItem
            key={index}
            question={item.question}
            answer={item.answer}
            index={index}
          />
        ))}
      </ul>
      <form onSubmit={onSubmit}>
        <label>
          Question:{" "}
          <input
            name="question"
            type="text"
            value={question}
            onChange={onChangeQuestion}
          />
        </label>
        <label>
          Answer:{" "}
          <textarea name="answer" value={answer} onChange={onChangeAnswer} />
        </label>
        <input type="submit" value="Add" />
      </form>
    </div>
  );
}

export default Faq;
```

````{dropdown} Differences
:animate: fade-in-slide-down
:icon: question

```dpatch
-import { useState } from "react";
+import { useState, useEffect } from "react";
 import { useSelector, useDispatch } from "react-redux";

-import { addFaqItem } from "../actions";
+import { addFaqItem, getFaqItems } from "../actions";
 import FaqItem from "./FaqItem";

 function Faq() {
@@ -26,6 +26,10 @@ function Faq() {
     setAnswer("");
   };

+  useEffect(() => {
+    dispatch(getFaqItems());
+  }, [dispatch]);
+
   return (
     <div>
       <ul>
```
````
