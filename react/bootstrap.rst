.. _bootstrap-label:

=============================
Bootstrapping A React Project
=============================

Installing dependencies
=======================

First step is to install the correct Node version using :file:`nvm`:

.. code-block:: console

    $ curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash

Then you can install the latest LTS version of node:

.. code-block:: console

    $ nvm install v8.11.3

We use the package manager :file:`yarn`, to install do:

.. code-block:: console

    $ npm install -g yarn

And add the :file:`create-react-app` package:

.. code-block:: console

    $ yarn global add create-react-app

Bootstrapping A Project
=======================

To create a newReactproject type the following:

.. code-block:: console

    $ create-react-app my-app

It will create a folder called `my-app` inside the current folder with the following structure:

.. code-block:: console

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

Running The Project
===================

To run the project you can type:

.. code-block:: console

    $ cd my-app
    $ yarn start

This will start the server and open up the website in your preferred browser.
