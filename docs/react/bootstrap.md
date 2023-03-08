---
myst:
  html_meta:
    "description": "Bootstrap a react project using create-react-app."
    "property=og:description": "Bootstrap a react project using create-react-app."
    "property=og:title": "Bootstrap React Project"
    "keywords": "Plone, trainings, SEO, yarn, nvm, create-react-app"
---

(bootstrap-react-label)=

# Bootstrapping A React Project

## Installing dependencies

First step is to install the correct Node version using `nvm`:

```shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
```

Then you can install the latest LTS version of Node:

```shell
nvm install --lts
```

Install the package manager `yarn`:

```shell
curl -o- -L https://yarnpkg.com/install.sh | bash
```

## Bootstrapping A Project

To create a new React project type the following:

```shell
npx create-react-app my-app
```

It will create a folder called `my-app` inside the current folder with the following structure:

```console
my-app
├── .gitignore
├── package.json
├── package-lock.json
├── public
│   ├── favicon.ico
│   ├── index.html
│   ├── logo192.png
│   ├── logo512.png
│   ├── manifest.json
│   └── robots.txt
├── README.md
└── src
    ├── App.css
    ├── App.js
    ├── App.test.js
    ├── index.css
    ├── index.js
    ├── logo.svg
    ├── reportWebVitals.js
    └── setupTests.js
```

```{note}
We omit from the structure the files and directories inside the `node_modules` directory because there are too many to list.
```

## Running The Project

To run the project you can type:

```shell
cd my-app
yarn start
```

This will start the server and open up the website in your preferred browser.
