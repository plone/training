---
myst:
  html_meta:
    "description": "Add form to add new question and answer."
    "property=og:description": "Add form to add new question and answer."
    "property=og:title": "Use Forms To Add An Item"
    "keywords": "Plone, training, exercise, solution, React"
---

(forms-label)=

# Use Forms To Add An Item

## Add The Form

To be able to add FAQ items to the list, we will start by adding an add form:

```{code-block} jsx
:emphasize-lines: 2,14-23
:lineno-start: 23
:linenos: true

return (
    <div>
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
```

````{dropdown} Differences
:animate: fade-in-slide-down
:icon: question

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -21,17 +21,28 @@ function App() {
   };

   return (
-    <ul>
-      {faqList.map((item, index) => (
-        <FaqItem
-          key={index}
-          question={item.question}
-          answer={item.answer}
-          index={index}
-          onDelete={onDelete}
-        />
-      ))}
-    </ul>
+    <div>
+      <ul>
+        {faqList.map((item, index) => (
+          <FaqItem
+            key={index}
+            question={item.question}
+            answer={item.answer}
+            index={index}
+            onDelete={onDelete}
+          />
+        ))}
+      </ul>
+      <form>
+        <label>
+          Question: <input name="question" type="text" />
+        </label>
+        <label>
+          Answer: <textarea name="answer" />
+        </label>
+        <input type="submit" value="Add" />
+      </form>
+    </div>
   );
 }
```
````

## Manage Field Values In The State

To manage the values of the fields in the form, we will use the state.
Add a question and answer value to the state which contains the values of the inputs.
Add `onChange` handlers to the input and textarea which will change the values in the state when the input changes.
This pattern is called "controlled inputs".

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 17-18,26-32,49-55,58-59
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

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const onDelete = (index) => {
    let faq = [...faqList];
    faq.splice(index, 1);
    setFaqList(faq);
  };

  const onChangeAnswer = (e) => {
    setAnswer(e.target.value);
  };

  const onChangeQuestion = (e) => {
    setQuestion(e.target.value);
  };

  return (
    <div>
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
      <form>
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

export default App;

```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -14,12 +14,23 @@ function App() {
     },
   ]);

+  const [question, setQuestion] = useState("");
+  const [answer, setAnswer] = useState("");
+
   const onDelete = (index) => {
     let faq = [...faqList];
     faq.splice(index, 1);
     setFaqList(faq);
   };

+  const onChangeAnswer = (e) => {
+    setAnswer(e.target.value);
+  };
+
+  const onChangeQuestion = (e) => {
+    setQuestion(e.target.value);
+  };
+
   return (
     <div>
       <ul>
@@ -35,10 +46,17 @@ function App() {
       </ul>
       <form>
         <label>
-          Question: <input name="question" type="text" />
+          Question:{" "}
+          <input
+            name="question"
+            type="text"
+            value={question}
+            onChange={onChangeQuestion}
+          />
         </label>
         <label>
-          Answer: <textarea name="answer" />
+          Answer:{" "}
+          <textarea name="answer" value={answer} onChange={onChangeAnswer} />
         </label>
         <input type="submit" value="Add" />
       </form>

```
````

## Submit Handler

Now that our values are managed in the state, we can write our submit handler.
Write an `onSubmit` handler which reads the values from the state and adds the new FAQ item to the list.
After the item is added, the inputs should also reset to empty values.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

And add this to the body of the function.

```{code-block} jsx
:emphasize-lines: 1-6,21
:lineno-start: 34
:linenos: true

  const onSubmit = (e) => {
    e.preventDefault();
    setFaqList([...faqList, { question, answer }]);
    setQuestion("");
    setAnswer("");
  };

  return (
    <div>
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
```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -31,6 +31,13 @@ function App() {
     setQuestion(e.target.value);
   };

+  const onSubmit = (e) => {
+    e.preventDefault();
+    setFaqList([...faqList, { question, answer }]);
+    setQuestion("");
+    setAnswer("");
+  };
+
   return (
     <div>
       <ul>
@@ -44,7 +51,7 @@ function App() {
           />
         ))}
       </ul>
-      <form>
+      <form onSubmit={onSubmit}>
         <label>
           Question:{" "}
           <input
```
````
