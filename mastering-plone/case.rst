.. _case-label:

The Case Study
==============

For this training we will build a website for a fictional Plone conference.

.. _case-background-label:

Background
----------

The Plone conference takes place every year and all Plone developers at least try to go there.

.. _case-requirements-label:

Requirements
------------

Here are some requirements that we want to meet when the site is done:

* As a visitor I want to find current information on the conference.
* As a visitor I want to find information about talks.
* As a speaker I want to be able to submit talks.
* As a speaker I want to see and edit my submitted talks.
* As an organizer I want to see a list of all proposed talks.
* As a jury member I want to vote on talks.
* As a jury member I want to decide which talks to accept, and which not.
* As a visitor I want to be able to register for the conference.
* As an organizer I want to have an overview about how many people registered.

Note that requirements connect roles with capabilities.
This is important because we'll want to limit the capabilities to those to whom we assign particular roles.

If you have ever organized a conference you will find that this story is pretty rough.
Like in many real projects new requirements will come up during the development of the project.

Here are some specific features-requirements that will come up:

* Talks should be assignable to rooms
* Available values for audience, type of talk and rooms be managed by a admin
* Talks should have a time and date to display them in a calendar
* We want a calendar-view that shows the talks in a timetable with rooms as columns

We see how you can adapt and extend the project to meet these new requirements.
