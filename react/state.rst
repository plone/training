.. _state-label:

==================================
How To Use State In Your Component
==================================

Store Questions And Answers In The State
========================================

To manipulate the FAQ later on we will move all the data to the state of the component.
The state of the component is the local state of that specific component.
When the state changes the render method is called again.
In the constructor of the class we can initialize the state.

.. code-block:: jsx
    :linenos: 
    :emphasize-lines: 6-20,25-27

    import React, { Component } from "react";
    import FaqItem from "./components/FaqItem";
    import "./App.css";

    class App extends Component {
      constructor(props) {
        super(props);
        this.state = {
          faq: [
            {
              question: "What does the Plone Foundation do?",
              answer: "The mission of the Plone Foundation is to protect and..."
            },
            {
              question: "Why does Plone need a Foundation?",
              answer: "Plone has reached critical mass, with enterprise..."
            }
          ]
        };
      }

      render() {
        return (
          <ul>
            {this.state.faq.map(item => (
              <FaqItem question={item.question} answer={item.answer} />
            ))}
          </ul>
        );
      }
    }

    export default App;



..  admonition:: Differences
    :class: toggle

    .. code-block:: dpatch

        --- a/src/App.js
        +++ b/src/App.js
        @@ -3,30 +3,28 @@ import FaqItem from "./components/FaqItem";
        import "./App.css";

        class App extends Component {
        +  constructor(props) {
        +    super(props);
        +    this.state = {
        +      faq: [
        +        {
        +          question: "What does the Plone Foundation do?",
        +          answer: "The mission of the Plone Foundation is to protect and..."
        +        },
        +        {
        +          question: "Why does Plone need a Foundation?",
        +          answer: "Plone has reached critical mass, with enterprise..."
        +        }
        +      ]
        +    };
        +  }
        +
          render() {
            return (
              <ul>
        -        <FaqItem
        -          question="What does the Plone Foundation do?"
        -          answer="
        -            The mission of the Plone Foundation is to protect and promote Plone.
        -            The Foundation provides marketing assistance, awareness, and
        -            evangelism assistance to the Plone community. The Foundation also
        -            assists with development funding and coordination of funding for
        -            large feature implementations. In this way, our role is similar to
        -            the role of the Apache Software Foundation and its relationship with
        -            the Apache Project."
        -        />
        -        <FaqItem
        -          question="Why does Plone need a Foundation?"
        -          answer="
        -            Plone has reached critical mass, with enterprise implementations and
        -            worldwide usage. The Foundation is able to speak for Plone, and
        -            provide strong and consistent advocacy for both the project and the
        -            community. The Plone Foundation also helps ensure a level playing
        -            field, to preserve what is good about Plone as new participants
        -            arrive."
        -        />
        +        {this.state.faq.map(item => (
        +          <FaqItem question={item.question} answer={item.answer} />
        +        ))}
              </ul>
            );
          }



Exercise
========

To save space in the view we want to be able to show and hide the answer when you click on the question.
Add a state variable to the :file:`FaqItem` component which keeps the state of the answer being shown or not
and adjust the render method to show or hide the answer.

..  admonition:: Solution
    :class: toggle

    .. code-block:: jsx
        :linenos: 
        :emphasize-lines: 11-16,22

        import React, { Component } from "react";
        import PropTypes from "prop-types";
        import "./FaqItem.css";

        class FaqItem extends Component {
          static propTypes = {
            question: PropTypes.string.isRequired,
            answer: PropTypes.string.isRequired
          };

          constructor(props) {
            super(props);
            this.state = {
              show: false
            };
          }

          render() {
            return (
              <li className="faq-item">
                <h2 className="question">{this.props.question}</h2>
                {this.state.show && <p>{this.props.answer}</p>}
              </li>
            );
          }
        }

        export default FaqItem;


    .. code-block:: dpatch

        --- a/src/components/FaqItem.jsx
        +++ b/src/components/FaqItem.jsx
        @@ -1,6 +1,5 @@
        import React, { Component } from "react";
        import PropTypes from "prop-types";
        -
        import "./FaqItem.css";

        class FaqItem extends Component {
        @@ -9,11 +8,18 @@ class FaqItem extends Component {
            answer: PropTypes.string.isRequired
          };

        +  constructor(props) {
        +    super(props);
        +    this.state = {
        +      show: false
        +    };
        +  }
        +
          render() {
            return (
              <li className="faq-item">
                <h2 className="question">{this.props.question}</h2>
        -        <p>{this.props.answer}</p>
        +        {this.state.show && <p>{this.props.answer}</p>}
              </li>
            );
          }