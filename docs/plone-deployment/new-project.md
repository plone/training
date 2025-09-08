---
myst:
  html_meta:
    "description": "Create a project for Plone deployment with Ansible and Docker"
    "property=og:description": "Create a project for Plone deployment with Ansible and Docker"
    "property=og:title": "Create a project for Plone deployment with Ansible and Docker"
    "keywords": "Plone, deployment, Ansible, Docker, create, project"
---

# Create a Project

As mentioned in the {doc}`intro`'s Training Choices, for this Training, GitHub is a requirement to build the Docker images automatically.
The steps in this training may be adapted to other providers, including GitLab.

## Generating the Codebase

Run `cookiecutter` to create a Plone project skeleton using the Cookiecutter {term}`cookiecutter-plone-starter` with the following command.

```{code-block} shell
cookiecutter gh:collective/cookiecutter-plone-starter
```

You will be presented with a series of prompts.

You can accept the default values in square brackets (`[default-option]`) by hitting the {kbd}`Enter` key, or enter your preferred values.

For this training, we recommend you to provide:

- `project_title`: **Plone Conference**
- `github_organization`: Your GitHub username
- `container_registry`: **2**

```{code-block} console
:emphasize-lines: 1,15,19
project_title [Project Title]: Plone Conference
project_slug [plone-conference]:
description [A new project using Plone 6.]:
author [Plone Foundation]:
email [collective@plone.org]:
python_package_name [plone_conference]:
plone_version [6.0.0b3]:
volto_version [16.0.0-alpha.42]:
Select language_code:
1 - en
2 - de
3 - es
4 - pt-br
Choose from 1, 2, 3, 4 [1]:
github_organization [collective]: <your-github-account>
Select container_registry:
1 - Docker Hub
2 - GitHub
Choose from 1, 2 [1]: 2
================================================================================
Plone Conference generation
================================================================================
Running sanity checks
  - Python: ✓
  - Node: ✓
  - yo: ✓
  - Docker: ✓
  - git: ✓

Summary:
  - Plone version: 6.0.0b3
  - Volto version: 16.0.0-alpha.42
  - Output folder: /<path-to-project>/plone-conference

Frontend codebase:
 - Install latest @plone/generator-volto
 - Generate frontend application with @plone/volto 16.0.0-alpha.42

Backend codebase
 - Format generated code in the backend
================================================================================

Project "Plone Conference" was generated

Now, code it, create a git repository, push to your organization.

Sorry for the convenience,
The Plone Community.

================================================================================
```

Now, change to your project directory {file}`plone-conference`.

```shell
cd plone-conference
```

### Understanding the Codebase

{file}`/backend`
: Folder containing the backend (api) solution.
: Inside this folder, the Python codebase can be found in {file}`src/plone_conference`.

{file}`/frontend`
: Folder containing the frontend (Volto) solution. The generated code was created using `@plone/generator-volto`.

{file}`/devops`
: Folder with Ansible and Docker Stacks.

{file}`/.github/workflows`
: GitHub Actions workflows to test the codebase and release container images to the choosen container registry.

{file}`/Makefile`
: File defining a set of tasks to manage the codebase.

We use [make](https://www.gnu.org/software/make/) here because it is well understood, just works, is mature and wide spread available.
For build and deployment this is an important criteria.
Future plans are to use make's dependency management and include capabilities more here, and in the dependent Makefiles.

To see all available commands and their descriptions, enter the following command.

```{code-block} shell
make help
```

## Installing the codebase and dependencies

To install both the Plone backend and frontend, use the following command.

```{code-block} shell
make install
```

This will take a few minutes.
☕️
First the backend, then the frontend will be installed.
At the start of the frontend installation part, you might see a prompt.

```console
Need to install the following packages:
  mrs-developer
Ok to proceed? (y)
```

Hit the {kbd}`Enter` key to proceed and install `mrs-developer`.

When the process completes successfully, it will exit with a message similar to the following.

```console
✨  Done in 98.97s.
```

````{note}
Due to an output difference when translations are built by the `@plone/generator-volto`, at the moment, it is necessary to run on the root directory:

```shell
make i18n
```
````
