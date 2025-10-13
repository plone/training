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

You can find this stack at {file}`devops/stacks/ploneconf2025-<your-github-username>.tangrama.com.br.yml`. It's modular, allowing easy integration of additional services like {term}`Varnish`, `Solr`, or `ElasticSearch`.

```{seealso}
[Traefik Proxy with HTTPS](https://dockerswarm.rocks/traefik/)
```

## Building Docker Images

Ensure you build the Docker images for the Frontend and Backend servers before deployment.
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

## Manual Deployment with Ansible

Utilize the {file}`Makefile` at {file}`devops/Makefile` for manual deployment.

### Deploying the Stack

Execute the following command from your project's {file}`devops/ansible` directory to deploy the stack defined in {file}`devops/stacks/ploneconf2025-<your-github-username>.tangrama.com.br.yml` to the remote server.

```shell
uv run ansible-playbook playbooks/deploy.yml --tags project
```

### Verifying Stack Status

To check the status of all services in your stack, access the remote server:

```shell
ssh root@ploneconf2025-<your-github-username>.tangrama.com.br
```

And then run the command:

```shell
docker stack ps ploneconf2025-<your-github-username>-tangrama-com-br
```

### Creating Plone Site

On the initial deployment, the frontend containers might be unhealthy due to the unconfigured Plone site on the backend. Create a new site with:

```shell
docker exec $(docker ps -qf 'name=_backend'|head -n1) ./docker-entrypoint.sh create-site
```

### Monitoring Logs

Monitor the logs of each service with these commands:

-   Traefik: `docker service logs traefik_traefik --follow`
-   Frontend: `docker service logs <stack-name>_frontend --follow`
-   Backend: `ocker service logs <stack-name>_backend --follow`
-   Database: `ocker service logs <stack-name>_db --follow`

## Automating Deployment with GitHub Actions

{term}`cookieplone` includes a GitHub Actions Workflow, located at {file}`.github/workflows/manual_deploy.yml`, enabling deployment directly from the GitHub UI.

### Repository Configuration

#### Creating a New Environment

```{important}
If you can't see the {guilabel}`Environment` option on the left in the {guilabel}`Settings` of your GitHub repository, you may have a private repository in a free account.
You must either have a public repository or a [GitHub Team plan](https://github.com/pricing#compare-features) or a [GitHub Pro plan](https://docs.github.com/en/get-started/learning-about-github/githubs-plans) for a private repository.
If you use a free additional organization under control of a paid GitHub account, the {guilabel}`Environment` will also not be visible.
```

1. Log in to [GitHub](https://github.com/).
2. Navigate to the project repository.
3. Click `Settings`.
4. Select `Environments`, then `New environment`.
5. Name it after the public URL of the deployment server and configure the environment.

```{seealso}
In the generated project's file {file}`devops/README-GHA.md`, you can find the exact values to use for your project when completing the {guilabel}`New environment` form.
```

#### Adding Environment Secrets

Add secrets in the `Secrets` section of your environment. Refer to the table below:

| Secret Name | Secret Value                                             | Description                                               |
|-------------|----------------------------------------------------------|-----------------------------------------------------------|
| DEPLOY_HOST | Your hostname or IP                                      | The Docker Swarm manager's address.                       |
| DEPLOY_PORT | 22                                                       | The SSHD port.                                            |
| DEPLOY_USER | Your username                                            | A user with Docker command permissions.                   |
| DEPLOY_SSH  | Content of {file}`devops/etc/keys/plone_prod_deploy_rsa` | The private SSH key for connection.                       |
| ENV_FILE    | Content of {file}`devops/.env_file_gha`                  | File containing environment variables for the stack file. |


## Initiating Manual Deployment

Ensure both Backend and Frontend tests are successful and images for both servers are available.

1. Go to the project's repository on GitHub.
2. Click the {guilabel}`Actions` tab.
3. Find {guilabel}`Manual Deployment...` and click {guilabel}`Run workflow`.
4. Select {guilabel}`Branch: main` under {guilabel}`Use workflow from`.
5. Press {guilabel}`Run workflow`.

The workflow connects to `DEPLOY_HOST` using `DEPLOY_USER` and `DEPLOY_SSH` key, initiates a new deployment using the specified stack, and provides a detailed deployment report.

## Accessing the Site

Your site should now be accessible via the defined public URL.

Note: Ensure you replace placeholders, such as `<url>`, with actual values per your project's specifics. Also, ensure that the paths to files and directories are correct and exist in your project structure.
