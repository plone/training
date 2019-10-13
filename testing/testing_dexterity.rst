Testing a Dexterity content-type
================================

The most common thing that we could develop in Plone are content-types.
Let's see how to test if a new content-type works like expected.

Create a new content-type
-------------------------

With plonecli we could add features on our package through command-line.

For example, let's create a new ``TestingItem`` content-type:

.. code-block:: console

  $ cd plonetraining.testing
  $ plonecli add content_type



With this command, plonecli will ask you some questions and will register new content-type in our package.

.. note::

    To follow this training, you need to ask questions like this:
    - Content type name (Allowed: _ a-z A-Z and whitespace) [Todo Task]: TestingItem

    - Content type description:

    - Use XML Model [y]: n

    - Dexterity base class (Container/Item) [Container]: Item

    - Should the content type globally addable? [y]: y

    - Create a content type class [y]: y

    - Activate default behaviors? [y]: y


Test the content-type
---------------------

If we now try to re-run tests, we could see that the tests number has increased.
This is because plonecli also creates a basic test for this new content-type in ``tests/test_ct_testing_item.py`` file:

.. literalinclude:: _snippets/test_ct_testing_item.py
        :language: python
        :lines: 25-69
        :emphasize-lines: 3,5-9


We can see some interesting things:

- We are using ``PLONETRAINING_TESTING_INTEGRATION_TESTING`` layer, because we don't need to write functional tests
- We are using ``setUp`` method to set some variables and add some roles to the testing user.


In these tests, we are testing some very basic stuffs for our content-type like for example if it's correctly registered in FTI, if we can create it
and if an user with a specific role (Contributor) can add it.

.. note::

    plone.app.testing gives us a default user for tests. We could import its username in a variable called ``TEST_USER_ID`` and set different roles when needed.

    By default each test is run with that user as logged-in user. If we want to run tests as anonymous users or with a different user, we need to logout/login.


Excercise 1
+++++++++++

- Change the permissions for our newly content-type and only allow Manager to add it.
- Fix old tests.
- Create a new one to test that Contributor can't add these types. 

..  admonition:: Solution
    :class: toggle

    In ``rolemap.xml``:

    .. code-block:: xml

        <permission name="plonetraining.testing: Add TestingItem" acquire="True">
            <role name="Manager"/>
        </permission>

    In test case file we need to import a new Exception:
    
    .. literalinclude:: _snippets/test_ct_testing_item.py
        :language: python
        :lines: 2

    And then update tests like this:

    .. literalinclude:: _snippets/test_ct_testing_item.py
        :language: python
        :lines: 50,52-63, 65-76

Functional test
---------------

Until now we wrote only ``ìntegration`` tests because we didn't needed to test browser integration or commit some transactions.

As previously said, if we don't need to create a functional test, it's better to avoid them because they are slower than integration ones.

.. note::

    It's always better avoiding transactions in tests because they invalidate the isolation between tests in the same test case.
    
    If we commit a transaction in one test, we persist that write into our testing database, and our changes are visible also in following tests in the same test case.

We could try to create a ``functional`` test just to see how they works and to test how our content-type creation works on browser.

Let's create a new test case in the same file.

First of all we need to import some new dependencies:

.. literalinclude:: _snippets/test_ct_testing_item.py
    :language: python
    :lines: 5,6,9,10

And then we can create a new test case:

.. literalinclude:: _snippets/test_ct_testing_item.py
    :language: python
    :lines: 78-123
    :emphasize-lines: 3,11-17
    

The first thing that we can see, is the new layer used: ``PLONETRAINING_TESTING_FUNCTIONAL_TESTING``.

In ``setUp`` we configure the test case to use the Zope web browser and we login as site owner.

In ``test_add_testing_item`` we simulate user interaction on creating a new content from the browser with following actions:

- Open the url for adding a new TestingItem content
- Find the title field and compile it
- Click to Save button
- Check that after saving it, we can see its title.

In ``test_view_testing_item`` we are checking that accessing directly to a content with his url, we can see some informations.

.. note::

    ``self.browser.contents`` shows the html of the last visited page.


Excercise
+++++++++

Try to add a behavior (for example a rich text field) to our content-type and check that the field is showed up in edit form and in the view.

..  admonition:: Solution
    :class: toggle

    In ``TestingItem.xml`` uncomment ``plone.richtext`` behavior.

    In test case file:

    .. literalinclude:: _snippets/test_ct_testing_item.py
        :language: python
        :lines: 125-137
