---
myst:
  html_meta:
    "description": "Why this training shows an end result: the challenges of deploying Plone to a multi-node cluster in real life."
    "property=og:description": "Why this training shows an end result: the challenges of deploying Plone to a multi-node cluster in real life."
    "property=og:title": "Deploy challenges in real life"
    "keywords": "Plone, Deployment, Docker Swarm, Traefik, GitLab, Training"
---

(deploy-challenges-label)=

# Deploy challenges in real life

This is a small chapter to give a bit more background on the 'why show the end result' in this training with 2 repos and deviate from the deployment training at <https://2025.training.plone.org>. It should also help the reader to maybe go to that training instead.

The 2025 training is still better suited to show a clean 'lab setup' for your first deployment to a containerised hosting setup. We could update the training to offer a separate 'get your own VM' instead of using a trainer provided `tangrama.com.br` setup.  One of the realities of mid 2026 is that a VM with 8 GB RAM costs more than 40 euro/month, compared to 7 euro/month in 2025.

A first source of extra challenges comes from going to a multi-node swarm cluster, where the backend/frontend runs on separate worker nodes, and we should place the postgresql container on a fixed 'storage' node.  These are essential multi-node containerisation skills to teach.

A second source of complexity comes from deploying more than one project to a cluster. The dynamic Traefik configuration using labels that get picked up when a service deploys, provides endless sources of collision fun, when you forget to point your frontend's `RAZZLE_INTERNAL_API_PATH` at `stackname_backend` instead of `backend`. This is also valid for the Traefik label namespaces where all routes, middlewares and services need to be unique in the cluster.  We accomplish this through a `STACK_PREFIX` in a fully parameterised Docker Swarm stack template.

Then GitLab has its own deviations from easier or more common GitHub configurations. This version of the training has been tested a few times now. Letting students stumble over these challenges during the training, rather than later when they try to extend the setup, is very valuable.
