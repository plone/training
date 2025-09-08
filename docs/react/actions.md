---
myst:
  html_meta:
    "description": "Using actions to manipulate the store and accessing the data from the store."
    "property=og:description": "Using actions to manipulate the store and accessing the data from the store."
    "property=og:title": "Use Actions To Manipulate The Store"
    "keywords": "Plone, training, exercise, solution, React, Redux"
---

(actions-label)=

# Use Actions To Manipulate The Store

## Wiring The Store

Now that we have our store ready, it's time to connect the store to our code and remove all the unneeded functionality.
The first step is to factor out the `Faq` component into a separate file called {file}`components/Faq.jsx`.
It is almost an exact copy of {file}`App.js`:

```{code-block} jsx
:emphasize-lines: 4,80
:linenos: true

import { useState } from "react";
import FaqItem from "./FaqItem";

function Faq() {
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

export default Faq;
```

Next we will create an `App` component with just the store and a reference to our newly created `Faq` component:

```{code-block} jsx
:emphasize-lines: 2-3,5-6,10,15-17
:linenos:

import { Provider } from "react-redux";
import { createStore } from "redux";

import rootReducer from "./reducers";
import Faq from "./components/Faq";

import "./App.css";

const store = createStore(rootReducer);

const App = () => {
  return (
    <Provider store={store}>
      <Faq />
    </Provider>
  );
};

export default App;
```

````{dropdown} Differences
:animate: fade-in-slide-down
:icon: question

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -1,81 +1,19 @@
-import { useState } from "react";
-import "./App.css";
-import FaqItem from "./components/FaqItem";
-
-function App() {
-  const [faqList, setFaqList] = useState([
-    {
-      question: "What does the Plone Foundation do?",
-      answer: "The mission of the Plone Foundation is to protect and...",
-    },
-    {
-      question: "Why does Plone need a Foundation?",
-      answer: "Plone has reached critical mass, with enterprise...",
-    },
-  ]);
-
-  const [question, setQuestion] = useState("");
-  const [answer, setAnswer] = useState("");
+import { Provider } from "react-redux";
+import { createStore } from "redux";

-  const onDelete = (index) => {
-    let faq = [...faqList];
-    faq.splice(index, 1);
-    setFaqList(faq);
-  };
+import rootReducer from "./reducers";
+import Faq from "./components/Faq";

-  const onChangeAnswer = (e) => {
-    setAnswer(e.target.value);
-  };
-
-  const onChangeQuestion = (e) => {
-    setQuestion(e.target.value);
-  };
-
-  const onEdit = (index, question, answer) => {
-    const faq = [...faqList];
-    faq[index] = { question, answer };
-    setFaqList(faq);
-  };
+import "./App.css";

-  const onSubmit = (e) => {
-    e.preventDefault();
-    setFaqList([...faqList, { question, answer }]);
-    setQuestion("");
-    setAnswer("");
-  };
+const store = createStore(rootReducer);

+const App = () => {
   return (
-    <div>
-      <ul>
-        {faqList.map((item, index) => (
-          <FaqItem
-            key={index}
-            question={item.question}
-            answer={item.answer}
-            index={index}
-            onDelete={onDelete}
-            onEdit={onEdit}
-          />
-        ))}
-      </ul>
-      <form onSubmit={onSubmit}>
-        <label>
-          Question:{" "}
-          <input
-            name="question"
-            type="text"
-            value={question}
-            onChange={onChangeQuestion}
-          />
-        </label>
-        <label>
-          Answer:{" "}
-          <textarea name="answer" value={answer} onChange={onChangeAnswer} />
-        </label>
-        <input type="submit" value="Add" />
-      </form>
-    </div>
+    <Provider store={store}>
+      <Faq />
+    </Provider>
   );
-}
+};

 export default App;
```
````

## Use The Data From The Store

Now that we have our store wired, we can start using the store data instead of our local state.
We will use the hook `useSelector` for extracting the data from the store, and `useDispatch` for dispatching the action which is needed by the component.

```{code-block} jsx
:emphasize-lines: 1-2
:lineno-start: 2
:linenos: true

import { useSelector,useDispatch } from "react-redux";
import { addFaqItem } from "../actions";
```


We can remove all the edit and delete references, since those will be handled by the `FaqItem` to clean up our code.
We will also change the `onSubmit` handler to use the  `addFaqItem` action.
The result will be as follows:

```{code-block} jsx
:emphasize-lines: 2-5,8-9,25
:linenos: true

import { useState } from "react";
import { useSelector, useDispatch } from "react-redux";

import { addFaqItem } from "../actions";
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
--- a/src/components/Faq.jsx
+++ b/src/components/Faq.jsx
@@ -1,27 +1,16 @@
 import { useState } from "react";
+import { useSelector, useDispatch } from "react-redux";
+
+import { addFaqItem } from "../actions";
 import FaqItem from "./FaqItem";

 function Faq() {
-  const [faqList, setFaqList] = useState([
-    {
-      question: "What does the Plone Foundation do?",
-      answer: "The mission of the Plone Foundation is to protect and...",
-    },
-    {
-      question: "Why does Plone need a Foundation?",
-      answer: "Plone has reached critical mass, with enterprise...",
-    },
-  ]);
+  const faqList = useSelector((state) => state.faq);
+  const dispatch = useDispatch();

   const [question, setQuestion] = useState("");
   const [answer, setAnswer] = useState("");

-  const onDelete = (index) => {
-    let faq = [...faqList];
-    faq.splice(index, 1);
-    setFaqList(faq);
-  };
-
   const onChangeAnswer = (e) => {
     setAnswer(e.target.value);
   };
@@ -30,16 +19,10 @@ function Faq() {
     setQuestion(e.target.value);
   };

-  const onEdit = (index, question, answer) => {
-    const faq = [...faqList];
-    faq[index] = { question, answer };
-    setFaqList(faq);
-  };
-
   const onSubmit = (e) => {
     e.preventDefault();
-    setFaqList([...faqList, { question, answer }]);
     setQuestion("");
+    dispatch(addFaqItem(question, answer));
     setAnswer("");
   };

@@ -51,8 +34,6 @@ function Faq() {
             question={item.question}
             answer={item.answer}
             index={index}
-            onDelete={onDelete}
-            onEdit={onEdit}
           />
         ))}
       </ul>
```
````

## Exercise

Now that we factored out the edit and delete actions from the `Faq` component, update the `FaqItem` component to call the actions we created for our store.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:emphasize-lines: 2,5,13,19,38
:linenos: true

import { useState } from "react";
import { useDispatch } from "react-redux";
import PropTypes from "prop-types";

import { editFaqItem, deleteFaqItem } from "../actions";
import "./FaqItem.css";

const FaqItem = (props) => {
  const [isAnswer, setAnswer] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setQuestionAnswer] = useState("");
  const dispatch = useDispatch();

  const toggle = () => {
    setAnswer(!isAnswer);
  };
  const ondelete = () => {
    dispatch(deleteFaqItem(props.index));
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
    dispatch(editFaqItem(props.index, question, answer));
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
};

export default FaqItem;
```

```dpatch
--- a/src/components/FaqItem.jsx
+++ b/src/components/FaqItem.jsx
@@ -1,18 +1,22 @@
 import { useState } from "react";
-import "./FaqItem.css";
+import { useDispatch } from "react-redux";
 import PropTypes from "prop-types";

+import { editFaqItem, deleteFaqItem } from "../actions";
+import "./FaqItem.css";
+
 const FaqItem = (props) => {
   const [isAnswer, setAnswer] = useState(false);
   const [isEditMode, setIsEditMode] = useState(false);
   const [question, setQuestion] = useState("");
   const [answer, setQuestionAnswer] = useState("");
+  const dispatch = useDispatch();

   const toggle = () => {
     setAnswer(!isAnswer);
   };
   const ondelete = () => {
-    props.onDelete(props.index);
+    dispatch(deleteFaqItem(props.index));
   };

   const onEdit = () => {
@@ -31,7 +35,7 @@ const FaqItem = (props) => {
   const onSave = (e) => {
     e.preventDefault();
     setIsEditMode(false);
-    props.onEdit(props.index, question, answer);
+    dispatch(editFaqItem(props.index, question, answer));
   };

   return (
@@ -76,8 +80,6 @@ FaqItem.propTypes = {
   question: PropTypes.string.isRequired,
   answer: PropTypes.string.isRequired,
   index: PropTypes.number.isRequired,
-  onDelete: PropTypes.func.isRequired,
-  onEdit: PropTypes.func.isRequired,
 };
```
````
