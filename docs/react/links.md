---
myst:
  html_meta:
    "description": "Add links to our App for navigating around the App."
    "property=og:description": "Add links to our App for navigating around the App."
    "property=og:title": "Using Link To Navigate"
    "keywords": "Plone, training, exercise, solution, React, link"
---

(links-label)=

# Using Links To Navigate

Links are used to navigate between pages in React Router.
This will make sure the browser doesn't do a full refresh, but just changes the route.
We will add a link to the `FaqItem` component so that we can go to the `FaqItemView` view.

```{code-block} jsx
:emphasize-lines: 1
:lineno-start: 4
:linenos:

import { Link } from "react-router-dom";
```

```{code-block} jsx
:emphasize-lines: 1
:lineno-start: 74
:linenos: true

<Link to={`/faq/${props.index}`}>View</Link>
```

The full listing of the `FaqItem` component is as follows:

```{code-block} jsx
:emphasize-lines: 4,74
:linenos: true

import { useState } from "react";
import { useDispatch } from "react-redux";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

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
          <Link to={`/faq/${props.index}`}>View</Link>
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

````{dropdown} Differences
:animate: fade-in-slide-down
:icon: question

```dpatch
--- a/src/components/FaqItem.jsx
+++ b/src/components/FaqItem.jsx
@@ -1,6 +1,7 @@
 import { useState } from "react";
 import { useDispatch } from "react-redux";
 import PropTypes from "prop-types";
+import { Link } from "react-router-dom";

 import { editFaqItem, deleteFaqItem } from "../actions";
 import "./FaqItem.css";
@@ -70,6 +71,7 @@ const FaqItem = (props) => {
           {isAnswer && <p>{props.answer}</p>}
           <button onClick={ondelete}>Delete</button>
           <button onClick={onEdit}>Edit</button>
+          <Link to={`/faq/${props.index}`}>View</Link>
         </li>
       )}
     </>
```
````
