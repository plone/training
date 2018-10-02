.. _state-label:

==================================
How To Use State In Your Component
==================================

Store Questions And Answers In The State
========================================

In order to manipulate the Faq later on we will move all the data to the state
of the component. The state of the component is the local state of that
specific component. When the state changes the render method is called again. In
the constructor of the class we can initialize the state.

::

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

Exercise
========

To save space in the view we want to be able to show and hide the answer when
you click on the question. Add a state variable to the :file:`FaqItem` component
which keeps the state of the answer being shown or not and adjust the render
method to show or hide the answer.

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
