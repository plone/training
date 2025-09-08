---
myst:
  html_meta:
    "description": "Husky and lint-staged"
    "property=og:description": "Husky and lint-staged"
    "property=og:title": "Husky and lint-staged"
    "keywords": "Volto, Plone, Github"
---

# Husky and lint-staged

Husky is a tool that creates git hooks in yur repo. It allows you to run commands during the git lifecycle events (eg. when you commit or push your code to the server). It's useful for running linters, prettifiers, and tests before or while that events are happening.

Here you can find the documentation: https://github.com/typicode/husky

You configure Husky in your `package.json`:

```json
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "post-checkout": "yarnhook",
      "post-merge": "yarnhook",
      "post-rebase": "yarnhook"
    }
  },
```

It has the concept of hooks that are mapped to the git lifecycle events.

Lint staged allows you to define specific commands given the type of staged file.

```json
  "lint-staged": {
    "src/**/*.{js,jsx,ts,tsx,json}": [
      "npx eslint --max-warnings=0 --fix",
      "npx prettier --single-quote --write",
      "yarn test:husky"
    ],
    "src/**/*.{jsx}": [
      "yarn i18n"
    ],
    "theme/**/*.{css,less}": [
      "npx stylelint --fix"
    ],
    "src/**/*.{css,less}": [
      "npx stylelint --fix"
    ],
    "theme/**/*.overrides": [
      "npx stylelint --fix"
    ],
    "src/**/*.overrides": [
      "npx stylelint --fix"
    ]
  },
```

You can extend or modify the existing husky/lint-staged configuration in your project in order to match your needs.
