Writing Viewlets
=================

A viewlet is no view but a snippet of html and logic that can be put somewhere in the site.

* show ``/@@manage-viewlets``
* we already customized a viewlet (``collophon.pt``), now we add a new one
* viewlets don't save data (portlets do)

social-viewlet
--------------

We add a new folder ``viewlets`` with an empty ``__init__.py``. This time we don't need a ``configure.zcml`` and don't need to register the folder in our eggs configure.zcml since we use ``grok`` to do that for us.

We just add a file viewlets.py containing the viewlet-class::

    # encoding=utf-8
    from five import grok
    from plone.app.layout.viewlets import interfaces as viewletIFs
    from zope.component import Interface


    class Social(grok.Viewlet):
        grok.context(Interface)
        grok.viewletmanager(viewletIFs.IBelowContentTitle)

This will add a viewlet to a slot below the title and expect a template ``social.pt`` in a folder ``viewlets_templates``.

Let's add it:

.. code-block:: html

    <div id="social-links">
        <a href="#"
           class="lanyrd-link"
           tal:define="link viewlet/lanyrd_link | nothing"
           tal:condition="link"
           tal:attributes="href link">
            See this talk on Lanyrd!
        </a>
    </div>

So now let's add some logic to the viewlet-class so that ``viewlet/lanyrd_link`` does returns the link::

    from five import grok
    from plone.app.layout.viewlets import interfaces as viewletIFs
    from plonekonf.talk.behavior.social import ISocial


    class Social(grok.Viewlet):
        grok.context(ISocial)
        grok.viewletmanager(viewletIFs.IBelowContentTitle)

        def lanyrd_link(self):
            adapted = ISocial(self.context)
            return adapted.lanyrd

TAG: 17_SOCIAL_VIEWLET

* We registered the viewlet to content that have the ISocial Interface.
* we adapt the object to it's behavior to be able to access the fields of the behavior
* we return the link

voting-viewlet
----------------

* Viewlet for IVoteable
* the viewlet-template
* add jquery include statements
* saving the vote on the object using annotations (Patrick)

We just added the logic that saves votes on the objects. Now let's add the user-interface to it.

Since we want to use the UI on more than one page (not only the talk-view but also the talk-listing) we need to put it somewhere.

* To handle the user-input we don't use a form but links and ajax.
* The voting itself is an fact handles by another view

We create a new file voting.py::

    # encoding=utf-8
    from five import grok
    from plone.app.layout.viewlets import interfaces as viewletIFs
    from zope.component import Interface


    class Vote(grok.Viewlet):
        grok.context(Interface)
        grok.viewletmanager(viewletIFs.IBelowContentTitle)

This will add a viewlet to a slot below the title and expect a template vote.pt in a folder 'voting_templates'.

Let's create this file without any logic

.. code-block:: html

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

writing the viewlet-class
-------------------------

Lets see the final code::

    # encoding=utf-8
    from Products.CMFCore.utils import getToolByName
    from Products.CMFDefault.permissions import ViewManagementScreens
    from five import grok
    from plone.app.layout.viewlets import interfaces as viewletIFs
    from plonekonf.talk.interfaces import IVotable, IVoting


    class Vote(grok.Viewlet):
        grok.context(IVotable)
        grok.viewletmanager(viewletIFs.IBelowContentTitle)

        @property
        def _vote(self):
            return IVoting(self.context)

        @property
        def voted(self):
            return self._vote.already_voted(self.request)

        @property
        def average(self):
            return self._vote.average_vote()

        @property
        def is_manager(self):
            membership_tool = getToolByName(self.context, 'portal_membership')
            return membership_tool.checkPermission(ViewManagementScreens,
                                                   self.context)

        @property
        def has_votes(self):
            return self._vote.has_votes()

* we changed the code so that only content that has the interface 'IVotable' get's the viewlet.
* _vote returns the context object adapted to the Behavior that adds the vote-functionality. This way we can access all methods that are in IVoting.
* voted, average and has_votes do exactly this and return the result of the methods we wrote in IVoting.
* is_manager checks if we are managers so only managers can reset the existing votes. To do this we check if the current user can 'ViewManagementScreens'.


the template
------------

the final temoplate looks like this:

.. code-block:: html

    <div class="voting">
      <div id="current_rating" tal:condition="viewlet/has_votes">
        Average rating: <span tal:content="viewlet/average">200</span>
      </div>
      <div id="alreadyvoted" class="voting_option">
        You already rated this voted for this talk!
      </div>
      <div id="notyetvoted" class="voting_option">
        Vote for this talk: <div class="votes"><span id="voting_plus">+1</span> <span id="voting_neutral">0</span> <span id="voting_negative">-1</span></div>
      </div>
      <div id="no_ratings" tal:condition="not: viewlet/has_votes">
        Be the first one to vote on this talk!
      </div>

      <tal:reset tal:condition="viewlet/is_manager">
        <div id="delete_votings">
          Delete all votings
        </div>
        <div id="delete_votings2" class="areyousure warning">
          Are you sure?
        </div>
      </tal:reset>

      <a href="#" class="hiddenStructure" id="context_url"
         tal:attributes="href context/absolute_url"></a>
      <span id="voted" tal:condition="viewlet/voted" />
    </div>

    <script type="text/javascript">
      jq(document).ready(function(){
        plonekonf.init_voting_viewlet(jq(".voting"));
      });
    </script>

* many small parts, most of which will be hidden by javascript unless needed.
* we use the methods the class provides
* some standard-code to initialize our js-code

The css for the template:

.. code-block:: css

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


The javascript code (Patrick)
-----------------------------

.. code-block:: js

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

Zunächst fragen wir den Marker ab, der anzeigt, ob der aktuelle
Benutzer schon abgestimmt hat. Abhängig davon zeigen bieten wir die
Abstimmungsmöglichkeit ab.

Danach schreiben wir die Funktion, welche die Stimme abgibt.
Wir sind schreibfaul, deswegen schreiben wir eine Funktion, die eine
Funktion zurückgibt.

Danach setzen wir für die einzelnen Abstimmungsmöglichkeiten, einen
Clickhandler

Wie funktioniert das? Wir rufen vote auf, die liefert eine Methode
zurück. Als Clickhandler speichert man normalerweise immer eine
Methode. Wenn nun jemand auf einen der Texte klickt, wir die Methode
inner_vote aufgerufen. Innerhalb der inner_vote Methode können wir
noch immer die gültige rating Variable aufrufen, die wir mit vote
übergeben haben. Die Methode die also als clickhandler für
#voting_plus aufgerufen wurde, sieht eine 1 wenn sie rating abfragt,
#voting_neutral sieht die 0 und so weiter.

Dann rufen wir die Methode post aus jquery auf, als ersten Parameter
suchen wir uns aus dem html die context_url die wir dort versteckt
haben, als Post Parameter übergeben wir das Rating, und zum Schluss
kommt die Methode, welche nach erfolgreichem Request aufgerufen
wird, und die Seite neu lädt.

Danach schreiben wir noch die Handler um per Two Step Verfahren die
Stimmen löschen zu können.

Jetzt müssen wir noch die Methoden schreiben, die per HTTP Post
aufgerufen werden.


2 Simpleviews schreiben (Patrick)
---------------------------------

Diese Views haben IVotable als Context, es gibt sie also nur auf
Objekten welche Votable sind.

ClearVotes ist nochmal mit der Management Permission geschützt. Ein
Hacker der den Javascript code von eben analysiert, könnte das
Löschen manuell antriggern, dadurch, das der View durch eine
Managementpermission geschützt ist, kann er keinen Schaden
anrichten. Ansonsten rufen diese Views nur Methoden des Behaviors
auf.



