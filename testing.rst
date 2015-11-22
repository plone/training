.. _testing-label:


Testing in Plone
================

In this chapter we:

  * Write tests

Topics covered:

  * Testing best practices
  * Internals of Plone

.. _testing-types-label:

Types of tests
--------------

.. only:: presentation

   * Unit tests
   * Integration tests
   * Functional tests
   * Acceptance tests
   * Javascript tests
   * Doctests

.. only:: not presentation


    Plone is using some common terminology for types of tests you might have heard elsewhere. But in Plone, these terms are usually used to differentiate the technical difference between the types of test.

    Unit tests
    ~~~~~~~~~~

    These match the normal meaning the most. Unit tests test a unit in isolation. That means there is no database, no component architecture and no browser. This means the code is very fast and it can mean that you can't test all that much if your code mostly interacts with other components.

    A unit test for a browser view would create an instance of the view directly. That means it is your responsibility to provide a proper context and a proper request. You can't really test user-dependent behavior because you just mock a Request object imitating a user or not. This code might be broken with the next version of Plone without the test failing.

    On the other hand, testing a complex rule with many different outcomes is still best tested in a unit test, because they are very fast.

    Integration tests
    ~~~~~~~~~~~~~~~~~

    Integration tests in Plone mean you have a real database and your component architecture. You can identify an integration test by the layer it is using which is based on a layer with integration in its name. We will explain shortly what a layer is.

    Integration tests also means your test is still quite fast, because the transaction mechanisms are used for test isolation. What does that mean? After each test, the transaction gets canceled and you have the database in the same state as before. It still takes a while to set up the test layer, but running each test is quite fast. But this also means you cannot commit a transaction. Most code does not commit transactions and this is not an issue.

    Functional tests
    ~~~~~~~~~~~~~~~~

    Functional tests in Plone have a real database and a component architecture, like Integration tests. In addition, you can simulate a browser in python code. When this browser tries to access a page, the complete transaction machinery is in use. For this to work, the test layer wraps the database into a demostorage. A Demostorage is for demonstration. A demostorage wraps a regular storage. When something gets written into the database, the demostorage stores it into memory or temporary fields. On reading it either returns what has been saved in memory or what is in the underlaying storage.
    After each test, the demostorage is wiped. This should make it nearly as fast as integration tests, but there is an additional overhead, when requests get through the transaction machinery.
    Also, the browser is pure python code. It knows nothing about javascript. You cannot test your javascript code with functional tests

    Acceptance tests
    ~~~~~~~~~~~~~~~~

    Acceptance tests are usually tests that can assert that an application would pass the requirements the customer gave. This implies that acceptance tests test the complete functionality and that they either allow the customer to understand what is being tested or at least clearly map to business requirements.
    In Plone, acceptance tests are tests written with the so called robot framework. Here you write tests in something resembling a natural language and which is driven by a real web browser. This implies you can also test Javascript.
    This is the slowest form of testing but also the most complete.
    Also, acceptance tests aren't limited to the original form of acceptance tests, but also for normal integration tests.

    Javascript tests
    ~~~~~~~~~~~~~~~~
    So far, it looks like we only have acceptance tests for testing javascript. Acceptance tests are also very new. This means we had no test story for testing javascript.
    In Plone 5, we have the mockup framework to write javascript components and the mockup framework provides also scaffolding for testing Javascript with xxx. While these tests use a real browser of some sort, they fall into the category of unit tests, because you have no database Server available to generate proper html.

    Doctests
    ~~~~~~~~
    Doctests are a popular way to write tests in documentation. Doctests parse documentation for code that has special formatting and runs the code and compares it with the output suggested in the documentation.
    Doctests are hard to debug, because there is no easy way to use a debugger in doctests. Doctests have a bad reputation, because when it came around, people thought they could write documentation and tests in one go. This resulted in packages like zope.component, where the documentation on pypi slowly transforms into half sentences split up by 5-10 lines of code testing an obscure feature that the half sentence does not properly explain.
    In Plone, this form of testing is not very common.
    We would like to transform our documentation to be testable with doctests.

.. _testing-writing-label:

Writing tests
-------------

.. only:: presentation

   * Testing is hard
   * Slow tests kill testing
   * It is ok to rewrite code for better testability
   * Steal from others
   * All rules and best practices have exceptions

.. only:: not presentation

    Writing tests is an art. If your testsuite needs half an hour to run, it loses a lot of value. If you limit yourself to unit tests and fake everything, you miss many bugs, either because Plone works differently than what you thought, or the next Plone versions run differently from today's.
    On the other hand, integration tests are not only slower, but often create test failures far away from the actual error in the code. Not only do the tests run more slowly, it also takes longer to debug why they fail.
    Here are some good rules to take into account.

    If you need to write many test cases for a browser view, you might want to factor this out into a component of its own, in such a way that this component can easily be tested with unit tests.
    If, for example, you have a list view that shall do a specific way of sorting, depending on gender, language and browser of a user, write a component that takes a list of names to sort, gender, language and browser as strings.
    This code can easily be tested for all combinations in unit tests, while extracting gender, language and browser from a request object takes only a few functional tests.

    Try not to mock code. The mocked code you generate mocks Plone in the version you are using today. The next version might work differently.

    Do not be afraid to rewrite your code for better testability. It pays off.

    If you have highly complex code, think about structuring code and data structures in such a way that they have no side effects. For one customer I wrote a complex ruleset of about 400 lines of code. A lot of small methods that have no side effects. It took a bit to write that code and corresponding tests, but as of today this code did not have a single failure.

    Steal from others. Unfortunately, it sometimes takes an intrinsic knowledge to know how to test some functionality. Some component functionality that is automatically handled by the browser must be done by hand. And the component documentation has been referenced in this chapter as a terrible example already. So, copy your code from somewhere else.

    Normally, you write a test that tests one thing only. Don't be afraid to break that rule when necessary. If, for example, you built some complex logic that involves multiple steps, don't shy away from writing a longer test showing the normal, good case. Add lots of comments explaining in each step what is happening, why and how. This helps other developers and the future you.

Plone tests
-----------

.. only:: presentation

   * Layers


.. only:: not presentation

    Plone is a complex system to run tests in. Because of this, we use a functionality from zope.testrunner: layers. We use the well known unittest framework which exhibits the same ideas as nearly every unittest framework out there. In addition for test setups we have the notion of layers. A layer is a test setup that can be shared. This way, you can run tests from 20 different testsuites but not each testsuite sets up their own complete Plone site. Instead, you use a Layer, and the testrunner takes care that every testsuite sharing a layer are run together.

    Usually, you create three layers on your own, an integration layer, a functional layer and an acceptance test layer. If you were to test code that uses the Solr search engine, you'd use another layer that starts and stops solr between tests. But most of the time you just use the default layers you copied from somewhere or that mr.bob gave you.

    By convention, layers are defined in a module ``testing`` in your module root, ie ``my.code.testing``. Your test classes should be in a folder named ``tests``

Getting started
~~~~~~~~~~~~~~~

Mr.bob already created the testing layers.
We will go through them now.

Next, it adds a method for testing that your add-on gets properly installed. This might seem stupid, but it isn't if you take into account that in plone land, things change with new releases. Having a GenericSetup profile installing Javascript files contains the assumption that the package wants a javascript file available in Plone.
This assumption is explained in the syntax of the current Plone. By testing that the result is met, the Javascript file really is available, we spell out that assumption more clearly.
The person that wants to make your package work 5 years from now, knows now that the result in his browser might be related to a missing file. Even if he does not understand the semantics from the old Plone on how to register js files, he has a good starting point on what to do to make this package compatible.

This is why it makes sense to write these tedious tests.

If nothing else matches, ``test_setup.py`` is the right location for anything GenericSetup related.
In :ref:`eggs1-label` we created a content type. It is time to test this.

We are going to create a test module named ``test_talk``:

.. literalinclude::  ploneconf.site_sneak/chapters/02_export_code_p5/src/ploneconf/site/tests/test_talk.py
    :linenos:

In :ref:`views1-label` we created a new view. We have to test this!
This time, though, we are going to test it with a browser, too.

First, we add a simple test for the custom template in our Functional Test layer

.. literalinclude:: ploneconf.site_sneak/chapters/03_zpt_p5/src/ploneconf/site/tests/test_talk.py
    :lines: 109-125
    :linenos:

Exercise 1
^^^^^^^^^^

We already wrote a talklistview and it is untested!
We like to write unit tests first. But if you look at the Talklistview, you notice that you'd have to mock the portal_catalog, the context, and complex results from the catalog. I wrote earlier that it is ok to rewrite code to make it better testable. But in this example look at what you would test if you mocked everything mentioned above. You would test that your code iterates over a mocked list of mocked items, restructuring mocked attributes.
There is not much sense in that. If you did some calculation, like ratings, things might look different, but not in this case.

We can write an integration test. We should test the good case, and edge cases.
The simplest test we can write is a test where no talks exist.

Then we can create content. Looking through the code, we do not want the talks list to render results for documents. So add a a document. Also, the code does not want to render results for a document out of the current context. So create a folder and use this as a context. Then add a talk outside of this folder. The method iterates over audiences, make sure that you have at least one talk that has multiple audiences and check for that.
Some advanced thing. Should you ever use an improved search system like collective.solr, results might get batched automatically. Check that if you have 101 talks, that you also get back 101 talks.
Think about what you want to check in your results. Do you want to make a one to one comparison? How would you handle UUIDs?

A test creating 101 talks can be slow. It tests an edge case. There is a trick: create a new TestCase Class, and set an attribute ``level`` with the value of 2. This test will then only be run when you run the tests with the argument ``-a 2`` or ``--all``

.. admonition:: Solution
   :class: toggle


       .. literalinclude:: ploneconf.site_sneak/chapters/final/src/ploneconf/site/tests/test_talk.py
           :lines: 56-138
           :linenos:


Robot tests
-----------

Finally, we write a robot test:

.. literalinclude:: ploneconf.site_sneak/chapters/03_zpt_p5/src/ploneconf/site/tests/robot/test_talk.robot
    :linenos:

When you run your tests, you might notice that the robot tests didn't run. This is a feature activated by the robot layer, because robot tests can be quite slow. If you run your tests with ``./bin/test --all``
your robot tests will run. Now you will realize that you cannot work any more because a browser window pops up all the time.

There are 3 possible workarounds:

- install the headless browser, Phantomjs.
  Then run the tests with an environment variable ``ROBOT_BROWSER=phantomjs bin/test --all`` This did not work for me btw.
- Install xvfb, a framebuffer. You wont see the browser then. After installing, start xvfb like this: ``Xvfb :99.0 -screen 0 1024x768x24``. Then run your tests, declaring to connect to the non default X Server: ``DISPLAY=:99.0 bin/test --all``
- Install Xephyr, it is also a framebuffer, but visible in a window. Start it the same way as you start Xvfb.

The first method, with Phantomjs, will throw failures with our tests, unfortunately.

For debugging, you can run the test like this ``ROBOT_SELENIUM_RUN_ON_FAILURE=Debug bin/test --all``. This will stop the test at the first failure and you end up in an interactive shell where you can try various Robot Framework commands.

More information
----------------

For more in-depth information and reference see 

* `plone.app.testing documentation <http://docs.plone.org/external/plone.app.testing/docs/source/index.html>`_.

* `plone.testing package <https://pypi.python.org/pypi/plone.testing>`_ 


