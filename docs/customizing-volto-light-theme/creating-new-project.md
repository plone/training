---
myst:
  html_meta:
    'description': 'Learn How to customize the Footer of the page'
    'property=og:description': 'Learn How to customize the Footer of the page'
    'property=og:title': 'Footer customization'
    'keywords': 'Plone, Volto, Training, Theme, Footer'
---

# Creating a New Project with Plone and Volto

Follow the steps below to create a new project using Plone 6 and Volto. This guide assumes you have `pipx` installed.

### Step 1: Install CookiePlone

First, install `cookieplone`—a tool for setting up new Plone projects—using `pipx`:

```shell
pipx install cookieplone
```

### Step 2: Create the Project

Once Cookieplone is installed, run the command below to start the project creation process:

```shell
pipx run cookieplone
```

You'll be prompted with several questions.
For this tutorial, you should accept the default values by pressing {kbd}`Enter`, except for the following.
[Insert exceptions here.]

Here are the prompts you will encounter:

```console
[1/17] Project Title (Project Title): my-vlt-project
[2/17] Project Description (A new project using Plone 6.): My Project
[3/17] Project Slug (Used for repository id) (my-vlt-project): my-project
[4/17] Project URL (without protocol) (my-project.example.com): my-project.example.com
[5/17] Author (Plone Foundation): <your name>
[6/17] Author E-mail (collective@plone.org):
[7/17] Should we use prerelease versions? (No):
[8/17] Plone Version (6.0.13):
[9/17] Volto Version (18.0.0):
[10/17] Python Package Name (my.project):
[11/17] Volto Addon Name (volto-my-project):
```

After answering these prompts, the project will be created.

### Step 3: Install Dependencies

Once the project is created, you need to install dependencies for both the backend and frontend.

1. **Install the backend and frontend dependencies**:

```shell
make install
```

2. **Start the backend**:

```shell
make backend-start
```

3. **Start the frontend**:

```shell
make frontend-start
```

### Step 4: Commit the Initial Changes

To commit your initial project files to Git, run the following commands:

```shell
git add .
git commit -m 'initial-commit' --no-verify
```

### Summary

- Use `cookieplone` to create a new Plone project.
- Use `make install` to install dependencies.
- Start backend with `make backend-start` and frontend with `make frontend-start`.
- Commit the initial files to version control using Git.

That's it! You've successfully set up your Plone project with Volto.
