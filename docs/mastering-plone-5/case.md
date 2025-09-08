---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-case-label)=

# The Case Study

For this training we will build a website for a fictional Plone conference.

(plone5-case-background-label)=

## Background

The Plone conference takes place every year and all Plone developers at least try to go there.

(plone5-case-requirements-label)=

## Requirements

Here are some requirements that we want to meet when the site is done:

- As a visitor I want to find current information on the conference.
- As a visitor I want to register for the conference.
- As a visitor I want to see the talks and sort them by my preferences.
- As a speaker I want to be able to submit talks.
- As a speaker I want to see and edit my submitted talks.
- As an organizer I want to see a list of all proposed talks.
- As an organizer I want to have an overview about how many people registered.
- As a jury member I want to vote on talks.
- As a jury member I want to decide which talks to accept, and which not.

Note that all of our requirements connect roles with capabilities.
This is important because we'll want to limit the capabilities to those to whom we assign particular roles.
