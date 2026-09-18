---
myst:
  html_meta:
    "description": "Code of the training – where, what, how to update"
    "property=og:description": "Code of the training – where, what, how to update"
    "property=og:title": "The code for the training 'Mastering Plone development'"
    "keywords": "code, setup, development environment"
---

(code-label)=

# The code for the training

You can get the complete code for this training from GitHub.
See {doc}`installation`.

The main training project is [mastering-plone-project](https://github.com/collective/mastering-plone-project).

The add-on developed in chapter 31 is [mastering-plone-votable-add-on](https://github.com/collective/mastering-plone-votable-add-on).

Both of these repositories are monorepos which contain:
- a backend package
- a frontend package
- Makefile commands to use during development
- configuration for automatic continuous integration workflows on GitHub


## Get the code for a particular chapter

The default branches of these repositories hold the code of the final chapter of the training.
Each chapter that adds code to the package has a tag that can be used to get the code for that chapter.

To use the code for a certain chapter, you need to checkout the appropriate tag for the chapter.
The package will then contain the complete code for that chapter (excluding exercises).

If you want to add the code for the chapter yourself, you have to check out the tag of the previous chapter.
Each chapter has a card at the top which tells you which tags to use.
The full list of tags is also shown in a table below.


### How to check out a tag of a git repository

You have two options: terminal or source editor (for example VSCode).

1. Terminal
   - `cd` to the folder which contains the repository (`mastering-plone-project`).
   - To check out the tag `talks`: `git checkout talks`
2. VSCode
   - Open `mastering-plone-project` in VSCode.
   - If not installed, install the extension "GitHub Pull Requests".
   - Open the source control sidebar.
   - Select the tag.
     ```{figure} _static/vscode_git.png
     Check out a tag
     ```


## Move from chapter to chapter

To change the code to the state of the next chapter, check out the tag for the next chapter:

```shell
git checkout views_3
```

If you made any changes to the code, you have to get them out of the way first. This involves two things.

```{warning}
Make sure you have no new files or changes in the folder structure of `mastering-plone-project` that you want to keep, because the following will delete them!
```

```shell
git clean -fd
git stash
```

This does two things:

1. It deletes any files that you added and are not part of the package.
1. It will move away changes to files that are part of the package but not delete them. 
   You can get them back later.
   You should learn about the command {command}`git stash` before you try to reapply stashed changes.

## Tags

These are the tags of the repositories `mastering-plone-project` and `mastering-plone-votable-add-on` for which there is code:


| Chapter                        | Tag name                 | Package |
| ------------------------------ | ------------------------ | --- |
| {doc}`about_mastering` | |
| {doc}`intro` | |
| {doc}`case` | |
| {doc}`what_is_plone` | |
| {doc}`installation` | initial | mastering-plone-project |
| {doc}`features` | |
| {doc}`configuring_customizing` | |
| {doc}`add-ons` | addons | mastering-plone-project |
| {doc}`extending` | |
| {doc}`dexterity` | |
| {doc}`volto_development` | |
| {doc}`dexterity_2_talk` | talks | mastering-plone-project |
| {doc}`dexterity_reference` | |
| {doc}`volto_overrides` | overrides | mastering-plone-project |
| {doc}`volto_talkview` | talkview | mastering-plone-project |
| {doc}`behaviors_1` | behaviors_1 | mastering-plone-project |
| {doc}`volto_frontpage` | frontpage | mastering-plone-project |
| {doc}`api` | |
| {doc}`events` | events | mastering-plone-project |
| {doc}`registry` | vocabularies | mastering-plone-project |
| {doc}`custom_search` | search | mastering-plone-project |
| {doc}`volto_testing` | testing | mastering-plone-project |
| {doc}`dexterity_3` | schema | mastering-plone-project |
| {doc}`upgrade_steps` | upgrade_steps | mastering-plone-project |
| {doc}`volto_listing_variation` | listing_variation | mastering-plone-project |
| {doc}`searchable` | searchable | mastering-plone-project |
| {doc}`volto_components_sponsors` | sponsors | mastering-plone-project |
| {doc}`custom_block` | block | mastering-plone-project |
| {doc}`user_generated_content` | user_generated_content | mastering-plone-project |
| {doc}`relations` | relations | mastering-plone-project |
| {doc}`voting-story/index` | initial | mastering-plone-votable-add-on |
| {doc}`voting-story/behaviors_2` | behaviors | mastering-plone-votable-add-on |
| {doc}`voting-story/endpoints` | endpoints | mastering-plone-votable-add-on |
| {doc}`voting-story/volto_actions` | actions | mastering-plone-votable-add-on |
| {doc}`voting-story/permissions` | permissions | mastering-plone-votable-add-on |
| {doc}`deployment_code` | |
