Acceptance testing
==================

Acceptance tests are the highest level of tests in the pyramid.

In previous chapters we tested if the code has no bugs and if the interaction of several methods/behaviors generates
the expected outputs, but what if we want to test if the output for the final user is correct?

Acceptance tests do exactly this. They simulate user interaction over different scenarios.

We can achieve something similar with the ``browser`` utility in functional tests, but it has some cons:
for example you can't test javascripts.

To write acceptance tests, we use `plone.app.robotframework <https://github.com/plone/plone.app.robotframework>`_: a Plone plugin that provides Robot Framework-compatible tools
and resources for writing functional Selenium-tests (including acceptance tests).

`Robot Framework <http://robotframework.org>`_ is a generic test automation framework for acceptance testing and acceptance test-driven development (ATDD),
even for behavior driven development (BDD).
It has easy-to-use ``plain text test syntax`` and utilizes the keyword-driven testing approach.

`Selenium <https://www.seleniumhq.org>`_ is a web browser automation framework that exercises the browser as if the user was interacting with the browser.

Each test will open a real browser instance and test user interaction with Selenium.

.. note::

    Selenium-bindings for Python use ``Firefox`` as the default browser.

    Unless you know how to configure other browsers to work with Selenium you should have Firefox installed in your system.
