Testing in Plone
================

Types of test
-------------

Plone is using some common terminology for types of tests you might have heard elsewhere. But in Plone, these terms are usually used to differenciate the technical difference between the types of test.

Unit tests
~~~~~~~~~~

These match the normal meaning the most. Unit tests test a unit in isolation. That means there is no database, no component architecture and no browser. This means, the code is very fast and it can mean that you can't test all that much if your code mostly interacts with other components.

A unit test for a browser view would create an instance of the view directly. That means, it is your responsability to provide a proper context and a proper request. You can't really test user dependent behavior because you just mock a Request object imitating a user or not. This code might be broken with the next version of Plone without the test failing.

On the other hand, testing a complex rule with many different outcomes is still best tested in a unit test, because they are very fast.

Integration tests
~~~~~~~~~~~~~~~~~

Integration tests in Plone mean, you have a real database and your component architecture. You can identify an integration test by the layer it is using which is based on an layer with integration in its name. We will explain shortly, what a layer is.

Integration tests also means your test is still quite fast, because the transaction mechanisms are used for test isolation. What does that mean? After each test, the transaction gets cancelled and you have the database at the same state as before. It still takes a while to set up the test layer, but running each test is quite fast. But this also means, you cannot commit a transaction. Most code does not commit transactions and this is not an issue.

Functional tests
~~~~~~~~~~~~~~~~

Functional ests in Plone have a real database and a component architectore, like Integration tests. In addition you can simulate a browser in python code. When this browser tries to access a page, the complete transaction machinery is in use. For this to work, the test layer wraps the database into a demostorage. A Demostorage is for demonstration. A demostorage wraps a regular storage. When something gets written into the database, the demostorage stores it into memory or temporary fields. On reading it either returns what has been saved in memory or what is in the underlaying storage.
After each test, the demostorage is wiped. This should make it nearly as fast as integration tests, but there is an additional overhead, when requests get through the transaction machinery.
Also, the browser is pure python code. It does know nothing about javascript. You cannot test your javascript code with functional tests

Acceptance tests
~~~~~~~~~~~~~~~~

Acceptance tests are usually tests that can assert that an application would pass the requirements the customer gave. This implies that acceptance tests test the complete funcionality and that they either allow the customer to understand what is being tested are at least clearly map to business requirements.
In Plone, acceptance tests are tests written with the so called robot framework. Here you write tests in something resembling a natural language and which is driven by a real web browser. This implies you can also test Javascript.
This is the slowest form of testing but also the most complete.
Also, acceptance tests aren't limited to the original form of acceptance tests, but also for normal integration tests.

Javascript tests
~~~~~~~~~~~~~~~~
So far, it looks like we only have acceptance tests for testing javascript. Acceptance tests are also very new. This means, we had no test story for testing javascript.
In Plone 5, we have the mockup framework to write javascript components and the mockup framework provides also scaffolding for testing Javascript with xxx. While these tests use a real browser of some sort, they fall into the category of unit tests, because you have no database Server available to generate proper html.

Doctests
~~~~~~~~
Doctests are a popular way to write tests in documentation. Doctests parse documentation for code that has special formatting and runs the code and compares it with the output suggested in the documentation.
Doctests are hard to debug, because there is no easy way to use a debugger in doctests. Doctests have a bad reputation, because when it came around, people thought they could write documentation and tests in one go. This resulted in packages like zope.component, where the documentation on pypi slowly transforms into half sentences split up by 5-10 lines of code testing an obscure feature that the half sentence does not properly explain.
In Plone, this form of testing is not very common.
We would like to transform our documentation to be testable with doctests.

Writing tests
-------------

Writing tests is an art. If your testsuite needs half an hour to run, it looses a lot of value. If you limit yourself to unit tests and fake everything, you loose many bugs, either because Plone works different to what you thought, or the next Plone versions run different from todays.
On the other hand, the more integrational tests are not only slower, but often create test failures for away from the actual error in code. Not only run the tests slower, it takes also longer to debug why they fail.
Here are some good rules to take into account.

If you need to write many test cases for a browser view, you might want to factor this out into a component of its own, in such a way that this component can easily be tested as a unit tests.
If, for example, you have a list view that shall do a specific way of sorting, depending on gender, language and browser of a user, write a component that takes a list of names to sort, gender, language and browser as strings.
This code can easily be tested for all combinations in unit tests, while extracting gender, language and browser from a request object takes only a few functional tests.

Try not to mock code. The mocking code you generate mock Plone in the version you are using today. The next version might work different.

Do not be afraid to rewrite your code for better testability. It pays off.

If you have highly complex code, think about structuring code and data structures in such a way that they have no side effects. For one customer I wrote a complex ruleset of about 400 lines of code. A lot of small methods that have no side effects. It took a bit to write that code and corresponding tests, but until today this code did not have a single failure.

Steal from others. Unfortunately, it sometimes takes an intrinsicate knowledge to know how to test some functionality. Some component functionality that is automatically handled by the browser must be done by hand. And the component documentation has been referenced in this chapter as a terrible example alreadySo, copy your code from somewhere else.

Normally, you write a test that tests one thing only. Don't be afraid to break that rule than necessary. If, for example, you built some complex logic that involves multiple steps, don't shy away from writing a longer test showing the normal. good case. Add lots of comments explaining in each step what is happening, why and how. This helps other developers and the future you.

Plone tests
-----------

Plone is a complex system to run tests in. Because of this, we use a functionality from the zope.testrunner, layers. We use the well known unittest framework which exhibits the same ideas as nearly every unittest framework out there. In addition for test setups we have the notion of layers. A layer is a testsetup that can be shared. This way, you can run tests from 20 different test suites but not each testsuite sets up their own complete Plone site. Instead, you use a Layer, and the testrunner takes care that every testsuite sharing a layer are run together.

Usually, you create a three layers on your own, an integration layer, a functional layer and an acceptance test layer. If you were to test code that uses the Solr search engine, you'd use another layer that starts an stops solr between tests. But most of the time you just use the default layers you copied from somewhere or that mr.bob gave you.

By convention, layers are defined in a module ``testing`` in your module root, ie ``my.code.testing``. Your test classes should be in a folder named ``tests``


Getting started
---------------

Mr.bob already created the testing layers.
We will go through them now.

Next, it adds a method for testing that it gets properly installed. This might look stupid, but it isn't if you take into account that in plone land, things change with new releases. Having a GenericSetup profile installing Javascript files contains the assumption, that the package wants a javascript file available in Plone.
This assumption is explained in the syntax of the current Plone. By testing that the result is met, the Javascript file really is available, we spell out that assumption more clearly.
The person that wants to make your package work 5 years from now, knows now that the result in his browser might be related to a missing file. Even if he does not understand the semantics from the old Plone on how to register js files, he has a good starting point on what to do to make this package compatibles.

This is why it makes sense to write these, tedious tests.


