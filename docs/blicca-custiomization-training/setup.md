---
myst:
    html_meta:
        "description": "Set up a Plone project with Blicca and the blicca.staticresourceoverride training add-on."
        "property=og:description": "Set up a Plone project with Blicca and the blicca.staticresourceoverride training add-on."
        "property=og:title": "Setup"
        "keywords": "Plone, Blicca, Cookieplone, mxdev, uv, pnpm, installation, training setup"
---

(blicca-setup-label)=

# Setup

In this chapter, we create a Plone project with Blicca, and install the training add-on.
At the end, your browser console proves that your first own bundle is loaded.

## Install the prerequisites

Install the prerequisites from the Plone documentation, {doc}`Create a project with Cookieplone <plone:install/create-project-cookieplone>`: uv, Make, and Git.
The add-on's JavaScript build additionally needs Node.js 22 or later, and pnpm.
Enable pnpm with `corepack enable`, as the version is pinned in the add-on's {file}`package.json`.

## Create a Plone project with Blicca

Cookieplone 2.0 no longer has a separate template for Blicca.
Generate a project with the `project` template, and answer the question `Use Volto as frontend?` with `No`:

```shell
uvx cookieplone project
```

Cookieplone asks 18 questions.
The following answers matter for the training, keep the defaults for the rest:

Plone Version
: `6.2.2` or later.

Use Volto as frontend?
: `No`, so that Cookieplone generates a Blicca project without a frontend.

Should we setup a caching server?, Add Ansible playbooks?, Add GitHub Action to Deploy this project?, Would you like to add a documentation scaffold to your project?
: `No`, to keep the project small.

Then install and start the backend:

```shell
cd <project-slug>
make install
make backend-start
```

The installation creates a virtual environment with uv, and a Plone site named `Plone`.
Your site now runs at `http://localhost:8080/Plone` with the login `admin` and password `admin`.

## Add the add-on as a source checkout

The generated project keeps the Plone backend in the {file}`backend` directory, with {file}`mx.ini` and {file}`pyproject.toml`.
Cookieplone projects manage source checkouts with [mxdev](https://github.com/mxstack/mxdev).
Add the training add-on to {file}`backend/mx.ini`, and pin `plone.staticresources` to a release with Mockup 5.6.14 or later in the same file:

```ini
[settings]
main-package = -e .[test]
version-overrides =
    plone.staticresources==3.0.9

[blicca.staticresourceoverride]
url = https://github.com/collective/blicca.staticresourceoverride.git
branch = main
```

Then add the add-on to the `dependencies` of {file}`backend/pyproject.toml`:

```toml
dependencies = [
    "Products.CMFPlone==6.2.2",
    "blicca.staticresourceoverride",
    "plone.api",
    "plone.restapi",
    "plone.classicui",
    "plone.app.caching",
    "z3c.jbot",
]
```

Run the installation again:

```shell
make install
```

mxdev clones the repository into {file}`backend/sources/blicca.staticresourceoverride`, registers it as an editable package in the `tool.uv.sources` table of {file}`pyproject.toml`, and turns the version override into a uv `override-dependencies` entry.
uv then installs everything.

```{note}
The `version-overrides` entry is what gives you Mockup 5.6.14, the version this add-on is built against.
Plone 6.2.2 ships `plone.staticresources` 3.0.6 with Mockup 5.6.10, which is enough for the first three chapters.
{ref}`blicca-svelte-override-label` needs the default component key from Mockup 5.6.11, and the stretch goal is written for the row scanning of Mockup 5.6.14.
```

## Build the JavaScript

Build the add-on's JavaScript inside the source checkout:

```shell
cd backend/sources/blicca.staticresourceoverride
pnpm install
pnpm run build
```

Start the backend again with `make backend-start`.
Then install {guilabel}`Blicca Static Resource Override (Training)` in the add-ons control panel.

## The pnpm caveats

The package manager is pnpm, the same as Mockup itself uses.
The file `pnpm-workspace.yaml` mirrors the known caveats of [plone/mockup](https://github.com/plone/mockup):

- `shamefullyHoist: true`, because webpack module resolution needs a flat `node_modules` directory.
- `overrides` that remove the git subdependencies `slick-carousel`, `slides`, and `select2`, because pnpm blocks exotic subdependencies.
  Only patterns that this add-on does not import need them.
- An `allowBuilds` allowlist, because pnpm 10 and later block dependency build scripts by default.

## Success check

Open any page of your site, and open the browser console.
You should see the following message:

```console
Patternslib Module Federation: Loaded and initialized bundle "__patternslib_mf__bliccastaticresourceoverride".
```

The Plone bundle, the host, has found and initialized your add-on bundle, the remote.
Now we can start overriding things.
