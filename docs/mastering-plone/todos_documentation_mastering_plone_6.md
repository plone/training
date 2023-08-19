# Proposed changes to this trainning for Plone 6

TODO Remove this file, when done.

```text
1. About Mastering Plone::

    1.1. Upcoming Trainings
    1.2. Previous Trainings
    1.3. Trainers
    1.4. Using the documentation for a training
    1.5. Building the documentation locally
    1.6. Build new
    1.7. Train the trainer
    1.8. Contributing
    1.9. License

2. Introduction::

    2.1. Who are you?
    2.2. What will we do?
    2.3. What will we not do?
    2.4. What to expect
    2.5. Classroom Protocol
    2.6. Documentation
    2.7. Further Reading

3. What is Plone?::

    3.1. Core concepts
    ++ Add Info on RESTAPI and VOLTO

4. Installation & Setup::

    4.1. Installing Plone
    ++ Add info on building the Frontend
    4.2. Hosting Plone
    ++ Add Info on deploying the Frontend
    4.3. Production Deployment

5. Installing Plone for the Training::

    5.1. Installing Plone without vagrant
    5.2. Installing Plone with Vagrant
    ++ Update to build VOLTO

6. The Case Study::

    6.1. Background
    6.2. Requirements
    ++ Discuss where which feature will need to be develop

7. The Features of Plone::

    7.1. Starting and Stopping Plone
    7.2. Walkthrough of the UI
    7.3. Users
    7.4. Configure a Mailserver
    7.5. Content-Types
    7.6. Folders
    7.7. Collections
    7.8. Content Rules
    7.9. History
    7.10. Manage members and groups
    7.11. Workflows
    7.12. Working copy
    7.13. Placeful workflows
    ++ Update to use new fronte

8. The Anatomy of Plone::

    ++ Start with Backend / RESTAPI / Fronte
    8.1. Database
    8.2. Zope
    8.3. Content Management Framework
    8.4. Zope Toolkit / Zope3
    8.5. Zope Component Architecture (ZCA)
    8.6. Pyramid
    8.7. Exercise

9. What’s New in Plone 5, 5.1 and Plone 5.2::

    ++ Rewrite for Plone 6 and Volto
    9.1. Default Theme
    9.2. New UI and widgets
    9.3. Folder Contents
    9.4. Content Types
    9.5. Resource Registry
    9.6. Chameleon template engine
    9.7. Control panel
    9.8. Date formatting on the client side
    9.9. plone.app.multilingual
    9.10. New portlet manager
    9.11. Remove portal_skins
    9.12. Plone 5.1
    9.13. Plone 5.2

10. Configuring and Customizing Plone::

    ++ Rewrite for Controlpanels in VOLTO
    10.1. The Control Panel
    10.2. Portlets
    10.3. Viewlets
    10.4. ZMI (Zope Management Interface)
    10.5. Summary

11. Theming::

    ??

12. Extending Plone::

    ++ Rewrite for React and RESTAPI
    12.1. Extension technologies

13. Extend Plone With Add-On Packages::

    ++ Rewrite to discuss frontend and backend-addons
    13.1. Some notable add-ons
    13.2. How to find add-ons
    13.3. Installing Add-ons
    13.4. collective.easyform
    13.5. Add page layout management with plone.app.mosaic
    13.6. Internationalization
    13.7. Summary

15. Buildout I::

    ++ Move after "Add your own addons"
    ++ Add a chapter that discusses the Volto-Addon structure
    15.1. Minimal Example
    15.2. Syntax
    15.3. Recipes
    15.4. References
    15.5. A real life example
    15.6. Mr. Developer
    15.7. Extensible
    15.8. Be McGuyver

Write Your Own Add-Ons to Customize Plone::

    ++ use plonecli
    1. Creating the package
    2. Eggs
    3. Inspecting the package
    4. Including the package in Plone
    5. Exercises
    6. Summary

Dexterity I: Content types::

    ++ Rewrite (Start with Python Schema in the Filesystem)
    1. What is a content type?
    2. The makings of a Plone content type
    4. Modifying existing types
    #. Default Behaviors
    5. Creating content types TTW
    7. Exercises


Dexterity II: Talk::

    #. The fti
    #. The type registration
    #. The schema
    #. The instance class
    #. Enabling our code (install/reinstall)
    #. Field type reference
    #. Schema directives: widgets, permissions
    #. point to later chapter for complete list of features


XX. Add your own Volto addon

    #. Add a Volto Addon (create-volto-app)

XX. Add a custom view component for talks

    #. Register new view src/components/Views/Talk.jsx
    #. Finish View incrementally


18. Views I::

    ++ Maybe move to a later state
    18.1. A simple browser view

19. Page Templates::

    ++ Remove / Replace with a chaptere on custom Components with JSX
    19.1. TAL and TALES
    19.2. Chameleon
    19.3. Exercise 1
    19.4. METAL and macros
    19.5. Accessing Plone from the template
    19.6. Exercise 2
    19.7. Accessing other views
    19.8. What we missed

20. Customizing Existing Templates::

    ++ Replace with chapter on overwriting existing React components
    20.1. The view for News Items
    20.2. The Summary View
    20.3. Finding the right template
    20.4. skin templates
    20.5. Summary

21. Views II: A Default View for “Talk”::

    ++ Replace with custom component
    21.1. View Classes
    21.2. Browser Views
    21.3. Reusing Browser Views
    21.4. The default view
    21.5. Using helper methods from DefaultView
    21.6. The complete template for talks
    21.7. Behind the scenes

22. Views III: A Talk List::

    ++ Replace with a custom component that uses the @search endpoint to get talks
    ++ Keep information on catalog, indexes and metadata. Discuss search endpoint
    22.1. Using portal_catalog
    22.2. brains and objects
    22.3. Querying the catalog
    22.4. Exercises
    22.5. The template for the listing
    22.6. Setting a custom view as default view on an object
    22.7. Summary

23. Testing in Plone::

    ++ ???
    23.1. Types of tests
    23.2. Writing tests
    23.3. Plone tests
    23.4. Robot tests
    23.5. More information

24. Behaviors::

    ++ Keep as it is
    24.1. Dexterity Approach
    24.2. Names and Theory
    24.3. Practical example
    24.4. Adding it to our talk

25. Writing Viewlets::

    ++ Replace with a component
    25.1. A viewlet for the featured behavior
    25.2. Featured viewlet
    25.3. Exercise 1
    25.4. Exercise 2

26. Programming Plone::

    ++ Add chapter (before or after) on restapi and various endpoints
    ++ Discuss best-practices and tools for JS/React-Development
    26.1. plone.api
    26.2. portal-tools
    26.3. Debugging
    26.4. Exercise

27. IDEs and Editors::

    ++ Same as above: Discuss helpful features in editors for JS Development


28. Dexterity Types II: Growing Up::

    ++ remove part on marker interfaces (since we already have a python
    28.1. Add a marker interface to the talk type Interface)
    28.2. Upgrade steps
    28.3. Add a browserlayer
    28.4. Add catalog indexes
    28.5. Query for custom indexes
    28.6. Exercise 1
    28.7. Add collection criteria
    28.8. Enable versioning
    28.9. Summary

29. Custom Search::

    ++ maybe remove or mention volto-based addons here
    29.1. eea.facetednavigation
    29.2. collective.collectionfilter

30. Turning Talks into Events::

    ++ Keep behavior. Replace view-change with reusing a (hopefully) existing react component
    30.1. Exercise 1
    30.2. Exercise 2

31. User Generated Content::

    ++ Keep this
    31.1. Self-registration
    31.2. Constrain types
    31.3. Grant local roles
    31.4. A custom workflow for talks
    31.5. Move the changes to the file system

32. Resources::

    ++ Remove or add info on theming with Volto

33. Using Third-Party Behaviors::

    ++ remove or replace.
    ++ Maybe the addon collective.behavior.banner could be useful in Volto as well with a custom endpoint
    33.1. Add Teaser With collective.behavior.banner

34. Dexterity Types III: Python::

    ++ Keep content-type as before
    ++ change Viewlet to custom component
    ++ the scaling-thing might be a problem
    34.1. The Python schema
    34.2. Directives
    34.3. Validation and default values
    34.4. The Factory Type Information, or FTI
    34.5. The view
    34.6. The viewlet
    34.7. The template for the viewlet

35. Relations::

    ++ Keep but add a use-case for the conferennce-Website (e.g. linking Users to Talks if self-registration and membrane would work in Plone 6)
    35.1. Creating relations in a schema
    35.2. Accessing and displaying related items
    35.3. Creating RelationFields through the web
    35.4. The stack
    35.5. RelationValues
    35.6. Accessing relations and backrelations from code

36. Manage Settings with Registry, Control Panels and Vocabularies::

    ++ Keep control panel in backend? Add example for control panel in Fronend?
    36.1. The Registry
    36.2. A setting
    36.3. Accessing and modifying values in the registry
    36.4. Add a custom control panel
    36.5. Vocabularies

37. Creating a Dynamic Front Page::

    ++ Remove with a simple blocks-bases site
    37.1. The Front Page
    37.2. The template
    37.3. Twitter
    37.4. Activating the view

38. Creating Reusable Packages::


39. More Complex Behaviors::

    ++ Add custom restapi-endpoint for voting
    ++ Change to use BTrees instead of PersitentDict
    39.1. Using Annotations
    39.2. Using Schema
    39.3. Writing Code

40. A Viewlet for the Votable Behavior::

    ++ Replace with new frontend component for the new Voting endpoint
    40.1. Voting Viewlet
    40.2. Writing the Viewlet code
    40.3. The template
    40.4. JavaScript code
    40.5. Writing 2 simple view helpers

41. Making Our Package Reusable::

    ++ Keep this since it ties the different addons together
    41.1. Adding permissions
    41.2. Using our permissions
    41.3. Provide defaults

42. Using starzel.votable_behavior in ploneconf.site::

    ++ keep

43. Releasing Your Code::

    ++ ???

44. Buildout II: Getting Ready for Deployment::

    44.1. The Starzel buildout
    44.2. A deployment setup
    44.3. Other tools we use

45. Plone REST API::

    ++ Add new custom react component for lightining talks
    ++ Move up since it is easier than voting
    45.1. Installing plone.restapi
    45.2. Explore the API
    45.3. Implementing the talklist
    45.4. Submit lightning talks
    45.5. Exercise

46. The Future of Plone::

    ++ Update


47. Optional::

    ?
```
