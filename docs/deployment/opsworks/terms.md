---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Deployment Terminology

It's probably a good idea to be familar with a few core Chef concepts, though
digging deeply into Chef is definitely not something I encourage Python
developers to do.

> - `Resource`: The basic building block in Chef (and also Ansible); defines files, directories, installed packaes, services, etc.
> - `Recipe`: A collection of resource definitions with some logic to connect them. These can be very simple or extraordinarily complex; A recipe can depend on other recipes. These basically play the same role as `Tasks` in Ansible.
> - `Cookbook`: A collection of recipes required to setup a service or similar. These play a similar role to `Roles` in Ansible. These generally can be found in the Chef Supermarket like Roles from the Ansible Galaxy.
> - `Berkshelf`: A single file configuration defining the set of cookbooks needed for a deployment. It consists of a `Berksfile` which defines locations and versions of all cookbooks required for a deployment.
> - `Attributes`: The deployment specific configuration for the cookbook and recipes. This is essentially a collection of JSON like primitives, similar to YAML group/host `Vars`.

## Opsworks

Amazon OpsWorks takes this basic configuration framework and provides its own set of concepts, to implement cluster orchestration.

When using OpsWorks, you will be making use built-in OpsWorks Chef Cookbooks provided by Amazon.
These built-in Cookbooks provide a number of Recipes for configuring and deploying many types of applications using
TTW (Through-The-Web) configuration from the OpsWorks control panel.

These include [Node.js](https://nodejs.org/en/), [Rails](https://rubyonrails.org/), [PHP](https://www.php.net/) , and Java applications, but not [Python](https://www.python.org/) [^id3].

I've created a couple supplemental Cookbooks that extend the existing OpsWorks
deployment recipes to support Python and Plone along with other supporting
services that are useful when making production deployments of Plone.

OpsWorks has its own vocabulary of concepts related to deploying and orchestrating clusters of servers.

The building blocks of OpsWorks are:

- `Stack`: The fundamental container for your configuration, this lives in a particular EC2 region and contains all the configuration for your cluster.
  Typically you would have a separate production stack and development stack.
  Creating this is the first step in the process of defining your cluster.
  Stacks can be cloned to replicate configuration across regions.
- `Layers`: A Layer defines a discrete set of functionality that may be provided by a server Instance.
  For example, a Plone cluster may have a frontend Layer running an Nginx web server, Varnish proxy cache and HAProxy load balancer [^id4] ,
  an Application Layer for your ZEO client instances, an Application Layer for your ZEO server, and a maintenance layer to manage database backups and packs.
  Layers define what recipes will be run on an instance, and which OS packages it requires,
  along with any Amazon resources and permissions are required to provide a service (e.g. static IP addresses, additional EBS storage volumes).
- `Instances`: An OpsWorks Instance is similar to an EC2 instance, it has a type (e.g. from micro to xlarge), an OS and an Availability Zone,
  but it is an abstraction. It becomes an actual EC2 instance once it's been started, but before that it's simply a metadata about a desired server.
  Instances are assigned to one or more Layers, and come in three varieties, 24/7, time-based and load-based.
- `Apps`: An App points to a code repository (in our case a buildout) which you want to deploy to a specific Application Layer. Typically you would have an App for your Plone instances and another for your Zeoserver. Both these Apps would typically point to the same buildout repository. You might also create an App to configure a Plone specific Solr server or to run a additional applications within the cluster.
- `Resources`: A set of Amazon EC2 resources that will be used by the stack by being attached/assigned to Instances when they are started.
  These include Elastic IP addresses, EBS storage volumes and RDS databases (useful you are running Relstorage).

A Stack can be configured with a single Instance running all the Layers, or multiple Instances each running different Layers.
You might, for example, have a production stack with five Instances running the Plone ZEO client Application Layer,
a single instance running the ZEO server Application Layer,
and two Instances running the front end proxy/loadbalancer Layer (with an Elastic Load Balancer in front of those).

You might also have a staging stack with all the same Layers applied to a single modest server.
Other than the Instance definitions (and perhaps the App repository branch), these Stacks would be essentially identical.

[^id3]: Boo!

[^id4]: Though you could separate each of these frontend services into their own layers if you wanted to,
    we combine them by default under a customized HAProxy layer which already provides a nice UI for a few HAProxy features.

## Instance Lifecycle

Each OpsWorks Instance goes through a few phases during its lifecycle:

> - `setup`
> - `deploy`
> - `configure`
> - `undeploy`
> - `shutdown`

Each of these lifecycle phases runs recipes assigned to that phase in the assigned Layers.
When these recipes are run, the Stack configuration is passed to the server.

This configuration includes complete information about the state of the entire Stack and all of its running Instances.

When an Instance starts, it first goes through a `setup` phase: installing all package dependencies
for all assigned Layers and running all the recipes assigned to the `setup` phase of those Layers.

Once the `setup` phase is complete, a `deploy` phase is automatically started.
Running all the recipes assigned to the `deploy` phase of any assigned Layers.

Subsequently, you may manually run a `deploy` for a specific Application on
any or all of the instances to update the application code and reconfigure services.

The `shutdown` phase is run automatically before an instance is stopped.

The `undeploy` phase is rarely used. It is triggered when an application is manually removed from an instance.

Whenever an Instance is started or stopped and it's `setup` or `shutdown` phase has completed a `configure` phase is initiated on all running
instances.

As with all recipe runs, the `configure` phase recipes are passed data about all the currently running Instances and their Layers so that they
can automatically reconfigure themselves based on the updated state of the Stack.

For example, a load balancer may need to automatically add or remove Plone ZEO clients from it's list of active backends,
a ZEO client may need to change its ZEO server or its Relstorage Memcache if configuration for those services have changed.

This `configure` phase, during which the current cluster state is automatically shared with all the instances, is where the orchestration magic
happens.
