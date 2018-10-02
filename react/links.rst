.. _links-label:

=======================
Using Links To Navigate
=======================

Links are used to navigate between pages in React Router. This will make sure
the browser doesn't do a full refresh but just changes the route. We will add
a link to the :file:`FaqItem` component so we can go to the :file:`FaqItemView`
view.

::

    import { Link } from "react-router-dom";

    ...

    <Link to={`/faq/${this.props.index}`}>View</Link>

The full listing of the :file:`FaqItem` component is as follows:

::

    import React, { Component } from "react";
    import PropTypes from "prop-types";
    import { connect } from "react-redux";
    import { Link } from "react-router-dom";

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
            <Link to={`/faq/${this.props.index}`}>View</Link>
          </li>
        );
      }
    }

    export default connect(
      () => {},
      { editFaqItem, deleteFaqItem }
    )(FaqItem);
