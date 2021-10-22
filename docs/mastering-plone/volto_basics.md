---
html_meta:
  "description": "What's new in Plone 6 React frontend? Should I adapt to it now?"
  "property=og:description": "What's new in Plone 6 React frontend? Should I adapt to it now?"
  "property=og:title": "Plone 6 Basics"
  "keywords": "overview, Plone6"
---

(volto-basics-label)=

# Plone 6 Basics

Plone is an Enterprise CMS, both mature and vivid.
With the current version 6, the success of over 20 years is continuing.
It brings some changes to former Plone versions.
The following is meant to give an orientation, which changes these are and how they affect your upcoming projects.

**Volto** is a React based frontend for Plone.
Beside the **Plone Classic** frontend and other frontends, it is the default frontend and editor from Plone 6 on.

The intention to build a new frontend was to achieve a new experience for editing the web.

Some facts about Plone 6:

First of all, it is important to note that,

**Volto is the default frontend for Plone 6 but Plone can still serve as backend and frontend.**

- All data is stored in Plone.
  Volto comes in to display and edit the content.
- Volto is built in [ReactJS](https://reactjs.org), a modern Javascript Framework.
- Volto uses [plone.restapi](https://plonerestapi.readthedocs.io/en/latest/) to communicate with the Plone backend.

Some details

- Volto is installed separately from the Plone backend.
  See chapter {ref}`installation-Volto-label` for instructions.
- Volto runs in a different process than the Plone backend.
  By default Volto runs on port 3000. If you start Volto with `yarn start` you can see the frontend on <http://localhost:3000>.
  The Plone backend runs by default on <http://localhost:8080>
- You create a new Plone instance in an already set up Zope environment via the backend.
  This is by now not possible in Volto.
- Volto takes advantage of [Semantic UI React components](https://react.semantic-ui.com/) to compose most of the views.
  For example the component [Image](https://react.semantic-ui.com/elements/image/) is used to render images.
- The Volto default theme is based on Semantic UI theme and is called [Pastanaga](https://www.youtube.com/watch?v=wW9mTl1Tavc&t=133s).
- Same as Plone Classic, Volto is highly extendable with add-ons for further features.
- Existing Volto components are customizable with a technology similar to `z3c.jbot` called {ref}`volto-overrides-componentshadowing-label`.
- Volto provides server side rendering (SSR), important for SEO-purposes.
- Volto aims to provide 100% of the features of the current Plone backend.
  Not all features of Plone are implemented in Volto yet.
- Volto provides additional functionality that Plone does not have.
- For example Volto features the Pastanaga Editor, allowing you to visually compose a page using blocks.
  This feature is enabled for content types that have the dexterity behavior `volto.blocks` enabled.
- Using the Pastanaga Editor, the content you add in blocks and the arrangement of blocks is stored as JSON in the schema fields `blocks` and `blocks_layout` provided by the dexterity behavior `volto.blocks`.
  Additionally you can edit all fields of the content type schema in a sidebar.
- If you do not use the behavior `volto.blocks`, the fields from a content-type schema are edited and stored exactly like previously in Plone.


**For theming your Plone 6 website you choose either Volto or the Plone Classic frontend.**

Here are some pointer that may help you decide:

- The new Plone 6 frontend is recommended for new projects. 
- There are a growing ecosystem of add-ons for the React frontend.
  Be aware that a Plone Classic add-on does have value for your project, as long as its not a theming component or anything that concerns the UI.
  That could be for example a backend add-on that implements the logic and storage of bookmarks. 
  The UI needs to be implemented in React, be it an open source add-on or your custom add-on.
  Both, frontend and backend, communicate via REST API.
- Existing projects that are updated to Plone 6 can decide which frontend to use.
  If a lot of customizations were done and you don't want to reimplement a lot of custom templates and features in Volto, it is a good idea to use Plone Classic.
- Most existing add-ons for Plone will have to be adapted to Volto if they touch the UI (e.g. templates for content types, control panels or viewlets).
- For a selection of awesome Volto add-ons see <https://github.com/collective/awesome-volto/>
