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

```{code-block} shell
source .env_local
make docker-setup
```

## Using provided Makefile

Run `make deploy` to deploy to the server. This command relies on environment variables defined in {file}`.env_local` (or the production env file you created)

```{code-block} shell
make deploy
```
Also use this also when there is a new version of any of the images.

### Check Stack Status

```{code-block} shell
make status
```

### Check Logs

|Tool|Command|
|-|-|
|webserver|`make logs-webserver`|
|frontend|`make logs-frontend`|
|backend|`make logs-backend`|

## Continuous Integration

### Using GitHub Actions

### Using GitLab CI
