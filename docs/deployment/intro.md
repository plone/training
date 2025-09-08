---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Introduction

The subject of this training is the deployment of Plone for production purposes.

We will, in particular, be focusing on automating deployment using tools which can target
a fresh Linux server and create on it an efficient, robust server.

That target server may be a cloud server newly created on {term}`AWS`, {term}`Linode` or {term}`DigitalOcean`.

Or, it may be a virtual machine created for testing on your own desk or laptop.

Our goal is that these deployments be *repeatable*.
If we run the automated deployment multiple times against multiple cloud servers, we should get the same results.

If we run the automated deployment against a virtual machine on our laptop, we should be able to test it as if it was a matching cloud server.

The tools we use for this purpose reflect the opinions of the Plone Installer Team.
*We are opinionated*.

With a great many years of experience administering servers and Plone, we feel we have a right to our opinions.
But, most importantly, we know we have to make choices and support those choices.

The tools we use may not be the ones you would choose.

They may not be the ones we would choose this month if we were starting over.

But, they are tools widely used in the Plone community.
They are well-understood, and you should get few "I've never heard of that" complaints if you ask questions of the Plone community.

## Our Choices

Linux

> BSD is great.
> macOS is familiar.
> Windows works fine, too.
> But our experience and the majority experience in the Plone community is with Linux for production servers.
> That doesn't mean you have to use Linux for your laptop or desktop; anything that runs Python is likely fine.

Major distributions

> We're supporting two target distribution families: Debian and EL (RedHat/CentOS).
> We're going to try to keep this working on the most recent LTS (Long-Term Support release) or its equivalent.

Platform packages

> We use platform packages whenever possible.
> We want the non-Plone components on your server to be automatically updatable using your platform tools.
> If a platform package is usable, we'll use it even if it isn't the newest, coolest version.

Ansible

> There are all sorts of great tools for automating deployment.
> People we respect have chosen Puppet, Salt/Minion and lots of other tools.
> We chose Ansible because it requires no preinstalled server component, it's written in Python,
> and its configuration language is YAML, which is awfully easy to read.

And ...

> We'll discuss particular parts of the deployment stack in the next section.
