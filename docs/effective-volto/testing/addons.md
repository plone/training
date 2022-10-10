---
myst:
  html_meta:
    "description": "Testing add-ons"
    "property=og:description": "Testing add-ons"
    "property=og:title": "Testing add-ons"
    "keywords": "Volto, Plone, Testing, CI, Add-ons"
---

# Testing add-ons

We should let jest know about our aliases and make them available to it to
resolve them, so in `package.json`:

```{code-block} json
:emphasize-lines: 6

  "jest": {
    "moduleNameMapper": {
      "@plone/volto/(.*)$": "<rootDir>/node_modules/@plone/volto/src/$1",
      "@package/(.*)$": "<rootDir>/src/$1",
      "@plone/some-volto-addon/(.*)$": "<rootDir>/src/addons/@plone/some-volto-addon/src/$1",
      "my-volto-addon/(.*)$": "<rootDir>/src/addons/my-volto-addon/src/$1",
      "~/(.*)$": "<rootDir>/src/$1"
    },
```

You can use `yarn test src/addons/addon-name` to run tests.

## Jest configuration override

In CI or for testing addons, it's interesting to provide an alternate Jest configuration
or slightly modify it. Volto provide a way to do it using a `jest.config.js` file or
pointing the test runner to a file of your choice, using `RAZZLE_JEST_CONFIG`
environment variable.

```shell
RAZZLE_JEST_CONFIG=my-custom-jest-config.js yarn test
```

```{note}
Both configurations are merged in a way that the keys of the config provided override  the initial (`package.json`) default config, either in Volto or in your projects.
```

This is specially useful in CI while developing add-ons, so you can pass an specific configuration that deals with the addon config properly.

## Testing add-ons in isolation

Testing an add-on in isolation as you would do when you develop a Plone Python backend add-on can be a bit challenging, since an add-on needs a working project in order to bootstrap itself.
There are some utilities available in order to help bootstrap a testing environment for isolated add-ons.

(plone-scripts-label)=

### `@plone/scripts`

This library adds some useful command line utilities that come in handy when testing add-ons in isolation.

First of all, your add-on should has `@plone/scripts` as dependency:

    ```json
    "dependencies": {
        "@plone/scripts": "*",
    }
    ```

Once done, your environment has an executable `addon` available which exposes a command line interface and you could run:

`npx -p @plone/scripts addon clone [options] <source> [destination]`

    Options:
      -p, --private          set if the repo is private, then GITHUB_TOKEN is used
      -b, --branch <branch>  set the repo branch, defaults to main
      -c, --canary           downloads latest Volto canary (alpha) version
      -h, --help             display help for command

Example:

`npx -p @plone/scripts addon clone https://github.com/kitconcept/volto-blocks-grid.git --branch my_new_branch --canary`

This will create a directory named `addon-testing-project` (this is a sensible default, but you can specify a custom one) and will bootstrap a new project using Volto's standard project generator.
It will adjust the configuration of this project to setup the add-on in the project using `mrs-developer` and the git URL given to fetch the add-on contents.
You can specify the branch to be used, if the project should use the latest alpha available.
There is an option for private repos as well, in that case, it will use the `GITHUB_TOKEN` present in your environment variables to fetch it.

After this, as a developer you can use the usual project commands to run tests (unit, linting, acceptance) inside the generated addon-testing-project`.
You can configure the CI of your choice for automated testing, you can take a look at how it's done in: https://github.com/kitconcept/volto-blocks-grid/tree/main/.github/workflows
The idea is to issue commands inside the generated `addon-testing-project` project and do your checks.
Take special care on how to pass down to the `npx` command the current PR branch.
