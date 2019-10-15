Robot tests
===========

Robot tests are written in test suites, which are plain text files, usually ending with ``.robot``.

Robot test file format
----------------------

We can see an example of robot tests in our package.
plonecli creates an example robot test file in ``tests/robot/test_example.robot``:

.. literalinclude:: _snippets/test_example.robot
    :language: none
    :lines: 24-66

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

.. literalinclude:: _snippets/test_example.robot
    :language: none
    :lines: 37-40

The initial state is the keyword that starts with "Given":

.. literalinclude:: _snippets/test_example.robot
    :language: none
    :lines: 39
  
This keyword is a set of sequential actions (defined in Keywords section):

.. literalinclude:: _snippets/test_example.robot
    :language: none
    :lines: 48-50  

First of all we open the login_form page. Then we wait the page to be loaded and the two fields are available in html.

.. note::

  ${PLONE_URL} is a global variable defined in an plone.app.robotframework imported library.

After a Given statement, there are a list of actions (``When``), and a final expectation (``Then``) that has the same structure.

.. note::
  
  Most of these actions came from default Selenium library (imported in Settings section).
  You can find a list of available actions `online <https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#keywords>`_.

  For standard plone actions and keywords, you can see the imported files (``keywords.robot`` and ``selenium.robot``).

Running robot tests
-------------------

A package created with plonecli is already configured to run robotframework tests.

To use robotframework tests in your package, it needs ``plone.app.robotframework`` dependency in ``setup.py`` file.

There is also a ``robot`` part in ``base.cfg`` file. This configuration is optional because it isn't required to run robot tests, but it
installs two helper scripts for writing tests:

- ``bin/robot-server`` starts a temporary Plone site with the given test layer set up
- ``bin/robot`` executes Robot Framework’s pybot-runner so that it will run the given test suite against the running robot-server, ensuring that tests will be run in isolation (database is cleaned between the tests)

.. literalinclude:: _snippets/buildout.cfg
    :language: ini
    :lines: 78-81

We can run robot tests with other tests running this command:

.. code-block:: console

  $ plonecli test --all

Or, as any other test, we can run only a single test with this command:

.. code-block:: console

  $ plonecli test -s plonetraining.testing -t test_example.robot --all

These commands takes time because each test case need to start a server, open a new browser window and then execute keywords and wait the reponse of the server.

When we are developing our tests, we can speedup this process, keeping a robot-server instance always up with this command:

.. code-block:: console

  $ bin/robot-server --reload-path src plonetraining.testing.testing.PLONETRAINING_TESTING_ACCEPTANCE_TESTING

This command will start a robotframework server that instantiate also a Plone instance.

This has a second advantage, because you can inspect Plone site every time and try things before writing actions in the test.

With robot server running, we can run test cases with this command:

.. code-block:: console

  $ bin/robot /src/plonetraining/testing/tests/robot/test_example.robot

.. note::

  These development helpers works well until Plone 5.1. At the moment of this training has been written, there are some problems starting robot-server instance with Plone 5.2 and WSGI.

Debugging robot tests
---------------------

Debugging a robot framework test could be hard because there could be problems on the server or on the client.
 

Test execution could be very slow and difficult to follow for a human, so we can slow it down to better understand what's happening:

.. code-block:: none

  *** Settings ***

  Suite setup  Set Selenium speed  2s

Alternatively we could pause (or set a sleep timeout) the execution of a test and manually inspect the site:

.. code-block:: none

  *** Test Cases ***

  Pause tests with included Pause-keyword
    Pause

  Pause tests for 10 minutes and then continue
    Sleep  10 min

Finally we could also pause the test execution and test keywords from console:

.. code-block:: none

  *** Test Cases ***

  Start interactive debugger
      Import library  DebugLibrary
      Debug

.. note::

  There are more detailed examples in Plone `documentation <https://docs.plone.org/external/plone.app.robotframework/docs/source/debugging.html>`_ online.


Test reports
------------

If we run a robot-framework test with ``plonecli test`` command, we have the usual output in console that tells us if a test succeeded or failed.

Robot tests are a combination between backend and frontend environments, so it isn't easy to have all informations about the status of the test on console.

For that reason, robotframework generates detailed reports in `parts/test` folder where you can see the status of last execution and detailed infos for each test case.

Excercise 1
+++++++++++

Let's write our first robot test!

Try to write some basic scenarios:

- Login on the site and create a new TestType content
- Visit TestType view passing a custom message in querystring

.. note::

  plonecli created a basic robot test for our TestType content-type, so the first part of the exercise could be copied from it.
  Try to not copying it and play with robot framework syntax by yourself.

  `Here <https://docs.plone.org/external/plone.app.robotframework/docs/source/index.html>`_ you can find some documentation that can help you writing your first robot framework test.


..  admonition:: Solution
  :class: toggle

  .. literalinclude:: _snippets/test_ct_testing_item.robot
    :language: text
    :lines: 35-99


Excercise 2
+++++++++++

Now let's test something that we can't test with functional tests: javascripts.

- Add a basic mockup pattern to testing-item-view (for example `autotoc <http://plone.github.io/mockup/dev/#pattern/autotoc>`_)
- Check that table of contents is rendered in page

..  admonition:: Solution
  :class: toggle

    First of all, add autotoc to the template:

    .. literalinclude:: _snippets/testing_item_view_toc.pt
      :language: html
      :lines: 1-28, 44-46
      :emphasize-lines: 13-28

    Now, create a test case that checks autotoc:

    .. literalinclude:: _snippets/test_autotoc.robot
      :language: text
      :lines: 35-42, 57-74, 79-84

Excercise 3
+++++++++++

Last test with javascripts: try to simulate clicks.

- Autotoc pattern can also be used for generate tabs.
- Check that clicking tabs, will be rendered different pieces of dom.

..  admonition:: Solution
  :class: toggle

    Add tabs to the template:

    .. literalinclude:: _snippets/testing_item_view_toc.pt
      :language: html
      :emphasize-lines: 29-43

    Update previous test with more test cases:

    .. literalinclude:: _snippets/test_autotoc.robot
      :language: text
      :emphasize-lines: 43-54,76-77,85-88 
