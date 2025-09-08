---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(trainthetrainers-training-theory-label)=

# Training theory: education, how people learn and process information

```{warning}
This chapter is a work in progress
```

This chapter will contain some background on learning, mental models that people use in different ways, how to improve remembering and understanding of knowledge, training rhythm and attention span, etc. etc.

These are helpful both before, during and after a training, that's why we have put them in a separate chapter that you should read before you start writing or improving the training material.

## Introduction

The science of learning and how we process information is a huge field of research, this chapter is nowhere near an overview or a complete introduction of learning. There are a number of subjects here that could give you some background and things to consider while you are preparing for, writing or giving a training. If you are a (Plone) trainer and have more subjects or wisdom, please add them here.

## Learning Styles and the Trainer

If you take a look at [Learning Styles on WikiPedia](https://en.wikipedia.org/wiki/Learning_styles) you will find a huge number of models and theories on how individuals learn.

Some of us are more visually oriented and love diagrams, drawings, schema's and other visual tools to structure and grasp information. Others are more comfortable with a narrative written down that they can follow along. If you're more auditory you'd love to follow along with a screencast or prefer to have a trainer in front of you who talks you through a procedure.

Other models/modes differentiate in learning by examples, or maybe you prefer to have the theoretical knowledge and background first before you see an example.

A big challenge for a trainer is to recognise his own preference of learning while preparing for and giving a training. So maybe you prefer to have a lot of theory first and then continue to the examples. If you then give a training to
a small group of students and you notice they loose focus after half an hour or theory, it might be that they are more pragmatists and would love to see an example first before learning about the reasons why.

If you don't like diagrams and figures yourself because they're always an abstraction and incomplete, you could leave them out of any training material, but a significant part of your future training audience will love them.

There's not a magic wand or solution because you will always be limited in time and space, but as a guideline, try to balance the visual/written information, balance theory and examples. Also, you can observe your students during the training day and try to figure out on which kind of information they light up on or loose interest. Or even better: just ask them during a break. If you have enough training material you can add a few more examples or exercises, discuss some visual schemes that you have in an appendix, etc. etc.

## Try to teach one thing at a time

Especially with Zope/Plone, there are a lot of concepts that students will have to grasp some time. We have CSS, HTML, Python, JavaScript, ZPT, METAL, TALES, ZCML, Generic Setup, Acquisition, component architecture, the Object Database, the ZMI, the Plone UI, etc. etc.

The irritating part with introducing any of these technologies is that when you try to teach one of them, two or three others will creep into the explanation as well. Some options:

1. Tell your students that they should ignore this and this and that you'll
   explain that part later while you're explaining X.

   Some students are very capable of learning this way, others will simply
   lock up inside and get distracted by this nagging thought about the 'other'
   stuff. If you can avoid parking concepts 'until later', please try:

2. Design your training in such a way that you start with concepts that
   are mostly 'stand alone' and from there build on the knowledge already
   there. (learning path)

   An example in the context of Zope is to first introduce the ZMI and object
   database, talk about objects in there, then continue to Zope Page Templates
   that are applied to the object in a context, talk about the TALES
   expressions inside ZPT and end with METAL macros.

   It's maybe old school and ugly, but you could explain most of
   ZPT/TALES/macros with students in the ZMI through the web without ever going
   to a command line or work in an editor. This is similar to:

3. Design isolated exercises/examples where you don't need multiple concepts
   at the same time.

These examples are not to promote teaching through the ZMI, but to be aware of stacking too many concepts to quickly in a training. :-)

## Attention Span

Both before and during a training it's vital to monitor the required attention span of the human mind.

When you prepare and write material, check your chapters or blocks for length, mental weight and structure.  Validate that a student can work through a chapter in 20-30 minutes. Provide an introduction, explain some theory, show/discuss examples, provide exercises and wrap up with for example references to more material.

Check that you don't try to teach multiple things at the same time and try to repeat your subject a few times so that it will stick more.

On a large scale, you can also improve the attention span for students during the traing day by keeping a cadence or rhythm.

1. At the beginning, show an agenda and discuss this with everybody present. In this agenda, plan breaks and lunch beforehand and mutually agree with your students.
2. Design a training day around multiple blocks of maximum 50-55 minutes and put a small break of 5-10 minutes after those blocks. Put a larger break in the middle of the morning with coffee etc. same in the afternoon, and of course the lunch break.
3. In each of those blocks, use a rhythm or structure to teach the subject. It's great if your training material already has this structure, then you can just flow along with the material. But if you're comfortable with this, you can also add more material and jump a bit through the material and select those exercises or examples that you think will appeal most to your current group.

The nice thing about teaching grown ups is that if you give them responsibility they will most of the time reward that with commitment. Tell your students when you discuss the agenda in the morning it's the general structure, but if you get to a tough subject and their heads are filled within half an hour: let them request a short break when they need it.

## The more you know, the less you know

As a trainer it is not your job or quality to know everything there is about the subject and to be able to answer any question your students have. It's your profesion to identify with your students, figure out how they learn best and provide the tools during that training day so that they will learn with the greatest ease and maximum recollection later on. And also that they'll have a great day or days.

The funny thing is that the more you know about a technical subject yourself, the more difficult it sometimes is to be emphatic and understand the learning difficulties of students. As long as you know 'a bit more' and you're able to transfer that knowledge, you're a trainer!

If you are nervous about getting 'difficult' technical questions from students during the day, try mentioning this in your introduction in the morning. It helps setting expectations:

> "I don't know a lot about Plone. But I know a bit more than you and I'm
> quite good at explaining and teaching stuff. So I'll probably not be able
> to answer all the questions you might have, but I have some very smart
> colleagues and a Plone community that will be able to answer those
> questions after the training and we'll figure it out."
