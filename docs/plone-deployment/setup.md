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

- Python >= 3.7

### Docker & Docker Compose

[Docker](https://docs.docker.com/get-docker/) should be version 20.10.9 or above (Check it with `docker --version`)

[Docker Compose](https://docs.docker.com/compose/install/) should be version 1.29.2 or above (Check it with `docker-compose --version`)

### Node and Node tools

- Node 14, latest NPM and Yarn

### Vagrant

- [Vagrant](https://www.vagrantup.com/downloads) and VirtualBox

## External Services

### Github Account

Please make sure your computer has the correct keys to your Github account

### Docker Hub

- Create an account at [Docker Hub](https://hub.docker.com/).
- Configure your local Docker to use Docker Hub credentials with `docker login`

## Code Repository

- Fork the repository at [https://github.com/collective/training-deploy-project](https://github.com/collective/training-deploy-project) to your Github account.
- Clone the new repository to your local computer i.e.: `git clone git@github.com:plone/training-deploy-project.git`
- Open the repository with your favorite text editor i.e.: `cd training-deploy-project && code ./`
- Find all occurrences of **DOCKER_HUB_USER_CHANGE_ME** and replace it with your Docker Hub username
