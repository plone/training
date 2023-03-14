---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Using the code for the training

```{todo}
- Add info and link to repository of volto package
```

You can get the complete code for this training from GitHub.
- The backend add-on [ploneconf.site](https://github.com/collective/ploneconf.site)
- The frontend Volto app [volto-ploneconf](https://github.com/collective/volto-ploneconf)

## The code-packages

The add-on package [ploneconf.site](https://github.com/collective/ploneconf.site) contains the complete backend code for this training excluding exercises.
It is automatically downloaded from GitHub when you run `make build` in your Plone backend set up from {doc}`instructions`.

The frontend app [volto-ploneconf](https://github.com/collective/volto-ploneconf) holds the code for the frontend excluding exercises.
As explained in {doc}`instructions`, it is to be installed side by side with the backend in a folder `/frontend/`.
Optional frontend add-ons are configured here in `packages.json`.

The default branches of these repositories hold the code of the final chapter of the training.
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
The tag for the chapter {doc}`/mastering-plone/registry` is `registry`.
You can get it with {command}`git checkout registry`.

## Moving from chapter to chapter

To change the code to the state of the next chapter checkout the tag for the next chapter:

```shell
git checkout views_3
```

If you made any changes to the code you have to get them out of the way first. This involves two things.

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

```{todo}
Update list of tags in backend add-on.
```

These are the tags of the backend add-on for which there is code:


| Chapter                        | Tag-Name                 |
| ------------------------------ | ------------------------ |
| {doc}`about_mastering`         |                          |
| {doc}`intro`                   |                          |
| {doc}`installation`            |                          |
| {doc}`case`                    |                          |
| {doc}`features`                |                          |
| {doc}`anatomy`                 |                          |
| {doc}`configuring_customizing` |                          |
| {doc}`theming`                 |                          |
| {doc}`extending`               |                          |
| {doc}`add-ons`                 |                          |
| {doc}`dexterity`               |                          |
| {doc}`buildout_1`              | `buildout_1`             |
| {doc}`eggs1`                   | `eggs1`                  |
| {doc}`views_1`                 | `views_1`                |
| {doc}`zpt`                     | `zpt`                    |
| {doc}`zpt_2`                   | `zpt_2`                  |
| {doc}`views_2`                 | `views_2`                |
| {doc}`views_3`                 | `views_3`                |
| {doc}`behaviors_1`             | `behaviors_1`            |
| {doc}`viewlets_1`              | `viewlets_1`             |
| {doc}`api`                     |                          |
| {doc}`ide`                     |                          |
| {doc}`custom_search`           |                          |
| {doc}`events`                  | `events`                 |
| {doc}`user_generated_content`  | `user_generated_content` |
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

This section is for **trainers** who want to update the code after changing something in the training documentation.

The current model uses only one branch of commits and maintains the integrity through rebases.

It goes like this:

- Only one branch (main)

- Write the code for chapter 1 and commit.

- Write the code for chapter 2 and commit.

- Add the code for chapter 3 and commit.

- You realize that something is wrong in chapter 1.

- You branch off at the commit id for chapter 1.
  `git checkout -b temp 123456`

- You change the code and do a commit.
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
