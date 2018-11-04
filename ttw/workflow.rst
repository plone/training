.. _workflow-label-ttw:

=========
Workflow
=========

This part of the class explains what workflow applications are, why they are useful,
and how you can build them using Plone without needing to write any code.

.. _workflow-what-is-workflow-label-ttw:

What Is Workflow?
=================

Workflow helps you track and control the state of a piece of Plone content, e.g., whether it is private or published.

For example, when you first create a Plone page, it starts off in the “Private” state: only you and someone with Manager role can view it. Once you have finished editing the page, you submit it for review: your page is now in the “Pending Review” state. Only someone with Reviewer role can approve the page for publication. If they do approve the page for publication, it is in the “Published” state: it is visible to everyone, including those visiting the site who aren’t logged in.

In Plone, a workflow definition includes the following:

* its states, e.g. “Private”, “Pending review”, “Published”
* the security settings for each state, e.g. which roles or groups can view or edit a content item in that particular state
* the transitions between states, e.g. “submit” (from “Private” to “Pending review” state), “publish” (from “Pending review” to “Published” state)
* the security settings for each transition, e.g. which roles or groups are allowed to initiate that particular transition

The DCWorkflow tool, which ships with Plone, is what makes this possible. The fact that DCWorkflow is a core component of Plone is one of the things that differentiates Plone from other content management systems, in which workflow is either not available or is an afterthought.

Workflow protects Plone site content from unauthorized viewing and editing, and lets you share those rights with others, via the Sharing tab.

.. _workflow-several-label-ttw:

Plone Comes With Several Workflows
==================================

Each Plone site includes several workflows out of the box:
* Simple Publication Workflow
* Single State Workflow
* Comment Review Workflow
* Community Workflow for Folders
* Intranet Workflow for Folders
* Intranet/Extranet Workflow
* Single State Workflow
* Community Workflow

Plone lets you assign a different workflow to each content type.

(Plone also lets you assign *no* workflow to a content type; in Plone 5, for example, File and Image content types are not assigned a workflow, so File and Image items take their state from their containing folder.)

Plone lets you create workflow policies that define which workflow should be assigned to a given folder and its contents.



.. _workflow-add-label-ttw:

You Can Add and Customize Workflows
===================================

Plone lets you edit workflows and add new ones to a site:
by installing an add-on that includes one or more new workflows
through the included Plone Management Interface
through the Workflow Manager (plone.app.workflowmanager) add-on

The Workflow Manager is a much better tool than the Management Interface for creating or editing complex workflows because it has a diagram-centric, visual user interface.

.. image:: _static/image12.jpg

For this class, however, we will be creating a simple workflow and so we will use the Management Interface. We also believe it is important for a Plone power user or site administrator to know how to use Plone’s built-in tools, in case you need to debug a security/permission issue and you can’t install the Workflow Manager add-on.


.. _workflow-applies-label-ttw:

Workflow Applies to Included and New Content Types
==================================================

As soon as you begin working with content in a Plone site, you are using its workflow capabilities.

Every content type in a Plone site is assigned a specific workflow or is assigned the site’s default workflow (the Simple Publication Workflow is the default default workflow for a Plone site):
* Pages
* Folders
* News Items
* Events
* Collections
* Files
* Images
* Links

But you can also have workflow apply to any new content types you add to your Plone site.

This means you can use Plone workflow to track anything that you can store in a Plone site, including the online equivalent of paper forms.

Especially in large organizations, the conversion of paper forms to Plone forms and content items can represent a tremendous increase in efficiency (time, accuracy, and retrievability).


.. _dexterity1-permits-label-ttw:

Example Business Process: Home Renovation Permits
=================================================

Imagine a scenario in which a city government wants homeowners to obtain a permit before renovating their home, so that inspectors can verify later whether a permit was obtained for that work.



.. _workflow-paper-label-ttw:

The Paper-Based Business Process
--------------------------------

Typically, the process would go like this:
* The homeowner goes to city hall to get the paper permit
* The homeowner fills out the permit
* The homeowner returns the permit to city hall, with payment

Within city hall, once the permit has been received by the city, there is an internal process to be followed:
* The permit must be verified (no missing required fields, everything filled out seems sensible
* Payment must have been received
* The permit is sent to one or more internal city departments for approval
* If the permit is approved, the homeowner is sent a copy of the approval, usually by (physical) mail

For enforcement purposes, the homeowner must display a copy of the approved permit. A city inspector may ask to see the approved permit, to ensure that the renovations being done were the ones included in the approved permit.


.. _workflow-online-label-ttw:

The Online Business Process
---------------------------

If all of the above steps could be performed electronically,
* a homeowner could instantaneously obtain and quickly fill out an online renovation permit;
* submitting the filled out permit could be done through a website without requiring any travel;
* electronic payment could be confirmed and associated electronically with the submitted permit;
* forwarding the permit for approvals within city hall could be done instantaneously;
* no more permit approvals would get lost or unnecessarily delayed in transit;
* phone calls from homeowners asking about the status of their permit would be eliminated;
* inspectors needing to look up a permit could do so instantaneously.


.. _workflow-what-is-a-workflow-application-label-ttw:

What is a Workflow Application?
===============================

A workflow application is what we call all the elements required to make an online business process:
* a form, to be filled out by the user
* content items, created by the form
* workflow, applied to each content item

Additionally, these elements are nice to have:
* a dashboard showing the state of all the content items (ie. have they been handled, are they done, what state is each one in?)
* a way of searching for individual content items, via any of their form field values
* a welcoming front page that directs users to the form, displays instructions, and provides useful links to the workflow application administrators and internal users (if any)


.. _workflow-why-label-ttw:

Why Use a Workflow Application?
===============================

The authors of this training class have helped organizations convert paper-based forms and their handling into online workflow applications.

In one case, a single (albeit complex) workflow application has allowed a university department to save at least half a staff person’s time, not so much to reduce staffing but to allow an already overburdened staff to be reassigned to work that cannot be automated. Over a ten-year period, the cost savings represent hundreds of thousands of dollars and counting, not including intangible benefits such as:

* clients have immediate access to forms at any time of day or night
* clients are notified by email when their submitted form is being processed
* clients can view their submitted forms and check their status at any time
* no submitted forms are lost
* no submitted forms are overlooked
* submitted forms can be searched for electronically
* staff working with submitted forms have always-updated status information and work lists
* staff have immediate access to submitted data, anywhere, anytime

For the remainder of this class, we will show how you can create each of these elements with Plone and how you put them together to make a workflow application.

.. _workflow-simple-label-ttw:

A Simple Workflow Application: Submitting Questions
===================================================

We will start by showing how to create a very simple workflow application: a form that a website visitor can fill out to ask a question.

Whenever the form is filled out, a “question” content item is created and is placed in the “unanswered” state.

The website administrator must answer the question (via email), then transition the question content item into the “answered” state.

At any time, there should be a way to see which questions have not yet been answered, and there should be a way to look up questions (by the submitter’s name, email address, and the text of their question).

.. _workflow-tools-label-ttw:

Tools for Building Workflow Applications
========================================

These are tools we can use to create each element of a workflow application:

* the form to be filled out:
  * `Dexterity <https://pypi.org/project/plone.app.dexterity/>`_ (included with Plone), or
  * `PloneFormGen <https://github.com/smcmahon/Products.PloneFormGen>`_, or
  * `EasyForm <https://github.com/collective/collective.easyform/>`_
* creating content items:
  * `Dexterity <https://pypi.org/project/plone.app.dexterity/>`_ (included with Plone), or
  * `uwosh.pfg.d2c <https://github.com/collective/uwosh.pfg.d2c>`_, or
  * `collective.pfg.dexterity <https://pypi.org/project/collective.pfg.dexterity/>`_
* creating the workflow:
  * the Management Interface, a low-level, legacy way of configuring Plone’s innards, or
  * `Workflow Manager <https://github.com/plone/plone.app.workflowmanager>`_, a Plone add-on that provides a more intuitive, graphical way of creating, editing, and applying workflows

For this training class we will use Dexterity and the Management Interface.

Dexterity is the content type framework that replaces Archetypes. (By “content type framework” we mean the infrastructure that supports the creation and customization of content types, and the mechanism that lets Plone sites read those content types so users can create content items). Dexterity is not a genuine form builder tool, but it includes one.

PloneFormGen is the venerable form builder for Plone, but since it is built using the old, deprecated Archetypes framework, we have begun to shy away from recommending it for new sites. It works well with Plone 5, but its long term future is in doubt.

EasyForm is intended to be the new PloneFormGen. It has been around for a few years now, and, with the release of Plone 5 in 2015, began gaining momentum and wider support within the community. It does not yet have all the functionality of PloneFormGen, which is why many of us still use and (with caveats) recommend PloneFormGen, even on new sites.

The Workflow Manager is a Plone add-on that provides an intuitive graphical way of creating, editing, and applying a workflow. It is a must-have when dealing with workflows that have many states and transitions, but is not needed for working with simple workflows like the ones included with Plone. (Compare this to, for example, one custom workflow the author of this training class has been working on that contains 36 states and 56 transitions).

.. _workflow-use-dexterity-label-ttw:

Use Dexterity to Build a Content Type and Form
==============================================

Your Plone site already includes Dexterity, and it is already activated.

You should be logged into your Plone site as an account with Manager role, e.g. “admin”.

1. Go to Site Setup
2. Go to the Dexterity Content Types control panel
3. Click the “Add New Content Type…” button
4. For “Type Name”, enter “Question”. Press Tab to move to the next field, “Short Name”. Allow the “Short Name” value to be set to “question”. Press Tab again to move to the “Description” field, and enter “A question asked by a website visitor”. Press the “Add” button.

.. image:: _static/workflow/image47.png

5. You will be taken back to the Dexterity Content Types control panel. The new Question content type will have been added to the bottom of the list of content types. Click on it (on the blue “Question” link in the “Type Name” column).

.. image:: _static/workflow/image28.jpg

.. image:: _static/workflow/image54.jpg

6. Click on the Fields tab to see the fields that this new content type contains. By default, new Dexterity content types have Title and Description fields.

.. image:: _static/workflow/image82.jpg

7. For this example, we don’t need them, so we will disable them by clicking on the Behaviors tab. Behaviors are essentially packaged sets of fields that work together. In this example we want to disable the “Dublin Core metadata” behavior, so that this content type no longer includes title and description fields. Uncheck the box next to “Dublin Core metadata” and click the “Save” button at the bottom of the page. You should see the message “Behaviors successfully updated”.

.. image:: _static/workflow/image68.jpg

.. image:: _static/workflow/image10.jpg

8. Click again on the Fields tab. There should be no fields shown for the content type

.. image:: _static/workflow/image42.jpg

9. Click “Add new field...”, and in the dialog box fill in “Title” with “Your Full Name”, press the Tab key, leave the default “Short Name” value “your_full_name”, press the Tab key, enter for “Help Text” the value “Please enter your full name”. Leave the “Field type” default value of “Text line (String)”, check the box for “Required field”, press the “Add” button.

.. image:: _static/workflow/image45.jpg

10. Click “Add new field...”, and in the dialog box give the new field the title “Your Email Address”, short name “your_email_address”, help text “Please enter your email address”, select “Email” for the field type, and make the field required. Press the “Add” button.

.. image:: _static/workflow/image97.jpg

.. image:: _static/workflow/image40.jpg

.. image:: _static/workflow/image17.jpg

11. Click “Add new field...”, and in the dialog box give the new field the title “Your Question”, short name “your_question”, help text “Please type your question here. We will reply via email as soon as possible.”, field type “Text”, and make the field required. Press the “Add” button.

.. image:: _static/workflow/image66.jpg

.. image:: _static/workflow/image7.jpg

.. image:: _static/workflow/image88.jpg

Congratulations, you have created the Question content type!


.. _workflow-about-dexterity-xml-label-ttw:

About the Dexterity XML Field Model
===================================

If you click on the “Edit XML Field Model” button, you can see how Dexterity stores the definition of the Question content type in XML format:

.. code-block:: xml

    <model xmlns:form="http://namespaces.plone.org/supermodel/form" xmlns:i18n="http://xml.zope.org/namespaces/i18n" xmlns:lingua="http://namespaces.plone.org/supermodel/lingua" xmlns:marshal="http://namespaces.plone.org/supermodel/marshal" xmlns:security="http://namespaces.plone.org/supermodel/security" xmlns:users="http://namespaces.plone.org/supermodel/users" xmlns="http://namespaces.plone.org/supermodel/schema">
      <schema>
        <field name="your_full_name" type="zope.schema.TextLine">
        <description>Please enter your full name</description>
        <title>Your Full Name</title>
        </field>
        <field name="your_email_address" type="plone.schema.email.Email">
        <description>Please enter your email address</description>
        <title>Your Email Address</title>
        </field>
        <field name="your_question" type="zope.schema.Text">
        <description>Please type your question here. We will reply via email as soon as possible.</description>
        <title>Your Question</title>
        </field>
      </schema>
    </model>

Power user tip: it can be easier and faster to edit the XML model directly if you need to add fields for which you already have the XML snippet or if you want to reorder fields or otherwise edit any aspect of the field definitions. If you want to copy a content type from one site to another, copying the XML model is much faster than trying to rebuild the content type via the clickable user interface.

.. _workflow-viewing-dexterity-form-label-ttw:

Viewing the Dexterity Form
==========================

Now that you have created the Question content type, you view its “add form” (the form that lets you add a Question to your site) by navigating to any part of your site and clicking the “Add new…” menu item in the left toolbar.

1. Click on Home in the portal tabs

.. image:: _static/workflow/image22.jpg

2. Click on “Add new…” in the toolbar. You will see the new “Question” content type at the bottom of the submenu. Click on it, and you will be shown the “Add Question” form:

.. image:: _static/workflow/image84.jpg

.. image:: _static/workflow/image55.jpg

This “Add Question” form is what your website visitors will use. It is equivalent to the PloneFormGen and EasyForm forms described above in Section XXX.

Click the “Cancel” button to return to the front page of your site.

.. _workflow-create-a-folder-label-ttw:

Create a Folder to Hold Filled Out Forms
========================================

You will not want to clutter up the root (top) folder of your website. Instead, create a folder called “Questions” in which website visitors’ Question items will be created:

1. Click “Add new…” in the left toolbar

2. Choose “Folder”

3. For the title, enter “Questions”; for the summary, enter “All questions go here”. Press the “Save” button; your browser will be directed to the new Questions folder.

.. image:: _static/workflow/image93.jpg

.. _workflow-grant-access-to-folder-label-ttw:

Grant Access to the Folder
==========================

We need to give anonymous (not logged in) website visitors permission to add new Question items to this folder.

1. Publish the Questions folder by clicking the “State” toolbar button and choosing “Publish”.

.. image:: _static/workflow/image77.jpg

2. While viewing the newly published Questions folder, click on your browser’s URL (web address) bar and append “/manage_main” to the URL of the folder, e.g. “http://localhost:8080/Plone/questions/manage_main” then press the Return key to go to that URL. You will see the Management Interface view of the Questions folder.

.. image:: _static/workflow/image8.jpg

3. Click on the “Security” tab.

.. image:: _static/workflow/image13.jpg

4. Use your browser’s “find on this page” feature (Control-F or Command-F key or Edit->Find menu item) to search for “Add portal content”. It will be almost halfway down this tall page.

.. image:: _static/workflow/image57.jpg

5. Check the box in that row under the “Anonymous” column, then scroll to the bottom of the page and press the “Save Changes” button.

.. image:: _static/workflow/image23.jpg


.. _worfklow-test-the-form-label-ttw:

Test the Form to Create Content Items
=====================================

We have a Question content type, a folder in which to create Question content items, and a working “add” form that we can use to create Question content items.

We should test that form now, as a user with Manager role and as an anonymous (not logged in) website visitor.


.. _worfklow-test-the-form-as-manager-label-ttw:

Test the Form as a Manager
--------------------------

To test the form as a Manager, use the same browser window you have been using in which you are logged in as “admin”.

1. Go to the Questions folder at http://localhost:8080/Plone/questions

.. image:: _static/workflow/image94.jpg

2. Click the “Add new…” button in the toolbar and choose “Question”

.. image:: _static/workflow/image37.jpg

3. Fill in all the fields with your name, your email address, and a question

.. image:: _static/workflow/image32.jpg

4. Press the “Save” button

If all works correctly, you will be redirected to view your new Question item at the URL http://localhost:8080/Plone/questions/question

.. image:: _static/workflow/image19.jpg


.. _workflow-test-the-form-as-anonymous-label-ttw:

Test the Form as an Anonymous Website Visitor
---------------------------------------------

To test the form as an anonymous (not logged in) website visitor, open a new “incognito” (or “private browsing”) browser window: for Safari and Firefox, use File -> New Private Window; for Chrome, use File -> New Incognito Window.

1. Go to the Questions folder at http://localhost:8080/Plone/questions

.. image:: _static/workflow/image60.jpg

2. There is no toolbar shown because you’re not logged in with this browser window. To use the equivalent of the “Add new…” toolbar button in the toolbar and its “Question” choice, you must visit this URL: http://localhost:8080/Plone/questions/++add++question

.. image:: _static/workflow/image92.jpg

3. Fill in all the fields with your name, your email address, and a question

4. Press the “Save” button.

Did everything work as you expected? Why would you be taken to the login form?

.. image:: _static/workflow/image90.jpg

If you look at the URL bar of your browser, you should see this: http://localhost:8080/Plone/acl_users/credentials_cookie_auth/require_login?came_from=http%3A//localhost%3A8080/Plone/questions/question

The “came_from” variable value is the original URL you tried to view when Plone decided you did not have the necessary permissions and sent you to the login form. In this case, that original URL is http://localhost:8080/Plone/questions/question, which indicates that the Question item was created. But, because you are not logged in, you do not have permission to view that new Question item, which is in the “private” state (the initial state of the Simple Publication Workflow, the default workflow for a Plone site). That is why you were redirected to the login form.


.. _workflow-create-thank-you-page-label-ttw:

Create a Thank You Page
=======================

Being shown the login form is not ideal nor expected behaviour for anonymous website visitors who have successfully filled out a question form.

Instead, when they have filled out their question form and have pressed “Save”, you want them to get a nice thank you message.

Anonymous users are redirected to the login page when they try to view the Question item they just created. This is done by the default view for any Plone content item: Plone will not display a content item that is in the private state to an anonymous (not logged-in) user, so it gives the user a chance to log in. If the user has an account on the site and logs in successfully, Plone then checks to see if the user has the necessary permissions or roles needed to view the content item.

To change this behaviour, we need to create a new view for the Question content type that does the following:

* checks in the user is anonymous; if so, redirects to the site homepage and displays a thank you message

* if the user is not anonymous (ie. is logged in) and has edit permissions on the Question item, displays the values of the Question fields

.. _workflow-create-new-view-label-ttw:

Create a New View for the Question Content Type
-----------------------------------------------

For Plone’s simplest views, you need to define only a page template. (More complex views require Python code and ZCML registration).

Here is how to create a new page template:

1. Navigate to the Management Interface at http://localhost:8080/Plone/manage_main

.. image:: _static/workflow/image64.jpg

2. Click on “portal_skins”

.. image:: _static/workflow/image11.jpg

3. Click on “custom”

.. image:: _static/workflow/image31.jpg

4. Use the drop down menu on the right side of the page, next to the “Add” button, to select “Page template”.

.. image:: _static/workflow/image56.jpg

5. In the “Id” field, enter “question_view”, then press the “Add and Edit” button.

.. image:: _static/workflow/image39.jpg

This is the default HTML for new page templates:

.. code-block:: xml

    <html>
      <head>
        <title tal:content="template/title">The title</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8">
      </head>
      <body>

        <h2><span tal:replace="here/title_or_id">content title or id</span>
            <span tal:condition="template/title"
                tal:replace="template/title">optional template title</span></h2>

        This is Page Template <em tal:content="template/id">template id</em>.
      </body>
    </html>

6. We want the page template to display a thank you message to anonymous website visitors who are directed to their newly-created Question. Replace the page template HTML with the following, then press the “Save Changes” button.

.. code-block:: xml

    <html>
      <body tal:define="checkPermission nocall: context/portal_membership/checkPermission; canedit python:checkPermission('Modify portal content',context)" >

      <tal:anon condition="not: canedit">
        <h2>Thank you</h2>
        We will respond to your question as soon as possible!
      </tal:anon>

      </body>
    </html>

This page template calls Plone’s “portal_membership” tool’s “checkPermission” method to determine if the user has edit permission on the Question item. If the user does not, a thank you message is displayed.

Before we handle the other case (when the user does have edit permission on the Question item), let’s set this new page template to be the default one for Question items.

.. _workflow-set-default-view-label-ttw:

Set the Default View for the Question Content Type
--------------------------------------------------

Here is how to make the new view the default one for Question items:

1. Navigate to the Management Interface at http://localhost:8080/Plone/manage_main

.. image:: _static/workflow/image64.jpg

2. Click on “portal_types”

.. image:: _static/workflow/image6.jpg

3. Click on the “question” portal type (should be at the bottom of the page) to view the Question content type’s factory type information (“FTI”):

.. image:: _static/workflow/image79.jpg

4. In the “Default view method” field, change “view” to “question_view”.

.. image:: _static/workflow/image81.jpg

5. In the “Available view methods” field, add a new line containing the word “question_view”, then press the “Save Changes” button at the bottom of the page.

.. image:: _static/workflow/image33.jpg

From now on, whenever anyone views a Question item, the new “question_view” will be used to display the item.

.. _workflow-test-new-default-view-label-ttw:

Test the New Default View
-------------------------

Let’s verify that Question items now use this new default view.

1. In the same browser window, navigate to http://localhost:8080/Plone/questions/question

2. You should see a blank page

.. image:: _static/workflow/image70.jpg

You see a blank page because the new view displays something (the thank you message) only if the user does not have edit permission on the Question item. Because in this browser window you do have edit permission on the Question item (you are logged in as “admin”, which has Manager role, giving it all permissions on the entire site), the new view shows you nothing.

Now let’s verify how the new view works for an anonymous web visitor who just filled out a new Question form:

1. In a new incognito or private browsing window, go to http://localhost:8080/Plone/questions/question

2. You should see the thank you message.

.. image:: _static/workflow/image73.jpg

In an incognito or private browsing window, you are not logged into the Plone site, so you have no permissions to edit anything. The new Question view determines that you have no edit permissions then displays the thank you message.

.. _workflow-add-replying-label-ttw:

Add Replying to the New View
============================

Let’s go back and enhance the new Question view to handle the case when the user does have edit permission on the Question item.

1. In a normal browser window or tab (in which you are logged into the Plone site as “admin”), go to http://localhost:8080/Plone/portal_skins/custom/question_view/pt_editForm

.. image:: _static/workflow/image59.jpg

2. Replace the page template’s HTML with the following, then press the “Save Changes” button:

.. code-block:: xml

    <html>
      <body tal:define="checkPermission nocall: context/portal_membership/checkPermission; canedit python:checkPermission('Modify portal content',context)" >

      <tal:anon condition="not: canedit">
        <h2>Thank you</h2>
        We will respond to your question as soon as possible!
      </tal:anon>

      <tal:canedit condition="canedit">
        <div tal:define="portal_name here/portal_url/Title;
                    subject python: 'Your inquiry at ' + portal_name;
                    question_encoded python: context.your_question.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '%20');
                    question_encoded_quoted python: '&gt; ' + question_encoded;
                    subject_encoded python: subject.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '%20');">

        <h3>From: <span tal:replace="here/your_full_name">[name]</span></h3>
        <p>Question: <span tal:replace="here/your_question">[question]</span></p>
        <p><a tal:attributes="href python: 'mailto:' + context.your_email_address + '?subject=' + subject_encoded + '&body=' + question_encoded_quoted">[reply]</a></p>

        </div>
      </tal:canedit>

      </body>
    </html>

The page template now handles the condition in which the user has edit permissions on the Question item by displaying the name of the person asking the question, their question, and a “reply” link that you can click on to compose an email reply.

.. image:: _static/workflow/image89.jpg

If you click on the “reply” link, your email client is invoked to compose a reply, filled in with the recipient email address, subject, and their question:

.. image:: _static/workflow/image78.jpg

.. _workflow-design-the-workflow-label-ttw:

Design the Workflow
===================

So far, we have done the following:

* created a Question content type
* created a folder to hold all Question items
* tested the “add form” for Questions
* created a default view for Questions that works for anonymous website visitors and users who have edit permission

The next step is to make it possible to track Questions according to whether they have been handled or not. By “handled”, in our example scenario, we mean whether someone has replied to a question.

.. _workflow-states-and-transitions-label-ttw:

Workflow States and Transitions
-------------------------------

