Plone REST API
==============

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <code>`):

    ..  code-block:: console

        git checkout restapi


In this chapter, we will have a look at the relatively new add-on `plone.restapi <https://plonerestapi.readthedocs.io/en/latest/index.html>`_.

It provides a hypermedia API to access Plone content using REST (Representational State Transfer).

We will use :py:mod:`plone.restapi` to develop a small standalone 'single page app' targeted at mobile devices.
We will present our users with a simple list of conference talks.

We add lightning talks as a new type of talk.
Users will be able to submit lightning talks e.g. using their mobile phone.

We have the following tasks:

* create a talk list view
* create a login screen and use JWT for authentication/authorization of requests
* let authenticated users submit lightning talks

Installing plone.restapi
------------------------

We install :py:mod:`plone.restapi` like any other add-on package by adding it to :file:`buildout.cfg` and then activating it in the :guilabel:`Add-ons` panel.
This will automatically add and configure a new PAS plugin named `jwt_auth` used for JSON web token authentication.

Explore the API
---------------

Make sure you add some talks to the talks folder and then start exploring the API.
We recommend using `Postman <https://www.getpostman.com>`_ or a similar tool, but you can also use `requests <https://pypi.python.org/pypi/requests>`_ in a Python virtual env.

:py:mod:`plone.restapi` uses 'content negotiation' to determine whether a client wants
a REST API response - if you set the ``Accept`` HTTP header to ``application/json``,
Plone will provide responses in JSON format. Some requests you could try:

.. code::

    GET /Plone/talks
    Accept: application/json

.. code::

    POST /@login HTTP/1.1
    Accept: application/json
    Content-Type: application/json

    {
        'login': 'admin',
        'password': 'admin',
    }

Exercise
++++++++

REST APIs use HTTP verbs for manipulating content.
``PATCH`` is used to update an existing resource.

Add a new talk in Plone and then update it's title to match 'Foo 42' using the REST API (from Postman or requests).

..  admonition:: Solution
    :class: toggle

    We need to login to change content.
    Using JWT, we do so by POSTing credentials to the ``@login`` resource to obtain a JSON web token
    that we can subsequently use to authorize requests.

    .. code-block:: http-request

       POST /@login HTTP/1.1
       Accept: application/json
       Content-Type: application/json

       {
           'login': 'admin',
           'password': 'admin',
       }

    The response will look like this:

    .. code-block:: http-request

       {
           "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6bnVsbCwic3ViIjoiYWRtaW4iLCJleHAiOjE0NzQ5MTU4Mzh9.s27se99V7leTVTo26N_pbYskebR28W5NS87Fb7zowNk"
       }

    Using the :py:mod:`requests` library from Python, you would do:

    .. code-block:: python

       >>> import requests
       >>> response = requests.post('http://localhost:8080/Plone/@login',
       ...                   headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
       ...                   data='{"login": "admin", "password": "admin"}')
       >>> response.status_code
       200
       >>> response.json()
       {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6bnVsbCwic3ViIjoiYWRtaW4iLCJleHAiOjE0NzQ5MTYyNzR9.zx8XJb6SCWB2taxyibLZ2461ibDloqU3QbWDkDzT8PY'}
       >>>

    Now we can change the talk title:

    .. code-block:: http-request

       PATCH /Plone/talks/example-talk
       Accept: application/json
       Content-Type: application/json
       Authentication: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6bnVsbCwic3ViIjoiYWRtaW4iLCJleHAiOjE0NzQ5MTYyNzR9.zx8XJb6SCWB2taxyibLZ2461ibDloqU3QbWDkDzT8PY

       {
           "@id": "http://localhost:8080/Plone/talks/example-talk",
           "title": "Foo 42"
       }

    Using :py:mod:`requests` again:

    .. code-block:: python

       >>> requests.patch('http://localhost:8080/Plone/talks/example-talk',
       ...                headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6bnVsbCwic3ViIjoiYWRtaW4iLCJleHAiOjE0NzQ5MTYyNzR9.zx8XJb6SCWB2taxyibLZ2461ibDloqU3QbWDkDzT8PY'},
       ...                data='{"@id":"http://localhost:8080/Plone/talks/example-talk", "title":"Foo 42"}')
       <Response [204]>


Implementing the talklist
-------------------------

We will use `Mobile Angular UI <http://mobileangularui.com/>`_ to develop our app.
This is a relatively lightweight JavaScript framework for developing hybrid web apps built on top of `AngularJS <https://angularjs.org/>`_.
There are a lot of other frameworks available (e.g. Ionic, OnsenUI, Sencha, ...),
but most of them have more dependencies than `Mobile Angular UI`.

For example, most of them require NodeJS as a development web server.

Our focus is Plone and interacting with :py:mod:`plone.restapi`, and `Mobile Angular UI` perfectly suits our needs
because it simply lets us use Plone as our development webserver.

To get started, we download the current `master branch of Mobile Angular UI <https://codeload.github.com/mcasimir/mobile-angular-ui/zip/master>`_
from GitHub, extract it and copy the :file:`dist` folder into a new subdirectory of :file:`browser` named :file:`talklist`.

Assuming the current working directory is the buildout directory:

.. code-block:: console

   wget https://codeload.github.com/mcasimir/mobile-angular-ui/zip/master
   unzip master.zip
   mkdir src/ploneconf.site/src/ploneconf/site/browser/talklist
   cp -a mobile-angular-ui-master/dist src/ploneconf.site/src/ploneconf/site/browser/talklist/

Then we add a new resource directory to :file:`browser/configure.zcml`:

.. code-block:: xml

    <browser:resourceDirectory
        name="talklist"
        directory="talklist"
        />

In the :file:`browser/talklist` directory, we add an HTML page called :file:`index.html`:

.. code-block:: html

    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        <base href="/Plone/++resource++talklist/" />
        <title>List Of Talks</title>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="viewport" content="user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimal-ui" />
        <meta name="apple-mobile-web-app-status-bar-style" content="yes" />
        <link rel="shortcut icon" href="/favicon.png" type="image/x-icon" />
        <link rel="stylesheet" href="dist/css/mobile-angular-ui-hover.min.css" />
        <link rel="stylesheet" href="dist/css/mobile-angular-ui-base.min.css" />
        <link rel="stylesheet" href="dist/css/mobile-angular-ui-desktop.min.css" />
      </head>
      <body
        ng-app="TalkListApp"
        ng-controller="MainController"
        >
        <h1>List of talks</h1>
        <div class="app">
          <!-- App Body -->
          <div class="app-body">
            <div class="scrollable-content section">
              <div class="panel-group"
                ui-shared-state="myAccordion"
                ui-default='2'>
                <div class="panel panel-default" ng-repeat="item in items">
                  <div class="panel-heading" ui-set="{'myAccordion': item.pos}">
                    <h4 class="panel-title">
                      {{item.type}}: {{item.title}} by {{item.speaker}}
                    </h4>
                    <b>{{item.start}}</b>
                  </div>
                  <div ui-if="myAccordion == {{item.pos}}">
                    <div class="panel-body">
                      {{item.details}}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div><!-- ~ .app -->
        <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.5.6/angular.min.js"></script>
        <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.5.6/angular-route.min.js"></script>
        <script src="dist/js/mobile-angular-ui.min.js"></script>
        <script src="talklist.js"></script>
      </body>
    </html>

Now you can point your browser to http://localhost:8080/Plone/++resource++talklist/index.html to see the result.

The page will display a list of published talks.

We also need some JavaScript that we put into a file named :file:`talklist.js` in the same folder:

.. code-block:: javascript

    'use strict';

    //
    // module depends on mobile-angular-ui
    //
    var app = angular.module('TalkListApp', [
      'mobile-angular-ui',
    ]);


    app.controller('MainController', function($rootScope, $scope, $http) {

      $scope.items = [];

      $scope.load_talks = function() {
        $http.get('/Plone/talks',
                  {headers:{'Accept':'application/json'}}).
          success(function(data, status, headers, config) {
            $scope.items = [];
            // get the paths of the talks
            var paths = [];
            for (var i=0; i < data.items_total; i++) {
              paths.push(data.items[i]['@id'])
            }
            // next get details for each talk
            for (var i=0; i < paths.length; i++) {
              $http.get(paths[i],
                        {headers:{'Accept':'application/json'}}).
                success(function(talkdata, status, headers, config) {
                  // this is an angular 'promise' - we cannot
                  // rely on variables from an outer scope
                  var path = talkdata['@id'];
                  var talk = {
                    'pos': paths.indexOf(path),
                    'path': path,
                    'title': talkdata.title,
                    'type': talkdata.type_of_talk,
                    'speaker': (talkdata.speaker != null) ? talkdata.speaker : talkdata.creators[0],
                    'start': talkdata.start,
                    'subjects': talkdata.subjects,
                    'details': (talkdata.details != null) ? talkdata.details.data : talkdata.description
                  }
                  $scope.items.push(talk);

                }).
                error(function(talkdata, status, headers, config) {});
            }
          }).
        error(function(data, status, headers, config) {
          $scope.items = [];
        });
      };

      // initialize
      $scope.load_talks();
    });


Submit lightning talks
----------------------

We add a new type of talk: lightning talk.
A lightning talk is a short presentation of up to 5 minutes duration that can cover just about any topic.

The information we need to provide for lightning talks is far less than for the more formal types of talk.

Often the information provided for lightning talks is restricted to the talk subject or title and the speaker name, but we allow for a short summary.

Before they can submit a lightning talk, potential speakers will need to login
and we will use their previously registered login name as the speaker's name to display in the talk list.

Before we can start to submit lightning talks using REST calls from our single page app, we have to adapt the talk schema:

.. code-block:: xml
   :linenos:
   :emphasize-lines: 18, 25, 52, 57

    <?xml version="1.0" encoding="UTF-8"?>
    <model xmlns="http://namespaces.plone.org/supermodel/schema"
       xmlns:form="http://namespaces.plone.org/supermodel/form"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n"
       xmlns:lingua="http://namespaces.plone.org/supermodel/lingua"
       xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
       xmlns:security="http://namespaces.plone.org/supermodel/security"
       xmlns:users="http://namespaces.plone.org/supermodel/users">
      <schema>
        <field name="type_of_talk" type="zope.schema.Choice"
          form:widget="z3c.form.browser.radio.RadioFieldWidget">
          <description />
          <title>Type of talk</title>
          <values>
            <element>Talk</element>
            <element>Training</element>
            <element>Keynote</element>
            <element>Lightning Talk</element>
          </values>
        </field>
        <field name="details" type="plone.app.textfield.RichText">
          <description>Add a short description of the talk (max. 2000 characters)</description>
          <max_length>2000</max_length>
          <title>Details</title>
          <required>False</required>
        </field>
        <field name="audience"
          type="zope.schema.Set"
          form:widget="z3c.form.browser.checkbox.CheckBoxFieldWidget">
          <description />
          <title>Audience</title>
          <value_type type="zope.schema.Choice">
            <values>
              <element>Beginner</element>
              <element>Advanced</element>
              <element>Professionals</element>
            </values>
          </value_type>
        </field>
        <field name="room"
          type="zope.schema.Choice"
          form:widget="z3c.form.browser.radio.RadioFieldWidget"
          security:write-permission="cmf.ReviewPortalContent">
          <description></description>
          <required>False</required>
          <title>Room</title>
          <vocabulary>ploneconf.site.vocabularies.Rooms</vocabulary>
        </field>
        <field name="speaker" type="zope.schema.TextLine">
          <description>Name (or names) of the speaker</description>
          <title>Speaker</title>
          <required>False</required>
        </field>
        <field name="email" type="plone.schema.email.Email">
          <description>Adress of the speaker</description>
          <title>Email</title>
          <required>False</required>
        </field>
        <field name="image" type="plone.namedfile.field.NamedBlobImage">
          <description />
          <required>False</required>
          <title>Image</title>
        </field>
        <field name="speaker_biography" type="plone.app.textfield.RichText">
          <description />
          <max_length>1000</max_length>
          <required>False</required>
          <title>Speaker Biography</title>
        </field>
      </schema>
    </model>

Next, in our JavaScript code, we provide a method for logging in a user and another one to check whether the user has a valid JSON web token.
We use the ``localStorage`` facility of the browser to store the token on the client.

.. code-block:: javascript

    ...
    app.controller('MainController', function($rootScope, $scope, $http) {
    ...
      $scope.login = function(login, passwd) {
        $http.post('/Plone/@login',
                  {'login':login,
                   'password':passwd},
                  {headers:
                   {'Content-type':'application/json',
                    'Accept':'application/json'}}).
          success(function(data, status, headers, config){
            localStorage.setItem('jwtoken', data.token);
          }).
          error(function(data, status, headers, config){
            alert('Could not log you in');
          });
      };

      $scope.is_logged_in = function() {
        // we assume the user is logged in when he has a JWT token (that is naive)
        return localStorage.getItem('jwtoken') != null;
      };
    ...

We continue with changes to :file:`index.html` so that it uses the new methods.
We provide a login form if the user doesn't have a valid JSON web token.

Only authenticated users can see the rest of the page.

.. code-block:: html
   :emphasize-lines: 4-30

          <div class="app-body">

            <div class="scrollable">
              <div class="scrollable-content section" ng-if="! is_logged_in()">
                <form role="form" ng-submit='login(userid,passwd)'>
                  <fieldset>
                    <legend>Login</legend>
                    <div class="form-group has-success has-feedback">
                      <label>Login</label>
                      <input type="text"
                        ng-model="userid"
                        class="form-control"
                        placeholder="Enter login">
                    </div>
                    <div class="form-group">
                      <label>Password</label>
                      <input type="password"
                        ng-model="passwd"
                        class="form-control"
                        placeholder="Password">
                    </div>
                  </fieldset>
                  <hr>
                  <button class="btn btn-primary btn-block">
                    Login
                  </button>
                </form>
              </div>

              <div class="scrollable-content section" ng-if="is_logged_in()">
                <div class="panel-group"

Last we have to add some code that allows authenticated users to submit a lightning talk. We add another JavaScript method first:

.. code-block:: javascript

    ...
    app.controller('MainController', function($rootScope, $scope, $http) {
    ...
      $scope.submit_talk = function(subject, summary) {
        $http.post('/Plone/talks',
                   {'@type':'talk',
                    'type_of_talk':'Lightning Talk',
                    'audience':['Beginner','Advanced','Professionals'],
                    'title':subject,
                    'description':summary},
                   {headers:
                    {'Content-type':'application/json',
                     'Authorization': 'Bearer ' + localStorage.getItem('jwtoken'),
                     'Accept':'application/json'}}).
          success(function(data, status, headers, config){
            if(status==201) { // created
              $scope.load_talks();
            }
          }).
          error(function(data, status, headers, config){
            // according to docs, status can be 400 or 500
            // we check wether the token has expired - in this case,
            // we remove it from localStorage and disply the login page.
            // In all other cases, we display the message received
            // from Plone
            if ( (status == 400) && (data.type == 'ExpiredSignatureError') ) {
              localStorage.removeItem('jwtoken');
              location.reload();
            } else {
              // reason/error msg is contained in response body
              alert(data.message);
            }
          });
      };
    ...

Exercise
---------

Rewrite the ``load_talks()`` JavaScript method that it uses the portal search instead of ``/Plone/talks``.
Sort the list by date.

..  admonition:: Solution
    :class: toggle

    .. code-block:: javascript
       :emphasize-lines: 3

       ...
       $scope.load_talks = function() {
         $http.get('/Plone/@search?portal_type=talk&sort_on=Date',
                   {headers:{'Accept':'application/json'}}).
           success(function(data, status, headers, config) {
       ...
         });
