class plone {

    file { ['/home/vagrant/tmp',
            '/home/vagrant/.buildout',
            '/home/vagrant/buildout-cache',
            '/home/vagrant/buildout-cache/eggs',
            '/home/vagrant/buildout-cache/downloads',
            '/home/vagrant/buildout-cache/extends',
            '/home/vagrant/buildout-cache/Plone',]:
        ensure => directory,
        owner => 'vagrant',
        group => 'vagrant',
        mode => '0755',
    }

    file { '/home/vagrant/.buildout/default.cfg':
        ensure => present,
        content => inline_template('[buildout]
eggs-directory = /home/vagrant/training/buildout-cache/eggs
download-cache = /home/vagrant/training/buildout-cache/downloads
extends-cache = /home/vagrant/training/buildout-cache/extends'),
        owner => 'vagrant',
        group => 'vagrant',
        mode => '0664',
    }

    Exec {
        path => [
           '/usr/local/bin',
           '/opt/local/bin',
           '/usr/bin',
           '/usr/sbin',
           '/bin',
           '/sbin'],
        logoutput => true,
    }

    # Get the unified installer and unpack the buildout-cache
    exec {'wget https://launchpad.net/plone/4.3/4.3.3/+download/Plone-4.3.3-UnifiedInstaller.tgz':
        alias => "download_installer",
        creates => '/home/vagrant/tmp/Plone-4.3.3-UnifiedInstaller.tgz',
        cwd => '/home/vagrant/tmp',
        user => 'vagrant',
        group => 'vagrant',
        before => Exec["untar_installer"],
        timeout => 600,
    }

    exec {'tar xzf Plone-4.3.3-UnifiedInstaller.tgz':
        alias => "untar_installer",
        creates => '/home/vagrant/tmp/Plone-4.3.3-UnifiedInstaller',
        cwd => '/home/vagrant/tmp',
        user => 'vagrant',
        before => Exec["virtualenv"],
        timeout => 300,
    }

    exec {'virtualenv --no-site-packages py27':
        alias => "virtualenv",
        creates => '/home/vagrant/py27',
        user => 'vagrant',
        cwd => '/home/vagrant',
        before => Exec["install_plone"],
        timeout => 300,
    }

    exec {'/home/vagrant/tmp/Plone-4.3.3-UnifiedInstaller/install.sh standalone --with-python=/home/vagrant/py27/bin/python --password=admin --instance=zinstance --target=/home/vagrant/Plone':
        alias => "install_plone",
        creates => '/home/vagrant/Plone/zinstance/bin/buildout',
        user => 'vagrant',
        cwd => '/home/vagrant',
        before => Exec["copy_cache"],
        timeout => 0,
    }

    exec {'cp -Rf /home/vagrant/Plone/buildout-cache/* /home/vagrant/buildout-cache/':
        alias => "copy_cache",
        creates => '/home/vagrant/buildout-cache/eggs/Products.CMFPlone-4.3.3-py2.7.egg/',
        user => 'vagrant',
        cwd => '/home/vagrant',
        timeout => 0,
    }

}

include plone