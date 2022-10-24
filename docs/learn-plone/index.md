---
myst:
  html_meta:
    "description": "Learn Plone"
    "property=og:description": "Learn Plone for Content Editors"
    "property=og:title": "Learn Plone"
    "keywords": "Plone, user guide, content, editors"
---
(learn-plone-label)=

# Learn Plone, for Content Editors and Managers #Ploneconf2022

# Outline
- Hello! Who we are
- Who YOU are
    - What are you hoping to get out of this class?
- Resources for this class
    - Documentation and training materials
        - "Working with Content" documentation [https://docs.plone.org/working-with-content/index.html](https://docs.plone.org/working-with-content/index.html)
        - Plone Training home [https://training.plone.org/](https://training.plone.org/)
        - Plone 6 documentation [https://6-dev-docs.plone.org/](https://6-dev-docs.plone.org/) (work in progress)
    - Demo sites
        - Plone 6 Classic demo site https://demo.plone.org/
        - Plone 6 Volto demo site [https://6.demo.plone.org/](https://6.demo.plone.org/)
            - Volto 16.0.0-alpha.42
            - Plone 6.0.0b3
            - plone.restapi 8.30.0
        - https://volto.kitconcept.dev 
            - Volto 16.0.0-alpha.42
            - Plone 6.0.0b3
            - plone.restapi 8.30.0
            - kitconcept.volto add-on version:   3.0.0a9.dev0 https://github.com/kitconcept/kitconcept.volto
    - Volto blocks examples [https://volto.kitconcept.dev/blocks-examples](https://volto.kitconcept.dev/blocks-examples)
    - Awesome Volto, the ecosystem of add-ons https://github.com/collective/awesome-volto


# What is Plone
- open source software
- community (users, developers, integrators, service providers)
- the Plone back end is written in Python
- the Plone front end is React, the widely used JavaScript front end framework
# Why Plone

Plone comes with all the functionality you need to create and manage websites and intranets. Add-ons can provide even more functionality.

- https://plone.org/what-is-plone/plone/plone-features
## Great features of Plone

Reasons why you should use Plone:

- Everything you need, in the box
- Support for multiple editors: version history, approval workflow, metadata
- Search, navigation
- Great for organizing content
- Multilingual support
- Secure
- Accessibility compliance
# Demo sites

In this training we will use the following demo sites:

- Plone 6 Volto demo site [https://6.demo.plone.org/](https://6.demo.plone.org/)
- Plone 6 Volto latest demo site https://volto.kitconcept.dev
- Plone 6 classic demo site https://demo.plone.org

You can set up Plone on a local computer by following the instructions at https://plone.org/download

If you’d like to set up your own server and site without needing to use the command line, see the Plone in a Box™ project at https://github.com/collective/plone-in-a-box. It makes it easy to set up a cloud server running Plone, on Amazon AWS, Linode, and DigitalOcean cloud providers.

# A Tour of Plone
- Logging in
- Top navigation
- Search
- Menu bar
- Footer
- Personal menu
- Site Setup and control panels
# Toolbar
- Editing an item
- Contents view
- Adding an item
    - event
    - file
    - image
    - link
    - news item
    - page
- … (more menu)
# Site Setup (control panels)
- many, but the notable ones:
    - Site
    - Social Media
    - Add-ons
    - Undo
    - URL Management (aliases)
    - Content Types
# Creating a page with blocks
- Adding, deleting blocks
- Many kinds of blocks
    - most used
        - …the blocks you use most often…
    - text
        - description
        - text
    - media
        - image
        - video
    - common
        - listing
        - table of contents
        - hero
        - maps
        - HTML
        - search
        - table
        - grid
        - images grid
        - teaser
        - system
    - on https://volto.kitconcept.dev:
        - text with background colour
        - heading
        - accordion
        - slider
        - button
        - carousel
- Exercise: create a page and add some blocks to it
# Content types

What is a content type?

A content type is a kind of object that can store information and is editable by users. We have different content types to reflect the different kinds of information about which we need to collect and display information. Pages, folders, events, news items, files (binary) and images are all content types.

It is common in developing a web site that you'll need customized versions of common content types, or perhaps even entirely new types.

What would a conference attendee want to know about a conference talk?

- title
- summary
- description
- information about the presenter (name, profile photo, Twitter handle)
- the intended audience (users, integrators, developers, designers, editors)
- the duration of the talk (short, long)
- the date and time of the talk
- the location (room) of the talk
## Metadata
- Information about your content
    - Title, summary, author, dates, keywords (tags)
- Exercise: apply the keyword “Track 1” to your talk in the Track 1 subfolder, and the keyword “Track 2” to your talk in the Track 2 subfolder
    - What happens if you click on a tag?
- Harnessing the power of tagging
- Using the related content feature
# How to create content types (Kim N)

…the no-code way!

(Tour of the Content Types control panel)

- Fields
- Behaviours

Exercises:

- Exercise: go to the Content Types control panel and create a Talk content type
- Exercise: go to the home page and create a Talk
- Exercise: create another Talk

For more information:

- For more info on creating content types the no-code and low-code way: see the Through the Web training https://training.plone.org/5/ttw/dexterity.html (currently Plone Classic)
- For more complex content types (Python coding required): see the Mastering Plone training https://training.plone.org/5/mastering-plone/index.html
# Listings and Search (Kim P)
- Examples of advanced blocks
    - listing blocks
        - can put multiple on the same page
        - https://2022.ploneconf.org/schedule/talks (keynotes and talks)
    - faceted search block
        - https://2022.ploneconf.org/speakers
# Dynamically organizing your content
- Displaying your content in different ways for different purposes
- Volto listing blocks
- Exercise: create a listing block that displays all talks
- Exercise: create a listing block that displays Track 1 talks
    - How did you do it? Is there another way to do this?
- Exercise: create a listing block that displays Beginner talks
    - What do you see? Is it what you expected?
- Faceted search with the Volto search block
    - Exercise: create a search that displays all talks
    - Exercise: create a search that displays Track 1 talks
    - Exercise: create a search that displays Beginner talks
    - Exercise: view these collections in another browser/tab
# Organizing Content
- How to organize content and re-arrange sections of your website
- Plone Classic folders vs Volto everything-is-a-container
- The contents view
- Exercise: create a Talks “folder”
- Exercise: move both your Talks into the Talks folder
- Exercise: use the folder contents view to move several talks
- What else can you do with the contents view?
- Aside: Folders and “default pages” (Plone Classic)
# Private vs Public Information
- Exercise: open your site in another browser or in an incognito/private window
    - Compare what you see in both windows/tabs
    - Why is that happening?
## Plone workflow
- States
- Transitions
- Plone comes with several workflows
    - simple publication workflow
    - intranet/extranet
    - community workflow
    - single state workflow
    - no workflow
- Exercise: publish your Talks folder, and view it in another browser/tab
- Specifying which workflows apply to content types
- Advanced:
    - Specifying which workflows apply to a folder
        - "placeful workflow policy"
# Users and Groups
    - Plone is a multiuser CMS
        - Unlimited users and groups
    - Organize users with groups
    - Exercise: create two users, “editor” and “reader”
    - Exercise: use the Users control panel to set roles on these users
    - Exercise: create two more users, “editor2” and “reader2”, use the Groups control panel to create two groups, “Editors” and “Readers”, and User Group Memberships control panel organize the users into their appropriate group
    - Exercise: use the Groups control panel to set roles on the “Editors” and “Readers” groups
    - Exercise: remove the roles on individual users
        - Why would we do this?
    - Advanced:
        - Connecting Plone to central authentication systems
# Sharing folders
- 
# Content rules
- automate advanced publishing strategies, send out notifications when content needs reviewing, and more
# Staging content
- “Working copy support”
# Themes
# Add-ons for forms processing
- PloneFormGen
- EasyForm
- volto-form-block https://github.com/collective/volto-form-block
# Which should I use: Plone Classic or Volto?
# Next steps:
        - For editors and managers
            - "Working with Content" documentation
        - 
        - For developers
            - Mastering Plone training (you can use the training materials on your own)
        - For theme designers
            - Theming Plone training (Volto or Diazo themes)
        - For system administrators
            - Installing, Managing And Updating Plone https://docs.plone.org/manage/index.html
# Resources
        - The People, the People!
            - Come talk to us! We’re friendly! We won’t bite! (probably not)
        - This conference https://2022.ploneconf.org
        - The sprints this weekend
            - We’d love you to join! Beginners are extra welcome! Get to know other Plonistas, help Plone get better, give us your ideas and thoughts (fresh eyes)
        - The forum https://community.plone.org
        - The Discord chat server https://plone.org/chat
        - Regional sprints throughout the year
        - Other events (symposia, Plone Open Garden, World Plone Day)
        - Podcasts: The Plone Newsroom, The Plone Podcast
        - Plone service providers https://plone.org/providers
        - Plone jobs/help wanted https://community.plone.org/c/jobs/38
        - Past conferences: (2021,2020,2019,2018,2017,2016,2015).ploneconf.org
        - YouTube Plone channel https://www.youtube.com/c/PloneCMS
        - Plone on social media
            - Twitter https://twitter.com/plone
            - Facebook https://www.facebook.com/Plone and https://www.facebook.com/plonecms/
            - Instagram https://www.instagram.com/plone/
            - Flickr https://www.flickr.com/photos/plone-foundation
        - Plone on GitHub
            - Plone core https://github.com/plone
            - Plone add-ons https://github.com/collective
# Learn Plone (2020 and 2021)
- In 2021, David Bain gave the Learn Plone training for which he created these nice slides [tinyurl.com/startplone](http://tinyurl.com/startplone); the recording is at 2021 https://2021.ploneconf.org/schedule/getting-started-with-your-plone-6-site
- David’s 2020 training can be seen at https://www.youtube.com/watch?v=kVBXAxFPxgU&list=PLGN9BI-OAQkTVkkJfSMHu-l-_AVW_uoRf&index=18



