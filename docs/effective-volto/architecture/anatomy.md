# Volto Anatomy

There are two ways of running Volto:

- standalone
- as a Volto project

Running Volto standalone is simple: make a clone of Volto from Github, run
`yarn` to download its dependencies, then `yarn start` to simply start Volto.
This is useful for developing Volto, but it is not the way to use it, if you
want to develop your own custom Volto project.

The second method of running Volto is to use the Volto App generator and
bootstrap (based on a fixed scaffolding) a new Javascript package that can
piggy-back on Volto and treat it as a library. We call this the "Volto
project".


The next steps, after bootstrapping the new Volto project, is to make it your
own. The community has settled, for now, to use [Yarn
Classic](https://classic.yarnpkg.com/lang/en/) as the default Javascript
package manager, so, to add dependencies on new third-party
Javascript packages, you'd run:

```
yarn add react-slick
```

to make the react-slick library available to your Volto project.

You can use this Volto Project scaffold to develop a complete Volto-powered
website, without needing to do anything else. You can use the `<root>/src/` folder to
host your custom Javascript code and the `<root>/theme` folder to customize the
Volto theme and create your custom look and feel.

But to enable a greater modularity and reusability of code, you can create new
Javascript packages that are deeply integrated with Volto, the so-called "Volto
addons".
