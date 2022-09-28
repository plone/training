# Configure a non-released add-on from an existing repository

We use `mrs-developer` tool to manage the development cycle.
This tool help us to pull the remote code and configure the current project to have the add-on(s) available for the build.

## Add mrs-developer dependency and related script

[Eric Brehault](https://github.com/ebrehault) ported this amazing Python tool,
which provides a way to pull a package from git and set it up as a dependency
for the current project codebase.

To facilitate addon development lifecycle we recommend using
[mrs-developer](https://www.npmjs.com/package/mrs-developer).

By doing this, you can develop both the project and the add-on product as if
they were both part of the current codebase. Once the add-on development is
done, you can publish the package to an npm repository.

```shell
yarn add mrs-developer
```

Then, in `package.json`:

```json hl_lines="2"
  "scripts": {
    "develop": "missdev --config=jsconfig.json --output=addons",
  }
```

We can configure `mrs-developer` to use any directory that you want. Here we
are telling it to create the directory `src/addons` and put the packages
managed by `mrs-developer` inside.

## mrs.developer.json

This is the configuration file that instructs `mrs-developer` from where it has
to pull the packages. So, create `mrs.developer.json` and add:

```json
{
  "acme-volto-foo-addon": {
    "package": "@acme/volto-foo-addon",
    "url": "git@github.com:acme/my-volto-addon.git",
    "path": "src"
  }
}
```

Then run:

```bash
yarn develop
```

Now the addon is found in `src/addons/`.

```{note}
`package` property is optional, set it up only if your package has a scope.
`src` is required if the content of your addon is located in the `src`
directory (but, as that is the convention recommended for all Volto add-on
packages, you will always include it)
```

If you want to know more about `mrs-developer` config options, please refer to
[its npm page](https://www.npmjs.com/package/mrs-developer).

## tsconfig.json / jsconfig.json

`mrs-developer` automatically creates this file for you, but if you choose not
to use mrs-developer, you'll have to add something like this to your
`tsconfig.json` or `jsconfig.json` file in the Volto project root:

```json
{
    "compilerOptions": {
        "paths": {
            "acme-volto-foo-addon": [
                "addons/acme-volto-foo-addon/src"
            ]
        },
        "baseUrl": "src"
    }
}
```

```{warning}
Please note that both `paths` and `baseUrl` are required to match your
project layout.
```

```{tip}
You should use the `src` path inside your package and point the `main` key
in `package.json` to the `index.js` file in `src/index.js`.
```

