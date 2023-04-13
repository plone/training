---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(zpt-label)=

# Page Templates

````{sidebar} Plone Classic UI Chapter
```{figure} _static/plone-training-logo-for-classicui.svg
:alt: Plone Classic UI
:class: logo
```

Solve the same tasks in the React frontend in chapter {doc}`volto_semantic_ui`

---

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout views_1
```

Code for the end of this chapter:

```shell
git checkout zpt
```
````

In this part you will:

- Learn to write page templates

Topics covered:

- TAL and TALES
- METAL
- Chameleon

Page Templates are HTML files with some additional information, written in TAL, METAL and TALES.

Page templates must be valid XML.

The three languages are:

- TAL: "Template Attribute Language"

  - Templating XML/HTML using special attributes
  - Using TAL we include expressions within HTML

- TALES: "TAL Expression Syntax"

  - defines the syntax and semantics of these expressions

- METAL: "Macro Expansion for TAL"

  - this enables us to combine, re-use and nest templates together

TAL and METAL are written like HTML attributes (href, src, title).
TALES are written like the values of HTML attributes.

They are used to modify the output:

```html
<p tal:content="string:I love red">I love blue</p>
```

results in:

```html
<p>I love red</p>
```

Let's try it.

Open the file {file}`training.pt` and add:

```html
<html>
  <body>
    <p>red</p>
  </body>
</html>
```

(zpt-tal-label)=

## TAL and TALES

Let's add some magic and modify the \<p>-tag:

```html
<p tal:content="string:blue">red</p>
```

This will result in:

```html
<p>blue</p>
```

Without restarting Plone open <http://localhost:8080/Plone/@@training>.

The same happens with attributes.

Replace the \<p>-line with:

```html
<a
  href="http://www.mssharepointconference.com"
  tal:define="a_fine_url string:https://www.ploneconf.org/"
  tal:attributes="href a_fine_url"
  tal:content="string:An even better conference"
>
  A sharepoint conference
</a>
```

results in:

```html
<a href="https://www.ploneconf.org/"> An even better conference </a>
```

We used three TAL-Attributes here.

This is the complete list of TAL-attributes:

`tal:define`

: define variables. We defined the variable `a_fine_url` to the string `"https://www.ploneconf.org/"`.

`tal:content`

: replace the content of an element. We replaced the default content above with "An even better conference"

`tal:attributes`

: dynamically change element attributes. We set the HTML attribute `href` to the value of the variable `a_fine_url`

`tal:condition`

: tests whether the expression is true or false, and outputs or omits the element accordingly.

`tal:repeat`

: repeats an iterable element, in our case the list of talks.

`tal:replace`

: replace the content of an element, like `tal:content` does, but removes the element only leaving the content.

`tal:omit-tag`

: remove an element, leaving the content of the element.

`tal:on-error`

: handle errors.

(python-expressions-label)=

### python expressions

Till now we only used one TALES expression (the `string:` bit).
Let's use a different TALES expression now.

With `python:` we can use Python code.

A example:

```html
<p tal:define="title python:context.title" tal:content="python:title.upper()">
  A big title
</p>
```

With `context.title` you access information from the context object, that is the object on which the view is called. Modify the template {file}`training.pt` like this

```xml
<p>
  ${python: 'This is the {0} "{1}" at {2}'.format(context.portal_type, context.title, context.absolute_url())}
</p>
```

Now call the view on different urls and see what happens:

- <http://localhost:8080/Plone/training>
- <http://localhost:8080/Plone/news/training>
- <http://localhost:8080/Plone/events/aggregator/training>
- <http://localhost:8080/Plone/the-event/training>
- <http://localhost:8080/Plone/news/conference-website-online/training>

And another python-statement:

```html
<p
  tal:define="talks python:['Dexterity for the win!',
                             'Deco is the future',
                             'A keynote on some weird topic',
                             'The talk that I did not submit']"
  tal:content="python:talks[0]"
>
  A talk
</p>
```

With python expressions:

- you can only write single statements
- you could import things but you should not

### tal:condition

`tal:condition`

: tests whether the expression is true or false.

- If it's true, then the tag is rendered.
- If it's false then the tag **and all its children** are removed and no longer evaluated.
- We can reverse the logic by perpending a `not:` to the expression.

Let's add another TAL Attribute to our above example:

```
tal:condition="python:talks"
```

We could also test for the number of talks:

```
tal:condition="python:len(talks) >= 1"
```

or if a certain talk is in the list of talks:

```
tal:condition="python:'Deco is the future' in talks"
```

### tal:repeat

Let's try another attribute:

```html
<p
  tal:define="talks python:['Dexterity for the win!',
                             'Deco is the future',
                             'A keynote on some weird topic',
                             'The talk that I did not submit']"
  tal:repeat="talk talks"
  tal:content="talk"
>
  A talk
</p>
```

`tal:repeat`

: repeats an iterable element, in our case the list of talks.

We change the markup a little to construct a list in which there is an `<li>` for every talk:

```{code-block} html
:linenos:

 <ul tal:define="talks python:['Dexterity for the win!',
                               'Deco is the future',
                               'A keynote on some weird topic',
                               'The talk that I did not submit']">
     <li tal:repeat="talk talks"
         tal:content="talk">
           A talk
     </li>
     <li tal:condition="not:talks">
           Sorry, no talks yet.
     </li>
 </ul>
```

### path expressions

Regarding TALES so far we used `string:` or `python:` or only variables.
The next and most common expression are path expressions.

Optionally you can start a path expression with `path:`

Every path expression starts with a variable name.
It can either be an object like {py:obj}`context`, {py:obj}`view` or {py:obj}`template` or a variable defined by you like {py:data}`talk`.

After the variable we add a slash `/` and the name of a sub-object, attribute or callable.
The `/` is used to end the name of an object and the start of the property name.

Properties themselves may be objects that in turn have properties.

```html
<p tal:content="context/title"></p>
```

We can chain several of those to get to the information we want.

```html
<p tal:content="context/REQUEST/form"></p>
```

This would return the value of the form dictionary of the HTTPRequest object. Useful for form handling.

The `|` ("or") character is used to find an alternative value to a path if the first path evaluates to `nothing` or does not exist.

```html
<p tal:content="context/title | context/id"></p>
```

This returns the id of the context if it has no title.

```html
<p tal:replace="talk/average_rating | nothing"></p>
```

This returns nothing if there is no 'average_rating' for a talk.

What will not work is `tal:content="python:talk['average_rating'] or ''"`.

Who knows what this would yield?

```{only} not presentation
We'll get `KeyError: 'average_rating'`. It is very bad practice to use `|` too often since it will swallow errors like a typo
in `tal:content="talk/averange_ratting | nothing"` and you might wonder why there are no ratings later on...

You can't and should not use it to prevent errors like a try/except block.
```

There are several **built-in variables** that can be used in paths:

The most frequently used one is `nothing` which is the equivalent to None

```html
<p tal:replace="nothing">this comment will not be rendered</p>
```

A dict of all the available variables at the current state is `econtext`

```{code-block} html
:linenos:

<dl>
  <tal:vars tal:repeat="variable econtext">
    <dt>${variable}</dt>
    <dd>${python:econtext[variable]}</dd>
  </tal:vars>
</dl>
```

Useful for debugging :-)

````{note}
In Plone 4 that used to be `CONTEXTS`

```{code-block} html
:linenos:

<dl>
  <tal:vars tal:repeat="variable CONTEXTS">
    <dt tal:content="variable"></dt>
    <dd tal:content="python:CONTEXTS[variable]"></dd>
  </tal:vars>
</dl>
```
````

### Pure TAL blocks

We can use TAL attributes without HTML Tags.

This is useful when we don't need to add any tags to the markup.

Syntax:

```html
<tal:block attribute="expression">some content</tal:block>
```

Examples:

```html
<tal:block define="id template/id">
  ...
  <b tal:content="id">The id of the template</b>
  ...
</tal:block>

<tal:news condition="python:context.portal_type == 'News Item'">
  This text is only visible if the context is a News Item
</tal:news>
```

### handling complex data in templates

Let's move on to a little more complex data. And to another TAL attribute:

tal:replace

: replace the content of an element and removes the element only leaving the content.

Example:

```html
<p>
  <img
    tal:define="tag string:<img src='https://plone.org/logo.png'>"
    tal:replace="tag"
  />
</p>
```

this results in:

```html
<p>&lt;img src='https://plone.org/logo.png'&gt;</p>
```

`tal:replace` drops its own base tag in favor of the result of the TALES expression.
Thus the original `<img... >` is replaced.

But the result is escaped by default.

To prevent escaping we use `structure`

```html
<p>
  <img
    tal:define="tag string:<img src='https://plone.org/logo.png'>"
    tal:replace="structure tag"
  />
</p>
```

Now let's emulate a typical Plone structure by creating a dictionary.

```{code-block} html
:linenos:

  <table tal:define="talks python:[{'title':'Dexterity for the win!',
                                    'subjects':('content-types', 'dexterity')},
                                   {'title':'Deco is the future',
                                    'subjects':('layout', 'deco')},
                                   {'title':'The State of Plone',
                                    'subjects':('keynote',) },
                                   {'title':'Diazo designs dont suck!',
                                    'subjects':('design', 'diazo', 'xslt')}
                                  ]">
      <tr>
          <th>Title</th>
          <th>Topics</th>
      </tr>
      <tr tal:repeat="talk talks">
          <td tal:content="talk/title">A talk</td>
          <td tal:define="subjects talk/subjects">
              <span tal:repeat="subject subjects"
                    tal:replace="subject">
              </span>
          </td>
      </tr>
  </table>
```

We emulate a list of talks and display information about them in a table.
We'll get back to the list of talks later when we use the real talk objects that we created with dexterity.

To complete the list here are the TAL attributes we have not yet used:

`tal:omit-tag`

: Omit the element tag, leaving only the inner content.

`tal:on-error`

: handle errors.

When an element has multiple TAL attributes, they are executed in this order:

1. define
2. condition
3. repeat
4. content or replace
5. attributes
6. omit-tag

## Chameleon

Since Plone 5 we have [Chameleon](https://chameleon.readthedocs.io/en/latest/).

Using the integration layer [five.pt](https://pypi.org/project/five.pt) it is fully compatible with the normal TAL syntax but offers some additional features:

You can use `${...}` as short-hand for text insertion in pure html effectively making `tal:content` and `tal:attributes` obsolete.

Here are some examples:

Plone 4 and Plone 5:

```{code-block} html
:linenos:

 <a tal:attributes="href string:${context/absolute_url}?ajax_load=1;
                    class python:context.portal_type.lower().replace(' ', '')"
    tal:content="context/title">
    The Title of the current object
 </a>
```

Plone 5 (and Plone 4 with `five.pt`):

```{code-block} html
:linenos:

 <a href="${context/absolute_url}?ajax_load=1"
    class="${python:context.portal_type.lower().replace(' ', '')}">
    ${python:context.title}
 </a>
```

You can also add pure python into the templates:

```{code-block} html
:linenos:

 <div>
   <?python
   someoptions = dict(
       id=context.id,
       title=context.title)
   ?>
   This object has the id "${python:someoptions['id']}"" and the title "${python:someoptions['title']}".
 </div>
```

(zpt-metal-label)=

## Exercise 1

Modify the following template and one by one solve the following problems:
\:

```{code-block} html
:linenos:

 <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                   'subjects': ('content-types', 'dexterity')},
                                  {'title': 'Mosaic will be the next big thing.',
                                   'subjects': ('layout', 'deco', 'views'),
                                   'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                  {'title': 'The State of Plone',
                                   'subjects': ('keynote',) },
                                  {'title': 'Diazo is a powerful tool for theming!',
                                   'subjects': ('design', 'diazo', 'xslt')},
                                  {'title': 'Magic templates in Plone 5',
                                   'subjects': ('templates', 'TAL'),
                                   'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                 ]">
     <tr>
         <th>Title</th>
         <th>Topics</th>
     </tr>
     <tr tal:repeat="talk talks">
         <td tal:content="talk/title">A talk</td>
         <td tal:define="subjects talk/subjects">
             <span tal:repeat="subject subjects"
                   tal:replace="subject">
             </span>
         </td>
     </tr>
 </table>
```

1. Display the subjects as comma-separated.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} html
:emphasize-lines: 21
:linenos:

<table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                  'subjects': ('content-types', 'dexterity')},
                                 {'title': 'Mosaic will be the next big thing.',
                                  'subjects': ('layout', 'deco', 'views'),
                                  'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                 {'title': 'The State of Plone',
                                  'subjects': ('keynote',) },
                                 {'title': 'Diazo is a powerful tool for theming!',
                                  'subjects': ('design', 'diazo', 'xslt')},
                                 {'title': 'Magic templates in Plone 5',
                                  'subjects': ('templates', 'TAL'),
                                  'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                ]">
    <tr>
        <th>Title</th>
        <th>Topics</th>
    </tr>
    <tr tal:repeat="talk talks">
        <td tal:content="talk/title">A talk</td>
        <td tal:define="subjects talk/subjects">
            <span tal:replace="python:', '.join(subjects)">
            </span>
        </td>
    </tr>
</table>
```
````

2. Turn the title in a link to the URL of the talk if there is one.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} html
:emphasize-lines: 20
:linenos:

 <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                   'subjects': ('content-types', 'dexterity')},
                                  {'title': 'Mosaic will be the next big thing.',
                                   'subjects': ('layout', 'deco', 'views'),
                                   'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                  {'title': 'The State of Plone',
                                   'subjects': ('keynote',) },
                                  {'title': 'Diazo is a powerful tool for theming!',
                                   'subjects': ('design', 'diazo', 'xslt')},
                                  {'title': 'Magic templates in Plone 5',
                                   'subjects': ('templates', 'TAL'),
                                   'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                 ]">
     <tr>
         <th>Title</th>
         <th>Topics</th>
     </tr>
     <tr tal:repeat="talk talks">
         <td>
             <a tal:attributes="href talk/url | nothing"
                tal:content="talk/title">
                A talk
             </a>
         </td>
         <td tal:define="subjects talk/subjects">
             <span tal:replace="python:', '.join(subjects)">
             </span>
         </td>
     </tr>
 </table>
```
````

3. If there is no URL, turn it into a link to a google search for that talk's title:

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} html
:emphasize-lines: 20, 21
:linenos:

 <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                   'subjects': ('content-types', 'dexterity')},
                                  {'title': 'Mosaic will be the next big thing.',
                                   'subjects': ('layout', 'deco', 'views'),
                                   'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                  {'title': 'The State of Plone',
                                   'subjects': ('keynote',) },
                                  {'title': 'Diazo is a powerful tool for theming!',
                                   'subjects': ('design', 'diazo', 'xslt')},
                                  {'title': 'Magic templates in Plone 5',
                                   'subjects': ('templates', 'TAL'),
                                   'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                 ]">
     <tr>
         <th>Title</th>
         <th>Topics</th>
     </tr>
     <tr tal:repeat="talk talks">
         <td>
             <a tal:define="google_url string:https://www.google.com/search?q=${talk/title}"
                tal:attributes="href talk/url | google_url"
                tal:content="talk/title">
                A talk
             </a>
         </td>
         <td tal:define="subjects talk/subjects">
             <span tal:replace="python:', '.join(subjects)">
             </span>
         </td>
     </tr>
 </table>
```
````

4\. Add alternating the CSS classes 'odd' and 'even' to the \<tr>. ({samp}`repeat.{<name of item in loop>}.odd` is True
if the ordinal index of the current iteration is an odd number).

> Use some CSS to test your solution:
>
> ```css
> <style type="text/css">
>   tr.odd {background-color: #ddd;}
> </style>
> ```

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} html
:emphasize-lines: 19
:linenos:

 <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                   'subjects': ('content-types', 'dexterity')},
                                  {'title': 'Mosaic will be the next big thing.',
                                   'subjects': ('layout', 'deco', 'views'),
                                   'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                  {'title': 'The State of Plone',
                                   'subjects': ('keynote',) },
                                  {'title': 'Diazo is a powerful tool for theming!',
                                   'subjects': ('design', 'diazo', 'xslt')},
                                  {'title': 'Magic templates in Plone 5',
                                   'subjects': ('templates', 'TAL'),
                                   'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                 ]">
     <tr>
         <th>Title</th>
         <th>Topics</th>
     </tr>
     <tr tal:repeat="talk talks"
         tal:attributes="class python: 'odd' if repeat.talk.odd else 'even'">
         <td>
             <a tal:define="google_url string:https://www.google.com/search?q=${talk/title};
                            "
                tal:attributes="href talk/url | google_url;
                                "
                tal:content="talk/title">
                A talk
             </a>
         </td>
         <td tal:define="subjects talk/subjects">
             <span tal:replace="python:', '.join(subjects)">
             </span>
         </td>
     </tr>
 </table>
```
````

5. Only use python expressions.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} html
:linenos:

 <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                   'subjects': ('content-types', 'dexterity')},
                                  {'title': 'Mosaic will be the next big thing.',
                                   'subjects': ('layout', 'deco', 'views'),
                                   'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                  {'title': 'The State of Plone',
                                   'subjects': ('keynote',) },
                                  {'title': 'Diazo is a powerful tool for theming!',
                                   'subjects': ('design', 'diazo', 'xslt')},
                                  {'title': 'Magic templates in Plone 5',
                                   'subjects': ('templates', 'TAL'),
                                   'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                 ]">
     <tr>
         <th>Title</th>
         <th>Topics</th>
     </tr>
     <tr tal:repeat="talk python:talks"
         tal:attributes="class python: 'odd' if repeat.talk.odd else 'even'">
         <td>
             <a tal:attributes="href python:talk.get('url', 'https://www.google.com/search?q=%s' % talk['title'])"
                tal:content="python:talk['title']">
                A talk
             </a>
         </td>
         <td tal:content="python:', '.join(talk['subjects'])">
         </td>
     </tr>
 </table>
```
````

6. Use the syntax of Plone 5 replacing `tal:attribute` and `tal:content` with inline `${}` statements.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} html
:emphasize-lines: 20, 24, 28
:linenos:

 <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                   'subjects': ('content-types', 'dexterity')},
                                  {'title': 'Mosaic will be the next big thing.',
                                   'subjects': ('layout', 'deco', 'views'),
                                   'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                  {'title': 'The State of Plone',
                                   'subjects': ('keynote',) },
                                  {'title': 'Diazo is a powerful tool for theming!',
                                   'subjects': ('design', 'diazo', 'xslt')},
                                  {'title': 'Magic templates in Plone 5',
                                   'subjects': ('templates', 'TAL'),
                                   'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                 ]">
     <tr>
         <th>Title</th>
         <th>Topics</th>
     </tr>

     <tr tal:repeat="talk python:talks"
         class="${python: 'odd' if repeat.talk.odd else 'even'}">
         <td>
             <a href="${python:talk.get('url', 'https://www.google.com/search?q=%s' % talk['title'])}">
                 ${python:talk['title']}
             </a>
         </td>
         <td>
             ${python:', '.join(talk['subjects'])}
         </td>
     </tr>
 </table>
```
````

7. Sort the talks alphabetically by title

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{code-block} html
:emphasize-lines: 19, 21
:linenos:

 <table tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                   'subjects': ('content-types', 'dexterity')},
                                  {'title': 'Mosaic will be the next big thing.',
                                   'subjects': ('layout', 'deco', 'views'),
                                   'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                  {'title': 'The State of Plone',
                                   'subjects': ('keynote',) },
                                  {'title': 'Diazo is a powerful tool for theming!',
                                   'subjects': ('design', 'diazo', 'xslt')},
                                  {'title': 'Magic templates in Plone 5',
                                   'subjects': ('templates', 'TAL'),
                                   'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'}
                                 ]">
     <tr>
         <th>Title</th>
         <th>Topics</th>
     </tr>

 <?python from operator import itemgetter ?>

     <tr tal:repeat="talk python:sorted(talks, key=itemgetter('title'))"
         class="${python: 'odd' if repeat.talk.odd else 'even'}">
         <td>
             <a href="${python:talk.get('url', 'https://www.google.com/search?q=%s' % talk['title'])}">
                 ${python:talk['title']}
             </a>
         </td>
         <td>
             ${python:', '.join(talk['subjects'])}
         </td>
     </tr>
 </table>
```

```{warning}
Do not use this trick in your projects! This level of python-logic belongs in a class, not in a template!
```
````

## METAL and macros

Why is our output so ugly?

How do we get our HTML to render in Plone the UI?

We use METAL (Macro Extension to TAL) to define slots that we can fill and macros that we can reuse.

Add this to the `<html>` tag:

```
metal:use-macro="context/main_template/macros/master"
```

And then wrap the code we want to put in the content area of Plone in:

```xml
<metal:content-core fill-slot="main">
    ...
</metal:content-core>
```

This will put our code in a section defined in the main_template called "content-core".

Now replace the `main` in `fill-slot="main"` with `content-core` and see what changes.

The template should now look like below when we exclude the last exercise.

Here also added the css-class `listing` to the table. It is one of many css-classes used by Plone that you can reuse in your projects:

```{code-block} xml
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
      lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>

<metal:content-core fill-slot="content-core">

<table class="listing"
       tal:define="talks python:[{'title': 'Dexterity is the new default!',
                                  'subjects': ('content-types', 'dexterity')},
                                 {'title': 'Mosaic will be the next big thing.',
                                  'subjects': ('layout', 'deco', 'views'),
                                  'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                                 {'title': 'The State of Plone',
                                  'subjects': ('keynote',) },
                                 {'title': 'Diazo is a powerful tool for theming!',
                                  'subjects': ('design', 'diazo', 'xslt')},
                                 {'title': 'Magic templates in Plone 5',
                                  'subjects': ('templates', 'TAL'),
                                  'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'},
                                ]">
    <tr>
        <th>Title</th>
        <th>Topics</th>
    </tr>

    <tr tal:repeat="talk python:talks"
        class="${python: 'odd' if repeat.talk.odd else 'even'}">
        <td>
            <a href="${python:talk.get('url', 'https://www.google.com/search?q=%s' % talk['title'])}">
                ${python:talk['title']}
            </a>
        </td>
        <td>
            ${python:', '.join(talk['subjects'])}
        </td>
    </tr>
</table>

</metal:content-core>

</body>
</html>
```

### macros in browser views

Define a macro in a new file {file}`macros.pt`

```html
<div metal:define-macro="my_macro">
  <p>I can be reused</p>
</div>
```

Register it as a simple BrowserView in zcml:

```xml
<browser:page
  for="*"
  name="abunchofmacros"
  template="templates/macros.pt"
  permission="zope2.View"
  />
```

Reuse the macro in the template {file}`training.pt`:

```html
<div metal:use-macro="context/@@abunchofmacros/my_macro">
  Instead of this the content of the macro will appear...
</div>
```

Which is the same as:

```html
<div
  metal:use-macro="python:context.restrictedTraverse('abunchofmacros')['my_macro']"
>
  Instead of this the content of the macro will appear...
</div>
```

Restart your Plone instance from the command line, and then open <http://localhost:8080/Plone/@@training> to see this macro
being used in our @@training browser view template.

(tal-access-plone-label)=

## Accessing Plone from the template

In the template you have access to:

- the **context** object on which your view is called on
- the **view** (and all python methods we'll put in the view later on)
- the **request**

With these three you can do almost anything!

Create a new talk object "Dexterity for the win!" and add some information to all fields, especially the speaker and the email-address.

Now access the view `training` on that new talk by opening <http://localhost:8080/Plone/dexterity-for-the-win/training> in the browser.

It will look the same as before.

Now modify the template {file}`training.pt` to display the title of the context:

```html
<h1>${python: context.title}</h1>
```

## Exercise 2

- Render a mail-link to the speaker.
- Display the speaker instead of the raw email-address.
- If there is no speaker-name display the address.
- Modify attributes of html-tags by adding your statements into the attributes directly like `title="${python: context.type_of_talk.capitalize()}"`.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```html
<a href="${python: 'mailto:{0}'.format(context.email)}">
   ${python: context.speaker if context.speaker else context.email}
</a>
```

```{note}
Alternatively you can also use `tal:attributes="<attr> <value>"` to modify attributes.
```
````

## Accessing other views

In templates we can also access other browser views. Some of those exist to provide easy access to methods we often need:

```
tal:define="context_state context/@@plone_context_state;
            portal_state context/@@plone_portal_state;
            plone_tools context/@@plone_tools;
            plone_view context/@@plone;"
```

`@@plone_context_state`

: The BrowserView {py:class}`plone.app.layout.globals.context.ContextState` holds useful methods having to do with the current context object such as {py:meth}`is_default_page`

`@@plone_portal_state`

: The BrowserView {py:class}`plone.app.layout.globals.portal.PortalState` holds methods for the portal like {py:meth}`portal_url`

`@@plone_tools`

: The BrowserView {py:class}`plone.app.layout.globals.tools.Tools` gives access to the most important tools like `plone_tools/catalog`

These are very widely used and there are many more.

(tal-missing-label)=

## What we missed

There are some things we did not cover so far:

`tal:condition="exists:expression"`

: checks if an object or an attribute exists (seldom used)

`tal:condition="nocall:context"`

: to explicitly not call a callable.

If we refer to content objects, without using the nocall: modifier these objects are unnecessarily rendered in memory as the expression is evaluated.

`i18n:translate` and `i18n:domain`

: the strings we put in templates can be translated automatically.

There is a lot more about TAL, TALES and METAL that we have not covered.
You'll only learn it if you keep reading, writing and customizing templates.

```{seealso}
- <https://5.docs.plone.org/adapt-and-extend/theming/templates_css/template_basics.html>
- Using Zope Page Templates: <https://zope.readthedocs.io/en/latest/zopebook/ZPT.html>
- Zope Page Templates Reference: <https://zope.readthedocs.io/en/latest/zopebook/AppendixC.html>
- <https://chameleon.readthedocs.io/en/latest/>
```
