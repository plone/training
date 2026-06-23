---
myst:
  html_meta:
    "description": "Set up a Plone deployment server with Ansible, Docker, and Docker Swarm"
    "property=og:description": "Set up a Plone deployment server with Ansible, Docker, and Docker Swarm"
    "property=og:title": "Set up your Plone deployment server"
    "keywords": "Plone, deployment, server, setup, Ansible, Docker, Docker Swarm"
---

# Set up your Plone deployment server

Your Plone project's generated code base includes a {file}`/devops/ansible` folder, equipped with tools for provisioning and setting up a basic server installation. We'll utilize **Ansible** for automation, **Docker** for containerization, and **Docker Swarm** for enhanced scalability and availability.

## Navigating to `devops`

Start by changing your directory to {file}`devops/ansible`:

```shell
cd devops/ansible
```

## Configure the environment

Create a new {file}`.env` file by copying the content from the existing `.env_dist` file:

```shell
cp .env_dist .env
```

Customize the {file}`.env` file to match your specific deployment environment. Here's an example configuration:

```shell
DEPLOY_ENV=prod
DEPLOY_HOST=pybr25-<your-github-username>.tangrama.com.br
DEPLOY_PORT=22
DEPLOY_USER=plone
DOCKER_CONFIG=.docker
STACK_NAME=pybr25-<your-github-username>-tangrama-com-br
```

```{note}
The {file}`.env` file is listed in {file}`.gitignore` to prevent pushing environment-specific configurations to the repository.
```

## Install Ansible

Run the following command to create a Python 3 virtual environment and install Ansible with its dependencies:

```shell
make install
```

## Configure the inventory

Update the {file}`devops/ansible/inventory/hosts.yml` file with the appropriate server details:

```yaml
---
cluster:
  hosts:
    pybr25-<your-github-username>.tangrama.com.br:
      ansible_user: root
      ansible_host: pybr25-<your-github-username>.tangrama.com.br
      host: pybr25-<your-github-username>
      hostname: pybr25-<your-github-username>.tangrama.com.br
      swarm_node:
        labels:
          type: manager
          env: production
```


## Initiate server setup

With the correct information in {file}`devops/ansible/inventory/hosts.yml`, test the connection to the server with:

```shell
uv run ansible-playbook playbooks/_connect.yml
```

And then, if the connection is successful, initiate the remote server setup by running:

```shell
uv run ansible-playbook playbooks/setup.yml
```

This command executes the Ansible playbook {file}`devops/playbooks/setup.yml` performing tasks like installing base packages, creating a user, setting up SSH, and initializing Docker Swarm on the remote server:

## Verify remote server access

You should now be able to SSH into the remote server as both **root** and **plone** users:

```shell
ssh root@pybr25-<your-github-username>.tangrama.com.br
ssh plone@pybr25-<your-github-username>.tangrama.com.br
```

# Review

By now you've now successfully set up a Plone deployment server using Ansible for automated provisioning, Docker for containerization, and Docker Swarm for scalability and availability.

The next step is to deploy your project to this server.
