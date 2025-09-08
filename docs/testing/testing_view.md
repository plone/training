---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Testing a view

Another base Plone feature that we can test is a View.

## Create a new view

Create a new view with plonecli:

```shell
cd plonetraining.testing
plonecli add view
```

Follow the prompts and create a new view with the `TestingItemView` Python class and a matching template.

This new view will be automatically registered in our package.

## Test the view

`plonecli` creates basic tests (in the `test_view_testing_item_view.py` file).

Inspecting this file, we see something like this:

```{literalinclude} _snippets/test_view_testing_item_view.py
:language: python
:lines: 17-26, 28,29, 31-34, 39-50
```

In `setUp` we are creating sample content that we will use in tests.

The first test (`test_testing_item_view_is_registered`) tries to call the view on a Folder and checks that everything works well and that we get the correct view.

The second test (`test_testing_item_view_not_matching_interface`) tries to call the view on a non-folderish content item (a Document) and checks that this raises an Exception.

If we take a look at the configure.zcml file where the view is registered, we can see that the view is registered only for folderish types. We want to test that this registration is correct.

We can test several things about a view:

- If it is available only for a certain type of object
- If it renders as we expect, by calling the view in an Integration test, or using the browser in a Functional test
- If its methods return what we expect, by calling methods directly from the view instance

### Exercise 1

We want to use this view only for our content type and not for all folderish ones (also because TestingItem isn't a folderish type).

- Change the view registration to be available only for our type
- Update tests to check that we can call it only on a TestingItem content
- The view template prints a string that is returned from its class. Write a test that checks this string.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

TestingItem objects implements the `ITestingItem` interface, so we need to update the view registration like this:

```xml
<browser:page
    name="testing-item-view"
    for="plonetraining.testing.content.testing_item.ITestingItem"
    class=".testing_item_view.TestingItemView"
    template="testing_item_view.pt"
    permission="zope2.View"
    />
```

Then our `test_view_testing_item_view` will become like this:

```{literalinclude} _snippets/test_view_testing_item_view.py
:emphasize-lines: 7, 11, 25-28, 30-36
:language: python
:lines: 21-29, 36-50, 52-64
```
````

```{note}
plonecli uses `getMultiAdapter` to obtain a view and we use this for consistency with these pre-created tests, but the preferred way of obtaining a view is via plone.api.
```

### Exercise 2

- Add a method in the view that gets a parameter from the request (`message`) and returns it.
- Check the method in the integration test
- Update the template to print the value from that method
- Test that calling the method from the view returns what we expect
- Write a functional test to test browser integration

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

First, we need to implement that method in our view class in the `views/testing_item_view.py` file:

```{literalinclude} _snippets/testing_item_view.py
:emphasize-lines: 11-12
:language: python
:lines: 9-20
```

Then we add this message into the template in `views/testing_item_view.pt`

```{literalinclude} _snippets/testing_item_view.pt
:emphasize-lines: 10-12
:language: html
```

And finally we want to test everything, so let's add an integration test for the method:

```{literalinclude} _snippets/test_view_testing_item_view.py
:language: python
:lines: 65-81
```

Now we can create a functional test:

```{literalinclude} _snippets/test_view_testing_item_view.py
:language: python
:lines: 83-145
```
````
