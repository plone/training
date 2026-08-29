---
myst:
  html_meta:
    "description": "How to deploy a Plone project using make, GitHub Actions, or Gitlab CI"
    "property=og:description": "How to deploy a Plone project using make, GitHub Actions, or Gitlab CI"
    "property=og:title": "How to deploy a Plone project using make, GitHub Actions, or Gitlab CI"
    "keywords": "deploy, Plone, Makefile, GitHub Actions, GitLab CI"
---

# Deploy the project

## Project stack

This guide outlines the steps to deploy the project using a Docker stack comprising:

Traefik
:   A router and TLS termination tool, integrated with [Let's Encrypt](https://letsencrypt.org/) for complimentary secure certificates.

Plone frontend using Volto
:   A service based on React for the frontend.

Plone backend
:   The API service.

Postgres 14 database
:   Handles data persistence.

You can find this stack at {file}`devops/stacks/ploneconf2025-<your-github-username>.tangrama.com.br.yml`. It's modular, allowing integration of additional services, such as {term}`Varnish`, `Solr`, or `ElasticSearch`.

```{seealso}
[Traefik Proxy with HTTPS](https://dockerswarm.rocks/traefik/)
```

## Build Docker images

Ensure you build the Docker images for the frontend and backend servers before deployment.
GitHub Actions, configured in {file}`.github/workflows/main.yml`, facilitate this process.

````{important}
Before deploying, run the following commands from your project's root directory to format the code and run tests.

```shell
make check
make test
```

The output from `make test` may vary according to changes in code.
The following console output indicates that no tests were run, and prompts you to choose an action.

```console
No tests found related to files changed since last commit.
Press `a` to run all tests, or run Jest with `--watchAll`.

Watch Usage
 › Press a to run all tests.
 › Press f to run only failed tests.
 › Press p to filter by a filename regex pattern.
 › Press t to filter by a test name regex pattern.
 › Press q to quit watch mode.
 › Press Enter to trigger a test run.
```

After these commands succeed, commit all code changes, push to GitHub, and ensure all GitHub Actions successfully complete their runs.
````

## Manual deployment with Ansible

Utilize the {file}`Makefile` at {file}`devops/Makefile` for manual deployment.

### Deploy the stack

Execute the following command from your project's {file}`devops/ansible` directory to deploy the stack defined in {file}`devops/stacks/ploneconf2025-<your-github-username>.tangrama.com.br.yml` to the remote server.

```shell
uv run ansible-playbook playbooks/deploy.yml --tags project
```

### Verify stack status

To check the status of all services in your stack, access the remote server:

```shell
ssh root@ploneconf2025-<your-github-username>.tangrama.com.br
```

And then run the command:

```shell
docker stack ps ploneconf2025-<your-github-username>-tangrama-com-br
```

### Create Plone site

On the initial deployment, the frontend containers might be unhealthy due to the unconfigured Plone site on the backend. Create a new site with:

```shell
docker exec $(docker ps -qf 'name=_backend'|head -n1) ./docker-entrypoint.sh create-site
```

### Monitor logs

Monitor the logs of each service with these commands:

```{code-block} shell
:caption: Traefik

docker service logs traefik_traefik --follow`
```

```{code-block} shell
:caption: frontend 

docker service logs <stack-name>_frontend --follow`
```

```{code-block} shell
:caption: backend

docker service logs <stack-name>_backend --follow`
```

```{code-block} shell
:caption: database

docker service logs <stack-name>_db --follow`
```

## Automate deployment with GitHub Actions

This section describes how to configure your GitHub repository to automatically deploy your project.

{term}`Cookieplone` includes a GitHub Actions workflow, located at {file}`.github/workflows/manual_deploy.yml`, enabling deployment directly from the GitHub UI.

First, create a new environment.

1.  Log in to [GitHub](https://github.com/).
1.  Navigate to the project repository.
1.  Click `Settings`.
1.  Select `Environments`, then `New environment`.

    ```{important}
    If you can't see the {guilabel}`Environment` option on the left in the {guilabel}`Settings` of your GitHub repository, you may have a private repository in a free account.
    You must either have a public repository or a [GitHub Team plan](https://github.com/pricing#compare-features) or a [GitHub Pro plan](https://docs.github.com/en/get-started/learning-about-github/githubs-plans) for a private repository.
    If you use a free additional organization under control of a paid GitHub account, the {guilabel}`Environment` will also not be visible.
    ```

1.  Name the new environment after the public URL of the deployment server and configure the environment secrets.
1.  Add each secret in the `Secrets` section of your environment, using the values in the generated project's file {file}`devops/README-GHA.md`.

    | Secret Name | Secret Value | Description |
    |---|---|---|
    | `DEPLOY_HOST` | Your hostname or IP | The Docker Swarm manager's address. |
    | `DEPLOY_PORT` | `22` | The SSHD port. |
    | `DEPLOY_USER` | `plone` by default, unless overridden. See {file}`devops/README-GHA.md` for actual value. | A user with Docker command permissions. |
    | `DEPLOY_SSH` | Content of {file}`devops/etc/keys/plone_prod_deploy_ed25519` | The private SSH key for the connection. |
    | `ENV_FILE` | Content of {file}`devops/.env_gha` | File containing environment variables for the stack file. |


## Initiate manual deployment

Ensure both backend and frontend tests are successful, and images for both servers are available.

1.  Go to the project's repository on GitHub.
1.  Click the {guilabel}`Actions` tab.
1.  Find {guilabel}`Manual Deployment of ploneconf2025-<your-github-username>.tangrama.com.br.yml` and click {guilabel}`Run workflow`.
1.  For {guilabel}`Use workflow from`, select {guilabel}`Branch: main`.
1.  Click {guilabel}`Run workflow`.

The workflow connects to `DEPLOY_HOST` using `DEPLOY_USER` and `DEPLOY_SSH` key, initiates a new deployment using the specified stack, and provides a detailed deployment report.

## Access the site

Your site should now be accessible via the defined public URL.

```{note}
Ensure you replace placeholders, such as `<url>`, with actual values per your project's specifics.
Also, ensure that the paths to files and directories are correct and exist in your project structure.
```
