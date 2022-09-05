---
myst:
  html_meta:
    "description": "How to install Plone 6"
    "property=og:description": "How to install Plone 6"
    "property=og:title": "Installation and Setup of Plone 6"
    "keywords": "installation, Plone 6"
---

(installation-label)=

# Installation and Setup of Plone 6

Plone is the combination of a backend (data storage) with a frontend (user interface) into a fully featured CMS.

**Plone 6** is an installation of Plone.
By default it uses Volto for the frontend, based on ReactJS, on top of the `plone.restapi` to interact with the backend.
This combines the stability, maturity, and security of the Plone backend with a modern, mature, user-friendly, and well maintained frontend.

**Plone Classic** is another installation of Plone.
It uses Barceloneta, a customized version of Twitter Bootstrap, for the frontend.
It will stay in place as a frontend option, giving developers and users time to adapt to Volto.

See the [Plone road map](https://plone.org/roadmap) for details.

This training is about Plone 6.

(installation-plone-label)=

## Installing Plone backend

Make sure you have a current and by Plone supported **Python 3** version.
One way to achieve is `pyenv` which lets you manage different Python versions.
It even let's you setup virtual Pythons of the same version for individual projects.
<https://github.com/pyenv/pyenv-installer>

```shell
pyenv install 3.9.5
pyenv virtualenv 3.9.5 plonepy
pyenv activate plonepy
```

This installs and activates a Python 3.9.5. It does not affect your system Python as it is an isolated virtual Python environment.

### Prerequisites

The following instructions are based on Ubuntu and macOS.
If you use a different operating system (OS), please adjust them to fit your OS.

On Ubuntu/Debian, you need to make sure your system is up-to-date:

```shell
sudo apt-get update
sudo apt-get -y upgrade
```

Then, you need to install the following packages:

```shell
sudo apt-get install python3.9-dev python3.9-tk python3.9-venv build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev
sudo apt-get install libreadline-dev wv poppler-utils
sudo apt-get install git
```

On MacOS you at least need to install some dependencies with [Homebrew](https://brew.sh/)

```shell
brew install zlib git readline jpeg libpng libyaml
```

```{seealso}
For more information or in case of problems see the [official installation instructions](https://docs.plone.org/manage/installing/installation.html).
```

### Get Plone backend and install

Download Plone from <https://plone.org/download>

Follow the instructions. Select option 'standalone' for your first Plone installation.

```{note}
You do not find a Plone 6 to download?
Well it's not released.
We still do a Plone 6 setup: Plone backend plus Plone frontend.
If Plone backend is still a Plone 5, that's OK.
```

```{eval-rst}
.. TODO::

    Install necessary helpers for Volto frontend: restapi, folderish contenttypes, dexterity root,…

```

(installation-volto-label)=

## Installing Plone frontend

For a Plone 6 installation by now two installations are needed: Plone backend and Volto frontend.
The former section is describing the options for a Plone backend installation.
This section is about setting up a Volto project.

(installation-volto-prerequisites-label)=

### Installing Prerequisites

First {ref}`plone6docs:frontend-getting-started-install-nvm-label`.

{ref}`Install Yarn (JavaScript package manager) <plone6docs:frontend-getting-started-yarn-label>`.


Install `@plone/generator-volto`, the Yeoman Volto App Generator:

```shell
npm install -g yo @plone/generator-volto
```

### Bootstrapping A Project

To create a new Volto project type the following:

```shell
yo @plone/volto
```

Follow the prompts' questions, providing `my-volto-app` as the project name.

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

### Running The Project

To run the project you can type:

```shell
cd my-volto-app
yarn start
```

This will start the server on port 3000.

You can change the port and/or hostname for the frontend by specifying `PORT` and/or `HOST`:

```shell
HOST=my_hostname PORT=1234 yarn start
```

If your backend runs on a different port and/or uses a different hostname you can specify the full URL:

```shell
RAZZLE_API_PATH=http://localhost:55001/plone yarn start
```


## Creating a Plone Website

Now that you have a backend and a frontend up and running, you can create your concrete website for a project.

Create a Plone site object **Plone** on <http://localhost:8080>

Point your browser to <http://localhost:3000> and see that Plone is up and running.

You can stop the Volto app anytime using {kbd}`ctrl + c`.


(installation-hosting-label)=

## Hosting Plone

```{only} not presentation
If you want to host a real live Plone site yourself then running it from your laptop is not a viable option.
```

You can host Plone...

- with one of many professional [hosting providers](https://plone.org/providers)
- on a virtual private server
- on dedicated servers

See all the ways you can [set up Plone](https://plone.org/download)

```{seealso}
Plone Installation Requirements: <https://docs.plone.org/manage/installing/requirements.html>
```


(installation-prod-deploy-label)=

## Production Deployment

The way we are setting up a Plone site during this class may be adequate for a small site
— or even a large one that's not very busy — but you are likely to want to do much more if you are using Plone for anything demanding.

- Using a production web server like Apache or nginx for URL rewriting, SSL and combining multiple, best-of-breed solutions into a single web site.
- Reverse proxy caching with a tool like Varnish to improve site performance.
- Load balancing to make best use of multiple core CPUs and even multiple servers.
- Optimizing cache headers and Plone's internal caching schemes with plone.app.caching.

And you will need to learn strategies for efficient backup and log file rotation.

All these topics are introduced in [Guide to deploying and installing Plone in production](https://docs.plone.org/manage/deploying/index.html).
