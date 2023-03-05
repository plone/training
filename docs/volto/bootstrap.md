---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(bootstrap-volto-label)=

# Bootstrapping A Volto Project

## Installing Plone

In order to run Volto you need a backend.
This can be either Plone or Guillotina.
For this course we will use Plone, you can download Plone at <https://plone.org/download>.
We need plone.restapi, so make sure you have that installed and configured correctly.
For an example look into the api folder of the Volto repository: <https://github.com/plone/volto/tree/master/api>

```{warning}
Make sure you set a CORS policy or things tend to magically go wrong. See <https://github.com/plone/volto/blob/master/api/buildout.cfg> for an example.
```

(install-deps-volto-label)=

## Installing Prerequisites

First {ref}`plone6docs:frontend-getting-started-install-nvm-label`.

{ref}`Install Yarn <plone6docs:frontend-getting-started-yarn-label>`.

Install `@plone/generator-volto`:

```shell
npm install -g yo @plone/generator-volto
```

## Bootstrapping A Project

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
├── build
├── create-sentry-release.sh
├── cypress
│   ├── fixtures
│   ├── .gitkeep
│   ├── integration
│   ├── plugins
│   └── support
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
├── yarn.lock
└── .yarnrc
```

## Running The Project

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

If your backend runs on a different port and/or uses a different hostname you can specify the full url:

```shell
RAZZLE_API_PATH=http://localhost:55001/plone yarn start
```
