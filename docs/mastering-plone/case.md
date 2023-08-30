---
myst:
  html_meta:
    "description": "Our training story"
    "property=og:description": "Our training story"
    "property=og:title": "The Case Study"
    "keywords": ""
---

(case-label)=

# The Case Study

(case-background-label)=

## Background

For this training we will build a website for a fictional Plone conference on Mars.
By 2050 human civilisation has reached the stars and each year the conference is held on a different planet.

The conference website we want to create should be reusable in the following years, so some things should be configurable.

(case-requirements-label)=

## Requirements

Here are some requirements that we want to meet when the site is done:

- As a visitor I want to find current information on the conference.
- As a visitor I want to find information about talks, trainings and keynotes.
- As a speaker I want to be able to submit talks.
- As a speaker I want to see and edit my submitted talks.
- As an organizer I want to see a list of all proposed talks.
- As an organizer I want to display the sponsors of the conference.
- As a jury member I want to vote on talk submission.
- As an organizer I want to decide which talks to accept and publish on the site, and which not.

Note that requirements connect roles with capabilities.
This is important because we'll want to limit the capabilities to those to whom we assign particular roles.

## Changing requirements

If you have ever organized a conference, you will find that this story is pretty rough.
Like in many real projects new requirements will come up during the development of the project.

Here are some specific feature requirements that will come up:

- Talks should be assignable to rooms
- Available values for audience, type of talk and rooms should be changable by a site administrator
- Talks should have a time and date to display them in a calendar
- We want a calendar view that shows the talks in a time table with rooms as columns
- Talks should be able to have multiple speakers (e.g. for panel discussions)
- We want to be able to easily submit lightning talks

We will see how you can adapt and extend the project to meet these changing requirements.

## Tasks

During the course of the training you will solve the following tasks.

- Installation of backend and frontend
- Create users and organize them
- Configure some basic settings of the website
- Create content with info about the conference using the default features
- Create a Plone add-on to hold our own python code in a backend add-on
- Create a content type 'talk' to store all the data required for a talk
- Create a view to display a talk in a nice way
- Create a Volto block variation that shows a list of talks to allow an easy overview
- Create a new field to mark arbitrary content as 'featured'
- Display this featured content on a dynamic frontpage
- Add date and time to talks to assign them in a schedule
- Display date and time on talks
- Allow potential speakers to self-register and then create and submit talks
- Store the data on the speaker in a custom content type
- Create a relation from speaker to talk upon creation of a talk
- Allow multiple speakers for one talk
- Create a sponsor content type to manage sponsors
- Store non-visible information about the sponsor in the sponsor-type
- Display sponsors on all pages sorted by level
- Allow some settings to be configurable by an admin in a control panel
- Create a separate add-on to allow voting on talks
- Create a React component for voting and connect it to the backend with a custom restapi-endpoint
