---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(letsencrypt-certbot)=

# Let's Encrypt Certificates and certbot

All websites should use TLS.
We use an Ansible role that will automatically install [certbot](https://certbot.eff.org/), a free secure certificate from [Let's Encrypt](https://letsencrypt.org), and create a cron job that will automatically renew the certificate.

## Installation

You need to install the role.

```shell
cd ansible-playbook
git clone https://github.com/geerlingguy/ansible-role-certbot.git geerlingguy.certbot
```

## Configuration

To use the role, you need to add the following variables to your `local-configure.yml`, and substitute your values as needed.

```yaml
# https://github.com/geerlingguy/ansible-role-certbot#role-variables
# override roles/geerlingguy.certbot/defaults/main.yml
certbot_create_if_missing: true
certbot_admin_email: email@example.com
certbot_auto_renew_options: '--quiet --no-self-upgrade
--pre-hook "service nginx stop" --post-hook "service nginx start"'

certbot_certs:
  - domains:
    - "{{ inventory_hostname }}"

webserver_virtualhosts:
  - hostname: "{{ inventory_hostname }}"
    port: 80
    protocol: http
    extra: return 301 https://$server_name$request_uri;
  - hostname: "{{ inventory_hostname }}"
    default_server: yes
    zodb_path: /Plone
    address: 1.1.1.1
    port: 443
    protocol: https
    certificate:
      key: /etc/letsencrypt/live/{{ inventory_hostname }}/privkey.pem
      crt: /etc/letsencrypt/live/{{ inventory_hostname }}/fullchain.pem
```

The above configuration redirects all traffic from `http` to `https`, using the `extra` key mentioned in {ref}`web-hosting-options`.

```{seealso}
[Read documentation of the role geerlingguy.certbot](https://github.com/geerlingguy/ansible-role-certbot).
```
