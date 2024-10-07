---
myst:
  html_meta:
    "description": "Relations between content instances"
    "property=og:description": "Relations between content instances"
    "property=og:title": "Relations"
    "keywords": "relation, reference"
---


(relations)=

# Relations

You can model relationships between content items by placing them in a hierarchy (e.g. a (folderish) page _speakers_ containing the (folderish) speakers and within each speaker the talks) or by linking them to each other in blocks.
But where would you then store a talk that two speakers give together?

Relations allow developers to model relationships between objects without using links or a hierarchy.
The behavior {py:class}`plone.app.relationfield.behavior.IRelatedItems` provides the field {guilabel}`Related Items` in the section {guilabel}`Categorization`.
That field simply says `a` is somehow related to `b`.

By using custom relations you can model your data in a much more meaningful way.


````{card} Backend and frontend chapter

Check out the code at the relevant tags!

Code for the beginning of this chapter:

```shell
# frontend
git checkout sponsors
```

```shell
# backend
git checkout user_generated_content
```

Code for the end of this chapter:

```shell
# frontend
git checkout relations
```

```shell
# backend
git checkout relations
```

More info in {doc}`code`
````


## Creating and configuring relations in a schema

Relate to **one** item only with `RelationChoice`.

```{code-block} python
:linenos:

from z3c.relationfield.schema import RelationChoice


    speaker = RelationChoice(
        title="Speaker",
        description="The speaker of the talk",
        vocabulary="plone.app.vocabularies.Catalog",
        required=False
    )
```

Relate to **multiple** items with `RelationList`.

```{code-block} python
:linenos:

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList


    speaker = RelationList(
        title="Speaker",
        description="Speakers of the talk",
        value_type=RelationChoice(
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[]
    )
```

```{seealso}
[Relation fields in docs.plone.org](https://6.docs.plone.org/volto/development/widget.html?highlight=staticcatalogvocabulary#relation-fields)
```


### Controlling what to relate to

The vocabulary controls which content instances can be related to from the field.

```{code-block} python
:linenos:
:emphasize-lines: 5

    speaker = RelationList(
        title="Speaker",
        description="Speakers of the talk",
        value_type=RelationChoice(
            vocabulary="ploneconf.speakers"
        ),
        required=False,
        default=[]
    )
```

We want to relate to content instances of type 'speaker'.
So we define a vocabulary of speakers.

{file}`src/ploneconf/site/vocabularies/configure.zcml`

```{code-block} xml
:linenos:

    <utility
        name="ploneconf.speakers"
        component="ploneconf.site.vocabularies.speaker.SpeakerVocabularyFactory"
        />
```

{file}`src/ploneconf/site/vocabularies/speaker.py`


```{code-block} python
:linenos:

from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory


@provider(IVocabularyFactory)
def SpeakerVocabularyFactory(context=None):
    return StaticCatalogVocabulary(
        {
            "portal_type": ["speaker"],
            "review_state": "published",
            "sort_on": "sortable_title",
        }
    )
```


## The widget

The widget allows the editor to edit the relations.

The default and only widget by now in Volto is the `select` widget.
It opens the tree of content to be selected by the editor.
On saving the talk, the selection is validated according the vocabulary.

For a more sophisticated widget see the explanation on how to write a custom widet in {doc}`plone6docs:volto/development/widget`.


## Accessing and displaying related items

The values of a relation 'speaker' can be displayed in 'TalkView' by iterating over the values.

```{code-block} jsx

{content.speaker?.length > 0 &&
    content.speaker.map((el) => (
    <UniversalLink href={el['@id']}>{el.title} </UniversalLink>
    ))}
```

Available attributes of the speakers are:

```{code-block} js

{
    "@id": "http://localhost:3000/speaker-1/regula-beimer",
    "@type": "speaker",
    "Subject": [],
    "UID": "8d31ccfacaaf42bba3210d3151db9dab",
    "description": "",
    "effective": "2024-09-28T08:54:49+00:00",
    "image_field": null,
    "image_scales": {
        "image": [
            {
                "content-type": "image/jpeg",
                "download": "@@images/image-1448-25cf21fa8ffb8345f090df9ba69ee78d.jpeg",
                "filename": "world_coffee_day.jpg",
                "height": 2048,
                "scales": {
                    "great": {
                        "download": "@@images/image-1200-5bea4c124fa5dc6f3b3745764619ba83.jpeg",
                        "height": 1697,
                        "width": 1200
                    },
                    "icon": {
                        "download": "@@images/image-32-67bd65cbf8bf791b545899735e679e24.jpeg",
                        "height": 32,
                        "width": 22
                    },
                    "large": {
                        "download": "@@images/image-800-2ff775ad2ff29c654c6cbcaefd0e42a5.jpeg",
                        "height": 1131,
                        "width": 800
                    },
                    "larger": {
                        "download": "@@images/image-1000-48769f94fb1be73ebec34a76b2008f98.jpeg",
                        "height": 1414,
                        "width": 1000
                    },
                    "mini": {
                        "download": "@@images/image-200-779b3a25d369ae2cfdd2dfd9b62ec4f6.jpeg",
                        "height": 282,
                        "width": 200
                    },
                    "preview": {
                        "download": "@@images/image-400-bd124545ee21ceaf4b08ee14e3e5da03.jpeg",
                        "height": 565,
                        "width": 400
                    },
                    "teaser": {
                        "download": "@@images/image-600-9b6158c5fa7a56bdeca39cf8703615ec.jpeg",
                        "height": 848,
                        "width": 600
                    },
                    "thumb": {
                        "download": "@@images/image-128-2fa41dcc6369c5ce53a4d61b66bbd5c2.jpeg",
                        "height": 128,
                        "width": 90
                    },
                    "tile": {
                        "download": "@@images/image-64-552ba9f0563c26226d8e93dd63b2ab8e.jpeg",
                        "height": 64,
                        "width": 45
                    }
                },
                "size": 494193,
                "width": 1448
            }
        ]
    },
    "review_state": "published",
    "title": "Regula Beimer",
    "type_title": "Speaker"
}
```


## Inspecting relations

In Plone 6 Volto you can inspect all relations and backrelations in your site using the control panel `relations` <http://localhost:3000/controlpanel/relations>.
You can even edit the relations.

```{figure} _static/inspect-relations_volto_annotations.png
:alt: The relations controlpanel

The relations controlpanel
```

You can find the backrelations of a content instance via the menu item {guilabel}`Links and references`



```{figure} _static/Links_and_references_and_relations_menu.png
:alt: Links and references menu

Links and references menu
```

```{figure} _static/Links_and_references_and_relations.png
:alt: Links and references

Links and references
```


## Programming with relations

Since Plone 6 `plone.api` has methods to create, read, and delete relations and backrelations.

```{code-block} python
:linenos:

from plone import api

portal = api.portal.get()
source = portal.schedule["workflows-made-easy"]
target = portal.speakers["urs-herbst"]
api.relation.create(source=source, target=target, relationship="speaker")
```

```{code-block} python
:linenos:

from plone import api

api.relation.get(source=portal.schedule["workflows-made-easy"])
api.relation.get(relationship="speaker")
api.relation.get(target=portal.speakers["urs-herbst"])
```

List all relations of name "speaker":

```{code-block} python

>>> for rel in api.relation.get(relationship="speaker"): rel.from_object, rel.to_object, rel.from_attribute
... 
(<Talk at /Plone/schedule/talkli>, <Speaker at /Plone/speakers/urs-herbst>, 'speaker')
(<Talk at /Plone/schedule/advanced-relations>, <Speaker at /Plone/speakers/katja-i-e-suss>, 'speaker')
```

See the chapter {ref}`plone6docs:chapter-relation` of the docs for `plone.api`  for more details.


### Plone 5.2 and older

In older Plone versions you can use [collective.relationhelpers](https://pypi.org/project/collective.relationhelpers) to create and read relations and backrelations in a very similar way.


## Exercise 1

Add a content type speaker and modify the content type talk to relate to speakers.
Write an upgrade step for the change of the field 'speaker'.

The code can be found in backend add-on `ploneconf.site` at tag `relations`.


## Exercise 2

The speaker is now a relation on talk.
Available on the TalkView is a subset of attributes of the speaker.
How would you achieve to show the github handle of the speaker?
It is by now not included in the available attributes.


```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

Add the name of the field to the relevant serializer implementing `IJSONSummarySerializerMetadata` in `src/ploneconf/site/serializers/summary.py`
```

