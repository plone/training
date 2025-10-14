---
myst:
  html_meta:
    "description": "Step-by-step guide to setting up your system for Plone deployment training"
    "property=og:description": "Plone deployment training setup"
    "property=og:title": "Setting Up for Plone Deployment Training"
    "keywords": "Plone, Deployment, Training, Setup, Installation"
---

# Training setup

Ensure a seamless learning experience by preparing your computer with the necessary software before the training commences.

## Prerequisites

### Operating system

See the Plone 6 documentation for {ref}`plone6docs:create-project-cookieplone-prerequisites-for-installation-label`.

macOS users should have [Homebrew](https://brew.sh/) installed to install missing prerequisites.

### jq

Use your package manager to install [jq](https://jqlang.org/).

`````{tab-set}
````{tab-item} macOS
```shell
brew install jq
```
````

````{tab-item} Unbuntu
```shell
apt install -y jq
```
````

````{tab-item} Debian
```shell
apt-get install jq
```
````
`````


### Git

See the Plone 6 documentation for how to install {ref}`plone6docs:prerequisites-for-installation-git-label`.

### Code editor

Choose a code editor you're comfortable with, such as VSCode, PyCharm, Sublime, vi, or Emacs.

### uv

See the Plone 6 documentation for how to install uv {ref}`plone6docs:prerequisites-for-installation-uv-label`.

### Docker

Ensure Docker version 27.2.0 or above is installed. Verify with:

```shell
docker --version
```

Ensure Docker is running. Verify with:

```shell
docker ps
```

### Node.js and its tools

See the Plone 6 documentation for how to install {ref}`plone6docs:prerequisites-for-installation-nodejs-label`.

````{todo}
In future versions of the cookiecutter template, a `.nvmrc` file will be included to simplify Node.js version management. The commands below will be applicable then.

```shell
nvm install
nvm use
```
````

### External services

#### GitHub account

Make sure your computer is set up with the appropriate keys to access your GitHub account,
as we will be utilizing GitHub extensively throughout this training.

If you are not sure about the keys you have on GitHub, you can check it by accessing the following URL:

`https://github.com/<your-github-username>.keys`

#### Container registry: GitHub or Docker Hub

We'll use the GitHub Container Registry during the training. The concepts are also applicable to Docker Hub. If you prefer Docker Hub:

- Create an account at [Docker Hub](https://hub.docker.com/).
- Configure your local Docker to use Docker Hub credentials.

  ```shell
  docker login
  ```

### Cookieplone

The latest version of {term}`Cookieplone` will be used, and it doesn't require a separate installation as we'll use `uvx`.

### Make

{term}`Make` is pre-installed on most Linux distributions. For macOS, install Xcode and its command-line tools. Windows users are advised to use [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) that includes `make`.

## Troubleshooting

### Insufficient Docker virtual disk space

Docker requires sufficient virtual disk space to install and build images. A typical error message may be: `Could not create directory.` or anything else that mentions writing to the image.
To resolve this, use an appropriate docker system prune option, such as:

```shell
docker system prune -a
```

```{seealso}
[docker system prune](https://docs.docker.com/reference/cli/docker/system/prune/)
```

You can also configure settings for Docker Desktop.
Under {guilabel}`Prefences > Resources > Advanced`, you can configure appropriate settings for virtual disk limit and memory.

```{seealso}
- [Change Docker Desktop settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/)
```

### Insufficient Docker virtual memory

Docker requires sufficient memory to install and build images. See the previous item for details.
