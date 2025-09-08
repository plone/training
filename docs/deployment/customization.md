---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Customized Use

We intend that you should be able to make most changes by changing default variable settings in your `local_configure.yml` file.
We've made a serious effort to make sure that all those settings are documented in the `Plone's Ansible Playbook <https://5.docs.plone.org/external/ansible-playbook/docs/index.html>` documentation.

For example, if you want to change the time at which backup occurs,
you can check the doc and discover that we have a [plone-backup-at setting](https://5.docs.plone.org/external/ansible-playbook/docs/plone.html#plone-backup-at).

The default setting is:

```yaml
plone_backup_at:
  minute: 30
  hour: 2
  weekday: "*"
```

That's 02:30 every morning.

To make it 03:57 instead, use:

```yaml
plone_backup_at:
  minute: 57
  hour: 3
  weekday: "*"
```

in your `local_configure.yml` file.

## Common Customization Points

Let's review the settings that are commonly changed.

### Plone Setup

#### Eggs And Versions

You're likely to want to add Python packages to your Plone installation to enable add-on functionality.

Let's say you want to add [collective.easyform](https://pypi.org/project/collective.easyform) and [webcouturier.dropdownmenu](https://pypi.org/project/webcouturier.dropdownmenu/).

Add to your `local_configure.yml`:

```yaml
plone_additional_eggs:
    - collective.easyform
    - webcouturier.dropdownmenu
```

If you add eggs, you should nearly always specify their versions:

```yaml
plone_additional_versions:
  - "collective.easyform = 2.0.0b2"
  - "webcouturier.dropdownmenu = 3.0.1"
```

That takes care of packages that are available on the [Python Package Index](https://pypi.org/).
What if your developing packages via git?

```yaml
plone_sources:
  -  "some.other.package = git git://example.com/git/some.other.package.git rev=1.1.5"
```

There's more that you can do with the `plone_sources` setting.
See the docs!

#### Buildout From Git Repository

It's entirely possible that the buildout created by the playbook won't be adequate to your needs.

If that's the case, you may check out your whole buildout directory via git:

```yaml
buildout_git_repo: https://github.com/plone/plone.com.ansible.git
buildout_git_version: master
```

Make sure you check the [documentation on this setting](https://5.docs.plone.org/external/ansible-playbook/docs/plone.html#plone-buildout-git-repo).

Even if you use your own buildout, you'll need to make sure that some of the playbook settings reflect your configuration.

#### Running Buildout And Restarting Clients

By default, the playbook tries to figure out if {command}`buildout` needs to be run.
If you add an egg, for example, the playbook will run buildout to make the buildout-controlled portions of the installation update.

If you don't want that behavior, change it:

```yaml
plone_autorun_buildout: no
```

If `autorun` is turned off, you'll need to log in to run buildout after it completes the first time.
(When you first run the playbook on a new server, buildout will always run.)

If automatically running buildout bothers you, automatically restarting Plone after running buildout will seem foolish.
You may turn it off:

```yaml
plone_restart_after_buildout: no
```

That gives you the option to log in and run the client restart script.
If you're conservative, you'll first try starting and stopping the reserved client.

```{note}
By the way, if buildout fails, your playbook run will halt.
You don't need to worry that an automated restart might occur after a failed buildout.
```

(web-hosting-options)=

### Web Hosting Options

It's likely that you're going to need to make some changes in nginx configuration.
Most of those changes are made via the `webserver_virtualhosts` setting.

`webserver_virtualhosts` should contain a list of the hostnames you wish to support.
For each one of those hostnames, you may make a variety of setup changes.

The playbook automatically creates a separate host file for each host you configure.

Here's the default setting:

```yaml
webserver_virtualhosts:
  - hostname: "{{ inventory_hostname }}"
    default_server: yes
    zodb_path: /Plone
```

This connects your inventory hostname for the server to the /Plone directory in the ZODB.

A more realistic setting might look something like:

```yaml
webserver_virtualhosts:
  - hostname: plone.org
    default_server: yes
    aliases:
      - www.plone.org
    zodb_path: /Plone
    port: 80
    protocol: http
    client_max_body_size: 4M
  - hostname: plone.org
    zodb_path: /Plone
    address: 92.168.1.150
    port: 443
    protocol: https
    certificate_file: /thiscomputer/path/mycert.crt
    key_file: /thiscomputer/path/mycert.key
```

Here we're setting up two separate hosts, one for `http` and one for `https`.
Both point to the same ZODB path, though they don't have to.

The https host item also refers to a key/certificate file pair on the Ansible host machine.
They'll be copied to the remote server.

Alternatively, you could specify use of certificates already on the server:

```yaml
webserver_virtualhosts:
  - hostname: ...
    ...
    certificate:
      key: /etc/ssl/private/ssl-cert-snakeoil.key
      crt: /etc/ssl/certs/ssl-cert-snakeoil.pem
```

```{caution}
One hazard for the current playbook web server support is that it does **not** delete old host files.
If you had previously set up `www.mynewclient.com` and then deleted that item from the playbook host list, the nginx host file would remain.
Log in and delete it if needed.
Yes, this is an exception to the "don't login to change configuration rule".
```

```{seealso}
For an example of using free Let's Encrypt certificates with certbot and auto-renewal, see {doc}`letsencrypt-certbot`.
```

#### Extra tricks

There are a couple of extra setting that allow you to do extra customization if you know nginx directives.
For example:

```yaml
- hostname: plone.com
  protocol: http
  extra: return 301 https://$server_name$request_uri;
```

This is a *redirect to https*.
It takes advantage of the fact that if you do not specify a zodb_path,
the playbook will not automatically create a location stanza with a rewrite and proxy_pass directives.

### Mail Relay

Some cloud server companies do not allow servers to directly send mail to standard mail ports.
Instead, they require that you use a *mail relay*.

This is a typical setup:

```yaml
mailserver_relayhost: smtp.sendgrid.net
mailserver_relayport: 587
mailserver_relayuser: yoursendgriduser
mailserver_relaypassword: yoursendgridpassword
```

### Bypassing Components

Remember our stack diagram?
The only part of the stack that you're stuck with is Plone.

All the other components my be replaced.
To replace them, first prevent the playbook from installing the default component.
Then, use a playbook of your own to install the alternative component.

For example, to install an alternative to the Postfix mail agent, add:

```yaml
install_mailserver: no
```

```{note}
If you choose not to install the HAProxy, varnish or Nginx, you take on some extra responsibilities.
You're going to need to make sure in particular that your port addresses match up.
If, for example, you replace HAProxy, you will need to point varnish to the new load-balancer's frontend.
You'll need to point the new load balancer to the ZEO clients.
```

### Multiple Plones Per Host

We've covered the simple case of having one Plone server installed on your server.
In fact, you may install additional Plones.

To do so, you create a list variable `playbook_plones` containing all the settings that are specific to one or more of your Plone instances.

Nearly all the plone\_\* variables, and a few others like loadbalancer_port and webserver_virtualhosts may be set in playbook_plones.
Here's a simple example:

```yaml
playbook_plones:
  - plone_instance_name: primary
    plone_zeo_port: 8100
    plone_client_base_port: 8081
    loadbalancer_port: 8080
    webserver_virtualhosts:
      - hostname: "{{ inventory_hostname }}"
        aliases:
          - default
        zodb_path: /Plone
  - plone_instance_name: secondary
    plone_zeo_port: 7100
    plone_client_base_port: 7081
    loadbalancer_port: 7080
    webserver_virtualhosts:
      - hostname: www.plone.org
        zodb_path: /Plone
```

Note that you're going to have to specify a minimum of an instance name, a zeo port and a client base port (the address of client1 for this Plone instance.)

You may specify up to four items in your `playbook_plones` list.
If you need more, see the docs as you'll need to make a minor change in the main playbook.

### The Plone Role -- Using It Independently

For big changes, you may find that the full playbook is of little or no use.
In that case, you may still wish to use Plone's Ansible Role independently, in your own playbooks.

The [Plone server role](https://github.com/plone/ansible.plone_server) is maintained separately, and may become a role in your playbooks if it works for you.
