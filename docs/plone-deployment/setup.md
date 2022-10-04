---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Training setup

Your computer should have the following software. Please prepare this before the training starts.

## Software

### Operating System

Use recent versions of Linux or macOS.

For macOS users, also have Homebrew installed.

Windows with WSL could work as well but isn't supported at this moment.

### Code Editor

- Code editor of your choice (VSCode, Sublime, VI, Emacs)

### Python

- Python >= 3.9

### Docker & Docker Compose

[Docker](https://docs.docker.com/get-docker/) should be version 20.10.18 or above (Check it with `docker --version`)

[Docker Compose](https://docs.docker.com/compose/install/) should be version 2.10.2 or above (Check it with `docker compose version`)

### Node and Node tools

- Node 16, latest NPM and Yarn

### Vagrant

- [Vagrant](https://www.vagrantup.com/downloads) and VirtualBox

```{note}
We use Vagrant in this training as a replacement for an external server.
```

## External Services

### GitHub Account

Please make sure your computer has the correct keys to your Github account

### Container Registry

During the training we will use the GitHub Container Registry, but everything explained here also applies to Docker Hub usage.

If you are willing to follow the training using Docker Hub as your registry, please:

- Create an account at [Docker Hub](https://hub.docker.com/).
- Configure your local Docker to use Docker Hub credentials with `docker login`

## Cookiecutter

- Install `cookiecutter` on your main Python installation with `pip install cookiecutter`
