Intro to tests
==============

What is a test?
---------------

A piece of code that proves that some part of a programm works in a certain way.

Why we test?
------------

- To ensure that our code works as expected
- To avoid (long and boring) manually tests each time that we change something
- To be confident that some changes don't break other parts of our code. Or if they do, we notice it instantly (as long as the tests pass and covers that feature)
- To have an up-to-date documentation about how our code is actually meant to do

Apparent issues with tests
--------------------------

- Testing is not easy (additional skills)
- Tests are code -> Cost of maintenance
- Setup, Test-Fixures is hard and does not translate to application-development
- Infrastructure (CI-Server) needs to be bought and maintained
- Test-Isolation can be hard
- Value is not apparent -> Hard sell

Benefits with tests
-------------------

- (good) Testing requires additional skills, but once you learn them and with some practice, testing will not take too much extra time.
- They are more code, but once a test runs, it doesn't need maintenance.
- We have some standard setups for testing Plone addons: plonecli is the answer.
- Travis, Bitbucket, Gitlab offers free-ish (it depends on what you need to do) CI solutions.
- Plone has fixtures for test isolation.
- A well tested application needs less maintainance and you can avoid regression errors on refactoring.
- Helps for better design and code-quality.
