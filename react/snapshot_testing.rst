.. _snapshot_testing-label:

====================
Use Snapshot Testing
====================

In order to test the rendered output of a specific component we can use snapshot
testing. We need to install the :file:`react-test-render` package first:

.. code-block:: console

    yarn add react-test-renderer --dev

Then we will create a file called :file:`FaqItem.test.js`. Here we will
render the component and assert the markup.

::

    import React from "react";
    import renderer from "react-test-renderer";

    import FaqItem from "./FaqItem";

    describe("FaqItem", () => {
      it("renders a faq item", () => {
        const component = renderer.create(
          <FaqItem
            question="What is the answer to life the universe and everything?"
            answer="42"
          />
        );
        const json = component.toJSON();
        expect(json).toMatchSnapshot();
      });
    });

To run our tests we will run the command:

.. code-block:: console

    yarn test
