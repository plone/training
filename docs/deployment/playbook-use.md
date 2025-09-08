---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Basic Use Of The Playbook

## Local Configuration File

For a quick start, copy one of the {file}`sample-*.yml` files to {file}`local-configure.yml`.

The {file}`local-configure.yml` file is automatically included in the main playbook if it's found.

```shell-session
cp sample-small.yml local-configure.yml
```

Now, edit the {file}`local-configure.yml` file to set some required variables:

admin_email

> The server admin's email.
> Probably yours.
> This email address will receive system notices and log analysis messages.

plone_initial_password

> The initial administrative password for the Zope/Plone installation.
> Not the same as the server shell login.

muninnode_query_ips

> Are you going to run a Munin monitor on a separate machine?
> (And, if not, why not?)
> Specify the IP address of the monitor machine.
> Or ...

install_muninnode

> Remove the "#" on the `install_muninnode: no` line if you are not using a Munin monitor.

You're also nearly certainly going to want to specify a Plone version via the `plone_version` setting.
You should be able to pick any version from 4.3.x or 5.x.x.
Note that the value for this variable must be quoted to make sure it's interpreted as a string.

## Use With Vagrant

If you've installed Vagrant/VirtualBox, you're ready to test.
Since Vagrant manages the connection, you don't need to create a inventory file entry.

There is a Vagrant setup file, {file}`Vagrantfile`, included with the playbook,
you may open a command-line prompt, make sure your Ansible virtualenv is activated, and type:

```shell-session
vagrant up
```

```{note}
The first time you use a "box" it will be downloaded.
These are large downloads; expect it to take some time.
```

```{note}
Instructor note:
Having several students simultaneously downloading a VirtualBox over wifi or a slow connection is a nightmare.
Have a plan.
```

Once you've run {program}`vagrant up`, running it again will not automatically provision the VirtualBox.
In this case, that means that Ansible is not run.

If you change your Ansible configuration, you'll need to use:

```shell-session
vagrant provision
```

```{note}
When you run `up` or `provision`, watch to make sure it completes successfully.
Note that failures for particular plays do not mean that Ansible provisioning failed.
The playbook has some tests that fail if particular system features are unavailable.
Those test failures are ignored and the provisioning continues.
The provisioning has failed if an error causes it to stop.
```

An example of an ignored failure:

```
TASK [varnish : Using systemd?] ************************************************
fatal: [trusty]: FAILED! => {"changed": true, "cmd": "which systemctl && systemctl is-enabled varnish.service", "delta": "0:00:00.002085", "end": "2016-09-14 17:50:06.385887", "failed": true, "rc": 1, "start": "2016-09-14 17:50:06.383802", "stderr": "", "stdout": "", "stdout_lines": [], "warnings": []}
...ignoring
```

### Vagrant Ports

The Vagrant setup (in {file}`Vagrantfile`) maps several ports on the guest machine (the VirtualBox) to the host box.
The general scheme is to forward a host port that is 1000 greater than the guest port.

For example, the load-balancer monitor port on the guest server is `1080`.
On the host machine, that's mapped by ssh tunnel to 2080.

We may see the HAProxy monitor at `http://localhost:2080/admin`.

The guest's `http` port (80) is reached via the host machine's port 1080 --
but that isn't actually useful due to URL rewriting for virtual hosting.

If you take a look at `http://localhost:1080` from your host machine, you'll see the default Plone site,
but style sheets, JavaScript and images will all be missing.

Instead, look at the load-balancer port (8080 on the guest, 9080 on the host) to see your ZODB root.

### Some Quick Vagrant

```shell-session
vagrant up                 # bring up the VirtualBox
vagrant provision          # provision the VirtualBox
vagrant up --no-provision  # bring the box up without provisioning
vagrant halt               # stop and save the state of the VirtualBox
vagrant destroy            # stop and destroy the box
vagrant ssh                # ssh to the guest box
```

To each of the these commands, you may add an ID to pick one of the boxes defined in Vagrantfile.
Read Vagrantfile for the IDs.

For example, `centos7` is the ID for a CentOS box.

```shell-session
vagrant up centos7
```

## Run Against Cloud

Let's provision a cloud server.
Here are the facts we need to know about our cloud server:

hostname

> A new server may or may not have a DNS host entry.
> If it does, use that hostname.
> If not, invent one and be prepared to supply an IP address.

login ID

> The user ID of a system account that is either the superuser (root) or is allowed to use {command}`sudo` to issue arbitrary commands as the superuser.

password

> If your cloud-hosting company does not set up the user account for ssh-keypair authentication, you'll need a password.
> Even if your account does allow passwordless login, it may still require a password to run {command}`sudo`.
>
> If your cloud-hosting company sets up a root user and password, it's a good practice to login (or use Ansible) to create a new, unprivileged user with sudo rights.
> Cautious sysadmins will also disable root login via ssh.

connection details

> If you don't have a DNS host record for your server, you'll need to have its IP address.
> If ssh is switched to an alternate port, you'll need that port number.

With that information, create an inventory file (if none exists) and create a host entry in it.

We use {file}`inventory.cfg` for an inventory file.

A typical inventory file:

```
www.mydomain.co.uk ansible_host=192.168.1.1 ansible_user=steve
```

You may leave off the `ansible_host` if the name supplied matches the DNS host record.
You may leave off the `ansible_user` if your user ID is the same on the server.

An inventory file may have many entries.
You may run Ansible against one, two, all of the hosts in the inventory file, or against alias groups like "plone-servers".

See [Ansible's inventory documentation](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html)
for information on grouping host entries and for more specialized host settings.

Now, let's make things easier for us going forward by creating an {file}`ansible.cfg` file in our playbook directory.

In that text file, specify the location of your inventory file:

```cfg
[defaults]
inventory = ./inventory.cfg
roles_path = ./roles
```

### Smoke Test

Now, let's see if we can use Ansible to connect to the remote machine that we've specified in our inventory.

Does the new machine allow an ssh key login, then you ought to be able to use the command:

```shell-session
ansible www.mydomain.co.uk -a "whoami"
```

If you need a password for login, try:

```shell-session
ansible www.mydomain.co.uk -a "whoami" -k
```

And, if that fails, ask for verbose feedback from Ansible:

```shell-session
ansible www.mydomain.co.uk -a "whoami" -k -vvvv
```

Now, let's test our ability to become superuser on the remote machine.

If you have passwordless sudo, this should work:

```shell-session
ansible www.mydomain.co.uk -a "whoami" -k --become
# omit the "-k" if you need no login password.
```

If sudo requires a password, try:

```shell-session
ansible www.mydomain.co.uk -a "whoami" -k --become -K
# again,  omit the "-k" if you need no login password.
```

If all that works, congratulations, you're ready to use Ansible to provision the remote machine.

```{note}
The "become" flag tells Ansible to carry out the action while becoming another user on the remote machine.

If no user is specified, we become the superuser.

If no method is specified, it's done via {command}`sudo`.

You won't often use the `--become` flag because the playbooks that need it specify it themselves.
```

### Diagnosing SSH Connection Failures

If Ansible has trouble connecting to the remote host, you're going to get a message like:

```ruby
myhost | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh.",
    "unreachable": true
}
```

If this happens to you, try adding `-vvv` to the {program}`ansible` or {program}`ansible-playbook` command line.

The extra information may -- or may not -- be useful.

The real test is to use a direct ssh login to get the ssh error.

There's a pretty good chance that the identity of the remote host will have changed, and ssh will give you a command line to clean it up.

### Running The Playbook

We're ready to run the playbook.

Make sure you're logged to your ansible-playbook directory and that you've activated the Python virtualenv that includes Ansible.

If you're targetting all the hosts in your inventory, running the playbook may be as easy as:

```shell-session
ansible-playbook playbook.yml
```

If you need a password for ssh login, add `-k`.

If you need a password for sudo, add `-K`.

If you need a password for both, add "-k -K".

If you want to target a particular host in your inventory, add `--limit=hostname`. Note that the `--limit` parameter is a search term; all hostnames matching the parameter will run.

```{note}
As with Vagrant, check the last message to make sure it completes successfully.
When first provisioning a server, timeout errors are more likely.

If you have a timeout, run the playbook again.
Note that failures for particular plays do not mean that Ansible provisioning failed.
```

### Firewalling

Running the Plone playbook does not set up server firewalling.
That's handled via a separate playbook, included with the kit.

We've separated the functions because many sysadmins will wish to handle firewalling themselves.

If you wish to use our firewall playbook, use the command:

```shell-session
ansible-playbook firewall.yml
```

{file}`firewall.yml` is a dispatcher.
Actual firewall code is in the {file}`firewalls` subdirectory and is platform-specific.
`ufw` is used for the Debian-family; `firewalld` is used for RedHat/CentOS.

The general firewall strategy is to block everything but the ports for ssh, http, https and munin-node.
The munin-node port is restricted to the monitor IP you specify.

```{note}
This strategy assumes that you're going to use ssh tunnelling if you need to connect to other ports.
```
