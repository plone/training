# Trainer: Preparation

Preparation of a Mastering Plone Development Training

You are about to give a training. Here are some tips what to prepare before.


## Technical set up to do before a training

- Update the Plone and Volto versions in [mastering-plone-project](https://github.com/collective/mastering-plone-project).
- If you do only a part of the training, prepare an installation with the steps of the previous chapters.
See {doc}`code` for more information.


## Update the example code

This section is for trainers who want to update the example project code to match a change in the training documentation.

The tags for each chapter described in {doc}`code` are actually branches, so that they can more easily be updated.

If you need to change code in the middle of the training, you have to rebase all the branches that come after it, so that they include the updated code.

That looks like this:

1. Check out the branch you need to update.
2. Commit the changes there. (You can use `git commit --amend` if you want to rewrite the commit instead of adding a new one.)
3. Check out the next branch. Rebase it onto the previous one.
4. Force push the updated branch to GitHub.
5. Continue checking out and rebasing each subsequent branch until you get to `main`.

The final result should look like this:

```{figure} _static/code_tree.png
:align: center
```
