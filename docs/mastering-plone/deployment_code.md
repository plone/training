---
myst:
  html_meta:
    "description": "Creating a release of an add-on"
    "property=og:description": "Creating a release of an add-on"
    "property=og:title": "Releasing your code"
    "keywords": "Plone, Volto, release, open source"
---

# Releasing your code

We finally have some working code!
Depending on your policies, you need repeatable deployments and definitive versions of software.
That means you don't just run your production site with your latest source code from your source repository.
You want to work with Python wheels/eggs and npm releases.

```{note}
You may want to move your add-on from your repository to the [Plone collective of add-ons](https://github.com/collective/) if it's relevant for general use cases.

Please contact the community on [community.plone.org](https://community.plone.org/) for a release.
```


## Releasing your backend add-on

When you are ready with development and tests are OK, you can release your package.

Test your add-on with 

```shell
make check
```

We are releasing the Python package on PyPI.
Go to [pypi.org](https://pypi.org) and create an account as explained in https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#create-an-account.

The package created with cookieplone is prepared for releasing with [`zest.releaser`](https://github.com/zestsoftware/zest.releaser/).
Run `fullrelease` in the root directory of your add-on.

```shell
fullrelease
```

% TODO Finish section on releasing backend add-on. Package is generated with cookieplone.


## Releasing your frontend add-on

When you are ready with development and tests are OK, you can release your package.

Frontend add-ons are Node packages and are released on https://www.npmjs.com.
So, please create an account (https://docs.npmjs.com/getting-started/setting-up-your-npm-user-account) and configure your local environment (https://docs.npmjs.com/getting-started/configuring-your-local-environment).

Have a look at the Makefile of your add-on.
You'll see that it is already prepared for a release.
The following command starts a dialog to release the package.

```{code-block} console
make release
```

You may want to trigger a test run before with

```{code-block} console
make release-dry-run
```

Congratulation!
