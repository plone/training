Acceptance testing
==================

Acceptance tests are the highest level of tests in the pyramid.

In previous chapters we tested if the code has no bugs and if the interaction of several methods/behaviors generates
the expected outputs, but what if we want to test if the output for the final user is correct?

Acceptance tests do exactly this thing. They simulate user interaction over different scenarios.

We can do something similar with the browser utility in functional tests, but it has some cons:
for example you can't test javascripts.

To write acceptance tests, we use plone.app.robotframework: a Plone plugin that provides Robot Framework-compatible tools
and resources for writing functional Selenium-tests (including acceptance tests).

Robot Framework is a generic test automation framework for acceptance testing and acceptance test-driven development (ATDD),
even for behavior driven development (BDD).
It has easy-to-use plain text test syntax and utilizes the keyword-driven testing approach.

Selenium is a web browser automation framework that exercises the browser as if the user was interacting with the browser.

.. note::

    Selenium-bindings for Python use Firefox as the default browser.

    Unless you know how to configure other browsers to work with Selenium you should have Firefox installed in your system.

Running robot tests
-------------------

A package created with plonecli is already configured to run robotframework tests.

To use robotframework tests in your package, it needs ``plone.app.robotframework`` dependency in ``setup.py`` file.

There is also a ``robot`` part in ``base.cfg`` file. This configuration is optional because it isn't required to run robot tests, but it
installs two helper scripts for writing tests:

- ``bin/robot-server`` starts a temporary Plone site with the given test layer set up
- ``bin/robot`` executes Robot Framework’s pybot-runner so that it will run the given test suite against the running robot-server, ensuring that tests will be run in isolation (database is cleaned between the tests)

.. code-block:: ini

    [robot]
    recipe = zc.recipe.egg
    eggs =
        ${test:eggs}
        plone.app.robotframework[debug,reload]


We can run robot tests with other tests running this command:

.. code-block:: console

  $ plonecli test --all

Or, as any other test, we can run only a single test with this command:

.. code-block:: console

  $ plonecli test -s plonetraining.testing -t test_example.robot --all



