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
        :linenos: 
        :emphasize-lines: 17-18,20-21,35-46,49-63,70

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

    .. code-block:: dpatch

        --- a/src/components/FaqItem.jsx
        +++ b/src/components/FaqItem.jsx
        @@ -14,8 +14,11 @@ class FaqItem extends Component {
            super(props);
            this.toggle = this.toggle.bind(this);
            this.onDelete = this.onDelete.bind(this);
        +    this.onEdit = this.onEdit.bind(this);
        +    this.onSave = this.onSave.bind(this);
            this.state = {
        -      show: false
        +      show: false,
        +      mode: "view"
            };
          }

        @@ -29,14 +32,42 @@ class FaqItem extends Component {
            this.props.onDelete(this.props.index);
          }

        +  onEdit() {
        +    this.setState({
        +      mode: "edit"
        +    });
        +  }
        +
        +  onSave(event) {
        +    this.setState({
        +      mode: "view"
        +    });
        +    event.preventDefault();
        +  }
        +
          render() {
        -    return (
        +    return this.state.mode === "edit" ? (
        +      <li className="faq-item">
        +        <form onSubmit={this.onSave}>
        +          <label>
        +            Question:
        +            <input name="question" />
        +          </label>
        +          <label>
        +            Answer:
        +            <textarea name="answer" />
        +          </label>
        +          <input type="submit" value="Save" />
        +        </form>
        +      </li>
        +    ) : (
              <li className="faq-item">
                <h2 onClick={this.toggle} className="question">
                  {this.props.question}
                </h2>
                {this.state.show && <p>{this.props.answer}</p>}
                <button onClick={this.onDelete}>Delete</button>
        +        <button onClick={this.onEdit}>Edit</button>
              </li>
            );
          }

Wiring Everything Together
==========================

Create a controlled form like the add form and pass an :file:`onEdit` handler to the :file:`FaqItem` component
like we did with the :file:`onDelete`

..  admonition:: FaqItem.jsx
    :class: toggle

    .. code-block:: jsx
        :linenos: 
        :emphasize-lines: 10-11,19-20,24-26,40-58,64,74,78

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


    .. code-block:: dpatch

        --- a/src/components/FaqItem.jsx
        +++ b/src/components/FaqItem.jsx
        @@ -7,7 +7,8 @@ class FaqItem extends Component {
            question: PropTypes.string.isRequired,
            answer: PropTypes.string.isRequired,
            index: PropTypes.number.isRequired,
        -    onDelete: PropTypes.func.isRequired
        +    onDelete: PropTypes.func.isRequired,
        +    onEdit: PropTypes.func.isRequired
          };

          constructor(props) {
        @@ -15,10 +16,14 @@ class FaqItem extends Component {
            this.toggle = this.toggle.bind(this);
            this.onDelete = this.onDelete.bind(this);
            this.onEdit = this.onEdit.bind(this);
        +    this.onChangeQuestion = this.onChangeQuestion.bind(this);
        +    this.onChangeAnswer = this.onChangeAnswer.bind(this);
            this.onSave = this.onSave.bind(this);
            this.state = {
              show: false,
        -      mode: "view"
        +      mode: "view",
        +      question: "",
        +      answer: ""
            };
          }

        @@ -34,7 +39,21 @@ class FaqItem extends Component {

          onEdit() {
            this.setState({
        -      mode: "edit"
        +      mode: "edit",
        +      question: this.props.question,
        +      answer: this.props.answer
        +    });
        +  }
        +
        +  onChangeQuestion(event) {
        +    this.setState({
        +      question: event.target.value
        +    });
        +  }
        +
        +  onChangeAnswer(event) {
        +    this.setState({
        +      answer: event.target.value
            });
          }

        @@ -42,6 +61,7 @@ class FaqItem extends Component {
            this.setState({
              mode: "view"
            });
        +    this.props.onEdit(this.props.index, this.state.question, this.state.answer);
            event.preventDefault();
          }

        @@ -51,11 +71,19 @@ class FaqItem extends Component {
                <form onSubmit={this.onSave}>
                  <label>
                    Question:
        -            <input name="question" />
        +            <input
        +              name="question"
        +              value={this.state.question}
        +              onChange={this.onChangeQuestion}
        +            />
                  </label>
                  <label>
                    Answer:
        -            <textarea name="answer" />
        +            <textarea
        +              name="answer"
        +              value={this.state.answer}
        +              onChange={this.onChangeAnswer}
        +            />
                  </label>
                  <input type="submit" value="Save" />
                </form>

..  admonition:: App.js
    :class: toggle

    .. code-block:: jsx
        :linenos: 
        :emphasize-lines: 9,39-48,87

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
                      value={this.state.answer}
                      onChange={this.onChangeAnswer}
                    />
                  </label>
                  <input type="submit" value="Add" />
                </form>
              </div>
            );
          }
        }

        export default App;

    .. code-block:: dpatch

        --- a/src/App.js
        +++ b/src/App.js
        @@ -6,6 +6,7 @@ class App extends Component {
          constructor(props) {
            super(props);
            this.onDelete = this.onDelete.bind(this);
        +    this.onEdit = this.onEdit.bind(this);
            this.onChangeQuestion = this.onChangeQuestion.bind(this);
            this.onChangeAnswer = this.onChangeAnswer.bind(this);
            this.onSubmit = this.onSubmit.bind(this);
        @@ -35,6 +36,17 @@ class App extends Component {
            });
          }

        +  onEdit(index, question, answer) {
        +    let faq = this.state.faq;
        +    faq[index] = {
        +      question,
        +      answer
        +    };
        +    this.setState({
        +      faq
        +    });
        +  }
        +
          onChangeQuestion(event) {
            this.setState({
              question: event.target.value
        @@ -72,6 +84,7 @@ class App extends Component {
                      answer={item.answer}
                      index={index}
                      onDelete={this.onDelete}
        +              onEdit={this.onEdit}
                    />
                  ))}
                </ul>
