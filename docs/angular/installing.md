---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Installing The Development Environment

First, we need NodeJS 6.10+. We recommend to use nvm to install NodeJS instead of using your OS-based version.

Install nvm on your system using the instructions and provided script at:

<https://github.com/nvm-sh/nvm#install-script>

Using nvm we will look up the latest lts version of NodeJS and install it

```shell
nvm ls-remote --lts
nvm install v6.10
nvm use v6.10
```

NodeJS is provided with npm, its package manager, we will use it to install the Angular CLI (ng)

```shell
npm install -g @angular/cli@latest
```

```{note}
`-g` means the CLI will be available globally in our nvm instance.
```

# Initializing A New Project

The CLI allows to initialize a project:

```shell
ng new training --style=scss
```

```{note}
`--style=scss` indicates we will use SCSS for style sheets.
```

If we inspect our newly created `./training`, we see a default Angular project structure:

- the sources are managed in the `./src` folder,
- the dependencies are declared in `package.json`,
- and they are installed in the `./node_modules` folder.

We can serve our project locally using the CLI.

```shell
cd ./training
ng serve
```

The result can be seen on <http://localhost:4200>.

This development server offers the different features we can expect for a convenient frontend development environment
like autoreload and sourcemaps.

The CLI also allows to run the tests:

```shell
ng test
```
