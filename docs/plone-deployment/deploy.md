---
myst:
  html_meta:
    "description": "Deploy Plone via make, GitHub Actions, or Gitlab CI"
    "property=og:description": "Deploy Plone via make, GitHub Actions, or Gitlab CI"
    "property=og:title": "Deploy Plone via make, GitHub Actions, or Gitlab CI"
    "keywords": "Deploy, Plone, Makefile, GitHub Actions, Gitlab CI"
---

# Deploy

Create a Docker context based on the environment to be used.

```shell
source .env_dev
make docker-setup
```

## Using provided Makefile

Run `make deploy` to deploy to the server. This command relies on environment variables defined in {file}`.env_dev` (or the production env file you created)

```shell
make deploy
```

Also use this command when there is a new version of any of the images.

### Check Stack Status

```shell
make status
```

Once everything is running, and if your deployment was local (with Vagrant), you will be able to visit your website at `https://plone-conference.localhost`.

### Check Logs

|Tool|Command|
|-|-|
|webserver|`make logs-webserver`|
|frontend|`make logs-frontend`|
|backend|`make logs-backend`|

## Continuous Integration

### Using GitHub Actions

### Using GitLab CI
