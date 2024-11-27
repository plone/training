---
myst:
  html_meta:
    "description": "Terms and definitions used throughout the Plone Training documentation."
    "property=og:description": "Terms and definitions used throughout the Plone Training documentation."
    "property=og:title": "Glossary"
    "keywords": "Plone, training, glossary, term, definition"
---

(glossary-label)=

# Glossary

```{glossary}
:sorted: true

AWS
    [Amazon Web Services](https://aws.amazon.com/) offers reliable, scalable, and inexpensive cloud computing services.
    Free to join, pay only for what you use.

Linode
    [Linode.com](https://www.linode.com/) is an American privately owned virtual private server provider company based in Galloway, New Jersey, United States.

DigitalOcean
    [DigitalOcean, Inc.](https://www.digitalocean.com/) is an American cloud infrastructure provider headquartered in New York City with data centers worldwide.

ZODB
    [A native object database for Python](https://zodb.org/en/latest/).

Barceloneta
    The default theme for Plone 5.

CMS
    Content Management System

CSS
    Cascading Style Sheets (CSS) is a style sheet language used for describing the (most of the times visual) representation of web pages.

Grunt
    The JavaScript Task Runner.
    Automates the creation and manipulation of static assets for the theme.

Less
    A dynamic style sheet language that can be compiled into {term}`CSS` (Cascading Style Sheets).

NPM
    npm is a package manager for the JavaScript programming language.
    It is the default package manager for the JavaScript runtime environment Node.js.
    Also a registry of JavaScript packages, similar to PyPI.

TTW
    Through-The-Web, changes in the browser.

S3
    [Amazon Web Services S3](https://aws.amazon.com/s3/).
    Object storage built to store and retrieve any amount of data from anywhere.

NFS
    [Network File System](https://en.wikipedia.org/wiki/Network_File_System).

Ansible
    [Ansible](https://www.ansible.com/) is an open source automation platform.
    Ansible can help you with configuration management, application deployment, task automation.

Archetypes
    The deprecated framework for building content types in Plone.

Chef
    [A configuration management tool written in Ruby and Erlang](https://www.chef.io/products/chef-infra/).

CloudFormation
    [AWS CloudFormation](https://aws.amazon.com/cloudformation/) gives developers and systems administrators a way to create and manage a collection of related AWS resources, provisioning and updating them in an orderly and predictable fashion.

Travis CI
    Travis CI is a hosted, distributed continuous integration service used to build and test software projects hosted at GitHub.
    Open source projects may be tested with limited runs via [travis-ci.com](https://www.travis-ci.com/).

Solr
    [Solr](https://solr.apache.org/) is a popular, blazing-fast, open source enterprise search platform built on Apache Lucene.

ZCML
    The [Zope Configuration Mark-up Language](https://5.docs.plone.org/develop/addons/components/zcml.html).

Diazo
    [Diazo theme engine guide](https://docs.diazo.org/en/latest/).
    Diazo allows you to apply a theme contained in a static HTML web page to a dynamic website created using any server-side technology.

Dexterity
    [Dexterity](https://github.com/plone/plone.dexterity), the base framework for building content types, both through-the-web and as filesystem code for Zope.

Dublin Core
    The Dublin Core Schema is a small set of vocabulary terms that can be used to describe web resources (video, images, web pages, and other online content).
    It can also be used to describe physical resources such as books or CDs, and objects like artworks.

ZMI
    The Zope Management Interface.
    The ZMI is a direct interface into the backend software stack of Plone.
    While it can still serve as a valuable tool for Plone specialists to fix problems or accomplish certain tasks, it is not recommended as a regular tool for Plone maintenance.

TALES
    TAL Expression Syntax (TALES) expression, which by default expects a path.
    Python and string expressions are also allowed.

XML
    The Extensible Markup Language.

XSLT
    The Extensible style sheet language Transformations.
    A language which defines elements to describe transformations to be applied on a document.

XPath
    XPath (XML Path Language) is a query language for selecting nodes from an XML document.

Rapido application
    It contains the features you implement.
    It is a folder containing templates, Python code, and YAML files.

block
    Blocks display chunks of HTML that can be inserted into your Plone pages.

element
    Elements are the dynamic components of your blocks.
    They can be input fields, buttons, or computed HTML.
    They can also return JSON if you call them from a JavaScript app.

record
    A Rapido app is able to store data as records.
    Records are basic dictionaries.

Project (Volto)
    The product of running `create-volto-app`, a customizable instance of Volto.

Add-on (Volto)
    A JavaScript package that integrates with Volto's configuration registry.

Add-on configuration loader (Volto)
    A function with signature `config => config`.

Configuration registry (Volto)
    A singleton object modeled using JavaScript modules, accessible from the Volto
    project using the `~/config` path.

Shadowing (Volto)
    Webpack provides an "alias" mechanism, where the path for a module can be aliased to another module.
    By using this mechanism Volto enables customization (file overrides), similar to `z3c.jbot.`

Razzle
    A tool that simplifies SPA and SSR configuration for React projects.

Webpack
    A tool that loads and bundles code and web resources using loaders.

Webpack entrypoint
    The main files generated by webpack as a result.
    They typically contain the application source code based on modules bundled together, but it can also include other resources, such as static resources.
    They can contain code to automatically trigger the load of other JavaScript code files called "chunks".

Babel
    A JavaScript compiler that "transpiles" newer standards JavaScript to something that any browser can load.

Express
    [Express](https://expressjs.com/) is a minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications.
    Volto uses Express.

Server-Side Rendering (SSR)
    When first loading any Plone page, users will get HTML markup that closely matches the final DOM structure of the React components used to render that page.

Single Page Application (SPA)
    A type of JavaScript application that aims to provide a better user experience by avoiding unnecessary reloading of the browser page, instead using AJAX to load backend information.

Hot Module Replacement (HMR)
    A development feature provided by Webpack that automatically reloads, in the browser, the JavaScript modules that have changed on disk.

Yeoman
    A popular scaffolding tool similar to Plone's `mr.bob` or `ZopeSkel`.

CommonJS
    A JavaScript package standard, the equivalent of a Python wheel or egg.
    Enables JavaScript modules.

Transpilation
    The transformation of JavaScript code that uses advanced language features, unavailable for some browsers, to code rewritten to support them.

ES6
ECMAScript 6
    [ECMAScript 6 (ES6)](https://262.ecma-international.org/6.0/) is a scripting language specification on which [JavaScript](https://developer.mozilla.org/en-US/docs/Glossary/JavaScript) is based.
    [Ecma International](https://ecma-international.org/) is in charge of standardizing ECMAScript.

mrs-developer
    Also called "missdev", a tool similar to buildout's `mr.developer`.
    It automatically downloads and keeps up to date copies of software and add-ons under development based on definitions stored in `mrs.developer.json`.
    As a byproduct of its update operations, it also automatically adjusts `jsconfig.json`, which is used by Volto to configure webpack aliases.

Yarn
    A popular JavaScript package manager similar to NPM.

Hydration (SSR)
    After loading an HTML page generated with SSR in the browser, React can "populate" the existing DOM elements, recreate and attach their coresponding components.

JSX
    A dialect of JavaScript that resembles XML, it is transpiled by Babel to JavaScript functions.
    React uses JSX as its component templating.

Scoped packages
    Namespace for JavaScript packages, they provide a way to avoid naming conflicts for common package names.

middleware (Redux)
    Custom wrappers for the Redux store dispatch methods.
    They allow customizing the behavior of the data flow inside the redux store.

hooks (React)
    Hooks are a React API that allow function components to use React features such as lifecycle methods, states, and so on.

hoisting (Yarn)
    An optimization provided by Yarn.
    By default JavaScript packages will directly include dependencies inside their local node_modules.
    By hoisting we're "lifting" these inner dependencies to the top level `node_modules` directory, and thus optimize the generated bundles.
    In case two dependencies have conflicting version dependencies of the same library, the hoisting will not be possible (for that conflicting dependency) and you'll see multiple instances of the same library in the bundle, or you'll see that the add-on receives its own `node_modules` folder.

React
    [React](https://react.dev/) is a JavaScript library for building user interfaces.
    Volto, the frontend for Plone 6, uses React.

Sphinx
    [Sphinx](https://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation.
    It was originally created for Python documentation, and it has excellent facilities for the documentation of software projects in a range of languages.
    Sphinx uses {term}`reStructuredText` as its markup language, and many of its strengths come from the power and straightforwardness of reStructuredText and its parsing and translating suite, {term}`Docutils`.

Docutils
    [Docutils](https://docutils.sourceforge.io/) is an open-source text processing system for processing plaintext documentation into useful formats, such as HTML, LaTeX, man-pages, OpenDocument, or XML.
    It includes {term}`reStructuredText`, the easy to read, easy to use, what-you-see-is-what-you-get plaintext markup language.

reStructuredText
    [reStructuredText (rST)](https://docutils.sourceforge.io/rst.html) is an easy-to-read, what-you-see-is-what-you-get plaintext markup syntax and parser system.
    The Training documentation was written in reStructuredText originally, then converted to {term}`MyST` in 2021.

MyST
    [Markedly Structured Text (MyST)](https://myst-parser.readthedocs.io/en/latest/) is a rich and extensible flavor of Markdown, for authoring training documentation.

Markdown
    [Markdown](https://daringfireball.net/projects/markdown/) is a text-to-HTML conversion tool for web writers.

fence
    A method to extend basic MyST syntax.
    You can define a directive with backticks (`` ` ``) followed by a reStructuredText directive in curly brackets (`{}`), and a matching number of closing backticks.
    You can also nest fences by increasing the number of backticks.

    `````md
    ````{warning}
    There be dragons!
    ```{important}
    Dragons have feelings, too!
    ```
    ````
    `````

    ````{warning}
    There be dragons!
    ```{important}
    Dragons have feelings, too!
    ```
    ````

Open Graph
    The [Open Graph protocol](https://ogp.me/) enables any web page to become a rich object in a social graph.
    For instance, this is used on Facebook to allow any web page to have the same functionality as any other object on Facebook.


mxdev
    [mxdev](https://github.com/mxstack/mxdev) [mɪks dɛv] is a utility that makes it easy to work with Python projects containing lots of packages, of which you only want to develop some.
    It is designed for developers who use stable version constraints, then layer their customizations on top of that base while using a version control system.
    This design allows developers to override their base package constraints with a customized or newer version.

plonecli
    A Plone CLI for creating Plone packages. [plonecli usage](https://github.com/plone/plonecli)

Cookiecutter
    A command-line utility that creates projects from cookiecutters (project templates), for example, creating a Python package project from a Python package project template.
    [See Cookiecutter's documentation](https://cookiecutter.readthedocs.io/en/stable/).

Cookieplone
    ```{versionadded} Volto 18.0.0-alpha.43
    ```

    [Cookieplone](https://github.com/plone/cookieplone) is the method to create a Plone project.
    You can use Cookieplone to build a backend add-on, a new Volto add-on, or a full project with both backend and frontend.
    Cookieplone simplifies the process using robust Cookiecutter templates from {term}`cookieplone-templates`.

cookieplone-templates
    [`cookieplone-templates`](https://github.com/plone/cookieplone-templates) is a collection of templates used by {term}`Cookieplone`.

GenericSetup
    [GenericSetup](https://5.docs.plone.org/develop/addons/components/genericsetup.html) is a framework to modify the Plone site during add-on package installation and uninstallation.
    It provides XML-based rules to change the configuration settings.

cookiecutter-plone-starter
    [cookiecutter-plone-starter](https://github.com/collective/cookiecutter-plone-starter) is a `cookiecutter` template, created by the Plone community, to bootstrap
    a new Plone 6 project using Volto and a relational database.

Traefik
    [Traefik](https://doc.traefik.io/traefik/) is an open-source reverse proxy and load balancer designed to handle HTTP and TCP applications.
    It simplifies the deployment and routing of services and is particularly well-suited for cloud-native and containerized environments,
    offering features like automatic service discovery, middleware plugins, and robust security options.

Nginx
    [Nginx](https://nginx.org/en/) is a high-performance web server, reverse proxy, and load balancer that is known for its speed, reliability, and flexibility.
    It can also serve as a mail proxy server and provides features for HTTP and TCP/UDP applications, making it a popular choice for serving web content,
    optimizing resource utilization, and enhancing web performance and security.

Varnish
    [Varnish](https://varnish-cache.org/intro/) is a high-performance HTTP accelerator and reverse proxy caching server designed to speed up web applications by caching content in memory.
    It serves stored content to users quickly, reducing the load on web servers and enhancing the overall user experience by delivering web pages at high speed.
