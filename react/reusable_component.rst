.. _reusable_component-label:

===============================
Convert To A Reusable Component
===============================

Create A Reusable component
===========================

In order to reuse the markup of a faq item we will split up the code. The app
component will contain just the data of the faq item and will render a newly
created sub component called :file:`FaqItem`. The data is passed to the sub
component using properties. The :file:`App.js` code will be changed to:

::

    import React, { Component } from "react";
    import FaqItem from "./components/FaqItem";
    import "./App.css";

    class App extends Component {
      render() {
        return (
          <ul>
            <FaqItem
              question="What does the Plone Foundation do?"
              answer="
                The mission of the Plone Foundation is to protect and promote Plone.
                The Foundation provides marketing assistance, awareness, and
                evangelism assistance to the Plone community. The Foundation also
                assists with development funding and coordination of funding for
                large feature implementations. In this way, our role is similar to
                the role of the Apache Software Foundation and its relationship with
                the Apache Project."
            />
            <FaqItem
              question="Why does Plone need a Foundation?"
              answer="
                Plone has reached critical mass, with enterprise implementations and
                worldwide usage. The Foundation is able to speak for Plone, and
                provide strong and consistent advocacy for both the project and the
                community. The Plone Foundation also helps ensure a level playing
                field, to preserve what is good about Plone as new participants
                arrive."
            />
          </ul>
        );
      }
    }

    export default App;


Exercise
========

Create the :file:`FaqItem` component which renders the same output. Take into
account best practices like property validation.

..  admonition:: Solution
    :class: toggle

    ::

        import React, { Component } from "react";
        import PropTypes from "prop-types";
        import "./FaqItem.css";

        class FaqItem extends Component {
          static propTypes = {
            question: PropTypes.string.isRequired,
            answer: PropTypes.string.isRequired
          };

          render() {
            return (
              <li className="faq-item">
                <h2 className="question">{this.props.question}</h2>
                <p>{this.props.answer}</p>
              </li>
            );
          }
        }

        export default FaqItem;
