---
myst:
  html_meta:
    "description": "Bootstrap Volto"
    "property=og:description": "Bootstrap Volto"
    "property=og:title": "Bootstrap Volto"
    "keywords": "Volto, Plone, Newbie"
---

# Bootstrap Volto

```{warning}
For the most up-to-date information on how to get started with Volto, the official [Plone documentation](https://6.docs.plone.org/install/index.html) is the canonical version.
A copy of this information is placed here, with the caveat that it may be out of date by the time you're reading this.
```

## Install nvm (NodeJS version manager)

If you have a working Node JavaScript development already set up on your machine or you prefer
another management tool to install/maintain node this step is not needed. If you have less
experience with setting up JavaScript, it's a good idea to integrate nvm for development, as
it provides easy access to any NodeJS released version.

1.  Open a terminal console and type:

    ```bash
    touch ~/.bash_profile
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.39.1/install.sh | bash
    ```

    (Please check the latest available version of nvm on the [main README](https://github.com/nvm-sh/nvm)

2.  Close the terminal and open a new one or execute:

    ```bash
    source ~/.bash_profile
    ```

3.  Test it:

    ```bash
    nvm version
    ```

4.  Install any active LTS version of NodeJS (https://github.com/nodejs/release#release-schedule):

    ```bash
    nvm install 18
    nvm use 18
    ```

5.  Test NodeJS:

    ```bash
    node -v
    ```

    ```{note}
    If you're using the fish shell, you can use [nvm.fish](https://github.com/jorgebucaran/nvm.fish)
    ```

    ```{note}
    Volto supports currently active NodeJS LTS versions based on [NodeJS
    Releases page](https://github.com/nodejs/release#release-schedule), starting with Node 12 LTS.
    ```


(frontend-getting-started-yarn-label)=

## Yarn (NodeJS package manager)

Install the Yarn Classic version (not the 2.x one!), of the popular node package manager.

1. Open a terminal and type:

    ```bash
    curl -o- -L https://yarnpkg.com/install.sh | bash
    ```

2. Test it, running:

    ```bash
    yarn -v
    ```

    ```{tip}
    As alternative, you can install `yarn` using several approaches too, depending on the
    platform you are on. Take a look at the original `yarn`
    [documentation](https://classic.yarnpkg.com/lang/en/) for a list of them.
    ```


(frontend-getting-started-use-or-install-docker-label)=

## Use or Install Docker

In order to run the API backend, it's recommended to start run it in a container.
For this getting started section we assume you are either using Linux, or Mac. Most
modern Linux distributions have docker in their package manager available.

To install Docker desktop for Mac, here are the detailed instructions:

    https://hub.docker.com/editions/community/docker-ce-desktop-mac

1. Download the appropriate .dmg for your Intel or Apple chip.

2. Install the package as any other Mac software, if required, follow
   instructions from:

    https://docs.docker.com/desktop/install/mac-install/

3. Check that docker is installed correctly, open a new terminal and type:

    ```shell
    docker ps
    ```

    should not throw an error and show the current running containers.


(frontend-getting-started-run-a-volto-ready-plone-docker-container-label)=

## Run a Volto ready Plone Docker container

When you have installed Docker, you can use the official Plone Docker container with the proper configuration for Volto using the `plone.volto` add'on right away by issuing:

```shell
docker run -it --rm --name=backend -p 8080:8080 -e SITE=Plone plone/server-dev
```

```{tip}
This setup is meant only for demonstration and quick testing purposes (since it destroys the container on exit (`--rm`)).
In case you need production ready deployment, check the training {doc}`/plone-deployment/index`.
```

```{note}
The example above does not persist yet any changes you make through Volto in
the Plone docker container backend! For this you need to map the /data directory
in the container properly. Check Docker
[storage documentation](https://docs.docker.com/engine/storage/) for more information.

As a quick example: if you add
`--mount type=bind,source="$(pwd)/plone-data",target=/data`
to the previous example. The local subdirectory plone-data relative to where you
execute `docker run` will be use to persist the backend server data.
```

If you are somewhat familiar with Python development, you can also install Plone locally
without using Docker. Check the {doc}`../getting-started` section.
It also has more information on plone.volto.


(frontend-getting-started-install-volto-label)=

## Install Volto

Use the project generator helper utility.

1.  Open a terminal and execute:

    ```bash
    $ npm install -g yo @plone/generator-volto
    $ yo @plone/volto
    ```

2.  Answer to the prompted questions and provide the name of the new app (folder) to be created. For the sake of this documentation, provide `myvoltoproject` as project name then.

    ````{note}
    You can run the generator with parameters to tailor your requirements.

    ```bash
    yo @plone/volto --help
    ```

    or take a look at the [README](https://github.com/plone/volto/blob/main/packages/generator-volto/README.md) for more information.
    ````

3.  Change directory to the newly created folder `myvoltoapp` (or the one you've chosen):
    ```bash
    cd myvoltoapp
    ```

    Then start Volto with:

    ```bash
    yarn start
    ```

    This command will build an in-memory bundle and execute Volto in development mode.
    Open a browser to take a look at http://localhost:3000

    ```{danger}
    `create-volto-app` was deprecated from January 2021, in favor of [@plone/generator-volto](https://github.com/plone/generator-volto).
    ```


(frontend-getting-started-build-the-production-bundle-label)=

## Build the production bundle

In production environments, you should build an static version of your (Volto) app. The
app should be run in a node process (because of the server side rendering
part), but it also have a client part that is provided and deployed by the server
side rendering process.

1.  Compile the app using the command:

    ```bash
    yarn build
    ```
    The resultant build is available in the `build` folder.

2.  Run the Volto Nodejs process
    ```bash
    yarn start:prod
    ```

    to run the node process with the production build. You can also run it manually:

    ```bash
    NODE_ENV=production node build/server.js
    ```
    Your production ready Volto will be available in http://localhost:3000

