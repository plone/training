.. _callbacks-label:

===============================
Use Callbacks To Delete An Item
===============================

Add Delete Button
=================

To be able to manage our faq entries we start by adding a delete button to
remove an item from the list. Add the delete button to the view and create
an empty :file:`onDelete` handler which is called when the button is pressed.

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
            this.toggle = this.toggle.bind(this);
            this.onDelete = this.onDelete.bind(this);
            this.state = {
              show: false
            };
          }

          toggle() {
            this.setState({
              show: !this.state.show
            });
          }

          render() {
            return (
              <li className="faq-item">
                <h2 onClick={this.toggle} className="question">
                  {this.props.question}
                </h2>
                {this.state.show && <p>{this.props.answer}</p>}
                <button onClick={this.onDelete}>Delete</button>
              </li>
            );
          }
        }

        export default FaqItem;

Write The onDelete Handler
==========================

Now that we have our dummy handler ready we need to add functionality to the
handler. Since the list of Faq items is managed by our :file:`App` component we
can't directly remove the item. Rewrite the :file:`FaqItem` component so that
a unique identifier of the Faq item and a callback to remove the Faq item can be
passed to this component. Also complete the :file:`onDelete` handler so it will
call the callback with the correct identifier.

..  admonition:: Solution
    :class: toggle

    ::

        import React, { Component } from "react";
        import PropTypes from "prop-types";
        import "./FaqItem.css";

        class FaqItem extends Component {
          static propTypes = {
            question: PropTypes.string.isRequired,
            answer: PropTypes.string.isRequired,
            index: PropTypes.number.isRequired,
            onDelete: PropTypes.func.isRequired
          };

          constructor(props) {
            super(props);
            this.toggle = this.toggle.bind(this);
            this.onDelete = this.onDelete.bind(this);
            this.state = {
              show: false
            };
          }

          toggle() {
            this.setState({
              show: !this.state.show
            });
          }

          onDelete() {
            this.props.onDelete(this.props.index);
          }

          render() {
            return (
              <li className="faq-item">
                <h2 onClick={this.toggle} className="question">
                  {this.props.question}
                </h2>
                {this.state.show && <p>{this.props.answer}</p>}
                <button onClick={this.onDelete}>Delete</button>
              </li>
            );
          }
        }

        export default FaqItem;

Write A Dummy Delete Handler
============================

Now we're ready to change the :file:`App` component to add a dummy :file:`onDelete`
handler. Add the :file:`onDelete` handler to the :file:`App` component which logs
the index of the Faq item to the console. Make sure to pass the index and the
callback to the :file:`FaqItem` component to wire everything together:

..  admonition:: Solution
    :class: toggle

    ::

        import React, { Component } from "react";
        import FaqItem from "./components/FaqItem";
        import "./App.css";

        class App extends Component {
          constructor(props) {
            super(props);
            this.onDelete = this.onDelete.bind(this);
            this.state = {
              faq: [
                {
                  question: "What does the Plone Foundation do?",
                  answer:
                    "The mission of the Plone Foundation is to protect and..."
                },
                {
                  question: "Why does Plone need a Foundation?",
                  answer:
                    "Plone has reached critical mass, with enterprise..."
                }
              ]
            };
          }

          onDelete(index) {
            console.log(index);
          }

          render() {
            return (
              <ul>
                {this.state.faq.map((item, index) => (
                  <FaqItem
                    question={item.question}
                    answer={item.answer}
                    index={index}
                    onDelete={this.onDelete}
                  />
                ))}
              </ul>
            );
          }
        }

        export default App;

Delete The Faq Item From The List
=================================

The last step is to remove the item from the list. Write the :file:`onDelete`
handler which removes the item from the list and creates the new state.

..  admonition:: Solution
    :class: toggle

    ::

        onDelete(index) {
          let faq = this.state.faq;
          faq.splice(index, 1);
          this.setState({
            faq
          });
        }
