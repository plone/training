---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-thirdparty-label)=

# Using Third-Party Behaviors

(plone5-thirdparty-banner-label)=

## Add Teaser With collective.behavior.banner

There are a lot of add-ons in Plone for sliders/banners/teasers.
We thought there should be a better one and created [collective.behavior.banner](https://pypi.org/project/collective.behavior.banner/).

```{figure} ../_static/standards.png
:align: center
```

To use it add the name to your list of eggs in {file}`buildout.cfg`:

```cfg
eggs =
    Plone
    ...
    collective.behavior.banner
```

Even though {py:mod}`collective.behavior.banner` has been released on PyPI we will now act as if this add-on exists on GitHub or has changes on GitHub that have not yet been released, but that you really want.
This is not to annoy you.
It happens surprisingly often if you work with new versions of Plone.

The training buildout has a section `[sources]` that tells buildout to download a specific add-on not from PyPI but from some code repository (usually GitHub):

```cfg
[sources]
collective.behavior.banner = git https://github.com/collective/collective.behavior.banner.git pushurl=git@github.com:collective/collective.behavior.banner.git rev=7c13285
```

Pinning the revision saves us from being surprised by changes in the code we might not want.
You can also pin a branch or a tag.

After adding the source, we need to add the egg to the list of eggs that should be checked out:

```cfg
# We want to checkout these eggs directly from github
auto-checkout =
    ploneconf.site
    collective.behavior.banner
```

You need to run {file}`./bin/buildout` again for these changes to take effect.

- Install the add-on
- Create a new dexterity content type `Banner` with **only** the behavior `Banner` enabled.
- Create a folder called `banners`
- Add two banners into that folder using images taken from <https://unsplash.com/> or <https://picsum.photos/>
- Add the Behavior `Slider` to the default content type `Page (Document)`
- Edit the front-page and link to the new banners.
