---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(case-label)=

# The Case Study

(case-background-label)=

## Background

For this training we will build a website for a fictional Plone conference on Mars.

By 2050 human civilisation has reached the stars and each year the conference is held on a different planet.

The conference-webseite we want to create should be reusable in the following years so some things should be configurable.

(case-requirements-label)=

## Requirements

Here are some requirements that we want to meet when the site is done:

- As a visitor I want to find current information on the conference.
- As a visitor I want to find information about talks, trainings and keynotes.
- As a speaker I want to be able to submit talks.
- As a speaker I want to see and edit my submitted talks.
- As an organizer I want to see a list of all proposed talks.
- As an organizer I want to display the sponsors of the conference.
- As a jury member I want to vote on talks.
- As a jury member I want to decide which talks to accept, and which not.

Note that requirements connect roles with capabilities.
This is important because we'll want to limit the capabilities to those to whom we assign particular roles.

## Changing requirements

If you have ever organized a conference you will find that this story is pretty rough.
Like in many real projects new requirements will come up during the development of the project.

Here are some specific features-requirements that will come up:

- Talks should be assignable to rooms
- Available values for audience, type of talk and rooms be managed by a admin
- Talks should have a time and date to display them in a calendar
- We want a calendar-view that shows the talks in a timetable with rooms as columns
- Talks should be able to have multiple speakers (e.g. for panel discussions)
- We want to be able to easily submit Lightning Talks

We will see how you can adapt and extend the project to meet these changing requirements.

## Tasks

During the course of the training you will solve the following tasks.

- Installation of backend and frontend
- Create users and organize them
- Configure some basic settings of the website
- Create content with info about the conference using the default features
- Create a Plone add-on to hold our own python code
- Create a contenttype 'talk' to store all the data required for a talk
- Create a view to display talks in a nice way
- Create a view that shows a list of talks to allow a easy overview
- Create a new field to mark arbitrary content as 'featured'
- Display this featured content on a dynamic frontpage
- Add date and time to talks to assign them in a schedule
- Display date and time on talks
- Allow potential speakers to self-register and then create and submit talks
- Store the data on the speaker in a custom content-type
- Create a relation from speaker to talk upon creation of a talk
- Allow multiple speakers for one talk
- Create a sponsor contenttype to manage sponsors
- Store non-visible information about the sponsor in the sponsor-type
- Display sponsors on all pages sorted by level
- Allow some avilable to be configurable by a admin in a controlpanel
- Create a calendar view to display talks
- Turn the calendar view in a reuseable block to include it on the frontpage
- Add a separate add-on to allow voting on talks
- Create a react-component for voting and connect it to the backend with a custom restapi-endpoint
- Create a simple mobile app that allows the easy submission of lightning talks (a type of talk)

(intro-what-happens-label)=

## What will we do?

Here are the technologies and tools we will use during the training:

- For the beginning training:

  > - [Virtualbox](https://www.virtualbox.org/)
  > - [Vagrant](https://www.vagrantup.com/)
  > - [Ubuntu linux](https://ubuntu.com/)
  > - [Buildout](https://www.buildout.org/en/latest/)
  > - XML
  > - Python 3
  > - React

- For the advanced chapters:

  > - [Git](https://git-scm.com/)
  > - [GitHub](https://github.com)
  > - [Resources to learn Git](https://docs.github.com/en/get-started/quickstart/set-up-git)
  > - TAL
  > - METAL
  > - ZCML
  > - [Python](https://www.python.org)
  > - Dexterity
  > - [GenericSetup](https://docs.plone.org/develop/addons/components/genericsetup.html)
  > - Viewlets

(intro-what-wont-happen-label)=

## What will we not do?

We will not cover the following topics:

- [Portlets](https://docs.plone.org/develop/plone/functionality/portlets.html)
- [z3c.forms](https://docs.plone.org/develop/plone/forms/z3c.form.html)
- [Theming](https://docs.plone.org/adapt-and-extend/theming/index.html)
- [Multilingual content and Internationalization](https://docs.plone.org/develop/plone/i18n/index.html)
- [Deployment, Hosting and Caching](https://docs.plone.org/manage/deploying/index.html)

Other topics are only covered lightly:

- [Zope Component Architecture](https://docs.plone.org/develop/addons/components/index.html)
- [ZODB](https://docs.plone.org/develop/plone/persistency/index.html)
- [Security](https://docs.plone.org/develop/plone/security/index.html)
- [Permissions](https://docs.plone.org/develop/plone/security/permissions.html)
- [Performance and tuning](https://docs.plone.org/manage/deploying/performance/index.html)
