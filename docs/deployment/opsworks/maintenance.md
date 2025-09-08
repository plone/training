---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Maintenance

## Backups

The recipes automatically setup weekly ZODB packing and log rotation.
I like to use Amazon's EBS snapshot feature for backups.

The EBS Snapshotting layer provides that functionality automatically.

It requires you to use the AWS IAM Console to create a new user with the following permissions:

```
ec2:CreateSnapshot
ec2:CreateTags
ec2:DeleteSnapshot
ec2:DescribeInstances
ec2:DescribeSnapshots
```

You will need to note the API credentials for this new user and enter them into the Stack

Custom JSON as follows:

```json
{
 "ebs_snapshots" : {
     "aws_key" : "***** AWS KEY FOR SNAPSHOTTING (IAM USER) *****",
     "aws_secret" : "***** AWS SECRET FOR SNAPSHOTTING (IAM USER) *****"}
}
```

The EBS Snapshotting Layer should be assigned to any production instance which has EBS volumes on which you are storing data.
Generally speaking, any production instance with the Zeoserver, Shared Blob, or Solr Layers assigned should
also have the EBS Snapshotting Layer assigned.

This Layer will setup automatic nightly snapshots of all mounted EBS volumes.
By default it retains up to 15 snapshots, but that can be configured setting
`ebs_snapshots["keep"]` to the number you wish to retain in the Stack Custom
JSON.

## Updates

Ubuntu security and OS package updates can be automated by adding the following Custom JSON configuration:

```json
{
 "apt": {
     "unattended_upgrades": {
       "package_blacklist": [],
       "enable": true,
       "mail": "youremail@here",
       "auto_fix_interrupted_dpkg": true
     }
 }
}
```

## Monitoring

{term}`AWS` provides various monitoring and alerting features, but most alerting features need to be manually configured on a per EC2 instance basis.

That's not so convenient for a stack of instances which may grow, shrink or change over time.

For that reason I like to use New Relic for server monitoring.

There is built-in integration in the recipes, which includes detailed performance server and client performance monitoring for Plone,
as well as plugins for Nginx, Varnish and HAProxy services and standard CPU, Disk space and RAM server metrics.

There's also a recipe provided to integrate the [Papertrail](https://www.papertrail.com) log tracing and searching service.

To help you live the dream of never having to SSH into your servers.

## Sending Mail

It's possible, and not difficult to install and configure a mailer using a chef postfix recipe and some more Custom JSON.

I do not recommend doing so.

Cloud Servers generally, and EC2 specifically tend to land on SPAM blacklists, ensuring your outgoing mail is not blackholed generally requires
some special care and requests to Amazon to setup reverse DNS and whitelist any outgoing mail servers.

Instead I recommend using a hosted mail delivery service like Amazon SES or perhaps GMail.

## SSH Access

Ideally, you never have to login to your cloud server, but things go wrong and you might have to eventually, even if only out of curiosity.

By default OpsWorks does not assign an SSH key to new instances, but you can set one if desired at either the instance or the Stack level.

Better yet, OpsWorks allows more granular access control in combination with IAM.

If you create a user via the AWS IAM console (no permissions need be assigned, and no credentials added or recorded for SSH access),
you can then import that user into the OpsWorks Users control panel.

In OpsWorks users can be given access to specific stacks, allowing them to view, deploy or manage them, as well as granting them SSH
and/or {command}`sudo` access to Stack Instances using a public key that can be added through the web interface.

Once you've imported an IAM user into OpsWorks and granted it SSH access with a public key,
that user should be able to log in to all instances in the stack. [^id2]

```{note}
A note on OS permissions: all application related files live under
`/srv/www` and are generally owned by the `deploy` user with fairly
restricted permissions. Any user SSH'ing in will probably need to {command}`sudo` to the
`deploy` user to see or do much of interest.
```

[^id2]: You should *never* manually modify any configuration on a cloud configured server, except for purposes of troubleshooting. Any changes you make to the server should be made via the Stack configuration (i.e. the Custom JSON and the Recipes assigned to Layers).
