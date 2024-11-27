---
myst:
  html_meta:
    "description": "Learn how to deploy Plone using make, GitHub Actions, or Gitlab CI with ease."
    "property=og:description": "A comprehensive guide to deploying Plone via various methods."
    "property=og:title": "Efficiently Deploy Plone: A Step-by-Step Guide"
    "keywords": "Deploy, Plone, Makefile, GitHub Actions, Gitlab CI"
---

# Deploying the Project

## Project Stack

This guide outlines the steps to deploy the project using a Docker stack comprising:

- **Traefik:** A router and SSL termination tool, integrated with [Let's Encrypt](https://letsencrypt.org/) for complimentary SSL certificates.
- **Plone Frontend using Volto:** A service based on React for the frontend.
- **Plone Backend:** The API service.
- **Postgres 14 Database:** Handles data persistence.

You can find this stack at {file}`devops/stacks/ploneconf2024-<your-github-username>.tangrama.com.br.yml`. It's modular, allowing easy integration of additional services like {term}`Varnish`, `Solr`, or `ElasticSearch`.

## Building Docker Images

Ensure you build the Docker images for the Frontend and Backend servers before deployment. GitHub Actions, configured in {file}`.github/workflows/backend.yml` and {file}`.github/workflows/frontend.yml`, facilitate this process.

````{important}
Before deploying, push all code changes and ensure GitHub Actions successfully complete their runs. Execute these commands to format the code and run tests:

```shell
make check
make test
```
````


## Manual Deployment with `devops/Makefile`

Utilize the `Makefile` at {file}`devops/Makefile` for manual deployment.

### Deploying the Stack

Execute the following command to deploy the stack defined in {file}`devops/stacks/ploneconf2024-<your-github-username>.tangrama.com.br.yml` to the remote server:

```shell
make stack-deploy
```

### Verifying Stack Status

To check the status of all services in your stack, run:

```shell
make stack-status
```

### Creating Plone Site

On the initial deployment, the frontend containers might be unhealthy due to the unconfigured Plone site on the backend. Create a new site with:

```shell
make stack-create-site
```

### Monitoring Logs

Monitor the logs of each service with these commands:

- Traefik: ```make logs-webserver```
- Frontend: ```make logs-frontend```
- Backend: ```make logs-backend```

## Automating Deployment with GitHub Actions

{term}`cookieplone` includes a GitHub Actions Workflow, located at {file}`.github/workflows/manual_deploy.yml`, enabling deployment directly from the GitHub UI.

### Repository Configuration

#### Creating a New Environment

1. Log in to [GitHub](https://github.com/).
2. Navigate to the project repository.
3. Click `Settings`.
4. Select `Environments`, then `New environment`.
5. Name it after your public URL and configure the environment.

#### Adding Environment Secrets

Add secrets in the `Secrets` section of your environment. Refer to the table below:

| Secret Name | Secret Value | Description |
|-------------|--------------|-------------|
| DEPLOY_HOST | Your hostname or IP | The Docker Swarm manager's address. |
| DEPLOY_PORT | 22 | The SSHD port. |
| DEPLOY_USER | Your username | A user with Docker command permissions. |
| DEPLOY_SSH  | Content of `devops/etc/keys/plone_prod_deploy_rsa` | The private SSH key for connection. |
| ENV_FILE    | Content of {file}`devops/.env_file_gha` | File containing environment variables for the stack file. |

#### Adding Repository Variables

Navigate to `Settings` > `Secrets and Variables` > `Actions`. Under `Variables`, add the repository variable:

| Name     | Value |
|----------|-------|
| LIVE_ENV | The name of the earlier created environment |

This variable is referenced in {file}`.github/workflows/manual_deploy.yml`.

## Initiating Manual Deployment

Ensure both Backend and Frontend tests are successful and images for both servers are available.

1. Go to the project's repository on GitHub.
2. Click the `Actions` tab.
3. Find **Manual Deployment...** and click `Run workflow`.
4. Select `Branch: main` under **Use workflow from**.
5. Press `Run workflow`.

The workflow connects to **DEPLOY_HOST** using **DEPLOY_USER** and **DEPLOY_SSH** key, initiates a new deployment using the specified stack, and provides a detailed deployment report.

## Accessing the Site

Your site should now be accessible via the defined public URL.

Note: Ensure to replace placeholders like `<url>` with actual values as per your project's specifics. Also, ensure that the paths to files and directories are correct and exist in your project structure.
