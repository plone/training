---
myst:
  html_meta:
    "description": "Add the Edit mode so that the user can edit the question and answer list."
    "property=og:description": "Add the Edit mode so that the user can edit the question and answer list."
    "property=og:title": "Use Initial Form Data To Edit An Item"
    "keywords": "Plone, training, exercise, solution, React"
---

(initial-form-data-label)=

# Use Initial Form Data To Edit An Item

## Two Modes For The FAQ Item

We will use inline editing to edit an item.
Create a button to switch to "edit" mode.
This mode should be set in the state.
Change the render method to show a form (similar to the "add" form) in "edit" mode, and the view we currently have in the "view" mode.
The `onSave` handler can be a dummy handler for now.
First we will focus on the two modes.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 7,16-23,26-40,48,50-51
:linenos: true

import { useState } from "react";
import "./FaqItem.css";
import PropTypes from "prop-types";

const FaqItem = (props) => {
  const [isAnswer, setAnswer] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);

  const toggle = () => {
    setAnswer(!isAnswer);
  };
  const ondelete = () => {
    props.onDelete(props.index);
  };

  const onEdit = () => {
    setIsEditMode(true);
  };

  const onSave = (e) => {
    e.preventDefault();
    setIsEditMode(false);
  };

  return (
    <>
      {isEditMode ? (
        <li className="faq-item">
          <form onSubmit={onSave}>
            <label>
              Question:
              <input name="question" />
            </label>
            <label>
              Answer:
              <textarea name="answer" />
            </label>
            <input type="submit" value="Save" />
          </form>
        </li>
      ) : (
        <li className="faq-item">
          <h2 className="question" onClick={toggle}>
            {props.question}
          </h2>
          {isAnswer && <p>{props.answer}</p>}
          <button onClick={ondelete}>Delete</button>
          <button onClick={onEdit}>Edit</button>
        </li>
      )}
    </>
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
@@ -4,6 +4,7 @@ import PropTypes from "prop-types";

 const FaqItem = (props) => {
   const [isAnswer, setAnswer] = useState(false);
+  const [isEditMode, setIsEditMode] = useState(false);

   const toggle = () => {
     setAnswer(!isAnswer);
@@ -12,14 +13,42 @@ const FaqItem = (props) => {
     props.onDelete(props.index);
   };

+  const onEdit = () => {
+    setIsEditMode(true);
+  };
+
+  const onSave = (e) => {
+    e.preventDefault();
+    setIsEditMode(false);
+  };
+
   return (
-    <li className="faq-item">
-      <h2 className="question" onClick={toggle}>
-        {props.question}
-      </h2>
-      {isAnswer && <p>{props.answer}</p>}
-      <button onClick={ondelete}>Delete</button>
-    </li>
+    <>
+      {isEditMode ? (
+        <li className="faq-item">
+          <form onSubmit={onSave}>
+            <label>
+              Question:
+              <input name="question" />
+            </label>
+            <label>
+              Answer:
+              <textarea name="answer" />
+            </label>
+            <input type="submit" value="Save" />
+          </form>
+        </li>
+      ) : (
+        <li className="faq-item">
+          <h2 className="question" onClick={toggle}>
+            {props.question}
+          </h2>
+          {isAnswer && <p>{props.answer}</p>}
+          <button onClick={ondelete}>Delete</button>
+          <button onClick={onEdit}>Edit</button>
+        </li>
+      )}
+    </>
   );
 };
```
````

## Wiring Everything Together

Create a controlled form like the add form, and pass an `onEdit` handler to the `FaqItem` component, like we did with the `onDelete`.

````{dropdown} FaqItem.jsx
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 8-9,20-28,34,44-48,52-56,80
:linenos: true

import { useState } from "react";
import "./FaqItem.css";
import PropTypes from "prop-types";

const FaqItem = (props) => {
  const [isAnswer, setAnswer] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setQuestionAnswer] = useState("");

  const toggle = () => {
    setAnswer(!isAnswer);
  };
  const ondelete = () => {
    props.onDelete(props.index);
  };

  const onEdit = () => {
    setIsEditMode(true);
    setQuestionAnswer(props.answer);
    setQuestion(props.question);
  };

  const onChangeAnswer = (e) => {
    setQuestionAnswer(e.target.value);
  };
  const onChangeQuestion = (e) => {
    setQuestion(e.target.value);
  };

  const onSave = (e) => {
    e.preventDefault();
    setIsEditMode(false);
    props.onEdit(props.index, question, answer);
  };

  return (
    <>
      {isEditMode ? (
        <li className="faq-item">
          <form onSubmit={onSave}>
            <label>
              Question:
              <input
                name="question"
                value={question}
                onChange={onChangeQuestion}
              />
            </label>
            <label>
              Answer:
              <textarea
                name="answer"
                value={answer}
                onChange={onChangeAnswer}
              />
            </label>
            <input type="submit" value="Save" />
          </form>
        </li>
      ) : (
        <li className="faq-item">
          <h2 className="question" onClick={toggle}>
            {props.question}
          </h2>
          {isAnswer && <p>{props.answer}</p>}
          <button onClick={ondelete}>Delete</button>
          <button onClick={onEdit}>Edit</button>
        </li>
      )}
    </>
  );
};

FaqItem.propTypes = {
  question: PropTypes.string.isRequired,
  answer: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  onDelete: PropTypes.func.isRequired,
  onEdit: PropTypes.func.isRequired,
};

export default FaqItem;

```

```dpatch
--- a/src/components/FaqItem.jsx
+++ b/src/components/FaqItem.jsx
@@ -5,6 +5,8 @@ import PropTypes from "prop-types";
 const FaqItem = (props) => {
   const [isAnswer, setAnswer] = useState(false);
   const [isEditMode, setIsEditMode] = useState(false);
+  const [question, setQuestion] = useState("");
+  const [answer, setQuestionAnswer] = useState("");

   const toggle = () => {
     setAnswer(!isAnswer);
@@ -15,11 +17,21 @@ const FaqItem = (props) => {

   const onEdit = () => {
     setIsEditMode(true);
+    setQuestionAnswer(props.answer);
+    setQuestion(props.question);
+  };
+
+  const onChangeAnswer = (e) => {
+    setQuestionAnswer(e.target.value);
+  };
+  const onChangeQuestion = (e) => {
+    setQuestion(e.target.value);
   };

   const onSave = (e) => {
     e.preventDefault();
     setIsEditMode(false);
+    props.onEdit(props.index, question, answer);
   };

   return (
@@ -29,11 +41,19 @@ const FaqItem = (props) => {
           <form onSubmit={onSave}>
             <label>
               Question:
-              <input name="question" />
+              <input
+                name="question"
+                value={question}
+                onChange={onChangeQuestion}
+              />
             </label>
             <label>
               Answer:
-              <textarea name="answer" />
+              <textarea
+                name="answer"
+                value={answer}
+                onChange={onChangeAnswer}
+              />
             </label>
             <input type="submit" value="Save" />
           </form>
@@ -57,6 +77,7 @@ FaqItem.propTypes = {
   answer: PropTypes.string.isRequired,
   index: PropTypes.number.isRequired,
   onDelete: PropTypes.func.isRequired,
+  onEdit: PropTypes.func.isRequired,
 };

 export default FaqItem;
```
````

````{dropdown} App.js
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 34-38,57
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

  const onEdit = (index, question, answer) => {
    const faq = [...faqList];
    faq[index] = { question, answer };
    setFaqList(faq);
  };

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
            onEdit={onEdit}
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

export default App;

```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -31,6 +31,12 @@ function App() {
     setQuestion(e.target.value);
   };

+  const onEdit = (index, question, answer) => {
+    const faq = [...faqList];
+    faq[index] = { question, answer };
+    setFaqList(faq);
+  };
+
   const onSubmit = (e) => {
     e.preventDefault();
     setFaqList([...faqList, { question, answer }]);
@@ -48,6 +54,7 @@ function App() {
             answer={item.answer}
             index={index}
             onDelete={onDelete}
+            onEdit={onEdit}
           />
         ))}
       </ul>
```
````
