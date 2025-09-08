---
myst:
  html_meta:
    "description": "Volto add-ons development training intro"
    "property=og:description": "Volto add-ons development training"
    "property=og:title": "Volto add-ons development intro"
    "keywords": "Volto"
---

(voltoaddons-intro-label)=

# Introduction

## Who are you?

Tell us about yourselves:

- Name, company, country...
- What is your Plone experience?
- What is your JavaScript experience?
- What is your Volto experience?
- What are your expectations for this hands-on session?

(voltoaddons-intro-what-will-we-do-label)=

## What will we do?

Some technologies and tools we use during the training:

- [React] & JSX
- [Yarn]
- [Volto] and [Plone], of course
- [generator-volto]

This training assumes that you have already taken (either in person at a Plone
Conference or online) the existing React and Volto trainings. If you're
following this training course on your own, you should first go through the
{ref}`voltohandson-label` training.

In a real training the instructor should quickly go through a number of key
concepts of React and Volto development, as a refresher.

## What to expect

At the end of this course you will know how to extend Volto using add-ons, what
are the current capabilities of add-ons, their pros and cons, how to distribute
add-ons and how to deploy them.

### Roadmap

- bootstrap a Volto project using the `@plone/volto` skeleton generator
- bootstrap a Volto add-on from scratch
- develop a simple Volto block
- write an action/reducer pair for network requests
- connect the block to network-fetched async data
- learn how to make React code reusable
- learn how to make blocks extensible

(voltoaddons-intro-documentation-label)=

## The hands-on exercise

The hands-on exercise will feature developing an add-on that provides table
views for data files (CSV). We will be using real-world patterns and
development models based on the experience gained while developing several
websites that use these types of add-ons.

Here's a preview of the block we'll build:

```{image} _static/final-block.png
```

We will be facing different challenges, and we will be solving them, introducing
or refreshing some concepts covered in the previous training classes.
We will cover the proper solution to each challenge, and we will provide an
overview of what to expect when developing for Volto.

## Before you start

You'll need to have a Plone instance with `plone.restapi` integrated. The quickest
way to get a Plone instance running is with Docker:

```shell
docker run -it --rm --name=plone \
  -p 8080:8080 -e SITE=Plone -e ADDONS="plone.volto" \
  -e ZCML="plone.volto.cors" \
  -e PROFILES="plone.volto:default-homepage" \
  plone
```

If you have the whole tool chain setup to develop Plone, you can also clone
and use Volto's development backend setup:

```shell
git clone https://github.com/plone/volto
cd volto
make build-backend
make backend-start
```

[generator-volto]: https://github.com/plone/generator-volto
[plone]: https://plone.org
[react]: https://react.dev/
[volto]: https://github.com/plone/volto
[yarn]: https://yarnpkg.com
