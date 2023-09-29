---
myst:
  html_meta:
    "description": "release-it"
    "property=og:description": "release-it"
    "property=og:title": "release-it"
    "keywords": "Volto, Plone, release-it, release management"
---

# `release-it`

Volto uses the library `release-it` in order to automate the release process of addons and other JS libraries.

You can also integrate it with your add-ons, since it's quite handy and saves you quite a lot of time.

```{note}
If you are familiarized with `zest.releaser` in the Python packaging world, this library aims to do the same.
```

## Basic configuration

In your `package.json`:

```json
  "release-it": {
    "hooks": {
      "before:bump": [
        "yarn i18n",
        "git add locales"
      ],
      "after:bump": "node changelogupdater.js bump ${version}",
      "after:release": "node changelogupdater.js back ${version} && git commit -am 'Back to development' && git push"
    },
    "git": {
      "changelog": "node changelogupdater.js excerpt",
      "requireUpstream": false,
      "requireCleanWorkingDir": false
    },
    "github": {
      "release": true,
      "releaseName": "${version}",
      "releaseNotes": "node changelogupdater.js excerpt"
    }
  },
```

```{note}
You can refer to the `release-it` documentation for further information:
https://www.npmjs.com/package/release-it
```

`release-it` defines a release workflow, were you can hook and issue your own commands.
It also has default named hooks that do common tasks like creating a Release on GitHub ('github'), or repository related tasks ('git') like update the changelog.
Hook into a state in the lifecycle is easy, you can issue several commands that will be added to the default defined ones (https://github.com/release-it/release-it/blob/HEAD/config/release-it.json).
You can modify the default ones to adjust to your requirements.
eg. in the example, we hook into the `before:bump`, `after:bump` and `after:release` to issue custom commands accordingly to each state of the release.

We also use the `changelogupdater` command from `@plone/scripts`. See {ref}`plone-scripts-label` for more information.
