Testing setup
=============

Now let's take a moment (this chapter) to understand how Plone tests works and what's their setup.

To run tests in Plone you need three things:

- Test runner
- Testing setup
- Tests

As previously said, plonecli already creates these things for us, so most of the configuration has already done and we also have
some basic tests to use as starting point.

.. note::

    If you want to add tests from scratch into your product or you want to update testing environment, the best way is to create a new
    package with plonecli with same namespace, and then copy testing files that you need into your product.

Test runner
-----------

A test runner is a script that collect all available tests and execute them.

Plone's test runner is a ``zope.testing`` script called "test" generated with a buildout recipe.

If we inspect ``base.cfg`` file, we could see a `test` part that uses this recipe:

.. code-block:: ini

  [test]
  recipe = zc.recipe.testrunner
  eggs = ${instance:eggs}
  initialization =
      os.environ['TZ'] = 'UTC'
  defaults = ['-s', 'plonetraining.testing', '--auto-color', '--auto-progress']

This particular configuration is made to run tests from our package only by default.

When we execute this script like this:

.. code-block:: console

    ./bin/test

We are actually executing this one:

.. code-block:: console

    ./bin/test -s plonetraining.testing --auto-color --auto-progress

``-s plonetraining.testing`` in particular means that we are executing all tests from a specific test-suite (plonetraining.testing).

.. note::

    If we have a project with several products and we want to test them, we could add a similar configuration in our project's buildout.

    In ``eggs`` option we could list all packages that we want to test.

    If we remove ``'-s', 'plonetraining.testing'`` from defaults, all tests from packages listed in ``eggs`` option will be
    run from default.


Testing setup
-------------

The testing setup for a Plone package is in a file called ``testing.py`` and it looks like this:

.. code-block:: python

  class PlonetrainingTestingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=plonetraining.testing)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plonetraining.testing:default')


  PLONETRAINING_TESTING_FIXTURE = PlonetrainingTestingLayer()


  PLONETRAINING_TESTING_INTEGRATION_TESTING = IntegrationTesting(
      bases=(PLONETRAINING_TESTING_FIXTURE,),
      name='PlonetrainingTestingLayer:IntegrationTesting',
  )


  PLONETRAINING_TESTING_FUNCTIONAL_TESTING = FunctionalTesting(
      bases=(PLONETRAINING_TESTING_FIXTURE,),
      name='PlonetrainingTestingLayer:FunctionalTesting',
  )


  PLONETRAINING_TESTING_ACCEPTANCE_TESTING = FunctionalTesting(
      bases=(
          PLONETRAINING_TESTING_FIXTURE,
          REMOTE_LIBRARY_BUNDLE_FIXTURE,
          z2.ZSERVER_FIXTURE,
      ),
      name='PlonetrainingTestingLayer:AcceptanceTesting',
  )

There are three main pieces:

- Layer definition (PlonetrainingTestingLayer): a layer setup a list of presets for testing environment (called fixtures) and make the packages available in testing environment.
- Package fixture definition: this is the base setup for testing our package (PLONETRAINING_TESTING_FIXTURE).
- Different test types: depending on our needs, we can use different test types like functional or integration tests.

plone.app.testing has a set of base Layers and Fixtures that we use as starting point.


.. note::

    We need to manually load all zcml dependencies because autoinclude is disabled in plone.app.testing to preserve isolation.


Setup and teardown hooks
------------------------

plone.app.testing provides a set of hooks that we can use to do several actions before a test (or suite) runs (setUp) or after it (tearDown).


In testing.py file we usually use these hooks:

- setUpZope(self, app, configurationContext): to configure Zope (mostly importing zcml profiles form the packages that we need to test, and its dependencies)
- setUpPloneSite(self, portal): to configure the actual Plone site. For example installing the product that we are going to test.
- tearDownPloneSite(self, portal): to cleanup some configurations when all tests ends.
- tearDownZope(self, app): to cleanup some configurations when all tests ends.

And they will be called every time a test case uses that layer.

In each test case, we could have the following methods:

- setUp(self)
- tearDown(self)

Usually we use these methods to define some common variables (for example to access to the portal object or the request), to pre-populate the site with some contents or to fix some permissions.

These methods are called for every single test.

Tests
-----

Tests are located into ``tests`` folder.

In this folder you can create as many tests as you want in different files. The only requirement is that they should start with ``test_``.

Tests can be grouped into test cases depending on the test type (unit, functional, integration or robot) and on the functionality that they are testing.

A test case defines which layer should be used, can setup the environment before tests execution (with ``setUp`` method) and can perform some actions after all tests has been executed (with ``tearDown`` method).

plonecli creates a basic test case for testing that the product installs correctly and registers its browserlayer.


Assertions
----------

A test is basically a method that executes something (calling a method, instantiating a Class or trying some more complex behavior) and checks that the result is what we expected.

These checks are made by ``assertions``. They are statements that checks if generated value is the same as the expected one.

If an assertion in a tests fails, the test fails. We could write as much assertions we want in a single test, and they should always succeed.

There are different types of assertions that we can use. For example:

.. code-block:: python

    assertEqual(a, b)
        a == b

    assertTrue(x)
        bool(x) is True

    assertFalse(x)
        bool(x) is False

    assertIsNotNone(x)
        x is not None

    assertIn(a, b)
        a in b

    assertIsInstance(a, b)
        isinstance(a, b)

    assertRaises(exc, fun, *args, **kwds)
        fun(*args, **kwds) raises exc

    assertGreater(a, b)
        a > b

    assertGreaterEqual(a, b)
        a >= b

Each assertion has also a "not" version:

.. code-block:: python

    assertNotEqual(a, b)
        a != b

    assertNotIn(a, b)
        a not in b
