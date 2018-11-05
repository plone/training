.. _actions-label:

===================================
Use Actions To Manipulate The Store
===================================

Wiring The Store
================

Now that we have our store ready it's time to connect the store to our code and remove all the unneeded functionality.
First step is to factor out the :file:`Faq` component into a separate file called :file:`components/Faq.jsx`,
it is almost a 100% copy of :file:`App.js`:

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 4,115

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

    export default Faq;

Next we will create an :file:`App` component with just the store and a reference to our newly created :file:`Faq` component:

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 2-3,5-6,10,15-17

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

..  admonition:: Differences
    :class: toggle

    .. code-block:: dpatch

        --- a/src/App.js
        +++ b/src/App.js
        @@ -1,114 +1,20 @@
        import React, { Component } from "react";
        -import FaqItem from "./components/FaqItem";
        -import "./App.css";
        -
        -class App extends Component {
        -  constructor(props) {
        -    super(props);
        -    this.onDelete = this.onDelete.bind(this);
        -    this.onEdit = this.onEdit.bind(this);
        -    this.onChangeQuestion = this.onChangeQuestion.bind(this);
        -    this.onChangeAnswer = this.onChangeAnswer.bind(this);
        -    this.onSubmit = this.onSubmit.bind(this);
        -    this.state = {
        -      faq: [
        -        {
        -          question: "What does the Plone Foundation do?",
        -          answer:
        -            "The mission of the Plone Foundation is to protect and promote Plone. The Foundation provides marketing assistance, awareness, and evangelism assistance to the Plone community. The Foundation also assists with development funding and coordination of funding for large feature implementations. In this way, our role is similar to the role of the Apache Software Foundation and its relationship with the Apache Project."
        -        },
        -        {
        -          question: "Why does Plone need a Foundation?",
        -          answer:
        -            "Plone has reached critical mass, with enterprise implementations and worldwide usage. The Foundation is able to speak for Plone, and provide strong and consistent advocacy for both the project and the community. The Plone Foundation also helps ensure a level playing field, to preserve what is good about Plone as new participants arrive."
        -        }
        -      ],
        -      question: "",
        -      answer: ""
        -    };
        -  }
        +import { Provider } from "react-redux";
        +import { createStore } from "redux";
        
        -  onDelete(index) {
        -    let faq = this.state.faq;
        -    faq.splice(index, 1);
        -    this.setState({
        -      faq
        -    });
        -  }
        -
        -  onEdit(index, question, answer) {
        -    let faq = this.state.faq;
        -    faq[index] = {
        -      question,
        -      answer
        -    };
        -    this.setState({
        -      faq
        -    });
        -  }
        +import rootReducer from "./reducers";
        +import Faq from "./components/Faq";
        
        -  onChangeQuestion(event) {
        -    this.setState({
        -      question: event.target.value
        -    });
        -  }
        -
        -  onChangeAnswer(event) {
        -    this.setState({
        -      answer: event.target.value
        -    });
        -  }
        +import "./App.css";
        
        -  onSubmit(event) {
        -    this.setState({
        -      faq: [
        -        ...this.state.faq,
        -        {
        -          question: this.state.question,
        -          answer: this.state.answer
        -        }
        -      ],
        -      question: "",
        -      answer: ""
        -    });
        -    event.preventDefault();
        -  }
        +const store = createStore(rootReducer);
        
        +class App extends Component {
          render() {
            return (
        -      <div>
        -        <ul>
        -          {this.state.faq.map((item, index) => (
        -            <FaqItem
        -              question={item.question}
        -              answer={item.answer}
        -              index={index}
        -              onDelete={this.onDelete}
        -              onEdit={this.onEdit}
        -            />
        -          ))}
        -        </ul>
        -        <form onSubmit={this.onSubmit}>
        -          <label>
        -            Question:
        -            <input
        -              name="question"
        -              type="text"
        -              value={this.state.question}
        -              onChange={this.onChangeQuestion}
        -            />
        -          </label>
        -          <label>
        -            Answer:
        -            <textarea
        -              name="answer"
        -              value={this.state.answer}
        -              onChange={this.onChangeAnswer}
        -            />
        -          </label>
        -          <input type="submit" value="Add" />
        -        </form>
        -      </div>
        +      <Provider store={store}>
        +        <Faq />
        +      </Provider>
            );
          }
        }

Use The Data From The Store
===========================

Now that we have our store wired we can start using the store data instead of our local state.
We will use the helper method :file:`connect` as a decorator to map both the data and the actions to our components.
The :file:`connect` call takes two parameters;
the first is a method which provides the redux state and props
and returns an object which will be mapped to props of the component.
The second is an object with all the actions which will also be mapped to props on the component.

.. code-block:: jsx
    :linenos: 
    :lineno-start: 3
    :emphasize-lines: 1,4-12

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

.. code-block:: jsx
    :linenos: 
    :lineno-start: 124
    :emphasize-lines: 1-6

    export default connect(
      (state, props) => ({
        faq: state.faq
      }),
      { addFaqItem }
    )(Faq);

We can remove all the edit and delete references since that will be handled by the :file:`FaqItem` to clean up our code.
We will also change the :file:`onSubmit` handler to use the attached :file:`addFaqItem` method.
The result will be as follows:

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 43,55

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

    export default connect(
      (state, props) => ({
        faq: state.faq
      }),
      { addFaqItem }
    )(Faq);


..  admonition:: Differences
    :class: toggle

    .. code-block:: dpatch


        --- a/src/components/Faq.jsx
        +++ b/src/components/Faq.jsx
        @@ -1,49 +1,32 @@
        import React, { Component } from "react";
        +import { connect } from "react-redux";
        +import PropTypes from "prop-types";
        +
        import FaqItem from "./FaqItem";
        +import { addFaqItem } from "../actions";

        class Faq extends Component {
        +  static propTypes = {
        +    faq: PropTypes.arrayOf(
        +      PropTypes.shape({
        +        question: PropTypes.string.isRequired,
        +        answer: PropTypes.string.isRequired
        +      })
        +    ),
        +    addFaqItem: PropTypes.func.isRequired
        +  };
        +
          constructor(props) {
            super(props);
        -    this.onDelete = this.onDelete.bind(this);
        -    this.onEdit = this.onEdit.bind(this);
            this.onChangeQuestion = this.onChangeQuestion.bind(this);
            this.onChangeAnswer = this.onChangeAnswer.bind(this);
            this.onSubmit = this.onSubmit.bind(this);
            this.state = {
        -      faq: [
        -        {
        -          question: "What does the Plone Foundation do?",
        -          answer: "The mission of the Plone Foundation is to protect and..."
        -        },
        -        {
        -          question: "Why does Plone need a Foundation?",
        -          answer: "Plone has reached critical mass, with enterprise..."
        -        }
        -      ],
              question: "",
              answer: ""
            };
          }

        -  onDelete(index) {
        -    let faq = this.state.faq;
        -    faq.splice(index, 1);
        -    this.setState({
        -      faq
        -    });
        -  }
        -
        -  onEdit(index, question, answer) {
        -    let faq = this.state.faq;
        -    faq[index] = {
        -      question,
        -      answer
        -    };
        -    this.setState({
        -      faq
        -    });
        -  }
        -
          onChangeQuestion(event) {
            this.setState({
              question: event.target.value
        @@ -57,14 +40,8 @@ class Faq extends Component {
          }

          onSubmit(event) {
        +    this.props.addFaqItem(this.state.question, this.state.answer);
            this.setState({
        -      faq: [
        -        ...this.state.faq,
        -        {
        -          question: this.state.question,
        -          answer: this.state.answer
        -        }
        -      ],
              question: "",
              answer: ""
            });
        @@ -75,13 +52,11 @@ class Faq extends Component {
            return (
              <div>
                <ul>
        -          {this.state.faq.map((item, index) => (
        +          {this.props.faq.map((item, index) => (
                    <FaqItem
                      question={item.question}
                      answer={item.answer}
                      index={index}
        -              onDelete={this.onDelete}
        -              onEdit={this.onEdit}
                    />
                  ))}
                </ul>
        @@ -110,4 +85,9 @@ class Faq extends Component {
          }
        }

        -export default Faq;
        +export default connect(
        +  (state, props) => ({
        +    faq: state.faq
        +  }),
        +  { addFaqItem }
        +)(Faq);

Exercise
========

Now that we factored out the edit and delete actions from the :file:`Faq` component
update the :file:`FaqItem` component to call the actions we created for our store.

..  admonition:: Solution
    :class: toggle

    .. code-block:: jsx
        :linenos: 
        :emphasize-lines: 3,5,14-15,41,68-72,112-115

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
          () => ({}),
          { editFaqItem, deleteFaqItem }
        )(FaqItem);


    .. code-block:: dpatch

        --- a/src/components/FaqItem.jsx
        +++ b/src/components/FaqItem.jsx
        @@ -1,5 +1,9 @@
        import React, { Component } from "react";
        import PropTypes from "prop-types";
        +import { connect } from "react-redux";
        +
        +import { editFaqItem, deleteFaqItem } from "../actions";
        +
        import "./FaqItem.css";

        class FaqItem extends Component {
        @@ -7,8 +11,8 @@ class FaqItem extends Component {
            question: PropTypes.string.isRequired,
            answer: PropTypes.string.isRequired,
            index: PropTypes.number.isRequired,
        -    onDelete: PropTypes.func.isRequired,
        -    onEdit: PropTypes.func.isRequired
        +    editFaqItem: PropTypes.func.isRequired,
        +    deleteFaqItem: PropTypes.func.isRequired
          };

          constructor(props) {
        @@ -34,7 +38,7 @@ class FaqItem extends Component {
          }

          onDelete() {
        -    this.props.onDelete(this.props.index);
        +    this.props.deleteFaqItem(this.props.index);
          }

          onEdit() {
        @@ -61,7 +65,11 @@ class FaqItem extends Component {
            this.setState({
              mode: "view"
            });
        -    this.props.onEdit(this.props.index, this.state.question, this.state.answer);
        +    this.props.editFaqItem(
        +      this.props.index,
        +      this.state.question,
        +      this.state.answer
        +    );
            event.preventDefault();
          }

        @@ -101,4 +109,7 @@ class FaqItem extends Component {
          }
        }

        -export default FaqItem;
        +export default connect(
        +  () => ({}),
        +  { editFaqItem, deleteFaqItem }
        +)(FaqItem);
