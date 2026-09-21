---
myst:
    html_meta:
        "description": "Half-day training on customizing the Blicca (formerly Plone Classic UI) JavaScript stack: pattern options, custom patterns, replacing core patterns, and overriding Svelte components."
        "property=og:description": "Half-day training on customizing the Blicca (formerly Plone Classic UI) JavaScript stack: pattern options, custom patterns, replacing core patterns, and overriding Svelte components."
        "property=og:title": "Blicca JS stack insights — how to customize Mockup"
        "keywords": "Plone, Blicca, Classic UI, Mockup, Patternslib, Svelte, JavaScript, training, customization"
---

(blicca-label)=

# Blicca JS stack insights — how to customize Mockup

Level
: Beginner to intermediate

Blicca — Plone's server-rendered frontend, formerly known as Classic UI — ships a modern JavaScript stack.
It consists of Patternslib-based patterns, webpack module federation, and Svelte apps such as the content browser.
The stack is very customizable, if you know where the hooks are.

In this half-day training, we build a small add-on that overrides the stack at every level, without forking `plone.staticresources` or Mockup.
The add-on [`blicca.staticresourceoverride`](https://github.com/collective/blicca.staticresourceoverride) is the reference implementation for this training and your safety net during the exercises.

## What you will learn

After this training, you can:

1.  Configure patterns site-wide via the `plone.patternoptions` registry record, without writing any JavaScript.
2.  Build and register your own Patternslib pattern, and ship it as a module federation remote bundle.
3.  Replace a core pattern using the pattern blacklist, while reusing the original implementation and its options.
4.  Override a Svelte component of the content browser via the shared `@plone/registry`.
5.  Explain how the Blicca JS stack loads, registers, and shares code, and debug it when it doesn't.

## Prerequisites

You need basic Plone knowledge, such as installing add-ons and working with GenericSetup profiles.
JavaScript basics with ES6 syntax and module imports are enough.
No Svelte experience is required.

Bring a laptop with the following software installed:

- The prerequisites from the Plone documentation, {doc}`Create a project with Cookieplone <plone:install/create-project-cookieplone>`: uv, Make, and Git
- Node.js 22 or later
- pnpm, where `corepack enable` is all it takes, as the version is pinned in the project's `package.json`
- A code editor

```{tip}
Run the setup from {ref}`blicca-setup-label` before the training.
This warms your package caches and saves conference wifi.
```

## How to use the step tags

The git history of the training repository mirrors the four training chapters.
Each tag is a working state of the add-on after the corresponding chapter:

| Tag      | State after                                                       |
| -------- | ----------------------------------------------------------------- |
| `step-1` | Pattern options via the registry only, no JavaScript build yet    |
| `step-2` | Own pattern `pat-blicca` plus webpack and module federation setup |
| `step-3` | Core pattern `markspeciallinks` replaced via the blacklist        |
| `step-4` | Svelte `SelectedItem` override, identical to `main`               |

If you fall behind, jump to the current step and continue from there:

```shell
git checkout step-2
pnpm install && pnpm run build
```

Reinstall the add-on, or reimport its profile, after switching steps, so that new registry records are applied.

## How to update your checkout

We keep improving the material until the training starts.
The `main` branch only moves forward, but the step tags are re-pointed whenever the material changes, and a plain `git fetch` does not update tags that already exist locally.
Update the source checkout in your project like this:

```shell
cd backend/sources/blicca.staticresourceoverride
git stash
git fetch --force --tags origin
git checkout main
git reset --hard origin/main
```

`git stash` saves your own changes from the exercises, so that you can restore them later with `git stash pop`.
`git reset --hard` discards everything that is not on `origin/main`.
Afterwards, run `pnpm install && pnpm run build` again, and reinstall the add-on.

```{toctree}
:caption: Chapters
:maxdepth: 1
:numbered:

intro
setup
pattern-options
own-pattern
replace-pattern
svelte-override
stretch-folder-contents
production
```
