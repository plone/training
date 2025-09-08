---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Installing The Development Environment

First, we need last LTS NodeJS version (8.12.0 at writing time).
We recommend to use nvm to install NodeJS instead of using your OS-based version.

Install nvm on your system using the instructions and provided script at:

<https://github.com/nvm-sh/nvm#install-script>

Using nvm we will look up the latest lts version of NodeJS and install it

```shell
nvm install --lts
nvm use --lts
```

NodeJS is provided with npm, its package manager, we will use it to install the GatsbyJS CLI

```shell
npm install --g gatsby-cli
```

```{note}
`-g` means the CLI will be available globally in our nvm instance.
```

When you are prompted to use either `yarn` or `npm` to install the GatsbyJS CLI, it's ok to use the default, `yarn`.

# Creating a new GatsbyJS site

The CLI allows to initialize a project:

```shell
gatsby new hello-world
```

This command tells gatsby-cli to create a new GatsbyJS project with the name `hello-world` with a basic default file structure.

There are several boilerplates created by the community that allows to bootstrap an application for different use-cases.

These boilerplates are called "starters" and in the [offical site](https://www.gatsbyjs.com/starters/?v=2) you could
find a complete list of available starters. There are starters with some pre-configured themes (for example material-ui or bootstrap), support for authentication, and so on.

There are also some starters that are specialized in integration with some external sources, such as a CMS like Plone or WordPress.
They create a boilerplate with all the configuration to fetch data from the external sources and give some helper methods to build the pages/interface with that specific data, such as the breadcrumbs or navigation.

Data fetching part is usually managed by a different type of plugins called "source-plugins" that can retrieve data from a specific source.

We will cover "source-plugins" in later chapters.

```{note}
To create a new project with a starter, you need to append the github URL of the desired starter in the cli command: `gatsby new [SITE_DIRECTORY] [URL_OF_STARTER_GITHUB_REPO]`
```

```shell
cd hello-world
gatsby develop
```

This command starts a development server.
You will be able to see and interact with your new site in a development environment at <http://localhost:8000>.

Now that we have a working installation, let us go deep inside GatsbyJS to see how it works and what are its main parts.
