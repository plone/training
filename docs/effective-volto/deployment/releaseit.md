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

In your `package.json` or in `.release-it.json`:

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
We also use the `changelogupdater` command from `@plone/scripts`. See {ref}`plone-scripts-label` for more information.
```

## Using it along with `towncrier` in add-ons

```json
{
  "hooks": {
    "after:bump": "pipx run towncrier build --draft --yes --version ${version} > .changelog.draft && pipx run towncrier build --yes --version ${version}",
    "after:release": "rm .changelog.draft"
  },
  "git": {
    "changelog": "pipx run towncrier build --draft --yes --version 0.0.0",
    "requireUpstream": false,
    "requireCleanWorkingDir": false,
    "commitMessage": "Release ${version}",
    "tagName": "${version}",
    "tagAnnotation": "Release ${version}"
  },
  "github": {
    "release": true,
    "releaseName": "${version}",
    "releaseNotes": "cat .changelog.draft"
  }
}
```

You need to setup an empty `news` folder and a `towncrier.toml`:

```ini
[tool.towncrier]
filename = "CHANGELOG.md"
directory = "news/"
title_format = "## {version} ({project_date})"
underlines = ["", "", ""]
template = "packages/scripts/templates/towncrier_template.jinja"
start_string = "<!-- towncrier release notes start -->\n"
issue_format = "[#{issue}](https://github.com/plone/volto/issues/{issue})"

[[tool.towncrier.type]]
directory = "breaking"
name = "Breaking"
showcontent = true

[[tool.towncrier.type]]
directory = "feature"
name = "Feature"
showcontent = true

[[tool.towncrier.type]]
directory = "bugfix"
name = "Bugfix"
showcontent = true

[[tool.towncrier.type]]
directory = "internal"
name = "Internal"
showcontent = true

[[tool.towncrier.type]]
directory = "documentation"
name = "Documentation"
showcontent = true
```

and make your add-on rely on `@plone/scripts` (which should already have) if your add-on has been created using the generator.

```{note}
You can refer to the `release-it` documentation for further information:
https://www.npmjs.com/package/release-it
```

`release-it` defines a release workflow, were you can hook and issue your own commands.
It also has default named hooks that do common tasks like creating a Release on GitHub ('github'), or repository related tasks ('git') like update the changelog.
Hook into a state in the lifecycle is easy, you can issue several commands that will be added to the default defined ones (https://github.com/release-it/release-it/blob/HEAD/config/release-it.json).
You can modify the default ones to adjust to your requirements.
eg. in the example, we hook into the `before:bump`, `after:bump` and `after:release` to issue custom commands accordingly to each state of the release.
