A viewlet for the voteable behavior
===================================


Voting Viewlet
--------------

* Viewlet for IVoteable
* the viewlet-template
* add jquery include statements
* saving the vote on the object using annotations


.. only:: manual

    Earlier we added the logic that saves votes on the objects. We now create the user interface for it.

    Since we want to use the UI on more than one page (not only the talk-view but also the talk-listing) we need to put it somewhere.

    * To handle the user-input we don't use a form but links and ajax.
    * The voting itself is a fact handled by another view

We register the viewlet in :file:`browser/configure.zcml`.

.. code-block:: xml
   :linenos:
   :emphasize-lines: 6-14

    <configure xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser">

        ...

      <browser:viewlet
        name="voting"
        for="starzel.votable_behavior.interfaces.IVoting"
        manager="plone.app.layout.viewlets.interfaces.IBelowContentTitle"
        layer="..interfaces.IVotableLayer"
        class=".viewlets.Voting"
        template="templates/voting_viewlet.pt"
        permission="zope2.View"
        />

        ....

    </configure>

We extend the file :file:`browser/viewlets.py`

.. code-block:: python
    :linenos:

    from plone.app.layout.viewlets import common as base


    class Vote(base.ViewletBase):
        pass

.. only:: manual

    This will add a viewlet to a slot below the title and expect a template :file:`voting_viewlet.pt` in a folder :file:`browser/templates`.

Let's create the file :file:`browser/templates/voting_viewlet.pt` without any logic

.. code-block:: html
   :linenos:

    <div class="voting">
        Wanna vote? Write code!
    </div>

    <script type="text/javascript">
      jq(document).ready(function(){
        // please add some jQuery-magic
      });
    </script>

* restart Plone
* show the viewlet

Writing the Viewlet code
------------------------

.. only:: mannual

    Now that we have the everything in place, we can add the Logic

Update the viewlet to contain the necessary logic in :file:`browser/viewlets`

.. code-block:: python
    :linenos:

    from plone.app.layout.viewlets import common as base
    from Products.CMFCore.permissions import ViewManagementScreens
    from Products.CMFCore.utils import getToolByName

    from starzel.votable_behavior.interfaces IVoting


    class Vote(base.ViewletBase):

        vote = None
        is_manager = None

        def update(self):
            super(Vote, self).update()

            if self.vote is None:
                self.vote = IVoting(self.context)
            if self.is_manager is None:
                membership_tool = getToolByName(self.context, 'portal_membership')
                self.is_manager = membership_tool.checkPermission(
                    ViewManagementScreens, self.context)

        def voted(self):
            return self.vote.already_voted(self.request)

        def average(self):
            return self.vote.average_vote()

        def has_votes(self):
            return self.vote.has_votes()


The template
------------

And extend the template in :file:`browser/templates/voting_viewlet.pt`

.. code-block:: html
    :linenos:

    <tal:snippet omit-tag="">
      <div class="voting">
        <div id="current_rating" tal:condition="viewlet/has_votes">
          The average vote for this talk is <span tal:content="viewlet/average">200</span>
        </div>
        <div id="alreadyvoted" class="voting_option">
          You already voted this talk. Thank you!
        </div>
        <div id="notyetvoted" class="voting_option">
          What do you think of this talk?
          <div class="votes"><span id="voting_plus">+1</span> <span id="voting_neutral">0</span> <span id="voting_negative">-1</span>
          </div>
        </div>
        <div id="no_ratings" tal:condition="not: viewlet/has_votes">
          This talk has not been voted yet. Be the first!
        </div>
        <div id="delete_votings" tal:condition="viewlet/is_manager">
          Delete all votings
        </div>
        <div id="delete_votings2" class="areyousure warning"
             tal:condition="viewlet/is_manager"
             >
          Are you sure?
        </div>
        <a href="#" class="hiddenStructure" id="context_url"
           tal:attributes="href context/absolute_url"></a>
        <span id="voted" tal:condition="viewlet/voted"></span>
      </div>
      <script type="text/javascript">
        $(document).ready(function(){
          starzel_votablebehavior.init_voting_viewlet($(".voting"));
        });
      </script>
    </tal:snippet>

.. only:: manual

    We have many small parts, most of which will be hidden by javascript unless needed.
    By providing all these status information in HTML, we can use standard translation tools to translate. Translating strings in javascript requires extra work.

We need some css that we store in :file:`static/starzel_votablebehavior.css`

.. code-block:: css
    :linenos:

    .voting {
        float: right;
        border: 1px solid #ddd;
        background-color: #DDDDDD;
        padding: 0.5em 1em;
    }

    .voting .voting_option {
        display: None;
    }

    .areyousure {
        display: None;
    }

    .voting div.votes span {
        border: 0 solid #DDDDDD;
        cursor: pointer;
        float: left;
        margin: 0 0.2em;
        padding: 0 0.5em;
    }

    .votes {
        display: inline;
        float: right;
    }

    .voting #voting_plus {
        background-color: LimeGreen;
    }

    .voting #voting_neutral {
        background-color: yellow;
    }

    .voting #voting_negative {
        background-color: red;
    }


The javascript code
-------------------

To make it work in the browser, some javascript :file:`static/starzel_votablebehavior.js`

.. code-block:: js
    :linenos:

    /*global location: false, window: false, jQuery: false */
    (function ($, starzel_votablebehavior) {
        "use strict";
        starzel_votablebehavior.init_voting_viewlet = function (context) {
            var notyetvoted = context.find("#notyetvoted"),
                alreadyvoted = context.find("#alreadyvoted"),
                delete_votings = context.find("#delete_votings"),
                delete_votings2 = context.find("#delete_votings2");

            if (context.find("#voted").length !== 0) {
                alreadyvoted.show();
            } else {
                notyetvoted.show();
            }

            function vote(rating) {
                return function inner_vote() {
                    $.post(context.find("#context_url").attr('href') + '/vote', {
                        rating: rating
                    }, function () {
                        location.reload();
                    });
                };
            }

            context.find("#voting_plus").click(vote(1));
            context.find("#voting_neutral").click(vote(0));
            context.find("#voting_negative").click(vote(-1));

            delete_votings.click(function () {
                delete_votings2.toggle();
            });
            delete_votings2.click(function () {
                $.post(context.find("#context_url").attr("href") + "/clearvotes", function () {
                    location.reload();
                });
            });
        };
    }(jQuery, window.starzel_votablebehavior = window.starzel_votablebehavior || {}));

.. only:: manual

    This js-code adheres to crockfort jshint rules, so all variables are declared at the beginning of the method.
    We show and hide quite a few small html elements here


Writing 2 simple view helpers
-----------------------------

.. only:: manual

    Our javascript code communicates with our site by calling views that don't exist yet.
    These Views do not need to render html, but should return a valid status.
    Exceptions set the right status and aren't being shown by javascript, so this will suit us fine.

    As you might remember, the :samp:`vote` method might return an exception, if somebody votes twice.
    We do not catch this exception. The user will never see this exception.

    .. seealso::

        Catching exceptions contain a gotcha for new developers.

        .. code-block:: python
            :linenos:

            try:
                something()
            except:
                fix_something()

        Zope claims some exceptions for themselves. It needs them to work correctly.

        For example, if two requests try to modify something at the same time, one request will throw an exception, a :samp:`ConflictError`.

        Zope catches the exception, waits for a random amount of time, and tries to process the request again, up to three times.
        If you catch that exception, you are in trouble, so don't do that. Ever.

As so often, we must extend :file:`browser/configure.zcml`:

.. code-block:: xml
    :linenos:

    ...

    <browser:page
      name="vote"
      for="starzel.votable_behavior.interfaces.IVotable"
      layer="..interfaces.IVotableLayer"
      class=".vote.Vote"
      permission="zope2.View"
      />

    <browser:page
      name="clearvotes"
      for="starzel.votable_behavior.interfaces.IVotable"
      layer="..interfaces.IVotableLayer"
      class=".vote.ClearVotes"
      permission="zope2.ViewManagementScreens"
      />

    ...

Then we add our simple views into the file :file:`browser/vote.py`

.. code-block:: python
    :linenos:

    from zope.publisher.browser import BrowserPage

    from starzel.votable_behavior.interfaces import IVoting


    class Vote(BrowserPage):

        def __call__(self, rating):
            voting = IVoting(self.context)
            voting.vote(rating, self.request)
            return "success"


    class ClearVotes(BrowserPage):

        def __call__(self):
            voting = IVoting(self.context)
            voting.clear()
            return "success"

A lot of moving parts have been created. Here is a small overview:

.. digraph:: composition

    rankdir=LR;
    layout=fdp;
    context[label="IVotable object" shape="box" pos="0,0!"];
    viewlet[label="Voting Viewlet" pos="3,-1!"];
    helperview1[label="Helper View for Voting" pos="3,0!"];
    helperview2[label="Helper View for deleting all votes" pos="3,1!"];
    js[label="JS Code" shape="box" pos="6,0!"];
    viewlet -> context [headlabel="reads" labeldistance="3"]
    helperview1 -> context [label="modifies"]
    helperview2 -> context [label="modifies"]
    js -> helperview1 [label="calls"]
    js -> helperview2 [taillabel="calls" labelangle="-10" labeldistance="6"]
    viewlet -> js [label="loads"]
    js -> viewlet [headlabel="manipulates" labeldistance="8" labelangle="-10"]

