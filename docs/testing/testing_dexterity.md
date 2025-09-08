---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Testing a Dexterity content type

The most common thing that we could develop in Plone are content types.
Let's see how to test if a new content type works as expected.

## Create a new content type

With plonecli we can add features to our package using the command line.

For example, let's create a new `TestingItem` content type:

```shell
cd plonetraining.testing
plonecli add content_type
```

With this command, plonecli will ask you some questions and will register a new content type in our package.

```{note}
To follow this training, you need to answer questions like this:

- Content type name (Allowed: _ a-z A-Z and whitespace) \[Todo Task\]: TestingItem
- Content type description:
- Use XML Model \[y\]: n
- Dexterity base class (Container/Item) \[Container\]: Item
- Should the content type globally addable? \[y\]: y
- Create a content type class \[y\]: y
- Activate default behaviors? \[y\]: y
```

## Test the content type

If we now try to re-run the tests, we see that the number of tests has increased.
This is because plonecli also creates a basic test for this new content type in the `tests/test_ct_testing_item.py` file:

```{literalinclude} _snippets/test_ct_testing_item.py
:emphasize-lines: 3,5-9
:language: python
:lines: 25-69
```

We can see some interesting things:

- We are using the `PLONETRAINING_TESTING_INTEGRATION_TESTING` layer, because we don't need to write functional tests
- We are using the `setUp` method to set some variables and add some roles to the testing user.

In these tests, we are testing some very basic things for our content type, for example if it's correctly registered with factory type information (FTI), if we can create an item of our content type
and if a user with a specific role (Contributor) can add it.

```{note}
plone.app.testing gives us a default user for tests. We could import its username in a variable called `TEST_USER_ID` and set different roles when needed.

By default, each test is run as that logged-in user. If we want to run tests as anonymous users or using a different user, we need to logout and login.
```

### Exercise 1

- Change the permissions for our new content type and only allow Manager role to add items of this type.
- Fix old tests.
- Create a new one test to verify that the Contributor role can't add items of this type.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

In `rolemap.xml`:

```xml
<permission name="plonetraining.testing: Add TestingItem" acquire="True">
    <role name="Manager"/>
</permission>
```

In the test case file we need to import a new Exception:

```{literalinclude} _snippets/test_ct_testing_item.py
:language: python
:lines: 2
```

And then we update tests like this:

```{literalinclude} _snippets/test_ct_testing_item.py
:language: python
:lines: 50,52-63, 65-76
```
````

## Functional test

So far, we have written only `ìntegration` tests because we didn't need to test browser integration or commit any transactions.

As we covered before, if we don't need to create functional tests, it's better to avoid them because they are slower than integration tests.

```{note}
It's always better to avoid transactions in tests because they invalidate the isolation between tests in the same test case.
```

However, we will create a `functional` test to see how it works and how content type creation works in a browser.

Let's create a new test case in the same file.

First, we need to import some new dependencies:

```{literalinclude} _snippets/test_ct_testing_item.py
:language: python
:lines: 5,6,9,10
```

Now we can create a new test case:

```{literalinclude} _snippets/test_ct_testing_item.py
:emphasize-lines: 3,11-19
:language: python
:lines: 78-123
```

The first thing we see is the new layer used: `PLONETRAINING_TESTING_FUNCTIONAL_TESTING`.

In `setUp` we configure the test case to use the Zope web browser and we login as site owner.

In `test_add_testing_item` we simulate the user interaction of creating a new content in the browser with following actions:

- Open the url for adding a new TestingItem content
- Find the title field and compile it
- Click to Save button
- Check that after saving it, we can see its title.

In `test_view_testing_item` we are checking that, by accessing a content item directly using a URL, we can see its values.

```{note}
`self.browser.contents` shows the HTML of the last visited page.
```
