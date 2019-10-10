Robot tests
===========

Robot tests are written in test suites, which are plain text files, usually ending with ``.robot``.

Robot test file format
----------------------

We can see an example of robot tests in our package.
plonecli creates an example robot test file in ``tests`` folder: ``test_example.robot``:

.. code-block:: none

  *** Settings *****************************************************************

  Resource  plone/app/robotframework/selenium.robot
  Resource  plone/app/robotframework/keywords.robot

  Library  Remote  ${PLONE_URL}/RobotRemote

  Test Setup  Open test browser
  Test Teardown  Close all browsers


  *** Test Cases ***************************************************************

  Scenario: As a member I want to be able to log into the website
    [Documentation]  Example of a BDD-style (Behavior-driven development) test.
    Given a login form
    When I enter valid credentials
    Then I am logged in


  *** Keywords *****************************************************************

  # --- Given ------------------------------------------------------------------

  a login form
    Go To  ${PLONE_URL}/login_form
    Wait until page contains  Login Name
    Wait until page contains  Password


  # --- WHEN -------------------------------------------------------------------

  I enter valid credentials
    Input Text  __ac_name  admin
    Input Text  __ac_password  secret
    Click Button  Log in


  # --- THEN -------------------------------------------------------------------

  I am logged in
    Wait until page contains  You are now logged in
    Page should contain  You are now logged in


As we can see, a robot test file is composed in different sections:

- ``Settings``: where we can import test libraries, resource files and variable files. We can define metadata for test suites and test cases and we can also define some actions to do when a test starts (Setup) or finished (TearDown) like opening the browser or closing it.
- ``Variables`` (not used in the example): a section where we can define some variables that could be used everywhere in the test.
- ``Test Cases``: a list of test scenarios based on available keywords
- ``Keywords``: a set of actions that we can do in the test.

Basically, a robot test is all about running test clauses (keywords).
Every test case may contain one or more keywords, which are run sequentially – usually until the first of them fails.

Keywords can have arguments, and are separated from their arguments (and arguments from each other) using at least two spaces.

.. note::
  
  Keywords are defined in keyword libraries and as user keywords and they can be imported in a test in ``Settings`` section.

  Keyword libraries can be Python libraries or XML-RPC-services.
  User keywords are just lists of test clauses reusing existing keywords or other user keywords.
  User keywords are described in the test suite, or imported from resource files.


Test scenarios
--------------

There are several ways to write robot test scenarios. In Plone we choose the ``Given-When-Then style``.

This format is very useful because allows to write test cases that everyone can understand as they are similar to human-like statements.

When writing test cases in this style, the initial state is usually expressed with a keyword starting with word ``Given``,
the actions are described with keyword starting with ``When`` and the expectations with a keyword starting with ``Then``.

.. note::

  Keyword starting with ``And`` or ``But`` may be used if a step has more than one action.

Let see how a keyword works. In our example, we have this scenario:

.. code-block:: none

    Scenario: As a member I want to be able to log into the website
      [Documentation]  Example of a BDD-style (Behavior-driven development) test.
      Given a login form
      When I enter valid credentials
      Then I am logged in

The initial state is the keyword that starts with "Given":

.. code-block:: none

  Given a login form
  
This keyword is a set of sequential actions (defined in Keywords section):

.. code-block:: none

  a login form
    Go To  ${PLONE_URL}/login_form
    Wait until page contains  Login Name
    Wait until page contains  Password

First of all we open the login_form page. Then we wait the page to be loaded and the two fields are available in html.

.. note::

  ${PLONE_URL} is a global variable defined in an plone.app.robotframework imported library.

After a Given statement, there are a list of ``When`` actions, and a final expectation that has the same structure.

.. note::
  
  Most of these actions came from imported Selenium library. You can find a list of available actions `online <https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#keywords>`_.

  For standard plone actions and keywords, you can see the imported files (``keywords.robot`` and ``selenium.robot``).


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

These commands takes time because each test case need to start a server, open a new browser window and then execute keywords and wait the reponse of the server.

When we are developing our tests, we can speedup a bit this process, keeping a robot-server instance always up with this command:

.. code-block:: console

  $ bin/robot-server --reload-path src plonetraining.testing.testing.PLONETRAINING_TESTING_ACCEPTANCE_TESTING

This command will start a robotframework server that instantiate also a Plone instance.
This has a second advantage, because you can inspect Plone site every time and try things before writing actions in the test.

To run a test case, we should run this command:

.. code-block:: console

  $ bin/robot /src/plonetraining/testing/tests/robot/test_example.robot

.. note::

  These development helpers works well until Plone 5.1. At the moment of this training has been written, there are some problems starting robot-server instance with Plone 5.2 and WSGI.

Test reports
------------

If we run a robot-framework test with ``plonecli test`` command, we have the usual testing output that tells us if a test succeeded or failed.

Robot tests are a combination between backend and frontend environments, so it isn't easy to have all informations about the status of the test on console.

For that reason, robotframework generates detailed reports in `parts/test` folder where you can see the status of last execution and detailed infos for each test case.
