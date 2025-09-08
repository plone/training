---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Some theory

## Test types

There are four main test types that we can use:

- unit tests
- integration tests
- functional tests
- acceptance tests

They can also be represented as a test pyramid:

```none
      = acceptance tests =
    === functional tests ===
  ===== integration tests ====
========== unit tests ==========
```

Complexity and time to execute increases from the bottom to the top of the pyramid.

Unit tests are the easiest ones to write because they test single isolated functions.

Going up through the pyramid, tests become more complex because they start to test the integration between functions and features, until acceptance tests (also called "e2e" or "end-to-end") where you test the final user interaction.

More complexity means also more time to execute a test, because you need different layers or services to run a single function or the complete application.

In Plone usually we do not need to write pure unit tests because most of the methods are already integrations of some CMS features and tools.
That is the reason why Plone tests usually start with integration tests.

The difference between integration and functional tests is that integration tests create a new transaction for each test and roll it back on test tear-down.
This means that they do not perform commits on the database.

Functional tests, on the other hand, use a temporary storage (called `DemoStorage`) that allows you to simulate transaction commits.
They are useful for browser interaction testing, for example, because they can simulate real HTTP requests with a transaction life cycle:

- Functional tests apply a transaction for each `browser.open()` request.
- Functional tests can perform traversing and can check cookie based permissions.
- Unit test methods are executed in a single transaction, which might make it impossible to test cache-related behavior.

Those are some of the reasons why functional tests are slower than integration tests.
