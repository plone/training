---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
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

### Docker & Docker Compose

[Docker](https://docs.docker.com/get-docker/) should be version 20.10.18 or above (Check it with `docker --version`)

[Docker Compose](https://docs.docker.com/compose/install/) should be version 2.10.2 or above (Check it with `docker compose version`)


### Node and Node tools

Node 16, latest NPM, Yarn (classic, not 2.x) and Yeoman.

Install [NVM](https://github.com/nvm-sh/nvm/blob/master/README.md).

Use it to install Node 16 and NPM (hint: check if a newer minor or bugfix release is available).

```bash
nvm install v16.17.1
nvm alias default v16.17.1
```

Now, having Node installed, install Yeoman.

```bash
npm install -g yo
```

Then execute `curl -o- -L https://yarnpkg.com/install.sh | bash` to install Yarn.

### Vagrant

- [Vagrant](https://www.vagrantup.com/downloads) and VirtualBox or libvirt (Linux)

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
