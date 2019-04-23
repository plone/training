Testing
=======

**Agenda**

- What is a test?
- Apparent issues with tests
- Why do we test?
- Testable code
- How to run tests
- Unittest
- Test-types
- The Testing-Pyramid
- Test-Setup in Plone
- plone.app.testing
- Test-Layers
- Functional tests
- Managing dependencies in tests
- Coverage
- Testing events
- Mocking
- Property based testing
- Testing views
- The process
- Handling Regressions
- Test data vs. real data
- Test-profiles


*More topics*

* What to tests and what not to tests?
* Examples of different tests from the Plone Core
* ftw.testing
* ftw.testbrowser
* CI-Systems: Travis, Gitlab-CI, Jenkins
* Javascript Testing
* Robottests
* Why not pytest


What is a test?
---------------

A piece of code that proves that some part of a programm works in a certain way.


Apparent issues with tests
--------------------------

- Testing is not easy (additional skills)
- Tests are code -> Cost of maintenance
- Setup, Test-Fixures is hard and doe not translate to application-development
- Infrastructure (CI-Server) needs to be bought and maintained
- Test-Isolation can be hard
- Value is not apparent -> Hard sell


Why do we test?
---------------

- Confidence
- Easier Refactoring and Extending
- Better Design and Code-Quality
- Protection from Regressions
- Faster Development


Testable code
-------------

- Isolation of concerns
- Code without plone-dependencies should not live in a class
- Test Driven Development und Alternativen


How to run tests
----------------

Test are run with ``./bin/test``. This uses `zope.testrunner <https://zopetestrunner.readthedocs.io/en/latest/>`_.

The most important options:

-t test
    Specify test names (one or more regexes). Can be the tese-method name, the class or the filename. Negate with a leading "!"

-s package
    Run tests for one specific package.

-D
    enable post-mortem debugging of test failures

--help
    show all command-line options (there are many more!)

--all
    Run all tests of all layers (including robot tests):

Options: https://pypi.python.org/pypi/zope.testrunner#some-useful-command-line-options-to-get-you-started


Examples:

``./bin/test -t test_adding``
    Run the test ``test_adding``

``./bin/test --all '!.robot'``
    Run all robot-tests

``./bin/test -s plone.app.contentypes``
    Run all test of the package plone.app.contentypes

``./bin/test -t FaqItemIntegrationTest -D``
    Run all test in the class ``FaqItemIntegrationTest`` and open a pdb on a error.


Unittest
--------

- structure of a test
- methods
- assert-statements
- See :doc:`unittest.rst`


Test-types
----------

- Unittests
- Integration Tests
- Functional Tests
- Acceptance Tests

Plus:

- Doctests

Difference between IntegrationTesting and FunctionalTesting:

"IntegrationTesting class will create a new transaction for each test and roll it back on test tear- down, which is efficient for integration testing, whilst FunctionalTesting will create a stacked DemoStorage for each test and pop it on test tear- down, making it possible to exercise code that performs an explicit commit (e.g. via tests that use zope.testbrowser)."

Unittest:

.. code-block:: python

    class TestSimplevoc(unittest.TestCase):

        def test_simplevoc(self):
            from kbo.webapp import utils
            values = [u'Vorstandskonferenzbeschluß- gut', u'Änderungsvorschlag']
            voc = utils.simplevoc(values)
            self.assertEqual(
                [i.value for i in voc],
                [u'vorstandskonferenzbeschluss_gut', u'aenderungsvorschlag'],
            )
            values2 = [
                u' Nicht so gut ',
                u'nicht  so  gut',
            ]
            self.assertRaises(ValueError, utils.simplevoc, values2)

        def test_safe_value(self):
            from kbo.webapp import utils
            self.assertEqual(utils.safe_value(u'München Üçø'), 'muenchen_ueco')
            self.assertEqual(utils.safe_value('üöä'), 'ueoeae')

Integration Test

.. code-block:: python

    class FaqFolderIntegrationTest(unittest.TestCase):

        layer = VDIVDEIT_FAQ_INTEGRATION_TESTING

        def test_add_faqfolder(self):
            obj = api.content.create(
                container=self.portal,
                type='FaqFolder',
                id='testfolder')
            self.assertTrue(IFaqFolder.providedBy(obj))

Functional Test

.. code-block:: python

    class TaskFunctionalTest(unittest.TestCase):

        layer = PLONETRAINING_TESTING_FUNCTIONAL_TESTING

        def setUp(self):
            app = self.layer['app']
            self.portal = self.layer['portal']
            self.portal_url = self.portal.absolute_url()
            self.browser = Browser(app)
            self.browser.handleErrors = False
            self.browser.addHeader(
                'Authorization',
                'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
            )

        def test_add_task(self):
            self.browser.open(self.portal_url + '/++add++Task')
            self.browser.getControl(name="form.widgets.title").value = 'My Task'
            self.browser.getControl(name='form.widgets.description').value = 'This is my task'
            self.browser.getControl('Save').click()
            self.assertEqual('My Task', self.portal['my-task'].title)

        def test_view_task(self):
            setRoles(self.portal, TEST_USER_ID, ['Manager'])
            api.content.create(
                container=self.portal,
                type='Task',
                id='my-task',
                title='My Task',
            )
            import transaction
            transaction.commit()
            self.browser.open(self.portal_url + '/my-task')
            self.assertTrue('My Task' in self.browser.contents)


The Testing-Pyramid
-------------------

.. code-block::

          = Acceptance Tests =
         == Functional Tests ==
       ==== Integration Tests ===
    ========== Unittests ===========

Does not really apply to Plone: We rarely write pure unittests. In a CMS most custom code only works in combination with the content to manage.


Test-Setup in Plone
-------------------

``buildout.cfg``:

.. code-block:: ini

    [test]
    recipe = zc.recipe.testrunner
    eggs =
        Plone
        ${buildout:test-eggs}
    defaults = ['--auto-color', '--auto-progress', '-vvv']


``testing.py``:

.. code-block:: python

    # -*- coding: utf-8 -*-
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
    from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
    from plone.app.testing import applyProfile
    from plone.app.testing import FunctionalTesting
    from plone.app.testing import IntegrationTesting
    from plone.app.testing import PloneSandboxLayer
    from plone.testing import z2

    import project.site


    class ProjectSiteLayer(PloneSandboxLayer):

        defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

        def setUpZope(self, app, configurationContext):
            # Load any other ZCML that is required for your tests.
            # The z3c.autoinclude feature is disabled in the Plone fixture base
            # layer.
            self.loadZCML(package=project.site)

        def setUpPloneSite(self, portal):
            applyProfile(portal, 'project.site:default')


    PROJECT_SITE_FIXTURE = ProjectSiteLayer()


    PROJECT_SITE_INTEGRATION_TESTING = IntegrationTesting(
        bases=(PROJECT_SITE_FIXTURE,),
        name='ProjectSiteLayer:IntegrationTesting'
    )


    PROJECT_SITE_FUNCTIONAL_TESTING = FunctionalTesting(
        bases=(PROJECT_SITE_FIXTURE,),
        name='ProjectSiteLayer:FunctionalTesting'
    )


    PROJECT_SITE_ACCEPTANCE_TESTING = FunctionalTesting(
        bases=(
            PROJECT_SITE_FIXTURE,
            REMOTE_LIBRARY_BUNDLE_FIXTURE,
            z2.ZSERVER_FIXTURE
        ),
        name='ProjectSiteLayer:AcceptanceTesting'
    )


``setup.py``:

.. code-block:: python

    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },

- Always use the template provided by bobtemplates.plone
- To save time on upgrading you could even create a new package wih the same name and copy the code and tests into it.


There are several hooks to setup and teardown

testing.py:

- setUpZope(self, app, configurationContext)
- setUpPloneSite(self, portal)
- tearDownPloneSite(self, portal)
- tearDownZope(self, app)

test_xxx.py:

- setUp(self)
- tearDown(self)


plone.app.testing
-----------------

- http://docs.plone.org/external/plone.app.testing/docs/source/index.html

helper-methods for user-management: http://docs.plone.org/external/plone.app.testing/docs/source/README.html#user-management

Product and profile installation: http://docs.plone.org/external/plone.app.testing/docs/source/README.html#product-and-profile-installation

Usefull Variables like PLONE_SITE_ID. See plone.app.testing.interfaces


Test-Layers
-----------

Layers create test fixtures that can be shared by multiple tests. For example, set up a database and configure components to access that database.

This type of test fixture setup is resource-intensive and time-consuming. Layers allow to save time by performing the setup and tear-down only once for a set of tests without losing isolation between those tests.

https://pypi.python.org/pypi/plone.testing/5.0.0#layer-basics

plone.app.testing has some usefull layers that can be reused:

http://docs.plone.org/external/plone.app.testing/docs/source/README.html#layer-reference

Example: ``MOCK_MAILHOST_FIXTURE``: sending an email will instead store each email as a string in ``portal.MailHost.messages``.

.. code-block:: python

    from plone.app.testing import MOCK_MAILHOST_FIXTURE

    MY_INTEGRATION_TESTING = IntegrationTesting(
        bases=(
            MY_FIXTURE,
            MOCK_MAILHOST_FIXTURE,
        ),
        name="MyFixture:Integration"
    )

In Plone 5 most addons should use ``plone.app.contenttypes.testing. PLONE_APP_CONTENTTYPES_FIXTURE`` as the base for their layers, which is a instance of ``plone.app.contenttypes.testing.PloneAppContenttypes`` and inherits ``plone.app.testing.helpers.PloneSandboxLayer``, ``plone.app.testing.layers.PloneFixture`` and ``plone.testing.z2.Startup``

Based on ``PLONE_APP_CONTENTTYPES_FIXTURE`` each package gets their own layer for each test-type:

- VDIVDEIT_FAQ_INTEGRATION_TESTING
- VDIVDEIT_FAQ_FUNCTIONAL_TESTING
- VDIVDEIT_FAQ_ACCEPTANCE_TESTING

Layer-Variables:

.. code-block:: python

    app = self.layer['app']
    portal = self.layer['portal']
    request = self.layer['request']


Functional tests
----------------

layer = XXX_FUNCTIONAL_TESTING

Use functional tests them when you make a commit or want test what is in the browser.

http://docs.plone.org/external/plone.app.testing/docs/source/README.html#simulating-browser-interaction

Debugging functional tests:

- http://docs.plone.org/external/plone.app.testing/docs/source/README.html#debugging-tips
- http://docs.plone.org/develop/testing/functional_testing.html#preparing-error-logger
- http://docs.plone.org/develop/testing/functional_testing.html#listing-available-form-controls
- http://docs.plone.org/external/plone.app.testing/docs/source/zope-testbrowser.html

Additional info:

* Webtest (replaced mechanize in Zope 4 / Plone 5.2).
* ftw.testbrowser


Managing dependencies in tests
------------------------------

Add dependecies to ``setup.py``.

Install zope-packages in ``setUpZope``

.. code-block:: python

    class MyPackageLayer(PloneSandboxLayer):

        defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

        def setUpZope(self, app, configurationContext):
            self.loadZCML(package=Products.PasswordStrength)
            z2.installProduct(app, 'Products.PasswordStrength')

Coverage
--------

- Why is it relevant?
- Examples
- Configuration
- Artefacts
- Coverage history

http://docs.plone.org/external/plone.testing/src/plone/testing/README.html#coverage-reporting


Testing events
--------------

- http://docs.plone.org/external/plone.testing/src/plone/testing/README.html#event-testing
- https://github.com/plone/plone.registry/blob/master/plone/registry/events.rst#registry-events


Mocking
-------

- You should rather not mock
- Plone changes -> tests might passt when they should not because a feature that changes is mocked
- Only mock your own objects or when you do not care about the behavior of the mocked object:

Examples:

.. code-block:: python

    with self.assertRaises(InvalidParameterError):
        api.content.transition(
            obj=mock.Mock(),
            transition='publish',
            to_state='published',
        )

.. code-block:: python

    @patch('project.site.utils.IIntIds', None)
    def test_without_intid(self):
        self.assertIsNone(get_intid(self.obj))


Property based testing
----------------------

http://hypothesis.works

Passes configurable random parameters to methods:

.. code-block:: python

    from hypothesis import given
    from hypothesis.strategies import text

    @given(text())
    def test_decode_inverts_encode(s):
        assert decode(encode(s)) == s


Testing views
-------------

.. code-block:: python

    def test_view(self):
        doc = api.content.create(
            container=self.portal,
            type='Document',
            id='test-doc')

        view1 = api.content.get_view('view', doc, self.request)
        html1 = view1()

        view2 = doc.restrictedTraverse('view')
        html2 = view2()

        self.assertEqual(html1, html2)

Traversal versus view-lookup:

Traversal will not take IPublishTraverse adapters into account, and you cannot pass query string parameters. In fact, restrictedTraverse() and unrestrictedTraverse() implement the type of traversal that happens with path expressions in TAL, which is similar, but not identical to URL traversal. See http://docs.plone.org/external/plone.app.testing/docs/source/README.html#traversal


The process
-----------

- Create branch
- Test one thing
- Get test to run
- Fix any code-analysis issues
- Commit and push branch
- Create pull-request from branch
- Assign pull-request to someone
- Wait for CI to finish
- Review, comment, fix
- Maybe rebase
- Merge and look at CI


Handling Regressions
--------------------

- Write test that fails (regression-test)
- Fix issues
- See that test now passes


Test data vs. real data
-----------------------

- Create application-structure and content in tests
- Makes it harder to maintain when the structure changes
- Keep a copy of the DB for manual testing

Code to create dummy-content: https://training.plone.org/5/mastering_plone/user_generated_content.html#exercise-1


Test-profiles
-------------

``configure.zcml``:

.. code-block:: xml

    <genericsetup:registerProfile
        name="testing"
        title="project.site Testing"
        directory="profiles/testing"
        description="Minimal testing content for project.site add-on"
        provides="Products.GenericSetup.interfaces.EXTENSION"
        post_handler=".setuphandlers.testing"
        />

    <genericsetup:registerProfile
        name="demo"
        title="project.site Demo"
        directory="profiles/demo"
        description="Demo content for project.site add-on"
        provides="Products.GenericSetup.interfaces.EXTENSION"
        post_handler=".setuphandlers.demo"
        />

``metadata.xml`` of the profile "testing"

.. code-block:: xml

    <?xml version="1.0"?>
    <metadata>
      <version>1000</version>
      <dependencies>
        <dependency>profile-kbo.webapp:default</dependency>
      </dependencies>
    </metadata>

``setuphandlers.py``:

.. code-block:: python

    def post_install(setup):
        delete_example_content()
        create_base_structure()
        apply_some_settings()


    def testing(setup):
        create_users_and_groups(setup)
        create_test_content()


    def demo(setup):
        portal = api.portal.get()
        todos = get_todos(setup)
        create_test_todos(portal, todos)
        create_test_activities()
        create_test_decisions(portal)
        meetings = get_random_meetings()
        create_test_meetings(portal, meetings)



