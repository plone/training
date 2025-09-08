---
myst:
  html_meta:
    "description": "Create a react component with a question and answer."
    "property=og:description": "Create a react component with question and answer."
    "property=og:title": " Create React Component"
    "keywords": "Plone, trainings, SEO, create-react-app, React, component, exercise, solution"
---

(component-label)=

# Create React Component

## Generated App Code

The following code is generated in the file {file}`src/App.js`.
It contains a function which is a React component.
A React component is a small view which will render some HTML and can have additional behavior.
The function has a `return` statement which contains JSX to render the view.
JSX is inline HTML which will be rendered as HTML in the view.

```{code-block} jsx
:linenos:

import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
```

## Exercise

Change the {file}`App.js` file to show two FAQ items with the following content:

- Question 1: What does the Plone Foundation do?
- Answer 1: The mission of the Plone Foundation is to protect and promote Plone. The Foundation provides marketing assistance, awareness, and evangelism assistance to the Plone community. The Foundation also assists with development funding and coordination of funding for large feature implementations. In this way, our role is similar to the role of the Apache Software Foundation and its relationship with the Apache Project.
- Question 2: Why does Plone need a Foundation?
- Answer 2: Plone has reached critical mass, with enterprise implementations and worldwide usage. The Foundation is able to speak for Plone, and provide strong and consistent advocacy for both the project and the community. The Plone Foundation also helps ensure a level playing field, to preserve what is good about Plone as new participants arrive.

Use an unordered list with an item for each FAQ entry containing an `h2` tag for the question, and a `p` tag for the answer.
Remove all other boilerplate code including styling.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} jsx
:linenos:

function App() {
  return (
    <ul>
      <li>
        <h2>What does the Plone Foundation do?</h2>
        <p>
          The mission of the Plone Foundation is to protect and promote Plone.
          The Foundation provides marketing assistance, awareness, and
          evangelism assistance to the Plone community. The Foundation also
          assists with development funding and coordination of funding for large
          feature implementations. In this way, our role is similar to the role
          of the Apache Software Foundation and its relationship with the Apache
          Project.
        </p>
      </li>
      <li>
        <h2>Why does Plone need a Foundation?</h2>
        <p>
          Plone has reached critical mass, with enterprise implementations and
          worldwide usage. The Foundation is able to speak for Plone, and
          provide strong and consistent advocacy for both the project and the
          community. The Plone Foundation also helps ensure a level playing
          field, to preserve what is good about Plone as new participants
          arrive.
        </p>
      </li>
    </ul>
  );
}

export default App;
```

```dpatch
--- a/src/App.js
+++ b/src/App.js
@@ -1,24 +1,32 @@
-import logo from './logo.svg';
-import './App.css';

function App() {
  return (
-    <div className="App">
-      <header className="App-header">
-        <img src={logo} className="App-logo" alt="logo" />
+    <ul>
+      <li>
+        <h2>What does the Plone Foundation do?</h2>
        <p>
-          Edit <code>src/App.js</code> and save to reload.
+          The mission of the Plone Foundation is to protect and promote Plone.
+          The Foundation provides marketing assistance, awareness, and
+          evangelism assistance to the Plone community. The Foundation also
+          assists with development funding and coordination of funding for large
+          feature implementations. In this way, our role is similar to the role
+          of the Apache Software Foundation and its relationship with the Apache
+          Project.
        </p>
-        <a
-          className="App-link"
-          href="https://reactjs.org"
-          target="_blank"
-          rel="noopener noreferrer"
-        >
-          Learn React
-        </a>
-      </header>
-    </div>
+      </li>
+      <li>
+        <h2>Why does Plone need a Foundation?</h2>
+        <p>
+          Plone has reached critical mass, with enterprise implementations and
+          worldwide usage. The Foundation is able to speak for Plone, and
+          provide strong and consistent advocacy for both the project and the
+          community. The Plone Foundation also helps ensure a level playing
+          field, to preserve what is good about Plone as new participants
+          arrive.
+        </p>
+      </li>
+    </ul>
  );
}
```
````

## Extra Information

If you're unfamiliar with React/ES6, here are some short pointers to the default `create-react-app` boilerplate.

JSX is a special format where it seems you are writing html code, but before execution the source is first transformed to valid JavaScript.
The `<div>`, `<ul>`, `<p>`, and other tags in this code are first translated into valid JavaScript code using the function `React.CreateElement`.
`create-react-app` automatically adds this preprocessing of JSX.

The last line of our `App` component is marked as the default export for this JavaScript file.
Check out [ES6 module documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules).

Note that React allows you to import and treat images and CSS as direct resources.
The curly braces used for the `<img src=>` attribute signal to JSX that what follows is executable JavaScript.
