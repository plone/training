Some theory
===========

Test types
----------

There are 4 main test types that we can use:

- Unittests
- Integration Tests
- Functional Tests
- Acceptance Tests

They can also be represented as a Test Pyramid:

.. code-block:: none

          = Acceptance Tests =
         == Functional Tests ==
       ==== Integration Tests ===
    ========== Unittests ===========

Complexity and time to execute increases from the bottom to the top of the pyramid.

Unittests are the easiest ones to write because they test single isolated functions.
Going up through the pyramid, tests become more complex because they start to test integration between functions and features
until Acceptance Tests (also called e2e) where you test the final user interaction.

More complexity means also more time to execute a test, because you need different layers/services to run a single function or the complete application.

In Plone usually we don't need to write pure unittest because most of the methods are already integrations with some CMS features and tools.
That's the reason why usually Plone tests starts from Integration Tests.

The difference between Integration and Functional tests is that Integration tests will create a new transaction for each test and roll 
it back on test tear-down. This means that they don't perform commits on the databse.
Functional tests on the other side, use a temporary storage (called DemoStorage) that allows to simulate transaction commits.
They are useful for browser interaction testing for example, but for this reason they are slower than Integration Tests.
