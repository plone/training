(plone5-intro-label)=

# Introduction

(plone5-intro-who-are-you-label)=

## Who are you?

Tell us about yourselves:

- Name, company, country...
- What is your Plone experience?
- What is your web development experience?
- What are your expectations for this tutorial?
- What is your favorite text editor?
- If this training will include the development chapters:  
    - Do you know the HTML of the output of this?

      ```html
      <div class="hiddenStructure"
            tal:repeat="num python:range(1, 10, 5)"
            tal:content="structure num"
            tal:omit-tag="">
        This is some weird sh*t!
      </div>
      ```

      ````{only} not presentation
      The answer is:

      ```
      1 6
      ```
      ````

    - Do you know what the following would return?:

      ```
      [(i.Title, i.getURL()) for i in context.getFolderContents()]
      ```

(plone5-intro-what-happens-label)=

## What will we do?

Some technologies and tools we use during the training:

- For the beginning training:

  > - [Virtualbox](https://www.virtualbox.org/)
  > - [Vagrant](https://www.vagrantup.com/)
  > - [Ubuntu linux](https://www.ubuntu.com/)
  > - Through-the-web (TTW)
  > - [Buildout](http://www.buildout.org/en/latest/)
  > - A little XML
  > - Python 3.7

- For the advanced chapters:

  > - [Git](https://git-scm.com/)
  > - [GitHub](https://github.com)
  > - [Try Git (Nice introduction to git and github)](http://try.github.io/levels/1/challenges/1/)
  > - TAL
  > - METAL
  > - ZCML
  > - [Python](https://www.python.org)
  > - Dexterity
  > - Viewlets
  > - [JQuery](http://jquery.com/)
  > - [Testing](https://docs.plone.org/external/plone.app.testing/docs/source/index.html)
  > - [References/Relations](https://docs.plone.org/external/plone.app.dexterity/docs/advanced/references.html)

(plone5-intro-what-wont-happen-label)=

## What will we not do?

We will not cover the following topics:

- [Archetypes](https://docs.plone.org/old-reference-manuals/archetypes/index.html)
- [Portlets](https://docs.plone.org/old-reference-manuals/portlets/index.html)
- [z3c.forms](https://docs.plone.org/develop/plone/forms/z3c.form.html)
- [Theming](https://docs.plone.org/adapt-and-extend/theming/index.html)
- [i18n and locales](https://docs.plone.org/develop/plone/i18n/index.html)
- [Deployment, Hosting and Caching](https://docs.plone.org/manage/deploying/index.html)
- Grok

Other topics are only covered lightly:

- [Zope Component Architecture](https://docs.plone.org/develop/addons/components/index.html)
- [GenericSetup](https://docs.plone.org/develop/addons/components/genericsetup.html)
- [ZODB](https://docs.plone.org/develop/plone/persistency/index.html)
- [Security](https://docs.plone.org/develop/plone/security/index.html)
- [Permissions](https://docs.plone.org/develop/plone/security/permissions.html)
- [Performance and Caching](https://docs.plone.org/manage/deploying/testing_tuning/performance/index.html)

(plone5-intro-expect-label)=

## What to expect

At the end of the first two days of training, you'll know many of the tools required for Plone installation,
integration and configuration.

You'll be able to install add-on packages and will know something about the technologies underlying Plone and their histories.

At the end of the second two days, you won't be a complete professional Plone-programmer,
but you will know some of the more powerful features of Plone and should be able to construct a more complex website with custom themes and packages.

You should also be able to find out where to look for instructions to do tasks we did not cover.
You will know most of the core technologies involved in Plone programming.

If you want to become a professional Plone developer or a highly sophisticated Plone integrator you should
definitely read [Martin Aspeli's book](https://www.packtpub.com/web-development/professional-plone-4-development)
and then re-read it again while actually doing a complex project.

(plone5-intro-classroom-protocol)=

## Classroom Protocol

````{only} not presentation
```{note}
- Stop us and ask questions when you have them!
- Tell us if we speak too fast, too slow or not loud enough.
- One of us is always there to help you if you are stuck. Please give us a sign if you are stuck.
- We'll take some breaks, the first one will be at XX.
- Where is food, restrooms
- Someone please record the time we take for each chapter (incl. title)
- Someone please write down errors
- Contact us after the training: <mailto:team@starzel.de>
```
````

**Questions to ask:**

> - What did you just say?
> - Please explain what we just did again?
> - How did that work?
> - Why didn't that work for me?
> - Is that a typo?

**Questions \_\_not\_\_ to ask:**

> - **Hypotheticals**: What happens if I do X?
> - **Research**: Can Plone do Y?
> - **Syllabus**: Are we going to cover Z in class?
> - **Marketing questions**: please just don't.
> - **Performance questions**: Is Plone fast enough?
> - **Unpythonic**: Why doesn't Plone do it some other way?
> - **Show off**: Look what I just did!

(plone5-intro-docs-label)=

## Documentation

Follow the training at <https://training.plone.org/5>

```{note}
You can use this presentation to copy & paste the code but you will memorize more if you type yourself.
```

(plone5-intro-further-reading-label)=

## Further Reading

- [Martin Aspeli: Professional Plone4 Development](https://www.packtpub.com/web-development/professional-plone-4-development)
- [Practical Plone](https://www.packtpub.com/web-development/practical-plone-3-beginners-guide-building-powerful-websites)
- [Zope Page Templates Reference](https://zope.readthedocs.io/en/latest/zopebook/AppendixC.html)
