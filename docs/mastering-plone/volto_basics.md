(volto-basics-label)=

# Volto Basics

Volto is a React based frontend for Plone. Beside the **Plone Classic** frontend and other frontends it is the default frontend and editor from Plone 6 on.

The intention to build a new frontend was to achieve a new experience for editing the web.

Here are some things you should know if you are new to Plone 6 or Volto:

**Volto is the default frontend for Plone 6 but Plone can still serve as backend and frontend.**

- All data is stored in Plone, Volto comes in to display and edit the content.
- Volto is built in [ReactJS](https://reactjs.org), a modern Javascript Framework.
- Volto uses [plone.restapi](https://plonerestapi.readthedocs.io/) to communicate with Plone backend.

Details

- Volto is installed separately from Plone backend. See chapter {ref}`installation-Volto-label` for instructions.
- Volto runs in a different process than the Plone backend. By default Volto runs on port 3000. If you start Volto with `yarn start` you can see the frontend on <http://localhost:3000>. The Plone backend runs by default on <http://localhost:8080>
- To create a new Plone site in your already set up Zope environment you use the backend, this is by now not possible in Volto.
- Volto takes advantage of [Semantic UI React components](https://react.semantic-ui.com/) to compose most of the views. For example the component [Image](https://react.semantic-ui.com/elements/image/) is used to render images.
- The Volto default theme is based on Semantic UI theme and is called [Pastanaga](https://youtu.be/wW9mTl1Tavc?t=133)
- Same as Plone, Volto is highly extendable with add-ons for further features.
- Existing Volto components are customizable with a technology similar to `z3c.jbot` called {ref}`volto-overrides-componentshadowing-label`.
- Volto provides server side rendering (SSR), important for SEO-purposes.
- Volto aims to provide 100% of the features of the current Plone backend. Not all features of Plone are implemented in Volto yet.
- Volto provides additional functionality that Plone does not have.
- For example Volto features the Pastanaga Editor, allowing you to visually compose a page using blocks. This feature is enabled for content types that have the dexterity behavior `volto.blocks` enabled.
- Using the Pastanaga Editor, the content you add in blocks and the arrangement of blocks is stored as JSON in the schema fields `blocks` and `blocks_layout` provided by the dexterity behavior `volto.blocks`. Additionally you can edit all fields of the content type schema in a sidebar.
- If you do not use the behavior `volto.blocks` the fields from a content-type schema are edited and stored exactly like previously in Plone.

**You have to decide for one frontend: Volto or the Plone Classic frontend.**

Here are some pointer that may help you decide:

- New projects should use Volto unless a important feature or add-on is still missing and cannot be implemented within the project budget
- Existing projects that are updated to Plone 6 can decide what frontend to use. If a lot of customizations were done and you don't want to reimplement lot of custom templates or features in Volto it is a good idea to use Plone Classic.
- Most existing add-ons for Plone will have to be adapted to Volto if they touch UI (e.g. templates for content types, control panels or viewlets).
- For a selection of Volto add-ons see <https://github.com/collective/awesome-volto/>
