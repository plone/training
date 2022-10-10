---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
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

## Continuos Integration

### Using GitHub Actions

### Using GitLab CI
