---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Acceptance testing

Acceptance tests are the highest level of tests in the testing hierarchy.

In previous chapters we tested to ensure that the code had no bugs and that the interaction of several methods and behaviors generated
the expected outputs, but what if we want to test that what the end user sees is correct?

Acceptance tests do exactly this: they simulate user interaction over different scenarios.

We can achieve something similar with the `browser` utility in functional tests, but it has some disadvantages:
for example, you can't test JavaScript.

To write acceptance tests, we use [plone.app.robotframework](https://github.com/plone/plone.app.robotframework): a
Plone plugin that provides Robot Framework-compatible tools and resources for writing functional Selenium tests.

The [Robot Framework](https://robotframework.org) is a generic test automation framework for acceptance testing,
acceptance test-driven development (ATDD), and behavior driven development (BDD).
It has an easy-to-use `plain text test syntax` and uses a keyword-driven testing approach.

[Selenium](https://www.selenium.dev/) is a web browser automation framework that exercises the browser as if the
user was interacting with the browser.

Each test opens a real browser instance and tests user interaction using Selenium.

```{note}
Selenium bindings for Python use `Firefox` as the default browser.

Unless you know how to configure other browsers to work with Selenium, you should have Firefox installed in your system.
```
