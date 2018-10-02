.. _actions-label:

===================================
Use Actions To Manipulate The Store
===================================

Wiring The Store
================

Now that we have our store ready it's time to connect the store to our code
and remove all the unneeded functionality. First step is to factor out the
:file:`Faq` component into a separate file called :file:`components/Faq.js`, it is
almost a 100% copy of :file:`App.js`:

::

    import React, { Component } from "react";
    import FaqItem from "./FaqItem";

    class Faq extends Component {
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
                "The mission of the Plone Foundation is to protect and..."
            },
            {
              question: "Why does Plone need a Foundation?",
              answer:
                "Plone has reached critical mass, with enterprise..."
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

    export default Faq;

Next we'll create an :file:`App` component with just the store and a reference
to our newly created :file:`Faq` component:

::

    import React, { Component } from "react";
    import { Provider } from "react-redux";
    import { createStore } from "redux";
    import rootReducer from "./reducers";
    import Faq from "./components/Faq";

    import "./App.css";

    const store = createStore(rootReducer);

    class App extends Component {
      render() {
        return (
          <Provider store={store}>
            <Faq />
          </Provider>
        );
      }
    }

    export default App;

Use The Data From The Store
===========================

Now that we have our store wired we can start using the store data instead of
our local state. We will use the helper method :file:`connect` as a decorator to
map both the data and the actions to our components. The :file:`connect` call
takes two parameters; the first is a method which provides the redux state and
props and returns an object which will be mapped to props of the component. The
second is an object with all the actions which will also be mapped to
props on the component.

::

    import addFaqItem from "./actions";

    class Faq extends Component {
      static propTypes = {
        faq: PropTypes.arrayOf(
          PropTypes.shape({
            question: PropTypes.string.isRequired,
            answer: PropTypes.string.isRequired
          })
        ),
        addFaqItem: PropTypes.func.isRequired
      };

      ...
    }

    export default connect(
      (state, props) => ({
        faq: state.faq
      }),
      { addFaqItem }
    )(Faq);

We can remove all the edit and delete references since that will be handled by
the :file:`FaqItem` to clean up our code. We will also change the :file:`onSubmit`
handler to use the attached :file:`addFaqItem` method. The result will be as
follows:

::

    import React, { Component } from "react";
    import { connect } from "react-redux";
    import PropTypes from "prop-types";

    import FaqItem from "./FaqItem";
    import { addFaqItem } from "../actions";

    class Faq extends Component {
      static propTypes = {
        faq: PropTypes.arrayOf(
          PropTypes.shape({
            question: PropTypes.string.isRequired,
            answer: PropTypes.string.isRequired
          })
        ),
        addFaqItem: PropTypes.func.isRequired
      };

      constructor(props) {
        super(props);
        this.onChangeQuestion = this.onChangeQuestion.bind(this);
        this.onChangeAnswer = this.onChangeAnswer.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.state = {
          question: "",
          answer: ""
        };
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
        this.props.addFaqItem(this.state.question, this.state.answer);
        this.setState({
          question: "",
          answer: ""
        });
        event.preventDefault();
      }

      render() {
        return (
          <div>
            <ul>
              {this.props.faq.map((item, index) => (
                <FaqItem
                  question={item.question}
                  answer={item.answer}
                  index={index}
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

    export default connect(
      (state, props) => ({
        faq: state.faq
      }),
      { addFaqItem }
    )(Faq);

Exercise
========

Now that we factored out the edit and delete actions from the :file:`Faq`
component update the :file:`FaqItem` component to call the actions we created
for our store.

..  admonition:: Solution
    :class: toggle

    ::

        import React, { Component } from "react";
        import PropTypes from "prop-types";
        import { connect } from "react-redux";

        import { editFaqItem, deleteFaqItem } from "../actions";

        import "./FaqItem.css";

        class FaqItem extends Component {
          static propTypes = {
            question: PropTypes.string.isRequired,
            answer: PropTypes.string.isRequired,
            index: PropTypes.number.isRequired,
            editFaqItem: PropTypes.func.isRequired,
            deleteFaqItem: PropTypes.func.isRequired
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
            this.props.deleteFaqItem(this.props.index);
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
            this.props.editFaqItem(
              this.props.index,
              this.state.question,
              this.state.answer
            );
            event.preventDefault();
          }

          render() {
            return this.state.mode === "edit" ? (
              <li className="faq-item">
                <form onSubmit={this.onSave}>
                  <label>
                    Question:
                    <input
                      name="question"
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

        export default connect(
          () => {},
          { editFaqItem, deleteFaqItem }
        )(FaqItem);
