---
myst:
  html_meta:
    "description": "Step-by-step guide to setting up a Plone deployment server."
    "property=og:description": "Easily set up a Plone deployment server with Ansible, Docker, and Docker Swarm."
    "property=og:title": "Efficient Plone Deployment Server Setup"
    "keywords": "Plone, Deployment, Server, Setup, Ansible, Docker, Docker Swarm"
---

# Setting Up Your Plone Deployment Server

Your Plone project's generated codebase includes a {file}`/devops` folder, equipped with tools for provisioning and setting up a basic server installation. We'll utilize **Ansible** for automation, **Docker** for containerization, and **Docker Swarm** for enhanced scalability and availability.

## Navigating to Devops

Start by changing your directory to {file}`devops`:

```shell
cd devops
```

## Configuring the Environment

Create a new {file}`.env` file by copying the content from the existing `.env_dist` file:

```shell
cp .env_dist .env
```

Customize the {file}`.env` file to match your specific deployment environment. Here's an example configuration:

```shell
DEPLOY_ENV=prod
DEPLOY_HOST=ploneconf2024-<your-github-username>.tangrama.com.br
DEPLOY_PORT=22
DEPLOY_USER=plone
DOCKER_CONFIG=.docker
STACK_NAME=ploneconf2024
```

```{note}
The {file}`.env` file is listed in {file}`.gitignore` to prevent pushing environment-specific configurations to the repository.
```

## Installing Ansible

Run the following command to create a Python 3 virtual environment and install Ansible with its dependencies:

```shell
make setup
```

## Configuring the Inventory

Update the {file}`inventory/hosts.yml` file with the appropriate server details:

```yaml
---
prod:
  hosts:
    ploneconf2024-<your-github-username>.tangrama.com.br:
      ansible_user: root
      host: ploneconf2024-<your-github-username>
      hostname: ploneconf2024-<your-github-username>.tangrama.com.br
```

## Initiating Server Setup

Execute the server setup command. It runs the Ansible playbook {file}`playbooks/setup.yml`, performing tasks like installing base packages, creating a user, setting up SSH, and initializing Docker Swarm on the remote server:

```shell
make server-setup
```

## Verifying Remote Server Access

You should now be able to SSH into the remote server as both **root** and **plone** users:

```shell
ssh root@ploneconf2024-<your-github-username>.tangrama.com.br
ssh plone@ploneconf2024-<your-github-username>.tangrama.com.br
```

## Setting Up Docker

Ensure you're logged into Docker, as the deployment process uses public images. Create a new Docker context for the remote server:

```shell
make docker-setup
```

Confirm the setup by retrieving information about the Docker context:

```shell
make docker-info
```

# Review

By now you've now successfully set up a Plone deployment server using Ansible for automated provisioning, Docker for containerization, and Docker Swarm for scalability and availability.

The next step is to deploy your project to this server.
