---
myst:
  html_meta:
    "description": "Step-by-step guide to setting up your system for Plone deployment training"
    "property=og:description": "Plone deployment training setup"
    "property=og:title": "Setting Up for Plone Deployment Training"
    "keywords": "Plone, Deployment, Training, Setup, Installation"
---

# Training Setup

Ensure a seamless learning experience by preparing your computer with the necessary software before the training commences.

## Prerequisites

### 1. Operating System

Linux/macOS
:   A recent version is preferred. macOS users should have [Homebrew](https://brew.sh/) installed.

Windows
:   Consider using [WSL2 with Ubuntu](https://documentation.ubuntu.com/wsl/en/latest/), though it's not officially tested for this training.

### 2. Code Editor

Choose a code editor you're comfortable with, such as VSCode, PyCharm, Sublime, VI, or Emacs.

### 3. Python

Install Python version 3.11.x or 3.12.x, ensuring that `pip` is included and updated.

```shell
python -m pip install --upgrade pip
```

Install `pipx` and `uv` for managing Python applications:

```shell
python -m pip install --upgrade pipx uv
```

```{tip}
Use [Pyenv](https://github.com/pyenv/pyenv) if your system doesn't provide the required Python version.
```

### 4. Docker

Ensure Docker version 27.2.0 or above is installed. Verify with:

```shell
docker --version
```

Ensure Docker is running. Verify with:

```shell
docker ps
```

### 5. Node and Node Tools

Install the latest Node LTS version using [NVM](https://github.com/nvm-sh/nvm/blob/master/README.md).

```shell
nvm install "lts/*"
```

```{warning}
Ensure to use the Node LTS Version (22) that is officially supported by Volto.
```

```shell
nvm install "22"
```

````{todo}
In future versions of the cookiecutter template, a `.nvmrc` file will be included to simplify Node version management. The commands below will be applicable then.

```shell
nvm install
nvm use
```
````

### 6. External Services

#### GitHub Account

Make sure your computer is set up with the appropriate keys to access your GitHub account,
as we will be utilizing GitHub extensively throughout this training.

#### Container Registry: GitHub or Docker Hub

We'll use the GitHub Container Registry during the training. The concepts are also applicable to Docker Hub. If you prefer Docker Hub:

- Create an account at [Docker Hub](https://hub.docker.com/).
- Configure your local Docker to use Docker Hub credentials.

  ```shell
  docker login
  ```

### 7. Cookieplone

The latest version of {term}`Cookieplone` will be used, and it doesn't require a separate installation as we'll use `pipx`.

### 8. Make

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
- [Change Docker Desktop settings on Mac](https://docs.docker.com/desktop/settings/#advanced)
- [Change Docker Desktop settings on Windows](https://docs.docker.com/desktop/settings/#advanced)
- [Change Docker Desktop settings on Linux](https://docs.docker.com/desktop/settings/#advanced)
```

### Insufficient Docker virtual memory

Docker requires sufficient memory to install and build images. See the previous item for details.
