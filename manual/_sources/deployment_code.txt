Deploying your code
===================

 * zest.releaser
 * pypi-test egg deployment

We finally have some working code! Depending on your policies, you need repeatable deployments and definitive versions of software. That means you don't just run your production site with your latest source code from your source repository. You want to work with eggs.

Making eggs is easy, making them properly not so much. There are a number of good practices that you would like to ensure.
Lets see. You want to have a sensible version number. By looking at the version number alone, one should get a good idea, how many changes there are (semantic version number scheme). You of course always document everything, but for upgrades it is even more important to have complete changelogs.

Sometimes, you cannot upgrade to a newer version, but you need a hotfix or whatever. It is crucial that you are able to checkout the exact version you use for your egg.

This is a lot of steps to do, and there are a lot of actions that can go wrong. luckily, there is a way to automate it. zest.releaser provides scripts to release an egg, to check what has changed since the release and to check if the documentation has errors.

There once was a book on python. It also had a chapter on releasing an egg with sample code. The sample code was about a printer of nested lists. There are a lot of packages to print out nested lists on pypi.

We will avoid this. Everybody, go to `testpypi.python.org <https://testpypi.python.org>`_ and create an account now.

Next, copy the pypirc_sample file to ~/.pypirc, modify it to contain your real username and password.

Now that we are prepared, let's install zest.releaser.

- lasttagdiff
- longtest
- prerelease
- release
- postrelease


