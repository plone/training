.. _component-label:

======================
Create React Component
======================

Generated App Code
==================

The following code is generated. It contains a class which is extended from
a React component. The class has a :file:`render` method which contains JSX to
render the view.

::

    import React, { Component } from 'react';
    import logo from './logo.svg';
    import './App.css';

    class App extends Component {
      render() {
        return (
          <div className="App">
            <header className="App-header">
              <img src={logo} className="App-logo" alt="logo" />
              <h1 className="App-title">Welcome to React</h1>
            </header>
            <p className="App-intro">
              To get started, edit <code>src/App.js</code> and save to reload.
            </p>
          </div>
        );
      }
    }

    export default App;

Exercise
========

Change the :file:`App.js` file to show two FAQ items with the following content:

* Question 1: What does the Plone Foundation do?
* Answer 1: The mission of the Plone Foundation is to protect and promote Plone. The Foundation provides marketing assistance, awareness, and evangelism assistance to the Plone community. The Foundation also assists with development funding and coordination of funding for large feature implementations. In this way, our role is similar to the role of the Apache Software Foundation and its relationship with the Apache Project.
* Question 2: Why does Plone need a Foundation?
* Answer 2: Plone has reached critical mass, with enterprise implementations and worldwide usage. The Foundation is able to speak for Plone, and provide strong and consistent advocacy for both the project and the community. The Plone Foundation also helps ensure a level playing field, to preserve what is good about Plone as new participants arrive.

Use an unordered list with an item for each faq entry containing an :file:`h2` tag for the question and a :file:`p` tag for the answer. Remove all other boiler plate code including styling.

..  admonition:: Solution
    :class: toggle

    ::

        import React, { Component } from "react";

        class App extends Component {
          render() {
            return (
              <ul>
                <li>
                  <h2>What does the Plone Foundation do?</h2>
                  <p>
                    The mission of the Plone Foundation is to protect and promote Plone.
                    The Foundation provides marketing assistance, awareness, and
                    evangelism assistance to the Plone community. The Foundation also
                    assists with development funding and coordination of funding for
                    large feature implementations. In this way, our role is similar to
                    the role of the Apache Software Foundation and its relationship with
                    the Apache Project.
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
        }

        export default App;
