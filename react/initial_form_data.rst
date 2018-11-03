.. _initial_form_data-label:

=====================================
Use Initial Form Data To Edit An Item
=====================================

Two Modes For The FAQ Item
==========================

We will use inline editing to edit an item.
Create a button to switch to 'edit' mode.
This mode should be set in the state.
Change the render method to show a form (similar to the 'add' form) in 'edit' mode
and the view we currently have in the 'view' mode.
The :file:`onSave` handler can be a dummy handler for now, first we will focus on the two modes.

..  admonition:: Solution
    :class: toggle

    .. code-block:: jsx

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
            this.onEdit = this.onEdit.bind(this);
            this.onSave = this.onSave.bind(this);
            this.state = {
              show: false,
              mode: "view"
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

          onEdit() {
            this.setState({
              mode: "edit"
            });
          }

          onSave(event) {
            this.setState({
              mode: "view"
            });
            event.preventDefault();
          }

          render() {
            return this.state.mode === "edit" ? (
              <li className="faq-item">
                <form onSubmit={this.onSave}>
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
                <h2 onClick={this.toggle} className="question">
                  {this.props.question}
                </h2>
                {this.state.show && <p>{this.props.answer}</p>}
                <button onClick={this.onDelete}>Delete</button>
                <button onClick={this.onEdit}>Edit</button>
              </li>
            );
          }
        }

        export default FaqItem;

Wiring Everything Together
==========================

Create a controlled form like the add form and pass an :file:`onEdit` handler to the :file:`FaqItem` component
like we did with the :file:`onDelete`

..  admonition:: FaqItem.js
    :class: toggle

    .. code-block:: jsx

        import React, { Component } from "react";
        import PropTypes from "prop-types";
        import "./FaqItem.css";

        class FaqItem extends Component {
          static propTypes = {
            question: PropTypes.string.isRequired,
            answer: PropTypes.string.isRequired,
            index: PropTypes.number.isRequired,
            onDelete: PropTypes.func.isRequired,
            onEdit: PropTypes.func.isRequired
          };

          constructor(props) {
            super(props);
            this.toggle = this.toggle.bind(this);
            this.onDelete = this.onDelete.bind(this);
            this.onEdit = this.onEdit.bind(this);
            this.onChangeQuestion = this.onChangeQuestion.bind(this);
            this.onChangeAnswer = this.onChangeAnswer.bind(this);
            this.onSave = this.onSave.bind(this);
            this.state = {
              show: false,
              mode: "view",
              question: "",
              answer: ""
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

          onEdit() {
            this.setState({
              mode: "edit",
              question: this.props.question,
              answer: this.props.answer
            });
          }

          onChangeQuestion(event) {
            this.setState({
              question: event.target.value
            });
          }

          onChangeAnswer(event) {
            this.setState({
              answer: event.target.value
            });
          }

          onSave(event) {
            this.setState({
              mode: "view"
            });
            this.props.onEdit(this.props.index, this.state.question, this.state.answer);
            event.preventDefault();
          }

          render() {
            return this.state.mode === "edit" ? (
              <li className="faq-item">
                <form onSubmit={this.onSave}>
                  <label>
                    Question:
                    <input name="question" value={this.state.question} onChange={this.onChangeQuestion} />
                  </label>
                  <label>
                    Answer:
                    <textarea name="answer" value={this.state.answer} onChange={this.onChangeAnswer} />
                  </label>
                  <input type="submit" value="Save" />
                </form>
              </li>
            ) : (
              <li className="faq-item">
                <h2 onClick={this.toggle} className="question">
                  {this.props.question}
                </h2>
                {this.state.show && <p>{this.props.answer}</p>}
                <button onClick={this.onDelete}>Delete</button>
                <button onClick={this.onEdit}>Edit</button>
              </li>
            );
          }
        }

        export default FaqItem;

..  admonition:: App.js
    :class: toggle

    .. code-block:: jsx

        import React, { Component } from "react";
        import FaqItem from "./components/FaqItem";
        import "./App.css";

        class App extends Component {
          constructor(props) {
            super(props);
            this.onDelete = this.onDelete.bind(this);
            this.onEdit = this.onEdit.bind(this);
            this.onChangeQuestion = this.onChangeQuestion.bind(this);
            this.onChangeAnswer = this.onChangeAnswer.bind(this);
            this.onSubmit = this.onSubmit.bind(this);
            this.state = {
              faq: [
                {
                  question: "What does the Plone Foundation do?",
                  answer:
                    "The mission of the Plone Foundation is to protect and promote Plone. The Foundation provides marketing assistance, awareness, and evangelism assistance to the Plone community. The Foundation also assists with development funding and coordination of funding for large feature implementations. In this way, our role is similar to the role of the Apache Software Foundation and its relationship with the Apache Project."
                },
                {
                  question: "Why does Plone need a Foundation?",
                  answer:
                    "Plone has reached critical mass, with enterprise implementations and worldwide usage. The Foundation is able to speak for Plone, and provide strong and consistent advocacy for both the project and the community. The Plone Foundation also helps ensure a level playing field, to preserve what is good about Plone as new participants arrive."
                }
              ],
              question: "",
              answer: ""
            };
          }

          onDelete(index) {
            let faq = this.state.faq;
            faq.splice(index, 1);
            this.setState({
              faq
            });
          }

          onEdit(index, question, answer) {
            let faq = this.state.faq;
            faq[index] = {
              question,
              answer
            };
            this.setState({
              faq
            });
          }

          onChangeQuestion(event) {
            this.setState({
              question: event.target.value
            });
          }

          onChangeAnswer(event) {
            this.setState({
              answer: event.target.value
            });
          }

          onSubmit(event) {
            this.setState({
              faq: [
                ...this.state.faq,
                {
                  question: this.state.question,
                  answer: this.state.answer
                }
              ],
              question: "",
              answer: ""
            });
            event.preventDefault();
          }

          render() {
            return (
              <div>
                <ul>
                  {this.state.faq.map((item, index) => (
                    <FaqItem
                      question={item.question}
                      answer={item.answer}
                      index={index}
                      onDelete={this.onDelete}
                      onEdit={this.onEdit}
                    />
                  ))}
                </ul>
                <form onSubmit={this.onSubmit}>
                  <label>
                    Question:
                    <input
                      name="question"
                      type="text"
                      value={this.state.question}
                      onChange={this.onChangeQuestion}
                    />
                  </label>
                  <label>
                    Answer:
                    <textarea
                      name="answer"
                      onChange={this.onChangeAnswer}
                      value={this.state.answer}
                    />
                  </label>
                  <input type="submit" value="Add" />
                </form>
              </div>
            );
          }
        }

        export default App;
