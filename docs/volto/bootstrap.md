---
myst:
  html_meta:
    "description": "Setting up backend and frontend"
    "property=og:description": "Setting up backend and frontend"
    "property=og:title": "Bootstrapping a Volto project"
    "keywords": "Plone, Volto"
---

(bootstrap-volto-label)=

# Bootstrapping a Volto project

```{note}
It is recommended to work on Linux or macOS.
```


## Installing Plone backend

In order to run Volto you need a backend.
This can be either Plone or Guillotina.
For this course we will use Plone.
Because we will focus on the frontend, for simplicity we will install a backend in a Docker container.
The installation of a Plone backend in a Docker container is described in {ref}`plone6docs:install-containers-label`.
 
In short, create a directory named `backend`, and run the following command.

```shell
docker run --name plone6-backend -e SITE=Plone -e CORS_ALLOW_ORIGIN='*' -d -p 8080:8080 plone/plone-backend:6.0
```

This installs and starts a Plone backend on port 8080.


(install-deps-volto-label)=

## Installing prerequisites for Volto (Plone frontend)

First {ref}`plone6docs:frontend-getting-started-install-nvm-label`.

{ref}`Install Yarn <plone6docs:frontend-getting-started-yarn-label>`.

Install `@plone/generator-volto`:

```shell
npm install -g yo @plone/generator-volto
```

## Create a Volto project

To create a new volto project type the following:

```shell
yo @plone/volto
```

Follow the prompts' questions, providing `my-volto-app` as the project name.

```{warning}
Do not start your project name with `volto`, as it will cause `plone/generator-volto` to fail.
```

It will create a folder called `my-volto-app` inside the current folder with the following structure:

```console
my-volto-app/
├── babel.config.js
├── cypress
│   ├── fixtures
│   ├── .gitkeep
│   ├── plugins
│   ├── support
│   └── tests
├── cypress.config.js
├── .editorconfig
├── .eslintignore
├── .eslintrc.js
├── .gitignore
├── jsconfig.json
├── locales
├── Makefile
├── mrs.developer.json
├── node_modules
├── omelette -> node_modules/@plone/volto/
├── package.json
├── patches
├── .prettierignore
├── public
│   ├── android-chrome-192x192.png
│   ├── android-chrome-512x512.png
│   ├── apple-touch-icon.png
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   ├── favicon.ico
│   ├── icon.svg
│   ├── index.html.spa
│   ├── robots.txt
│   └── site.webmanifest
├── razzle.config.js
├── README.md
├── src
│   ├── actions
│   ├── addons
│   ├── client.js
│   ├── components
│   ├── config.js
│   ├── constants
│   ├── customizations
│   ├── helpers
│   ├── index.js
│   ├── reducers
│   ├── routes.js
│   └── theme.js
├── .storybook
├── theme
│   └── theme.config
├── .yarn
├── yarn.lock
└── .yarnrc.yml
```

## Running the project

To run the project you can type:

```shell
cd my-volto-app
yarn start
```

This will start the server on port 3000.
You can change the port and/or hostname for the frontend by specifying PORT and/or HOST:

```shell
HOST=my_hostname PORT=1234 yarn start
```

Per default the Plone backend runs on port 8080.
If your backend runs on a different port and/or uses a different hostname you can specify the full url:

```shell
RAZZLE_API_PATH=http://localhost:55001/plone yarn start
```
