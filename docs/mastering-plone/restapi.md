---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Using plone.restapi without Volto

````{sidebar} Plone Backend Chapter
```{figure} _static/plone-training-logo-for-backend.svg
:alt: Plone backend
:class: logo
```

Get the code for this chapter ({doc}`More info <code>`):

```shell
git checkout restapi
```
````

In this chapter, we will use {doc}`plone6docs:plone.restapi/docs/source/index`, to iteract with the backend without using Volto.

It provides a hypermedia API to access Plone content using REST (Representational State Transfer).

We will use {py:mod}`plone.restapi` to develop a small standalone 'single page app' targeted at mobile devices.
We will present our users with a simple list of conference talks.

We add lightning talks as a new type of talk.
Users will be able to submit lightning talks e.g. using their mobile phone.

We have the following tasks:

- create a talk list view
- create a login screen and use JWT for authentication/authorization of requests
- let authenticated users submit lightning talks

## Installing plone.restapi

We install {py:mod}`plone.restapi` like any other add-on package by adding it to {file}`buildout.cfg` and then activating it in the {guilabel}`Add-ons` panel.
This will automatically add and configure a new PAS plugin named `jwt_auth` used for JSON web token authentication.

## Explore the API

Make sure you add some talks to the talks folder and then start exploring the API.
We recommend using [Postman](https://www.postman.com) or a similar tool, but you can also use [requests](https://pypi.org/project/requests) in a Python virtual env.

{py:mod}`plone.restapi` uses 'content negotiation' to determine whether a client wants
a REST API response - if you set the `Accept` HTTP header to `application/json`,
Plone will provide responses in JSON format. Some requests you could try:

```http
GET /Plone/talks HTTP/1.1
Accept: application/json
```

```http
POST /@login HTTP/1.1
Accept: application/json
Content-Type: application/json

{
    "login": "admin",
    "password": "admin"
}
```

### Exercise

REST APIs use HTTP verbs for manipulating content.
`PATCH` is used to update an existing resource.

Add a new talk in Plone and then update it's title to match 'Foo 42' using the REST API (from Postman or requests).

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

We need to login to change content.
Using JWT, we do so by POSTing credentials to the `@login` resource to obtain a JSON web token
that we can subsequently use to authorize requests.

```http
POST /@login HTTP/1.1
Accept: application/json
Content-Type: application/json

{
    "login": "admin",
    "password": "admin"
}
```

The response will look like this:

```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6bnVsbCwic3ViIjoiYWRtaW4iLCJleHAiOjE0NzQ5MTU4Mzh9.s27se99V7leTVTo26N_pbYskebR28W5NS87Fb7zowNk"
}
```

Using the {py:mod}`requests` library from Python, you would do:

```python
>>> import requests
>>> response = requests.post('http://localhost:8080/Plone/@login',
...                   headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
...                   data='{"login": "admin", "password": "admin"}')
>>> response.status_code
200
>>> response.json()
{'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6bnVsbCwic3ViIjoiYWRtaW4iLCJleHAiOjE0NzQ5MTYyNzR9.zx8XJb6SCWB2taxyibLZ2461ibDloqU3QbWDkDzT8PY'}
>>>
```

Now we can change the talk title:

```http
PATCH /Plone/talks/example-talk HTTP/1.1
Accept: application/json
Content-Type: application/json
Authentication: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6bnVsbCwic3ViIjoiYWRtaW4iLCJleHAiOjE0NzQ5MTYyNzR9.zx8XJb6SCWB2taxyibLZ2461ibDloqU3QbWDkDzT8PY

{
    "@id": "http://localhost:8080/Plone/talks/example-talk",
    "title": "Foo 42"
}
```

Using {py:mod}`requests` again:

```python
>>> requests.patch('http://localhost:8080/Plone/talks/example-talk',
...                headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6bnVsbCwic3ViIjoiYWRtaW4iLCJleHAiOjE0NzQ5MTYyNzR9.zx8XJb6SCWB2taxyibLZ2461ibDloqU3QbWDkDzT8PY'},
...                data='{"@id":"http://localhost:8080/Plone/talks/example-talk", "title":"Foo 42"}')
<Response [204]>
```
````

## Implementing the talklist

We will use [Vue.js](https://vuejs.org/) to develop our app.
This is a relatively lightweight JavaScript framework for developing hybrid web apps.
A big advantage of Vue.js over other frameworks for our purpose is that it doesn't require
NodeJS..

Our focus is Plone and interacting with {py:mod}`plone.restapi`, and `Vue.js` perfectly suits our needs
because it simply lets us use Plone as our development webserver.

To get started, we create a new subdirectory of {file}`browser` named {file}`talklist`.

Assuming the current working directory is the buildout directory:

```shell
mkdir src/ploneconf.site/src/ploneconf/site/browser/talklist
```

Then we add a new resource directory to {file}`browser/configure.zcml`:

```xml
<browser:resourceDirectory
    name="talklist"
    directory="talklist"
    />
```

In the {file}`browser/talklist` directory, we add an HTML page called {file}`index.html`:

```html
<!DOCTYPE html>
<html
  xmlns:v-on="https://vuejs.org/"
  xmlns:="https://vuejs.org/">
  <head>
    <meta charset="utf-8" />
    <base href="/Plone/++resource++talklist/" />
    <title>List Of Talks</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="viewport" content="user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimal-ui" />
    <meta name="apple-mobile-web-app-status-bar-style" content="yes" />
    <link rel="shortcut icon" href="/favicon.png" type="image/x-icon" />
    <!-- Load required Bootstrap and BootstrapVue CSS -->
    <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap/dist/css/bootstrap.min.css" />
    <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap-vue@latest/dist/bootstrap-vue.min.css" />
  </head>

  <body>

    <h1>List of talks</h1>

    <div id="talklist">

      <div role="tablist">
        <b-card no-body class="mb-1" v-for="(item, index) in items">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button block href="#" v-b-toggle="'accordion-' + index" variant="info">{{ item.type }}: {{ item.title }} by {{ item.speaker }}</b-button>
          </b-card-header>
          <b-collapse :id="'accordion-' + index" accordion="talklist-accordion" role="tabpanel">
            <b-card-body>
              <b-card-text>{{item.details}}</b-card-text>
            </b-card-body>
          </b-collapse>
        </b-card>
      </div>

    </div>
    <!-- Load polyfills to support older browsers -->
    <script src="//polyfill.io/v3/polyfill.min.js?features=es2015%2CMutationObserver" crossorigin="anonymous"></script>

    <!-- Load Vue followed by BootstrapVue -->
    <script src="//unpkg.com/vue@latest/dist/vue.min.js"></script>
    <script src="//unpkg.com/bootstrap-vue@latest/dist/bootstrap-vue.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vue-resource@1.5.1"></script>
    <script src="talklist.js"></script>
  </body>
</html>
```

Now you can point your browser to <http://localhost:8080/Plone/++resource++talklist/index.html> to see the result.

The page will display a list of published talks.

We also need some JavaScript that we put into a file named {file}`talklist.js` in the same folder:

```javascript
"use strict";

var app = new Vue({
  el: "#talklist",
  data: {
    items: [],
    userid: "",
    passwd: "",
    subject: "",
    summary: "",
  },

  methods: {
    load_talks: function () {
      this.$http
        .get("/Plone/talks", { headers: { Accept: "application/json" } })
        .then(
          function (response) {
            this.items = [];
            // get the paths of the talks
            var paths = [];
            for (var i = 0; i < response.data.items_total; i++) {
              paths.push(response.data.items[i]["@id"]);
            }
            // next get details for each talk
            for (var i = 0; i < paths.length; i++) {
              this.$http
                .get(paths[i], { headers: { Accept: "application/json" } })
                .then(
                  function (resp) {
                    var talkdata = resp.data;
                    var path = talkdata["@id"];
                    var talk = {
                      pos: paths.indexOf(path),
                      path: path,
                      title: talkdata.title,
                      type: talkdata.type_of_talk,
                      speaker:
                        talkdata.speaker != null
                          ? talkdata.speaker
                          : talkdata.creators[0],
                      start: talkdata.start,
                      subjects: talkdata.subjects,
                      details:
                        talkdata.details != null
                          ? talkdata.details.data
                          : talkdata.description,
                    };
                    this.items.push(talk);
                  },
                  function (error) {}
                );
            }
          },
          function (error) {
            this.items = [];
          }
        );
    },
  },

  mounted: function () {
    // initialize
    this.load_talks();
  },
});
```

## Submit lightning talks

We add a new type of talk: lightning talk.
A lightning talk is a short presentation of up to 5 minutes duration that can cover just about any topic.

The information we need to provide for lightning talks is far less than for the more formal types of talk.

Often the information provided for lightning talks is restricted to the talk subject or title and the speaker name, but we allow for a short summary.

Before they can submit a lightning talk, potential speakers will need to login
and we will use their previously registered login name as the speaker's name to display in the talk list.

Before we can start to submit lightning talks using REST calls from our single page app, we have to adapt the talk schema:

```{code-block} xml
:emphasize-lines: 18, 25, 52, 57
:linenos:

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
           <element>Professional</element>
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
```

Next, in our JavaScript code, we provide a method for logging in a user and another one to check whether the user has a valid JSON web token.
We use the `localStorage` facility of the browser to store the token on the client.

```{code-block} javascript
:emphasize-lines: 3-21

 ...
   methods: {
     login: function(userid, passwd) {
       this.userid = '';
       this.passwd = '';
       this.$http.post('/Plone/@login',
                 {'login': userid,
                  'password': passwd},
                 {headers:
                  {'Content-type':'application/json',
                   'Accept':'application/json'}}).
         then(function(data, status, headers, config){
           localStorage.setItem('jwtoken', data.token);
         }, function(error){
           alert('Could not log you in');
         });
     },
     is_logged_in: function() {
       // we assume the user is logged in when he has a JWT token (that is naive)
       return localStorage.getItem('jwtoken') != null;
     },
 ...
```

We continue with changes to {file}`index.html` so that it uses the new methods.
We provide a login form if the user doesn't have a valid JSON web token.

Only authenticated users can see the rest of the page.

```{code-block} html
:emphasize-lines: 3-18

     <div id="talklist">

       <div v-if="! is_logged_in()">
         <form role="form">
           <fieldset>
             <legend>Login</legend>
               <label for="userid">Login</label>
               <input type="text" id="userid" v-model="userid" placeholder="Enter login">
               <label for="passwd">Password</label>
               <input type="password" id="passwd" v-model="passwd" placeholder="Password">
           </fieldset>
           <button v-on:click="login(userid,passwd)">
             Login
           </button>
         </form>
       </div>

       <div v-if="is_logged_in()">
         <div role="tablist">
```

Last we have to add some code that allows authenticated users to submit a lightning talk. We add another JavaScript method first:

```javascript
...
    submit_talk: function(subject, summary) {
      this.$http.post('/Plone/talks',
                 {'@type':'talk',
                  'type_of_talk':'Lightning Talk',
                  'audience':['Beginner','Advanced','Professional'],
                  'title':subject,
                  'description':summary},
                 {headers:
                  {'Content-type':'application/json',
                   'Authorization': 'Bearer ' + localStorage.getItem('jwtoken'),
                   'Accept':'application/json'}}).
        then(function(response){
          if(response.status === 201) { // created
            this.load_talks();
          }
        }, function(error){
          // according to docs, status can be 400 or 500
          // we check wether the token has expired - in this case,
          // we remove it from localStorage and disply the login page.
          // In all other cases, we display the message received
          // from Plone
          if ( (error.status == 400) && (error.data.type == 'ExpiredSignatureError') ) {
            localStorage.removeItem('jwtoken');
            location.reload();
          } else {
            // reason/error msg is contained in response body
            alert(error.message);
          }
        });
    },
...
```

## Exercise

Rewrite the `load_talks()` JavaScript method that it uses the portal search instead of `/Plone/talks`.
Sort the list by date.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} javascript
:emphasize-lines: 3

...
$scope.load_talks = function() {
  this.$http.get('/Plone/@search?portal_type=talk&sort_on=Date',
            {headers:{'Accept':'application/json'}}).
    then(function(response) {
...
  });
```
````
