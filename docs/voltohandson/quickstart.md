---
myst:
  html_meta:
    "description": "Set up your project and development environment"
    "property=og:description": "Set up your project and development environment"
    "property=og:title": "Initial project setup"
    "keywords": "Plone, Volto, Training, Setup, Docker"
---

(voltohandson-quickstart-label)=

# Quick Start

## Set Up Volto Project

To create our first volto project we will youse the volto generator tool (https://www.npmjs.com/package/@plone/generator-volto). It needs the Yeoman generator as a dependency. install that with `npm install -g yo` When you have that installed you can use it to generate a brand new volto project. In our case we will use the latest alpha version of Volto by using the `--canary`flag like this:

```shell
yo @plone/volto <project-name> --canary
```

The dialogue in the console will ask you wether you want to install any addons. You can skip by pressing the `enter` button, as we dont want to use any addons for the training.

## Build environments

We need to build two environments.
Start two terminal sessions, one for each environment, Plone and Yarn, and a third session to issue git and other shell commands.
In each terminal session you should be in your project folder `volto-hands-on-training` or whatever you named your project.

### Plone environment

To run our Volto site, we will use the latest Plone 6 backend Docker image.
You can start it by running the following command:

```shell
docker run -p 8080:8080 -e SITE=Plone plone/plone-backend:6.0.0b3
```

Keep that process running during the whole training in one of your terminal windows because the container does not have a persistant storage. So once you stop that container again some of you work might get lost again.

### Yarn environment

To ensure all required dependencies for starting Volto are installed run:

```shell
yarn
```

You can now start up your Volto instance by running the following command:

```shell
yarn start
```

## Volto source code

When developing Volto you will find yourself looking quite often at the Volto source code to see how things are done, the code syntax, and how to clone or override components.
For convenience, a symlink to a copy of the Volto code is set up inside `node_modules` when you run `yarn` in your Volto project folder.
You will find this copy of Volto in the `omelette` folder.

## Recommended plugins

No matter which integrated development environment (IDE) you use, you should also install these plugins for a better workflow:

- Prettier
- ESlint
- prettier-stylelint (for VSCode)
