---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Using the code for the training

You can get the complete code for this training from [GitHub](https://github.com/collective/ploneconf.site).

## The code-package

The package [ploneconf.site](https://github.com/collective/ploneconf.site) contains the complete code for this training excluding exercises.
It is automatically downloaded from GitHub when you run buildout.

The master branch of that repository holds the code of the final chapter of this training.
Each chapter that adds code to the package has a tag that can be used to get the code for that chapter.

## Getting the code for a certain chapter

To use the code for a certain chapter you need to checkout the appropriate tag for the chapter.
The package will then contain the complete code for that chapter (excluding exercises).

If you want to add the code for the chapter yourself you have to checkout the tag for the previous chapter.

Here is an example:

```shell
git checkout views_2
```

The names of the tags are the same as the URL of the chapter.
The tag for the chapter {doc}`registry` is `registry`.
You can get it with {command}`git checkout registry`.

## Moving from chapter to chapter

To change the code to the state of the next chapter checkout the tag for the next chapter:

```shell
git checkout views_3
```

If you made any changes to the code you have to get them out of the way first. This inviolved two things

```{warning}
Make sure you have no new files or changes in the folder structure of `ploneconf.site` that you want to keep because the following will delete them!!!
```

```shell
git clean -fd
git stash
```

This does two things:

1. It deletes any files that you added and are not part of the package.
2. It will move away changes to files that are part of the package but not delete them. You can get them back later. You should learn about the command {command}`git stash` before you try reapply stashed changes.

## Tags

These are the tags for which there is code:

| Chapter                        | Tag-Name                 |
| ------------------------------ | ------------------------ |
| {doc}`about_mastering`         |                          |
| {doc}`intro`                   |                          |
| {doc}`installation`            |                          |
| {doc}`case`                    |                          |
| {doc}`features`                |                          |
| {doc}`anatomy`                 |                          |
| {doc}`plone5`                  |                          |
| {doc}`configuring_customizing` |                          |
| {doc}`theming`                 |                          |
| {doc}`extending`               |                          |
| {doc}`add-ons`                 |                          |
| {doc}`dexterity`               |                          |
| {doc}`buildout_1`              | `buildout_1`             |
| {doc}`eggs1`                   | `eggs1`                  |
| {doc}`export_code`             | `export_code`            |
| {doc}`views_1`                 | `views_1`                |
| {doc}`zpt`                     | `zpt`                    |
| {doc}`zpt_2`                   | `zpt_2`                  |
| {doc}`views_2`                 | `views_2`                |
| {doc}`views_3`                 | `views_3`                |
| {doc}`testing`                 | `testing`                |
| {doc}`behaviors_1`             | `behaviors_1`            |
| {doc}`viewlets_1`              | `viewlets_1`             |
| {doc}`api`                     |                          |
| {doc}`ide`                     |                          |
| {doc}`dexterity_2`             | `dexterity_2`            |
| {doc}`custom_search`           |                          |
| {doc}`events`                  | `events`                 |
| {doc}`user_generated_content`  | `user_generated_content` |
| {doc}`resources`               | `resources`              |
| {doc}`thirdparty_behaviors`    | `thirdparty_behaviors`   |
| {doc}`dexterity_3`             | `dexterity_3`            |
| {doc}`relations`               | `relations`              |
| {doc}`registry`                | `registry`               |
| {doc}`frontpage`               | `frontpage`              |
| {doc}`eggs2`                   |                          |
| {doc}`behaviors_2`             |                          |
| {doc}`viewlets_2`              |                          |
| {doc}`reusable`                |                          |
| {doc}`embed`                   |                          |
| {doc}`deployment_code`         |                          |
| {doc}`deployment_sites`        |                          |

## Updating the code-package

This section is for trainers who want to update the code in {py:mod}`ploneconf.site` after changing something in the training documentation.

The current model uses only one branch of commits and maintains the integrity through rebases.

It goes like this:

- Only one one branch (master)

- Write the code for chapter 1 and commit

- Write the code for chapter 2 and commit

- Add the code for chapter 3 and commit

- You realize that something or wrong in chapter 1

- You branch off at the commit id for chapter 1
  `git checkout -b temp 123456`

- You cange the code and do a commit.
  `git commit -am 'Changed foo to also do bar'`

- Switch to master and rebase on the branch holding the fix which will inject the new commit into master at the right place:
  `git checkout master`
  `git rebase temp`
  That inserts the changes into master in the right place. You only maintain a master branch that is a sequence of commits.

- Then you need to update your chapter-docs to point to the corresponding commit ids:

  - chapter one: `git checkout 121431243`
  - chapter two: `git checkout 498102980`

Additionally you can

- set tags on the respective commits and move these tags. This way the docs do not need to be changed when the code changes.
- squash the commits between the chapters to every chapter is one commit.

To move tags after changes you do:

- Move a to another commit: `git tag -a <tagname> <commithash> -f`
- Move the tag on the server `git push --tags -f`

The final result should look like this:

```{figure} ../_static/code_tree.png
:align: center
```
