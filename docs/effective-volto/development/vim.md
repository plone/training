---
myst:
  html_meta:
    "description": "vim and neovim integration"
    "property=og:description": "vim and neovim integration"
    "property=og:title": "vim and neovim integration"
    "keywords": "Volto, Plone, Vim, Development"
---

# vim and neovim integration

For code linting and formatting, Volto relies on a working configuration of
ESLint and Prettier (as an ESlint plugin). This makes it possible to integrate
automated code linting and formatting in any compatible editor.

One possible way to integrate these features with Vim and NeoVim is to use the
[ALE](https://github.com/dense-analysis/ale).

A working Vim setup might look like this:

```vim

Plug 'w0rp/ale'

"...

let g:ale_fixers = {
      \   'python': [
      \       'black',
      \       'isort',
      \       'trim_whitespace',
      \       'remove_trailing_lines',
      \   ],
      \   'javascript': ['eslint'],
      \   'css': ['prettier', 'stylelint'],
      \   'less': ['prettier', 'stylelint'],
      \   'json': ['prettier']
      \}

let g:ale_linters = {
      \ 'python': ['flake8'],
      \ 'javascript': ['eslint'],
      \ 'xml': ['xmllint'],
      \ 'css': ['stylelint'],
      \ 'less': ['stylelint']
      \ }

```

Note: you should not install eslint standalone on your computer. Volto projects
automatically install it for you, and ALE will detect it in the Volto project's
`node_modules`. Generated Volto projects also include a `.eslintrc.js` file in
the root, so you should start Vim from the Volto project root, so that ALE will
use the proper `eslint` and the `eslint` process will read the proper settings.

A short checklist for proper integration:

- invalid imports are identified
- missing imports, broken syntax, invalid react code is flagged
- JSX and JavaScript code is automatically formatted, on save
