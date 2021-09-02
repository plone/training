(bootstrap-react-label)=

# Bootstrapping A React Project

## Installing dependencies

First step is to install the correct Node version using {file}`nvm`:

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

To create a new React project type the following:

```console
$ npx create-react-app my-app
```

It will create a folder called `my-app` inside the current folder with the following structure:

```console
my-app
├── README.md
├── node_modules
├── package.json
├── .gitignore
├── public
│   ├── favicon.ico
│   ├── index.html
│   └── manifest.json
└── src
    ├── App.css
    ├── App.js
    ├── App.test.js
    ├── index.css
    ├── index.js
    ├── logo.svg
    └── registerServiceWorker.js
```

## Running The Project

To run the project you can type:

```console
$ cd my-app
$ yarn start
```

This will start the server and open up the website in your preferred browser.
