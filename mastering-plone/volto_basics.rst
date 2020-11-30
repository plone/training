.. _volto_basics-label:

Volto Basics
============

Volto is a React-based frontend for Plone. Beside the classic Plone frontend and other frontends it is the default frontend and editor since Plone 6.

The intention to build a new frontend was to achieve a new experience for editing the web.

Here are some things you should know if you are new to Plone 6 or Volto:

**Volto is optional. Plone will still serve as backend and frontend.**

* All data is stored in Plone, Volto comes in to display and edit the content.
* Volto is built in `ReactJS <https://reactjs.org>`_, a modern Javascript Framework.
* Volto uses `plone.restapi <https://plonerestapi.readthedocs.io/>`_ to communicate with Plone backend.

Details

* Volto is installed separately from Plone backend. See chapter :ref:`instructions-install_frontend-label` for instructions.
* Volto runs in a different process than the Plone-backend. By default Volto runs on port 3000. If you start Volto with ``yarn start`` you can see the frontend on http://localhost:3000. The Plone backend runs by default on http://localhost:8080
* To create a new Plone site in your already setup Zope environment you use the backend, this is by now not possible in Volto.
* Volto takes advantage of `Semantic UI React components <https://react.semantic-ui.com/>`_ to compose most of the views. For example the component `Image <https://react.semantic-ui.com/elements/image/>`_ is used to render images.
* The Volto default theme is based on Semantic UI theme and is called `Pastanaga <https://youtu.be/wW9mTl1Tavc?t=133>`_
* Same as Plone, Volto is highly extendable with add-ons for further features.
* Existing Volto components are customizable with a technology similar to `z3c.jbot` called :ref:`volto_overrides-componentshadowing-label`.
* Volto provides server side rendering (SSR), important for SEO-purposes.
* Volto aims to provide 100% of the features of the current Plone backend. Volto provides additional functionality that Plone does not have.
* Volto features the Pastanaga Editor, allowing you to visually compose a page using blocks. This feature is enable for content-types that have the dexterity-behavior ``volto.blocks`` enabled.
* Using the Pastanaga Editor, the content you add in blocks and the arrangement of blocks is stored as JSON in the schema-fields `blocks` and `blocks_layout` provided by the dexterity-behavior `volto.blocks`. Additionally you can edit all fields from the content-type schema in a sidebar.
* If you do not use the behavior ``volto.blocks`` the fields from a content-type schema are edited and stored exactly like previously in Plone.


**You are about to decide for one frontend: Volto or the Plone Classic frontend.**


* Most existing add-ons for Plone will have to be adapted to Volto if they touch UI (e.g. templates for content-types, controlpanels or viewlets).
* For Volto add-ons see https://github.com/collective/awesome-volto/
