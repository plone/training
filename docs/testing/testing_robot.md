---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Robot tests

Robot tests are written in test suites, which are plain text files, usually with the filename ending `.robot`.

## Robot test file format

We can see an example of robot tests in our package.
plonecli creates an example robot test file in `tests/robot/test_example.robot`:

```{literalinclude} _snippets/test_example.robot
:language: none
:lines: 24-66
```

A robot test file is composed of different sections:

- `Settings`: where we can import test libraries, resource files and variable files. We can define metadata for test suites and test cases and we can also define some actions to perform when a test starts (Setup) or finishes (TearDown), such as opening the browser or closing it.
- `Variables` (not used in this example): a section where we can define some variables that could be used everywhere in the test.
- `Test Cases`: a list of test scenarios based on available keywords.
- `Keywords`: a set of actions that we can perform during the test.

Basically, a robot test is all about running test clauses (keywords).
Every test case may contain one or more keywords, which are run sequentially – usually until one fails.

Keywords can have arguments, and are separated from their arguments (and arguments from each other) using at least two spaces.

```{note}
Keywords are defined in keyword libraries and as user keywords, and they can be imported into a test in the `Settings` section.

Keyword libraries can be Python libraries or XML-RPC services.
User keywords are just lists of test clauses reusing existing keywords or other user keywords.
User keywords are described in the test suite, or imported from resource files.
```

## Test scenarios

There are several ways to write robot test scenarios. In Plone we choose the `Given-When-Then style`.

This format is very useful because allows you to write test cases that everyone can understand, as they are written in a familiar way.

When you write test cases in this style, you express the initial state with a keyword starting with word `Given`,
actions with keywords starting with the word `When` and the expectations with a keyword starting with the word `Then`.

```{note}
Keyword starting with `And` or `But` may be used if a step has more than one action.
```

Let's see how a keyword works. In our example, we have this scenario:

```{literalinclude} _snippets/test_example.robot
:language: none
:lines: 37-40
```

The initial state is the keyword that starts with "Given":

```{literalinclude} _snippets/test_example.robot
:language: none
:lines: 39
```

This keyword is a set of sequential actions (defined in the Keywords section):

```{literalinclude} _snippets/test_example.robot
:language: none
:lines: 48-50
```

First, we open the login_form page. We wait for the page to be loaded and for the two fields to be available in HTML.

```{note}
\$\{PLONE_URL} is a global variable defined in an plone.app.robotframework imported library.
```

After a Given statement, there is a list of actions (`When`), and a final expectation (`Then`) that has the same structure.

```{note}
Most of these actions come from the default Selenium library (imported in the Settings section).
You can find a list of [available actions online](https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#Keywords).

For standard Plone actions and keywords, see the imported files (`keywords.robot` and `selenium.robot`).
```

## Running robot tests

A package created with plonecli is already configured to run robotframework tests.

To use robotframework tests in your package, you need the `plone.app.robotframework` dependency in the `setup.py` file.

There is also a `robot` part in the `base.cfg` file. This configuration isn't required to run robot tests, but it
installs two helper scripts for writing tests:

- `bin/robot-server` starts a temporary Plone site with the given test layer set up
- `bin/robot` executes Robot Framework’s pybot-runner so that it will run the given test suite against the running robot-server, ensuring that tests will be run in isolation (i.e., the database is cleaned up between tests)

```{literalinclude} _snippets/buildout.cfg
:language: ini
:lines: 78-81
```

We can run robot tests along with other tests, using this command:

```shell
plonecli test --all
```

Or, as with any other test, we can run only a single test using this command:

```shell
plonecli test -s plonetraining.testing -t test_example.robot --all
```

These commands take time because each test case needs to start a server, open a new browser window and then execute keywords and await the server reponse.

When we are developing our tests, we can speedup this process, keeping a robot-server instance always up with this command:

```shell
bin/robot-server --reload-path src plonetraining.testing.testing.PLONETRAINING_TESTING_ACCEPTANCE_TESTING
```

This command will start a robotframework server that also instantiates a Plone instance.

This has a second advantage: you can inspect the Plone site every time and try things manually before writing actions in the test.

With robot server running, we can run test cases with this command:

```shell
bin/robot /src/plonetraining/testing/tests/robot/test_example.robot
```

```{note}
These development helpers worked well, up to and including Plone 5.1. At the moment, there are problems starting a robot-server instance using Plone 5.2 and WSGI.
```

## Debugging robot tests

Debugging a robot framework test can be hard because there could be problems in the server or in the client.

Test execution could be very slow and difficult to follow for a human, so we can slow it down to better understand what's happening:

```none
*** Settings ***

Suite setup  Set Selenium speed  2s
```

Alternatively, we could pause (or set a sleep timeout on) the execution of a test, and use the time to manually inspect the site:

```none
*** Test Cases ***

Pause tests with included Pause-keyword
  Pause

Pause tests for 10 minutes and then continue
  Sleep  10 min
```

Finally, we could also pause the test execution and test keywords using the console:

```none
*** Test Cases ***

Start interactive debugger
    Import library  DebugLibrary
    Debug
```

```{note}
There are more detailed examples in the [Plone robot framework documentation](https://5.docs.plone.org/external/plone.app.robotframework/docs/source/debugging.html).
```

## Test reports

If we run a robot framework test using the `plonecli test` command, we have the usual console output that tells us if a test succeeded or failed.

Robot tests are a combination of backend and frontend environments, so it isn't easy to have all information about the test status in the console.

For that reason, the robot framework generates detailed reports in the `parts/test` folder where you can see the status of the last test execution and detailed information on each test case.

### Exercise 1

Let's write our first robot test!

Try to write some basic scenarios:

- Login to the site and create a new TestType content item
- Visit the TestType view, passing a custom message in the query string

```{note}
plonecli created a basic robot test for our TestType content type, so the first part of the exercise could be copied from it.
Try not copying it and try using the robot framework syntax by yourself.

In the [robot framework documentation](https://5.docs.plone.org/external/plone.app.robotframework/docs/source/index.html) you can find some information that can help you write your first robot framework test.
```

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{literalinclude} _snippets/test_ct_testing_item.robot
:language: text
:lines: 35-99
```
````

### Exercise 2

Now let's test something that we can't test using functional tests: JavaScript.

- Add a basic mockup pattern to testing-item-view (for example, the [autotoc](https://plone.github.io/mockup/dev/#pattern/autotoc) pattern)
- Check that the table of contents is rendered on the page

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

> First, add autotoc to the template:
>
> ```{literalinclude} _snippets/testing_item_view_toc.pt
> :emphasize-lines: 13-28
> :language: html
> :lines: 1-28, 44-46
> ```
>
> Now, create a test case that checks autotoc:
>
> ```{literalinclude} _snippets/test_autotoc.robot
> :language: text
> :lines: 35-42, 57-74, 79-84
> ```
````

### Exercise 3

For the last JavaScript test, try to simulate clicks.

- The autotoc pattern can also be used for generate tabs.
- Check that clicking on tabs results in changes to the document object model (DOM).

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

> Add tabs to the template:
>
> ```{literalinclude} _snippets/testing_item_view_toc.pt
> :emphasize-lines: 29-43
> :language: html
> ```
>
> Update the previous test with more test cases:
>
> ```{literalinclude} _snippets/test_autotoc.robot
> :emphasize-lines: 43-54,76-77,85-88
> :language: text
> ```
````
