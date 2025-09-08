---
myst:
  html_meta:
    "description": "Contributing to JavaScript code and documentation in Plone 5"
    "property=og:description": "Contributing to JavaScript code and documentation in Plone 5"
    "property=og:title": "JavaScript Development Process"
    "keywords": "Plone, JavaScript, development, code, style, lint, mockup, documentation"
---

# JavaScript Development Process

## Code Style

Together with [plone.api](https://github.com/plone/plone.api) we developed [Plone code style guidelines](https://5.docs.plone.org/develop/styleguide/), which we are enforcing now for core Plone development.

This makes code so much more readable.

It currently does not cover JavaScript code guidelines, but those were considered when Mockup was developed.

And luckily, similar to PEP 8 and the associated tooling ({program}`pep8`, {program}`pyflakes`, {program}`flake8`), JavaScript also has some guidelines - not official, but well respected.

[Douglas Crockford](https://crockford.com/javascript/) - besides of specifying the JSON standard - wrote the well known book "JavaScript the good parts".

Out of that he developed the code linter [JSLint](https://www.jslint.com/).

Because this one was too strict, some other people wrote [JSHint](https://jshint.com/).

```{todo}
`Mockup` got an overhaul.
The following content regarding JSHint is valid up to [`mockup` 2.7.7](https://github.com/plone/mockup/releases/tag/2.7.7).
The link to **.jshintrc configuration file** is broken and needs to be updated.
See https://github.com/plone/training/issues/611
```

Mockup uses JSHint with the following [.jshintrc configuration file](https://github.com/plone/mockup/blob/master/mockup/.jshintrc):

```json
{
   "bitwise": true,
   "curly": true,
   "eqeqeq": true,
   "immed": true,
   "latedef": true,
   "newcap": true,
   "noarg": true,
   "noempty": true,
   "nonew": true,
   "plusplus": true,
   "undef": true,
   "strict": true,
   "trailing": true,
   "browser": true,
   "evil": true,
   "globals": {
      "console": true,
      "it": true,
      "describe": true,
      "afterEach": true,
      "beforeEach": true,
      "define": false,
      "requirejs": true,
      "require": false,
      "tinymce": true,
      "document": false,
      "window": false
   }
}
```

```{note}
When working with JSHint or JSLint, it can be very useful to get some more context and explanation about several lint-errors.
For JSHint there is a list of all configurable options: <https://jshint.com/docs/options/>
```

We strongly recommend to configure your editor of choice to do JavaScript code linting on save.
The Mockup project is enforcing Lint-error-free code.

Besides of that, this will also make you a better coder.
The JSHint site lists some editors with Plugins to support JSHint linting: <https://jshint.com/install/>

Regarding spaces/tabs and indentation:

- Spaces instead of tabs.
- Tab indentation: 2 characters (to save screen estate).

You have to configure your editor to respect these settings.

Confirming on a common code style makes contributing much more easier, friendly and fun!

## Mockup Contributions

For each feature, create a branch and make pull-requests on GitHub.

Try to include all your changes in one commit only, so that our commit history stays clean.

Still, you can do many commits to not accidentally lose changes and still commit to the last commit by doing the following:

```shell
git commit --amend -am"my commit message".
```

Do not forget to also include a change log entry in the {file}`CHANGES.rst` file.

## Documentation

Besides documenting your changes in the {file}`CHANGES.rst` file, also include user and developer documentation as appropriate.

For patterns, the user documentation is included in a comment in the header of the pattern file, as described in {ref}`mockup-writing-documentation`.

For function and methods, write an API documentation, following the [apidocjs](https://apidocjs.com/) standard.

You can find some examples throughout the source code.

We also very welcome contributions to the [training documentation](https://github.com/plone/training) and the [official documentation](https://github.com/plone/documentation).

As with other contributions: please create branches and make pull-requests!
