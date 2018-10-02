.. _redirects-label:

========================
Navigate Using Redirects
========================

If we want to navigate programmatically for example after submitting a form we
have to use a different method. In this example we will create a back button
in the :file:`FaqItemView` to return to the overview. First we'll create the
button:

::

    <button onClick={this.onBack}>Back</button>

Then we'll add the handler to handle the back event. This event will make
use of the :file:`history` property passed by React Router. This property has a
push method which will push the new route.

::

    onBack() {
      this.props.history.push("/");
    }

The full listing of our new :file:`FaqItemView` will look as follows:

::

    import React, { Component } from "react";
    import PropTypes from "prop-types";
    import { connect } from "react-redux";

    import { getFaqItems } from "../actions";

    class FaqItemView extends Component {
      static propTypes = {
        faqItem: PropTypes.shape({
          question: PropTypes.string,
          answer: PropTypes.string
        }).isRequired,
        history: PropTypes.shape({
          push: PropTypes.func
        }).isRequired
      };

      constructor(props) {
        super(props);
        this.onBack = this.onBack.bind(this);
      }

      componentDidMount() {
        this.props.getFaqItems();
      }

      onBack() {
        this.props.history.push("/");
      }

      render() {
        return (
          <div>
            <h2 className="question">{this.props.faqItem.question}</h2>
            <p>{this.props.faqItem.answer}</p>
            <button onClick={this.onBack}>Back</button>
          </div>
        );
      }
    }

    export default connect(
      (state, props) => {
        const index = parseInt(props.match.params.index, 10);
        return {
          faqItem: index < state.faq.length ? state.faq[index] : {}
        };
      },
      { getFaqItems }
    )(FaqItemView);
