---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-installation-label)=

# Installation & Setup

(plone5-installation-plone-label)=

## Installing Plone

The following table shows the Python versions required by Plone from version 3.x to 5.2.x:

| Plone | Python         |
| ----- | -------------- |
| 3.x   | 2.4            |
| 4.0.x | 2.6            |
| 4.1.x | 2.6            |
| 4.2.x | 2.6 or 2.7     |
| 4.3.x | 2.7            |
| 5.0.x | 2.7            |
| 5.1.x | 2.7.9          |
| 5.2.x | 2.7.14 or 3.6+ |

(Hopefully you won't have to deal with any Plone sites older than version 4.3.x)

Plone 5.x requires a working Python 2.7 (or Python 3.6+ for Plone 5.2.x) and other system tools that not every OS provides.
The installation of Plone is different on every system.
Here are some ways that Python can be installed:

- use a Python that comes pre-installed in your operating system (most Linux Distributions and macOS have one)
- use the [python buildout](https://github.com/collective/buildout.python)
- building Linux packages
- [Homebrew](https://brew.sh) (macOS)
- PyWin32 (Windows)

Most developers use their primary system to develop Plone.
For complex setups they often use Linux virtual machines.

- macOS: Use the system python and [Homebrew](https://brew.sh) for some missing Linux tools.
- Linux: Depending on your Linux flavor you might have to install Python 3.7 yourself and install some tools.
- Windows: Alan Runyan (one of Plone's founders) uses it. A downside: Plone seems to be running slower on Windows.

Plone offers multiple options for being installed:

1. Unified installers (all 'nix, including macOS)
2. A Vagrant/VirtualBox install kit (all platforms)
3. A VirtualBox Appliance
4. A [Windows installer](https://github.com/plone/WinPloneInstaller)
5. Use your own Buildout

Visit the [download page](https://plone.org/download) to see all the options.

```{only} not presentation
For the training you will use option 2 or 5 to install and run Plone.
We will create our own Buildout and extend it as we wish.
If you choose to do so you will run it in a Vagrant machine.

For your own first experiments we recommend option 1 or 2 (if you have a Windows laptop or encounter problems).
Later on you should be able to use your own Buildout (we will cover that later on).
```

```{only} presentation
For the training we will use option 2 or 5 to install and run Plone.
```

```{seealso}
- <https://5.docs.plone.org/manage/installing/installation.html>
```

(plone5-installation-hosting-label)=

## Hosting Plone

```{only} not presentation
If you want to host a real live Plone site yourself then running it from your laptop is not a viable option.
```

You can host Plone...

- with one of many professional [hosting providers](https://plone.org/providers)
- on a virtual private server
- on dedicated servers

See all the ways you can [set up Plone](https://plone.org/download)
```{seealso}
- Plone Installation Requirements: <https://5.docs.plone.org/manage/installing/requirements.html>
```

(plone5-installation-prod-deploy-label)=

## Production Deployment

The way we are setting up a Plone site during this class may be adequate for a small site
— or even a large one that's not very busy — but you are likely to want to do much more if you are using Plone for anything demanding.

- Using a production web server like Apache or Nginx for URL rewriting, SSL and combining multiple, best-of-breed solutions into a single web site.
- Reverse proxy caching with a tool like Varnish to improve site performance.
- Load balancing to make best use of multiple core CPUs and even multiple servers.
- Optimizing cache headers and Plone's internal caching schemes with plone.app.caching.

And, you will need to learn strategies for efficient backup and log file rotation.

All these topics are introduced in [Guide to deploying and installing Plone in production](https://5.docs.plone.org/manage/deploying/index.html).
