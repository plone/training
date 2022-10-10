---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(viewlets2-label)=

# A Viewlet for the Votable Behavior

````{sidebar} Plone Classic UI Chapter
```{figure} _static/plone-training-logo-for-classicui.svg
:alt: Plone Classic UI
:class: logo
```

Solve the same tasks in the React frontend in chapter {doc}`volto_actions`

---

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout user_generated_content
```

Code for the end of this chapter:

```shell
git checkout resources
```
````

(viewlets2-voting-label)=

## Voting Viewlet

In this part you will:

- Write the viewlet template
- Add jQuery include statements

Topics covered:

- Viewlets
- JavaScript inclusion

```{only} not presentation
Earlier we added the logic that saves votes on the objects. We now create the user interface for it.

Since we want to use the UI on more than one page (not only the talk view but also the talk listing) we need to put it somewhere.

- To handle the user input we don't use a form but links and ajax.
- The voting itself is a fact handled by another view
```


```{figure} _static/voting_viewlet.png
:align: center
```

We register the viewlet in {file}`browser/configure.zcml`.

```{code-block} xml
:emphasize-lines: 6-14
:linenos:

 <configure xmlns="http://namespaces.zope.org/zope"
     xmlns:browser="http://namespaces.zope.org/browser">

     ...

   <browser:viewlet
     name="voting"
     for="starzel.votable_behavior.interfaces.IVoting"
     manager="plone.app.layout.viewlets.interfaces.IBelowContentTitle"
     layer="..interfaces.IVotableLayer"
     class=".viewlets.Vote"
     template="templates/voting_viewlet.pt"
     permission="zope2.View"
     />

     ....

 </configure>
```

We extend the file {file}`browser/viewlets.py`

```{code-block} python
:linenos:

from plone.app.layout.viewlets import common as base


class Vote(base.ViewletBase):
    pass
```

```{only} not presentation
This will add a viewlet to a slot below the title and expect a template {file}`voting_viewlet.pt` in a folder {file}`browser/templates`.
```

Let's create the file {file}`browser/templates/voting_viewlet.pt` without any logic

```{code-block} html
:linenos:

 <div class="voting">
     Wanna vote? Write code!
 </div>

 <script type="text/javascript">
   jq(document).ready(function(){
     // please add some jQuery-magic
   });
 </script>
```

- restart Plone
- show the viewlet

(viewlets2-code-label)=

## Writing the Viewlet code

```{only} manual
Now that we have the everything in place, we can add the Logic
```

Update the viewlet to contain the necessary logic in {file}`browser/viewlets.py`

```{code-block} python
:linenos:

from plone.app.layout.viewlets import common as base
from Products.CMFCore.permissions import ViewManagementScreens
from Products.CMFCore.utils import getToolByName

from starzel.votable_behavior.interfaces import IVoting


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
```

(viewlets2-template-label)=

## The template

And extend the template in {file}`browser/templates/voting_viewlet.pt`

```{code-block} html
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
      Delete all votes
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
```

```{only} not presentation
We have many small parts, most of which will be hidden by JavaScript unless needed.
By providing all this status information in HTML, we can use standard translation tools to translate.

Translating strings in JavaScript requires extra work.
```

We need some css that we store in {file}`static/starzel_votablebehavior.css`

```{code-block} css
:linenos:

.voting {
    float: right;
    border: 1px solid #ddd;
    background-color: #DDDDDD;
    padding: 0.5em 1em;
}

.voting .voting_option {
    display: none;
}

.areyousure {
    display: none;
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
```

(viewlets2-js-label)=

## JavaScript code

To make it work in the browser, some JavaScript {file}`static/starzel_votablebehavior.js`

```{code-block} js
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
```

```{only} not presentation
This js code adheres to crockfort jshint rules, so all variables are declared at the beginning of the method.
We show and hide quite a few small HTML elements here.
```

(viewlets2-helpers-label)=

## Writing 2 simple view helpers

`````{only} not presentation
Our JavaScript code communicates with our site by calling views that don't exist yet.
These Views do not need to render HTML, but should return a valid status.
Exceptions set the right status and aren't being shown by JavaScript, so this will suit us fine.

As you might remember, the {samp}`vote` method might return an exception, if somebody votes twice.
We do not catch this exception. The user will never see this exception.

````{seealso}
Catching exceptions contain a gotcha for new developers.

```{code-block} python
:linenos:

try:
    something()
except:
    fix_something()
```

Zope claims some exceptions for itself.
It needs them to work correctly.

For example, if two requests try to modify something at the same time, one request will throw an exception, a {samp}`ConflictError`.

Zope catches the exception, waits for a random amount of time, and tries to process the request again, up to three times.
If you catch that exception, you are in trouble, so don't do that. Ever.
````
`````

As so often, we must extend {file}`browser/configure.zcml`:

```{code-block} xml
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
```

Then we add our simple views into the file {file}`browser/vote.py`

```{code-block} python
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
```

A lot of moving parts have been created. Here is a small overview:

```{figure} ../_static/voting_flowchart.png
:align: center
```
