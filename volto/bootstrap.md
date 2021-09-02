(bootstrap-volto-label)=

# Bootstrapping A Volto Project

## Installing Plone

On order to run Volto you need a backend.
This can be either Plone or Guillotina.
For this course we will use Plone, you can download Plone at <https://plone.org/download>.
We need plone.restapi, so make sure you have that installed and configured correctly.
For an example look into the api folder of the Volto repostory: <https://github.com/plone/volto/tree/master/api>

```{warning}
Make sure you set a CORS policy or things tend to magically go wrong. See <https://github.com/plone/volto/blob/master/api/buildout.cfg> for an example.
```

(install-deps-volto-label)=

## Installing Dependencies

First step is to install the correct Node version using `nvm`:

```console
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
```

Then you can install the latest LTS version of node:

```console
$ nvm install --lts
```

We use the package manager {file}`yarn`, to install do:

```console
$ curl -o- -L https://yarnpkg.com/install.sh | bash
```

## Bootstrapping A Project

To create a new volto project type the following:

```console
$ npx @plone/create-volto-app my-volto-app
```

It will create a folder called `my-volto-app` inside the current folder with the following structure:

```console
my-volto-app
├── README.md
├── node_modules
├── package.json
├── .babelrc
├── .eslintrc
├── .gitignore
├── .yarnrc
├── locales
├── public
│   ├── favicon.ico
│   └── robots.txt
├── theme
│   └── theme.config
└── src
    ├── actions
    ├── components
    ├── constants
    ├── customizations
    ├── helpers
    ├── reducers
    ├── client.js
    ├── config.js
    ├── index.js
    └── routes.js
```

## Running The Project

To run the project you can type:

```console
$ cd my-volto-app
$ yarn start
```

This will start the server on port 3000.
You can change the port and/or hostname for the frontend by specifying PORT and/or HOST:

```console
$ HOST=my_hostname PORT=1234 yarn start
```

If your backend runs on a different port and/or uses a different hostname you can specify the full url:

```console
$ RAZZLE_API_PATH=http://localhost:55001/plone yarn start
```
