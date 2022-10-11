---
myst:
  html_meta:
    "description": "Plone deployment server setup"
    "property=og:description": "Plone deployment server setup"
    "property=og:title": "Plone deployment server setup"
    "keywords": "Plone, deployment, server, setup"
---

# Server Setup

The generated codebase contains a {file}`/devops` folder with the tools needed to provision and setup a basic installation of your Plone project using {term}`Ansible` and {term}`Docker`.

## Install Dependencies

Change to the {file}`devops` folder in your project directory.

```{code-base} shell
cd devops
```

And then install all dependencies.

```{code-block} shell
source .env_local
make clean
make setup
```

This will create a new Python 3 virtual environment with Ansible.

## Provisioning the Server

We are using Vagrant in this training, and to create a new Vagrant box, as defined in the {file}`Vagrantfile`, run:

```shell
make provision
```
## Ansible Playbook

### Configure SSH key

Edit the `group_vars/users.yml` file and replace the line **public_keys: []** with

```{code-block} yaml
    public_keys:
      - '<your ssh public key>'
```
### Run playbook

Setup the server, by installing base packages, creating `UFW` configuration and adding users

```shell
make run-playbook
```

### For Production

Create `.env_prod`, if it does not exist, setting all values defined in `.env_local`, then:

```{code-block} shell
source .env_prod
```

Also, add a `prod.yml` file to `inventory` folder (with information about the production server), and a `plone-conference-prod.yml` to `host_vars` folder.
