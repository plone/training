---
myst:
  html_meta:
    "description": "Contributing to Plone Training"
    "property=og:description": "Contributing to Plone Training"
    "property=og:title": "Contributing to Plone Training"
    "keywords": "Plone, Trainings, Plone Contributor Agreement, License, Code of Conduct"
---

(contributing-index-label)=

# Contributing to Plone Training

This document describes how to contribute to the Plone Training.

Contributions to the Plone Training are welcome.


(contributing-permission-to-publish-label)=

## Granting permission to publish

Before you contribute, you must give permission to publish your contribution according to the license we use.
You may give that permission in two ways.

- Sign the [Plone Contributor Agreement](https://plone.org/foundation/contributors-agreement).
  This method also covers contributions to Plone code.
  It is a one-time only process.
- In every pull request or commit message, include the following statement.

  > I, [full name], agree to have this contribution published under Creative Commons 4.0 International License (CC BY 4.0), with attribution to the Plone Foundation.

The Plone Trainings Documentation is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
A copy of the license is included in the root of this repository.


(contributing-manage-on-github-label)=

## Managing contributions on GitHub

Contributions are managed through the [Training repository on GitHub](https://github.com/plone/training).

First discuss whether you should perform any work.
Any method below is acceptable, but are listed in order of most likely to get a response.

- [Search for open issues](https://github.com/plone/training/issues) and comment on them.
- [Create a new issue](https://github.com/plone/training/issues/new/choose).
- Discuss during conferences, trainings, and other Plone events.
- Ask on the [Plone Community Forum, Training topic](https://community.plone.org/c/training/46).
- Ask in the [Plone chat on Discord](https://discord.com/invite/zFY3EBbjaj).

As a convenience, at the top right of every page, there is a GitHub navigation menu.
Tap, click, or hover over the GitHub Octocat icon for options.

```{image} _static/github-navigation.png
:alt: GitHub navigation menu 
```

You can use this menu to quickly navigate to the source repository, open an issue, or suggest an edit to the current document.
Of course, you can use whichever tools you like.

Filing an issue is a valuable contribution to the trainings.
If you want to propose a solution, and you have already put the topic up for discussion and clarified that the topic needs a solution, then please follow the next steps to propose your solution via a pull request.

- Build the trainings as described in {doc}`setup-build`.
- Create a branch.
- Make your changes.
- Run `make test`. 
- If tests are OK: commit your changes. 
- If tests are not OK and you are not sure if it depends on your changes, please contact the community by opening an issue.
- Submit a pull request.
  Optionally, if you want to mark your pull request as a "work in progress" that is not ready to merge or should be discussed further, you can convert it to a draft.

Members who subscribe to the repository will receive a notification and review your request. 

```{note}
Reviewers do not have to build the training on a local machine.
A preview of all pull requests is attempted to be built, and if successful, is available and linked in the pull request comments.
```


(contributing-roles-label)=

## Contributor Roles

Contributors to the Training docs may perform one or many roles.

- **Plone users and developers** use this documentation because it is accurate and actively maintained.
  People in these roles typically contribute minor corrections.
  They should read {doc}`setup-build` and {doc}`writing-docs-guide`.
- **Authors** create the Training documentation.
  They should read {doc}`setup-build` and {doc}`writing-docs-guide`.
  They should also read {doc}`authors` for guidance and tips for writing good Training documentation.
- **Trainers** should read {doc}`setup-build` and {doc}`/teaching/index`.
  These documents help trainers prepare for a successful training experience.


(contributing-quality-requirements-label)=

## Documentation quality requirements

We use GitHub Actions with every pull request to enforce Training documentation quality.
We recommend that you build the documentation locally to catch errors and warnings early on.
See {doc}`setup-build` for instructions for how to set up and build the documentation and to run quality checks.


(contributing-code-of-conduct-label)=

## Code of Conduct

The Plone Foundation has published a [Code of Conduct](https://plone.org/foundation/materials/foundation-resolutions/code-of-conduct).
All contributors to the Plone Trainings Documentation follow the Code of Conduct.


```{toctree}
---
caption: Contributing
maxdepth: 2
hidden: true
---

setup-build
writing-docs-guide
authors
```
