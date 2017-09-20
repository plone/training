class plone {

    $plone_version = "5.0.6"

    file { ['/home/ubuntu/tmp',
            '/home/ubuntu/.buildout',
            '/home/ubuntu/buildout-cache',
            '/home/ubuntu/buildout-cache/eggs',
            '/home/ubuntu/buildout-cache/downloads',
            '/home/ubuntu/buildout-cache/extends',
            ]:
        ensure => directory,
        owner => 'ubuntu',
        group => 'ubuntu',
        mode => '0755',
    }

    file { '/home/ubuntu/.buildout/default.cfg':
        ensure => present,
        content => inline_template('[buildout]
eggs-directory = /home/ubuntu/buildout-cache/eggs
download-cache = /home/ubuntu/buildout-cache/downloads
extends-cache = /home/ubuntu/buildout-cache/extends'),
        owner => 'ubuntu',
        group => 'ubuntu',
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
        creates => '/home/ubuntu/py27',
        user => 'ubuntu',
        cwd => '/home/ubuntu',
        before => Exec["download_buildout_cache"],
        timeout => 300,
    }

    # Download the buildout-cache from dist.plone.org
    exec {"wget http://dist.plone.org/release/${plone_version}/buildout-cache.tar.bz2":
        alias => "download_buildout_cache",
        creates => "/home/ubuntu/buildout-cache.tar.bz2",
        cwd => '/home/ubuntu',
        user => 'ubuntu',
        group => 'ubuntu',
        before => Exec["unpack_buildout_cache"],
        timeout => 600,
    }

    # Unpack the buildout-cache to /home/ubuntu/buildout-cache/
    exec {"tar xjf /home/ubuntu/buildout-cache.tar.bz2":
        alias => "unpack_buildout_cache",
        creates => "/home/ubuntu/buildout-cache/eggs/Products.CMFPlone-${plone_version}-py2.7.egg/",
        user => 'ubuntu',
        cwd => '/home/ubuntu',
        before => Exec["checkout_training"],
        timeout => 0,
    }

    # get training buildout
    exec {'git clone https://github.com/collective/training_buildout.git buildout && cd buildout && cd ..':
        alias => "checkout_training",
        creates => '/vagrant/buildout',
        user => 'ubuntu',
        cwd => '/vagrant',
        before => Exec["bootstrap_training"],
        timeout => 0,
    }

    # bootstrap training buildout
    exec {'/home/ubuntu/py27/bin/python bootstrap.py':
        alias => "bootstrap_training",
        creates => '/vagrant/buildout/bin/buildout',
        user => 'ubuntu',
        cwd => '/vagrant/buildout',
        before => Exec["buildout_training"],
        timeout => 0,
    }

    # run training buildout
    exec {'/vagrant/buildout/bin/buildout -c vagrant_provisioning.cfg':
        alias => "buildout_training",
        creates => '/vagrant/buildout/bin/instance',
        user => 'ubuntu',
        cwd => '/vagrant/buildout',
        # before => Exec["buildout_final"],
        timeout => 0,
    }

}

include plone
