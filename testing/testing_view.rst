Testing a view
==============

Another base Plone feature that we can test, is a View.

Create a new view
-----------------

Create a new view with plonecli:

.. code-block:: console

  $ cd plonetraining.testing
  $ plonecli add view

Follow prompt wizard and create a new view with with ``TestingItemView`` Python class and a template.

With this command, a new view will be automatically registered in our package.

Test the view
-------------

Like for Dexterity types, also for views ``plonecli`` created some basic tests (in ``test_view_testing_item_view.py`` file).

Inspecting this file, we could see something like this:

.. literalinclude:: _snippets/test_view_testing_item_view.py
    :language: python
    :lines: 17-26, 28,29, 31-34, 39-50

On ``setUp`` we are creating some example contents that we are going to use in tests.

The first test (``test_testing_item_view_is_registered``) tries to call the view on a Folder and checks that everything works well and we get the correct view.

The second one (``test_testing_item_view_not_matching_interface``), tries to call the view on a non-folderish content (a Document) and checks that this action raises an Exception.

If we take a look to the configre.zcml file where the view is registered, we can see that it's registered for folderish types, so that's the reason of these tests.

With a view we could test several things:

- If it is available only for a certain type of objects
- If it renders like we expected (calling the view in an Integration test, or using the browser in a Functional test)
- If its methods returns what we expects (calling methods directly from the view instance)

Excercise 1
+++++++++++

We want to use this view only for our content-type and not for all folderish ones (also because TestingItem isn't a folderish type).

- Change view registration to be available only for our type
- Update tests to check that we can call it only on a TestingItem content
- The view template prints a string that is returned from its class. Write a test that checks this thing.

..  admonition:: Solution
    :class: toggle

    TestingItem objects implements ``ITestingItem`` interface, so we need to update view registration like this:
    
    .. code-block:: xml

        <browser:page
            name="testing-item-view"
            for="plonetraining.testing.content.testing_item.ITestingItem"
            class=".testing_item_view.TestingItemView"
            template="testing_item_view.pt"
            permission="zope2.View"
            />
        
    Then our ``test_view_testing_item_view`` will become like this:

    .. literalinclude:: _snippets/test_view_testing_item_view.py
        :language: python
        :lines: 21-29, 36-50, 52-64
        :emphasize-lines: 7, 11, 25-28

.. note::

    plonecli uses ``getMultiAdapter`` to get a view and we keep it for coherence in pre-created tests, but preferred way is the plone.api one.

Excercise 2
+++++++++++

- Add a method in the view that get a parameter from the request (``message``) and returns it (it's a dumb method, but it's just an example).
- Check the method in integration test
- Update the template to print the value from that method
- Test that calling the method from the view, it returns what we expect
- Write a functional test to test browser integration

..  admonition:: Solution
    :class: toggle

    First of all we need to implement that method in our view class in ``views/testing_item_view.py`` file:

    .. literalinclude:: _snippets/testing_item_view.py
        :language: python
        :lines: 9-20
        :emphasize-lines: 11-12

    Then we could add this message into the template in ``views/testing_item_view.pt``

    .. literalinclude:: _snippets/testing_item_view.pt
        :language: html
        :emphasize-lines: 10-12

    And finally we could test everything. First of all, let's add an integration test for the method:

    .. literalinclude:: _snippets/test_view_testing_item_view.py
        :language: python
        :lines: 65-81

    Now we can create a functional test:

    .. literalinclude:: _snippets/test_view_testing_item_view.py
        :language: python
        :lines: 83-145
    