class plone {

    $plone_version = "5.0.6"

    file { ['/home/vagrant/tmp',
            '/home/vagrant/.buildout',
            '/home/vagrant/buildout-cache',
            '/home/vagrant/buildout-cache/eggs',
            '/home/vagrant/buildout-cache/downloads',
            '/home/vagrant/buildout-cache/extends',
            ]:
        ensure => directory,
        owner => 'vagrant',
        group => 'vagrant',
        mode => '0755',
    }

    file { '/home/vagrant/.buildout/default.cfg':
        ensure => present,
        content => inline_template('[buildout]
eggs-directory = /home/vagrant/buildout-cache/eggs
download-cache = /home/vagrant/buildout-cache/downloads
extends-cache = /home/vagrant/buildout-cache/extends'),
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

    # Create virtualenv
    exec {'virtualenv --no-site-packages py27':
        alias => "virtualenv",
        creates => '/home/vagrant/py27',
        user => 'vagrant',
        cwd => '/home/vagrant',
        before => Exec["download_buildout_cache"],
        timeout => 300,
    }

    # Download the buildout-cache from dist.plone.org
    exec {"wget http://dist.plone.org/release/${plone_version}/buildout-cache.tar.bz2":
        alias => "download_buildout_cache",
        creates => "/home/vagrant/buildout-cache.tar.bz2",
        cwd => '/home/vagrant',
        user => 'vagrant',
        group => 'vagrant',
        before => Exec["unpack_buildout_cache"],
        timeout => 600,
    }

    # Unpack the buildout-cache to /home/vagrant/buildout-cache/
    exec {"tar xjf /home/vagrant/buildout-cache.tar.bz2":
        alias => "unpack_buildout_cache",
        creates => "/home/vagrant/buildout-cache/eggs/Products.CMFPlone-${plone_version}-py2.7.egg/",
        user => 'vagrant',
        cwd => '/home/vagrant',
        before => Exec["checkout_training"],
        timeout => 0,
    }

    # get training buildout
    exec {'git clone https://github.com/collective/training_buildout.git buildout && cd buildout && cd ..':
        alias => "checkout_training",
        creates => '/vagrant/buildout',
        user => 'vagrant',
        cwd => '/vagrant',
        before => Exec["bootstrap_training"],
        timeout => 0,
    }

    # bootstrap training buildout
    exec {'/home/vagrant/py27/bin/python bootstrap.py':
        alias => "bootstrap_training",
        creates => '/vagrant/buildout/bin/buildout',
        user => 'vagrant',
        cwd => '/vagrant/buildout',
        before => Exec["buildout_training"],
        timeout => 0,
    }

    # run training buildout
    exec {'/vagrant/buildout/bin/buildout -c vagrant_provisioning.cfg':
        alias => "buildout_training",
        creates => '/vagrant/buildout/bin/instance',
        user => 'vagrant',
        cwd => '/vagrant/buildout',
        # before => Exec["buildout_final"],
        timeout => 0,
    }

}

include plone
