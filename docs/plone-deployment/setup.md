---
myst:
  html_meta:
    "description": "Plone deployment training setup"
    "property=og:description": "Plone deployment training setup"
    "property=og:title": "Plone deployment training setup"
    "keywords": "Plone, deployment, training, setup"
---

# Training setup

Your computer should have the following software.
Please prepare this before the training starts.

## Software

### Operating System

Use recent versions of Linux or macOS.

For macOS users, also have Homebrew installed.

Windows with [WSL2 and Ubuntu](https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10) could work too but was not checked for this training.

### Code Editor

Code editor of your choice (VSCode, Pycharm, Sublime, VI, Emacs)

### Python

Python version 3.9.x or 3.10.x.

Ensure Pip is installed and up to date.

```{tip}
If the system does not provide a suitable version, you can use [Pyenv](https://github.com/pyenv/pyenv) to install almost any Python version.
```

### Docker

[Docker](https://docs.docker.com/get-docker/) should be version 20.10.18 or above (Check it with `docker --version`)

### Node and Node tools

Latest Node LTS version (Node 16), latest NPM, Yarn (classic, not 2.x) and Yeoman.

Install [NVM](https://github.com/nvm-sh/nvm/blob/master/README.md).

Use it to install the latest version of Node LTS and NPM (hint: check if a newer minor or bugfix release is available).

```shell
nvm install "lts/*"
```

```{warning}
The current Node LTS Version (Node 18 - v18.12.1) is not supported by Volto at this time.
Use the older LTS Version (Node 16 - currently v16.17.1) instead.
```

```shell
nvm install "16"
```

````{todo}
In an upcoming version of the cookiecutter template, there will be a file `.nvmrc` within the generated project that will simplify and combine the foregoing steps.
When it is released, you will use the following commands.

```shell
nvm install
nvm use
```

````

Now with a current Node LTS version installed, install additional tools globally:

* Yeoman
* Yarn

```shell
nvm alias default "lts/*"
npm install -g yo
npm install -g yarn
```

Then execute `curl -o- -L https://yarnpkg.com/install.sh | bash` to install Yarn.

### Vagrant

- [Vagrant](https://developer.hashicorp.com/vagrant/downloads) and VirtualBox or libvirt (Linux / macOS).

```{warning}
VirtualBox does not run on Apple Silicon, use libvirt+qemu instead.
```

```{note}
We use Vagrant boxes in this training as a replacement for an external server.
```

## External Services

### GitHub Account

Please make sure your computer has the correct keys to your Github account.

### Container Registry

During the training we will use the GitHub Container Registry, but everything explained here also applies to Docker Hub usage.
If you are willing to follow the training using Docker Hub as your registry, please:

- Create an account at [Docker Hub](https://hub.docker.com/).
- Configure your local Docker to use Docker Hub credentials with `docker login`

While Gitlab with it's container registry works the same, we do not include it in the training.

## Cookiecutter

- Install or upgrade {term}`Cookiecutter` in your user's Python:

```shell
pip install --user --upgrade cookiecutter
```

## Make

{term}`Make` comes installed on most Linux distributions.
On macOS, you must first [install Xcode](https://developer.apple.com/xcode/resources/), then install its command line tools.
On Windows, it is strongly recommended to [Install Linux on Windows with WSL](https://learn.microsoft.com/en-us/windows/wsl/install), which will include `make`.
