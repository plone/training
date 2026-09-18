---
myst:
  html_meta:
    "description": "How to put your Plone website online"
    "property=og:description": "How to put your Plone website online"
    "property=og:title": "Deploy in production"
    "keywords": "Plone, Volto, deploy, release, production, open source"
---

# Deploy in production

We finally have some working code!
But the conference website we've built isn't very useful if no one else can access it.

Production deployments are not the main focus of this training, but let's take a brief look at what can happen next.

## Release the add-on

Production deployments should ideally use a specific released version of add-ons.
This avoids accidentally deploying changes when development of the add-on continues.

In this case, we should release the add-on `mastering-plone-votable-add-on` that we've been developing.

The add-on template from Cookieplone comes with tools to release the backend Python package on {term}`PyPI` and the frontend Volto package on {term}`npm`.

It uses _RepoPlone_ which has a single command (`repoplone release`) to release both packages at once.
See https://github.com/plone/repoplone for details.

```{warning}
Please don't actually make a release of `mastering-plone-votable-add-on`.
Once the name has been claimed by one person, other participants in the class would not be able to make a release with the same name.
You can practice with a different add-on.
```

Then update the project's {file}`pyproject.toml` and {file}`mrs.developer.json` to use the released packages instead of the still-being-developed local packages that were used in {doc}`voting-story/index`.

## Deploy using containers

The Cookieplone project template comes with tools to build your project as container images that can be run using Docker or container-based hosting providers.

You may have already noticed the start of this deployment pipeline.
Whenever you push a change to the project repository in GitHub, an automated workflow builds new container images.

The remaining part is to actually run those images somewhere.
Another training, {doc}`../plone-deployment/index`, shows how to do this on any Linux-based virtual server.
