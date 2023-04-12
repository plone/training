---
myst:
  html_meta:
    "description": "Redirecting the user from the one route to another route."
    "property=og:description": "Redirecting the user from the one route to another route."
    "property=og:title": "Navigate Using Redirects"
    "keywords": "Plone, training, exercise, solution, React"
---

(redirects-label)=

# Navigate Using Redirects

If we want to navigate programmatically, for example after submitting a form, we have to use a different method.
In this example we will create a back button in the `FaqItemView` to return to the overview.
First we will create the button:

```{code-block} jsx
:emphasize-lines: 1
:lineno-start: 21
:linenos: true

<button onClick={onBack}>Back</button>
```

Then we will add the handler to handle the back event.
This event will make use of the `useHistory` hook provide by the `react-router-dom`.
Once you call this hook, it will give you access to the history instance that you may use to navigate.
It has a push method which will push to the new route.

```{code-block} jsx
:emphasize-lines: 1-3
:lineno-start: 14
:linenos: true

  const onBack = () => {
    history.push("/");
  };
```

The full listing of our new `FaqItemView` will look as follows:

```{code-block} jsx
:emphasize-lines: 4,8,14-17,26
:linenos: true

import { useEffect } from "react";
import { getFaqItems } from "../actions";
import { useSelector, useDispatch } from "react-redux";
import { useParams, useHistory } from "react-router-dom";

const FaqItemView = () => {
  const { index } = useParams();
  let history = useHistory();
  const dispatch = useDispatch();
  const faqItem = useSelector((state) =>
    state.faq.length ? state.faq[index] : {}
  );

  const onBack = () => {
    history.push("/");
  };

  useEffect(() => {
    dispatch(getFaqItems());
  }, [dispatch]);

  return (
    <div>
      <h2 className="question">{faqItem.question}</h2>
      <p>{faqItem.answer}</p>
      <button onClick={onBack}>Back</button>
    </div>
  );
};

export default FaqItemView;

```

````{dropdown} Differences
:animate: fade-in-slide-down
:icon: question

```dpatch
--- a/src/components/FaqItemView.jsx
+++ b/src/components/FaqItemView.jsx
@@ -1,15 +1,20 @@
 import { useEffect } from "react";
 import { getFaqItems } from "../actions";
 import { useSelector, useDispatch } from "react-redux";
-import { useParams } from "react-router-dom";
+import { useParams, useHistory } from "react-router-dom";

 const FaqItemView = () => {
   const { index } = useParams();
+  let history = useHistory();
   const dispatch = useDispatch();
   const faqItem = useSelector((state) =>
     state.faq.length ? state.faq[index] : {}
   );

+  const onBack = () => {
+    history.push("/");
+  };
+
   useEffect(() => {
     dispatch(getFaqItems());
   }, [dispatch]);
@@ -18,6 +23,7 @@ const FaqItemView = () => {
     <div>
       <h2 className="question">{faqItem.question}</h2>
       <p>{faqItem.answer}</p>
+      <button onClick={onBack}>Back</button>
     </div>
   );
 };
```
````
