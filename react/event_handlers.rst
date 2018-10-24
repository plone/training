.. _event_handlers-label:

==================
Use Event Handlers
==================

Toggle Method
=============

To show or hide the answer we will add a toggle handler to the class :file:`FaqItem`.
This method needs to be bound to the instance like this:

.. code-block:: jsx

    constructor(props) {
      super(props);
      this.toggle = this.toggle.bind(this);
      this.state = {
        show: false
      };
    }

Exercise
========

Write the toggle handler which will toggle the :file:`show` state variable
and set the new state using the :file:`setState` method:

..  admonition:: Solution
    :class: toggle

    .. code-block:: jsx

        toggle() {
          this.setState({
            show: !this.state.show
          });
        }

Click Handler
=============

To call the newly created :file:`toggle` method we will add an on click handler to the question:

.. code-block:: jsx

    render() {
      return (
        <li className="faq-item">
          <h2 onClick={this.toggle} className="question">
            {this.props.question}
          </h2>
          {this.state.show && <p>{this.props.answer}</p>}
        </li>
      );
    }
