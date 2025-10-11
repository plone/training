---
myst:
  html_meta:
    "description": "Step-by-step guide to setting up a Plone deployment server."
    "property=og:description": "Easily set up a Plone deployment server with Ansible, Docker, and Docker Swarm."
    "property=og:title": "Efficient Plone Deployment Server Setup"
    "keywords": "Plone, Deployment, Server, Setup, Ansible, Docker, Docker Swarm"
---

# Setting Up Your Plone Deployment Server

Your Plone project's generated codebase includes a {file}`/devops/ansible` folder, equipped with tools for provisioning and setting up a basic server installation. We'll utilize **Ansible** for automation, **Docker** for containerization, and **Docker Swarm** for enhanced scalability and availability.

## Navigating to Devops

Start by changing your directory to {file}`devops/ansible`:

```shell
cd devops/ansible
```

## Configuring the Environment

Create a new {file}`.env` file by copying the content from the existing `.env_dist` file:

```shell
cp .env_dist .env
```

Customize the {file}`.env` file to match your specific deployment environment. Here's an example configuration:

```shell
DEPLOY_ENV=prod
DEPLOY_HOST=ploneconf2025-<your-github-username>.tangrama.com.br
DEPLOY_PORT=22
DEPLOY_USER=plone
DOCKER_CONFIG=.docker
STACK_NAME=ploneconf2025-<your-github-username>-tangrama-com-br
```

```{note}
The {file}`.env` file is listed in {file}`.gitignore` to prevent pushing environment-specific configurations to the repository.
```

## Installing Ansible

Run the following command to create a Python 3 virtual environment and install Ansible with its dependencies:

```shell
make install
```

## Configuring the Inventory

Update the {file}`devops/ansible/inventory/hosts.ym` file with the appropriate server details:

```yaml
---
cluster:
  hosts:
    ploneconf2025-<your-github-username>.tangrama.com.br:
      ansible_user: root
      ansible_host: ploneconf2025-<your-github-username>.tangrama.com.br
      host: ploneconf2025-<your-github-username>
      hostname: ploneconf2025-<your-github-username>.tangrama.com.br
      swarm_node:
        labels:
          type: manager
          env: production
```



## Initiating Server Setup

With the correct information in {file}`devops/ansible/inventory/hosts.yml`, test the connection to the server with:

```shell
uv run ansible-playbook playbooks/_connect.yml
```

And then, if the connection is successful, initiate the remote server setup by running:

```shell
uv run ansible-playbook playbooks/setup.yml
```

This command executes the Ansible playbook {file}`devops/playbooks/setup.yml` performing tasks like installing base packages, creating a user, setting up SSH, and initializing Docker Swarm on the remote server:

## Verifying Remote Server Access

You should now be able to SSH into the remote server as both **root** and **plone** users:

```shell
ssh root@ploneconf2025-<your-github-username>.tangrama.com.br
ssh plone@ploneconf2025-<your-github-username>.tangrama.com.br
```

# Review

By now you've now successfully set up a Plone deployment server using Ansible for automated provisioning, Docker for containerization, and Docker Swarm for scalability and availability.

The next step is to deploy your project to this server.
