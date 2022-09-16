---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Intro to tests

## What is a test?

A test is a piece of code that proves that some part of a program works in a certain way.

## Why do we test?

- To ensure that our code works as expected
- To avoid (long and boring) manual testing each time we change something
- To be confident that changes in one part of our code don't break other parts, or, if they do, we know it immediately
  (as long as the tests pass and they cover those other parts)
- To have up-to-date documentation about how our code is actually meant to work

## Apparent issues with tests

- Testing is not easy (it requires additional skills)
- Tests are code -> tests are an added cost of maintenance
- Setup and test fixtures can be difficult concepts that do not translate to application development
- Infrastructure, such as a continuous integration (CI) server, must be provisioned and maintained and may cost money
- Test isolation can be difficult
- The value of writing and maintaining tests is not apparent, making tests a hard sell to clients and to management

## Benefits of tests

- Good testing requires additional skills, but once you learn them and, with some practice, testing will not take too much extra time.
- Tests are more code, but once a test runs, it doesn't need maintenance (unless you change the code being tested).
- We have standard setups for testing Plone add-ons: plonecli is the answer.
- Travis, Bitbucket, and Gitlab offer free-ish (depending on your needs) CI solutions.
- Plone has fixtures for test isolation.
- A well-tested application needs less maintainance and you can avoid regression errors when you make code changes,
  whether small or large, such as in refactoring.
- Tests help you create better code design and result in better code quality.
